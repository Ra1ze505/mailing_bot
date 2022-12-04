from src.common.exceptions.weather import WeatherException
from src.domain.weather.dto.base import WeatherNowOutSchema
from src.domain.weather.interfaces import IGetWeatherNow, IGetWeatherNowPretty, IWeatherRepository


class GetWeatherNow(IGetWeatherNow):
    def __init__(self, weather_repo: IWeatherRepository):
        self.weather_repo = weather_repo

    async def __call__(self, city: str) -> WeatherNowOutSchema | None:
        try:
            return await self.weather_repo.get_weather_now(city)
        except WeatherException:
            return None


class GetWeatherNowPretty(IGetWeatherNowPretty):
    def __init__(self, get_weather_now: IGetWeatherNow):
        self.get_weather_now = get_weather_now

    async def __call__(self, city: str) -> str:
        weather = await self.get_weather_now(city)
        if weather is None:
            return "Не удалось получить погоду, попробуйте позже"
        return weather.get_pretty_weather()
