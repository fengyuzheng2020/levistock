from levistock.stock.stock_spot_em import stock_spot_em

data = stock_spot_em(["000001", "600519", "300750"])
for item in data:
    print(f"{item['stock_name']}: {item['price']} ({item['change_pct']}%)")