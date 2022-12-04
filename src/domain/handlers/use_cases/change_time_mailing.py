import datetime

from telethon import events
from telethon.tl.custom import Conversation

from src.domain.handlers.buttons import change_time_markup, start_markup
from src.domain.handlers.interfaces import IChangeTimeMailing
from src.domain.user.interfaces import IGetOrCreateUser, IUserRepository


class ChangeTimeMailing(IChangeTimeMailing):
    def __init__(self, user_repo: IUserRepository, get_or_create_user: IGetOrCreateUser):
        self.repository = user_repo
        self.get_or_create_user = get_or_create_user

    async def __call__(self, event: events.NewMessage.Event, conv: Conversation) -> None:
        user = await self.get_or_create_user(event)
        current_time_mailing = self._get_time_with_timezone(user.time_mailing, user.timezone)
        await conv.send_message(
            f"Ваше время рассылки: {current_time_mailing.strftime('%H:%M')}\n"
            "Напишите новое время в формате HH:MM",
            buttons=change_time_markup,
        )

        new_time_with_timezone = await self._get_time(conv)
        if new_time_with_timezone is None:
            return await conv.send_message("Время не изменено", buttons=start_markup)

        new_time = self._get_time_without_timezone(new_time_with_timezone, user.timezone)

        user = await self.repository.update(object_id=user.id, data={"time_mailing": new_time})

        new_current_time_mailing = self._get_time_with_timezone(user.time_mailing, user.timezone)
        return await conv.send_message(
            f"Время изменено на {new_current_time_mailing.strftime('%H:%M')}",
            buttons=start_markup,
        )

    async def _get_time(self, conv: Conversation) -> datetime.time | None:
        answer = await conv.get_response()
        if answer.text == "Отмена":
            return None
        try:
            time = datetime.datetime.strptime(answer.text, "%H:%M").time()
        except ValueError:
            await conv.send_message("Некорректное время\nПопробуйте еще раз")
            return await self._get_time(conv)
        return time

    def _get_time_with_timezone(self, time: datetime.time, timezone: int) -> datetime.time:
        time_hour = time.hour + timezone
        if time_hour > 23:
            time_hour -= 24
        elif time_hour < 0:
            time_hour += 24
        return datetime.time(time_hour, time.minute)

    def _get_time_without_timezone(self, time: datetime.time, timezone: int) -> datetime.time:
        time_hour = time.hour - timezone
        if time_hour > 23:
            time_hour -= 24
        elif time_hour < 0:
            time_hour += 24
        return datetime.time(time_hour, time.minute)
