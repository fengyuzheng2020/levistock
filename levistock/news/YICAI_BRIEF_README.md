# 第一财经快讯 - 飞书推送服务

## 功能说明

实时监控第一财经（yicai.com）快讯，检测到新消息时自动推送到飞书机器人。

## 快速开始

### 1. 配置飞书机器人

编辑 `config.py` 文件，配置以下参数：

```python
# 飞书机器人 Webhook URL
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN"

# 是否开启第一财经快讯监控
ENABLE_YICAI_MONITOR = True

# 轮询间隔（秒）
YICAI_POLL_INTERVAL = 30

# 关键词过滤（可选）
YICAI_KEYWORDS = None  # 例如: ["涨停", "利好", "重组"]
```

### 2. 运行服务

#### 方式一：单独运行第一财经监控

```bash
cd levistock/news
python yicai_monitor.py
```

#### 方式二：使用统一服务（推荐）

在 `config.py` 中设置：
```python
ENABLE_YICAI_MONITOR = True  # 开启第一财经
ENABLE_NEWS_MONITOR = False  # 关闭财联社（可选）
ENABLE_MARKET_REPORT = False  # 关闭市场数据（可选）
```

然后运行：
```bash
cd levistock/news
python unified_service.py
```

## API 使用

### 获取第一财经快讯

```python
import levistock as lk

# 获取最新20条快讯
data = lk.news_brief_yicai()
print(f"获取到 {len(data)} 条快讯")

# 获取指定数量
data = lk.news_brief_yicai(limit=5)

# 遍历快讯
for item in data:
    print(f"[{item['time']}] {item['title']}")
    print(f"内容: {item['content']}")
    print(f"链接: {item['share_url']}")
    print("---")
```

### 返回数据结构

```python
{
    "id": 103227797,              # 快讯ID
    "title": "国际油价跌幅扩大",   # 标题
    "content": "WTI原油期货...",  # 内容
    "time": "2026-06-12 15:59:54", # 发布时间
    "share_url": "https://m.yicai.com/brief/...", # 分享链接
    "important": false             # 是否重要消息
}
```

## 高级用法

### 关键词过滤

只推送包含特定关键词的快讯：

```python
from levistock.news.feishu_monitor import FeishuBot
from levistock.news.yicai_monitor import YicaiBriefMonitor, create_filter_by_keywords

# 创建飞书机器人
bot = FeishuBot(webhook_url="YOUR_WEBHOOK_URL")

# 创建关键词过滤器
filter_func = create_filter_by_keywords(["涨停", "利好", "重组"])

# 创建监控器
monitor = YicaiBriefMonitor(
    feishu_bot=bot,
    interval=30,
    filter_func=filter_func
)

# 启动监控
monitor.start()
```

### 自定义过滤函数

```python
def my_filter(news_item):
    """只推送重要消息"""
    return news_item.get("important", False)

monitor = YicaiBriefMonitor(
    feishu_bot=bot,
    interval=30,
    filter_func=my_filter
)
```

## 配置说明

| 配置项 | 说明 | 默认值 | 建议值 |
|--------|------|--------|--------|
| ENABLE_YICAI_MONITOR | 是否开启监控 | False | True |
| YICAI_POLL_INTERVAL | 轮询间隔（秒） | 30 | 30-60 |
| YICAI_KEYWORDS | 关键词过滤 | None | 根据需求设置 |

## 注意事项

1. **轮询间隔**：建议设置为 30-60 秒，避免频繁请求
2. **关键词过滤**：如果设置了关键词，只有包含这些关键词的消息才会推送
3. **历史消息**：服务启动时会加载最近20条历史消息，避免重复推送
4. **HTML标签**：内容中的HTML标签会自动去除

## 与其他服务配合使用

可以在统一服务中同时开启多个功能：

```python
# config.py
ENABLE_NEWS_MONITOR = True      # 财联社电报
ENABLE_YICAI_MONITOR = True     # 第一财经快讯
ENABLE_MARKET_REPORT = True     # 市场数据播报
ENABLE_MARKET_WIND = True       # 风口板块播报
```

运行统一服务后，会同时启动所有开启的功能。

## 常见问题

### Q: 如何获取飞书机器人 Webhook URL？

A: 在飞书群聊中添加机器人 -> 选择"自定义机器人" -> 复制 Webhook 地址

### Q: 为什么收不到推送？

A: 检查以下几点：
1. Webhook URL 是否正确
2. 网络连接是否正常
3. 是否有新消息产生
4. 是否设置了关键词过滤

### Q: 如何停止服务？

A: 按 `Ctrl+C` 即可优雅停止服务

## 示例输出

```
====================================================================
                    第一财经快讯 - 飞书推送服务
====================================================================
轮询间隔: 30秒
启动时间: 2026-06-12 16:00:00
====================================================================
开始监控...

[INFO] 初始化，加载已有消息...
[INFO] 已加载 20 条历史消息

[INFO] 暂无新消息 (16:00:30)
[INFO] 暂无新消息 (16:01:00)

[INFO] 发现 2 条新消息
[SUCCESS] 推送成功: 国际油价跌幅扩大...
[SUCCESS] 推送成功: 港交所回应期货限价放宽...
```
