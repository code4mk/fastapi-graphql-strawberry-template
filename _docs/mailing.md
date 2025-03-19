# simple mailing

```python
from fastapi_pundra.common.mailer.mail import send_mail

await send_mail(
    subject="Hello, World!",
    to=["test@example.com"],
    template_name="welcome_email.html",
    context={"name": "John Doe"},
)
```

# background mailing

```python
from fastapi_pundra.common.mailer.mail import send_mail_background

await send_mail_background(
    background_tasks=background_tasks,
    subject="Hello, World!",
    to=["test@example.com"],
    template_name="welcome_email.html",
    context={"name": "John Doe"},
)
```

## routing tips

- if you want to send mail in background, you can use `background_tasks` in your route

```python
from fastapi import BackgroundTasks

@router.post("/users/registration")
@dto(UserCreateSchema)
async def registration(request: Request, background_tasks: BackgroundTasks) -> JSONResponse:
    ...
```

> note: background_tasks paramter will be after `request` parameter in your route

# queue mailing with celery

```python
from fastapi_pundra.common.mailer.task import send_email_queue_task

send_email_queue_task.delay(
    subject="Hello, World!",
    to=["test@example.com"],
    template_name="welcome_email.html",
    context={"name": "John Doe"},
)
```

# queue mailing with celery with countdown

```python
from fastapi_pundra.common.mailer.task import send_email_queue_task

send_email_queue_task.apply_async(
    args=[
        f"Welcome, {new_user.name or new_user.email}!",
        [new_user.email],
        template_name,
        context,
    ],
    countdown=120,
)
```