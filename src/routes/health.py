from fastapi import APIRouter

from src.schema.response import Response, success

router = APIRouter()


@router.post("/health", response_model=Response[None])
@router.get("/health", response_model=Response[None])
async def health():
    return success(message="ok")
