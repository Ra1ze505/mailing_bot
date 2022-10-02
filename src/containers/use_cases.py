from dependency_injector import containers, providers

from src.domain.handlers.use_cases.start import StartHandler
from src.domain.handlers.use_cases.weather import WeatherByDayHandler, WeatherHandler
from src.domain.user.use_cases.get_or_create import GetOrCreateUser
from src.domain.weather.use_cases.get_weather_forecast import GetWeatherForecast
from src.domain.weather.use_cases.get_weather_now import GetWeatherNow


class UseCasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repos = providers.DependenciesContainer()

    get_or_create_user = providers.Factory(GetOrCreateUser, user_repo=repos.user_repo)
    get_weather_now = providers.Factory(GetWeatherNow, weather_repo=repos.weather)
    get_weather_forecast = providers.Factory(GetWeatherForecast, weather_repo=repos.weather)

    # Handlers
    start_handler = providers.Factory(
        StartHandler, get_or_create_user=get_or_create_user, config=config.app
    )
    weather_handler = providers.Factory(
        WeatherHandler, get_weather_now=get_weather_now, get_or_create_user=get_or_create_user
    )
    weather_by_day_handler = providers.Factory(
        WeatherByDayHandler,
        get_weather_forecast=get_weather_forecast,
        get_or_create_user=get_or_create_user,
    )
