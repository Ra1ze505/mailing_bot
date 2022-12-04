from src.common.exceptions.weather import WeatherException
from src.domain.weather.dto.base import CityWeather
from src.domain.weather.interfaces import IGetWeatherCity, IWeatherRepository


class GetWeatherCity(IGetWeatherCity):
    def __init__(self, weather_repo: IWeatherRepository):
        self.weather_repo = weather_repo

    async def __call__(self, city: str) -> CityWeather | None:
        try:
            weather = await self.weather_repo.get_weather_now(city)
        except WeatherException:
            return None
        return CityWeather(city=city, timezone=weather.timezone)
