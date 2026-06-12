"""
测试新浪财经快讯模块
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levistock.news.news_sina import news_brief_sina


def test_news_brief_sina():
    """测试获取新浪财经快讯"""
    print("=" * 70)
    print("测试：获取新浪财经快讯")
    print("=" * 70)
    
    # 测试1：获取默认20条
    print("\n[TEST 1] 获取默认20条快讯...")
    try:
        data = news_brief_sina()
        print(f"✓ 成功获取 {len(data)} 条快讯")
        
        if data:
            print("\n最新3条快讯：")
            for i, item in enumerate(data[:3], 1):
                print(f"\n{i}. [{item['time']}] {item['title']}")
                print(f"   内容: {item['content'][:100]}...")
                print(f"   来源: {item['source']}")
                print(f"   阅读: {item['view_num']}")
    except Exception as e:
        print(f"✗ 失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试2：获取指定数量
    print("\n\n[TEST 2] 获取5条快讯...")
    try:
        data = news_brief_sina(limit=5)
        print(f"✓ 成功获取 {len(data)} 条快讯")
        
        if data:
            print("\n快讯列表：")
            for i, item in enumerate(data, 1):
                print(f"{i}. [{item['time']}] {item['title'][:50]}")
    except Exception as e:
        print(f"✗ 失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试3：验证数据结构
    print("\n\n[TEST 3] 验证数据结构...")
    try:
        data = news_brief_sina(limit=1)
        if data:
            item = data[0]
            required_fields = ['id', 'title', 'content', 'time', 'source', 'view_num']
            
            missing_fields = [f for f in required_fields if f not in item]
            if missing_fields:
                print(f"✗ 缺少字段: {missing_fields}")
            else:
                print("✓ 数据结构完整，包含所有必需字段")
            
            print(f"\n完整数据示例：")
            for key, value in item.items():
                if isinstance(value, str) and len(value) > 100:
                    print(f"  {key}: {value[:100]}...")
                else:
                    print(f"  {key}: {value}")
    except Exception as e:
        print(f"✗ 失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("测试完成")
    print("=" * 70)


if __name__ == "__main__":
    test_news_brief_sina()
