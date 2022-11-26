import logging

from sqlalchemy.exc import IntegrityError

from src.domain.news.interfaces import INewsRepository, IParseLastNews, IParseNewsRepository


class ParseLastNews(IParseLastNews):
    def __init__(self, parse_repo: IParseNewsRepository, news_repo: INewsRepository) -> None:
        self.parse_repository = parse_repo
        self.news_repository = news_repo

    async def __call__(self) -> None:
        message = await self.parse_repository.parse_last_message()
        try:
            await self.news_repository.create(message.dict())
        except IntegrityError:
            logging.info("News already exists")
