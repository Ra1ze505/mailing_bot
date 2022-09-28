import copy
from typing import Generic, Protocol, Type, TypeVar

from pydantic import parse_obj_as
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from src.common.db import Base, Database
from src.common.dto.base import BaseOutputSchema
from src.common.exceptions.db import NotFoundException
from src.common.repo.interfaces import IBaseRepository, ModelType, SchemaOutType


class BaseRepository(IBaseRepository[SchemaOutType], Protocol[ModelType, SchemaOutType]):

    model: Type[ModelType]
    schema: Type[SchemaOutType]
    query: Select | None = None
    db: Database

    def __init__(self, db: Database):
        self.db = db

    @property
    def session(self) -> AsyncSession:
        return self.db.session

    def get_query(self) -> Select:
        query = self.query if self.query is not None else select(self.model)
        return copy.copy(query)

    async def create(self, data: dict) -> SchemaOutType:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()

        q = (
            self.get_query()
            .where(self.model.id == obj.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(q)
        obj = result.unique().scalars().one()

        return parse_obj_as(self.schema, obj)

    async def update(self, object_id: int, data: dict) -> SchemaOutType:
        q = self.get_query().where(self.model.id == object_id)
        result = await self.session.execute(q)
        try:
            obj = result.unique().scalars().one()
        except NoResultFound:
            raise NotFoundException

        for key, val in data.items():
            setattr(obj, key, val)

        self.session.add(obj)
        await self.session.commit()

        q = (
            self.get_query()
            .where(self.model.id == obj.id)
            .execution_options(populate_existing=True)
        )
        result = await self.session.execute(q)
        obj = result.unique().scalars().one()

        return parse_obj_as(self.schema, obj)

    async def get(self, obj_id: int) -> SchemaOutType:
        q = self.get_query().where(self.model.id == obj_id)
        result = await self.session.execute(q)
        try:
            obj = result.unique().scalars().one()
        except NoResultFound:
            raise NotFoundException

        return parse_obj_as(self.schema, obj)

    async def get_or_create(self, data: dict) -> SchemaOutType:
        try:
            return await self.get(data["id"])
        except NotFoundException:
            return await self.create(data)

    async def create_or_update(self, data: dict) -> SchemaOutType:
        try:
            return await self.update(data["id"], data)
        except NotFoundException:
            return await self.create(data)
