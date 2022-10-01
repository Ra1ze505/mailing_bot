from src.domain.weather.dto.base import WeatherOutSchema
from src.domain.weather.interfaces import IGetWeatherNow, IWeatherRepository


class GetWeatherNow(IGetWeatherNow):
    def __init__(self, weather_repo: IWeatherRepository):
        self.weather_repo = weather_repo

    async def __call__(self, city: str) -> WeatherOutSchema:
        return await self.weather_repo.get_weather_now(city)
