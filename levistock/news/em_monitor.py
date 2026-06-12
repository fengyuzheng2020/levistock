"""
东方财富快讯 - 飞书机器人推送服务

功能说明:
- 实时监控东方财富快讯
- 检测到新消息时自动推送到飞书机器人
- 支持自定义推送间隔和过滤规则
"""

import time
import datetime
from typing import Optional, Callable


class EMBriefMonitor:
    """东方财富快讯监控器"""
    
    def __init__(
        self,
        feishu_bot,
        interval: int = 30,
        filter_func: Optional[Callable] = None
    ):
        """
        初始化监控器
        
        Args:
            feishu_bot: 飞书机器人实例（FeishuBot对象）
            interval: 轮询间隔（秒），默认30秒
            filter_func: 自定义过滤函数，接收消息dict，返回True则推送
        """
        self.feishu_bot = feishu_bot
        self.interval = interval
        self.filter_func = filter_func
        self.seen_ids = set()  # 已处理的消息ID集合
        self.running = False
    
    def _fetch_latest_news(self, limit: int = 5) -> list:
        """
        获取最新的快讯消息
        
        Args:
            limit: 获取数量限制
            
        Returns:
            最新消息列表
        """
        from levistock.news.news_em import news_brief_em
        
        try:
            # 获取最新的快讯
            print(f"[DEBUG] 正在获取最新 {limit} 条东方财富快讯...")
            data = news_brief_em(limit=limit)
            
            if not data:
                print(f"[WARNING] 未获取到数据")
                return []
            
            print(f"[DEBUG] 成功获取 {len(data)} 条数据")
            return data
        except Exception as e:
            print(f"[ERROR] 获取东方财富快讯失败: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _format_message(self, news_item: dict) -> tuple:
        """
        格式化消息为飞书推送格式
        
        Args:
            news_item: 单条快讯数据
            
        Returns:
            (标题, 内容列表)
        """
        title = news_item.get("title", "无标题")
        content = news_item.get("content", "")
        time_str = news_item.get("time", "")
        stock_list = news_item.get("stock_list", [])
        
        # 构建富文本内容
        content_list = [
            [{"tag": "text", "text": f"⏰ 时间: {time_str}"}],
            [{"tag": "text", "text": f"📰 标题: {title}"}],
        ]
        
        if content:
            # 内容过长时截断
            if len(content) > 500:
                content = content[:500] + "..."
            content_list.append([{"tag": "text", "text": f"📝 内容: {content}"}])
        
        # 添加相关股票
        if stock_list:
            # 兼容字符串和字典两种格式
            stocks_text = ""
            for s in stock_list[:5]:
                if isinstance(s, dict):
                    name = s.get("name", "")
                elif isinstance(s, str):
                    name = s
                else:
                    name = ""
                if name:
                    stocks_text += name + ", "
            
            if stocks_text:
                stocks_text = stocks_text.rstrip(", ")
                content_list.append([{"tag": "text", "text": f"📊 相关股票: {stocks_text}"}])
        
        # 添加来源标识
        content_list.append([{"tag": "text", "text": "🔗 来源: 东方财富"}])
        content_list.append([{"tag": "text", "text": "---"}])
        
        return title, content_list
    
    def _send_to_feishu(self, news_item: dict) -> bool:
        """
        发送单条消息到飞书
        
        Args:
            news_item: 单条快讯数据
            
        Returns:
            是否发送成功
        """
        try:
            title, content_list = self._format_message(news_item)
            result = self.feishu_bot.send_post(title=title, content_list=content_list)
            
            if result.get("code") == 0:
                print(f"[SUCCESS] 推送成功: {title[:50]}...")
                return True
            else:
                print(f"[ERROR] 推送失败: {result}")
                return False
        except Exception as e:
            print(f"[ERROR] 推送异常: {e}")
            return False
    
    def _check_new_messages(self) -> list:
        """
        检查新消息
        
        Returns:
            新消息列表
        """
        latest_news = self._fetch_latest_news(limit=10)
        new_messages = []
        
        print(f"[DEBUG] 检查到 {len(latest_news)} 条最新消息")
        print(f"[DEBUG] 已处理消息数: {len(self.seen_ids)}")
        
        for news in latest_news:
            # 使用 code 作为唯一标识
            msg_id = news.get("code", "")
            
            if not msg_id:
                print(f"[WARNING] 消息缺少ID，跳过: {news.get('title', '无标题')}")
                continue
            
            if msg_id not in self.seen_ids:
                # 应用自定义过滤
                if self.filter_func and not self.filter_func(news):
                    print(f"[DEBUG] 消息被过滤器拦截: {news.get('title', '')[:30]}")
                    continue
                
                print(f"[DEBUG] 发现新消息 ID={msg_id}: {news.get('title', '')[:50]}")
                new_messages.append(news)
                self.seen_ids.add(msg_id)
            else:
                print(f"[DEBUG] 消息已存在 ID={msg_id}")
        
        return new_messages
    
    def start(self):
        """启动监控服务"""
        self.running = True
        print("=" * 60)
        print("东方财富快讯 - 飞书推送服务")
        print("=" * 60)
        print(f"轮询间隔: {self.interval}秒")
        print(f"启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        print("开始监控...\n")
        
        # 首次运行时，先加载已有消息（避免重复推送）
        print("[INFO] 初始化，加载已有消息...")
        initial_news = self._fetch_latest_news(limit=20)
        for news in initial_news:
            msg_id = news.get("code", "")
            if msg_id:
                self.seen_ids.add(msg_id)
        print(f"[INFO] 已加载 {len(self.seen_ids)} 条历史消息\n")
        
        try:
            while self.running:
                new_messages = self._check_new_messages()
                
                if new_messages:
                    print(f"\n[INFO] 发现 {len(new_messages)} 条新消息")
                    for msg in new_messages:
                        self._send_to_feishu(msg)
                        # 每条消息之间稍微延迟，避免频繁请求
                        time.sleep(1)
                else:
                    print(f"[INFO] 暂无新消息 ({datetime.datetime.now().strftime('%H:%M:%S')})")
                
                time.sleep(self.interval)
                
        except KeyboardInterrupt:
            print("\n\n[INFO] 服务已停止")
            self.stop()
    
    def stop(self):
        """停止监控服务"""
        self.running = False
        print("[INFO] 监控服务已停止")


def create_filter_by_keywords(keywords: list) -> Callable:
    """
    创建基于关键词的过滤器
    
    Args:
        keywords: 关键词列表
        
    Returns:
        过滤函数
    """
    def filter_func(news_item: dict) -> bool:
        title = news_item.get("title", "").lower()
        content = news_item.get("content", "").lower()
        
        for keyword in keywords:
            if keyword.lower() in title or keyword.lower() in content:
                return True
        return False
    
    return filter_func


if __name__ == "__main__":
    # ==================== 配置区域 ====================
    
    # 飞书机器人 Webhook URL（替换为你的实际URL）
    FEISHU_WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN"
    
    # 飞书机器人签名密钥（如果启用了签名验证，否则设为None）
    FEISHU_SECRET = None  # "your_secret_here"
    
    # 轮询间隔（秒）
    POLL_INTERVAL = 30
    
    # 关键词过滤（可选，设为None则不过滤）
    # 例如: KEYWORDS = ["涨停", "利好", "公告"]
    KEYWORDS = None
    
    # ================================================
    
    # 导入飞书机器人
    from levistock.news.feishu_monitor import FeishuBot
    
    # 创建飞书机器人实例
    bot = FeishuBot(webhook_url=FEISHU_WEBHOOK_URL, secret=FEISHU_SECRET)
    
    # 创建过滤器（如果需要）
    filter_func = None
    if KEYWORDS:
        filter_func = create_filter_by_keywords(KEYWORDS)
        print(f"启用关键词过滤: {KEYWORDS}")
    
    # 创建监控器
    monitor = EMBriefMonitor(
        feishu_bot=bot,
        interval=POLL_INTERVAL,
        filter_func=filter_func
    )
    
    # 启动监控
    monitor.start()
