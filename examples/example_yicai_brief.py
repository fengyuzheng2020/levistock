"""
第一财经快讯 - 使用示例

展示如何使用 news_brief_yicai() 函数获取第一财经快讯
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import levistock as lk


def example_basic_usage():
    """基础用法：获取最新快讯"""
    print("=" * 70)
    print("示例1：基础用法 - 获取最新20条快讯")
    print("=" * 70)
    
    data = lk.news_brief_yicai()
    print(f"\n✓ 成功获取 {len(data)} 条快讯\n")
    
    for i, item in enumerate(data[:5], 1):
        print(f"{i}. [{item['time']}] {item['title']}")
        if item['important']:
            print("   🔴 重要消息")
        print(f"   {item['content'][:80]}...")
        print()


def example_custom_limit():
    """自定义数量：获取指定条数"""
    print("=" * 70)
    print("示例2：自定义数量 - 获取5条快讯")
    print("=" * 70)
    
    data = lk.news_brief_yicai(limit=5)
    print(f"\n✓ 成功获取 {len(data)} 条快讯\n")
    
    for i, item in enumerate(data, 1):
        print(f"{i}. {item['title']}")


def example_filter_important():
    """过滤重要消息"""
    print("=" * 70)
    print("示例3：过滤重要消息")
    print("=" * 70)
    
    data = lk.news_brief_yicai(limit=30)
    important_news = [item for item in data if item['important']]
    
    print(f"\n共获取 {len(data)} 条快讯，其中重要消息 {len(important_news)} 条\n")
    
    if important_news:
        for i, item in enumerate(important_news[:5], 1):
            print(f"{i}. 🔴 [{item['time']}] {item['title']}")
            print(f"   {item['content'][:80]}...")
            print()
    else:
        print("暂无重要消息")


def example_detailed_info():
    """显示详细信息"""
    print("=" * 70)
    print("示例4：显示详细信息")
    print("=" * 70)
    
    data = lk.news_brief_yicai(limit=1)
    
    if data:
        item = data[0]
        print(f"\n标题: {item['title']}")
        print(f"时间: {item['time']}")
        print(f"ID: {item['id']}")
        print(f"重要: {'是' if item['important'] else '否'}")
        print(f"\n内容:")
        print(f"  {item['content']}")
        print(f"\n链接: {item['share_url']}")


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print(" " * 20 + "第一财经快讯 - 使用示例")
    print("=" * 70 + "\n")
    
    try:
        example_basic_usage()
        print("\n")
        
        example_custom_limit()
        print("\n")
        
        example_filter_important()
        print("\n")
        
        example_detailed_info()
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("示例运行完成")
    print("=" * 70 + "\n")
