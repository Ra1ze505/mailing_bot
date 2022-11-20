import datetime
from typing import AsyncGenerator
from unittest.mock import AsyncMock, Mock

import pytest

from src.containers.container import Container
from src.data.models import User
from src.domain.bot.interfaces import IBotRepository
from tests.factories.user import UserFactory


class BotMock(IBotRepository):
    def __init__(self) -> None:
        self.sent_messages: list[tuple[int, str]] = []
        self.entered = False

    async def send_message(self, to: int, msg: str) -> None:
        if self.entered:
            self.sent_messages.append((to, msg))

    async def __aenter__(self) -> "BotMock":
        self.entered = True
        return self

    async def __aexit__(self, *args: tuple, **kwargs: dict) -> None:
        self.entered = False


@pytest.fixture(autouse=True)
async def bot_mock(container: Container) -> AsyncGenerator[BotMock, None]:
    mock = BotMock()
    with container.repos.bot_repo.override(mock):
        yield mock


@pytest.fixture(autouse=True)
async def weather_mock(container: Container) -> AsyncGenerator[BotMock, None]:
    mock = AsyncMock()
    output_mock = Mock()
    output_mock.get_pretty_forecast.return_value = "test"
    mock.return_value = output_mock
    with container.use_cases.get_weather_forecast.override(mock):
        yield mock


async def test_bulk_mailing(container: Container, bot_mock: BotMock) -> None:
    users: list[User] = await UserFactory.create_batch(3)
    current_time = datetime.datetime.now()
    time_mailing = datetime.time(hour=current_time.hour, minute=current_time.minute)
    for user in users:
        user.time_mailing = time_mailing
    use_case = container.use_cases.bulk_mailing()
    await use_case()
    assert bot_mock.sent_messages == [(user.id, "test") for user in users]
