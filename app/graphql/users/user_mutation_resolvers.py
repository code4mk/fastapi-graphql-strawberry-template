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


@strawberry.type
class UserMutationResolvers:
    @strawberry.mutation
    @dto_validation(UserRegisterDTO)
    def user_registration(self, info: Info, user: UserRegisterInput) -> UserMutationResponse:
        """Register a new user."""
        user = UserService.s_user_registration(info, user)
        return user

    @strawberry.mutation
    @dto_validation(UserLoginDTO)
    def user_login(self, info: Info, user: UserLoginInput) -> LoginResponse:
        """Login a user."""
        user = UserService.s_user_login(info, user)
        return user

    @strawberry.mutation
    @dto_validation(UserUpdateDTO)
    def user_update(self, info: Info, user: UserUpdateInput) -> UserMutationResponse:
        """Update a user."""
        user = UserService.s_user_update(info, user)
        return user

    @strawberry.mutation
    @dto_validation(UserDeleteDTO)
    def user_delete(self, info: Info, user: UserDeleteInput) -> UserDeleteResponse:
        """Delete a user."""
        user = UserService.s_user_delete(info, user)
        return user
