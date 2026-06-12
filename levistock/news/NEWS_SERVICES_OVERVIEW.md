# News 目录 - 服务总览

本目录包含两个飞书推送服务，用于实时监控和播报股市资讯。

## 📁 文件结构

```
levistock/news/
├── 核心模块
│   ├── news_cls.py                  # 财联社电报快讯接口封装
│   ├── feishu_monitor.py            # 飞书机器人和监控器核心实现
│   └── market_data_bot.py           # 市场数据播报器（新增）
│
├── 服务程序
│   ├── feishu_monitor_service.py    # 电报快讯实时监控服务
│   └── market_data_service.py       # 市场数据定时播报服务（新增）
│
├── 配置文件
│   ├── config_example.py            # 配置模板
│   └── config.py                    # 实际配置（需自行创建，已加入.gitignore）
│
├── 测试脚本
│   ├── test_feishu_bot.py           # 飞书机器人测试
│   └── test_market_data_bot.py      # 市场数据接口测试（新增）
│
├── 启动脚本
│   ├── start_service.sh             # 电报服务简单启动
│   ├── background_service.sh        # 电报服务后台管理
│   └── start_market_bot.sh          # 市场数据服务后台管理（需创建）
│
└── 文档
    ├── QUICKSTART.md                # 快速开始指南
    ├── FEISHU_SERVICE_README.md     # 电报服务详细文档
    ├── MARKET_DATA_BOT_README.md    # 市场数据播报文档（新增）
    └── NEWS_SERVICES_OVERVIEW.md    # 本文档：服务总览
```

## 🎯 两个服务的区别

### 服务1：电报快讯实时监控 (feishu_monitor_service.py)

**功能**：
- 实时监控财联社电报快讯
- 检测到新消息立即推送
- 支持关键词过滤

**特点**：
- ✅ 事件驱动：有新消息才推送
- ✅ 智能去重：避免重复推送
- ✅ 实时性强：30秒轮询一次
- ✅ 可过滤：支持关键词白名单/黑名单

**适用场景**：
- 需要及时获取突发新闻
- 关注特定题材或个股
- 追踪公司公告

**配置项**：
```python
MESSAGE_CATEGORY = "important"  # 消息类型
POLL_INTERVAL = 30              # 轮询间隔（秒）
KEYWORDS = ["涨停", "利好"]     # 关键词过滤
```

---

### 服务2：市场数据定时播报 (market_data_service.py) ⭐ 新增

**功能**：
- 每分钟播报今日主线机会
- 每分钟播报板块热度 Top10
- 每分钟播报板块轮动近4日

**特点**：
- ✅ 定时播报：固定间隔推送
- ✅ 数据丰富：三个维度全面覆盖
- ✅ 格式美观：结构化展示
- ✅ 自动更新：无需人工干预

**适用场景**：
- 监控市场主线变化
- 跟踪热门板块动态
- 观察板块轮动趋势
- 辅助短线交易决策

**配置项**：
```python
MARKET_DATA_INTERVAL = 60  # 播报间隔（秒）
```

---

## 🚀 快速部署

### 第一步：配置飞书机器人

```bash
cd levistock/news/
cp config_example.py config.py
# 编辑 config.py，填写 Webhook URL
```

### 第二步：测试配置

```bash
# 测试飞书机器人
python3 test_feishu_bot.py

# 测试市场数据接口
python3 test_market_data_bot.py
```

### 第三步：启动服务

#### 方案A：只运行电报监控

```bash
# 前台运行
python3 feishu_monitor_service.py

# 后台运行
./background_service.sh start
```

#### 方案B：只运行市场数据播报

```bash
# 前台运行
python3 market_data_service.py

# 后台运行（需先创建 start_market_bot.sh）
./start_market_bot.sh start
```

#### 方案C：同时运行两个服务 ⭐ 推荐

```bash
# 终端1：电报监控
./background_service.sh start

# 终端2：市场数据播报
./start_market_bot.sh start
```

---

## 📊 消息示例对比

### 电报快讯消息

```
⏰ 时间: 2026-06-12 14:30:00
📰 标题: XX公司发布重大资产重组公告
📝 内容: XX公司今日发布公告，拟以发行股份...
---
```

**特点**：单条消息，即时推送

---

### 市场数据播报消息

```
⏰ 播报时间: 2026-06-12 14:30:00

🔥 今日主线机会
【主线1】半导体芯片
  国产替代加速，多只个股涨停
  板块: 半导体、芯片、光刻机

【主线2】新能源汽车
  政策利好持续，产业链全线上涨
  板块: 锂电池、充电桩、整车

---

📊 板块热度排行 Top10
 1. 半导体芯片     热度:  98.5  变化: ↑2
 2. 新能源汽车     热度:  95.2  变化: ↑1
 3. 人工智能       热度:  92.8  变化:  -
...

---

🔄 板块轮动（近4日Top10）
📅 2026-06-12
  1. 半导体芯片     +5.23% 🔺
  2. 新能源汽车     +3.87% 🔺
...

---
💡 每分钟自动更新 | 数据来源: 财联社
```

**特点**：综合报告，定时推送

---

## ⚙️ 配置说明

### 共用配置

```python
# 飞书机器人 Webhook URL（必须配置）
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"

# 签名密钥（可选）
FEISHU_SECRET = None
```

### 电报服务专属配置

```python
# 消息类型
MESSAGE_CATEGORY = "important"  # important/all/company

# 轮询间隔（秒）
POLL_INTERVAL = 30

# 关键词过滤
KEYWORDS = ["涨停", "利好"]
BLACKLIST_KEYWORDS = ["广告"]
```

### 市场数据服务专属配置

```python
# 播报间隔（秒）
MARKET_DATA_INTERVAL = 60  # 建议 60-300
```

---

## 💡 使用建议

### 个人投资者

**推荐配置**：
- 电报服务：`MESSAGE_CATEGORY = "important"`, `POLL_INTERVAL = 30`
- 市场数据：`MARKET_DATA_INTERVAL = 120`（2分钟）

**理由**：
- 重要消息及时推送
- 市场数据适度更新，避免打扰

---

### 专业交易者

**推荐配置**：
- 电报服务：`MESSAGE_CATEGORY = "all"`, `POLL_INTERVAL = 15`
- 市场数据：`MARKET_DATA_INTERVAL = 60`（1分钟）

**理由**：
- 全量消息，不错过任何信息
- 高频更新，及时捕捉变化

---

### 量化策略

**推荐配置**：
- 电报服务：`KEYWORDS = ["涨停", "重组", "收购"]`
- 市场数据：`MARKET_DATA_INTERVAL = 300`（5分钟）

**理由**：
- 只关注特定关键词
- 低频更新，作为策略辅助数据

---

## 🔧 高级用法

### 自定义过滤规则

```python
# 在 config.py 中设置
KEYWORDS = ["半导体", "芯片", "AI"]  # 只关注科技股
```

### 调整播报频率

```python
# 交易时间高频，非交易时间低频
# 需要修改代码实现
```

### 添加更多数据源

编辑 `market_data_bot.py`：

```python
def send_market_report(self):
    # 添加新的数据源
    from levistock.market.market_emotion_cls import market_emotion_cls
    emotion_data = market_emotion_cls()
    
    # 格式化并添加到报告
    emotion_text = f"市场热度: {emotion_data['market_degree']}"
    full_report += f"\n\n{emotion_text}"
```

### 多群推送

创建多个 bot 实例：

```python
bot1 = FeishuBot(webhook_url="WEBHOOK_1")
bot2 = FeishuBot(webhook_url="WEBHOOK_2")

# 分别推送到不同群
```

---

## ⚠️ 注意事项

### API 频率限制

| 服务 | 建议间隔 | 最大频率 |
|------|---------|---------|
| 电报监控 | 30秒 | 不低于15秒 |
| 市场数据 | 60秒 | 不低于30秒 |

### 交易时间

- **最佳运行时间**：9:30 - 15:00（A股交易时间）
- **非交易时间**：数据不会更新，可以停止服务节省资源

### 资源占用

| 服务 | CPU | 内存 | 网络 |
|------|-----|------|------|
| 电报监控 | 低 | ~50MB | 中等 |
| 市场数据 | 低 | ~50MB | 较高（每次3个API） |

### 消息长度

- 飞书消息有长度限制
- 如果内容过长会自动截断
- 建议适当调整显示数量

---

## 🐛 故障排查

### 常见问题

**Q1: 收不到消息？**
- 检查 Webhook URL 是否正确
- 运行测试脚本验证
- 查看日志文件

**Q2: 数据为空？**
- 确认是交易日
- 确认在交易时间内
- 手动测试接口

**Q3: 服务异常退出？**
- 查看日志中的错误信息
- 检查网络连接
- 确认依赖已安装

**Q4: 消息太多/太少？**
- 调整轮询/播报间隔
- 使用关键词过滤
- 修改消息类型

---

## 📝 总结

### 两个服务如何选择？

| 需求 | 推荐服务 |
|------|---------|
| 需要及时获取突发新闻 | 电报监控 |
| 需要监控市场整体态势 | 市场数据播报 |
| 两者都需要 | 同时运行 ⭐ |

### 最佳实践

1. **首次使用**：先运行测试脚本
2. **生产环境**：使用后台模式运行
3. **监控日志**：定期检查日志文件
4. **灵活调整**：根据实际需求调整配置
5. **组合使用**：两个服务互补，效果更佳

---

## 🔗 相关链接

- [快速开始](QUICKSTART.md)
- [电报服务文档](FEISHU_SERVICE_README.md)
- [市场数据播报文档](MARKET_DATA_BOT_README.md)
- [levistock 主文档](../README.md)

---

**祝使用愉快，投资顺利！** 📈💰
