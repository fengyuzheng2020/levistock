"""
快速测试第一财经快讯功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levistock.news.news_yicai import news_brief_yicai


def quick_test():
    """快速测试"""
    print("=" * 70)
    print("快速测试：第一财经快讯")
    print("=" * 70)
    
    try:
        print("\n[1] 尝试获取 3 条快讯...")
        data = news_brief_yicai(limit=3)
        
        print(f"\n✓ 成功获取 {len(data)} 条数据\n")
        
        if not data:
            print("⚠️  警告：返回的数据为空列表")
            print("可能原因：")
            print("  1. API 接口变化")
            print("  2. 网络连接问题")
            print("  3. 数据解析错误")
            return
        
        for i, item in enumerate(data, 1):
            print(f"{i}. [{item['time']}] {item['title']}")
            print(f"   ID: {item['id']}")
            print(f"   重要: {item['important']}")
            print(f"   内容: {item['content'][:80]}...")
            print(f"   链接: {item['share_url']}")
            print()
            
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 70)


if __name__ == "__main__":
    quick_test()
