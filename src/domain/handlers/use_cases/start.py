from telethon import events

from src.domain.handlers.interfaces import IStartHandler
from src.domain.user.dto.base import UserBaseSchema
from src.handlers.buttons import start_markup


class StartHandler(IStartHandler):
    async def __call__(self, event: events.NewMessage.Event) -> None:
        print("StartHandler")
        user = UserBaseSchema(
            id=event.sender_id,
            chat_id=event.chat_id,
        )
        await self.user_repo.get_or_create(user.dict())

        await event.respond(self.config["start_message"], buttons=start_markup)
