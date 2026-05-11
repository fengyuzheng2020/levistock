"""
开盘红 - 精选板块模块

数据源: 开盘红 (kaipanhong.com)
模块说明: 提供A股历史精选板块列表及板块内股票详情数据接口
注意: 当日数据由 WebSocket 推送，此接口仅支持历史日期查询
"""

import requests

_HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "User-Agent":   "Dalvik/2.1.0 (Linux; U; Android 12; 2206123SC Build/c069a49.2)",
    "Accept-Encoding": "gzip",
}

_BASE_PARAMS = {
    "PhoneOSNew": "1",
    "DeviceID":   "1a609dd6-b2b8-3bf9-ac40-a77581551454",
    "VerSion":    "6.0.6",
    "Token":      "0",
    "UserID":     "0",
    "Red":        "1",
    "apiv":       "w45",
}

_HOST = "https://apphis.kaipanhong.com/w1/api/index.php"

# 板块字段映射（接口返回数组索引 → 字段名）
_PLATE_FIELDS = {
    0:  "plate_id",       # 板块ID
    1:  "plate_name",     # 板块名称
    2:  "amount",         # 成交额（元）
    3:  "change_pct",     # 涨跌幅%
    4:  "amplitude",      # 振幅%
    5:  "net_inflow",     # 净流入（元）
    6:  "net_inflow_5d",  # 5日净流入
    7:  "buy_amount",     # 主买金额
    8:  "sell_amount",    # 主卖金额
    9:  "turnover_rate",  # 换手率%
    10: "market_cap",     # 总市值
    11: "avg_change",     # 平均涨幅
    17: "stock_count",    # 成分股数量
    18: "change_pct2",    # 涨跌幅%（同3）
}

# 股票字段映射（接口返回数组索引 → 字段名）
_STOCK_FIELDS = {
    0:  "code",           # 股票代码
    1:  "name",           # 股票名称
    4:  "tags",           # 概念标签
    5:  "price",          # 现价
    6:  "change_pct",     # 涨跌幅%
    7:  "amount",         # 成交额（元）
    8:  "turnover_rate",  # 换手率%
    10: "float_amount",   # 流通市值
    11: "main_buy",       # 主力买入
    12: "main_sell",      # 主力卖出
    13: "main_net",       # 主力净额
    14: "buy_ratio",      # 主买占比%
    15: "sell_ratio",     # 主卖占比%
    16: "net_ratio",      # 净额占比%
    23: "limit_tag",      # 板块标签（首板/2连板）
    24: "rank_tag",       # 龙虎榜（龙一/龙二）
    33: "recent_chg",     # 近期涨幅%
    40: "limit_count",    # 近期涨停次数
    62: "chg_1d",         # 1日涨幅%
    63: "chg_5d",         # 5日涨幅%
    64: "chg_20d",        # 20日涨幅%
}


def _parse_plate(row: list) -> dict:
    """解析板块数据行"""
    return {_PLATE_FIELDS.get(i, f"f{i}"): v for i, v in enumerate(row)
            if i in _PLATE_FIELDS}


def _parse_stock(row: list) -> dict:
    """解析股票数据行"""
    return {_STOCK_FIELDS.get(i, f"f{i}"): v for i, v in enumerate(row)
            if i in _STOCK_FIELDS}


def sector_ranking_kph(date: str) -> list:
    """
    获取历史精选板块列表（开盘红）

    数据源: 开盘红
    接口地址: https://apphis.kaipanhong.com/w1/api/index.php
    注意: 仅支持历史日期查询，当日数据由 WebSocket 推送无法获取

    Args:
        date (str): 交易日期，格式 "YYYY-MM-DD"，如 "2026-05-06"
                    注意：非交易日返回空列表

    Returns:
        list[dict]: 精选板块列表（最多50个），每条数据包含以下字段：

        =============== ====================== ====================
        字段名           说明                    示例
        =============== ====================== ====================
        plate_id         板块ID                 "801807"
        plate_name       板块名称               "算力"
        change_pct       涨跌幅(%)              2.88
        amount           成交额(元)             123456789.0
        amplitude        振幅(%)                3.50
        net_inflow       净流入(元)              12345678.0
        net_inflow_5d    5日净流入(元)           56789012.0
        buy_amount       主买金额(元)            98765432.0
        sell_amount      主卖金额(元)            87654321.0
        turnover_rate    换手率(%)              5.21
        market_cap       总市值(元)             1234567890000.0
        avg_change       平均涨幅(%)            1.50
        stock_count      成分股数量             50
        =============== ====================== ====================

    Raises:
        ValueError: 日期格式不正确时抛出
        RuntimeError: 接口返回异常时抛出
        requests.exceptions.RequestException: 网络请求异常时抛出

    Example:
        >>> import levistock as lk
        >>> data = lk.sector_ranking_kph(date="2026-05-06")
        >>> print(f"精选板块数: {len(data)}")
        >>> print(data[0])
        >>>
        >>> # 按涨跌幅排序
        >>> sorted_data = sorted(data, key=lambda x: x["change_pct"], reverse=True)
        >>> print(f"涨幅最大: {sorted_data[0]['plate_name']}")
    """
    from datetime import datetime, date as date_type
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"日期格式错误，应为 YYYY-MM-DD，实际传入：{date}")

    # 格式验证通过后再判断大小
    if parsed_date >= date_type.today():
        raise ValueError(f"日期必须小于今天，实际传入：{date}")

    data = {
        **_BASE_PARAMS,
        "a":      "RealRankingInfo",
        "c":      "ZhiShuRanking",
        "Order":  "1",
        "st":     "50",
        "Index":  "0",
        "Date":   date,
        "Type":   "1",
        "ZSType": "7",
    }

    resp = requests.post(_HOST, headers=_HEADERS, data=data, timeout=10)
    resp.raise_for_status()
    result = resp.json()

    raw_plates = result.get("list", [])
    return [_parse_plate(row) for row in raw_plates]


def sector_ranking_stocks_kph(plate_id: str, date: str) -> list:
    """
    获取精选板块内股票详情（开盘红）

    数据源: 开盘红
    接口地址: https://apphis.kaipanhong.com/w1/api/index.php
    注意: 仅支持历史日期查询，每个板块返回前20条股票

    Args:
        plate_id (str): 板块ID，如 "801807"
                        可通过 sector_ranking_kph() 获取各板块ID
        date     (str): 交易日期，格式 "YYYY-MM-DD"，如 "2026-05-06"

    Returns:
        list[dict]: 板块内股票列表（最多20条），每条数据包含以下字段：

        =============== ====================== ====================
        字段名           说明                    示例
        =============== ====================== ====================
        code             股票代码               "000001"
        name             股票名称               "平安银行"
        price            现价(元)               11.50
        change_pct       涨跌幅(%)              0.35
        amount           成交额(元)             123456789.0
        turnover_rate    换手率(%)              0.21
        float_amount     流通市值(元)            220000000000.0
        main_buy         主力买入(元)            12345678.0
        main_sell        主力卖出(元)            11234567.0
        main_net         主力净额(元)            1111111.0
        buy_ratio        主买占比(%)            45.0
        sell_ratio       主卖占比(%)            43.0
        net_ratio        净额占比(%)            2.0
        tags             概念标签               ["银行", "沪深300"]
        limit_tag        板块标签               "首板"
        rank_tag         龙虎榜标签             "龙一"
        recent_chg       近期涨幅(%)            5.50
        limit_count      近期涨停次数           2
        chg_1d           1日涨幅(%)             0.35
        chg_5d           5日涨幅(%)             2.10
        chg_20d          20日涨幅(%)            8.50
        =============== ====================== ====================

    Raises:
        ValueError: plate_id 为空或日期格式不正确时抛出
        RuntimeError: 接口返回异常时抛出
        requests.exceptions.RequestException: 网络请求异常时抛出

    Example:
        >>> import levistock as lk
        >>> # 先获取板块列表
        >>> plates = lk.sector_ranking_kph(date="2026-05-06")
        >>> plate_id = plates[0]["plate_id"]
        >>> # 再获取该板块内股票
        >>> stocks = lk.sector_ranking_stocks_kph(plate_id=plate_id, date="2026-05-06")
        >>> print(f"股票数: {len(stocks)}")
        >>> print(stocks[0])
    """
    if not plate_id:
        raise ValueError("plate_id 不能为空")

    from datetime import datetime, date as date_type
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(f"日期格式错误，应为 YYYY-MM-DD，实际传入：{date}")

    # 格式验证通过后再判断大小
    if parsed_date >= date_type.today():
        raise ValueError(f"日期必须小于今天，实际传入：{date}")

    data = {
        **_BASE_PARAMS,
        "a":          "ZhiShuStockList_W8",
        "c":          "ZhiShuRanking",
        "Order":      "1",
        "st":         "20",       # 每个板块只取前20条
        "old":        "1",
        "Index":      "0",
        "Date":       date,
        "Type":       "6",
        "PlateID":    plate_id,
        "IsZZ":       "0",
        "IsKZZType":  "0",
        "TSZB":       "0",
        "TSZB_Type":  "0",
        "filterType": "0",
    }

    resp = requests.post(_HOST, headers=_HEADERS, data=data, timeout=10)
    resp.raise_for_status()
    result = resp.json()

    raw_stocks = result.get("list", [])
    return [_parse_stock(row) for row in raw_stocks]
