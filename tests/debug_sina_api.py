"""
调试新浪财经 API 响应
"""

import requests
import time


def debug_sina_api():
    """调试 API 响应"""
    url = "https://app.cj.sina.com.cn/api/news/pc"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Referer": "https://finance.sina.com.cn/",
        "Accept": "*/*",
    }
    
    params = {
        "callback": f"jQuery{int(time.time() * 1000)}",
        "page": 1,
        "size": 5,
        "tag": 0,
        "id": "",
        "type": 0,
        "_": int(time.time() * 1000),
    }
    
    print("=" * 70)
    print("调试新浪财经 API")
    print("=" * 70)
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        
        print(f"\n状态码: {resp.status_code}")
        print(f"Content-Type: {resp.headers.get('Content-Type', 'Unknown')}")
        print(f"\n响应长度: {len(resp.text)} 字符")
        
        # 显示前1000字符
        print(f"\n响应内容（前1000字符）:")
        print("-" * 70)
        print(resp.text[:1000])
        print("-" * 70)
        
        # 检查是否包含 JSON
        if '{' in resp.text and '}' in resp.text:
            print("\n✓ 响应中包含 JSON 结构")
            
            # 找到 JSON 开始和结束位置
            start = resp.text.find('{')
            end = resp.text.rfind('}')
            
            if start != -1 and end != -1:
                json_part = resp.text[start:end+1]
                print(f"\n提取的 JSON 部分（前500字符）:")
                print(json_part[:500])
                
                # 尝试解析
                import json
                try:
                    data = json.loads(json_part)
                    print("\n✓ JSON 解析成功！")
                    print(f"顶层键: {list(data.keys())}")
                    
                    # 检查数据结构
                    if 'result' in data:
                        result = data['result']
                        print(f"result 键: {list(result.keys())}")
                        
                        if 'data' in result:
                            feed_data = result['data'].get('feed', {})
                            feed_list = feed_data.get('list', [])
                            print(f"feed.list 长度: {len(feed_list)}")
                            
                            if feed_list:
                                print(f"\n第一条数据键: {list(feed_list[0].keys())}")
                                
                except json.JSONDecodeError as e:
                    print(f"\n✗ JSON 解析失败: {e}")
        else:
            print("\n✗ 响应中未找到 JSON 结构")
            
    except Exception as e:
        print(f"\n✗ 请求失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    debug_sina_api()
