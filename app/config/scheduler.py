from fastapi_pundra.common.scheduler.schedule import Schedule
from app.tasks.my_task import my_task

schedules = [Schedule().task(my_task).name("my-task-one").everyMinute()]
