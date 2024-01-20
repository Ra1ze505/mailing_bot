import httpx
from pydantic import HttpUrl, parse_obj_as
from telethon import TelegramClient

from src.domain.news.dto.base import NewsInSchema
from src.domain.rate.dto.base import RateInSchema


class ParseNewsRepository:
    def __init__(self, parse_client: TelegramClient, config: dict) -> None:
        self.parse_client = parse_client
        self.news_channel = config.get("news_channel")
        self.key_word = config.get("key_word")

    async def parse_last_message(self) -> NewsInSchema:  # type: ignore
        chat = await self.parse_client.get_entity(self.news_channel)
        async for message in self.parse_client.iter_messages(chat, search=self.key_word):
            return parse_obj_as(NewsInSchema, message)


class ParseRateRepository:
    def __init__(
        self,
        api_url: HttpUrl,
    ):
        self.api_url = api_url

    async def get_rate(self) -> RateInSchema | None:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.api_url)
            if response.status_code == 200:
                return parse_obj_as(RateInSchema, response.json())
        return None
