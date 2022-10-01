from telethon import events

from src.domain.handlers.interfaces import IStartHandler
from src.domain.user.dto.base import UserBaseSchema
from src.domain.user.interfaces import IGetOrCreateUser
from src.handlers.buttons import start_markup


class StartHandler(IStartHandler):
    def __init__(self, get_or_create_user: IGetOrCreateUser, config: dict):
        self.get_or_create_user = get_or_create_user
        self.config = config

    async def __call__(self, event: events.NewMessage.Event) -> None:
        await self.get_or_create_user(event)
        await event.respond(self.config["start_message"], buttons=start_markup)
