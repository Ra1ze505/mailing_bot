import asyncio

from celery import Celery
from celery.schedules import crontab

from src.common.db import Database
from src.containers.container import container

container.gateways.logging_setup.init()  # type: ignore
app = container.gateways.celery()


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs: dict) -> None:
    sender.add_periodic_task(crontab(hour="*"), parse.s())
    sender.add_periodic_task(crontab(minute="*"), mailing.s())


@app.task()
def mailing() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_mailing())


async def _mailing() -> None:
    await container.init_resources()  # type: ignore
    db: Database = container.gateways.db()
    async with db.database_scope():
        bulk_mailing = await container.use_cases.bulk_mailing()
        await bulk_mailing()


@app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 5})
def parse() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_parse())


async def _parse() -> None:
    await container.init_resources()  # type: ignore
    db: Database = container.gateways.db()
    async with db.database_scope():
        parse_news = await container.use_cases.parse_last_news()
        parse_rate = container.use_cases.parse_current_rate()
        tasks = [parse_news(), parse_rate()]
        await asyncio.gather(*tasks)
