# 配置文件说明

此目录用于存放 Levistock 服务的配置文件。

## 📁 目录结构

```
config/
└── config.py          # 主配置文件（从 config_example.py 复制）
```

## 🔧 配置步骤

### 1. 首次使用

```bash
# 从示例文件复制
cp ../levistock/news/config_example.py config.py

# 编辑配置
vim config.py
```

### 2. 必填配置

```python
# 飞书机器人 Webhook URL（必须修改）
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_TOKEN_HERE"
```

### 3. 可选配置

```python
# 功能开关
ENABLE_NEWS_MONITOR = True      # 电报快讯监控
ENABLE_MARKET_REPORT = False    # 市场数据播报
ENABLE_YICAI_MONITOR = False    # 第一财经快讯
ENABLE_SINA_MONITOR = False     # 新浪财经快讯
ENABLE_EM_MONITOR = False       # 东方财富快讯

# 轮询间隔（秒）
POLL_INTERVAL = 30
YICAI_POLL_INTERVAL = 30
SINA_POLL_INTERVAL = 30
EM_POLL_INTERVAL = 30

# 关键词过滤（可选）
KEYWORDS = ["涨停", "利好"]
```

## 🔄 配置生效

修改配置后，重启容器即可生效：

```bash
# 方法1：使用部署脚本
../deploy.sh reload

# 方法2：手动重启
docker restart levistock-service
```

## ⚠️ 注意事项

1. **不要提交到 Git**：`config.py` 包含敏感信息，已添加到 `.gitignore`
2. **备份配置**：修改前建议备份 `cp config.py config.py.bak`
3. **语法检查**：修改后可运行 `python3 -c "import config"` 验证语法

## 📖 更多配置项

查看完整配置示例：`../levistock/news/config_example.py`

或参考文档：`../DOCKER_DEPLOY.md`
