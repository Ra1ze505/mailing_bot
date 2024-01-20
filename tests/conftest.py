import pathlib
from typing import AsyncGenerator, Generator

import pytest
from faker import Faker

from src.common.container import BaseAppContainer
from src.containers.container import Container
from src.containers.container import container as app_container
from src.domain.bot.interfaces import IBotRepository

pytest_plugins = ("tests.fixtures.base",)


@pytest.fixture(scope="session")
def project_dir() -> Generator[pathlib.Path, None, None]:
    yield pathlib.Path(__file__).resolve().parent.parent.absolute()


@pytest.fixture(scope="session")
def migrations_dir() -> Generator[pathlib.Path, None, None]:
    yield pathlib.Path(__file__).resolve().parent.parent.absolute() / "src/data/database/migrations"


@pytest.fixture(scope="session")
def migrate_to() -> Generator[str, None, None]:
    yield "head"


@pytest.fixture()
async def container() -> BaseAppContainer:
    return app_container


@pytest.fixture()
def faker() -> Faker:
    """Fixture that returns a seeded and suitable ``Faker`` instance."""
    fake = Faker(locale="ru_RU")
    return fake


class BotMock(IBotRepository):
    def __init__(self) -> None:
        self.sent_messages: list[tuple[int, str]] = []

    async def send_message(self, to: int, msg: str) -> None:
        self.sent_messages.append((to, msg))


@pytest.fixture(autouse=True)
async def bot_mock(container: Container) -> AsyncGenerator[BotMock, None]:
    mock = BotMock()
    with container.repos.bot_repo.override(mock):
        yield mock
