from net_vision_microservice.server.api.api_v1.responses.main import BaseResponse


class EntryNotFound(BaseResponse):
    detail: str = "Entry not found"


class DuplicateEntry(BaseResponse):
    detail: str = "Duplicate entry"
