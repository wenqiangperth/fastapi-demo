#!/bin/bash

# 本地测试运行用脚本
# 直接执行此脚本，如果src目录有改动，会自动同步到docker容器中，便于开发同学调试

sh scripts/run_docker.sh -t v1.0.0 -n fastapi-demo-container-local -p 8000 -w 1 -m  $(pwd)/src:/app/src
