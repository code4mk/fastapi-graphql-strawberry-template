# List of GraphQL fields that require authorization checks before execution.
AUTHORIZATION_ABLE_FIELDS = [
    # Query fields
    "users",
    "s_raw_sql_users",
    # Mutation fields
    "user_update",
    "user_delete",
]
