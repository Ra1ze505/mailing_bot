from dependency_injector import containers, providers

from src.common.db import Database
from src.common.logging import setup_logging
from src.common.telegram_clients import init_bot, init_parse_client


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    logging_setup: providers.Provider[None] = providers.Resource(
        setup_logging, config=config.logger
    )
    db = providers.Singleton(Database, config.database)
    bot = providers.Singleton(init_bot, config.bot)
    parse_client = providers.Singleton(init_parse_client, config.parse)
