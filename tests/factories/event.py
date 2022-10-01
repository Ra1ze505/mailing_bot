from typing import Any, Callable

from faker import Faker


class EventFactory:
    def __init__(
        self,
        sender_id: int | None = None,
        message: str | None = None,
        chat_id: int | None = None,
        respond: Callable | None = None,
    ):
        fake = Faker(locale="ru_RU")
        self.sender_id = fake.pyint() if sender_id is None else sender_id
        self.message = fake.pystr() if message is None else message
        self.chat_id = fake.pyint() if chat_id is None else chat_id
        self._respond = self._default_respond if respond is None else respond

    async def respond(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> Callable:
        return await self._respond(*args, **kwargs)

    async def _default_respond(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        return None
