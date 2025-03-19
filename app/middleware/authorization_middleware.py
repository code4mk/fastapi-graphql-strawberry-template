# ruff: noqa

from collections.abc import Callable
from strawberry.types import Info
from strawberry.extensions import SchemaExtension
from jose import jwt
from graphql import GraphQLError
from fastapi_pundra.common.jwt_utils import decode_token
from app.config.authorization import AUTHORIZATION_ABLE_FIELDS


class AuthorizationError(GraphQLError):
    """Authorization error."""

    def __init__(self, message: str) -> None:
        """Initialize the authorization error."""
        super().__init__(
            message=message,
            extensions={
                "code": "UNAUTHORIZED",
                "category": "Authorization",
            },
        )


class AuthorizationMiddleware(SchemaExtension):
    """Authorization middleware."""

    def __init__(self) -> None:
        """Initialize the authorization middleware."""
        super().__init__()
        # Define fields that require authentication
        self.protected_fields = AUTHORIZATION_ABLE_FIELDS

    async def resolve(
        self,
        next_: Callable,
        root,
        info: Info,
        *args,
        **kwargs,
    ):
        request = info.context["request"]

        # Check if the current field requires authentication
        if info.field_name in self.protected_fields:
            auth_header = request.headers.get("Authorization")
            auth_error_message = "Authentication required. Please provide valid credentials."
            if not auth_header:
                raise AuthorizationError(auth_error_message)

            try:
                scheme, token = auth_header.split()

                if scheme.lower() != "bearer":
                    auth_error_message = "Invalid authentication scheme. Use 'Bearer' token."
                    raise AuthorizationError(auth_error_message)

                try:
                    request.state.user = decode_token(token)
                except jwt.JWTError as e:
                    auth_error_message = f"Invalid or expired token: {e!s}"
                    raise AuthorizationError(auth_error_message) from e
            except IndexError as e:
                auth_error_message = "Invalid authorization header format. Use 'Bearer <token>'"
                raise AuthorizationError(auth_error_message) from e

        result = next_(root, info, *args, **kwargs)
        return await result if hasattr(result, "__await__") else result
