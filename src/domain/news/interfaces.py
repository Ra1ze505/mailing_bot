import abc

from src.common.repo.interfaces import IBaseRepository
from src.domain.news.dto.base import NewsInSchema, NewsOutSchema


class INewsRepository(IBaseRepository[NewsOutSchema]):
    @abc.abstractmethod
    async def get_last_news(self) -> NewsOutSchema:
        ...


class IParseNewsRepository(abc.ABC):
    @abc.abstractmethod
    async def parse_last_message(self) -> NewsInSchema:
        ...


class IParseLastNews(abc.ABC):
    @abc.abstractmethod
    async def __call__(self) -> None:
        ...


class IGetCurrentNews(abc.ABC):
    @abc.abstractmethod
    async def __call__(self) -> NewsOutSchema:
        ...
