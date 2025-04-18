from fastapi import APIRouter

from app.api.routes.health import health_router
from app.api.routes.projects import projects_router
from app.api.routes.recomendations import recomendations_router

server_router: APIRouter = APIRouter(
    prefix="/evergreen/pro",
)

server_router.include_router(health_router)
server_router.include_router(projects_router)
server_router.include_router(recomendations_router)
