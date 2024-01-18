from datetime import datetime, time

from src.domain.bot.interfaces import IBotRepository
from src.domain.news.interfaces import IGetCurrentNews
from src.domain.rate.interfaces import IGetCurrentRate
from src.domain.user.interfaces import IUserRepository
from src.domain.weather.interfaces import IGetWeatherForecastPretty

MESSAGE = "{forecast}\n\n{rate}\n\n{news}\nпроверочка"


class BulkMailing:
    def __init__(
        self,
        user_repo: IUserRepository,
        get_weather_forecast_pretty: IGetWeatherForecastPretty,
        bot: IBotRepository,
        get_current_news: IGetCurrentNews,
        get_current_rate: IGetCurrentRate,
    ):
        self.user_repo = user_repo
        self.get_weather_forecast_pretty = get_weather_forecast_pretty
        self.bot = bot
        self.get_current_news = get_current_news
        self.get_current_rate = get_current_rate

    async def __call__(self) -> None:
        time_now = datetime.utcnow()
        users = await self.user_repo.get_by_sending_time(
            time(hour=time_now.hour, minute=time_now.minute)
        )
        last_news = await self.get_current_news()
        rate = await self.get_current_rate()
        async with self.bot as bot:
            for user in users:
                forecast = await self.get_weather_forecast_pretty(user.city)
                await bot.send_message(
                    user.chat_id,
                    MESSAGE.format(
                        forecast=forecast, rate=rate.pretty_rate, news=last_news.content
                    ),
                )
