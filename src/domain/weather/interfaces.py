import abc

from src.domain.weather.dto.base import WeatherOutSchema


class IWeatherRepository(abc.ABC):
    async def get_weather_now(self, city: str) -> WeatherOutSchema:
        ...


class IGetWeatherNow(abc.ABC):
    async def __call__(self, city: str) -> WeatherOutSchema:
        ...
