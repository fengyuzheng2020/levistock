from levistock.utils.trade_day import is_trade_day

if is_trade_day():
    print("今天是交易日")
else:
    print("今天不是交易日")