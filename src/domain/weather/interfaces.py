import abc

from src.domain.weather.dto.base import WeatherByDaySchema, WeatherNowOutSchema


class IWeatherRepository(abc.ABC):
    async def get_weather_now(self, city: str) -> WeatherNowOutSchema:
        ...

    async def get_weather_forecast(self, city: str) -> WeatherByDaySchema:
        ...


class IGetWeatherNow(abc.ABC):
    async def __call__(self, city: str) -> WeatherNowOutSchema:
        ...
