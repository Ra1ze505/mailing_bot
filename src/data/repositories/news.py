from pydantic import parse_obj_as
from sqlalchemy import select

from src.common.repo.base import BaseRepository
from src.data.models import News
from src.domain.news.dto.base import NewsOutSchema


class NewsRepository(BaseRepository):
    model = News
    schema = NewsOutSchema

    async def get_last_news(self) -> NewsOutSchema:
        stmt = select(self.model).order_by(self.model.created_at.desc()).limit(1)
        async with self.session_factory() as session:
            result = await session.execute(stmt)
            return parse_obj_as(self.schema, result.scalar_one())
