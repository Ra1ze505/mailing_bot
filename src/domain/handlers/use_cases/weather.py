from telethon import events

from src.domain.handlers.buttons import start_markup, weather_markup
from src.domain.handlers.interfaces import IWeatherHandler
from src.domain.user.interfaces import IGetOrCreateUser
from src.domain.weather.dto.base import WeatherForecastSchema
from src.domain.weather.interfaces import IGetWeatherForecast, IGetWeatherNow


class WeatherHandler(IWeatherHandler):
    def __init__(self, get_weather_now: IGetWeatherNow, get_or_create_user: IGetOrCreateUser):
        self.get_weather_now = get_weather_now
        self.get_or_create_user = get_or_create_user

    async def __call__(self, event: events.NewMessage.Event) -> None:
        user = await self.get_or_create_user(event)
        weather = await self.get_weather_now(user.city)
        await event.respond(weather.get_pretty_weather(), buttons=weather_markup)


class WeatherByDayHandler(IWeatherHandler):
    def __init__(
        self, get_weather_forecast: IGetWeatherForecast, get_or_create_user: IGetOrCreateUser
    ):
        self.get_weather_forecast = get_weather_forecast
        self.get_or_create_user = get_or_create_user

    async def __call__(self, event: events.CallbackQuery.Event) -> None:
        user = await self.get_or_create_user(event)
        weather: WeatherForecastSchema = await self.get_weather_forecast(user.city)
        await event.respond(weather.get_pretty_forecast(), buttons=start_markup)
