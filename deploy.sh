#!/bin/bash

# ========================================
# Levistock Docker 部署脚本
# 使用纯 Docker 命令，不依赖 docker-compose
# ========================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目名称
PROJECT_NAME="levistock"
CONTAINER_NAME="levistock-service"

# 打印信息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Docker 是否安装
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
}

# 创建配置目录和示例配置文件
setup_config() {
    print_info "检查配置文件..."
    
    # 创建 config 目录
    if [ ! -d "config" ]; then
        mkdir -p config
        print_info "创建配置目录: config/"
    fi
    
    # 检查 config.py 是否存在
    if [ ! -f "config/config.py" ]; then
        print_warn "配置文件不存在，从示例文件复制..."
        if [ -f "levistock/news/config_example.py" ]; then
            cp levistock/news/config_example.py config/config.py
            print_info "已复制示例配置: config/config.py"
            print_warn "请编辑 config/config.py 填写你的飞书 Webhook URL"
        else
            print_error "找不到示例配置文件: levistock/news/config_example.py"
            exit 1
        fi
    else
        print_info "配置文件已存在: config/config.py"
    fi
}

# 构建 Docker 镜像
build_image() {
    print_info "构建 Docker 镜像..."
    
    # 检查是否使用快速构建
    if [ "$1" == "fast" ]; then
        print_info "使用快速构建模式（国内镜像源）..."
        docker build -f Dockerfile.fast -t ${PROJECT_NAME}:latest .
    else
        docker build -t ${PROJECT_NAME}:latest .
    fi
    
    print_info "镜像构建完成"
}

# 启动服务
start_service() {
    print_info "启动 Levistock 服务..."
    
    # 检查容器是否已存在
    if docker ps -a | grep -q $CONTAINER_NAME; then
        print_warn "容器已存在，先停止并删除..."
        docker stop $CONTAINER_NAME 2>/dev/null || true
        docker rm $CONTAINER_NAME 2>/dev/null || true
    fi
    
    # 启动新容器
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
        ${PROJECT_NAME}:latest
    
    print_info "服务已启动"
    print_info "查看日志: docker logs -f ${CONTAINER_NAME}"
}

# 停止服务
stop_service() {
    print_info "停止 Levistock 服务..."
    
    if docker ps | grep -q $CONTAINER_NAME; then
        docker stop $CONTAINER_NAME
        print_info "服务已停止"
    else
        print_warn "服务未运行"
    fi
}

# 重启服务
restart_service() {
    print_info "重启 Levistock 服务..."
    
    if docker ps | grep -q $CONTAINER_NAME; then
        docker restart $CONTAINER_NAME
        print_info "服务已重启"
    else
        print_warn "服务未运行，尝试启动..."
        start_service
    fi
}

# 查看日志
view_logs() {
    print_info "查看服务日志..."
    docker logs -f $CONTAINER_NAME
}

# 查看状态
show_status() {
    print_info "服务状态:"
    docker ps -a | grep $CONTAINER_NAME || print_warn "容器不存在"
}

# 清理资源
cleanup() {
    print_warn "清理 Docker 资源（包括镜像、容器）..."
    read -p "确认清理？(y/N): " confirm
    
    if [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]]; then
        # 停止并删除容器
        if docker ps -a | grep -q $CONTAINER_NAME; then
            docker stop $CONTAINER_NAME 2>/dev/null || true
            docker rm $CONTAINER_NAME 2>/dev/null || true
            print_info "容器已删除"
        fi
        
        # 删除镜像
        if docker images | grep -q $PROJECT_NAME; then
            docker rmi ${PROJECT_NAME}:latest 2>/dev/null || true
            print_info "镜像已删除"
        fi
        
        print_info "清理完成"
    else
        print_info "取消清理"
    fi
}

# 更新配置后重启
reload_config() {
    print_info "重新加载配置并重启服务..."
    
    # 验证配置文件语法
    if python3 -c "import sys; sys.path.insert(0, 'config'); import config" 2>/dev/null; then
        print_info "配置文件语法检查通过"
        restart_service
    else
        print_error "配置文件语法错误，请检查 config/config.py"
        exit 1
    fi
}

# 显示帮助信息
show_help() {
    echo "用法: $0 <命令> [选项]"
    echo ""
    echo "命令:"
    echo "  start       启动服务"
    echo "  stop        停止服务"
    echo "  restart     重启服务"
    echo "  rebuild     重新构建并启动"
    echo "  logs        查看日志"
    echo "  status      查看状态"
    echo "  reload      重新加载配置并重启"
    echo "  cleanup     清理所有资源"
    echo "  help        显示此帮助信息"
    echo ""
    echo "选项:"
    echo "  fast        使用快速构建模式（国内镜像源）"
    echo ""
    echo "示例:"
    echo "  $0 start          # 启动服务"
    echo "  $0 start fast     # 快速构建并启动（推荐国内用户）"
    echo "  $0 logs           # 查看实时日志"
    echo "  $0 reload         # 修改配置后重新加载"
}

# 主函数
main() {
    check_docker
    
    case "${1:-start}" in
        start)
            setup_config
            build_image "${2:-}"
            start_service
            ;;
        stop)
            stop_service
            ;;
        restart)
            restart_service
            ;;
        rebuild)
            setup_config
            build_image "${2:-}"
            start_service
            ;;
        logs)
            view_logs
            ;;
        status)
            show_status
            ;;
        reload)
            reload_config
            ;;
        cleanup)
            cleanup
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "未知命令: $1"
            show_help
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"
