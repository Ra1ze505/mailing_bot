from pydantic import parse_obj_as
from telethon import TelegramClient

from src.domain.news.dto.base import NewsInSchema


class ParseNewsRepository:
    def __init__(self, parse_client: TelegramClient, config: dict) -> None:
        self.parse_client = parse_client
        self.news_channel = config.get("news_channel")
        self.key_word = config.get("key_word")

    async def parse_last_message(self) -> NewsInSchema:  # type: ignore
        chat = await self.parse_client.get_entity(self.news_channel)
        async for message in self.parse_client.iter_messages(chat, search=self.key_word):
            return parse_obj_as(NewsInSchema, message)
