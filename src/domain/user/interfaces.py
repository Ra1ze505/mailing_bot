import abc

from telethon import events

from src.common.repo.interfaces import IBaseRepository
from src.data.models import User
from src.domain.user.dto.base import UserOutSchema


class IUserRepository(IBaseRepository[UserOutSchema]):
    ...


class IGetOrCreateUser(abc.ABC):
    async def __call__(self, event: events.NewMessage.Event) -> UserOutSchema:
        ...
