#!/bin/bash
set -e

# Gunicorn 进程数 (与 Dockerfile 中的 --workers 保持一致或基于 CPU 数量计算)
# 推荐计算方式：(2 * CPU核心数) + 1
# 假设 Docker 分配了 4 核，这里设置为 4 或 9
export WORKER_NUM=${WORKER_NUM:-4}

# 绑定地址和端口
export SERVICE_PORT=${SERVICE_PORT:-8000}


# 设置超时时间 (例如：120秒，防止长时间请求阻塞 Worker)
export GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-120}


# 设置日志级别 (例如：info, warning, error, critical)
export GUNICORN_LOGLEVEL=${GUNICORN_LOGLEVEL:-info}


echo "Starting Gunicorn with uvicorn.workers.UvicornWorker workers..."

exec gunicorn src.main:app \
    --workers "$WORKER_NUM" \
    --worker-class "uvicorn.workers.UvicornWorker" \
    --bind "0.0.0.0:$SERVICE_PORT" \
    --timeout "$GUNICORN_TIMEOUT" \
    --log-level "$GUNICORN_LOGLEVEL" \
    "$@" # 允许通过 CMD 传递额外参数
