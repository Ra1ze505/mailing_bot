from typing import AsyncGenerator

from loguru import logger
from sqlalchemy import select, text
from telethon import TelegramClient
from telethon.sessions import StringSession

from src.common.db import Database
from src.data.models.bot_session import BotSession


async def get_session(db: Database) -> str | None:
    async with db.session() as db_session:
        stmt = select(BotSession)
        result: list[BotSession] = (await db_session.execute(stmt)).unique().scalars().all()
        if not result:
            return None

        return result[0].session


async def save_session(db: Database, session: str) -> None:
    async with db.session() as db_session:
        truncate_stmt = text(f"TRUNCATE TABLE {BotSession.__tablename__};")
        await db_session.execute(truncate_stmt)
        await db_session.commit()

        session_obj = BotSession(session=session)
        db_session.add(session_obj)
        await db_session.commit()


async def create_bot(config: dict, session: str | None = None) -> TelegramClient:
    return TelegramClient(
        StringSession(session), config.get("api_id"), config.get("api_hash")
    ).start(bot_token=config.get("token"))


async def init_bot(config: dict, db: Database) -> TelegramClient:
    session = await get_session(db)
    try:
        bot = await create_bot(config, session)
    except Exception as e:
        logger.warning(f"Failed create bot. Saved session {bool(session)}: {e}")
        bot = await create_bot(config)

    try:
        await save_session(db, bot.session.save())
    except Exception as e:
        logger.warning(f"Fail to save bot session: {e}")

    return bot


def init_parse_client(config: dict) -> AsyncGenerator[TelegramClient, None]:
    client = TelegramClient(
        StringSession(config.get("string_session")),
        config.get("api_id"),
        config.get("api_hash"),
    ).start()
    return client
