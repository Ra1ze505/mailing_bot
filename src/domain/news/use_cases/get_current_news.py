from src.domain.news.dto.base import NewsOutSchema
from src.domain.news.interfaces import IGetCurrentNews, INewsRepository


class GetCurrentNews(IGetCurrentNews):
    def __init__(self, news_repository: INewsRepository):
        self.news_repository = news_repository

    async def __call__(self) -> NewsOutSchema:
        return await self.news_repository.get_last_news()
