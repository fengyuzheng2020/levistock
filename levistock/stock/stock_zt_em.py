"""
东方财富 - 涨停板模块

数据源: 东方财富 (eastmoney.com)
模块说明: 提供A股涨停板数据接口，包括涨停池查询
"""

import requests
from datetime import datetime

_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://quote.eastmoney.com/",
}

_BASE_URL = "http://push2ex.eastmoney.com/getTopicZTPool"


def stock_zt_pool_em(date: str = None) -> list:
    """
    获取涨停板股票池（东方财富）

    数据源: 东方财富
    接口地址: http://push2ex.eastmoney.com/getTopicZTPool
    更新频率: 交易日实时更新

    Args:
        date (str): 交易日期，格式 YYYYMMDD，如 "20240101"
                    默认为 None，自动取当天日期
                    支持查询历史涨停数据
                    注意：非交易日或无数据时返回空列表

    Returns:
        list[dict]: 涨停股票列表，每条数据包含以下字段：

        ============= ====================== ====================
        字段名         说明                    示例
        ============= ====================== ====================
        date           交易日期               "20240101"
        stock_code     股票代码               "000001"
        stock_name     股票名称               "平安银行"
        market         市场                   "0"(深) "1"(沪)
        price          现价(元)               11.50
        change_pct     涨跌幅(%)              10.01
        amount         成交额(元)             123456789.0
        circ_market    流通市值(元)            223000000000.0
        circ_share     流通股本(股)            100000000.0
        turnover_rate  换手率(%)              5.21
        continuous     连板次数               2
        first_zt_time  首次涨停时间           "093000"
        last_zt_time   最后涨停时间           "150000"
        main_inflow    主力净流入(元)          12345678.0
        open_times     炸板次数               0
        sector         所属行业板块            "银行"
        ============= ====================== ====================

    Raises:
        ValueError: 日期格式不正确时抛出
        RuntimeError: 接口返回异常时抛出
        requests.exceptions.RequestException: 网络请求异常时抛出

    Example:
        >>> import levistock as lk
        >>> # 查询今日涨停池
        >>> data = lk.stock_zt_pool_em()
        >>> print(len(data))
        >>> print(data[0])
        >>>
        >>> # 查询历史涨停池
        >>> data = lk.stock_zt_pool_em(date="20240101")
        >>> if data:
        ...     print(data[0])
        ... else:
        ...     print("当日无涨停数据或非交易日")
    """
    # 校验日期格式
    if date is not None:
        try:
            datetime.strptime(date, "%Y%m%d")
        except ValueError:
            raise ValueError(f"日期格式错误，应为 YYYYMMDD，如 '20240101'，实际传入：{date}")
    else:
        # 默认取当天日期
        date = datetime.now().strftime("%Y%m%d")

    params = {
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "dpt": "wz.ztzt",
        "Pageindex": 0,
        "pagesize": 3000,
        "sort": "fbt:asc",
        "date": date,
    }

    resp = requests.get(_BASE_URL, params=params, headers=_HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if data.get("rc") != 0:
        raise RuntimeError(f"接口返回异常，rc={data.get('rc')}")

    body = data.get("data")
    # 非交易日或无数据时接口返回 data 为 None
    if body is None:
        return []

    items = body.get("pool", [])
    result = []

    for item in items:
        # 现价需除以1000
        price = item.get("p", 0)
        try:
            price = round(float(price) / 1000, 2)
        except (ValueError, TypeError):
            price = "-"

        result.append({
            "date":          date,
            "stock_code":    str(item.get("c", "")),
            "stock_name":    str(item.get("n", "")),
            "market":        str(item.get("m", "")),
            "price":         price,
            "change_pct":    item.get("zdp", "-"),
            "amount":        item.get("amount", "-"),
            "circ_market":   item.get("ltsz", "-"),
            "circ_share":    item.get("tshare", "-"),
            "turnover_rate": item.get("hs", "-"),
            "continuous":    item.get("lbc", "-"),
            "first_zt_time": str(item.get("fbt", "")),
            "last_zt_time":  str(item.get("lbt", "")),
            "main_inflow":   item.get("fund", "-"),
            "open_times":    item.get("zbc", "-"),
            "sector":        str(item.get("hybk", "")),
        })

    return result