from celery import Celery
from celery.schedules import crontab

from src.containers.container import container

container.gateways.logging_setup.init()  # type: ignore
app = container.gateways.celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs: dict) -> None:

    sender.add_periodic_task(
        crontab(minute="*"),
        mailing.s(),
        name="add every minute",
    )


@app.task
def mailing() -> None:
    ...
