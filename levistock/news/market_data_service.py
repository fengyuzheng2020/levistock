"""
财联社市场数据 - 定时播报服务（主程序）

使用方法:
1. 确保已配置 config.py
2. 运行: python market_data_service.py
3. 按 Ctrl+C 停止服务
"""

import sys
import os
import signal

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levistock.news.feishu_monitor import FeishuBot
from levistock.news.market_data_bot import MarketDataBot


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


def main():
    """主函数"""
    print("=" * 70)
    print(" " * 15 + "财联社市场数据 - 定时播报服务")
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
    
    # 创建市场数据播报器
    market_bot = MarketDataBot(feishu_bot=bot)
    
    # 注册信号处理器（优雅退出）
    def signal_handler(sig, frame):
        print("\n\n[INFO] 收到退出信号，正在停止服务...")
        market_bot.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 获取播报间隔（默认60秒）
    interval = getattr(config, 'MARKET_DATA_INTERVAL', 60)
    
    # 显示配置信息
    print("=" * 70)
    print("配置信息:")
    print(f"  播报内容:")
    print(f"    1. 今日主线机会 (market_mainline_cls)")
    print(f"    2. 板块热度排行 Top10 (get_sector_heat)")
    print(f"    3. 板块轮动近4日 (get_sector_rotation)")
    print(f"  播报间隔:     {interval}秒")
    print("=" * 70)
    print()
    
    # 启动播报
    try:
        market_bot.start(interval=interval)
    except Exception as e:
        print(f"\n[ERROR] 服务异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
