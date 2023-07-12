from dataclasses import dataclass
from uuid import UUID


@dataclass
class Entry:
    uuid: UUID
    text: str
