from datetime import time

from pydantic import parse_obj_as
from sqlalchemy import select

from src.common.repo.base import BaseRepository
from src.data.models import User
from src.domain.user.dto.base import UserOutSchema


class UserRepository(BaseRepository):
    model = User
    schema = UserOutSchema

    async def get_by_sending_time(self, time_mailing: time) -> list[UserOutSchema]:
        stmt = select(self.model).where(self.model.time_mailing == time_mailing)
        result = (await self.db.session.execute(stmt)).scalars().all()
        return [parse_obj_as(self.schema, obj) for obj in result]
