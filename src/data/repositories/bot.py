import httpx

from src.domain.bot.interfaces import IBotRepository


class BotRepositoryException(Exception):
    ...


class BotRepository(IBotRepository):
    def __init__(self, config: dict):
        api_token = config.get("token")
        self.base_url = f"https://api.telegram.org/bot{api_token}"

    async def send_message(self, to: int, msg: str) -> None:
        api_url = f"{self.base_url}/sendMessage"
        async with httpx.AsyncClient() as client:
            response = await client.post(
                api_url, data={"chat_id": to, "text": msg, "parse_mode": "MarkdownV2"}
            )
            if response.status_code != 200:
                raise BotRepositoryException(response.text, response.status_code)
