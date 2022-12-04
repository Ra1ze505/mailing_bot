import abc

from telethon import events
from telethon.tl.custom import Conversation


class IStartHandler(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, event: events.NewMessage.Event) -> None:
        ...


class IWeatherHandler(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, event: events.NewMessage.Event) -> None:
        ...


class IChangeCity(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, event: events.NewMessage.Event, conv: Conversation) -> None:
        ...


class IChangeTimeMailing(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, event: events.NewMessage.Event, conv: Conversation) -> None:
        ...
