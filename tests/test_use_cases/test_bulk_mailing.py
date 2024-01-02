import datetime
from typing import AsyncGenerator
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.containers.container import Container
from src.data.models import Users
from tests.conftest import BotMock
from tests.factories.news import NewsFactory
from tests.factories.rate import RateFactory
from tests.factories.user import UserFactory


@pytest.fixture(autouse=True)
async def weather_mock(container: Container) -> AsyncGenerator[BotMock, None]:
    mock = AsyncMock()
    output_mock = Mock()
    output_mock.get_pretty_forecast.return_value = "test"
    mock.return_value = output_mock
    with container.use_cases.get_weather_forecast.override(mock):
        yield mock


async def test_bulk_mailing(
    container: Container, bot_mock: BotMock, db_session: AsyncSession
) -> None:
    users: list[Users] = await UserFactory.create_batch(3)
    await UserFactory()
    await NewsFactory()
    await RateFactory()

    current_time = datetime.datetime.utcnow()
    time_mailing = datetime.time(hour=current_time.hour, minute=current_time.minute)
    for user in users:
        user.time_mailing = time_mailing
    use_case = container.use_cases.bulk_mailing()
    await use_case()
    assert [i[0] for i in bot_mock.sent_messages] == [user.id for user in users]
