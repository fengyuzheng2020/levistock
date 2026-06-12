"""
财联社电报快讯 - 飞书推送服务配置文件

使用说明:
1. 复制此文件为 config.py
2. 填写你的飞书机器人 Webhook URL
3. 根据需要调整其他配置
4. 运行: python feishu_monitor_service.py
"""

# ==================== 飞书机器人配置 ====================

# 飞书机器人 Webhook URL
# 获取方式: 飞书群聊 -> 添加机器人 -> 自定义机器人 -> 复制 Webhook 地址
FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/9cda1509-c434-4bba-85d8-d9f8147dc568"

# 飞书机器人签名密钥（可选）
# 如果在创建机器人时启用了签名验证，请填写此处
# 如果未启用，设为 None
FEISHU_SECRET = None

# ==================== 监控配置 ====================

# 消息类型
# 可选值:
#   - "all":       全部电报
#   - "important": 加红重要消息（推荐）
#   - "company":   公司公告
MESSAGE_CATEGORY = "important"

# 轮询间隔（秒）
# 建议: 30-60秒，避免频繁请求
POLL_INTERVAL = 30

# ==================== 过滤配置 ====================

# 关键词过滤（可选）
# 如果设置了关键词，只有包含这些关键词的消息才会推送
# 设为 None 则推送所有消息
# 示例: KEYWORDS = ["涨停", "利好", "重组", "收购"]
KEYWORDS = None

# 黑名单关键词（可选）
# 包含这些关键词的消息将被过滤掉
# 设为 None 则不过滤
# 示例: BLACKLIST_KEYWORDS = ["广告", "推广"]
BLACKLIST_KEYWORDS = None

# ==================== 高级配置 ====================

# 是否显示调试信息
DEBUG = False

# 最大历史消息数（启动时加载，避免重复推送）
MAX_INITIAL_MESSAGES = 50

# 单次推送最大消息数
MAX_BATCH_SIZE = 5

# 推送失败重试次数
RETRY_COUNT = 3

# 重试间隔（秒）
RETRY_INTERVAL = 5

# ==================== 市场数据播报配置 ====================

# 市场数据播报间隔（秒）
# 用于 market_data_service.py，默认60秒（1分钟）
# 建议: 60-300秒，避免频繁请求
MARKET_DATA_INTERVAL = 60

# ==================== 统一服务功能开关 ====================

# 是否开启电报快讯监控
# True = 开启, False = 关闭
ENABLE_NEWS_MONITOR = True

# 是否开启市场数据播报
# True = 开启, False = 关闭
ENABLE_MARKET_REPORT = True

# 是否开启风口板块播报
# True = 开启, False = 关闭
ENABLE_MARKET_WIND = False

# ==================== 风口板块播报配置 ====================

# 风口板块播报间隔（秒）
# 默认300秒（5分钟），建议 180-600秒
MARKET_WIND_INTERVAL = 300

# 是否包含龙头股信息
# True = 包含, False = 不包含
MARKET_WIND_INCLUDE_STOCKS = True
