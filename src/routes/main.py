from fastapi import APIRouter

from src.routes import health

api_router = APIRouter()

api_router.include_router(health.router)
