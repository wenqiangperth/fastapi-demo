from pydantic import BaseModel, Field

from app.schema.response import Response


class User(BaseModel):
    """用户模型"""

    id: int
    username: str
    age: int | None = None


class UserCreate(BaseModel):
    """创建用户请求"""

    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    age: int | None = Field(None, ge=1, le=150, description="年龄")


UserResponse = Response[User]
