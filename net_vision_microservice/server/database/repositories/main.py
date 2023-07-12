import uuid

import sqlalchemy as sa

from abc import ABC
from typing import TypeVar, Generic, Optional, Union, Sequence, Type, Any

from sqlalchemy.ext.asyncio import AsyncSession

from net_vision_microservice.server.database.models.main import DatabaseBase

Model = TypeVar("Model", bound=DatabaseBase)
Id = Union[int, uuid.UUID]


class Repository(ABC, Generic[Model]):

    def __init__(self, model: Type[Model], session: AsyncSession):
        self._model = model
        self._session = session

    async def _read_by_id(self, id: Id) -> Optional[Model]:
        return await self._session.get(self._model, id)

    async def _read_all(self, limit: Optional[int] = None) -> Sequence[Model]:
        stmt = sa.select(self._model)

        if limit is not None:
            stmt = stmt.limit(limit)

        result: sa.ScalarResult[Model] = await self._session.scalars(stmt)

        return result.all()

    async def _delete(self, *args: Any) -> Optional[Model]:
        stmt = sa.delete(self._model).where(*args).returning(self._model)

        result = await self._session.scalars(
            sa.select(self._model).from_statement(stmt)
        )
        await self._session.commit()

        return result.one_or_none()
