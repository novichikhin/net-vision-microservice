from uuid import UUID

import sqlalchemy as sa

from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from net_vision_microservice.server import dto, exceptions
from net_vision_microservice.server.database import models
from net_vision_microservice.server.database.repositories.main import Repository


class EntryRepository(Repository[models.Entry]):

    def __init__(self, session: AsyncSession):
        super().__init__(model=models.Entry, session=session)

    async def read_by_id(self, uuid: UUID) -> Optional[dto.Entry]:
        entry = await self._read_by_id(id=uuid)

        if not entry:
            raise exceptions.EntryNotFound

        return entry.to_dto() if entry else None

    async def read_all(self, limit: Optional[int] = None) -> list[dto.Entry]:
        entries = await self._read_all(limit=limit)

        return [entry.to_dto() for entry in entries]

    async def create(
            self,
            uuid: UUID,
            text: str
    ) -> Optional[dto.Entry]:
        stmt = insert(models.Entry).values(uuid=uuid, text=text).returning(models.Entry)

        try:
            result: sa.ScalarResult[models.Entry] = await self._session.scalars(
                sa.select(models.Entry).from_statement(stmt)
            )
            await self._session.commit()
        except IntegrityError:
            raise exceptions.DuplicateEntry
        else:
            entry: Optional[models.Entry] = result.one_or_none()

            if not entry:
                raise exceptions.EntryNotFound

            return entry.to_dto() if entry else None

    async def delete_by_id(self, uuid: UUID) -> Optional[dto.Entry]:
        entry: Optional[models.Entry] = await self._delete(models.Entry.uuid == uuid)

        if not entry:
            raise exceptions.EntryNotFound

        return entry.to_dto() if entry else None
