from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from net_vision_microservice.server.api.api_v1.dependencies.database import DatabaseEngineMarker


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    engine: AsyncEngine = app.dependency_overrides[DatabaseEngineMarker]()

    await engine.dispose()
