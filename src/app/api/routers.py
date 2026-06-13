from fastapi import APIRouter

from src.app.api.v1.admin import router as admin_router
from src.app.api.v1.auth import router as auth_router
from src.app.api.v1.payments import router as payments_router
from src.app.api.v1.users import router as users_router

api_router = APIRouter()
api_router.include_router(admin_router)
api_router.include_router(auth_router)
api_router.include_router(payments_router)
api_router.include_router(users_router)
