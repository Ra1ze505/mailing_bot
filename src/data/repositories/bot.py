from sqlalchemy import select
from telethon import TelegramClient

from src.common.db import Database
from src.data.models import User


class BotRepository:
    def __init__(self, db: Database, bot: TelegramClient):
        self.db = db
        self.bot = bot

    async def send_message(self, to: int, msg: str) -> None:
        await self.bot.send_message(to, msg)

    async def send_message_all(self, msg: str) -> None:
        stmt = select(User.chat_id)
        users_ids = (await self.db.session.execute(stmt)).scalars().all()
        for user_chat_id in users_ids:
            await self.bot.send_message(user_chat_id, msg)

    async def __aenter__(self) -> "BotRepository":
        await self.bot.start()
        return self

    async def __aexit__(self) -> None:
        await self.bot.disconnect()
