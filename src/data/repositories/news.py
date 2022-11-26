from src.common.repo.base import BaseRepository
from src.data.models import News
from src.domain.news.dto.base import NewsOutSchema


class NewsRepository(BaseRepository):
    model = News
    schema = NewsOutSchema
