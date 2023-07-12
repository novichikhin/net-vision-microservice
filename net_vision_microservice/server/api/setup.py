from fastapi import FastAPI

from net_vision_microservice.server import types
from net_vision_microservice.server.api.api_v1.dependencies.database import (
    DatabaseEngineMarker,
    DatabaseSessionMarker,
    DatabaseHolderMarker
)
from net_vision_microservice.server.api.api_v1.endpoints.setup import register_routers
from net_vision_microservice.server.api.api_v1.exception import register_exceptions
from net_vision_microservice.server.core.event import lifespan
from net_vision_microservice.server.database.factory import (
    sa_create_engine,
    sa_create_session_factory,
    sa_create_holder
)


def register_app(settings: types.Setting) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    engine = sa_create_engine(connection_uri=settings.database_uri)
    session_factory = sa_create_session_factory(engine=engine)

    register_routers(app=app)
    register_exceptions(app=app)

    app.dependency_overrides.update(
        {
            DatabaseEngineMarker: lambda: engine,
            DatabaseSessionMarker: lambda: session_factory,
            DatabaseHolderMarker: sa_create_holder(session_factory=session_factory)
        }
    )

    return app
