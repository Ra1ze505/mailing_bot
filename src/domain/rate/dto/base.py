from datetime import datetime

from pydantic import Field

from src.common.dto.base import BaseOutputSchema, OrmModel


class RateBaseSchema(OrmModel):
    id: int | None
    data: dict
    date: datetime | None


class RateInSchema(RateBaseSchema):
    data: dict = Field(..., alias="Valute")


class RateOutSchema(RateBaseSchema, BaseOutputSchema):
    ...

    @property
    def usd(self) -> float:
        return self.data["USD"]["Value"]

    @property
    def eur(self) -> float:
        return self.data["EUR"]["Value"]

    @property
    def pretty_rate(self) -> str:
        return f"**Курс валют на сегодня**\nДоллар: {self.usd}\nЕвро: {self.eur}"
