import strawberry
import uuid
from datetime import datetime
from fastapi_pundra.gql_berry import pydantic_experimental
from app.graphql.users.user_dto import UserRegisterDTO, UserUpdateDTO, UserLoginDTO, UserDeleteDTO
from fastapi_pundra.gql_berry.common_gql_type import PaginatedList


@strawberry.type(description="User type")
class UserData:
    id: uuid.UUID
    email: str
    first_name: str | None
    last_name: str | None = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    @strawberry.field()
    def full_name(self) -> str:
        """Get the full name of the user."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.first_name:
            return self.first_name
        if self.last_name:
            return self.last_name
        return ""


#############################
# Mutation related types
#############################


@pydantic_experimental.input(
    model=UserRegisterDTO, all_fields=True, description="Input type for registering a new user"
)
class UserRegisterInput:
    pass


@pydantic_experimental.input(
    model=UserLoginDTO, all_fields=True, description="Input type for login a user"
)
class UserLoginInput:
    pass


@pydantic_experimental.input(
    model=UserUpdateDTO, all_fields=True, description="Input type for updating a user"
)
class UserUpdateInput:
    pass


@pydantic_experimental.input(
    model=UserDeleteDTO, all_fields=True, description="Input type for deleting a user"
)
class UserDeleteInput:
    pass


###########################
# Response related types
###########################


@strawberry.type(description="Response type for user registration")
class UserMutationResponse:
    user: UserData
    message: str


@strawberry.type(description="Response type for user login")
class LoginResponse:
    access_token: str
    refresh_token: str
    token_type: str
    user: UserData


@strawberry.type(description="Response type for listing users")
class UserListResponse(PaginatedList[UserData]):
    pass


@strawberry.type(description="Response type for deleting a user")
class UserDeleteResponse:
    message: str
