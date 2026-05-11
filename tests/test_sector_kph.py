from levistock.sector.sector_kph import sector_ranking_kph, sector_ranking_stocks_kph

# 精选板块列表
plates = sector_ranking_kph(date="2026-05-07")
print(f"精选板块数: {len(plates)}")
print(f"第一个板块: {plates[0]}")

# 板块内股票
stocks = sector_ranking_stocks_kph(plate_id=plates[0]["plate_id"], date="2026-05-06")
print(f"\n股票数: {len(stocks)}")
print(f"第一条: {stocks[0]}")