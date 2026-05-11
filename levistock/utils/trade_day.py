"""
交易日工具模块

数据源: api.levizhang.com
模块说明: 提供A股交易日查询接口，数据实时准确，无需手动维护节假日
"""

import requests

_TRADE_DAY_URL = "https://api.levizhang.com/isTradeDay"


def is_trade_day() -> bool:
    """
    判断今天是否为A股交易日

    数据源: api.levizhang.com
    接口地址: https://api.levizhang.com/isTradeDay
    更新频率: 实时

    与本地维护节假日数据相比，此接口数据更准确，
    可正确处理调休、补班等特殊情况。

    Returns:
        bool: True 表示今天是交易日，False 表示今天不是交易日

    Raises:
        requests.exceptions.RequestException: 网络请求异常时抛出

    Example:
        >>> import levistock as lk
        >>> if lk.is_trade_day():
        ...     print("今天是交易日，开始获取数据")
        ... else:
        ...     print("今天不是交易日")
    """
    resp = requests.get(_TRADE_DAY_URL, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return data.get("code") == "000000"
