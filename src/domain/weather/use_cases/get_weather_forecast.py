from src.domain.weather.dto.base import WeatherForecastSchema
from src.domain.weather.interfaces import IGetWeatherForecast, IWeatherRepository


class GetWeatherForecast(IGetWeatherForecast):
    def __init__(self, weather_repo: IWeatherRepository):
        self.weather_repo = weather_repo

    async def __call__(self, city: str) -> WeatherForecastSchema:
        return await self.weather_repo.get_weather_forecast(city)
