import abc

from telethon import events


class IStartHandler(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, event: events.NewMessage.Event) -> None:
        ...


class IWeatherHandler(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, event: events.NewMessage.Event) -> None:
        ...
