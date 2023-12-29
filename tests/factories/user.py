import factory

from src.data.models import Users
from tests.async_alchemy_factory import AsyncSQLAlchemyModelFactory


class UserFactory(AsyncSQLAlchemyModelFactory):
    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f"username_{n}")
    chat_id = factory.Sequence(lambda n: n)
    city = factory.Sequence(lambda n: f"Город {n}")
    timezone = factory.Sequence(lambda n: n)

    class Meta:
        model = Users
