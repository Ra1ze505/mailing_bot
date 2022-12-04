from telethon import events

from src.domain.handlers.buttons import start_markup, weather_markup
from src.domain.handlers.interfaces import IWeatherHandler
from src.domain.user.interfaces import IGetOrCreateUser
from src.domain.weather.interfaces import IGetWeatherForecastPretty, IGetWeatherNowPretty


class WeatherHandler(IWeatherHandler):
    def __init__(
        self,
        get_weather_now_pretty: IGetWeatherNowPretty,
        get_or_create_user: IGetOrCreateUser,
    ):
        self.get_weather_now_pretty = get_weather_now_pretty
        self.get_or_create_user = get_or_create_user

    async def __call__(self, event: events.NewMessage.Event) -> None:
        user = await self.get_or_create_user(event)
        weather = await self.get_weather_now_pretty(user.city)
        await event.respond(weather, buttons=weather_markup)


class WeatherByDayHandler(IWeatherHandler):
    def __init__(
        self,
        get_weather_forecast_pretty: IGetWeatherForecastPretty,
        get_or_create_user: IGetOrCreateUser,
    ):
        self.get_weather_forecast_pretty = get_weather_forecast_pretty
        self.get_or_create_user = get_or_create_user

    async def __call__(self, event: events.CallbackQuery.Event) -> None:
        user = await self.get_or_create_user(event)
        weather = await self.get_weather_forecast_pretty(user.city)
        await event.respond(weather, buttons=start_markup)
