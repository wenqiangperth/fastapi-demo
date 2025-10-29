from typing import Any

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger


class APIException(Exception):
    """API异常基类"""

    def __init__(self, message: str, code: int = 400, data: Any = None):
        self.message = message
        self.code = code
        self.data = data
        super().__init__(message)


# 常用的几个异常类
class BadRequestException(APIException):
    """请求参数错误"""

    def __init__(self, message: str = "请求参数错误", data: Any = None):
        super().__init__(message, code=400, data=data)


class NotFoundException(APIException):
    """资源不存在"""

    def __init__(self, message: str = "资源不存在", data: Any = None):
        super().__init__(message, code=404, data=data)


class UnauthorizedException(APIException):
    """未授权"""

    def __init__(self, message: str = "未授权, 请先登录", data: Any = None):
        super().__init__(message, code=401, data=data)


class ForbiddenException(APIException):
    """无权限"""

    def __init__(self, message: str = "权限不足", data: Any = None):
        super().__init__(message, code=403, data=data)


# ================异常处理器========================


async def api_exception_handler(request: Request, exc: APIException):
    """自定义API异常处理"""
    logger.warning(
        f"API Exception | Path: {request.url.path} | "
        f"Code: {exc.code} | Message: {exc.message}"
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"code": exc.code, "message": exc.message, "data": exc.data},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """参数验证异常处理"""
    # 简化错误信息
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])  # 去掉 'body'
        errors.append(f"{field}: {error['msg']}")

    error_msg = "; ".join(errors)
    logger.warning(f"Validation Error | Path: {request.url.path} | Errors: {error_msg}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 422,
            "message": "参数验证失败: " + "; ".join(errors),
            "data": None,
        },
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """处理 FastAPI 内置的 HTTPException"""
    logger.warning(
        f"HTTP Exception | Path: {request.url.path} | "
        f"Status: {exc.status_code} | Detail: {exc.detail}"
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"code": exc.status_code, "message": exc.detail, "data": None},
    )


async def general_exception_handler(request: Request, exc: Exception):
    """兜底异常处理"""
    logger.error(
        f"Unhandled Exception | Path: {request.url.path} | Error: {exc!s}",
        exc_info=True,
    )

    # 开发环境返回详细错误，生产环境隐藏
    import os

    is_dev = os.getenv("ENV", "dev") == "dev"

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 500,
            "message": str(exc) if is_dev else "服务器内部错误",
            "data": None,
        },
    )
