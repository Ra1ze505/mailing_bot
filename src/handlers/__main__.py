from telethon import TelegramClient, events

from src.containers.container import container

container.gateways.logging_setup.init()  # type: ignore
bot: TelegramClient = container.gateways.bot()


@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event: events.NewMessage.Event) -> None:
    use_case = container.use_cases.start_handler()
    await use_case(event)


@bot.on(events.NewMessage(pattern=r"Изменить\sгород$"))
async def change_city_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"Изменить\sвремя\sрассылки$"))
async def change_time_mailing_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"Погода$"))
async def weather_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"Курс$"))
async def rate_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"Новости$"))
async def help_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"Написать\sнам$"))
async def write_us_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"О боте$"))
async def about_handler(event: events.NewMessage.Event) -> None:
    ...


# For run bot
with bot:
    bot.run_until_disconnected()
