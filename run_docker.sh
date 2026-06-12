#!/bin/bash

# ========================================
# Levistock 简化版 Docker 启动脚本
# 不依赖 docker-compose
# ========================================

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

CONTAINER_NAME="levistock-service"
IMAGE_NAME="levistock:latest"

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查配置目录
if [ ! -d "config" ]; then
    mkdir -p config
    print_info "创建配置目录: config/"
fi

if [ ! -f "config/config.py" ]; then
    if [ -f "levistock/news/config_example.py" ]; then
        cp levistock/news/config_example.py config/config.py
        print_warn "已复制示例配置，请编辑 config/config.py"
    else
        print_error "找不到示例配置文件"
        exit 1
    fi
fi

# 停止并删除旧容器
if docker ps -a | grep -q $CONTAINER_NAME; then
    print_info "停止旧容器..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
fi

# 构建镜像
print_info "构建 Docker 镜像..."
docker build \
    --dns 100.100.2.136 \
    --dns 100.100.2.138 \
    --dns 223.5.5.5 \
    --dns 223.6.6.6 \
    -t $IMAGE_NAME .

# 启动容器
print_info "启动容器..."
docker run -d \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    --dns 100.100.2.136 \
    --dns 100.100.2.138 \
    --dns 223.5.5.5 \
    --dns 223.6.6.6 \
    -v $(pwd)/config/config.py:/app/levistock/news/config.py:ro \
    -e TZ=Asia/Shanghai \
    -e PYTHONUNBUFFERED=1 \
    --cpus=1.0 \
    --memory=512m \
    --log-driver json-file \
    --log-opt max-size=10m \
    --log-opt max-file=3 \
    $IMAGE_NAME

print_info "容器已启动"
print_info "查看日志: docker logs -f ${CONTAINER_NAME}"
print_info "停止服务: docker stop ${CONTAINER_NAME}"
print_info "重启服务: docker restart ${CONTAINER_NAME}"
