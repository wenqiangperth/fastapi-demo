import time
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

# 用于存储请求信息的上下文变量
request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件"""

    async def dispatch(self, request: Request, call_next):
        # 尝试从请求头中获取请求ID
        request_id = request.headers.get("traceId")
        if not request_id:
            request_id = str(uuid4())
        request_id_var.set(request_id)

        start_time = time.time()
        # ⭐ 使用 contextualize 绑定 request_id 到所有后续日志
        with logger.contextualize(request_id=request_id):
            # 记录请求
            logger.info(
                f"{request.method} {request.url.path} | Client: {request.client.host}"
            )
            try:
                response = await call_next(request)
                duration = (time.time() - start_time) * 1000

                # 记录响应
                logger.info(
                    f"{request.method} {request.url.path} | "
                    f"Status: {response.status_code} | "
                    f"Duration: {duration:.2f}ms"
                )

                response.headers["X-Request-ID"] = request_id
                return response

            except Exception as e:
                duration = (time.time() - start_time) * 1000

                logger.error(
                    f"{request.method} {request.url.path} | "
                    f"Duration: {duration:.2f}ms | "
                    f"Error: {str(e)}"
                )
                raise
