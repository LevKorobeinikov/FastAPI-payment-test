from fastapi import FastAPI

from src.app.api.routers import api_router
from src.app.core.config import settings

app = FastAPI(title=settings.project_name, version='0.1.0')
app.include_router(api_router, prefix=settings.api_v1_prefix)
