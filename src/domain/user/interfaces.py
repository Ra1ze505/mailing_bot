import abc
from datetime import time

from telethon import events
from telethon.tl.custom import Conversation

from src.common.repo.interfaces import IBaseRepository
from src.domain.user.dto.base import FeedBackOutSchema, UserOutSchema


class IUserRepository(IBaseRepository[UserOutSchema]):
    @abc.abstractmethod
    async def get_by_sending_time(self, time_mailing: time) -> list[UserOutSchema]:
        ...

    @abc.abstractmethod
    async def filter_by_chat_ids(self, chat_ids: list[int]) -> list[UserOutSchema]:
        ...

    @abc.abstractmethod
    async def filter_by_usernames(self, usernames: list[str]) -> list[UserOutSchema]:
        ...

    @abc.abstractmethod
    async def get_all(self) -> list[UserOutSchema]:
        ...


class IGetOrCreateUser(abc.ABC):
    async def __call__(self, event: events.NewMessage.Event) -> UserOutSchema:
        ...


class IFeedBackRepository(IBaseRepository[FeedBackOutSchema]):
    ...


class ICreateFeedBack(abc.ABC):
    async def __call__(
        self, event: events.NewMessage.Event, conv: Conversation
    ) -> FeedBackOutSchema:
        ...
