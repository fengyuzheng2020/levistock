# 财联社电报快讯 - 飞书推送服务

## 📋 项目概述

这是一个实时监控财联社电报快讯并自动推送到飞书群聊的服务。基于 `levistock` SDK 的 `news_telegraph_cls()` 接口实现。

## 📁 文件结构

```
levistock/news/
├── feishu_monitor.py              # 核心模块：飞书机器人和监控器实现
├── feishu_monitor_service.py      # 主程序：服务启动入口
├── config_example.py              # 配置模板（需要复制为 config.py）
├── test_feishu_bot.py             # 测试脚本：验证飞书配置
├── background_service.sh          # 后台服务管理脚本
├── start_service.sh               # 简单启动脚本
├── QUICKSTART.md                  # 快速开始指南（5分钟部署）
├── FEISHU_SERVICE_README.md       # 完整使用文档
└── README_NEWS_SERVICE.md         # 本文件：项目总览
```

## 🚀 快速开始

### 1. 配置飞书机器人

```bash
cd levistock/news/
cp config_example.py config.py
# 编辑 config.py，填写你的飞书 Webhook URL
```

### 2. 测试配置

```bash
python3 test_feishu_bot.py
```

### 3. 启动服务

**前台运行（测试）：**
```bash
python3 feishu_monitor_service.py
```

**后台运行（推荐）：**
```bash
chmod +x background_service.sh
./background_service.sh start
```

详细步骤请查看 [QUICKSTART.md](QUICKSTART.md)

## ✨ 核心功能

### 1. 实时监控
- 自动轮询财联社电报快讯
- 智能去重，避免重复推送
- 支持自定义轮询间隔

### 2. 消息过滤
- 关键词白名单过滤
- 关键词黑名单过滤
- 自定义过滤函数

### 3. 多种消息类型
- `important`: 加红重要消息（默认）
- `all`: 全部电报
- `company`: 公司公告

### 4. 富文本推送
- 美观的飞书消息格式
- 包含时间、标题、内容
- 支持 @ 指定人员

### 5. 后台运行
- 支持后台模式
- systemd 服务支持
- 完整的日志记录

## 📖 文档说明

| 文档 | 说明 | 适用场景 |
|------|------|----------|
| [QUICKSTART.md](QUICKSTART.md) | 5分钟快速部署指南 | 首次使用，快速上手 |
| [FEISHU_SERVICE_README.md](FEISHU_SERVICE_README.md) | 完整使用文档 | 深入了解功能和配置 |
| 本文档 | 项目总览和文件说明 | 了解项目结构 |

## 🔧 主要模块

### feishu_monitor.py

核心实现模块，包含：

- **FeishuBot**: 飞书机器人客户端
  - `send_text()`: 发送文本消息
  - `send_post()`: 发送富文本消息
  - 支持签名验证

- **CLSTelegraphMonitor**: 电报监控器
  - 实时轮询财联社接口
  - 智能去重机制
  - 消息过滤和格式化
  - 自动推送到飞书

- **工具函数**:
  - `create_filter_by_keywords()`: 创建关键词过滤器

### feishu_monitor_service.py

主程序入口，负责：
- 加载配置文件
- 初始化飞书机器人
- 创建监控器
- 注册信号处理器（优雅退出）
- 启动监控循环

### config_example.py

配置模板文件，包含：
- 飞书机器人配置（Webhook URL、签名密钥）
- 监控配置（消息类型、轮询间隔）
- 过滤配置（关键词白名单/黑名单）
- 高级配置（调试模式、重试策略）

### background_service.sh

后台服务管理脚本，支持：
- `start`: 启动服务（后台运行）
- `stop`: 停止服务
- `restart`: 重启服务
- `status`: 查看服务状态

## 💡 使用示例

### 基础用法

```python
from levistock.news.feishu_monitor import FeishuBot, CLSTelegraphMonitor

# 创建飞书机器人
bot = FeishuBot(webhook_url="YOUR_WEBHOOK_URL")

# 创建监控器
monitor = CLSTelegraphMonitor(
    feishu_bot=bot,
    category="important",
    interval=30
)

# 启动监控
monitor.start()
```

### 关键词过滤

```python
from levistock.news.feishu_monitor import create_filter_by_keywords

# 只推送包含"涨停"或"利好"的消息
filter_func = create_filter_by_keywords(["涨停", "利好"])

monitor = CLSTelegraphMonitor(
    feishu_bot=bot,
    category="important",
    interval=30,
    filter_func=filter_func
)
```

### 自定义过滤

```python
def my_filter(news_item):
    """只推送标题长度超过10的消息"""
    return len(news_item.get("title", "")) > 10

monitor = CLSTelegraphMonitor(
    feishu_bot=bot,
    category="important",
    interval=30,
    filter_func=my_filter
)
```

## ⚙️ 配置说明

### 必要配置

```python
# 飞书机器人 Webhook URL（必须配置）
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"
```

### 可选配置

```python
# 签名密钥（如果启用了签名验证）
FEISHU_SECRET = None

# 消息类型: important/all/company
MESSAGE_CATEGORY = "important"

# 轮询间隔（秒）
POLL_INTERVAL = 30

# 关键词白名单
KEYWORDS = ["涨停", "利好"]

# 关键词黑名单
BLACKLIST_KEYWORDS = ["广告"]
```

## 🎯 应用场景

1. **个人投资者**: 实时接收重要市场资讯
2. **交易团队**: 监控重大公告和利好消息
3. **量化策略**: 作为消息面数据源
4. **研究分析**: 跟踪特定板块或个股动态

## ⚠️ 注意事项

1. **API 频率限制**: 建议轮询间隔 ≥ 30 秒
2. **网络安全**: 不要泄露 Webhook URL 和签名密钥
3. **消息过滤**: 合理使用过滤，避免消息过多
4. **合规使用**: 仅用于个人学习和研究

## 🐛 故障排查

### 收不到消息？

1. 检查 Webhook URL 是否正确
2. 运行测试脚本: `python3 test_feishu_bot.py`
3. 查看日志文件: `tail -f cls_feishu_monitor.log`
4. 确认有新消息产生

### 服务异常退出？

1. 查看日志文件中的错误信息
2. 检查网络连接
3. 确认依赖已安装: `pip install levistock`

### 消息重复推送？

服务会自动去重，但重启后可能重新推送最近的消息，这是正常行为。

## 📝 更新日志

### v1.0.0 (2026-06-12)
- ✅ 初始版本发布
- ✅ 支持实时监控财联社电报
- ✅ 支持飞书机器人推送
- ✅ 支持关键词过滤
- ✅ 支持后台运行
- ✅ 完整的文档和示例

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🔗 相关链接

- [levistock 项目主页](../README.md)
- [财联社官网](https://www.cls.cn/)
- [飞书开放平台](https://open.feishu.cn/)

---

**祝使用愉快！** 🎉

如有问题，请查看详细文档或提交 Issue。
