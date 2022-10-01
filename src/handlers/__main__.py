from loguru import logger
from telethon import TelegramClient

from src.containers.container import container
from src.handlers.handlers import (
    about_handler,
    change_city_handler,
    change_time_mailing_handler,
    help_handler,
    rate_handler,
    start_handler,
    weather_handler,
    write_us_handler,
)

bot: TelegramClient = container.gateways.bot()


async def on_startup() -> None:
    await container.init_resources()  # type: ignore
    logger.info("Start bot")


loop = bot.loop
loop.run_until_complete(on_startup())

# For run bot
with bot:
    bot.run_until_disconnected()
