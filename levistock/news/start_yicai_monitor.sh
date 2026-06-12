#!/bin/bash

# 第一财经快讯监控 - 快速启动脚本

echo "=========================================="
echo "  第一财经快讯监控 - 快速启动"
echo "=========================================="
echo ""

# 检查配置文件
if [ ! -f "config.py" ]; then
    echo "[ERROR] 配置文件 config.py 不存在"
    echo "[INFO] 请复制 config_example.py 为 config.py 并配置"
    exit 1
fi

# 检查是否启用了第一财经监控
ENABLED=$(python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from config import ENABLE_YICAI_MONITOR
    print('True' if ENABLE_YICAI_MONITOR else 'False')
except:
    print('False')
")

if [ "$ENABLED" != "True" ]; then
    echo "[WARNING] 第一财经快讯监控未启用"
    echo "[INFO] 请在 config.py 中设置 ENABLE_YICAI_MONITOR = True"
    echo ""
    read -p "是否继续运行？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo "[INFO] 启动第一财经快讯监控服务..."
echo "[INFO] 按 Ctrl+C 停止服务"
echo ""

# 启动服务
python3 yicai_monitor.py
