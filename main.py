import asyncio
import os
import threading
import signal
import sys
import time
from collections import defaultdict
from typing import List
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from models import Opportunity
from fetcher import AsyncFetcher
from web_dashboard import start_flask_app, update_dashboard_data
from notifier import TelegramNotifier

load_dotenv()
console = Console()

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
FETCH_INTERVAL = int(os.getenv("FETCH_INTERVAL", 0.0001))
MIN_SPREAD = float(os.getenv("MIN_SPREAD", 0.025))

class ArbitrageBot:
    def __init__(self):
        self.fetcher = AsyncFetcher(USER_AGENT)
        self.notifier = TelegramNotifier()
        self.running = True
        self.latest_opportunities = []

    def calculate_arbitrage(self, rates: List) -> List[Opportunity]:
        
        opps = []
        
        # 1. Filter for POSITIVE rates (> 0)
        positives = [r for r in rates if r.rate > 0]
        
        # 2. Sort DESCENDING (Most positive first: 5.0, 2.0, 0.1)
        positives.sort(key=lambda x: x.rate, reverse=True)

        for r in positives:
            # Check if 'price' exists on the FundingRate object, else N/A
            price_val = getattr(r, 'price', 'N/A')
            price_str = f"${price_val}" if price_val != 'N/A' else "N/A"

            opp = Opportunity(
                symbol=r.symbol,
                long_exchange=r.exchange,
                long_rate=r.rate,
                short_exchange=price_str,  # Storing Price here
                short_rate=0.0,
                spread=r.rate,
                annualized_spread=r.rate * 3 * 365
            )
            
            opps.append(opp)
        
        return opps

    async def run_loop(self):
        await self.fetcher.start_session()
        console.print(Panel.fit("[bold green]📈 Positive Funding Monitor Active[/bold green]", border_style="green"))
        
        while self.running:
            start_time = time.perf_counter()
            
            # 1. Fetch
            all_rates = await self.fetcher.fetch_all()
            
            # 2. Stats
            total_pairs = len(set(r.symbol for r in all_rates))
            
            # 3. Calculate
            self.latest_opportunities = self.calculate_arbitrage(all_rates)
            
            # 4. Notify & Web
            update_dashboard_data(self.latest_opportunities, total_pairs)
            await self.notifier.process(self.latest_opportunities)
            
            elapsed = time.perf_counter() - start_time
            
            # 5. Output
            self._print_dashboard(len(all_rates), total_pairs, len(self.latest_opportunities), elapsed)
            
            sleep_time = max(0, FETCH_INTERVAL - elapsed)
            await asyncio.sleep(sleep_time)

    def _print_dashboard(self, total_rates, total_pairs, opp_count, latency):
        summary = Table(box=box.SIMPLE, show_header=False)
        summary.add_column("Key", style="cyan")
        summary.add_column("Val", style="bold white")
        summary.add_row("⏱️ Latency", f"{latency:.3f}s")
        summary.add_row("📡 Points", f"{total_rates}")
        summary.add_row("📈 Positives", f"{opp_count}")
        
        # Display Table: Highest Positive Funding
        opp_table = Table(title="📈 HIGHEST FUNDING RATES (Positive to 0)", box=box.ROUNDED)
        opp_table.add_column("#", style="dim")
        opp_table.add_column("Symbol", style="bold white")
        opp_table.add_column("Exchange", style="cyan")
        opp_table.add_column("Funding Rate", justify="right", style="bold green")
        opp_table.add_column("Price", justify="right", style="yellow")
        
        # Display top 20
        for i, o in enumerate(self.latest_opportunities[:20], 1):
            # o.short_exchange is where we stored the price string
            opp_table.add_row(
                str(i), 
                o.symbol, 
                o.long_exchange, 
                f"{o.long_rate:.4f}%", 
                o.short_exchange 
            )

        console.print(Panel(summary, title="Status"))
        if self.latest_opportunities:
            console.print(opp_table)
        else:
            console.print("[yellow]No positive funding rates found.[/yellow]")

    async def close(self):
        await self.fetcher.close()

def signal_handler(sig, frame):
    print("\n[INFO] Shutting down...")
    sys.exit(0)

async def main():
    bot = ArbitrageBot()
    try:
        await bot.run_loop()
    finally:
        await bot.close()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    try:
        if sys.platform != 'win32':
            import uvloop
            uvloop.install()
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
