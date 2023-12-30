from typing import AsyncGenerator

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.celery import init_celery
from src.common.db import Database
from src.common.logging import setup_logging
from src.common.telegram_clients import init_bot, init_parse_client


async def get_session(db: Database) -> AsyncGenerator[AsyncSession, None]:
    try:
        sess = db.session
        yield sess
    finally:
        await sess.close()


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging_setup: providers.Provider[None] = providers.Resource(
        setup_logging, config=config.logger
    )
    db = providers.Singleton(Database, config.database)
    session = providers.Factory(get_session, db)
    bot = providers.Singleton(init_bot, config.bot)
    parse_client = providers.Singleton(init_parse_client, config.parse)
    celery = providers.Singleton(init_celery, config.broker.broker_url)
