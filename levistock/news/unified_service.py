"""
财联社飞书推送 - 统一服务

功能：
- 通过配置开关控制开启/关闭不同播报功能
- 支持电报快讯监控
- 支持市场数据定时播报（主线机会、板块热度、板块轮动）
- 单一入口，统一管理

使用方法：
    python3 unified_service.py
"""

import sys
import os
import time
import signal
import datetime
from multiprocessing import Process

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_config():
    """加载配置文件"""
    # 获取项目根目录（levistock 的父目录）
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(project_root, "config", "config.py")
    
    if not os.path.exists(config_path):
        print(f"[ERROR] 配置文件不存在: {config_path}")
        print(f"[INFO] 请复制 config_example.py 为 config/config.py 并配置")
        sys.exit(1)
    
    # 动态导入配置
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    return config


def check_config(config):
    """检查必要配置"""
    if not hasattr(config, 'FEISHU_WEBHOOK_URL') or \
       config.FEISHU_WEBHOOK_URL == "https://open.feishu.cn/open-apis/bot/v2/hook/your_webhook_token_here":
        print("[ERROR] 请配置 FEISHU_WEBHOOK_URL")
        print("[INFO] 编辑 config.py 文件，填写你的飞书机器人 Webhook URL")
        sys.exit(1)


def run_news_monitor():
    """运行电报监控服务"""
    from levistock.news.feishu_monitor import FeishuBot, CLSTelegraphMonitor
    
    # 重新加载配置
    config = load_config()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "启动电报快讯监控")
    print("=" * 70)
    
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    
    # 创建过滤器
    filter_func = None
    if hasattr(config, 'KEYWORDS') and config.KEYWORDS:
        from levistock.news.feishu_monitor import create_filter_by_keywords
        filter_func = create_filter_by_keywords(config.KEYWORDS)
    
    monitor = CLSTelegraphMonitor(
        feishu_bot=bot,
        category=getattr(config, 'MESSAGE_CATEGORY', 'important'),
        interval=getattr(config, 'POLL_INTERVAL', 30),
        filter_func=filter_func
    )
    
    try:
        monitor.start()
    except KeyboardInterrupt:
        print("\n[INFO] 电报监控服务已停止")
    except Exception as e:
        print(f"\n[ERROR] 电报监控服务异常: {e}")
        import traceback
        traceback.print_exc()


def run_market_report():
    """运行市场数据播报服务"""
    from levistock.news.feishu_monitor import FeishuBot
    from levistock.news.market_data_bot import MarketDataBot
    
    # 重新加载配置
    config = load_config()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "启动市场数据播报")
    print("=" * 70)
    
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    
    market_bot = MarketDataBot(feishu_bot=bot)
    
    try:
        market_bot.start(interval=getattr(config, 'MARKET_DATA_INTERVAL', 60))
    except KeyboardInterrupt:
        print("\n[INFO] 市场数据播报服务已停止")
    except Exception as e:
        print(f"\n[ERROR] 市场数据播报服务异常: {e}")
        import traceback
        traceback.print_exc()


def run_market_wind_report():
    """运行风口板块播报服务"""
    from levistock.news.feishu_monitor import FeishuBot
    from levistock.market.market_wind_bot import MarketWindBot
    
    # 重新加载配置
    config = load_config()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "启动风口板块播报")
    print("=" * 70)
    
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    
    wind_bot = MarketWindBot(feishu_bot=bot)
    
    try:
        wind_bot.start(
            interval=getattr(config, 'MARKET_WIND_INTERVAL', 300),
            include_stocks=getattr(config, 'MARKET_WIND_INCLUDE_STOCKS', True)
        )
    except KeyboardInterrupt:
        print("\n[INFO] 风口板块播报服务已停止")
    except Exception as e:
        print(f"\n[ERROR] 风口板块播报服务异常: {e}")
        import traceback
        traceback.print_exc()


def run_yicai_monitor():
    """运行第一财经快讯监控服务"""
    from levistock.news.feishu_monitor import FeishuBot
    from levistock.news.yicai_monitor import YicaiBriefMonitor
    
    # 重新加载配置
    config = load_config()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "启动第一财经快讯监控")
    print("=" * 70)
    
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    
    # 创建过滤器
    filter_func = None
    if hasattr(config, 'YICAI_KEYWORDS') and config.YICAI_KEYWORDS:
        from levistock.news.yicai_monitor import create_filter_by_keywords
        filter_func = create_filter_by_keywords(config.YICAI_KEYWORDS)
    
    monitor = YicaiBriefMonitor(
        feishu_bot=bot,
        interval=getattr(config, 'YICAI_POLL_INTERVAL', 30),
        filter_func=filter_func
    )
    
    try:
        monitor.start()
    except KeyboardInterrupt:
        print("\n[INFO] 第一财经快讯监控服务已停止")
    except Exception as e:
        print(f"\n[ERROR] 第一财经快讯监控服务异常: {e}")
        import traceback
        traceback.print_exc()


def run_sina_monitor():
    """运行新浪财经快讯监控服务"""
    from levistock.news.feishu_monitor import FeishuBot
    from levistock.news.sina_monitor import SinaBriefMonitor
    
    # 重新加载配置
    config = load_config()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "启动新浪财经快讯监控")
    print("=" * 70)
    
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    
    # 创建过滤器
    filter_func = None
    if hasattr(config, 'SINA_KEYWORDS') and config.SINA_KEYWORDS:
        from levistock.news.sina_monitor import create_filter_by_keywords
        filter_func = create_filter_by_keywords(config.SINA_KEYWORDS)
    
    monitor = SinaBriefMonitor(
        feishu_bot=bot,
        interval=getattr(config, 'SINA_POLL_INTERVAL', 30),
        filter_func=filter_func
    )
    
    try:
        monitor.start()
    except KeyboardInterrupt:
        print("\n[INFO] 新浪财经快讯监控服务已停止")
    except Exception as e:
        print(f"\n[ERROR] 新浪财经快讯监控服务异常: {e}")
        import traceback
        traceback.print_exc()


def run_em_monitor():
    """运行东方财富快讯监控服务"""
    from levistock.news.feishu_monitor import FeishuBot
    from levistock.news.em_monitor import EMBriefMonitor
    
    # 重新加载配置
    config = load_config()
    
    print("\n" + "=" * 70)
    print(" " * 20 + "启动东方财富快讯监控")
    print("=" * 70)
    
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    
    # 创建过滤器
    filter_func = None
    if hasattr(config, 'EM_KEYWORDS') and config.EM_KEYWORDS:
        from levistock.news.em_monitor import create_filter_by_keywords
        filter_func = create_filter_by_keywords(config.EM_KEYWORDS)
    
    monitor = EMBriefMonitor(
        feishu_bot=bot,
        interval=getattr(config, 'EM_POLL_INTERVAL', 30),
        filter_func=filter_func
    )
    
    try:
        monitor.start()
    except KeyboardInterrupt:
        print("\n[INFO] 东方财富快讯监控服务已停止")
    except Exception as e:
        print(f"\n[ERROR] 东方财富快讯监控服务异常: {e}")
        import traceback
        traceback.print_exc()


def main():
    """主函数"""
    print("=" * 70)
    print(" " * 15 + "财联社飞书推送 - 统一服务")
    print("=" * 70)
    
    # 加载配置
    try:
        config = load_config()
        print("[SUCCESS] 配置文件加载成功\n")
    except Exception as e:
        print(f"[ERROR] 配置文件加载失败: {e}")
        sys.exit(1)
    
    # 检查配置
    check_config(config)
    
    # 读取功能开关
    enable_news = getattr(config, 'ENABLE_NEWS_MONITOR', True)
    enable_market = getattr(config, 'ENABLE_MARKET_REPORT', True)
    enable_wind = getattr(config, 'ENABLE_MARKET_WIND', False)  # 新增：风口板块播报
    enable_yicai = getattr(config, 'ENABLE_YICAI_MONITOR', False)  # 新增：第一财经快讯
    enable_sina = getattr(config, 'ENABLE_SINA_MONITOR', False)  # 新增：新浪财经快讯
    enable_em = getattr(config, 'ENABLE_EM_MONITOR', False)  # 新增：东方财富快讯
    
    # 显示配置信息
    print("=" * 70)
    print("功能配置:")
    print(f"  电报快讯监控: {'✅ 开启' if enable_news else '❌ 关闭'}")
    if enable_news:
        print(f"    - 消息类型: {getattr(config, 'MESSAGE_CATEGORY', 'important')}")
        print(f"    - 轮询间隔: {getattr(config, 'POLL_INTERVAL', 30)}秒")
        keywords = getattr(config, 'KEYWORDS', None)
        if keywords:
            print(f"    - 关键词过滤: {keywords}")
    
    print(f"  市场数据播报: {'✅ 开启' if enable_market else '❌ 关闭'}")
    if enable_market:
        print(f"    - 播报间隔: {getattr(config, 'MARKET_DATA_INTERVAL', 60)}秒")
        print(f"    - 播报内容:")
        print(f"      1. 今日主线机会")
        print(f"      2. 板块热度排行 Top10")
        print(f"      3. 板块轮动近4日")
    
    print(f"  风口板块播报: {'✅ 开启' if enable_wind else '❌ 关闭'}")
    if enable_wind:
        print(f"    - 播报间隔: {getattr(config, 'MARKET_WIND_INTERVAL', 300)}秒")
        print(f"    - 包含龙头股: {'是' if getattr(config, 'MARKET_WIND_INCLUDE_STOCKS', True) else '否'}")
        print(f"    - 播报内容:")
        print(f"      1. 今日风口板块列表")
        if getattr(config, 'MARKET_WIND_INCLUDE_STOCKS', True):
            print(f"      2. 风口板块龙头股")
        print(f"      3. 今日主线机会")
    
    print(f"  第一财经快讯: {'✅ 开启' if enable_yicai else '❌ 关闭'}")
    if enable_yicai:
        print(f"    - 轮询间隔: {getattr(config, 'YICAI_POLL_INTERVAL', 30)}秒")
        keywords = getattr(config, 'YICAI_KEYWORDS', None)
        if keywords:
            print(f"    - 关键词过滤: {keywords}")
    
    print(f"  新浪财经快讯: {'✅ 开启' if enable_sina else '❌ 关闭'}")
    if enable_sina:
        print(f"    - 轮询间隔: {getattr(config, 'SINA_POLL_INTERVAL', 30)}秒")
        keywords = getattr(config, 'SINA_KEYWORDS', None)
        if keywords:
            print(f"    - 关键词过滤: {keywords}")
    
    print(f"  东方财富快讯: {'✅ 开启' if enable_em else '❌ 关闭'}")
    if enable_em:
        print(f"    - 轮询间隔: {getattr(config, 'EM_POLL_INTERVAL', 30)}秒")
        keywords = getattr(config, 'EM_KEYWORDS', None)
        if keywords:
            print(f"    - 关键词过滤: {keywords}")
    
    print("=" * 70)
    print()
    
    # 检查是否至少开启一个功能
    if not enable_news and not enable_market and not enable_wind and not enable_yicai and not enable_sina and not enable_em:
        print("[ERROR] 至少需要开启一个功能")
        print("[INFO] 请在 config.py 中设置 ENABLE_NEWS_MONITOR、ENABLE_MARKET_REPORT、ENABLE_MARKET_WIND、ENABLE_YICAI_MONITOR、ENABLE_SINA_MONITOR 或 ENABLE_EM_MONITOR 为 True")
        sys.exit(1)
    
    # 注册信号处理器
    processes = []
    
    def signal_handler(sig, frame):
        print("\n\n[INFO] 收到退出信号，正在停止服务...")
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join()
        print("[INFO] 所有服务已停止")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动服务
    processes = []
    
    # 统计开启的服务数量
    enabled_count = sum([enable_news, enable_market, enable_wind, enable_yicai, enable_sina, enable_em])
    
    if enabled_count == 1:
        # 只开启一个服务，直接运行
        if enable_news:
            print("[INFO] 启动电报监控服务...\n")
            run_news_monitor()
        elif enable_market:
            print("[INFO] 启动市场数据播报服务...\n")
            run_market_report()
        elif enable_wind:
            print("[INFO] 启动风口板块播报服务...\n")
            run_market_wind_report()
        elif enable_yicai:
            print("[INFO] 启动第一财经快讯监控服务...\n")
            run_yicai_monitor()
        elif enable_sina:
            print("[INFO] 启动新浪财经快讯监控服务...\n")
            run_sina_monitor()
        elif enable_em:
            print("[INFO] 启动东方财富快讯监控服务...\n")
            run_em_monitor()
    
    else:
        # 开启多个服务，使用多进程
        print(f"[INFO] 同时启动 {enabled_count} 个服务...\n")
        
        if enable_news:
            p = Process(target=run_news_monitor)
            processes.append(p)
        
        if enable_market:
            p = Process(target=run_market_report)
            processes.append(p)
        
        if enable_wind:
            p = Process(target=run_market_wind_report)
            processes.append(p)
        
        if enable_yicai:
            p = Process(target=run_yicai_monitor)
            processes.append(p)
        
        if enable_sina:
            p = Process(target=run_sina_monitor)
            processes.append(p)
        
        if enable_em:
            p = Process(target=run_em_monitor)
            processes.append(p)
        
        # 依次启动进程
        for i, p in enumerate(processes):
            p.start()
            if i < len(processes) - 1:
                time.sleep(2)  # 错开启动时间
        
        try:
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            signal_handler(None, None)


if __name__ == "__main__":
    main()
