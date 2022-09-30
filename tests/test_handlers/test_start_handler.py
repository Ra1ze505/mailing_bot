from typing import Any

from dependency_injector import containers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import User
from src.handlers.handlers import start_handler


async def test_start_handler(
    container: containers.DeclarativeContainer,
    db_session: AsyncSession,
) -> None:
    async def respond(*args: tuple[Any], **kwargs: dict[str, Any]) -> None:
        ...

    event = type("Event", (), {"sender_id": 1, "message": "test", "chat_id": 1, "respond": respond})
    await start_handler(event=event())

    stmt = select(User)
    result = (await db_session.execute(stmt)).scalars().all()
    print(result[0].id)
