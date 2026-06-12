"""
市场数据播报 - 测试脚本

用于测试三个数据接口是否正常
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_market_mainline():
    """测试主线机会接口"""
    print("\n" + "=" * 70)
    print("[TEST 1] 测试 market_mainline_cls()")
    print("=" * 70)
    
    try:
        from levistock.market.market_wind_cls import market_mainline_cls
        
        data = market_mainline_cls()
        print(f"[SUCCESS] 获取成功")
        print(f"数据类型: {type(data)}")
        
        if data:
            print(f"\n数据结构预览:")
            for key in list(data.keys())[:5]:
                print(f"  - {key}: {type(data[key])}")
            
            # 显示主线1的信息
            if "faucet_1" in data:
                faucet_1 = data["faucet_1"]
                print(f"\n主线1:")
                print(f"  标题: {faucet_1.get('title', 'N/A')}")
                print(f"  描述: {faucet_1.get('desc', 'N/A')[:100]}...")
        else:
            print("[WARN] 返回数据为空（可能是非交易时间）")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sector_heat():
    """测试板块热度接口"""
    print("\n" + "=" * 70)
    print("[TEST 2] 测试 get_sector_heat()")
    print("=" * 70)
    
    try:
        from levistock.sector.sector_heat_cls import get_sector_heat
        
        data = get_sector_heat()
        print(f"[SUCCESS] 获取成功")
        print(f"板块数量: {len(data)}")
        
        if data:
            print(f"\nTop 5 热门板块:")
            for i, item in enumerate(data[:5], 1):
                plate_name = item.get("plate_name", "")
                cur_heat = item.get("cur_heat", 0)
                rank_change = item.get("rank_change", 0)
                
                change_str = f"↑{rank_change}" if rank_change > 0 else (f"↓{abs(rank_change)}" if rank_change < 0 else "-")
                print(f"  {i}. {plate_name:<12} 热度:{cur_heat:>6.1f}  变化:{change_str}")
        else:
            print("[WARN] 返回数据为空")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sector_rotation():
    """测试板块轮动接口"""
    print("\n" + "=" * 70)
    print("[TEST 3] 测试 get_sector_rotation()")
    print("=" * 70)
    
    try:
        from levistock.sector.sector_rotation_cls import get_sector_rotation
        
        data = get_sector_rotation(days=4)
        print(f"[SUCCESS] 获取成功")
        print(f"天数: {len(data)}")
        
        if data:
            print(f"\n最近交易日板块轮动:")
            for day_data in data[:2]:  # 只显示最近2天
                trade_date = day_data.get("trade_date", "")
                plates = day_data.get("plates", [])
                
                print(f"\n  📅 {trade_date}")
                for i, plate in enumerate(plates[:3], 1):  # 每天只显示前3个
                    plate_name = plate.get("plate_name", "")
                    change = plate.get("change", 0)
                    change_str = f"+{change:.2f}%" if change > 0 else f"{change:.2f}%"
                    print(f"    {i}. {plate_name:<12} {change_str}")
        else:
            print("[WARN] 返回数据为空")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_feishu_format():
    """测试飞书消息格式化"""
    print("\n" + "=" * 70)
    print("[TEST 4] 测试消息格式化")
    print("=" * 70)
    
    try:
        from levistock.news.feishu_monitor import FeishuBot
        from levistock.news.market_data_bot import MarketDataBot
        
        # 创建临时的 bot 实例（不需要真实的 webhook）
        class MockBot:
            def send_text(self, text):
                print(f"\n[MOCK] 模拟发送消息（长度: {len(text)} 字符）")
                print(f"消息预览:\n{text[:500]}...")
                return {"code": 0}
        
        mock_bot = MockBot()
        market_bot = MarketDataBot(feishu_bot=mock_bot)
        
        # 获取真实数据并格式化
        from levistock.market.market_wind_cls import market_mainline_cls
        from levistock.sector.sector_heat_cls import get_sector_heat
        from levistock.sector.sector_rotation_cls import get_sector_rotation
        
        mainline_data = market_mainline_cls()
        heat_data = get_sector_heat()
        rotation_data = get_sector_rotation(days=4)
        
        # 格式化
        mainline_text = market_bot._format_mainline(mainline_data)
        heat_text = market_bot._format_sector_heat(heat_data, top_n=5)
        rotation_text = market_bot._format_sector_rotation(rotation_data)
        
        print(f"\n[SUCCESS] 格式化成功")
        print(f"  主线机会: {len(mainline_text)} 字符")
        print(f"  板块热度: {len(heat_text)} 字符")
        print(f"  板块轮动: {len(rotation_text)} 字符")
        
        # 模拟发送
        market_bot.send_market_report()
        
        return True
        
    except Exception as e:
        print(f"[ERROR] 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    print("=" * 70)
    print(" " * 20 + "市场数据播报 - 测试套件")
    print("=" * 70)
    
    results = []
    
    # 测试1：主线机会
    results.append(("主线机会", test_market_mainline()))
    
    # 测试2：板块热度
    results.append(("板块热度", test_sector_heat()))
    
    # 测试3：板块轮动
    results.append(("板块轮动", test_sector_rotation()))
    
    # 测试4：消息格式化
    results.append(("消息格式化", test_feishu_format()))
    
    # 总结
    print("\n" + "=" * 70)
    print("测试结果总结:")
    print("=" * 70)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
        if not result:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n[SUCCESS] 所有测试通过！可以启动服务了。")
        print("[INFO] 运行: python3 market_data_service.py")
    else:
        print("\n[FAILED] 部分测试失败，请检查错误信息。")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
