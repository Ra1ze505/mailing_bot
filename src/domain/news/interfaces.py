import abc

from src.common.repo.interfaces import IBaseRepository
from src.domain.news.dto.base import NewsInSchema, NewsOutSchema


class INewsRepository(IBaseRepository[NewsOutSchema]):
    ...


class IParseNewsRepository(abc.ABC):
    @abc.abstractmethod
    async def parse_last_message(self) -> NewsInSchema:
        ...


class IParseLastNews(abc.ABC):
    async def __call__(self) -> None:
        ...
