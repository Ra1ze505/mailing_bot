from src.common.repo.base import BaseRepository
from src.data.models import FeedBack
from src.domain.user.dto.base import FeedBackOutSchema


class FeedBackRepository(BaseRepository):
    model = FeedBack
    schema = FeedBackOutSchema
