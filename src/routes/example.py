"""
示例接口 - 演示正常响应和异常返回
"""

from fastapi import APIRouter, Path, Query
from loguru import logger
from pydantic import BaseModel, Field

from src.core.exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)
from src.core.response import Response, success

router = APIRouter(prefix="/examples", tags=["示例接口"])


# ==================== 数据模型 ====================


class User(BaseModel):
    """用户模型"""

    id: int
    username: str
    age: int | None = None


class UserCreate(BaseModel):
    """创建用户请求"""

    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    age: int | None = Field(None, ge=1, le=150, description="年龄")


# ==================== 接口示例 ====================

UserResponse = Response[User]


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(..., ge=1, description="用户ID")):
    """
    示例1: 获取用户详情

    ✅ 正常响应: GET /examples/users/1
    返回:
    {
        "code": 200,
        "message": "success",
        "data": {
            "id": 1,
            "username": "user_1",
            "age": 25
        }
    }

    ❌ 异常响应: GET /examples/users/999
    返回:
    {
        "code": 404,
        "message": "用户 999 不存在",
        "data": null
    }
    """
    # 模拟：ID > 100 的用户不存在
    if user_id > 100:
        logger.warning(f"User {user_id} not found")
        raise NotFoundException(f"用户 {user_id} 不存在")

    # 正常返回
    user = User(id=user_id, username=f"user_{user_id}", age=20 + user_id)
    return success(data=user)


@router.post("/users", response_model=UserResponse)
async def create_user(user_in: UserCreate):
    """
    示例2: 创建用户

    ✅ 正常响应: POST /examples/users
    请求体:
    {
        "username": "newuser",
        "age": 25
    }
    返回:
    {
        "code": 200,
        "message": "用户创建成功",
        "data": {
            "id": 100,
            "username": "newuser",
            "age": 25
        }
    }

    ❌ 异常响应1 (业务错误): POST /examples/users
    请求体:
    {
        "username": "admin",
        "age": 25
    }
    返回:
    {
        "code": 400,
        "message": "用户名 admin 已被占用",
        "data": null
    }

    ❌ 异常响应2 (参数验证失败): POST /examples/users
    请求体:
    {
        "username": "ab",
        "age": 200
    }
    返回:
    {
        "code": 422,
        "message": "参数验证失败: username: ensure this value has at least 3 characters; age: ensure this value is less than or equal to 150",
        "data": {...}
    }
    """
    # 模拟：用户名为 admin 或 root 的已存在
    if user_in.username in ["admin", "root"]:
        raise BadRequestException(f"用户名 {user_in.username} 已被占用")

    # 正常返回
    new_user = User(id=100, username=user_in.username, age=user_in.age)
    return success(data=new_user, message="用户创建成功")


@router.delete("/users/{user_id}", response_model=Response[None])
async def delete_user(
    user_id: int = Path(..., ge=1, description="用户ID"),
    token: str = Query(None, description="认证令牌"),
):
    """
    示例3: 删除用户

    ✅ 正常响应: DELETE /examples/users/5?token=valid_token
    返回:
    {
        "code": 200,
        "message": "用户删除成功",
        "data": null
    }

    ❌ 异常响应1 (未授权): DELETE /examples/users/5
    返回:
    {
        "code": 401,
        "message": "未授权，请提供 token 参数",
        "data": null
    }

    ❌ 异常响应2 (token无效): DELETE /examples/users/5?token=wrong_token
    返回:
    {
        "code": 401,
        "message": "token 无效",
        "data": null
    }

    ❌ 异常响应3 (资源不存在): DELETE /examples/users/999?token=valid_token
    返回:
    {
        "code": 404,
        "message": "用户 999 不存在",
        "data": null
    }
    """
    # 模拟：没有 token 视为未授权
    if not token:
        raise UnauthorizedException("未授权，请提供 token 参数")

    # 模拟：token 不是 valid_token 视为未授权
    if token != "valid_token":
        raise UnauthorizedException("token 无效")

    # 模拟：ID > 100 的用户不存在
    if user_id > 100:
        raise NotFoundException(f"用户 {user_id} 不存在")

    # 正常返回
    return success(message="用户删除成功")
