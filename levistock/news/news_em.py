"""
东方财富 - 快讯模块

数据源: 东方财富 (eastmoney.com)
模块说明: 提供东方财富快讯数据接口，支持分页拉取最新财经资讯
注意: API 返回 JSONP 格式，需要特殊解析
"""

import datetime
import requests
import re
import json


_BASE_URL = "https://np-weblist.eastmoney.com/comm/web/getFastNewsList"

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Referer": "https://kuaixun.eastmoney.com/",
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
            except json.JSONDecodeError:
                continue
    
    # 如果所有模式都失败，尝试直接查找 JSON
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        json_str = text[start:end+1]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    raise ValueError("无法解析 JSONP 响应")


def _fetch_news_list(page_size: int = 50, sort_end: str = "") -> dict:
    """
    请求东方财富快讯列表
    
    Args:
        page_size: 每页数量，默认50
        sort_end: 排序结束时间戳，用于分页
        
    Returns:
        API响应JSON
    """
    import time
    
    params = {
        "client": "web",
        "biz": "web_724",
        "fastColumn": 102,
        "sortEnd": sort_end,
        "pageSize": page_size,
        "req_trace": int(time.time() * 1000),
        "_": int(time.time() * 1000),
        "callback": f"jQuery{int(time.time() * 1000)}",
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


def news_brief_em(limit: int = 20) -> list:
    """
    获取东方财富快讯（东方财富）
    
    数据源: 东方财富
    接口地址: https://np-weblist.eastmoney.com/comm/web/getFastNewsList
    更新频率: 实时
    
    Args:
        limit: 获取数量限制，默认20条
        
    Returns:
        list[dict]: 快讯列表，按时间从新到旧排列，每条数据包含以下字段：
        
        ============= ====================== ====================
        字段名         说明                    示例
        ============= ====================== ====================
        code           快讯ID                 "202606123769960617"
        title          标题                   "今年前5月全国铁路..."
        content        正文内容               "【今年前5月..."
        time           发布时间（格式化）       "2026-06-12 16:59:23"
        stock_list     相关股票列表            []
        ============= ====================== ====================
        
    Raises:
        RuntimeError: 接口返回异常时抛出
        requests.exceptions.RequestException: 网络请求异常时抛出
        
    Example:
        >>> import levistock as lk
        >>> # 获取最新20条快讯
        >>> data = lk.news_brief_em()
        >>> print(f"最新快讯: {len(data)} 条")
        >>>
        >>> # 获取最新5条快讯
        >>> data = lk.news_brief_em(limit=5)
        >>> for item in data:
        ...     print(f"{item['time']} | {item['title']}")
    """
    if limit <= 0:
        raise ValueError("limit 必须大于0")
    
    all_items = []
    sort_end = ""
    
    # 计算需要请求的次数
    page_size = min(limit, 50)  # 单次最多50条
    requests_needed = (limit + page_size - 1) // page_size
    
    for _ in range(requests_needed):
        try:
            data = _fetch_news_list(page_size=page_size, sort_end=sort_end)
            
            # 解析响应数据
            if data.get("code") != "1":
                print(f"[WARNING] API 返回错误: {data.get('message', 'Unknown')}")
                break
            
            fast_news_list = data.get("data", {}).get("fastNewsList", [])
            
            if not fast_news_list:
                break
            
            all_items.extend(fast_news_list)
            
            # 更新 sort_end 用于下一次请求
            sort_end = data.get("data", {}).get("sortEnd", "")
            
            # 如果已经获取足够的数据，提前退出
            if len(all_items) >= limit:
                break
                
        except Exception as e:
            print(f"[ERROR] 获取数据失败: {e}")
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
        show_time = item.get("showTime", "")
        
        # 时间已经是格式化好的字符串
        time_str = show_time
        
        # 提取标题和内容
        title = item.get("title", "")
        summary = item.get("summary", "")
        
        # 如果没有标题，使用摘要的前50个字符
        if not title and summary:
            title = summary[:50] + "..." if len(summary) > 50 else summary
        
        # 提取相关股票列表
        stock_list = item.get("stockList", [])
        
        # 处理 stock_list 可能是字符串列表或字典列表的情况
        processed_stock_list = []
        if stock_list:
            for s in stock_list:
                if isinstance(s, dict):
                    # 如果是字典，直接使用
                    processed_stock_list.append(s)
                elif isinstance(s, str):
                    # 如果是字符串，转换为字典格式
                    processed_stock_list.append({"name": s})
        
        result.append({
            "code": item.get("code", ""),
            "title": title,
            "content": summary,
            "time": time_str,
            "stock_list": processed_stock_list,
        })
    
    return result
