from fastapi import FastAPI

from app.api.router import server_router
from app.config.conf import config

app: FastAPI = FastAPI(
    title=config.API_NAME,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
)

app.include_router(server_router)
