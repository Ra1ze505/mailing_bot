from telethon import TelegramClient

from src.domain.user.dto.base import UserOutSchema
from src.domain.weather.interfaces import IGetWeatherForecastPretty


class Mailing:
    def __init__(
        self,
        get_weather_forecast_pretty: IGetWeatherForecastPretty,
        bot: TelegramClient,
    ):
        self.get_weather_forecast_pretty = get_weather_forecast_pretty
        self.bot = bot

    async def __call__(self, to: UserOutSchema) -> None:
        weather = await self.get_weather_forecast_pretty(to.city)
        await self.bot.send_message(to.chat_id, weather)
