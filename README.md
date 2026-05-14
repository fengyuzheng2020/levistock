# levistock

A股市场数据 SDK，封装东方财富、财联社、同花顺、开盘红、i问财常用接口。

## 安装

```bash
pip install levistock
```

或从 GitHub 安装最新版：

```bash
pip install git+https://github.com/fleetinglife/levistock.git
```

## 快速开始

```python
import levistock as lk

# 大盘指数
lk.market_index_em()

# 涨停池
lk.stock_zt_pool_em()

# 行业板块
lk.sector_em()
```

---

## 接口文档

### 目录

| 模块 | 接口 | 数据源 | 说明 |
|------|------|--------|------|
| 工具 | [is_trade_day](#is_trade_day) | 自有服务器 | 判断今天是否为交易日 |
| 大盘 | [market_index_em](#market_index_em) | 东方财富 | 常用6个大盘指数 |
| 大盘 | [market_index_all_em](#market_index_all_em) | 东方财富 | 全部大盘指数 |
| 大盘 | [market_emotion_cls](#market_emotion_cls) | 财联社 | 市场情绪数据 |
| 大盘 | [market_emotion_kph](#market_emotion_kph) | 开盘红 | 市场情绪数据（实时/历史） |
| 大盘 | [market_wind_cls](#market_wind_cls) | 财联社 | 今日风口板块 |
| 大盘 | [market_wind_stocks_cls](#market_wind_stocks_cls) | 财联社 | 风口板块龙头股 |
| 大盘 | [market_mainline_cls](#market_mainline_cls) | 财联社 | 今日主线机会 |
| 板块 | [sector_em](#sector_em) | 东方财富 | 行业/概念板块列表 |
| 板块 | [sector_stocks_em](#sector_stocks_em) | 东方财富 | 板块成分股 |
| 板块 | [sector_stock_belong_em](#sector_stock_belong_em) | 东方财富 | 股票所属板块 |
| 板块 | [sector_industry_cls](#sector_industry_cls) | 财联社 | 行业板块实时行情 |
| 板块 | [sector_ranking_kph](#sector_ranking_kph) | 开盘红 | 精选/行业/地区板块排行 |
| 板块 | [sector_stocks_his_kph](#sector_stocks_his_kph) | 开盘红 | 历史板块成分股 |
| 股票 | [stocks_all_em](#stocks_all_em) | 东方财富 | 全量A股实时行情 |
| 股票 | [stocks_em](#stocks_em) | 东方财富 | 指定股票实时行情 |
| 股票 | [stock_zt_pool_em](#stock_zt_pool_em) | 东方财富 | 涨停板股票池 |
| 股票 | [stock_dt_pool_em](#stock_dt_pool_em) | 东方财富 | 跌停板股票池 |
| 股票 | [stock_yesterday_zt_em](#stock_yesterday_zt_em) | 东方财富 | 昨日涨停今日表现 |
| 股票 | [stock_zt_pool_cls](#stock_zt_pool_cls) | 财联社 | 涨停池（含涨停原因） |
| 股票 | [limit_up_his_kph](#limit_up_his_kph) | 开盘红 | 历史涨停股列表 |
| 股票 | [limit_down_his_kph](#limit_down_his_kph) | 开盘红 | 历史跌停股列表 |
| 股票 | [wind_vane_his_kph](#wind_vane_his_kph) | 开盘红 | 历史风向标列表 |
| 股票 | [stock_changes_em](#stock_changes_em) | 东方财富 | 盘口异动列表 |
| 股票 | [stock_changes_detail_em](#stock_changes_detail_em) | 东方财富 | 个股异动明细 |
| 股票 | [stock_hot_rank_ths](#stock_hot_rank_ths) | 同花顺 | 人气股排行榜 |
| 股票 | [stock_timeline_cls](#stock_timeline_cls) | 财联社 | 个股分时数据 |
| 股票 | [stock_kline_cls](#stock_kline_cls) | 财联社 | 个股K线数据 |
| 股票 | [stock_strategy_wencai](#stock_strategy_wencai) | i问财 | 自然语言策略查询 |
| 资讯 | [news_telegraph_cls](#news_telegraph_cls) | 财联社 | 电报快讯 |

---

### 工具

#### `is_trade_day`

判断今天是否为A股交易日。

```python
if lk.is_trade_day():
    print("今天是交易日")
```

| 返回值 | 说明 |
|--------|------|
| `bool` | True=交易日，False=非交易日 |

---

### 大盘 market

#### `market_index_em`

获取A股常用大盘指数实时行情（东方财富），返回上证指数、深证成指、创业板指、科创50、沪深300、中证500。

```python
data = lk.market_index_em()
for item in data:
    print(f"{item['name']}: {item['price']} ({item['change_pct']}%)")
```

| 字段 | 说明 |
|------|------|
| name | 指数名称 |
| code | 指数代码 |
| price | 最新价 |
| change_pct | 涨跌幅(%) |
| change_amt | 涨跌额 |
| volume | 成交量 |
| amount | 成交额(元) |
| high | 最高价 |
| low | 最低价 |
| open | 开盘价 |
| pre_close | 昨收价 |

---

#### `market_index_all_em`

获取全部大盘指数，字段同 `market_index_em`。

```python
data = lk.market_index_all_em()
print(f"共 {len(data)} 个指数")
```

---

#### `market_emotion_cls`

获取A股市场情绪数据（财联社），包含涨跌分布、封板率、连板梯队等。

```python
data = lk.market_emotion_cls()
print(f"市场热度: {data['market_degree']}")
print(f"上涨家数: {data['up_down_dis']['rise_num']}")
print(f"涨停家数: {data['up_down_dis']['up_num']}")
print(f"封板率: {data['up_ratio']}")
```

| 字段 | 说明 |
|------|------|
| market_degree | 市场热度(0-100) |
| shsz_balance | 两市成交额 |
| shsz_balance_change_px | 较上日成交额变化 |
| up_ratio | 封板率 |
| up_ratio_num | 封板数量 |
| up_open_num | 炸板数量 |
| performance | 昨涨停今表现 |
| up_open_ratio | 高开率 |
| profit_ratio | 获利率 |
| up_down_dis | 涨跌分布(dict) |
| limit_up_board | 连板梯队(dict) |

---

#### `market_emotion_kph`

获取A股市场情绪数据（开盘红）。不传日期查今天实时，传历史日期查历史。

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYY-MM-DD"`，不传默认今天 |

```python
data = lk.market_emotion_kph()
data = lk.market_emotion_kph(date="2026-05-13")
print(f"涨停: {data['zt']}只")
print(f"跌停: {data['dt']}只")
print(f"市场人气: {data['sign']}")
```

| 字段 | 说明 |
|------|------|
| zt | 涨停总数 |
| dt | 跌停总数 |
| sjzt | 实际涨停（非ST） |
| sjdt | 实际跌停（非ST） |
| stzt | ST涨停 |
| stdt | ST跌停 |
| rise_num | 上涨家数 |
| fall_num | 下跌家数 |
| flat | 平盘家数 |
| sign | 市场人气判断文字 |
| rise_dist | 各涨幅区间股票数 {1:xx, 2:xx ... 10:xx} |
| fall_dist | 各跌幅区间股票数 {-1:xx, -2:xx ... -10:xx} |
| szln | 沪市成交额(元) |
| qscln | 全市成交额(元) |
| s_zrcs | 昨日沪市成交额(元) |
| q_zrcs | 昨日全市成交额(元) |

---

#### `market_wind_cls`

获取今日风口板块列表（财联社）。

```python
data = lk.market_wind_cls()
for item in data:
    print(f"{item['plate_name']}: {item['catalyst'][:30]}...")
```

| 字段 | 说明 |
|------|------|
| plate_code | 板块代码 |
| plate_name | 板块名称 |
| catalyst | 催化剂描述 |

---

#### `market_wind_stocks_cls`

获取风口板块龙头股（财联社）。

| 参数 | 说明 |
|------|------|
| plate_code | 板块代码，通过 `market_wind_cls()` 获取 |

```python
wind = lk.market_wind_cls()
stocks = lk.market_wind_stocks_cls(wind[0]["plate_code"])
```

| 字段 | 说明 |
|------|------|
| secu_code | 股票代码（含市场前缀） |
| secu_name | 股票名称 |
| last_px | 现价 |
| change | 涨跌幅 |
| continuous | 连板次数 |

---

#### `market_mainline_cls`

获取今日主线机会（财联社），返回主线题材、板块及龙头股。

```python
data = lk.market_mainline_cls()
print(data)
```

---

### 板块 sector

#### `sector_em`

获取A股板块列表（东方财富），支持行业板块（全量/分级）和概念板块。

| 参数 | 说明 |
|------|------|
| sector_type | 板块类型，默认 `"industry"` |

板块类型：

| 类型值 | 说明 |
|--------|------|
| `"industry"` | 全部行业板块（默认） |
| `"concept"` | 概念板块 |
| `"industry_l1"` | 东财一级行业（31个） |
| `"industry_l2"` | 东财二级行业（128个） |
| `"industry_l3"` | 东财三级行业（337个） |

```python
industry = lk.sector_em()
concept  = lk.sector_em(sector_type="concept")
l1       = lk.sector_em(sector_type="industry_l1")
l2       = lk.sector_em(sector_type="industry_l2")
l3       = lk.sector_em(sector_type="industry_l3")
```

| 字段 | 说明 |
|------|------|
| sector_code | 板块代码 |
| sector_name | 板块名称 |
| change_pct | 涨跌幅(%) |
| amount | 成交额(元) |
| main_inflow | 主力净流入(元) |
| lead_stock_name | 领涨股名称 |
| lead_stock_code | 领涨股代码 |
| lead_stock_chg | 领涨股涨跌幅(%) |
| up_count | 上涨家数 |
| down_count | 下跌家数 |

---

#### `sector_stocks_em`

获取板块成分股（东方财富），行业板块和概念板块通用。

| 参数 | 说明 |
|------|------|
| sector_code | 板块代码，如 `"BK1033"` |

```python
stocks = lk.sector_stocks_em("BK1033")
```

| 字段 | 说明 |
|------|------|
| stock_code | 股票代码 |
| stock_name | 股票名称 |

---

#### `sector_stock_belong_em`

批量查询股票所属行业板块（东方财富）。

| 参数 | 说明 |
|------|------|
| stock_codes | 股票代码列表，如 `["000001", "600001"]` |

```python
data = lk.sector_stock_belong_em(["000001", "600001", "300001"])
for item in data:
    print(f"{item['stock_name']} → {item['sector_name']}")
```

| 字段 | 说明 |
|------|------|
| stock_code | 股票代码 |
| stock_name | 股票名称 |
| sector_name | 所属行业板块 |

---

#### `sector_industry_cls`

获取A股行业板块实时行情（财联社），按涨跌幅从高到低排序。

```python
data = lk.sector_industry_cls()
sorted_data = sorted(data, key=lambda x: x["main_fund_diff"], reverse=True)
```

| 字段 | 说明 |
|------|------|
| secu_name | 板块名称 |
| secu_code | 板块代码 |
| change | 涨跌幅 |
| main_fund_diff | 主力净流入(元) |
| limit_up | 上涨家数 |
| limit_down | 下跌家数 |
| limit_up_num | 涨停家数 |
| limit_down_num | 跌停家数 |
| first_stock | 领涨股信息(dict) |

---

#### `sector_ranking_kph`

获取精选/行业/地区板块排行（开盘红）。传今天日期查实时，传历史日期查历史。

板块类型常量：

| 常量 | 值 | 说明 |
|------|----|------|
| `SECTOR_SELECTED` | `"7"` | 精选板块 |
| `SECTOR_INDUSTRY` | `"4"` | 行业板块 |
| `SECTOR_REGION` | `"6"` | 地区板块 |

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYY-MM-DD"`，必填 |
| zs_type | 板块类型，必填，使用上方常量 |
| fetch_all | 是否获取全量，默认 `False`（前50条） |

```python
data = lk.sector_ranking_kph(date="2026-05-14", zs_type=lk.SECTOR_SELECTED)
data = lk.sector_ranking_kph(date="2026-05-13", zs_type=lk.SECTOR_INDUSTRY, fetch_all=True)
data = lk.sector_ranking_kph(date="2026-05-14", zs_type=lk.SECTOR_REGION)
```

| 字段 | 说明 |
|------|------|
| plate_id | 板块ID |
| plate_name | 板块名称 |
| change_pct | 涨跌幅(%) |
| amount | 成交额(元) |
| net_inflow | 净流入(元) |
| net_inflow_5d | 5日净流入(元) |
| buy_amount | 主买金额(元) |
| sell_amount | 主卖金额(元) |
| turnover_rate | 换手率(%) |
| market_cap | 总市值(元) |
| avg_change | 平均涨幅(%) |
| stock_count | 成分股数量 |

---

#### `sector_stocks_his_kph`

获取历史板块成分股（开盘红），精选/行业/地区通用，日期必须小于今天。

| 参数 | 说明 |
|------|------|
| plate_id | 板块ID，通过 `sector_ranking_kph()` 获取，必填 |
| date | 交易日期，格式 `"YYYY-MM-DD"`，必填，必须小于今天 |

```python
plates = lk.sector_ranking_kph(date="2026-05-13", zs_type=lk.SECTOR_SELECTED)
stocks = lk.sector_stocks_his_kph(plate_id=plates[0]["plate_id"], date="2026-05-13")
print(f"成分股数: {len(stocks)}")
```

| 字段 | 说明 |
|------|------|
| code | 股票代码 |
| name | 股票名称 |
| price | 现价(元) |
| change_pct | 涨跌幅(%) |
| amount | 成交额(元) |
| turnover_rate | 换手率(%) |
| float_amount | 流通市值(元) |
| main_buy | 主力买入(元) |
| main_sell | 主力卖出(元) |
| main_net | 主力净额(元) |
| buy_ratio | 主买占比(%) |
| sell_ratio | 主卖占比(%) |
| net_ratio | 净额占比(%) |
| tags | 概念标签 |
| limit_tag | 连板标签 |
| rank_tag | 龙虎榜标签 |
| recent_chg | 近期涨幅(%) |
| limit_count | 近期涨停次数 |
| chg_1d | 1日涨幅(%) |
| chg_5d | 5日涨幅(%) |
| chg_20d | 20日涨幅(%) |

---

### 股票 stock

#### `stocks_all_em`

获取A股全量实时行情（东方财富）。

| 参数 | 说明 |
|------|------|
| filter_st | 是否过滤ST股，默认 `True` |

```python
data = lk.stocks_all_em()
print(f"股票数: {len(data)}")
```

| 字段 | 说明 |
|------|------|
| stock_code | 股票代码 |
| stock_name | 股票名称 |
| price | 现价 |
| change_pct | 涨跌幅(%) |
| change_amt | 涨跌额 |
| volume | 成交量(手) |
| amount | 成交额(元) |
| turnover_rate | 换手率(%) |
| pe_ttm | 市盈率TTM |
| volume_ratio | 量比 |
| high | 最高价 |
| low | 最低价 |
| open | 开盘价 |
| pre_close | 昨收价 |
| total_market | 总市值(元) |
| circ_market | 流通市值(元) |
| pb | 市净率PB |

---

#### `stocks_em`

获取指定股票实时行情（东方财富），最多支持100只。

| 参数 | 说明 |
|------|------|
| stock_codes | 股票代码列表，如 `["000001", "600001"]`，最多100只 |

```python
data = lk.stocks_em(["000001", "600519", "300750"])
for item in data:
    print(f"{item['stock_name']}: {item['price']} ({item['change_pct']}%)")
```

字段同 `stocks_all_em()`。

---

#### `stock_zt_pool_em`

获取涨停板股票池（东方财富），支持历史日期查询。

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYYMMDD"`，默认今天 |

```python
data = lk.stock_zt_pool_em()
data = lk.stock_zt_pool_em(date="20260513")
```

| 字段 | 说明 |
|------|------|
| stock_code | 股票代码 |
| stock_name | 股票名称 |
| price | 现价(元) |
| change_pct | 涨跌幅(%) |
| continuous | 连板次数 |
| first_zt_time | 首次涨停时间 |
| last_zt_time | 最后涨停时间 |
| open_times | 炸板次数 |
| amount | 成交额(元) |
| turnover_rate | 换手率(%) |
| main_inflow | 主力净流入(元) |
| sector | 所属行业板块 |

---

#### `stock_dt_pool_em`

获取跌停板股票池（东方财富），支持历史日期查询。

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYYMMDD"`，默认今天 |

```python
data = lk.stock_dt_pool_em()
data = lk.stock_dt_pool_em(date="20260513")
```

| 字段 | 说明 |
|------|------|
| stock_code | 股票代码 |
| stock_name | 股票名称 |
| price | 现价(元) |
| change_pct | 涨跌幅(%) |
| days | 连续跌停天数 |
| last_dt_time | 最后跌停时间 |
| seal_amount | 封单金额(元) |
| amount | 成交额(元) |
| turnover_rate | 换手率(%) |
| main_inflow | 主力净流入(元) |
| sector | 所属行业板块 |

---

#### `stock_yesterday_zt_em`

获取昨日涨停今日表现（东方财富）。

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYYMMDD"`，默认今天 |

```python
data = lk.stock_yesterday_zt_em()
for item in data[:5]:
    print(f"{item['stock_name']} 今日:{item['change_pct']}% 高开:{item['open_ratio']}%")
```

| 字段 | 说明 |
|------|------|
| stock_code | 股票代码 |
| stock_name | 股票名称 |
| price | 现价(元) |
| zt_price | 涨停价(元) |
| change_pct | 今日涨跌幅(%) |
| amount | 成交额(元) |
| turnover_rate | 换手率(%) |
| amplitude | 振幅(%) |
| open_ratio | 高开比(%) |
| yesterday_time | 昨日涨停时间 |
| yesterday_cont | 昨日连板数 |
| sector | 所属行业板块 |
| zt_days | 近期涨停天数 |
| zt_count | 近期涨停次数 |

---

#### `stock_zt_pool_cls`

获取当日涨停池（财联社），含涨停原因，仅支持当天。

```python
data = lk.stock_zt_pool_cls()
for item in data:
    print(f"{item['secu_name']}: {item['up_reason']}")
```

| 字段 | 说明 |
|------|------|
| secu_code | 股票代码（含市场前缀） |
| secu_name | 股票名称 |
| last_px | 现价(元) |
| change | 涨跌幅 |
| up_reason | 涨停原因 |

---

#### `limit_up_his_kph`

获取历史涨停股列表（开盘红），日期必须小于今天。

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYY-MM-DD"`，必须小于今天 |

```python
data = lk.limit_up_his_kph(date="2026-05-13")
for item in data:
    print(f"{item['name']} 原因:{item['reason']} 题材:{item['themes']} 连板:{item['limit_count']}")
```

| 字段 | 说明 |
|------|------|
| code | 股票代码 |
| name | 股票名称 |
| reason | 涨停原因 |
| themes | 题材 |
| industry_id | 行业ID |
| industry_zt | 同行业涨停数 |
| limit_tag | 连板标签（首板/二板...） |
| limit_count | 连板数 |
| limit_time | 最后涨停时间戳 |
| open_time | 开板时间戳（0=未开板） |
| seal_amount | 封单量 |
| seal_money | 封单金额(元) |
| turnover | 成交额(元) |
| turnover_rate | 换手率(%) |
| net_inflow | 净流入(元) |
| market_cap | 流通市值(元) |

---

#### `limit_down_his_kph`

获取历史跌停股列表（开盘红），日期必须小于今天。

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYY-MM-DD"`，必须小于今天 |

```python
data = lk.limit_down_his_kph(date="2026-05-13")
for item in data:
    print(f"{item['name']} 换手:{item['turnover_rate']}% 题材:{item['themes']}")
```

| 字段 | 说明 |
|------|------|
| code | 股票代码 |
| name | 股票名称 |
| themes | 题材 |
| industry_id | 行业ID |
| limit_time | 跌停时间戳 |
| open_time | 开板时间戳（0=未开板） |
| seal_amount | 封单量 |
| seal_money | 封单金额(元) |
| turnover | 成交额(元) |
| turnover_rate | 换手率(%) |
| net_inflow | 净流入(元) |
| market_cap | 流通市值(元) |

---

#### `wind_vane_his_kph`

获取历史风向标列表（开盘红），日期必须小于今天。

| 参数 | 说明 |
|------|------|
| date | 交易日期，格式 `"YYYY-MM-DD"`，必须小于今天 |

```python
data = lk.wind_vane_his_kph(date="2026-05-13")
for item in data:
    print(f"{item['name']} 换手:{item['turnover_rate']}% 题材:{item['themes']}")
```

字段同 `limit_up_his_kph()`。

---

#### `stock_changes_em`

获取实时盘口异动股票列表（东方财富）。

| 参数 | 说明 |
|------|------|
| change_type | 异动类型，默认 `"8201"` 火箭发射 |
| filter_st | 是否过滤ST及三板，默认 `True` |

常用异动类型：

| 类型值 | 说明 |
|--------|------|
| `"8201"` | 火箭发射 |
| `"8202"` | 快速反弹 |
| `"8193"` | 大笔买入 |
| `"8205"` | 封涨停板 |
| `"64"` | 有大买盘 |

```python
data = lk.stock_changes_em()
data = lk.stock_changes_em(change_type="8193")
```

---

#### `stock_changes_detail_em`

获取个股盘口异动明细（东方财富）。

| 参数 | 说明 |
|------|------|
| stock_code | 股票代码，如 `"000001"` |
| market | 市场，`"0"` 深市，`"1"` 沪市 |
| date | 日期，格式 `"YYYYMMDD"`，默认今天 |

```python
data = lk.stock_changes_detail_em(stock_code="000001", market="0")
```

---

#### `stock_hot_rank_ths`

获取A股人气股排行榜（同花顺）。

| 参数 | 说明 |
|------|------|
| limit | 返回条数，默认100 |

```python
data = lk.stock_hot_rank_ths()
for item in data[:5]:
    print(f"{item['rank']}. {item['name']} {item['change_pct']}%")
```

| 字段 | 说明 |
|------|------|
| rank | 排名 |
| code | 股票代码 |
| name | 股票名称 |
| price | 现价(元) |
| change_pct | 涨跌幅(%) |
| change_amt | 涨跌额 |
| tag | 标签信息(dict) |

---

#### `stock_timeline_cls`

获取个股分时数据（财联社）。

| 参数 | 说明 |
|------|------|
| stock_code | 股票代码，支持 `"002664"` 或 `"sz002664"` 格式 |

```python
data = lk.stock_timeline_cls("002664")
```

| 字段 | 说明 |
|------|------|
| date | 交易日期 |
| minute | 分钟时间 |
| last_px | 最新价 |
| business_balance | 成交额 |
| business_amount | 成交量 |
| open_px | 开盘价 |
| preclose_px | 昨收价 |
| av_px | 均价 |

---

#### `stock_kline_cls`

获取个股K线数据（财联社）。

| 参数 | 说明 |
|------|------|
| stock_code | 股票代码，支持 `"002664"` 或 `"sz002664"` 格式 |
| kline_type | K线类型，默认 `"daily"` |
| limit | 返回条数，默认50 |
| offset | 偏移量，默认0 |

K线类型：

| 类型值 | 说明 |
|--------|------|
| `"daily"` | 日K（默认） |
| `"weekly"` | 周K |
| `"monthly"` | 月K |
| `"yearly"` | 年K |

```python
data = lk.stock_kline_cls("002664")
data = lk.stock_kline_cls("002664", kline_type="weekly", limit=100)
```

---

#### `stock_strategy_wencai`

i问财自然语言股票策略查询。

| 参数 | 说明 |
|------|------|
| query | 自然语言查询条件 |
| page | 页码，默认1 |
| limit | 每页条数，默认50 |

```python
data = lk.stock_strategy_wencai(query="连板3板以上")
print(data["title"])
print(data["result"])
```

---

### 资讯 news

#### `news_telegraph_cls`

获取财联社电报快讯，数据超过20条时自动显示进度条。

| 参数 | 说明 |
|------|------|
| date | 日期，格式 `"YYYY-MM-DD"`，默认今天 |
| category | 消息类型，默认 `"important"` |

消息类型：

| 类型值 | 说明 |
|--------|------|
| `"all"` | 全部电报 |
| `"important"` | 加红重要消息（默认） |
| `"company"` | 公司公告 |

```python
data = lk.news_telegraph_cls()
data = lk.news_telegraph_cls(category="all")
data = lk.news_telegraph_cls(date="2026-05-07", category="company")
for item in data:
    print(f"{item['time']} | {item['title']}")
```

| 字段 | 说明 |
|------|------|
| id | 电报ID |
| title | 标题 |
| content | 正文内容 |
| time | 发布时间，格式 `"YYYY-MM-DD HH:MM:SS"` |

---

## License

MIT