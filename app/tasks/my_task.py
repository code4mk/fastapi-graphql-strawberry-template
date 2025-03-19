from celery import shared_task


@shared_task()
def my_task() -> None:
    """My task."""
    print("My task is running, pundra")  # noqa: T201
