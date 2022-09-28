from typing import AsyncGenerator

from telethon import TelegramClient
from telethon.sessions import StringSession


def init_bot(config: dict) -> AsyncGenerator[TelegramClient, None]:
    bot = TelegramClient(StringSession(), config.get("api_id"), config.get("api_hash")).start(
        bot_token=config.get("token")
    )
    return bot
