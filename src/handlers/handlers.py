from telethon import TelegramClient, events

from src.containers.container import container

bot: TelegramClient = container.gateways.bot()


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
    use_case = await container.use_cases.weather_handler()
    await use_case(event)


@bot.on(events.CallbackQuery(pattern=r"weather_by_day"))
async def weather_by_day_handler(event: events.CallbackQuery.Event) -> None:
    use_case = await container.use_cases.weather_by_day_handler()
    await use_case(event)


@bot.on(events.NewMessage(pattern=r"Курс$"))
async def rate_handler(event: events.NewMessage.Event) -> None:
    use_case = container.use_cases.rate_by_day()
    await use_case(event)


@bot.on(events.NewMessage(pattern=r"Новости$"))
async def help_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"Написать\sнам$"))
async def write_us_handler(event: events.NewMessage.Event) -> None:
    ...


@bot.on(events.NewMessage(pattern=r"О боте$"))
async def about_handler(event: events.NewMessage.Event) -> None:
    ...
