import httpx
from telethon.extensions import html, markdown

from src.domain.bot.interfaces import IBotRepository


class BotRepositoryException(Exception):
    ...


class BotRepository(IBotRepository):
    def __init__(self, config: dict):
        api_token = config.get("token")
        self.base_url = f"https://api.telegram.org/bot{api_token}"

    async def send_message(self, to: int, msg: str) -> None:
        api_url = f"{self.base_url}/sendMessage"
        html_msg = html.unparse(*markdown.parse(msg))
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url,
                data={"chat_id": to, "text": html_msg, "parse_mode": "html"},
            )
            if response.status_code != 200:
                raise BotRepositoryException(response.text, response.status_code)
