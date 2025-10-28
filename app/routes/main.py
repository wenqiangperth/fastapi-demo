from fastapi import APIRouter

from app.routes import analyze_answers, eval_image, example, health

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(example.router)

api_router.include_router(eval_image.router)
api_router.include_router(analyze_answers.router)
