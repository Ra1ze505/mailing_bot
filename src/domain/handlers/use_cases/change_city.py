from telethon import events
from telethon.tl.custom import Conversation

from src.domain.handlers.buttons import change_city_markup, start_markup
from src.domain.user.interfaces import IGetOrCreateUser, IUserRepository
from src.domain.weather.dto.base import CityWeather
from src.domain.weather.interfaces import IGetWeatherCity


class ChangeCity:
    def __init__(
        self,
        get_or_create_user: IGetOrCreateUser,
        get_weather_city: IGetWeatherCity,
        user_repo: IUserRepository,
    ):
        self.get_or_create_user = get_or_create_user
        self.get_weather_city = get_weather_city
        self.user_repo = user_repo

    async def __call__(self, event: events.NewMessage.Event, conv: Conversation) -> None:
        user = await self.get_or_create_user(event)
        await conv.send_message(
            f"Ваш город сейчас: {user.city}\nНапишите свой город",
            buttons=change_city_markup,
        )

        new_city = await self._get_city(conv)
        if new_city is None:
            return await conv.send_message("Город не изменен", buttons=start_markup)

        user.city = new_city.city
        user.timezone = new_city.timezone
        await self.user_repo.update(
            object_id=user.id, data={"city": user.city, "timezone": user.timezone}
        )

        return await conv.send_message(f"Город изменен на {user.city}", buttons=start_markup)

    async def _get_city(self, conv: Conversation) -> CityWeather | None:
        answer = await conv.get_response()
        if answer.text == "Отмена":
            return None
        city = await self.get_weather_city(answer.text)
        if city:
            return city
        else:
            await conv.send_message("Некорректный город\nПопробуйте еще раз")
            return await self._get_city(conv)
