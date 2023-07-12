from uuid import UUID

import sqlalchemy.orm as so

import uuid6

from net_vision_microservice.server import dto
from net_vision_microservice.server.database.models.main import DatabaseBase


class Entry(DatabaseBase):
    __tablename__ = "entries"

    uuid: so.Mapped[UUID] = so.mapped_column(primary_key=True, default=uuid6.uuid7)
    text: so.Mapped[str] = so.mapped_column(nullable=False)

    def to_dto(self) -> dto.Entry:
        return dto.Entry(uuid=self.uuid, text=self.text)
