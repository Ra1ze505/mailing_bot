from loguru import logger
from telethon import TelegramClient, events

from src.containers.container import container
from src.domain.handlers.buttons import start_markup

container.gateways.logging_setup.init()  # type: ignore
logger.info("Configure bot...")
bot: TelegramClient = container.gateways.bot()
logger.info("Start handling...")


@bot.on(events.NewMessage(pattern="/start"))
async def start_handler(event: events.NewMessage.Event) -> None:
    use_case = container.use_cases.start_handler()
    await use_case(event)


@bot.on(events.NewMessage(pattern=r"Изменить\sгород$"))
async def change_city_handler(event: events.NewMessage.Event) -> None:
    async with bot.conversation(event.sender_id) as conv:
        use_case = container.use_cases.change_city()
        await use_case(event, conv)


@bot.on(events.NewMessage(pattern=r"Изменить\sвремя\sрассылки$"))
async def change_time_mailing_handler(event: events.NewMessage.Event) -> None:
    async with bot.conversation(event.sender_id) as conv:
        use_case = container.use_cases.change_time_mailing()
        await use_case(event, conv)


@bot.on(events.NewMessage(pattern=r"Погода$"))
async def weather_handler(event: events.NewMessage.Event) -> None:
    use_case = container.use_cases.weather_handler()
    await use_case(event)


@bot.on(events.CallbackQuery(pattern=r"weather_by_day"))
async def weather_by_day_handler(event: events.CallbackQuery.Event) -> None:
    use_case = container.use_cases.weather_by_day_handler()
    await use_case(event)


@bot.on(events.NewMessage(pattern=r"Курс$"))
async def rate_handler(event: events.NewMessage.Event) -> None:
    use_case = container.use_cases.rate_by_day()
    await use_case(event)


@bot.on(events.NewMessage(pattern=r"Новости$"))
async def news_handler(event: events.NewMessage.Event) -> None:
    use_case = container.use_cases.get_news_by_day()
    await use_case(event)


@bot.on(events.NewMessage(pattern=r"Написать\sнам$"))
async def write_us_handler(event: events.NewMessage.Event) -> None:
    async with bot.conversation(event.sender_id) as conv:
        use_case = container.use_cases.create_feedback()
        await use_case(event, conv)


@bot.on(events.NewMessage(pattern=r"О боте$"))
async def about_handler(event: events.NewMessage.Event) -> None:
    await event.respond(
        "Этот бот предназначен для получения новостей, погоды и курса валют.\n"
        "Код бота можно посмотреть [туть](https://github.com/Ra1ze505/mailing_bot)",
        buttons=start_markup,
    )
