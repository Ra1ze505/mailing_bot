from loguru import logger
from sqlalchemy.util import asyncio
from telethon import TelegramClient

from src.containers.container import container
from src.handlers.handlers import setup_handlers


async def run() -> None:
    bot: TelegramClient = await container.gateways.bot()
    await setup_handlers()

    # For run bot
    async with bot:
        await bot.run_until_disconnected()


container.gateways.logging_setup.init()  # type: ignore
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
