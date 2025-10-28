from pydantic import BaseModel, Field

from app.schema.response import Response


class AnalyzeAnswersItem(BaseModel):
    title: str = Field(description="题目名称")
    ans: str = Field(description="题目正确答案")
    user_ans: str = Field(description="用户答案", alias="userAns")
    parse: str = Field(description="答案解析")


class AnswerAnalysis(BaseModel):
    analysis: str = Field(description="分析结果")


AnalyzeAnswersResponse = Response[AnswerAnalysis]
