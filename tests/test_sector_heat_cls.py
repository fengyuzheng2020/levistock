"""
测试财联社板块热度接口 sector_heat_cls.py
"""

from levistock.sector.sector_heat_cls import get_sector_heat

print("=" * 50)
print("[1] 板块热度 get_sector_heat")
print("=" * 50)
heat = get_sector_heat()
print(f"共 {len(heat)} 个板块")
for item in heat[:10]:
    new_tag = " [新上榜]" if item["is_new"] else ""
    change = item["rank_change"]
    change_str = f"↑{change}" if change > 0 else (f"↓{abs(change)}" if change < 0 else "-")
    print(f"  {item['rank']:>3}. {item['plate_name']:<12} 热度:{item['cur_heat']:.1f}  排名变化:{change_str}{new_tag}")
