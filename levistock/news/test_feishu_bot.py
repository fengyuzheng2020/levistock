"""
飞书机器人测试脚本

用于测试飞书机器人配置是否正确
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levistock.news.feishu_monitor import FeishuBot


def load_config():
    """加载配置文件"""
    config_path = os.path.join(os.path.dirname(__file__), "config.py")
    
    if not os.path.exists(config_path):
        print(f"[ERROR] 配置文件不存在: {config_path}")
        print(f"[INFO] 请复制 config_example.py 为 config.py 并配置")
        return None
    
    import importlib.util
    spec = importlib.util.spec_from_file_location("config", config_path)
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)
    
    return config


def test_text_message(bot: FeishuBot):
    """测试文本消息"""
    print("\n[TEST] 发送文本消息...")
    
    text = """🔔 财联社电报快讯 - 测试消息

这是一条测试消息，用于验证飞书机器人配置是否正确。

如果收到此消息，说明配置成功！✅"""
    
    result = bot.send_text(text)
    print(f"响应: {result}")
    
    if result.get("code") == 0:
        print("[SUCCESS] 文本消息发送成功 ✅")
        return True
    else:
        print(f"[FAILED] 文本消息发送失败 ❌")
        return False


def test_post_message(bot: FeishuBot):
    """测试富文本消息"""
    print("\n[TEST] 发送富文本消息...")
    
    title = "财联社电报快讯 - 测试"
    content_list = [
        [{"tag": "text", "text": "⏰ 时间: 2026-06-12 14:30:00"}],
        [{"tag": "text", "text": "📰 标题: 测试消息标题"}],
        [{"tag": "text", "text": "📝 内容: 这是一条测试消息，用于验证富文本格式。"}],
        [{"tag": "text", "text": "---"}],
        [{"tag": "text", "text": "如果收到此消息，说明配置成功！✅"}],
    ]
    
    result = bot.send_post(title=title, content_list=content_list)
    print(f"响应: {result}")
    
    if result.get("code") == 0:
        print("[SUCCESS] 富文本消息发送成功 ✅")
        return True
    else:
        print(f"[FAILED] 富文本消息发送失败 ❌")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("  飞书机器人配置测试")
    print("=" * 60)
    
    # 加载配置
    config = load_config()
    if not config:
        sys.exit(1)
    
    # 验证配置
    if not hasattr(config, 'FEISHU_WEBHOOK_URL') or \
       config.FEISHU_WEBHOOK_URL == "https://open.feishu.cn/open-apis/bot/v2/hook/your_webhook_token_here":
        print("[ERROR] 请配置 FEISHU_WEBHOOK_URL")
        print("[INFO] 编辑 config.py 文件，填写你的飞书机器人 Webhook URL")
        sys.exit(1)
    
    # 创建机器人实例
    bot = FeishuBot(
        webhook_url=config.FEISHU_WEBHOOK_URL,
        secret=getattr(config, 'FEISHU_SECRET', None)
    )
    
    print("[INFO] 开始测试...\n")
    
    # 测试文本消息
    success1 = test_text_message(bot)
    
    # 等待一下
    import time
    time.sleep(1)
    
    # 测试富文本消息
    success2 = test_post_message(bot)
    
    # 总结
    print("\n" + "=" * 60)
    if success1 and success2:
        print("[SUCCESS] 所有测试通过！✅")
        print("[INFO] 可以启动正式服务了: python3 feishu_monitor_service.py")
    else:
        print("[FAILED] 部分测试失败 ❌")
        print("[INFO] 请检查配置和网络连接")
    print("=" * 60)


if __name__ == "__main__":
    main()
