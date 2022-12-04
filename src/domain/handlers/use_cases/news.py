from telethon import events

from src.domain.handlers.buttons import start_markup
from src.domain.handlers.interfaces import IGetNewsByDay
from src.domain.news.interfaces import IGetCurrentNews


class GetNewsByDay(IGetNewsByDay):
    def __init__(self, get_current_news: IGetCurrentNews):
        self.get_current_news = get_current_news

    async def __call__(self, event: events.NewMessage.Event) -> None:
        news = await self.get_current_news()
        await event.respond(news.content, buttons=start_markup)
