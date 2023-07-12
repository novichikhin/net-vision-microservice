from fastapi import FastAPI

from net_vision_microservice.server.api.api_v1.endpoints import entry, healthcheck


def register_routers(app: FastAPI) -> None:
    app.include_router(entry.router, tags=["entry"])
    app.include_router(
        healthcheck.router,
        prefix="/healthcheck",
        tags=["healthcheck"]
    )
