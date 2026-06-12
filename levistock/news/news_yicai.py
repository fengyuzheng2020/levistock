"""
第一财经 - 快讯/简报模块

数据源: 第一财经 (yicai.com)
模块说明: 提供第一财经快讯数据接口，支持分页拉取最新财经资讯
"""

import datetime
import requests


_BASE_URL = "https://www.yicai.com/api/ajax/getbrieflist"

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Referer": "https://www.yicai.com/brief/",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "*/*",
}


def _fetch_brief_list(page: int = 1, page_size: int = 20) -> dict:
    """
    请求第一财经快讯列表
    
    Args:
        page: 页码，从1开始
        page_size: 每页数量
        
    Returns:
        API响应JSON
    """
    params = {
        "page": page,
        "pagesize": page_size,
        "type": 0,
        "id": 0,
    }
    
    try:
        resp = requests.get(_BASE_URL, headers=_HEADERS, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"请求失败: {e}")


def news_brief_yicai(limit: int = 20) -> list:
    """
    获取第一财经快讯（第一财经）
    
    数据源: 第一财经
    接口地址: https://www.yicai.com/api/ajax/getbrieflist
    更新频率: 实时
    
    Args:
        limit: 获取数量限制，默认20条
        
    Returns:
        list[dict]: 快讯列表，按时间从新到旧排列，每条数据包含以下字段：
        
        ============= ====================== ====================
        字段名         说明                    示例
        ============= ====================== ====================
        id             快讯ID                 103227797
        title          标题                   "国际油价跌幅扩大"
        content        正文内容               "WTI原油期货跌幅..."
        time           发布时间（格式化）       "2026-06-12 15:59:54"
        share_url      分享链接               "https://m.yicai.com/brief/..."
        important      是否重要消息            True/False
        ============= ====================== ====================
        
    Raises:
        RuntimeError: 接口返回异常时抛出
        requests.exceptions.RequestException: 网络请求异常时抛出
        
    Example:
        >>> import levistock as lk
        >>> # 获取最新20条快讯
        >>> data = lk.news_brief_yicai()
        >>> print(f"最新快讯: {len(data)} 条")
        >>>
        >>> # 获取最新5条快讯
        >>> data = lk.news_brief_yicai(limit=5)
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
            data = _fetch_brief_list(page=page, page_size=page_size)
            
            # 解析响应数据 - API 可能直接返回列表或包含在字典中
            if isinstance(data, list):
                # 直接返回列表
                brief_list = data
            elif isinstance(data, dict):
                # 字典格式，尝试不同的键
                brief_list = data.get("data", []) or data.get("result", []) or data.get("list", [])
            else:
                print(f"[WARNING] 未知的数据类型: {type(data)}")
                break
            
            if not brief_list:
                break
            
            all_items.extend(brief_list)
            
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
        create_date = item.get("CreateDate", "")
        
        # 解析时间字符串
        try:
            if create_date:
                dt = datetime.datetime.strptime(create_date, "%Y-%m-%dT%H:%M:%S")
                time_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            else:
                time_str = ""
        except ValueError:
            time_str = create_date
        
        # 提取内容（优先使用 LiveContent，其次 newcontent）
        content = item.get("LiveContent", "") or item.get("newcontent", "")
        
        # 提取标题
        title = item.get("LiveTitle", "") or item.get("NewsTitle", "") or item.get("indexTitle", "")
        
        result.append({
            "id": item.get("LiveID", 0),
            "title": title,
            "content": content,
            "time": time_str,
            "share_url": item.get("ShareUrl", ""),
            "important": item.get("IsImportant", False) or item.get("important", False),
        })
    
    return result
