from dependency_injector import containers, providers

from src.domain.handlers.use_cases.change_city import ChangeCity
from src.domain.handlers.use_cases.change_time_mailing import ChangeTimeMailing
from src.domain.handlers.use_cases.rate import RateByDay
from src.domain.handlers.use_cases.start import StartHandler
from src.domain.handlers.use_cases.weather import WeatherByDayHandler, WeatherHandler
from src.domain.mailing.use_cases.bulk_mailing import BulkMailing
from src.domain.mailing.use_cases.mailing import Mailing
from src.domain.news.use_cases.parse_last_news import ParseLastNews
from src.domain.rate.use_cases.get_current_rate import GetCurrentRate
from src.domain.rate.use_cases.parse_current_rate import ParseCurrentRate
from src.domain.user.use_cases.get_or_create import GetOrCreateUser
from src.domain.weather.use_cases.get_city_weather import GetWeatherCity
from src.domain.weather.use_cases.get_weather_forecast import (
    GetWeatherForecast,
    GetWeatherForecastPretty,
)
from src.domain.weather.use_cases.get_weather_now import GetWeatherNow, GetWeatherNowPretty


class UseCasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    repos = providers.DependenciesContainer()

    get_or_create_user = providers.Factory(GetOrCreateUser, user_repo=repos.user_repo)
    get_weather_now = providers.Factory(GetWeatherNow, weather_repo=repos.weather)
    get_weather_forecast = providers.Factory(GetWeatherForecast, weather_repo=repos.weather)
    get_weather_now_pretty = providers.Factory(GetWeatherNowPretty, get_weather_now=get_weather_now)
    get_weather_forecast_pretty = providers.Factory(
        GetWeatherForecastPretty, get_weather_forecast=get_weather_forecast
    )
    get_weather_city = providers.Factory(GetWeatherCity, weather_repo=repos.weather)

    get_current_rate = providers.Factory(GetCurrentRate, rate_repository=repos.rate_repo)

    mailing = providers.Factory(Mailing, bot=repos.bot_repo)
    bulk_mailing = providers.Factory(
        BulkMailing,
        user_repo=repos.user_repo,
        get_weather_forecast_pretty=get_weather_forecast_pretty,
        bot=repos.bot_repo,
    )

    # Parser
    parse_last_news = providers.Factory(
        ParseLastNews, parse_repo=repos.parse_news_repo, news_repo=repos.news_repo
    )
    parse_current_rate = providers.Factory(
        ParseCurrentRate,
        parse_rate_repo=repos.parse_rate_repo,
        rate_repo=repos.rate_repo,
    )

    # Handlers
    start_handler = providers.Factory(
        StartHandler, get_or_create_user=get_or_create_user, config=config.app
    )
    weather_handler = providers.Factory(
        WeatherHandler,
        get_weather_now_pretty=get_weather_now_pretty,
        get_or_create_user=get_or_create_user,
    )
    weather_by_day_handler = providers.Factory(
        WeatherByDayHandler,
        get_weather_forecast=get_weather_forecast,
        get_or_create_user=get_or_create_user,
    )
    change_city = providers.Factory(
        ChangeCity,
        get_or_create_user=get_or_create_user,
        get_weather_city=get_weather_city,
        user_repo=repos.user_repo,
    )
    change_time_mailing = providers.Factory(
        ChangeTimeMailing,
        get_or_create_user=get_or_create_user,
        user_repo=repos.user_repo,
    )
    rate_by_day = providers.Factory(RateByDay, get_current_rate=get_current_rate)
