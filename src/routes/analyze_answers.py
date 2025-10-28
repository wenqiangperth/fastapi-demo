from fastapi import APIRouter

from src.schema.analyze_answers import AnalyzeAnswersItem, AnalyzeAnswersResponse
from src.schema.response import success

router = APIRouter()


@router.post("/analyze_answers", response_model=AnalyzeAnswersResponse)
async def analyze_answers(answers: list[AnalyzeAnswersItem]):
    return success()
