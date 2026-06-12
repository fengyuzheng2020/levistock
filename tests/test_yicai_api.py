"""
测试第一财经 API 响应结构
"""

import requests
import json


def test_api_response():
    """测试 API 响应"""
    url = "https://www.yicai.com/api/ajax/getbrieflist"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Referer": "https://www.yicai.com/brief/",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "*/*",
    }
    
    params = {
        "page": 1,
        "pagesize": 5,
        "type": 0,
        "id": 0,
    }
    
    print("=" * 70)
    print("测试第一财经 API 响应")
    print("=" * 70)
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        
        print(f"\n状态码: {resp.status_code}")
        print(f"响应头: {dict(resp.headers)}")
        
        # 尝试解析 JSON
        data = resp.json()
        
        print(f"\n响应类型: {type(data)}")
        
        if isinstance(data, list):
            print(f"✓ 直接返回列表，长度: {len(data)}")
            if len(data) > 0:
                print(f"  第一条数据键: {list(data[0].keys())}")
                print(f"\n完整响应结构（前1000字符）:")
                print(json.dumps(data[0], ensure_ascii=False, indent=2)[:1000])
        elif isinstance(data, dict):
            print(f"✓ 返回字典")
            print(f"\n顶层键: {list(data.keys())}")
            print(f"\n完整响应结构（前2000字符）:")
            print(json.dumps(data, ensure_ascii=False, indent=2)[:2000])
            
            # 检查可能的数据结构
            for key in ['data', 'result', 'list', 'items', 'briefs']:
                if key in data:
                    value = data[key]
                    print(f"\n✓ 找到 '{key}' 键")
                    print(f"  类型: {type(value)}")
                    if isinstance(value, list):
                        print(f"  列表长度: {len(value)}")
                        if len(value) > 0:
                            print(f"  第一条数据键: {list(value[0].keys())}")
        else:
            print(f"✗ 未知类型: {type(data)}")
                
    except Exception as e:
        print(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    test_api_response()
