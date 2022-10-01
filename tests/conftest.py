import pathlib
from typing import Generator

import pytest
from dependency_injector import containers
from faker import Faker

from src.containers.container import container as app_container

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
async def container() -> containers.DeclarativeContainer:
    return app_container


@pytest.fixture()
def faker() -> Faker:
    """Fixture that returns a seeded and suitable ``Faker`` instance."""
    fake = Faker(locale="ru_RU")
    return fake
