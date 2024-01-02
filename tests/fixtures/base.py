import asyncio
import pathlib
import sys
from asyncio import AbstractEventLoop
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, Generator

import pytest
from alembic import command
from alembic.config import Config
from alembic.script import Script, ScriptDirectory
from dependency_injector import providers
from pytest_async_sqlalchemy import create_database, drop_database
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, AsyncSessionTransaction, session
from sqlalchemy.orm import sessionmaker

from src.common.container import BaseAppContainer
from src.common.db import Base, Database
from src.config import PostgresConfig
from src.containers.container import container as app_container
from tests.async_alchemy_factory import AsyncSQLAlchemyModelFactory

db_config = PostgresConfig(db="test_database")


@pytest.fixture()
async def container() -> BaseAppContainer:
    return app_container


@pytest.fixture(scope="session")
def event_loop() -> Generator[AbstractEventLoop, None, None]:
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


def build_alembic_config(
    project_dir: pathlib.Path, database_url: str, migrations_dir: pathlib.Path
) -> Config:

    config = Config(project_dir / "alembic.ini")  # type: ignore
    config.set_main_option("sqlalchemy.url", database_url.replace("+asyncpg", ""))
    config.set_main_option("script_location", str(migrations_dir))
    return config


@pytest.fixture(scope="session")
def _database_url() -> str:
    return db_config.url


@pytest.fixture(scope="session")
def alembic_config(
    project_dir: pathlib.Path,
    database_url: str,
    migrations_dir: pathlib.Path,
) -> Config:
    return build_alembic_config(
        project_dir=project_dir,
        database_url=database_url,
        migrations_dir=migrations_dir,
    )


@pytest.fixture(scope="session", autouse=True)
async def database(
    migrate_to: str,
    database_url: str,
    alembic_config: Config,
) -> AsyncGenerator[str, None]:
    """
    Создание БД, применение миграций и удаление БД
    """
    try:
        await create_database(database_url)
        command.upgrade(alembic_config, migrate_to)
        yield database_url
    finally:
        await drop_database(database_url)


@pytest.fixture(scope="function")
def migrations_database_url(database_url: str) -> str:
    database_url += "migrations"
    return database_url


@pytest.fixture(scope="function")
def migrations_alembic_config(
    project_dir: pathlib.Path,
    migrations_database_url: str,
    migrations_dir: pathlib.Path,
) -> Config:
    return build_alembic_config(
        project_dir=project_dir,
        database_url=migrations_database_url,
        migrations_dir=migrations_dir,
    )


@pytest.fixture(scope="function")
async def migrations_database(
    project_dir: pathlib.Path,
    migrations_database_url: str,
    migrations_dir: pathlib.Path,
) -> AsyncGenerator[str, None]:
    try:
        await create_database(migrations_database_url)
        yield migrations_database_url
    finally:
        await drop_database(migrations_database_url)


@pytest.fixture(scope="function")
def migration_revisions(migrations_alembic_config: Config, migrate_to: str) -> list[Script]:
    revisions_dir = ScriptDirectory.from_config(migrations_alembic_config)
    revisions = list(revisions_dir.walk_revisions("base", migrate_to))
    revisions.reverse()
    return revisions


class MockDatabase:
    def __init__(self, session: AsyncSession):
        self.sess = session

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        yield self.sess

    @asynccontextmanager
    async def database_scope(self, **kwargs: Any) -> AsyncGenerator["MockDatabase", None]:
        yield self


@pytest.fixture()
async def db_session(sqla_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    connection = await sqla_engine.connect()
    trans = await connection.begin()

    Session = sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
    session = Session()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture(scope="session")
def init_database() -> Callable:
    return Base.metadata.create_all


@pytest.fixture(autouse=True)
def init_factories(db_session: AsyncSession) -> None:
    """Init factories."""
    AsyncSQLAlchemyModelFactory._session = db_session


@pytest.fixture(autouse=True)
async def override_session_in_container(
    db_session: AsyncEngine,
    container: BaseAppContainer,
) -> None:
    """Замена сессии в контейнере БД"""

    db = providers.Singleton(MockDatabase, db_session)
    if hasattr(container.gateways, "db"):
        container.gateways.db.override(db)
    elif hasattr(container.repos, "db"):
        container.repos.db.override(db)


@pytest.fixture()
async def db(_container: BaseAppContainer) -> Database:
    return _container.repos.db()
