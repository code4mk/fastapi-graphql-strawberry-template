import strawberry
from app.services.user_service import UserService
from app.graphql.users.user_gql_types import (
    UserRegisterInput,
    UserMutationResponse,
    UserLoginInput,
    LoginResponse,
    UserUpdateInput,
    UserDeleteInput,
    UserDeleteResponse,
)
from app.graphql.users.user_dto import UserRegisterDTO, UserLoginDTO, UserUpdateDTO, UserDeleteDTO
from strawberry.types import Info
from fastapi_pundra.gql_berry.validation import dto_validation
from app.database.database import get_db_session

@strawberry.type
class UserMutationResolvers:
    @strawberry.mutation
    @dto_validation(UserRegisterDTO)
    def user_registration(self, info: Info, user: UserRegisterInput) -> UserMutationResponse:
        """Register a new user."""
        db = next(get_db_session())
        try:
            user = UserService.s_user_registration(info, db, user)
            return user
        finally:
            db.close()

    @strawberry.mutation
    @dto_validation(UserLoginDTO)
    def user_login(self, info: Info, user: UserLoginInput) -> LoginResponse:
        """Login a user."""
        db = next(get_db_session())
        try:
            user = UserService.s_user_login(info, db, user)
            return user
        finally:
            db.close()

    @strawberry.mutation
    @dto_validation(UserUpdateDTO)
    def user_update(self, info: Info, user: UserUpdateInput) -> UserMutationResponse:
        """Update a user."""
        db = next(get_db_session())
        try:
            user = UserService.s_user_update(info, db, user)
            return user
        finally:
            db.close()

    @strawberry.mutation
    @dto_validation(UserDeleteDTO)
    def user_delete(self, info: Info, user: UserDeleteInput) -> UserDeleteResponse:
        """Delete a user."""
        db = next(get_db_session())
        try:
            user = UserService.s_user_delete(info, db, user)
            return user
        finally:
            db.close()
