import abc


class IBotRepository(abc.ABC):
    @abc.abstractmethod
    async def send_message(self, to: int, msg: str) -> None:
        ...
