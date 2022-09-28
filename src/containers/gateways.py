from dependency_injector import containers, providers

from src.common.bot import init_bot
from src.common.db import Database


class Gateways(containers.DeclarativeContainer):
    config = providers.Configuration()

    db = providers.Singleton(Database, config.database)
    bot = providers.Singleton(init_bot, config.bot)
