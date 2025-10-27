from fastapi import APIRouter

from src.routes import example, health

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(example.router)
