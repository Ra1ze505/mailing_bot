import re
import uuid
from contextlib import asynccontextmanager
from contextvars import ContextVar
from typing import Any, AsyncGenerator, Union, cast

from sqlalchemy import MetaData, Table
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import as_declarative, declared_attr, sessionmaker


class Database:
    """Этот класс реализует работу со scoped_session, через Contextvar.
    Для использования сессий в рамках одного http запроса должна использоваться одна сессия базы
    данных. За исключением конкурентных операций со вставкой данных, тогда для каждой задачи asyncio
    должна обеспечена своя сессия базы данных, для предотвращения коллизий.
    В иных вариантах использования бд (таких как работа с очередями сообщений или ci команд) scope
    сессии определяется в зависимости от условий выполнения.
    """

    def __init__(self, config: dict) -> None:
        self.current_context: ContextVar[str] = ContextVar("current_context", default="")
        engine: AsyncEngine = create_async_engine(config["url"])

        self.session_factory = sessionmaker(
            autoflush=config["autoflush"],
            autocommit=config["autocommit"],
            expire_on_commit=config["expire_on_commit"],
            class_=AsyncSession,
            bind=engine,
        )

        self.scoped_session = async_scoped_session(self.session_factory, self._scopefunc)

    def _scopefunc(self) -> str | None:
        scope_str = self.current_context.get()
        return scope_str

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        sess = self.scoped_session()
        try:
            yield sess
        except Exception:
            await sess.rollback()
            raise
        finally:
            await sess.close()

    @asynccontextmanager
    async def database_scope(self, **kwargs: Any) -> AsyncGenerator["Database", None]:
        """Создайте новый scope сессии базы данных (область действия).
        Это создает новую сессию базы данных для обработки всех подключений из одного scope (запрос
        или процесс). Этот метод обычно должен вызываться только в middleware или в начале рабочих
        процессов.
        Args:
            ``**kwargs``: Необязательные kwargs для session
        """
        token = self.current_context.set(str(uuid.uuid4()))
        self.scoped_session(**kwargs)
        try:
            yield self
        finally:
            await self.scoped_session.remove()
            self.current_context.reset(token)


def camel_to_snake(came_str: str) -> str:
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", came_str)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


@as_declarative()
class Base:
    id: Union[int, uuid.UUID]
    metadata: MetaData

    __table__: Table

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # Для корректной работы mypy
        pass

    @declared_attr
    def __tablename__(cls) -> str:  # noqa
        return camel_to_snake(cls.__name__)

    __mapper_args__ = {"eager_defaults": True}
