from typing import Any, AsyncGenerator

from telethon import TelegramClient
from telethon.sessions import StringSession


def init_bot(config: dict) -> AsyncGenerator[TelegramClient, None]:
    bot = TelegramClient(StringSession(), config.get("api_id"), config.get("api_hash")).start(
        bot_token=config.get("token")
    )
    return bot


def init_parse_client(config: dict) -> AsyncGenerator[TelegramClient, None]:
    client = TelegramClient(
        StringSession(config.get("string_session")),
        config.get("api_id"),
        config.get("api_hash"),
    ).start()
    return client
