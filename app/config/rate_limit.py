RATE_LIMIT_CONFIG = {
    # Maximum number of requests allowed within the time window
    "rate_max": 3,
    # Time window in seconds for rate limiting (e.g., 3 requests per 60 seconds)
    "rate_seconds": 60,
    # Maximum depth of nested queries allowed to prevent deep recursive queries
    "depth_max": 50,
    # Maximum number of total resolver calls allowed in a single request
    "call_max": 500,
    # List of types to apply rate limiting to (currently only users)
    "type_name": ["users"],
}
