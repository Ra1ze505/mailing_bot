from telethon import TelegramClient

from src.common.db import Database
from src.domain.bot.interfaces import IBotRepository


class BotRepository(IBotRepository):
    def __init__(self, db: Database, bot: TelegramClient):
        self.bot = bot

    async def send_message(self, to: int, msg: str) -> None:
        await self.bot.send_message(to, msg)

    async def __aenter__(self) -> "BotRepository":
        await self.bot.start()
        return self

    async def __aexit__(self, *args: tuple, **kwargs: dict) -> None:
        await self.bot.disconnect()
