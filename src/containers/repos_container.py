from dependency_injector import containers, providers

from src.common.db import Database
from src.data.repositories.bot import BotRepository
from src.data.repositories.user import UserRepository
from src.data.repositories.weather import WeatherApiRepository
from src.domain.weather.interfaces import IWeatherRepository


class ReposContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db: providers.Provider[Database] = providers.Dependency()
    gateways = providers.DependenciesContainer()

    bot_repo = providers.Factory(BotRepository, bot=gateways.bot)
    weather: providers.Factory[IWeatherRepository] = providers.Factory(
        WeatherApiRepository, http_client=gateways.http_client, config=config.open_weather
    )
    user_repo = providers.Factory(UserRepository, db=db)
