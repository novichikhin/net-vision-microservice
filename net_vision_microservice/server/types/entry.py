from uuid import UUID

from pydantic import BaseModel

from net_vision_microservice.server import dto


class BaseEntry(BaseModel):
    uuid: UUID
    text: str


class Entry(BaseEntry):

    @classmethod
    def from_dto(cls, entry: dto.Entry) -> "Entry":
        return Entry(uuid=entry.uuid, text=entry.text)


class CreateEntry(BaseEntry):
    pass
