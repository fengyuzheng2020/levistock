#!/bin/bash

# 财联社电报快讯 - 飞书推送服务后台启动脚本

SERVICE_NAME="cls_feishu_monitor"
PID_FILE="${SERVICE_NAME}.pid"
LOG_FILE="${SERVICE_NAME}.log"

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "[INFO] 服务已在运行 (PID: $PID)"
            exit 1
        else
            echo "[WARN] 发现过期的 PID 文件，清理中..."
            rm -f "$PID_FILE"
        fi
    fi
    
    # 检查配置文件
    if [ ! -f "config.py" ]; then
        echo "[ERROR] 配置文件 config.py 不存在"
        echo "[INFO] 请复制 config_example.py 为 config.py 并配置"
        exit 1
    fi
    
    echo "[INFO] 启动服务（后台模式）..."
    nohup python3 feishu_monitor_service.py > "$LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"
    
    echo "[SUCCESS] 服务已启动 (PID: $PID)"
    echo "[INFO] 日志文件: $LOG_FILE"
    echo "[INFO] 查看日志: tail -f $LOG_FILE"
    echo "[INFO] 停止服务: ./stop_service.sh"
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "[WARN] PID 文件不存在，服务可能未运行"
        return
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "[INFO] 停止服务 (PID: $PID)..."
        kill $PID
        
        # 等待进程结束
        for i in {1..10}; do
            if ! ps -p $PID > /dev/null; then
                break
            fi
            sleep 1
        done
        
        # 如果还在运行，强制杀死
        if ps -p $PID > /dev/null; then
            echo "[WARN] 进程未响应，强制终止..."
            kill -9 $PID
        fi
        
        rm -f "$PID_FILE"
        echo "[SUCCESS] 服务已停止"
    else
        echo "[WARN] 进程不存在 (PID: $PID)，清理 PID 文件"
        rm -f "$PID_FILE"
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "[INFO] 服务正在运行 (PID: $PID)"
            echo "[INFO] 启动时间: $(ps -p $PID -o lstart=)"
            echo "[INFO] 运行时长: $(ps -p $PID -o etime=)"
            
            if [ -f "$LOG_FILE" ]; then
                echo "[INFO] 日志文件大小: $(du -h "$LOG_FILE" | cut -f1)"
                echo "[INFO] 最后10行日志:"
                tail -n 10 "$LOG_FILE"
            fi
        else
            echo "[WARN] PID 文件存在但进程不存在 (PID: $PID)"
            echo "[INFO] 清理过期的 PID 文件..."
            rm -f "$PID_FILE"
        fi
    else
        echo "[INFO] 服务未运行"
    fi
}

restart() {
    stop
    sleep 2
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status}"
        echo ""
        echo "命令说明:"
        echo "  start   - 启动服务（后台运行）"
        echo "  stop    - 停止服务"
        echo "  restart - 重启服务"
        echo "  status  - 查看服务状态"
        exit 1
        ;;
esac
