from telethon import TelegramClient

from src.domain.user.dto.base import UserOutSchema
from src.domain.weather.dto.base import WeatherForecastSchema
from src.domain.weather.interfaces import IGetWeatherForecast


class Mailing:
    def __init__(self, get_weather_forecast: IGetWeatherForecast, bot: TelegramClient):
        self.get_weather_forecast = get_weather_forecast
        self.bot = bot

    async def __call__(self, to: UserOutSchema) -> None:
        weather: WeatherForecastSchema = await self.get_weather_forecast(to.city)
        msg = weather.get_pretty_forecast()
        await self.bot.send_message(to.chat_id, msg)
