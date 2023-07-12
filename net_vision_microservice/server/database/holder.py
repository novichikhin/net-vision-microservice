from sqlalchemy.ext.asyncio import AsyncSession

from net_vision_microservice.server.database.repositories.entry import EntryRepository


class DatabaseHolder:

    def __init__(self, session: AsyncSession):
        self.entry = EntryRepository(session=session)
