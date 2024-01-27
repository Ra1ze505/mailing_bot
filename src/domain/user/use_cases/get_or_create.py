from telethon import events

from src.domain.user.dto.base import UserInSchema, UserOutSchema
from src.domain.user.interfaces import IUserRepository


class GetOrCreateUser:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def __call__(self, event: events.NewMessage.Event) -> UserOutSchema:
        user = UserInSchema(
            id=event.sender_id,
            username=event.sender.username or "",
            chat_id=event.chat_id,
        )
        return await self.user_repo.get_or_create(user.dict())
