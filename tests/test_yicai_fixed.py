"""
测试修复后的第一财经快讯功能
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from levistock.news.news_yicai import news_brief_yicai


def test_fixed():
    """测试修复后的功能"""
    print("=" * 70)
    print("测试：修复后的第一财经快讯")
    print("=" * 70)
    
    try:
        print("\n[1] 尝试获取 5 条快讯...")
        data = news_brief_yicai(limit=5)
        
        print(f"\n结果：获取到 {len(data)} 条数据\n")
        
        if not data:
            print("✗ 失败：仍然没有数据")
            print("\n请运行 test_yicai_api.py 查看 API 响应结构")
            return False
        
        print("✓ 成功！数据显示如下：\n")
        
        for i, item in enumerate(data, 1):
            print(f"{i}. [{item['time']}] {item['title']}")
            print(f"   ID: {item['id']}")
            print(f"   重要: {'是' if item['important'] else '否'}")
            content_preview = item['content'][:80].replace('\n', ' ').replace('<br />', ' ')
            print(f"   内容: {content_preview}...")
            if item['share_url']:
                print(f"   链接: {item['share_url']}")
            print()
        
        print("=" * 70)
        print("✅ 修复成功！第一财经快讯功能正常工作")
        print("=" * 70)
        return True
            
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_fixed()
    sys.exit(0 if success else 1)
