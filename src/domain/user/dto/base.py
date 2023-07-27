import datetime

from pydantic import Field

from src.common.dto.base import BaseOutputSchema, OrmModel


class UserBaseSchema(OrmModel):
    id: int = Field(..., description="Идентификатор пользователя")
    username: str = Field(..., description="Имя пользователя")
    chat_id: int = Field(..., description="Идентификатор чата")
    city: str = Field("Москва", description="Город")


class UserOutSchema(UserBaseSchema, BaseOutputSchema):
    time_mailing: datetime.time = Field(..., description="Время рассылки")
    timezone: int = Field(..., discription="Временная зона")


class UserInSchema(UserBaseSchema):
    ...
