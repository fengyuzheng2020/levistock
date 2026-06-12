#!/bin/bash

# ========================================
# 配置阿里云 Docker 镜像加速器
# ========================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否 root
if [ "$EUID" -ne 0 ]; then 
    print_error "请使用 sudo 运行此脚本"
    exit 1
fi

print_info "配置阿里云 Docker 镜像加速器..."

# 创建或更新 daemon.json
cat > /etc/docker/daemon.json << 'EOF'
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://huecker.io",
    "https://dockerhub.timeweb.cloud",
    "https://noohub.ru"
  ],
  "dns": [
    "100.100.2.136",
    "100.100.2.138",
    "223.5.5.5",
    "223.6.6.6"
  ]
}
EOF

print_info "配置文件已更新: /etc/docker/daemon.json"

# 重启 Docker
print_info "重启 Docker 服务..."
systemctl daemon-reload
systemctl restart docker

print_info "Docker 已重启"

# 验证配置
print_info "验证配置..."
docker info | grep -A 5 "Registry Mirrors"

print_info "✅ 配置完成！"
print_info ""
print_info "现在可以重新构建镜像："
print_info "  ./deploy.sh start"
print_info ""
print_info "或者手动测试："
print_info "  docker pull python:3.11-slim"
