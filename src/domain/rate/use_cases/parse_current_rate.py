from src.domain.rate.interfaces import IParseCurrentRate, IParseRateRepository, IRateRepository


class ParseCurrentRate(IParseCurrentRate):
    def __init__(self, parse_rate_repo: IParseRateRepository, rate_repo: IRateRepository) -> None:
        self.parse_rate_repo = parse_rate_repo
        self.rate_repo = rate_repo

    async def __call__(self) -> None:
        rate = await self.parse_rate_repo.get_rate()
        if rate is not None:
            await self.rate_repo.create(rate.dict())
