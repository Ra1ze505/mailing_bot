import factory

from src.data.models import News
from tests.async_alchemy_factory import AsyncSQLAlchemyModelFactory


class NewsFactory(AsyncSQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    content = factory.Faker("text")
    created_at = factory.Faker("date_time")

    class Meta:
        model = News
