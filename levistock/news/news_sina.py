"""
新浪财经 - 快讯/直播模块

数据源: 新浪财经 (finance.sina.com.cn)
模块说明: 提供新浪财经快讯数据接口，支持分页拉取最新财经资讯
注意: API 返回 JSONP 格式，需要特殊解析
"""

import datetime
import requests
import re
import json


_BASE_URL = "https://app.cj.sina.com.cn/api/news/pc"

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Referer": "https://finance.sina.com.cn/",
    "Accept": "*/*",
}


def _parse_jsonp(text: str) -> dict:
    """
    解析 JSONP 响应
    
    Args:
        text: JSONP 格式的响应文本
        
    Returns:
        解析后的字典
    """
    # 尝试多种匹配模式
    patterns = [
        r'\((\{.*\})\);?\s*$',  # callback({...});
        r'\((\{.*\})\)',         # callback({...})
        r'jQuery\w+\((\{.*\})\);?',  # jQuery123({...});
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            json_str = match.group(1)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                continue
    
    # 如果所有模式都失败，尝试直接查找 JSON
    # 找到第一个 { 和最后一个 }
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        json_str = text[start:end+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    raise ValueError(f"无法解析 JSONP 响应")


def _fetch_news_list(page: int = 1, size: int = 20) -> dict:
    """
    请求新浪财经快讯列表
    
    Args:
        page: 页码，从1开始
        size: 每页数量
        
    Returns:
        API响应JSON
    """
    import time
    
    params = {
        "callback": f"jQuery{int(time.time() * 1000)}",
        "page": page,
        "size": size,
        "tag": 0,
        "id": "",
        "type": 0,
        "_": int(time.time() * 1000),
    }
    
    try:
        resp = requests.get(_BASE_URL, headers=_HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        
        # 解析 JSONP
        text = resp.text
        return _parse_jsonp(text)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"请求失败: {e}")
    except (ValueError, json.JSONDecodeError) as e:
        raise RuntimeError(f"解析失败: {e}")


def news_brief_sina(limit: int = 20) -> list:
    """
    获取新浪财经快讯（新浪财经）
    
    数据源: 新浪财经
    接口地址: https://app.cj.sina.com.cn/api/news/pc
    更新频率: 实时
    
    Args:
        limit: 获取数量限制，默认20条
        
    Returns:
        list[dict]: 快讯列表，按时间从新到旧排列，每条数据包含以下字段：
        
        ============= ====================== ====================
        字段名         说明                    示例
        ============= ====================== ====================
        id             快讯ID                 4932293
        title          标题                   "云南发行7年期棚改..."
        content        正文内容               "云南发行7年期..."
        time           发布时间（格式化）       "2026-06-12 16:44:22"
        source         来源                   "其他"
        view_num       阅读量                 "4.38万 阅读"
        ============= ====================== ====================
        
    Raises:
        RuntimeError: 接口返回异常时抛出
        requests.exceptions.RequestException: 网络请求异常时抛出
        
    Example:
        >>> import levistock as lk
        >>> # 获取最新20条快讯
        >>> data = lk.news_brief_sina()
        >>> print(f"最新快讯: {len(data)} 条")
        >>>
        >>> # 获取最新5条快讯
        >>> data = lk.news_brief_sina(limit=5)
        >>> for item in data:
        ...     print(f"{item['time']} | {item['title']}")
    """
    if limit <= 0:
        raise ValueError("limit 必须大于0")
    
    # 计算需要请求的页数
    page_size = min(limit, 20)  # 单次最多20条
    pages_needed = (limit + page_size - 1) // page_size
    
    all_items = []
    
    for page in range(1, pages_needed + 1):
        try:
            data = _fetch_news_list(page=page, size=page_size)
            
            # 解析响应数据
            result = data.get("result", {})
            feed_data = result.get("data", {}).get("feed", {})
            feed_list = feed_data.get("list", [])
            
            if not feed_list:
                break
            
            all_items.extend(feed_list)
            
            # 如果已经获取足够的数据，提前退出
            if len(all_items) >= limit:
                break
                
        except Exception as e:
            print(f"[ERROR] 获取第{page}页数据失败: {e}")
            import traceback
            traceback.print_exc()
            break
    
    # 截取指定数量的数据
    all_items = all_items[:limit]
    
    return _format(all_items)


def _format(items: list) -> list:
    """格式化快讯数据"""
    result = []
    for item in items:
        create_time = item.get("create_time", "")
        
        # 解析时间字符串
        try:
            if create_time:
                dt = datetime.datetime.strptime(create_time, "%Y-%m-%d %H:%M:%S")
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                time_str = ""
        except ValueError:
            time_str = create_time
        
        # 提取内容（rich_text）
        rich_text = item.get("rich_text", "")
        
        # JSON 解析时已经自动处理了 Unicode 转义，直接使用
        content = rich_text
        
        # 提取标签作为标题（如果有）
        tags = item.get("tag", [])
        tag_names = [t.get("name", "") for t in tags if t.get("name")]
        title = " | ".join(tag_names) if tag_names else ""
        
        # 如果没有标签，使用内容的前50个字符作为标题
        if not title and content:
            title = content[:50] + "..." if len(content) > 50 else content
        
        # 提取来源
        source = tag_names[0] if tag_names else "未知"
        
        # 提取阅读量
        view_num = item.get("view_num", "")
        
        result.append({
            "id": item.get("id", 0),
            "title": title,
            "content": content,
            "time": time_str,
            "source": source,
            "view_num": view_num,
        })
    
    return result
