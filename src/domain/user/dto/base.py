import datetime

from pydantic import BaseModel, Field

from src.common.dto.base import BaseOutputSchema, OrmModel


class UserBaseSchema(OrmModel):
    id: int = Field(..., description="Идентификатор пользователя")
    chat_id: int = Field(..., description="Идентификатор чата")
    city: str | None = Field(None, description="Город")
    timezone: int | None = Field(None, discription="Временная зона")
    time_mailing: datetime.time | None = Field(None, description="Время рассылки")


class UserOutSchema(UserBaseSchema, BaseOutputSchema):
    ...
