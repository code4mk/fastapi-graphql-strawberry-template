from fastapi_pundra.common.scheduler.celery import create_celery_app

app = create_celery_app(project_name="fastapi_app", broker_type="redis")

if __name__ == "__main__":
    app.start()
