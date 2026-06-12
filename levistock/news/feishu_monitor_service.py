"""
财联社电报快讯 - 飞书推送服务（主程序）

使用方法:
1. 复制 config_example.py 为 config.py 并配置
2. 运行: python feishu_monitor_service.py
3. 按 Ctrl+C 停止服务
"""

import sys
import os
import time
import datetime
import signal

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levistock.news.feishu_monitor import FeishuBot, CLSTelegraphMonitor, create_filter_by_keywords


def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), "config.py")
    
    if not os.path.exists(config_path):
        print(f"[ERROR] 配置文件不存在: {config_path}")
        print(f"[INFO] 请复制 config_example.py 为 config.py 并配置")
        sys.exit(1)
    
    # 动态导入配置
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    return config


def create_blacklist_filter(blacklist: list) -> callable:
    """创建黑名单过滤器"""
    def filter_func(news_item: dict) -> bool:
        title = news_item.get("title", "").lower()
        content = news_item.get("content", "").lower()
        
        for keyword in blacklist:
            if keyword.lower() in title or keyword.lower() in content:
                return False  # 黑名单命中，过滤掉
        return True
    
    return filter_func


def main():
    """主函数"""
    print("=" * 70)
    print(" " * 15 + "财联社电报快讯 - 飞书推送服务")
    print("=" * 70)
    
    # 加载配置
    try:
        config = load_config()
        print("[SUCCESS] 配置文件加载成功\n")
    except Exception as e:
        print(f"[ERROR] 配置文件加载失败: {e}")
        sys.exit(1)
    
    # 验证必要配置
    if not hasattr(config, 'FEISHU_WEBHOOK_URL') or \
       config.FEISHU_WEBHOOK_URL == "https://open.feishu.cn/open-apis/bot/v2/hook/your_webhook_token_here":
        print("[ERROR] 请配置 FEISHU_WEBHOOK_URL")
        print("[INFO] 编辑 config.py 文件，填写你的飞书机器人 Webhook URL")
        sys.exit(1)
    
    # 创建飞书机器人实例
    print("[INFO] 初始化飞书机器人...")
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    print("[SUCCESS] 飞书机器人初始化完成\n")
    
    # 创建组合过滤器
    filter_funcs = []
    
    # 关键词白名单过滤
    if hasattr(config, 'KEYWORDS') and config.KEYWORDS:
        whitelist_filter = create_filter_by_keywords(config.KEYWORDS)
        filter_funcs.append(whitelist_filter)
        print(f"[INFO] 启用关键词白名单过滤: {config.KEYWORDS}")
    
    # 黑名单过滤
    if hasattr(config, 'BLACKLIST_KEYWORDS') and config.BLACKLIST_KEYWORDS:
        blacklist_filter = create_blacklist_filter(config.BLACKLIST_KEYWORDS)
        filter_funcs.append(blacklist_filter)
        print(f"[INFO] 启用关键词黑名单过滤: {config.BLACKLIST_KEYWORDS}")
    
    # 组合多个过滤器
    combined_filter = None
    if filter_funcs:
        def combined_filter(news_item):
            return all(f(news_item) for f in filter_funcs)
    
    print()
    
    # 创建监控器
    monitor = CLSTelegraphMonitor(
        feishu_bot=bot,
        category=getattr(config, 'MESSAGE_CATEGORY', 'important'),
        interval=getattr(config, 'POLL_INTERVAL', 30),
        filter_func=combined_filter
    )
    
    # 注册信号处理器（优雅退出）
    def signal_handler(sig, frame):
        print("\n\n[INFO] 收到退出信号，正在停止服务...")
        monitor.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 显示配置信息
    print("=" * 70)
    print("配置信息:")
    print(f"  消息类型:     {getattr(config, 'MESSAGE_CATEGORY', 'important')}")
    print(f"  轮询间隔:     {getattr(config, 'POLL_INTERVAL', 30)}秒")
    print(f"  关键词白名单: {getattr(config, 'KEYWORDS', None)}")
    print(f"  关键词黑名单: {getattr(config, 'BLACKLIST_KEYWORDS', None)}")
    print(f"  调试模式:     {getattr(config, 'DEBUG', False)}")
    print("=" * 70)
    print()
    
    # 启动监控
    try:
        monitor.start()
    except Exception as e:
        print(f"\n[ERROR] 服务异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
