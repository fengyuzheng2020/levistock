"""
统一服务 - 配置测试脚本

用于验证配置是否正确
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_config():
    """测试配置文件"""
    print("=" * 70)
    print(" " * 25 + "配置测试")
    print("=" * 70)
    print()
    
    # 加载配置
    config_path = os.path.join(os.path.dirname(__file__), "config.py")
    
    if not os.path.exists(config_path):
        print("[ERROR] 配置文件不存在")
        print("[INFO] 请复制 config_example.py 为 config.py")
        return False
    
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    print("[SUCCESS] 配置文件加载成功\n")
    
    # 检查必要配置
    errors = []
    
    # 1. 检查 Webhook URL
    if not hasattr(config, 'FEISHU_WEBHOOK_URL'):
        errors.append("缺少 FEISHU_WEBHOOK_URL 配置")
    elif config.FEISHU_WEBHOOK_URL == "https://open.feishu.cn/open-apis/bot/v2/hook/your_webhook_token_here":
        errors.append("FEISHU_WEBHOOK_URL 未配置，请填写实际的 Webhook URL")
    
    # 2. 检查功能开关
    enable_news = getattr(config, 'ENABLE_NEWS_MONITOR', None)
    enable_market = getattr(config, 'ENABLE_MARKET_REPORT', None)
    enable_wind = getattr(config, 'ENABLE_MARKET_WIND', None)  # 新增
    
    if enable_news is None:
        errors.append("缺少 ENABLE_NEWS_MONITOR 配置")
    
    if enable_market is None:
        errors.append("缺少 ENABLE_MARKET_REPORT 配置")
    
    if enable_wind is None:
        errors.append("缺少 ENABLE_MARKET_WIND 配置")
    
    if enable_news is False and enable_market is False and enable_wind is False:
        errors.append("至少需要开启一个功能（ENABLE_NEWS_MONITOR、ENABLE_MARKET_REPORT 或 ENABLE_MARKET_WIND）")
    
    # 3. 检查电报监控配置（如果开启）
    if enable_news:
        if not hasattr(config, 'MESSAGE_CATEGORY'):
            errors.append("开启电报监控但缺少 MESSAGE_CATEGORY 配置")
        
        if not hasattr(config, 'POLL_INTERVAL'):
            errors.append("开启电报监控但缺少 POLL_INTERVAL 配置")
    
    # 4. 检查市场数据配置（如果开启）
    if enable_market:
        if not hasattr(config, 'MARKET_DATA_INTERVAL'):
            errors.append("开启市场数据播报但缺少 MARKET_DATA_INTERVAL 配置")
    
    # 5. 检查风口板块配置（如果开启）
    if enable_wind:
        if not hasattr(config, 'MARKET_WIND_INTERVAL'):
            errors.append("开启风口板块播报但缺少 MARKET_WIND_INTERVAL 配置")
    
    # 显示配置信息
    print("当前配置:")
    print("-" * 70)
    print(f"FEISHU_WEBHOOK_URL: {getattr(config, 'FEISHU_WEBHOOK_URL', '未配置')[:50]}...")
    print(f"FEISHU_SECRET: {'已配置' if getattr(config, 'FEISHU_SECRET', None) else '未配置'}")
    print()
    print(f"ENABLE_NEWS_MONITOR: {enable_news}")
    if enable_news:
        print(f"  MESSAGE_CATEGORY: {getattr(config, 'MESSAGE_CATEGORY', 'N/A')}")
        print(f"  POLL_INTERVAL: {getattr(config, 'POLL_INTERVAL', 'N/A')}秒")
        keywords = getattr(config, 'KEYWORDS', None)
        print(f"  KEYWORDS: {keywords if keywords else '无'}")
    print()
    print(f"ENABLE_MARKET_REPORT: {enable_market}")
    if enable_market:
        print(f"  MARKET_DATA_INTERVAL: {getattr(config, 'MARKET_DATA_INTERVAL', 'N/A')}秒")
    print()
    print(f"ENABLE_MARKET_WIND: {enable_wind}")
    if enable_wind:
        print(f"  MARKET_WIND_INTERVAL: {getattr(config, 'MARKET_WIND_INTERVAL', 'N/A')}秒")
        include_stocks = getattr(config, 'MARKET_WIND_INCLUDE_STOCKS', 'N/A')
        print(f"  MARKET_WIND_INCLUDE_STOCKS: {include_stocks}")
    print("-" * 70)
    print()
    
    # 显示结果
    if errors:
        print("[FAILED] 配置检查失败:\n")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        print()
        return False
    else:
        print("[SUCCESS] 配置检查通过！\n")
        
        # 显示将要启动的功能
        print("将要启动的功能:")
        if enable_news:
            print("  ✅ 电报快讯监控")
        if enable_market:
            print("  ✅ 市场数据播报")
        if enable_wind:
            print("  ✅ 风口板块播报")
        print()
        
        print("[INFO] 可以运行以下命令启动服务:")
        print("  python3 unified_service.py")
        print()
        
        return True


def main():
    """主函数"""
    success = test_config()
    
    if success:
        print("=" * 70)
        print("配置正确，可以启动服务了！")
        print("=" * 70)
        sys.exit(0)
    else:
        print("=" * 70)
        print("请修复配置错误后重试")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
