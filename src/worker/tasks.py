from asyncio import run

from celery import Celery
from celery.schedules import crontab

from src.common.start_up import on_startup
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
    sender.add_periodic_task(crontab(minute="*"), parse.s(), name="add every 5 minutes")


@app.task
def mailing() -> None:
    ...


@app.task
def parse() -> None:
    run(_parse())


async def _parse() -> None:
    await on_startup()
    use_case = await container.use_cases.parse_last_news()
    await use_case()
