from fastapi import APIRouter

from src.schema.eval_image import EvalImageRequest, EvalImageResponse
from src.schema.response import success

router = APIRouter()


@router.post("/eval_single_image", response_model=EvalImageResponse)
async def eval_single_image(request: EvalImageRequest):
    return success()


@router.post(
    "/eval_batch_image",
)
async def eval_batch_image():
    return success()
