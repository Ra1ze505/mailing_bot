from datetime import datetime

from pydantic import BaseModel, Field

from src.common.dto.base import BaseOutputSchema, OrmModel


class NewsBaseSchema(OrmModel):
    id: int
    content: str
    created_at: datetime


class NewsOutSchema(NewsBaseSchema, BaseOutputSchema):
    ...


class NewsInSchema(NewsBaseSchema):
    created_at: datetime = Field(..., alias="date")
    content: str = Field(..., alias="message")
