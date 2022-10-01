from telethon import events

from src.domain.handlers.interfaces import IWeatherHandler
from src.domain.user.interfaces import IGetOrCreateUser
from src.domain.weather.interfaces import IGetWeatherNow


class WeatherHandler(IWeatherHandler):
    def __init__(self, get_weather_now: IGetWeatherNow, get_or_create_user: IGetOrCreateUser):
        self.get_weather_now = get_weather_now
        self.get_or_create_user = get_or_create_user

    async def __call__(self, event: events.NewMessage.Event) -> None:
        user = await self.get_or_create_user(event)
        weather = await self.get_weather_now(user.city)
        await event.respond(weather.get_pretty_weather())
