from src.common.exceptions.weather import WeatherException
from src.domain.weather.dto.base import WeatherForecastSchema
from src.domain.weather.interfaces import (
    IGetWeatherForecast,
    IGetWeatherForecastPretty,
    IWeatherRepository,
)


class GetWeatherForecast(IGetWeatherForecast):
    def __init__(self, weather_repo: IWeatherRepository):
        self.weather_repo = weather_repo

    async def __call__(self, city: str) -> WeatherForecastSchema | None:
        try:
            return await self.weather_repo.get_weather_forecast(city)
        except WeatherException:
            return None


class GetWeatherForecastPretty(IGetWeatherForecastPretty):
    def __init__(self, get_weather_forecast: IGetWeatherForecast):
        self.get_weather_forecast = get_weather_forecast

    async def __call__(self, city: str) -> str:
        weather = await self.get_weather_forecast(city)
        if weather is None:
            return "Не удалось получить прогноз погоды, попробуйте позже"
        return weather.get_pretty_forecast()
