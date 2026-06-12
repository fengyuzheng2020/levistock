# 财联社市场数据 - 定时播报服务

## 📋 功能说明

每分钟自动播报以下市场数据到飞书群：

1. **今日主线机会** (`market_mainline_cls`)
   - 显示当前市场的3条主线题材
   - 包含主线描述和相关板块

2. **板块热度排行 Top10** (`get_sector_heat`)
   - 实时热度最高的10个板块
   - 显示热度值、排名变化、新上榜标记

3. **板块轮动近4日** (`get_sector_rotation`)
   - 最近4个交易日每日Top5板块
   - 显示涨跌幅和趋势

## 🚀 快速开始

### 1. 配置飞书机器人

确保已配置 `config.py`（参考 QUICKSTART.md）

### 2. 调整播报间隔（可选）

编辑 `config.py`：

```python
# 市场数据播报间隔（秒）
MARKET_DATA_INTERVAL = 60  # 默认60秒（1分钟）

# 可以调整为：
MARKET_DATA_INTERVAL = 120  # 2分钟
MARKET_DATA_INTERVAL = 300  # 5分钟
```

### 3. 启动服务

**前台运行（测试）：**
```bash
python3 market_data_service.py
```

**后台运行：**
```bash
# 创建后台启动脚本
cat > start_market_bot.sh << 'EOF'
#!/bin/bash
SERVICE_NAME="market_data_bot"
PID_FILE="${SERVICE_NAME}.pid"
LOG_FILE="${SERVICE_NAME}.log"

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null; then
            echo "[INFO] 服务已在运行 (PID: $PID)"
            exit 1
        fi
    fi
    
    echo "[INFO] 启动市场数据播报服务..."
    nohup python3 market_data_service.py > "$LOG_FILE" 2>&1 &
    PID=$!
    echo $PID > "$PID_FILE"
    
    echo "[SUCCESS] 服务已启动 (PID: $PID)"
    echo "[INFO] 日志文件: $LOG_FILE"
    echo "[INFO] 查看日志: tail -f $LOG_FILE"
}

stop() {
    if [ ! -f "$PID_FILE" ]; then
        echo "[WARN] PID 文件不存在"
        return
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null; then
        echo "[INFO] 停止服务 (PID: $PID)..."
        kill $PID
        rm -f "$PID_FILE"
        echo "[SUCCESS] 服务已停止"
    fi
}

case "$1" in
    start) start ;;
    stop) stop ;;
    restart) stop; sleep 2; start ;;
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p $PID > /dev/null; then
                echo "[INFO] 服务正在运行 (PID: $PID)"
            else
                echo "[WARN] 进程不存在"
            fi
        else
            echo "[INFO] 服务未运行"
        fi
        ;;
    *)
        echo "用法: $0 {start|stop|restart|status}"
        ;;
esac
EOF

chmod +x start_market_bot.sh

# 启动服务
./start_market_bot.sh start

# 查看状态
./start_market_bot.sh status

# 查看日志
tail -f market_data_bot.log

# 停止服务
./start_market_bot.sh stop
```

## 📊 消息示例

飞书群收到的消息格式：

```
⏰ 播报时间: 2026-06-12 14:30:00

🔥 今日主线机会

【主线1】半导体芯片
  国产替代加速，多只个股涨停
  板块: 半导体、芯片、光刻机

【主线2】新能源汽车
  政策利好持续，产业链全线上涨
  板块: 锂电池、充电桩、整车

【主线3】人工智能
  大模型应用落地，算力需求激增
  板块: AI芯片、云计算、大数据

---

📊 板块热度排行 Top10

 1. 半导体芯片     热度:  98.5  变化:  ↑2
 2. 新能源汽车     热度:  95.2  变化:  ↑1
 3. 人工智能       热度:  92.8  变化:   -
 4. 光伏储能       热度:  88.3  变化:  ↓1 🆕
 5. 消费电子       热度:  85.7  变化:  ↑3
...

---

🔄 板块轮动（近4日Top10）

📅 2026-06-12
  1. 半导体芯片     +5.23% 🔺
  2. 新能源汽车     +3.87% 🔺
  3. 人工智能       +2.45% 🔺
  4. 光伏储能       +1.92% 🔺
  5. 消费电子       +1.56% 🔺

📅 2026-06-11
  1. 医药生物       +2.34% 🔺
  2. 食品饮料       +1.89% 🔺
  ...

---
💡 每分钟自动更新 | 数据来源: 财联社
```

## ⚙️ 配置说明

### 播报间隔 (MARKET_DATA_INTERVAL)

| 值 | 说明 | 适用场景 |
|---|---|---|
| `60` | 1分钟（默认） | 高频监控，及时捕捉变化 |
| `120` | 2分钟 | 平衡及时性和API调用频率 |
| `300` | 5分钟 | 低频监控，节省资源 |

**建议**：
- 交易时间（9:30-15:00）：使用 60-120 秒
- 非交易时间：可以停止服务或延长间隔

### 自定义播报内容

如果需要修改播报内容，编辑 `market_data_bot.py`：

```python
def send_market_report(self):
    """发送市场数据报告"""
    
    # 修改这里可以自定义播报内容
    mainline_text = self._format_mainline(mainline_data)
    heat_text = self._format_sector_heat(heat_data, top_n=10)  # 改为 top_n=5 只显示前5
    rotation_text = self._format_sector_rotation(rotation_data)
    
    # 组合消息
    full_report = f"""..."""
```

## 🔧 高级用法

### 同时运行两个服务

可以同时运行电报快讯和市场数据两个服务：

```bash
# 终端1：电报快讯监控
cd levistock/news/
./background_service.sh start

# 终端2：市场数据播报
cd levistock/news/
./start_market_bot.sh start
```

### 不同时间段使用不同间隔

可以编写脚本根据时间自动调整：

```python
import datetime

def get_interval():
    """根据时间返回不同的播报间隔"""
    now = datetime.datetime.now()
    hour = now.hour
    
    # 交易时间（9:30-15:00）：1分钟
    if 9 <= hour < 15:
        return 60
    # 其他时间：5分钟
    else:
        return 300
```

### 添加更多数据源

可以在 `send_market_report()` 中添加其他数据：

```python
from levistock.market.market_emotion_cls import market_emotion_cls

# 获取市场情绪数据
emotion_data = market_emotion_cls()

# 格式化并添加到报告中
emotion_text = f"市场热度: {emotion_data['market_degree']}"
full_report += f"\n\n{emotion_text}"
```

## ⚠️ 注意事项

1. **API 频率限制**
   - 建议间隔 ≥ 60 秒
   - 避免过于频繁的请求

2. **交易时间**
   - 建议在交易时间（9:30-15:00）运行
   - 非交易时间数据不会更新

3. **资源占用**
   - 每次播报会调用3个API接口
   - 注意服务器带宽和CPU使用

4. **消息长度**
   - 飞书消息有长度限制
   - 如果内容过长会自动截断

## 🐛 故障排查

### 收不到消息？

1. 检查飞书配置是否正确
2. 运行测试：`python3 test_feishu_bot.py`
3. 查看日志：`tail -f market_data_bot.log`
4. 确认是交易日且在交易时间内

### 数据为空？

1. 确认是交易日
2. 确认在交易时间内（9:30-15:00）
3. 检查网络连接
4. 手动测试接口：
   ```python
   from levistock.market.market_wind_cls import market_mainline_cls
   data = market_mainline_cls()
   print(data)
   ```

### 服务异常退出？

1. 查看日志中的错误信息
2. 检查是否有足够的内存
3. 确认依赖已安装：`pip install levistock`

## 📝 总结

这个服务可以帮你：
- ✅ 实时监控市场主线机会
- ✅ 跟踪热门板块动态
- ✅ 观察板块轮动趋势
- ✅ 自动推送到飞书群
- ✅ 无需人工干预

适合：
- 短线交易者
- 板块轮动策略
- 市场情绪监控
- 量化交易辅助

祝投资顺利！📈
