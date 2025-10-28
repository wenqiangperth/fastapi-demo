from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError

from app.core.config import settings
from app.core.exceptions import (
    APIException,
    api_exception_handler,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from app.core.logging import setup_logging
from app.middleware.logging import LoggingMiddleware  # 导入中间件
from app.routes.main import api_router

# 配置日志
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs" if settings.ENV == "dev" else None,
    redoc_url=f"{settings.API_V1_STR}/redoc" if settings.ENV == "dev" else None,
)

# ⭐ 注册日志中间件
app.add_middleware(LoggingMiddleware)

# 注册异常处理器
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

app.include_router(api_router, prefix=settings.API_V1_STR)
