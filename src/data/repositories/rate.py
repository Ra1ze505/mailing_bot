from pydantic import parse_obj_as
from sqlalchemy import select

from src.common.repo.base import BaseRepository
from src.data.models.rate import Rate
from src.domain.rate.dto.base import RateOutSchema


class RateRepository(BaseRepository):

    model = Rate
    schema = RateOutSchema

    async def get_last_rate(self) -> RateOutSchema:
        stmt = select(self.model).order_by(self.model.date.desc()).limit(1)
        async with self.session_factory() as session:
            result = await session.execute(stmt)
            return parse_obj_as(self.schema, result.scalar_one())
