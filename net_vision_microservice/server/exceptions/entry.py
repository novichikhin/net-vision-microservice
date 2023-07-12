from net_vision_microservice.server.exceptions.main import BaseAppException


class EntryNotFound(BaseAppException):

    @property
    def message(self) -> str:
        return "Entry not found"


class DuplicateEntry(BaseAppException):

    @property
    def message(self) -> str:
        return "Duplicate entry"
