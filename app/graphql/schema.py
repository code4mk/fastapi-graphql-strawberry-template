import strawberry
from strawberry.schema.config import StrawberryConfig
from app.middleware.authorization_middleware import AuthorizationMiddleware
from fastapi_pundra.gql_berry.strawberry_resolver_utils import (
    load_resolver_class,
    discover_resolvers,
)
from app.middleware.rate_limit_middleware import RateLimitMiddleware

# Discover query and mutation resolver paths
query_resolver_paths, mutation_resolver_paths = discover_resolvers()

# Dynamically load all resolver classes
query_resolver_classes = [load_resolver_class(path) for path in query_resolver_paths]
mutation_resolver_classes = [load_resolver_class(path) for path in mutation_resolver_paths]


@strawberry.type
class Query(*query_resolver_classes):
    pass


@strawberry.type
class Mutation(*mutation_resolver_classes):
    pass


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    config=StrawberryConfig(auto_camel_case=False),
    extensions=[
        AuthorizationMiddleware(),
        RateLimitMiddleware(),
    ],
)
