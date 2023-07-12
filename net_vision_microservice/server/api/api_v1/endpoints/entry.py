from uuid import UUID

from fastapi import APIRouter, Depends, Query
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_409_CONFLICT
)

from net_vision_microservice.server import types
from net_vision_microservice.server.api.api_v1 import responses
from net_vision_microservice.server.api.api_v1.dependencies.database import DatabaseHolderMarker
from net_vision_microservice.server.database.holder import DatabaseHolder

router = APIRouter()


@router.post(
    "/new",
    response_model=types.Entry,
    responses={
        HTTP_409_CONFLICT: {
            "description": "Duplicate entry error",
            "model": responses.DuplicateEntry
        },
        HTTP_404_NOT_FOUND: {
            "description": "Entry not found error",
            "model": responses.EntryNotFound
        }
    }
)
async def create(create_entry: types.CreateEntry, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    entry = await holder.entry.create(uuid=create_entry.uuid, text=create_entry.text)

    return types.Entry.from_dto(entry=entry)


@router.get("/all", response_model=list[types.Entry])
async def read_all(holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    entries = await holder.entry.read_all()

    return [types.Entry.from_dto(entry=entry) for entry in entries]


@router.get(
    "/{uuid}",
    response_model=types.Entry,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Entry not found error",
            "model": responses.EntryNotFound
        }
    }
)
async def read(uuid: UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    entry = await holder.entry.read_by_id(uuid=uuid)

    return types.Entry.from_dto(entry=entry)


@router.get("/", response_model=list[types.Entry])
async def read_all_count(count: int = Query(ge=0, le=1000), holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    entries = await holder.entry.read_all(limit=count)

    return [types.Entry.from_dto(entry=entry) for entry in entries]


@router.delete(
    "/{uuid}",
    status_code=HTTP_200_OK,
    responses={
        HTTP_404_NOT_FOUND: {
            "description": "Entry not found error",
            "model": responses.EntryNotFound
        }
    }
)
async def delete(uuid: UUID, holder: DatabaseHolder = Depends(DatabaseHolderMarker)):
    await holder.entry.delete_by_id(uuid=uuid)
