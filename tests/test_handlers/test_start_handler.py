from dependency_injector import containers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import User
from src.handlers.handlers import start_handler
from tests.factories.event import EventFactory


async def test_start_handler(
    container: containers.DeclarativeContainer,
    db_session: AsyncSession,
) -> None:
    event = EventFactory()
    await start_handler(event=event)

    stmt = select(User)
    result = (await db_session.execute(stmt)).scalars().all()
    assert len(result) == 1
    assert result[0].id == event.sender_id
    assert result[0].chat_id == event.chat_id
