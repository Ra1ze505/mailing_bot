from pydantic import BaseModel, Field, validator

from src.domain.utils import _get_wind_direction

PRETTY_WEATHER_NOW_MESSAGE = """
**Погода в городе {city}:**
{description}
Температура: {temp}°C
Ветер {wind_direction}
Скорость ветра: {wind_speed} м/с
Влажность: {humidity}%
Облачность: {clouds_all}%
"""


class CoordinatesSchema(BaseModel):
    lon: float
    lat: float


class WeatherSchema(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class WeatherMainSchema(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: int
    grnd_level: int


class WindSchema(BaseModel):
    speed: float
    deg: int
    gust: float


class WeatherOutSchema(BaseModel):
    coord: CoordinatesSchema
    weather: list[WeatherSchema]
    base: str
    main: WeatherMainSchema
    visibility: int
    wind: WindSchema
    rain: dict
    clouds: dict
    dt: int
    sys: dict
    timezone: int
    id: int
    name: str
    cod: int

    def get_pretty_weather(self) -> str:
        return PRETTY_WEATHER_NOW_MESSAGE.format(
            city=self.name,
            description=self.weather[0].description.title(),
            temp=int(self.main.temp),
            wind_direction=_get_wind_direction(self.wind.deg),
            wind_speed=int(self.wind.speed),
            humidity=int(self.main.humidity),
            clouds_all=int(self.clouds.get("all", 0)),
        )
