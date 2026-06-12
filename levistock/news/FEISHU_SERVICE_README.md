# 财联社电报快讯 - 飞书推送服务

实时监控股市资讯，自动推送到飞书群聊。

## 功能特性

✅ **实时监控** - 自动轮询财联社电报快讯  
✅ **智能去重** - 避免重复推送相同消息  
✅ **灵活过滤** - 支持关键词白名单/黑名单过滤  
✅ **多种类型** - 支持全部/重要/公司公告三种消息类型  
✅ **富文本推送** - 美观的飞书消息格式  
✅ **后台运行** - 支持后台模式和 systemd 服务  
✅ **日志记录** - 完整的运行日志  

## 快速开始

### 1. 配置飞书机器人

#### 创建飞书机器人
1. 打开飞书群聊
2. 点击群设置 → 添加机器人 → 自定义机器人
3. 设置机器人名称（如"股市资讯助手"）
4. 复制 Webhook 地址
5. （可选）启用签名验证，复制签名密钥

### 2. 安装依赖

```bash
pip install levistock
```

### 3. 配置文件

```bash
cd levistock/news/
cp config_example.py config.py
```

编辑 `config.py`：

```python
# 填写你的飞书机器人 Webhook URL
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"

# 如果启用了签名验证，填写密钥
FEISHU_SECRET = "your_secret_here"  # 或 None

# 选择消息类型
MESSAGE_CATEGORY = "important"  # important/all/company

# 设置轮询间隔（秒）
POLL_INTERVAL = 30

# （可选）关键词过滤
KEYWORDS = ["涨停", "利好", "重组"]  # 只推送包含这些关键词的消息
BLACKLIST_KEYWORDS = ["广告"]  # 过滤掉包含这些关键词的消息
```

### 4. 启动服务

#### 方式一：前台运行（测试用）

```bash
python3 feishu_monitor_service.py
```

按 `Ctrl+C` 停止服务。

#### 方式二：后台运行（推荐）

```bash
chmod +x background_service.sh

# 启动服务
./background_service.sh start

# 查看状态
./background_service.sh status

# 查看日志
tail -f cls_feishu_monitor.log

# 停止服务
./background_service.sh stop

# 重启服务
./background_service.sh restart
```

## 配置说明

### 消息类型 (MESSAGE_CATEGORY)

| 值 | 说明 | 适用场景 |
|---|---|---|
| `"important"` | 加红重要消息（默认） | 关注重大市场动态 |
| `"all"` | 全部电报 | 全面监控所有资讯 |
| `"company"` | 公司公告 | 关注上市公司公告 |

### 轮询间隔 (POLL_INTERVAL)

- **建议值**: 30-60 秒
- **最小值**: 10 秒（避免频繁请求）
- 间隔越短，消息越及时，但请求频率越高

### 关键词过滤

#### 白名单过滤 (KEYWORDS)

只推送包含指定关键词的消息：

```python
KEYWORDS = ["涨停", "利好", "重组", "收购", "业绩"]
```

#### 黑名单过滤 (BLACKLIST_KEYWORDS)

过滤掉包含指定关键词的消息：

```python
BLACKLIST_KEYWORDS = ["广告", "推广", "营销"]
```

可以同时使用白名单和黑名单。

## 高级用法

### 自定义过滤器

在代码中使用自定义过滤逻辑：

```python
from levistock.news.feishu_monitor import CLSTelegraphMonitor, FeishuBot

def my_filter(news_item):
    """自定义过滤函数"""
    # 只推送涨跌幅超过5%的消息
    if "涨" in news_item.get("title", "") or "跌" in news_item.get("title", ""):
        return True
    return False

bot = FeishuBot(webhook_url="YOUR_WEBHOOK_URL")
monitor = CLSTelegraphMonitor(
    feishu_bot=bot,
    category="important",
    interval=30,
    filter_func=my_filter
)
monitor.start()
```

### 多机器人推送

可以配置多个飞书机器人，推送不同类型的消息：

```python
# 重要消息推送到管理群
bot_important = FeishuBot(webhook_url="WEBHOOK_1")
monitor_important = CLSTelegraphMonitor(
    feishu_bot=bot_important,
    category="important",
    interval=30
)

# 公司公告推送到公告群
bot_company = FeishuBot(webhook_url="WEBHOOK_2")
monitor_company = CLSTelegraphMonitor(
    feishu_bot=bot_company,
    category="company",
    interval=60
)
```

### systemd 服务（Linux 服务器）

创建 systemd 服务文件 `/etc/systemd/system/cls-feishu.service`：

```ini
[Unit]
Description=CLS Telegraph Feishu Monitor
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/levistock/news
ExecStart=/usr/bin/python3 /path/to/levistock/news/feishu_monitor_service.py
Restart=always
RestartSec=10
StandardOutput=append:/path/to/levistock/news/service.log
StandardError=append:/path/to/levistock/news/service.log

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable cls-feishu
sudo systemctl start cls-feishu

# 查看状态
sudo systemctl status cls-feishu

# 查看日志
sudo journalctl -u cls-feishu -f
```

## 消息示例

飞书群收到的消息格式：

```
⏰ 时间: 2026-06-12 14:30:00
📰 标题: XX公司发布重大资产重组公告
📝 内容: XX公司今日发布公告，拟以发行股份及支付现金方式购买资产...
---
```

## 常见问题

### Q: 收不到消息？

A: 检查以下几点：
1. Webhook URL 是否正确
2. 飞书机器人是否已添加到群聊
3. 是否有新消息产生（可以先测试 `news_telegraph_cls()`）
4. 查看日志文件是否有错误信息

### Q: 消息重复推送？

A: 服务会自动去重，但如果重启服务，可能会重新推送最近的消息。这是正常行为。

### Q: 如何调整推送频率？

A: 修改 `config.py` 中的 `POLL_INTERVAL` 参数。

### Q: 可以在 Windows 上运行吗？

A: 可以，使用 `python3 feishu_monitor_service.py` 前台运行即可。后台脚本仅适用于 Linux/Mac。

### Q: 如何确保服务稳定运行？

A: 
1. 使用后台模式或 systemd 服务
2. 定期检查日志文件
3. 设置进程监控（如 supervisor）
4. 配置开机自启

## 注意事项

⚠️ **重要提示**

1. **API 频率限制**: 不要设置过短的轮询间隔（建议 ≥30 秒）
2. **网络安全**: 不要泄露 Webhook URL 和签名密钥
3. **消息过滤**: 合理使用关键词过滤，避免消息过多
4. **资源占用**: 服务会持续运行，注意服务器资源
5. **合规使用**: 仅用于个人学习和研究，遵守相关法律法规

## 技术支持

如有问题，请查看：
- 项目文档: [levistock README](../README.md)
- 日志文件: `cls_feishu_monitor.log`

## 许可证

MIT License
