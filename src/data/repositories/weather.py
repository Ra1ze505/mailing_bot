from aiocache import cached
from httpx import AsyncClient

from src.common.utils import serialize
from src.domain.weather.dto.base import WeatherForecastSchema, WeatherNowOutSchema
from src.domain.weather.interfaces import IWeatherRepository


class WeatherApiRepository(IWeatherRepository):

    base_url: str = "https://api.openweathermap.org/data/2.5/"

    def __init__(self, http_client: AsyncClient, config: dict):
        self.http_client = http_client
        self.api_key = config["api_key"]

    def _base_params(self) -> dict[str, str | int]:
        return {"units": "metric", "lang": "ru", "appid": self.api_key}

    @serialize
    @cached(ttl=60, noself=True)
    async def get_weather_now(self, city: str) -> WeatherNowOutSchema:
        params = self._base_params()
        params.update(
            {
                "q": city,
            }
        )
        response = await self.http_client.get(self.base_url + "weather", params=params)
        return response.json()

    @serialize
    @cached(ttl=60, noself=True)
    async def get_weather_forecast(self, city: str) -> WeatherForecastSchema:
        params = self._base_params()
        params.update(
            {
                "q": city,
                "cnt": 6,
            }
        )
        response = await self.http_client.get(self.base_url + "forecast", params=params)
        return response.json()
