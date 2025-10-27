from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.core.response import Response, success

router = APIRouter()


class EvalImageRequest(BaseModel):
    image: str = Field(description="图像url")


class EvalImageDimension(BaseModel):
    composition: int = Field(description="构图评分")
    technique: int = Field(description="技术评分")
    lighting: int = Field(description="光影评分")
    color: int = Field(description="色彩评分")
    narrative: int = Field(description="叙事性评分")
    emotion: int = Field(description="情感表达评分")


class EvalImageScore(BaseModel):
    overall_score: int = Field(description="图像整体评分", alias="overallScore")
    dimensions: EvalImageDimension = Field(description="图像维度评分")


EvalImageResponse = Response[EvalImageScore]


@router.post("/eval_single_image", response_model=EvalImageResponse)
async def eval_single_image(request: EvalImageRequest):
    return success()


@router.post(
    "/eval_batch_image",
)
async def eval_batch_image():
    return success()
