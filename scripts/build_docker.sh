#!/bin/bash

# 设置默认值
DEFAULT_TAG="v1.0.0"
DEFAULT_DOCKERFILE="docker/Dockerfile"
DEFAULT_REGISTRY="qlchat-prod-acr-registry-vpc.cn-hangzhou.cr.aliyuncs.com/xqd-ai"
DEFAULT_IMAGE_NAME="fastapi-demo"
REMOVE_EXISTING=false  # 是否删除已有镜像

# 脚本使用帮助
show_help() {
    echo "使用说明: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -t, --tag TAG           指定镜像标签，默认: $DEFAULT_TAG"
    echo "  -f, --file DOCKERFILE   指定Dockerfile文件，默认: $DEFAULT_DOCKERFILE"
    echo "  -r, --remove-existing   如果存在相同镜像则先删除"
    echo "  -h, --help              显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                      使用默认参数构建镜像"
    echo "  $0 -t v1.1.2 -r         删除已有镜像后构建"
}

# 解析命令行参数
tag=$DEFAULT_TAG
dockerfile=$DEFAULT_DOCKERFILE

while [[ $# -gt 0 ]]; do
    key="$1"

    case $key in
        -t|--tag)
            tag="$2"
            shift
            shift
            ;;
        -f|--file)
            dockerfile="$2"
            shift
            shift
            ;;
        -r|--remove-existing)
            REMOVE_EXISTING=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 构建完整镜像名
full_image_name="$DEFAULT_REGISTRY/$DEFAULT_IMAGE_NAME:$tag"

# 检查Dockerfile是否存在
if [ ! -f "$dockerfile" ]; then
    echo "错误: Dockerfile '$dockerfile' 不存在!"
    exit 1
fi

# 检查本地是否存在该镜像
existing_image_id=$(docker images -q "$full_image_name")

if [ -n "$existing_image_id" ]; then
    echo "检测到已有镜像 $full_image_name (ID: $existing_image_id)"

    if [ "$REMOVE_EXISTING" = true ]; then
        echo "正在删除已有镜像..."
        docker rmi "$full_image_name"
        if [ $? -ne 0 ]; then
            echo "错误: 删除已有镜像失败!"
            exit 1
        fi
        echo "旧镜像删除成功。"
    else
        echo "错误: 镜像 $full_image_name 已存在，脚本退出。"
        exit 1
    fi
fi


# 显示构建信息
cat << EOF
开始构建Docker镜像:
- Dockerfile: $dockerfile
- 镜像标签: $tag
- 完整镜像名: $full_image_name
EOF

# 执行构建命令
echo "\n开始构建过程..."
docker build \
    -f $dockerfile \
    --progress=plain \
    --tag=$full_image_name \
    .

# 检查构建是否成功
if [ $? -ne 0 ]; then
    echo "\n错误: Docker镜像构建失败!"
    exit 1
fi

echo "\nDocker镜像构建成功!"
