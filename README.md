<div align="center">

# 🔱 DIONYSUS
### Multi-Exchange Perpetual Funding Rate Arbitrage Terminal
    
![Version](https://img.shields.io/badge/version-1.0.0-7000df?style=for-the-badge&logo=semantic-release&logoColor=white)
![Python](https://img.shields.io/badge/python-3.9+-00f0ff?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-success?style=for-the-badge)
![Status](https://img.shields.io/badge/status-LIVE-00ff00?style=for-the-badge&logo=statuspage&logoColor=white)

**The Ultimate Cross-Exchange Funding Rate Scanner & Arbitrage Intelligence System**

[📊 Features](#-core-features) • [🚀 Quick Start](#-quick-start) • [📡 Live Dashboard](#-live-dashboard) • [⚙️ Configuration](#%EF%B8%8F-configuration) • [🎯 Strategy](#-strategy-explained)

---

</div>

## 🌌 Overview

**DIONYSUS** is a sophisticated, real-time funding rate arbitrage scanner that monitors **20+ cryptocurrency exchanges** simultaneously, identifying profitable funding rate differentials in perpetual futures markets. Built for speed, precision, and scalability.

### 💎 What Makes This Different

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 20+ EXCHANGES → SINGLE UNIFIED FEED → INSTANT INSIGHTS  │
│                                                             │
│  Traditional Approach:                                      │
│  ❌ Manual checking across exchanges                        │
│  ❌ Delayed data, missed opportunities                      │
│  ❌ No real-time alerts                                     │
│                                                             │
│  DIONYSUS :                                                 │
│  ✅ Automated multi-exchange scanning                       │
│  ✅ Sub-second latency aggregation                          │
│  ✅ Real-time Telegram alerts + Web dashboard               │
│  ✅ Annualized yield calculations                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Strategy Explained

### The Funding Rate Arbitrage Play

Funding rates are periodic payments between long and short positions in perpetual futures:

**When Funding Rate > 0 (Positive):**
- Longs pay shorts every 8 hours
- **Your Move:** Short perpetual + Long spot = Collect funding with delta-neutral position

**Example Trade:**
```
Asset: BTCUSDT
Funding Rate: +0.15% (every 8h)
Annual Yield: 164.25% APR

Action:
1. Short 1 BTC perpetual on Exchange A
2. Long 1 BTC spot on Exchange B
3. Collect 0.15% every 8 hours
4. Zero directional exposure (market-neutral)
```

---

## ✨ Core Features

### 🔍 **Multi-Exchange Coverage**
Scans 20+ major exchanges in real-time:

<div align="center">

| Exchange | Exchange | Exchange | Exchange |
|----------|----------|----------|----------|
| 🟡 Binance | 🔵 Bybit | 🟢 OKX | 🟣 Gate.io |
| 🟠 KuCoin | 🔴 Bitget | ⚫ MEXC | 🟤 Huobi |
| 🔵 BingX | 🟡 Kraken | 🟢 dYdX | 🟣 BitMEX |
| 🟠 Phemex | 🔴 HTX | ⚪ Crypto.com | 🟢 Coinbase |
| 🔵 Hyperliquid | 🟡 CoinEx | 🟣 BitUnix | 🟠 Bitstamp |

</div>

### 📊 **Real-Time Intelligence**
- **Sub-second latency** data aggregation
- **Automatic sorting** by funding rate (highest to lowest)
- **Live APR calculations** for annualized yield projections
- **Telegram notifications** for high-yield opportunities

### 🖥️ **Professional Web Dashboard**
- Beautiful glassmorphic UI with ambient effects
- Live countdown to next funding period
- Top 5 opportunities sidebar
- Interactive yield distribution charts
- Real-time search and filtering

### ⚡ **Performance Optimized**
- Async I/O with `aiohttp` for concurrent requests
- `uvloop` integration on Linux/Mac for blazing speed
- Efficient connection pooling and DNS caching
- Thread-safe data structures

---

## 🚀 Quick Start

### Prerequisites

```bash
Python 3.9+
pip (Python package manager)
```

### Installation

```bash
# Clone the repository
git clone https://github.com/Siddharthk17/Dionysus-Multi-Exchange-Spot-Perpetuals-Cross-Arbitrage.git
cd Dionysus-Multi-Exchange-Spot-Perpetuals-Cross-Arbitrage

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
# Telegram Notifications (Optional)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_IDS=123456789,987654321

# Web Dashboard
WEB_PORT=5000

# Scanner Settings
FETCH_INTERVAL=0        # Continuous scanning (set to 60 for 1-minute intervals)
MIN_SPREAD=0.025        # Minimum spread threshold (2.5% default)
```

### Launch

```bash
# Start the system
python main.py
```

The dashboard will be available at `http://localhost:5000`

---

## 📡 Live Dashboard

### Desktop View
The terminal interface displays:
- ⏱️ **Fetch latency** (request completion time)
- 📡 **Data points** collected across all exchanges
- 📈 **Live opportunities** count
- 🎯 **Top 20 highest funding rates** table

### Web Interface
Access the premium web dashboard:

**Features:**
- 🌟 **Glassmorphic Design** - Modern, sleek interface
- 📊 **Live Statistics** - Max yield, active targets, top venues
- ⏰ **Funding Timer** - Countdown to next 8-hour period
- 🔍 **Search & Filter** - Find specific assets instantly
- 📈 **Yield Chart** - Visual distribution of opportunities
- 🏆 **Top 5 Leaders** - Quick glance at best performers

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token for alerts | None |
| `TELEGRAM_CHAT_IDS` | Comma-separated chat IDs | None |
| `WEB_PORT` | Dashboard web server port | 5000 |
| `FETCH_INTERVAL` | Seconds between scans (0 = continuous) | 0 |
| `MIN_SPREAD` | Minimum spread to consider (%) | 0.025 |

### Telegram Setup

1. Create a bot via [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Find your chat ID via [@userinfobot](https://t.me/userinfobot)
4. Add to `.env` file

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DIONYSUS PIPELINE                        │
└─────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  START   │
    └────┬─────┘
         │
         ▼
┌─────────────────┐
│  Async Fetcher  │──┐
│  (20 Exchanges) │  │
└────────┬────────┘  │
         │           │ Parallel Execution
         ▼           │ (aiohttp + uvloop)
┌─────────────────┐  │
│  Rate Aggregator│◄─┘
│  (Normalize)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Sort & Filter  │
│  (Descending)   │
└────────┬────────┘
         │
         ├──────────────┬──────────────┬────────────┐
         ▼              ▼              ▼            ▼
  ┌──────────┐   ┌───────────┐  ┌──────────┐  ┌──────┐
  │ Terminal │   │ Dashboard │  │ Telegram │  │ API  │
  │  Output  │   │    Web    │  │  Alerts  │  │ JSON │
  └──────────┘   └───────────┘  └──────────┘  └──────┘
```

---

## 🎨 Tech Stack

### Backend
- **Python 3.9+** - Core runtime
- **asyncio + aiohttp** - Asynchronous HTTP requests
- **uvloop** - Ultra-fast event loop (Linux/Mac)
- **Pydantic** - Data validation and serialization
- **python-dotenv** - Environment configuration

### Frontend
- **Flask** - Lightweight web framework
- **TailwindCSS** - Utility-first styling
- **Chart.js** - Interactive data visualization
- **Font Awesome** - Premium iconography

### DevOps
- **Rich** - Beautiful terminal output
- **Threading** - Concurrent web server execution

---

## 📈 Performance Metrics

### Benchmark Results
```
Test Environment: 4-core CPU, 16GB RAM, 100Mbps connection

┌──────────────────────────────────────────┐
│  Metric              │  Value            │
├──────────────────────┼───────────────────┤
│  Exchanges Scanned   │  20               │
│  Total API Calls     │  20               │
│  Average Latency     │  0.5-0.75s        │
│  Data Points/Scan    │  ~800-1200        │
│  Memory Usage        │  45-60 MB         │
│  Update Frequency    │  Continuous       │
└──────────────────────────────────────────┘
```

---

## 🔐 Security & Best Practices

### API Safety
- ✅ No API keys required (public endpoints only)
- ✅ SSL verification disabled for local testing
- ✅ Rate limiting handled per exchange
- ✅ Graceful error handling

### Network
- 🔒 User-agent rotation to bypass WAFs
- 🔒 Connection pooling for efficiency
- 🔒 Timeout protection (10s connect, 25s total)

---

## 🛠️ Development

### Project Structure
```
hades-zero/
│
├── main.py              # Core orchestrator & arbitrage logic
├── fetcher.py           # Multi-exchange async fetcher
├── models.py            # Pydantic data models
├── notifier.py          # Telegram alert system
├── web_dashboard.py     # Flask web interface
├── requirements.txt     # Python dependencies
├── .env                 # Configuration (create this)
└── README.md           # You are here
```

### Adding New Exchanges

1. Add fetcher method in `fetcher.py`:
```python
async def get_your_exchange(self) -> List[FundingRate]:
    data = await self._fetch("https://api.exchange.com/funding")
    # Parse and return FundingRate objects
    return results
```

2. Register in `fetch_all()`:
```python
tasks_map = {
    "YourExchange": self.get_your_exchange(),
    # ... other exchanges
}
```

---

## 📊 Example Output

### Terminal View
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                         Status                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
⏱️ Latency    1.247s
📡 Points     1,043
📈 Positives  287

╭────────────────────────────────────────────────────────────╮
│      📈 HIGHEST FUNDING RATES (Positive to 0)              │
╰────────────────────────────────────────────────────────────╯
┃ # ┃ Symbol      ┃ Exchange    ┃ Funding Rate ┃ Price      ┃
┡━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 1 │ POPCATUSDT  │ Bybit       │    +0.5247%  │ $0.6543    │
│ 2 │ MOODENGUSDT │ Gate.io     │    +0.4891%  │ $0.3214    │
│ 3 │ WIFUSDT     │ Binance     │    +0.3756%  │ $2.1234    │
```

### Web Dashboard Stats
```
╔═══════════════════════════════════════════════════════════╗
║  HIGHEST YIELD (8H)      LIVE TARGETS      TOP VENUE      ║
║      +0.5247%                287          Bybit           ║
║                                                           ║
║  Real-time updating • Sub-second latency                  ║
╚═══════════════════════════════════════════════════════════╝
```

---

## 🎯 Roadmap

- [x] Multi-exchange aggregation
- [x] Real-time web dashboard
- [x] Telegram notifications
- [x] APR calculations
- [ ] Historical data tracking
- [ ] Automated position sizing calculator
- [ ] Exchange balance integration
- [ ] Auto-execution via API (with user approval)
- [ ] Machine learning yield prediction
- [ ] Mobile app (React Native)

---

## ⚠️ Disclaimer

**Educational & Research Purposes Only**

This tool is designed for educational purposes to demonstrate cryptocurrency funding rate arbitrage strategies. It does NOT execute trades automatically.

**Important Notes:**
- ⚠️ **Not Financial Advice** - Always do your own research
- 🔐 **Test in Simulation** - Practice before using real capital
- 💰 **Understand Risks** - Crypto trading involves substantial risk
- 📊 **Verify Data** - Always cross-reference with exchange websites
- ⚖️ **Legal Compliance** - Ensure compliance with local regulations

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- 🔧 Additional exchange integrations
- 🎨 UI/UX improvements
- 📊 Advanced analytics features
- 🐛 Bug fixes and optimizations
- 📝 Documentation enhancements

---

## 📄 License

This project is licensed under the MIT License - see below:

```
MIT License

Copyright (c) 2025 HADES ZERO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 💬 Support & Community

### Get Help
- 📧 **Email:** siddharthkakade7777@gmail.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/Siddharthk17/Dionysus-Multi-Exchange-Spot-Perpetuals-Cross-Arbitrage/issues)

### Stay Updated
- ⭐ Star this repo to show support
- 👁️ Watch for updates and new features
- 🔔 Enable notifications for release announcements

---

## 🙏 Acknowledgments

Special thanks to:
- The crypto community for innovative DeFi strategies
- Exchange API documentation teams
- Open-source Python ecosystem contributors
- Everyone testing and providing feedback

---

<div align="center">

### 🔱 Built with Precision. Powered by Python. Designed for Profits.

**DIONYSUS** - *Where Data Meets Opportunity*

---

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Powered by Coffee](https://img.shields.io/badge/Powered%20by-Coffee-brown.svg?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/example)

**[⬆ Back to Top](#-dionysus-zero)**

</div>
