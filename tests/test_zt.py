from levistock.stock.stock_zt_em import stock_zt_pool_em

# 查今日涨停
data = stock_zt_pool_em()
print(f"今日涨停数: {len(data)}")
print(f"第一条: {data[0]}")

# 查历史涨停
data_history = stock_zt_pool_em(date="20260506")
if data_history:
    print(f"历史涨停数: {len(data_history)}")
    print(f"第一条: {data_history[0]}")
else:
    print("当日无涨停数据或非交易日")

# 测试日期格式错误
try:
    stock_zt_pool_em(date="2024-01-01")
except ValueError as e:
    print(f"日期格式错误: {e}")