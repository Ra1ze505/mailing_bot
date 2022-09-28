import abc
from typing import Generic, Protocol, Type, TypeVar

from sqlalchemy.sql import Select

from src.common.db import Base, Database
from src.common.dto.base import BaseOutputSchema

SchemaOutType = TypeVar("SchemaOutType", bound=BaseOutputSchema)
ModelType = TypeVar("ModelType", bound=Base)


class IBaseRepository(Protocol[SchemaOutType]):

    schema: Type[SchemaOutType]
    query: Select | None = None

    async def create(self, data: dict) -> SchemaOutType:
        ...

    async def update(self, object_id: int, data: dict) -> SchemaOutType:
        ...

    async def get(self, obj_id: int) -> SchemaOutType:
        ...

    async def get_or_create(self, data: dict) -> SchemaOutType:
        ...

    async def create_or_update(self, data: dict) -> SchemaOutType:
        ...
