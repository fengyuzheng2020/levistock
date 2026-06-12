# 统一服务使用指南

## 🚀 快速开始

### 1. 配置功能开关

编辑 `config.py`，设置要开启的功能：

```python
# ==================== 统一服务功能开关 ====================

# 是否开启电报快讯监控
ENABLE_NEWS_MONITOR = True   # True=开启, False=关闭

# 是否开启市场数据播报
ENABLE_MARKET_REPORT = True  # True=开启, False=关闭
```

### 2. 启动服务

```bash
cd levistock/news/
python3 unified_service.py
```

就这么简单！服务会根据你的配置自动启动相应的功能。

---

## ⚙️ 配置说明

### 场景1：同时开启两个功能（推荐）

```python
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = True
```

**效果**：
- ✅ 实时监控电报快讯
- ✅ 每分钟播报市场数据

---

### 场景2：只开启电报监控

```python
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = False
```

**效果**：
- ✅ 实时监控电报快讯
- ❌ 不播报市场数据

---

### 场景3：只开启市场数据播报

```python
ENABLE_NEWS_MONITOR = False
ENABLE_MARKET_REPORT = True
```

**效果**：
- ❌ 不监控电报快讯
- ✅ 每分钟播报市场数据

---

### 场景4：全部关闭（会报错）

```python
ENABLE_NEWS_MONITOR = False
ENABLE_MARKET_REPORT = False
```

**效果**：
- ❌ 启动时会提示至少需要开启一个功能

---

## 📊 其他配置项

### 电报监控相关配置

```python
# 消息类型
MESSAGE_CATEGORY = "important"  # important/all/company

# 轮询间隔（秒）
POLL_INTERVAL = 30

# 关键词过滤（可选）
KEYWORDS = ["涨停", "利好"]
BLACKLIST_KEYWORDS = None
```

### 市场数据播报相关配置

```python
# 播报间隔（秒）
MARKET_DATA_INTERVAL = 60
```

### 飞书机器人配置

```python
# Webhook URL（必须配置）
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"

# 签名密钥（可选）
FEISHU_SECRET = None
```

---

## 💡 使用示例

### 示例1：短线交易者

```python
# 需要及时掌握所有信息
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = True

MESSAGE_CATEGORY = "important"
POLL_INTERVAL = 30
MARKET_DATA_INTERVAL = 60
```

---

### 示例2：只关注突发新闻

```python
# 只需要电报监控
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = False

MESSAGE_CATEGORY = "all"
POLL_INTERVAL = 15
KEYWORDS = ["涨停", "重组", "收购"]
```

---

### 示例3：只关注市场态势

```python
# 只需要市场数据播报
ENABLE_NEWS_MONITOR = False
ENABLE_MARKET_REPORT = True

MARKET_DATA_INTERVAL = 120  # 2分钟播报一次
```

---

### 示例4：低频监控（节省资源）

```python
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = True

POLL_INTERVAL = 60           # 电报1分钟检查一次
MARKET_DATA_INTERVAL = 300   # 市场数据5分钟播报一次
```

---

## 🔧 高级用法

### 根据时间段动态调整

如果需要更复杂的控制，可以修改 `unified_service.py`：

```python
import datetime

def get_config_by_time():
    """根据时间返回不同的配置"""
    now = datetime.datetime.now()
    hour = now.hour
    
    # 交易时间（9:30-15:00）：全开
    if 9 <= hour < 15:
        return {
            'ENABLE_NEWS_MONITOR': True,
            'ENABLE_MARKET_REPORT': True,
            'POLL_INTERVAL': 30,
            'MARKET_DATA_INTERVAL': 60
        }
    # 非交易时间：只开市场数据，低频
    else:
        return {
            'ENABLE_NEWS_MONITOR': False,
            'ENABLE_MARKET_REPORT': True,
            'MARKET_DATA_INTERVAL': 300
        }
```

---

## 📝 启动流程

当你运行 `python3 unified_service.py` 时：

1. **加载配置** - 读取 `config.py`
2. **检查配置** - 验证必要参数
3. **显示配置** - 打印当前启用的功能
4. **启动服务** - 根据开关启动相应服务
   - 如果两个都开启：使用多进程同时运行
   - 如果只开启一个：直接运行
5. **等待信号** - 按 Ctrl+C 停止

---

## ⚠️ 注意事项

### 1. 至少开启一个功能

```python
# ❌ 错误：两个都关闭
ENABLE_NEWS_MONITOR = False
ENABLE_MARKET_REPORT = False

# ✅ 正确：至少开启一个
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = False
```

### 2. 配置修改后需重启

修改 `config.py` 后，需要重新启动服务才能生效：

```bash
# 停止服务（Ctrl+C）
# 修改 config.py
# 重新启动
python3 unified_service.py
```

### 3. 资源占用

- 同时开启两个服务会占用更多资源
- 如果服务器资源有限，建议只开启需要的功能

### 4. 日志查看

服务会在控制台输出实时日志，可以直接看到运行状态。

---

## 🐛 故障排查

### Q1: 提示配置文件不存在？

```bash
ls -la config.py
# 如果不存在
cp config_example.py config.py
```

### Q2: 提示至少需要开启一个功能？

检查 `config.py`：
```python
# 确保至少有一个是 True
ENABLE_NEWS_MONITOR = True  # 或
ENABLE_MARKET_REPORT = True
```

### Q3: 某个功能没有生效？

1. 检查对应的开关是否为 `True`
2. 检查该功能的其他配置是否正确
3. 查看控制台输出是否有错误信息

### Q4: 如何完全停止服务？

按 `Ctrl+C` 即可停止所有服务。

---

## 📋 配置模板

### 完整配置示例

```python
# ==================== 飞书机器人配置 ====================
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
FEISHU_SECRET = None

# ==================== 电报监控配置 ====================
MESSAGE_CATEGORY = "important"
POLL_INTERVAL = 30
KEYWORDS = None
BLACKLIST_KEYWORDS = None

# ==================== 市场数据播报配置 ====================
MARKET_DATA_INTERVAL = 60

# ==================== 统一服务功能开关 ====================
ENABLE_NEWS_MONITOR = True
ENABLE_MARKET_REPORT = True
```

---

## 🎯 总结

**最简单的使用方式：**

```bash
# 1. 配置（只需一次）
cp config_example.py config.py
# 编辑 config.py，设置 ENABLE_NEWS_MONITOR 和 ENABLE_MARKET_REPORT

# 2. 启动
python3 unified_service.py

# 3. 停止
按 Ctrl+C
```

通过修改两个开关，就可以灵活控制开启哪些功能！🎉
