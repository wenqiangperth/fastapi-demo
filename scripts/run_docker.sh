#!/bin/bash

# 设置默认值
DEFAULT_TAG="v1.0.0"
DEFAULT_REGISTRY="qlchat-prod-acr-registry-vpc.cn-hangzhou.cr.aliyuncs.com/xqd-ai"
DEFAULT_IMAGE_NAME="fastapi-demo"
DEFAULT_SERVICE_PORT="8000"
DEFAULT_WORKER_NUM="1"
DEFAULT_CONTAINER_NAME="fastapi-demo-container"
# 目录映射默认不设置
volume_mapping=""

# 脚本使用帮助
show_help() {
    echo "使用说明: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -t, --tag TAG           指定镜像标签，默认: $DEFAULT_TAG"
    echo "  -n, --name NAME         指定容器名称，默认: $DEFAULT_CONTAINER_NAME"
    echo "  -p, --port PORT         指定服务端口，默认: $DEFAULT_SERVICE_PORT"
    echo "  -w, --workers NUM       指定工作进程数，默认: $DEFAULT_WORKER_NUM"
    echo "  -m, --mount PATH        指定目录映射，格式为'主机路径:容器路径'，无默认值"
    echo "  -h, --help              显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                      使用默认参数运行容器"
    echo "  $0 -t latest            使用最新标签运行容器"
    echo "  $0 -n my-qlchat-app     使用自定义容器名运行容器"
    echo "  $0 -p 5070 -w 2         自定义端口和工作进程数"
    echo "  $0 -m /host/path:/container/path  添加目录映射"
}

# 解析命令行参数
tag="$DEFAULT_TAG"
container_name="$DEFAULT_CONTAINER_NAME"
service_port="$DEFAULT_SERVICE_PORT"
worker_num="$DEFAULT_WORKER_NUM"

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -t|--tag)
            tag="$2"
            shift
            shift
            ;;
        -n|--name)
            container_name="$2"
            shift
            shift
            ;;
        -p|--port)
            service_port="$2"
            shift
            shift
            ;;
        -w|--workers)
            worker_num="$2"
            shift
            shift
            ;;
        -m|--mount)
            volume_mapping="$2"
            shift
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)  # 未知选项
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 构建完整镜像名称
full_image="$DEFAULT_REGISTRY/$DEFAULT_IMAGE_NAME:$tag"

# 显示运行信息
cat << EOF
正在启动Docker容器：
- 镜像名称: $full_image
- 容器名称: $container_name
- 服务端口: $service_port
- 工作进程数: $worker_num
EOF

# 如果设置了目录映射，显示映射信息
if [ -n "$volume_mapping" ]; then
    echo "- 目录映射: $volume_mapping"
fi

# 检查镜像是否存在
docker image inspect "$full_image" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "
警告: 镜像 $full_image 不存在，将尝试从仓库拉取..."
    docker pull "$full_image"
    if [ $? -ne 0 ]; then
        echo "
错误: 无法拉取镜像 $full_image! 请检查标签是否正确。"
        exit 1
    fi
fi

# 检查容器名是否已存在
docker ps -a --filter name="^${container_name}$" --format "{{.Names}}" | grep -q "^${container_name}$"
if [ $? -eq 0 ]; then
    echo "
警告: 容器名 '$container_name' 已存在! 将尝试停止并移除现有容器..."
    docker stop "$container_name" > /dev/null 2>&1
    docker rm "$container_name" > /dev/null 2>&1
fi

# 构建docker run命令
run_command="docker run \
    --network host \
    --name \"$container_name\" \
    -e SERVICE_PORT=$service_port \
    -e WORKER_NUM=$worker_num \
    -d"

# 如果设置了目录映射，添加-v选项
if [ -n "$volume_mapping" ]; then
    run_command="$run_command \
    -v $volume_mapping"
fi

# 添加镜像名称
run_command="$run_command \
    $full_image"

# 执行docker run命令
eval $run_command

# 检查运行是否成功
if [ $? -ne 0 ]; then
    echo "
错误: Docker容器启动失败!"
    exit 1
fi


echo "
Docker容器启动成功! 容器名称: $container_name"

# 显示如何进入容器
echo "
使用以下命令查看容器状态:"
echo "docker ps -a | grep $container_name"
echo "
使用以下命令进入容器:"
echo "docker exec -it $container_name /bin/bash"
echo "
使用以下命令查看容器日志:"
echo "docker logs -f $container_name"


# 显示如何停止容器
echo "
使用以下命令停止容器:"
echo "docker stop $container_name"
echo "
使用以下命令删除容器:"
echo "docker rm $container_name"
