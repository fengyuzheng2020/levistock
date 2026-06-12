# 风口板块播报功能说明

## 📋 功能介绍

新增风口板块播报功能，包括：

1. **今日风口板块列表** (`market_wind_cls`)
   - 显示当前市场的热门风口板块
   - 包含催化剂描述

2. **风口板块龙头股** (`market_wind_stocks_cls`)
   - 显示每个风口板块的龙头股
   - 包含价格、涨跌幅、连板次数

3. **今日主线机会** (`market_mainline_cls`)
   - 显示市场主线题材
   - 包含相关板块信息

---

## ⚙️ 配置说明

### 1. 开启风口板块播报

编辑 `config.py`：

```python
# 是否开启风口板块播报
ENABLE_MARKET_WIND = True  # False → True
```

### 2. 调整播报间隔

```python
# 风口板块播报间隔（秒）
# 默认300秒（5分钟），建议 180-600秒
MARKET_WIND_INTERVAL = 300

# 可以调整为：
MARKET_WIND_INTERVAL = 180  # 3分钟
MARKET_WIND_INTERVAL = 600  # 10分钟
```

### 3. 控制是否包含龙头股

```python
# 是否包含龙头股信息
MARKET_WIND_INCLUDE_STOCKS = True   # 包含（默认）
MARKET_WIND_INCLUDE_STOCKS = False  # 不包含（更快）
```

**注意**：包含龙头股会增加API调用次数，播报速度会变慢。

---

## 🚀 使用方法

### 方式一：单独开启风口板块播报

```python
ENABLE_NEWS_MONITOR = False
ENABLE_MARKET_REPORT = False
ENABLE_MARKET_WIND = True  # 只开这个
```

运行：
```bash
python3 unified_service.py
```

---

### 方式二：同时开启所有功能

```python
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = True
ENABLE_MARKET_WIND = True  # 三个都开
```

运行：
```bash
python3 unified_service.py
```

会同时启动3个服务（使用多进程）。

---

### 方式三：风口板块 + 电报监控

```python
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = False
ENABLE_MARKET_WIND = True
```

---

## 📊 消息示例

飞书群收到的消息格式：

```
⏰ 播报时间: 2026-06-12 14:30:00

🌪️ 今日风口板块

1. 半导体芯片
   国产替代加速，政策利好持续

2. 新能源汽车
   销量超预期，产业链全线上涨

3. 人工智能
   大模型应用落地，算力需求激增

---

🐉 风口板块龙头股

  📈 半导体芯片 龙头股:
    • 中芯国际 52.30元 +3.45% (2连板)
    • 北方华创 285.60元 +5.67%
    • 韦尔股份 98.40元 +2.34%

  📈 新能源汽车 龙头股:
    • 比亚迪 268.50元 +4.56%
    • 宁德时代 198.30元 +3.21% (3连板)

---

🎯 今日主线机会

主线1: 科技自立自强
  政策支持力度加大，多个细分领域受益
  相关板块: 半导体、芯片、光刻机、软件

主线2: 新能源产业链
  全球能源转型加速，需求持续增长
  相关板块: 锂电池、光伏、风电

---
💡 数据来源: 财联社
```

---

## 💡 配置建议

### 场景1：短线交易者（高频）

```python
ENABLE_MARKET_WIND = True
MARKET_WIND_INTERVAL = 180  # 3分钟
MARKET_WIND_INCLUDE_STOCKS = True  # 需要龙头股信息
```

---

### 场景2：趋势跟踪者（中频）

```python
ENABLE_MARKET_WIND = True
MARKET_WIND_INTERVAL = 300  # 5分钟（默认）
MARKET_WIND_INCLUDE_STOCKS = True
```

---

### 场景3：长期投资者（低频）

```python
ENABLE_MARKET_WIND = True
MARKET_WIND_INTERVAL = 600  # 10分钟
MARKET_WIND_INCLUDE_STOCKS = False  # 不需要龙头股，更快
```

---

### 场景4：节省资源

```python
ENABLE_MARKET_WIND = True
MARKET_WIND_INTERVAL = 600  # 10分钟
MARKET_WIND_INCLUDE_STOCKS = False  # 减少API调用
```

---

## ⚠️ 注意事项

### 1. API调用频率

- 每次播报会调用 2-5 个API接口
  - `market_wind_cls()` - 1次
  - `market_mainline_cls()` - 1次
  - `market_wind_stocks_cls()` - 每个板块1次（如果开启）

- 如果开启龙头股且有3个风口板块，总共5次API调用

### 2. 播报间隔建议

| 场景 | 建议间隔 | 原因 |
|------|---------|------|
| 交易时间 | 180-300秒 | 及时捕捉变化 |
| 非交易时间 | 600-900秒 | 数据不更新，降低频率 |
| 包含龙头股 | ≥300秒 | API调用较多 |
| 不包含龙头股 | ≥180秒 | API调用较少 |

### 3. 资源占用

- CPU: 低
- 内存: ~50MB
- 网络: 中等（取决于是否包含龙头股）

### 4. 最佳运行时间

- **推荐**: 9:30 - 15:00（A股交易时间）
- **非交易时间**: 数据不会更新，可以关闭或延长间隔

---

## 🔧 高级用法

### 根据时间段动态调整

如果需要更智能的控制，可以修改 `market_wind_bot.py`：

```python
def get_interval_by_time():
    """根据时间返回不同的播报间隔"""
    import datetime
    now = datetime.datetime.now()
    hour = now.hour
    
    # 交易时间：3分钟
    if 9 <= hour < 15:
        return 180
    # 非交易时间：10分钟
    else:
        return 600
```

### 自定义过滤

只关注特定板块：

```python
def _format_wind_plates(self, data: list) -> str:
    # 添加过滤逻辑
    filtered_data = [
        item for item in data 
        if "半导体" in item.get("plate_name", "") 
        or "芯片" in item.get("plate_name", "")
    ]
    # ... 后续处理
```

---

## 🐛 故障排查

### Q1: 收不到消息？

1. 检查 `ENABLE_MARKET_WIND` 是否为 `True`
2. 检查 Webhook URL 是否正确
3. 查看控制台输出是否有错误

### Q2: 播报很慢？

可能原因：
- 开启了龙头股信息（`MARKET_WIND_INCLUDE_STOCKS = True`）
- 风口板块数量较多

解决方法：
- 设置 `MARKET_WIND_INCLUDE_STOCKS = False`
- 增加 `MARKET_WIND_INTERVAL`

### Q3: API调用失败？

1. 检查网络连接
2. 确认是交易日
3. 手动测试接口：
   ```python
   from levistock.market.market_wind_cls import market_wind_cls
   data = market_wind_cls()
   print(data)
   ```

---

## 📝 总结

**快速启用风口板块播报：**

```python
# config.py
ENABLE_MARKET_WIND = True
MARKET_WIND_INTERVAL = 300
MARKET_WIND_INCLUDE_STOCKS = True
```

```bash
python3 unified_service.py
```

就这么简单！🎉
