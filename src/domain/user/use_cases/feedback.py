from loguru import logger
from telethon import events
from telethon.tl.custom import Conversation

from src.domain.bot.interfaces import IBotRepository
from src.domain.user.dto.base import FeedBackInSchema, FeedBackOutSchema, UserOutSchema
from src.domain.user.interfaces import ICreateFeedBack, IFeedBackRepository
from src.domain.user.use_cases.get_or_create import GetOrCreateUser

ADMIN_NOTIFICATION_MESSAGE: str = "Новое сообщение от @{username}:\n\n{message}"


class CreateFeedBack(ICreateFeedBack):
    def __init__(
        self,
        get_or_create_user: GetOrCreateUser,
        feedback_repo: IFeedBackRepository,
        bot_repo: IBotRepository,
        admin_tg_id: int,
    ):
        self.get_or_create_user: GetOrCreateUser = get_or_create_user
        self.feedback_repo = feedback_repo
        self.bot_repo = bot_repo
        self.admin_tg_id = admin_tg_id

    async def __call__(
        self, event: events.NewMessage.Event, conv: Conversation
    ) -> FeedBackOutSchema:
        user: UserOutSchema = await self.get_or_create_user(event)
        await conv.send_message("Внимательно слушаю 😊")
        answer = await conv.get_response()
        fb = FeedBackInSchema(user_id=user.id, message=answer.text)
        feedback = await self.feedback_repo.create(fb.dict())
        try:
            await self.bot_repo.send_message(
                self.admin_tg_id,
                ADMIN_NOTIFICATION_MESSAGE.format(username=user.username, message=feedback.message),
            )
        except Exception as e:
            logger.warning(f"Error when try send feedback for admin: {e}")
        finally:
            await conv.send_message("Спасибо за отзыв!")
            return feedback
