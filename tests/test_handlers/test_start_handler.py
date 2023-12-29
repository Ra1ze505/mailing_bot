from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.container import BaseAppContainer
from src.data.models import Users
from src.domain.handlers.interfaces import IStartHandler
from tests.factories.event import EventFactory


async def test_start_handler(
    container: BaseAppContainer,
    db_session: AsyncSession,
) -> None:
    event = EventFactory()
    use_case: IStartHandler = container.use_cases.start_handler()
    await use_case(event=event)

    stmt = select(Users)
    result = (await db_session.execute(stmt)).scalars().all()
    assert len(result) == 1
    assert result[0].id == event.sender_id
    assert result[0].chat_id == event.chat_id
