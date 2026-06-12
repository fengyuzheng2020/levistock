"""
财联社市场数据 - 飞书定时播报服务

功能说明:
- 每分钟播报今日主线机会 (market_mainline_cls)
- 每分钟播报板块热度排行 Top10 (get_sector_heat)
- 每分钟播报板块轮动近4日数据 (get_sector_rotation)
- 自动推送到飞书机器人
"""

import time
import datetime
from typing import Optional


class MarketDataBot:
    """市场数据飞书播报机器人"""
    
    def __init__(self, feishu_bot):
        """
        初始化播报机器人
        
        Args:
            feishu_bot: FeishuBot 实例（来自 feishu_monitor.py）
        """
        self.feishu_bot = feishu_bot
        self.running = False
    
    def _format_mainline(self, data: dict) -> str:
        """
        格式化主线机会数据
        
        Args:
            data: market_mainline_cls() 返回的数据
            
        Returns:
            格式化后的文本
        """
        if not data:
            return "暂无主线机会数据"
        
        lines = ["🔥 **今日主线机会**\n"]
        
        # 解析 faucet_1, faucet_2, faucet_3 等主线
        for i in range(1, 4):
            key = f"faucet_{i}"
            if key in data:
                faucet = data[key]
                title = faucet.get("title", "")
                desc = faucet.get("desc", "")
                
                if title:
                    lines.append(f"【主线{i}】{title}")
                    if desc:
                        # 截断过长的描述
                        if len(desc) > 100:
                            desc = desc[:100] + "..."
                        lines.append(f"  {desc}")
                    
                    # 显示相关板块
                    plates = faucet.get("plate_list", [])
                    if plates:
                        plate_names = [p.get("plate_name", "") for p in plates[:5]]
                        lines.append(f"  板块: {'、'.join(plate_names)}")
                    
                    lines.append("")
        
        return "\n".join(lines)
    
    def _format_sector_heat(self, data: list, top_n: int = 10) -> str:
        """
        格式化板块热度数据
        
        Args:
            data: get_sector_heat() 返回的数据
            top_n: 显示前N个板块
            
        Returns:
            格式化后的文本
        """
        if not data:
            return "暂无板块热度数据"
        
        lines = ["📊 **板块热度排行 Top{}**\n".format(top_n)]
        
        for i, item in enumerate(data[:top_n], 1):
            plate_name = item.get("plate_name", "")
            cur_heat = item.get("cur_heat", 0)
            rank_change = item.get("rank_change", 0)
            is_new = item.get("is_new", 0)
            
            # 排名变化箭头
            if rank_change > 0:
                change_str = f"↑{rank_change}"
            elif rank_change < 0:
                change_str = f"↓{abs(rank_change)}"
            else:
                change_str = "-"
            
            # 新上榜标记
            new_tag = " 🆕" if is_new == 1 else ""
            
            lines.append(f"{i:2d}. {plate_name:<12} 热度:{cur_heat:>6.1f}  变化:{change_str:>4}{new_tag}")
        
        return "\n".join(lines)
    
    def _format_sector_rotation(self, data: list) -> str:
        """
        格式化板块轮动数据
        
        Args:
            data: get_sector_rotation() 返回的数据
            
        Returns:
            格式化后的文本
        """
        if not data:
            return "暂无板块轮动数据"
        
        lines = ["🔄 **板块轮动（近4日Top10）**\n"]
        
        for day_data in data:
            trade_date = day_data.get("trade_date", "")
            plates = day_data.get("plates", [])
            
            lines.append(f"📅 {trade_date}")
            
            # 显示前5个板块
            for i, plate in enumerate(plates[:5], 1):
                plate_name = plate.get("plate_name", "")
                change = plate.get("change", 0)
                
                # 涨跌幅颜色标记
                if change > 0:
                    change_str = f"+{change:.2f}% 🔺"
                elif change < 0:
                    change_str = f"{change:.2f}% 🔻"
                else:
                    change_str = f"{change:.2f}%"
                
                lines.append(f"  {i}. {plate_name:<12} {change_str}")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def send_market_report(self):
        """
        发送市场数据报告到飞书
        
        Returns:
            是否发送成功
        """
        try:
            from levistock.market.market_wind_cls import market_mainline_cls
            from levistock.sector.sector_heat_cls import get_sector_heat
            from levistock.sector.sector_rotation_cls import get_sector_rotation
            
            print(f"[INFO] 获取市场数据... ({datetime.datetime.now().strftime('%H:%M:%S')})")
            
            # 获取三个数据源
            mainline_data = market_mainline_cls()
            heat_data = get_sector_heat()
            rotation_data = get_sector_rotation(days=4)
            
            # 格式化消息
            mainline_text = self._format_mainline(mainline_data)
            heat_text = self._format_sector_heat(heat_data, top_n=10)
            rotation_text = self._format_sector_rotation(rotation_data)
            
            # 组合完整报告
            report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_report = f"""⏰ 播报时间: {report_time}

{mainline_text}

---

{heat_text}

---

{rotation_text}

---
💡 每分钟自动更新 | 数据来源: 财联社"""
            
            # 发送到飞书
            title = f"市场数据播报 - {report_time}"
            result = self.feishu_bot.send_text(full_report)
            
            if result.get("code") == 0:
                print(f"[SUCCESS] 播报发送成功")
                return True
            else:
                print(f"[ERROR] 播报发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"[ERROR] 播报异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start(self, interval: int = 60):
        """
        启动定时播报服务
        
        Args:
            interval: 播报间隔（秒），默认60秒（1分钟）
        """
        self.running = True
        print("=" * 70)
        print(" " * 15 + "财联社市场数据 - 定时播报服务")
        print("=" * 70)
        print(f"播报内容:")
        print(f"  1. 今日主线机会 (market_mainline_cls)")
        print(f"  2. 板块热度排行 Top10 (get_sector_heat)")
        print(f"  3. 板块轮动近4日 (get_sector_rotation)")
        print(f"播报间隔: {interval}秒")
        print(f"启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print("开始播报...\n")
        
        try:
            while self.running:
                success = self.send_market_report()
                
                if not success:
                    print("[WARN] 本次播报失败，等待下次尝试")
                
                # 等待下一次播报
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n[INFO] 服务已停止")
            self.stop()
    
    def stop(self):
        """停止播报服务"""
        self.running = False
        print("[INFO] 播报服务已停止")


if __name__ == "__main__":
    # ==================== 配置区域 ====================
    
    # 导入飞书机器人
    from feishu_monitor import FeishuBot
    
    # 加载配置
    import os
    import importlib.util
    
    config_path = os.path.join(os.path.dirname(__file__), "config.py")
    if os.path.exists(config_path):
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        FEISHU_WEBHOOK_URL = config.FEISHU_WEBHOOK_URL
        FEISHU_SECRET = getattr(config, 'FEISHU_SECRET', None)
        POLL_INTERVAL = getattr(config, 'POLL_INTERVAL', 60)
    else:
        print("[ERROR] 配置文件不存在，请复制 config_example.py 为 config.py")
        exit(1)
    
    # ================================================
    
    # 创建飞书机器人
    bot = FeishuBot(webhook_url=FEISHU_WEBHOOK_URL, secret=FEISHU_SECRET)
    
    # 创建市场数据播报器
    market_bot = MarketDataBot(feishu_bot=bot)
    
    # 启动播报（每分钟一次）
    market_bot.start(interval=POLL_INTERVAL)
