import strawberry
from app.services.user_service import UserService
from app.graphql.users.user_gql_types import UserListResponse
from strawberry.types import Info


@strawberry.type
class UserQueryResolvers:
    @strawberry.field
    def users(self, info: Info, page: int = 1, per_page: int = 10) -> UserListResponse:
        """Get a list of users."""
        # Get the authenticated user from context
        # request = info.context["request"]
        # current_user = request.state.user
        # print(f"Current user: {current_user}")
        # print(f"Info: {info.context['request'].keys()}")

        return UserService.s_users(info, page=page, per_page=per_page)

    @strawberry.field
    def s_raw_sql_users(self, info: Info, page: int = 1, per_page: int = 10) -> UserListResponse:
        """Get a list of users."""
        return UserService.s_raw_sql_users(info, page=page, per_page=per_page)
