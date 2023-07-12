from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette import status

from net_vision_microservice.server import exceptions
from net_vision_microservice.server.exceptions.main import BaseAppException


def register_exceptions(app: FastAPI) -> None:
    app.add_exception_handler(exceptions.EntryNotFound, entry_not_found_handler)
    app.add_exception_handler(exceptions.DuplicateEntry, duplicate_entry_handler)


async def entry_not_found_handler(_, err: exceptions.EntryNotFound) -> ORJSONResponse:
    return await handle_error(err, status_code=status.HTTP_404_NOT_FOUND)


async def duplicate_entry_handler(_, err: exceptions.DuplicateEntry) -> ORJSONResponse:
    return await handle_error(err, status_code=status.HTTP_409_CONFLICT)


async def handle_error(err: BaseAppException, status_code: int) -> ORJSONResponse:
    return ORJSONResponse({"status": "fail", "detail": err.message}, status_code=status_code)
