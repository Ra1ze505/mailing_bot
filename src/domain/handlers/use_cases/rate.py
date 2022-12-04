from telethon import events

from src.domain.handlers.buttons import start_markup
from src.domain.handlers.interfaces import IRateByDay
from src.domain.rate.interfaces import IGetCurrentRate


class RateByDay(IRateByDay):
    def __init__(self, get_current_rate: IGetCurrentRate):
        self.get_current_rate = get_current_rate

    async def __call__(self, event: events.CallbackQuery.Event) -> None:
        rate = await self.get_current_rate()
        await event.respond(rate.pretty_rate, buttons=start_markup)
