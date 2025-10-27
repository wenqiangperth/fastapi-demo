from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """统一响应模型"""

    code: int = Field(default=200, description="业务状态码")
    message: str = Field(default="success", description="响应消息")
    data: T | None = Field(default=None, description="响应数据")


def success(data=None, message="success", code=200):
    """成功响应"""
    return {"code": code, "message": message, "data": data}
