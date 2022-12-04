import abc

from src.common.repo.interfaces import IBaseRepository
from src.domain.rate.dto.base import RateInSchema, RateOutSchema


class IParseRateRepository(abc.ABC):
    @abc.abstractmethod
    async def get_rate(self) -> RateInSchema | None:
        ...


class IRateRepository(IBaseRepository[RateOutSchema]):
    ...


class IParseCurrentRate(abc.ABC):
    @abc.abstractmethod
    async def __call__(self) -> None:
        ...
