#!/usr/bin/env bash
set -e  # 遇到错误退出

echo "🚀 开始准备开发环境..."

# 1️⃣ 检查 uv 是否存在
if ! command -v uv &> /dev/null; then
    echo "🧩 未检测到 uv，正在下载安装..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # 确保 uv 可用
    export PATH="$HOME/.local/bin:$PATH"
else
    echo "✅ 检测到 uv: $(uv --version)"
fi

# 2️⃣ 检查 pre-commit
if ! command -v pre-commit &> /dev/null; then
    echo "🧩 未检测到 pre-commit，使用 uv 安装中..."
    uv tool install pre-commit
    echo "✅ 安装完成 pre-commit: $(pre-commit --version)"
else
    echo "✅ 检测到 pre-commit: $(pre-commit --version)"
fi

# 3️⃣ 安装项目依赖
if [ -f "pyproject.toml" ]; then
    echo "📦 检测到 pyproject.toml，使用 uv 安装依赖..."
    uv sync
elif [ -f "requirements.txt" ]; then
    echo "📦 检测到 requirements.txt，使用 uv 安装依赖..."
    uv pip install -r requirements.txt
else
    echo "⚠️ 未找到依赖文件 pyproject.toml 或 requirements.txt"
fi

# 4️⃣ 初始化 pre-commit hook
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🔧 初始化 pre-commit hook..."
    pre-commit install
else
    echo "⚠️ 未检测到 .pre-commit-config.yaml，跳过 pre-commit 安装"
fi

echo "🎉 开发环境准备完成！"
