"""
财联社市场数据 - 风口板块播报服务

功能：
- 播报今日风口板块列表
- 播报风口板块龙头股
- 播报今日主线机会
- 通过配置开关控制
"""

import time
import datetime


class MarketWindBot:
    """风口板块飞书播报机器人"""
    
    def __init__(self, feishu_bot):
        """
        初始化播报机器人
        
        Args:
            feishu_bot: FeishuBot 实例（来自 news/feishu_monitor.py）
        """
        self.feishu_bot = feishu_bot
        self.running = False
    
    def _format_wind_plates(self, data: list) -> str:
        """
        格式化风口板块数据
        
        Args:
            data: market_wind_cls() 返回的数据
            
        Returns:
            格式化后的文本
        """
        if not data:
            return "暂无风口板块数据"
        
        lines = ["🌪️ **今日风口板块**\n"]
        
        for i, item in enumerate(data, 1):
            plate_name = item.get("plate_name", "")
            catalyst = item.get("catalyst", "")
            
            # 截断过长的描述
            if len(catalyst) > 50:
                catalyst = catalyst[:50] + "..."
            
            lines.append(f"{i}. **{plate_name}**")
            if catalyst:
                lines.append(f"   {catalyst}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _format_wind_stocks(self, plate_code: str, plate_name: str) -> str:
        """
        格式化风口板块龙头股
        
        Args:
            plate_code: 板块代码
            plate_name: 板块名称
            
        Returns:
            格式化后的文本
        """
        try:
            from levistock.market.market_wind_cls import market_wind_stocks_cls
            
            stocks = market_wind_stocks_cls(plate_code)
            
            if not stocks:
                return f"  {plate_name}: 暂无龙头股数据"
            
            lines = [f"  📈 {plate_name} 龙头股:"]
            
            for stock in stocks[:5]:  # 只显示前5只
                secu_name = stock.get("secu_name", "")
                last_px = stock.get("last_px", "-")
                change = stock.get("change", "-")
                continuous = stock.get("continuous", "-")
                
                # 连板标记
                cont_tag = f" ({continuous}连板)" if continuous and continuous != "-" else ""
                
                lines.append(f"    • {secu_name} {last_px}元 {change}{cont_tag}")
            
            return "\n".join(lines)
            
        except Exception as e:
            return f"  {plate_name}: 获取龙头股失败 ({e})"
    
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
        
        lines = ["🎯 **今日主线机会**\n"]
        
        # 解析 faucet_1, faucet_2, faucet_3 等主线
        for i in range(1, 4):
            key = f"faucet_{i}"
            if key in data:
                faucet = data[key]
                title = faucet.get("title", "")
                desc = faucet.get("desc", "")
                
                if title:
                    lines.append(f"**主线{i}: {title}**")
                    if desc:
                        # 截断过长的描述
                        if len(desc) > 80:
                            desc = desc[:80] + "..."
                        lines.append(f"  {desc}")
                    
                    # 显示相关板块
                    plates = faucet.get("plate_list", [])
                    if plates:
                        plate_names = [p.get("plate_name", "") for p in plates[:5]]
                        lines.append(f"  相关板块: {'、'.join(plate_names)}")
                    
                    lines.append("")
        
        return "\n".join(lines)
    
    def send_market_wind_report(self, include_stocks: bool = True):
        """
        发送风口板块报告到飞书
        
        Args:
            include_stocks: 是否包含龙头股信息
            
        Returns:
            是否发送成功
        """
        try:
            from levistock.market.market_wind_cls import market_wind_cls, market_mainline_cls
            
            print(f"[INFO] 获取风口板块数据... ({datetime.datetime.now().strftime('%H:%M:%S')})")
            
            # 获取风口板块
            wind_data = market_wind_cls()
            
            # 获取主线机会
            mainline_data = market_mainline_cls()
            
            # 格式化消息
            wind_text = self._format_wind_plates(wind_data)
            mainline_text = self._format_mainline(mainline_data)
            
            # 如果需要，获取龙头股信息
            stocks_text = ""
            if include_stocks and wind_data:
                stocks_lines = ["\n🐉 **风口板块龙头股**\n"]
                for plate in wind_data[:3]:  # 只显示前3个板块的龙头股
                    plate_code = plate.get("plate_code", "")
                    plate_name = plate.get("plate_name", "")
                    if plate_code:
                        stock_info = self._format_wind_stocks(plate_code, plate_name)
                        stocks_lines.append(stock_info)
                        stocks_lines.append("")
                stocks_text = "\n".join(stocks_lines)
            
            # 组合完整报告
            report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_report = f"""⏰ 播报时间: {report_time}

{wind_text}

---
{stocks_text}
---

{mainline_text}

---
💡 数据来源: 财联社"""
            
            # 发送到飞书
            title = f"风口板块播报 - {report_time}"
            result = self.feishu_bot.send_text(full_report)
            
            if result.get("code") == 0:
                print(f"[SUCCESS] 风口板块播报发送成功")
                return True
            else:
                print(f"[ERROR] 风口板块播报发送失败: {result}")
                return False
                
        except Exception as e:
            print(f"[ERROR] 风口板块播报异常: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start(self, interval: int = 300, include_stocks: bool = True):
        """
        启动定时播报服务
        
        Args:
            interval: 播报间隔（秒），默认300秒（5分钟）
            include_stocks: 是否包含龙头股信息
        """
        self.running = True
        print("=" * 70)
        print(" " * 15 + "财联社风口板块 - 定时播报服务")
        print("=" * 70)
        print(f"播报内容:")
        print(f"  1. 今日风口板块列表")
        if include_stocks:
            print(f"  2. 风口板块龙头股")
        print(f"  3. 今日主线机会")
        print(f"播报间隔: {interval}秒")
        print(f"启动时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print("开始播报...\n")
        
        try:
            while self.running:
                success = self.send_market_wind_report(include_stocks=include_stocks)
                
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
        print("[INFO] 风口板块播报服务已停止")


if __name__ == "__main__":
    # 测试代码
    import sys
    import os
    
    # 添加 news 目录到路径以使用 FeishuBot
    news_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "news")
    sys.path.insert(0, news_dir)
    
    from feishu_monitor import FeishuBot
    
    # 加载配置
    config_path = os.path.join(news_dir, "config.py")
    if os.path.exists(config_path):
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", config_path)
        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config)
        
        bot = FeishuBot(
            webhook_url=config.FEISHU_WEBHOOK_URL,
            secret=getattr(config, 'FEISHU_SECRET', None)
        )
        
        wind_bot = MarketWindBot(feishu_bot=bot)
        
        # 测试单次播报
        wind_bot.send_market_wind_report(include_stocks=True)
    else:
        print("[ERROR] 配置文件不存在")
