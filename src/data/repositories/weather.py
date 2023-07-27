import httpx
from aiocache import cached

from src.common.exceptions.weather import WeatherException
from src.common.utils import serialize
from src.domain.weather.dto.base import WeatherForecastSchema, WeatherNowOutSchema
from src.domain.weather.interfaces import IWeatherRepository


class WeatherApiRepository(IWeatherRepository):

    base_url: str = "https://api.openweathermap.org/data/2.5/"

    def __init__(self, config: dict):
        self.api_key = config["api_key"]

    def _base_params(self) -> dict[str, str | int]:
        return {"units": "metric", "lang": "ru", "appid": self.api_key}

    @serialize
    @cached(ttl=60, noself=True)
    async def get_weather_now(self, city: str) -> WeatherNowOutSchema:
        params = self._base_params()
        params.update({"q": city})
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + "weather", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise WeatherException(response.text)

    @serialize
    @cached(ttl=120, noself=True)
    async def get_weather_forecast(self, city: str) -> WeatherForecastSchema:
        params = self._base_params()
        params.update(
            {
                "q": city,
                "cnt": 6,
            }
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + "forecast", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise WeatherException(response.text)
