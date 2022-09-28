from src.common.repo.base import BaseRepository
from src.data.models import User
from src.domain.user.dto.base import UserBaseSchema


class UserRepository(BaseRepository):
    model = User
    schema = UserBaseSchema
