from datetime import datetime, time

from src.domain.bot.interfaces import IBotRepository
from src.domain.user.interfaces import IUserRepository
from src.domain.weather.interfaces import IGetWeatherForecastPretty


class BulkMailing:
    def __init__(
        self,
        user_repo: IUserRepository,
        get_weather_forecast_pretty: IGetWeatherForecastPretty,
        bot: IBotRepository,
    ):
        self.user_repo = user_repo
        self.get_weather_forecast_pretty = get_weather_forecast_pretty
        self.bot = bot

    async def __call__(self) -> None:
        time_now = datetime.now()
        users = await self.user_repo.get_by_sending_time(
            time(hour=time_now.hour, minute=time_now.minute)
        )
        async with self.bot as bot:
            for user in users:
                forecast = await self.get_weather_forecast_pretty(user.city)
                await bot.send_message(user.chat_id, forecast)
