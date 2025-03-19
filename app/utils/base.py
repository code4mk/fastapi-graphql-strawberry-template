from datetime import datetime


def datetime_now() -> datetime:
    """Get the current datetime in UTC."""
    return datetime.now(tz=datetime.UTC)
