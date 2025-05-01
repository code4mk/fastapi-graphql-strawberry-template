import strawberry
from app.services.user_service import UserService
from app.graphql.users.user_gql_types import UserListResponse
from strawberry.types import Info
from app.database.database import get_db_session

@strawberry.type
class UserQueryResolvers:
    @strawberry.field
    def users(self, info: Info, page: int = 1, per_page: int = 10) -> UserListResponse:
        """Get a list of users."""
        db = next(get_db_session())
        try:
            return UserService.s_users(info, db=db, page=page, per_page=per_page)
        finally:
            db.close()

    @strawberry.field
    def s_raw_sql_users(self, info: Info, page: int = 1, per_page: int = 10) -> UserListResponse:
        """Get a list of users."""
        db = next(get_db_session())
        try:
            return UserService.s_raw_sql_users(info, db=db, page=page, per_page=per_page)
        finally:
            db.close()
