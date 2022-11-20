import abc


class IBotRepository(abc.ABC):
    @abc.abstractmethod
    async def send_message(self, to: int, msg: str) -> None:
        ...

    @abc.abstractmethod
    async def __aenter__(self) -> "IBotRepository":
        ...

    @abc.abstractmethod
    async def __aexit__(self, *args: tuple, **kwargs: dict) -> None:
        ...
