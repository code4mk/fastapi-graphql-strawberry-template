from app.graphql.users.user_gql_types import (
    UserData,
    UserMutationResponse,
    LoginResponse,
    UserListResponse,
    UserDeleteResponse,
)
from app.graphql.users.user_dto import UserRegisterDTO, UserLoginDTO, UserUpdateDTO, UserDeleteDTO
from datetime import datetime
from fastapi_pundra.gql_berry.exception import NotFoundError, DuplicateError
from app.database.database import get_db
from strawberry.types import Info
from app.models.user import User
from fastapi_pundra.common.password import generate_password_hash, compare_hashed_password
from fastapi_pundra.common.jwt_utils import create_access_token, create_refresh_token
from fastapi_pundra.gql_berry.pagination import paginate
from fastapi_pundra.common.mailer.mail import send_mail_background
from fastapi_pundra.common.raw_sql.utils import (
    load_sql_file,
    raw_sql_fetch_all,
    raw_sql_paginate_gql,
)
import uuid


class UserService:
    """User service."""

    def __init__(self) -> None:
        """Initialize the user service."""
        self.db = get_db()

    def __del__(self) -> None:
        """Close the database session when the service is destroyed."""
        self.db.close()

    @classmethod
    async def s_user_registration(cls, info: Info, data: UserRegisterDTO) -> UserMutationResponse:
        """Register a new user."""
        self = cls()

        retrieved_user = self.db.query(User).filter(User.email == data.email).first()
        if retrieved_user:
            error_message = f"User with email {data.email} already exists"
            raise DuplicateError(error_message)

        try:
            new_user = User()
            new_user.email = data.email
            new_user.password = generate_password_hash(data.password)
            new_user.first_name = data.first_name
            new_user.last_name = data.last_name
            new_user.is_active = True
            # new_user.created_at = datetime.now()
            # new_user.updated_at = datetime.now()

            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            # Send welcome email in background
            template_name = "welcome_email.html"
            context = {
                "name": new_user.first_name or new_user.email,
                "activation_link": f"{info.context['request'].base_url}api/v1/users/activate",
            }

            background_tasks = info.context["background_tasks"]

            await send_mail_background(
                background_tasks=background_tasks,
                subject=f"Welcome, {new_user.first_name or new_user.email}!",
                to=[new_user.email],
                template_name=template_name,
                context=context,
            )

            return UserMutationResponse(user=new_user, message="User registered successfully")
        except Exception:
            self.db.rollback()
            raise

    @classmethod
    def s_user_login(cls, info: Info, data: UserLoginDTO) -> LoginResponse:
        """Login a user."""
        self = cls()  # Create instance to use the managed db session

        user = self.db.query(User).filter(User.email == data.email).first()
        if not user:
            error_message = "Your email or password is incorrect"
            raise NotFoundError(error_message)

        if not compare_hashed_password(data.password, user.password):
            error_message = "Your email or password is incorrect"
            raise NotFoundError(error_message)

        # Create a clean dict with only the needed user data
        user_data = {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
        }

        access_token = create_access_token(user_data)
        refresh_token = create_refresh_token(user_data)

        return LoginResponse(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer", user=user
        )

    @classmethod
    def s_users(cls, info: Info, page: int = 1, per_page: int = 10) -> UserListResponse:
        """Get a list of users."""
        self = cls()

        query = self.db.query(User)

        # Example of adding additional data
        def get_additional_data(users: dict) -> dict:
            """Get additional data."""
            return {
                "total_active_users": sum(1 for user in users if user.is_active),
                "total_inactive_users": sum(1 for user in users if not user.is_active),
            }

        output = paginate(query, page, per_page, additional_data=get_additional_data)

        return UserListResponse(**output)

    @classmethod
    def s_raw_sql_users(cls, info: Info, page: int = 1, per_page: int = 10) -> UserListResponse:
        """Get a list of users."""
        self = cls()

        the_sql_content = load_sql_file("users.fetch-all-users")
        result = self.db.execute(the_sql_content)
        users_list = raw_sql_fetch_all(result)
        paginated_data = raw_sql_paginate_gql(users_list, the_page=page, the_per_page=per_page)

        # Convert dictionary data to UserData objects
        user_data_objects = [
            UserData(
                id=uuid.UUID(user["id"]),
                email=user["email"],
                first_name=user["first_name"] or None,
                last_name=user["last_name"] or None,
                is_active=bool(user["is_active"]),
                created_at=datetime.fromisoformat(user["created_at"])
                if user["created_at"]
                else None,
                updated_at=datetime.fromisoformat(user["updated_at"])
                if user["updated_at"]
                else None,
            )
            for user in paginated_data["data"]
        ]

        # Create the response with converted data
        response_data = {"data": user_data_objects, "pagination": paginated_data["pagination"]}

        return UserListResponse(**response_data)

    @classmethod
    def s_user_update(cls, info: Info, data: UserUpdateDTO) -> UserMutationResponse:
        """Update a user."""
        self = cls()

        user = self.db.query(User).filter(User.id == data.id).first()
        if not user:
            error_message = f"User with id {data.id} not found"
            raise NotFoundError(error_message)

        if data.first_name:
            user.first_name = data.first_name

        if data.last_name:
            user.last_name = data.last_name

        if data.is_active:
            user.is_active = data.is_active

        user.updated_at = datetime.now()  # noqa: DTZ005

        self.db.commit()
        self.db.refresh(user)

        return UserMutationResponse(user=user, message="User updated successfully")

    @classmethod
    def s_user_delete(cls, info: Info, data: UserDeleteDTO) -> UserDeleteResponse:
        """Delete a user."""
        self = cls()

        user = self.db.query(User).filter(User.id == data.user_id).first()
        if not user:
            error_message = f"User with id {data.user_id} not found"
            raise NotFoundError(error_message)

        self.db.delete(user)
        self.db.commit()

        return UserDeleteResponse(message="User deleted successfully")
