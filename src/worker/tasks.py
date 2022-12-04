import asyncio

from celery import Celery
from celery.schedules import crontab

from src.containers.container import container

container.gateways.logging_setup.init()  # type: ignore
app = container.gateways.celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs: dict) -> None:

    # sender.add_periodic_task(
    #     crontab(minute="*"),
    #     mailing.s(),
    #     name="add every minute",
    # )
    sender.add_periodic_task(crontab(minute="*"), parse.s())


@app.task
def mailing() -> None:
    ...


@app.task
def parse() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_parse())


async def _parse() -> None:
    parse_news = await container.use_cases.parse_last_news()
    parse_rate = container.use_cases.parse_current_rate()
    tasks = [parse_news(), parse_rate()]
    await asyncio.gather(*tasks)
