import abc

from telethon import events

from src.common.repo.interfaces import IBaseRepository
from src.data.models import User
from src.domain.user.dto.base import UserOutSchema


class IUserRepository(IBaseRepository[UserOutSchema]):
    ...


class IStartHandler(abc.ABC):
    def __init__(self, user_repo: IUserRepository, config: dict):
        self.user_repo = user_repo
        self.config = config

    @abc.abstractmethod
    async def __call__(self, event: events.NewMessage.Event) -> None:
        ...
