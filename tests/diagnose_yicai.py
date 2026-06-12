"""
第一财经快讯 - 完整诊断工具

用于排查为什么没有推送消息
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def diagnose():
    """完整诊断"""
    print("=" * 70)
    print(" " * 20 + "第一财经快讯 - 诊断工具")
    print("=" * 70)
    
    # 1. 测试数据获取
    print("\n[步骤 1] 测试数据获取...")
    try:
        from levistock.news.news_yicai import news_brief_yicai
        data = news_brief_yicai(limit=5)
        
        if not data:
            print("✗ 失败：未获取到任何数据")
            print("\n可能原因：")
            print("  1. API 接口已变化")
            print("  2. 网络连接问题")
            print("  3. 数据解析错误")
            return False
        
        print(f"✓ 成功获取 {len(data)} 条数据")
        print(f"\n第一条数据示例：")
        first = data[0]
        for key, value in first.items():
            if isinstance(value, str) and len(value) > 100:
                print(f"  {key}: {value[:100]}...")
            else:
                print(f"  {key}: {value}")
                
    except Exception as e:
        print(f"✗ 失败：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 2. 测试飞书机器人
    print("\n[步骤 2] 测试飞书机器人配置...")
    try:
        config_path = os.path.join(os.path.dirname(__file__), "..", "news", "config.py")
        
        if not os.path.exists(config_path):
            print(f"✗ 配置文件不存在: {config_path}")
            return False
        
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        webhook_url = getattr(config, 'FEISHU_WEBHOOK_URL', None)
        
        if not webhook_url or "your_webhook_token_here" in webhook_url:
            print("✗ 飞书 Webhook URL 未配置")
            print(f"  当前值: {webhook_url}")
            print("  请在 config.py 中配置正确的 FEISHU_WEBHOOK_URL")
            return False
        
        print(f"✓ Webhook URL 已配置")
        print(f"  URL: {webhook_url[:50]}...")
        
        # 测试发送一条消息
        from levistock.news.feishu_monitor import FeishuBot
        bot = FeishuBot(
            webhook_url=webhook_url,
            secret=getattr(config, 'FEISHU_SECRET', None)
        )
        
        print("\n  发送测试消息...")
        result = bot.send_text("🔔 第一财经快讯诊断测试\n这是一条测试消息")
        
        if result.get("code") == 0:
            print("  ✓ 测试消息发送成功")
        else:
            print(f"  ✗ 测试消息发送失败: {result}")
            if result.get("code") == 11232:
                print("  ⚠️  频率限制：请等待几分钟后再试")
            return False
            
    except Exception as e:
        print(f"✗ 失败：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 3. 测试监控器
    print("\n[步骤 3] 测试监控器初始化...")
    try:
        from levistock.news.yicai_monitor import YicaiBriefMonitor
        
        monitor = YicaiBriefMonitor(
            feishu_bot=bot,
            interval=30,
            filter_func=None
        )
        
        print("✓ 监控器初始化成功")
        
        # 测试获取最新消息
        print("\n  测试获取最新消息...")
        latest = monitor._fetch_latest_news(limit=3)
        
        if not latest:
            print("  ✗ 未获取到消息")
            return False
        
        print(f"  ✓ 获取到 {len(latest)} 条消息")
        
        # 检查消息ID
        for i, msg in enumerate(latest, 1):
            msg_id = msg.get("id", 0)
            print(f"  消息{i}: ID={msg_id}, 标题={msg.get('title', '')[:30]}")
            
            if not msg_id:
                print(f"    ⚠️  警告：消息{i} 缺少ID")
        
    except Exception as e:
        print(f"✗ 失败：{e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 4. 总结
    print("\n" + "=" * 70)
    print("诊断结果：✅ 所有检查通过")
    print("=" * 70)
    print("\n建议操作：")
    print("1. 启动监控服务：python yicai_monitor.py")
    print("2. 观察日志输出，查看是否有新消息")
    print("3. 如果还是没有推送，可能是：")
    print("   - 所有消息都已被标记为已读（seen_ids）")
    print("   - 需要等待新的消息产生")
    print("   - 关键词过滤太严格")
    print("\n调试技巧：")
    print("- 查看 [DEBUG] 日志了解详细流程")
    print("- 检查 [WARNING] 和 [ERROR] 日志")
    print("- 确认 seen_ids 的数量是否正常")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    diagnose()
