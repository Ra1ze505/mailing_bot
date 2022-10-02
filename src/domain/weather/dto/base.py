from pydantic import BaseModel, Field, validator

from src.common.utils import get_wind_direction

PRETTY_WEATHER_NOW_MESSAGE = """
**Погода в городе {city}:**
{description}
Температура: {temp}°C
Ветер {wind_direction}
Скорость ветра: {wind_speed} м/с
Влажность: {humidity}%
Облачность: {clouds_all}%
"""

PRETTY_WEATHER_MESSAGE = """
**Погода в городе {city}**
В течении дня:
-- Cредняя температура  {mean_temp}°C
-- Максимальная температура {max_temp}°C
-- Минимальная температура {min_temp}°C"""


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


class WeatherNowOutSchema(BaseModel):
    coord: CoordinatesSchema
    weather: list[WeatherSchema]
    base: str
    main: WeatherMainSchema
    visibility: int
    wind: WindSchema
    rain: dict | None = None
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
            wind_direction=get_wind_direction(self.wind.deg),
            wind_speed=int(self.wind.speed),
            humidity=int(self.main.humidity),
            clouds_all=int(self.clouds.get("all", 0)),
        )


class WeatherListSchema(BaseModel):
    dt: int
    main: WeatherMainSchema
    weather: list[WeatherSchema]
    clouds: dict
    wind: WindSchema
    visibility: int
    pop: float
    rain: dict | None = None
    sys: dict
    dt_txt: str


class WeatherByDaySchema(BaseModel):
    cod: str
    message: int
    cnt: int
    list: list[WeatherListSchema]
    city: dict

    def get_pretty_forecast(self) -> str:
        mean_temp = int(sum([item.main.temp for item in self.list]) / len(self.list))
        max_temp = int(max([item.main.temp for item in self.list]))
        min_temp = int(min([item.main.temp for item in self.list]))
        return PRETTY_WEATHER_MESSAGE.format(
            city=self.city["name"],
            mean_temp=mean_temp,
            max_temp=max_temp,
            min_temp=min_temp,
        )
