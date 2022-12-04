from src.domain.rate.dto.base import RateOutSchema
from src.domain.rate.interfaces import IGetCurrentRate, IRateRepository


class GetCurrentRate(IGetCurrentRate):
    def __init__(self, rate_repository: IRateRepository):
        self.rate_repository = rate_repository

    async def __call__(self) -> RateOutSchema:
        return await self.rate_repository.get_last_rate()
