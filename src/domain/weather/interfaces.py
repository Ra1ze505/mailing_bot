import abc

from src.domain.weather.dto.base import WeatherNowOutSchema


class IWeatherRepository(abc.ABC):
    async def get_weather_now(self, city: str) -> WeatherNowOutSchema:
        ...


class IGetWeatherNow(abc.ABC):
    async def __call__(self, city: str) -> WeatherNowOutSchema:
        ...
