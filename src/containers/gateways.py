from dependency_injector import containers, providers
from httpx import AsyncClient

from src.common.bot import init_bot
from src.common.celery import init_celery
from src.common.db import Database
from src.common.http_client import init_async_http_client
from src.common.logging import setup_logging
from src.common.scheduler import init_scheduler


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging_setup: providers.Provider[None] = providers.Resource(
        setup_logging, config=config.logger
    )
    http_client: providers.Provider[AsyncClient] = providers.Resource(
        init_async_http_client,
        base_url="",
    )
    db = providers.Singleton(Database, config.database)
    bot = providers.Singleton(init_bot, config.bot)
    scheduler = providers.Singleton(init_scheduler)
    celery = providers.Singleton(init_celery, config.broker.broker_url)
