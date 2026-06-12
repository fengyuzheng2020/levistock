"""
测试东方财富快讯接口
"""

import sys
sys.path.insert(0, '/Users/zyb/data/my/project/levistock')

from levistock.news.news_em import news_brief_em


def test_news_brief_em():
    """测试获取东方财富快讯"""
    
    print("=" * 70)
    print("测试1: 获取默认20条快讯")
    print("=" * 70)
    
    try:
        data = news_brief_em()
        print(f"✓ 成功获取 {len(data)} 条快讯\n")
        
        if len(data) > 0:
            print("最新3条快讯:\n")
            for i, item in enumerate(data[:3], 1):
                print(f"{i}. [{item['time']}]")
                print(f"   标题: {item['title']}")
                print(f"   内容: {item['content'][:100]}...")
                print(f"   ID: {item['code']}")
                if item['stock_list']:
                    stocks = ", ".join([s.get('name', '') for s in item['stock_list'][:3]])
                    print(f"   相关股票: {stocks}")
                print()
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("测试2: 获取5条快讯")
    print("=" * 70)
    
    try:
        data = news_brief_em(limit=5)
        print(f"✓ 成功获取 {len(data)} 条快讯\n")
        
        if len(data) > 0:
            print("快讯列表:\n")
            for i, item in enumerate(data, 1):
                print(f"{i}. [{item['time']}] {item['title'][:60]}")
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)


if __name__ == "__main__":
    test_news_brief_em()
