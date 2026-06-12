#!/bin/bash

# 财联社电报快讯 - 飞书推送服务启动脚本

echo "======================================"
echo "  财联社电报快讯 - 飞书推送服务"
echo "======================================"
echo ""

# 检查配置文件
if [ ! -f "config.py" ]; then
    echo "[ERROR] 配置文件 config.py 不存在"
    echo "[INFO] 请复制 config_example.py 为 config.py 并配置"
    exit 1
fi

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 未安装"
    exit 1
fi

echo "[INFO] 启动服务..."
echo "[INFO] 按 Ctrl+C 停止服务"
echo ""

# 启动服务
python3 feishu_monitor_service.py
