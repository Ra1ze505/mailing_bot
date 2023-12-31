from dataclasses import dataclass
from typing import Any, Callable

from faker import Faker


class EventFactory:
    def __init__(
        self,
        sender_id: int | None = None,
        username: str | None = None,
        message: str | None = None,
        chat_id: int | None = None,
        respond: Callable | None = None,
    ):
        fake = Faker(locale="ru_RU")
        self.sender_id = fake.pyint() if sender_id is None else sender_id
        self.username = fake.user_name() if username is None else username
        self.message = fake.pystr() if message is None else message
        self.chat_id = fake.pyint() if chat_id is None else chat_id
        self._respond = self._default_respond if respond is None else respond
        self.messages: list = list()

    async def respond(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        return await self._respond(*args, **kwargs)

    async def _default_respond(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        self.messages.append((args, kwargs))
        return None

    @property
    def sender(self) -> "EventFactory":
        return self


@dataclass
class Response:
    text: str = ""


class ConversationFactory:
    def __init__(self, event: EventFactory, get_response: Callable | None = None) -> None:
        self.event = event
        self._get_response = self._default_get_respond if get_response is None else get_response

    async def send_message(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        await self.event.respond(*args, **kwargs)

    async def get_response(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> Any:
        return await self._get_response(*args, **kwargs)

    async def _default_get_respond(self, *args: tuple[Any], **kwargs: dict[str, Any]) -> Response:
        return Response()
