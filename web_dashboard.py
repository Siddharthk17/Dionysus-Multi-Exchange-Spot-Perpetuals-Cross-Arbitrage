import logging
from flask import Flask, render_template_string, jsonify
from threading import Lock
import time
from collections import Counter

# Silence Flask logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

# Thread-safe Data Store
data_lock = Lock()
latest_data = {
    "opportunities": [],
    "metadata": {
        "last_update": 0,
        "total_pairs_scanned": 0,
        "active_exchanges": 0,
        "top_short_exchange": "Initializing...",
        "api_latency": 0
    }
}

def update_dashboard_data(opportunities, total_pairs_count=0):
    """
    Updates global data with Positive Funding opportunities.
    """
    global latest_data
    with data_lock:
        timestamp = time.time()
        
        opps_list = []
        short_exchanges = []
        unique_exchanges = set()

        for opp in opportunities:
            # Logic: Positive Funding Rate (>0)
            # Strategy: Short Perp (Receive Funding) / Long Spot
            opps_list.append({
                "symbol": opp.symbol,
                "funding_rate": opp.long_rate,      # The positive rate
                "exchange": opp.long_exchange,      # The exchange to SHORT
                "price": opp.short_exchange,        # The current price (hack from main.py)
                "apr": opp.annualized_spread        # Annualized Yield
            })
            
            short_exchanges.append(opp.long_exchange)
            unique_exchanges.add(opp.long_exchange)

        top_short = Counter(short_exchanges).most_common(1)
        top_short_name = top_short[0][0] if top_short else "N/A"

        latest_data = {
            "opportunities": opps_list,
            "metadata": {
                "last_update": timestamp,
                "total_pairs_scanned": total_pairs_count,
                "active_exchanges": len(unique_exchanges),
                "top_short_exchange": top_short_name,
                "count": len(opps_list)
            }
        }

@app.route('/api/data')
def get_data():
    with data_lock:
        return jsonify(latest_data)

@app.route("/")
def dashboard():
    return render_template_string(HTML_TEMPLATE)

def start_flask_app():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hades | Arbitrage Terminal</title>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    
    <!-- Premium Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@300;400;500;700&display=swap" rel="stylesheet">

    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Plus Jakarta Sans', 'sans-serif'],
                        mono: ['Space Grotesk', 'monospace'],
                    },
                    colors: {
                        void: '#030014',
                        glass: 'rgba(255, 255, 255, 0.03)',
                        glassBorder: 'rgba(255, 255, 255, 0.08)',
                        accent: '#7000df',
                        success: '#00f0ff',
                    }
                }
            }
        }
    </script>

    <style>
        body {
            background-color: #030014;
            color: #ffffff;
            overflow-x: hidden;
        }

        /* Ambient Background Glow */
        .ambient-glow {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: 
                radial-gradient(circle at 15% 50%, rgba(112, 0, 223, 0.15), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(0, 240, 255, 0.1), transparent 25%);
            z-index: -1;
            pointer-events: none;
        }

        /* Glassmorphism Card */
        .glass-card {
            background: linear-gradient(180deg, rgba(20, 20, 30, 0.6) 0%, rgba(10, 10, 15, 0.8) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
            transition: all 0.3s ease;
        }

        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 0 20px rgba(112, 0, 223, 0.2);
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #1f1f2e; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #7000df; }

        /* Loading Animation */
        .loader {
            width: 32px;
            height: 32px;
            border: 2px solid #FFF;
            border-radius: 50%;
            display: inline-block;
            position: relative;
            box-sizing: border-box;
            animation: rotation 1s linear infinite;
        }
        .loader::after {
            content: '';  
            position: absolute; left: 50%; top: 50%;
            transform: translate(-50%, -50%);
            width: 24px; height: 24px;
            border-radius: 50%;
            border: 2px solid;
            border-color: #7000df transparent;
        }
        @keyframes rotation { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="h-screen flex flex-col font-sans">
    
    <div class="ambient-glow"></div>

    <!-- NAVBAR -->
    <nav class="h-16 flex items-center justify-between px-8 border-b border-white/5 z-50 bg-void/50 backdrop-blur-md">
        <div class="flex items-center gap-4">
            <div class="relative w-8 h-8 flex items-center justify-center bg-white/5 rounded-lg border border-white/10 shadow-lg">
                <i class="fa-solid fa-layer-group text-sm text-white"></i>
                <div class="absolute -top-1 -right-1 w-1.5 h-1.5 bg-success rounded-full animate-pulse"></div>
            </div>
            <div>
                <h1 class="text-lg font-bold tracking-wide text-white">HADES <span class="font-light text-gray-400">Zero</span></h1>
            </div>
        </div>

        <div class="flex items-center gap-6">
            <div class="hidden md:flex flex-col items-end">
                <span class="text-[9px] text-gray-500 uppercase tracking-widest font-semibold">Funding Timer</span>
                <span id="funding-timer" class="font-mono text-sm font-medium text-white/90">--:--:--</span>
            </div>
            <div class="h-6 w-px bg-white/10 hidden md:block"></div>
            <div class="flex items-center gap-2">
                <i class="fa-regular fa-clock text-gray-500 text-xs"></i>
                <span id="utc-clock" class="font-mono text-xs text-gray-400">00:00:00 UTC</span>
            </div>
        </div>
    </nav>

    <!-- MAIN DASHBOARD -->
    <div class="flex-1 p-6 flex flex-col gap-6 overflow-hidden">
        
        <!-- BENTO GRID STATS -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 shrink-0">
            
            <!-- Hero Stat: Max Yield -->
            <div class="glass-card rounded-2xl p-5 relative overflow-hidden group">
                <div class="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                    <i class="fa-solid fa-bolt text-5xl text-white"></i>
                </div>
                <div class="text-[10px] text-gray-400 font-mono uppercase tracking-widest mb-1">Highest Yield (8h)</div>
                <div class="flex items-baseline gap-2">
                    <div id="stat-max-rate" class="text-3xl font-mono font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-300">0.00%</div>
                </div>
                <div class="mt-2 text-xs text-success flex items-center gap-1">
                    <i class="fa-solid fa-arrow-trend-up"></i> Top Performer
                </div>
            </div>

            <!-- Stat 2: Total Pairs Scanned (REPLACED APR) -->
            <div class="glass-card rounded-2xl p-5">
                <div class="text-[10px] text-gray-400 font-mono uppercase tracking-widest mb-1">Market Coverage</div>
                <div id="stat-pairs-main" class="text-3xl font-mono font-medium text-white">0</div>
                <div class="mt-2 text-xs text-gray-500">
                    Total Unique Pairs Scanned
                </div>
            </div>

            <!-- Stat 3: Live Targets -->
            <div class="glass-card rounded-2xl p-5">
                <div class="text-[10px] text-gray-400 font-mono uppercase tracking-widest mb-1">Live Targets</div>
                <div class="flex items-center justify-between">
                    <div id="stat-count" class="text-3xl font-mono font-medium text-white">0</div>
                </div>
                <div class="mt-2 text-xs text-gray-500">
                    Assets > 0% Funding
                </div>
            </div>

            <!-- Stat 4: Top Venue -->
            <div class="glass-card rounded-2xl p-5 flex flex-col justify-between">
                <div>
                    <div class="text-[10px] text-gray-400 font-mono uppercase tracking-widest mb-1">Top Venue</div>
                    <div id="stat-dom-short" class="text-xl font-medium text-white truncate">Scanning...</div>
                </div>
                <div class="flex justify-between items-end mt-2">
                    <div class="text-[10px] text-gray-500 uppercase">Short Liquidity Source</div>
                    <div class="w-1.5 h-1.5 bg-success rounded-full shadow-[0_0_8px_#00f0ff]"></div>
                </div>
            </div>
        </div>

        <!-- CONTENT SPLIT -->
        <div class="flex-1 grid grid-cols-1 lg:grid-cols-3 gap-6 overflow-hidden">
            
            <!-- MAIN TABLE -->
            <div class="lg:col-span-2 glass-card rounded-2xl flex flex-col overflow-hidden">
                <!-- Toolbar -->
                <div class="px-6 py-4 border-b border-white/5 flex justify-between items-center bg-white/[0.01]">
                    <h2 class="font-mono text-xs text-gray-300 uppercase tracking-widest flex items-center gap-2">
                        <i class="fa-solid fa-list text-accent"></i> Market Opportunities
                    </h2>
                    
                    <div class="relative group">
                        <input type="text" id="table-search" placeholder="SEARCH..." 
                            class="bg-white/5 border border-white/10 rounded-lg pl-3 pr-8 py-1 text-[10px] text-white font-mono focus:outline-none focus:border-accent/50 w-32 transition-all placeholder-gray-600 uppercase">
                        <i class="fa-solid fa-magnifying-glass absolute right-2.5 top-1/2 -translate-y-1/2 text-gray-600 text-[10px]"></i>
                    </div>
                </div>

                <!-- Table Header -->
                <div class="grid grid-cols-12 px-6 py-3 bg-black/20 border-b border-white/5 text-[9px] font-bold text-gray-500 uppercase tracking-wider font-mono">
                    <div class="col-span-1">#</div>
                    <div class="col-span-3">Asset</div>
                    <div class="col-span-2 text-right">Funding Rate</div>
                    <div class="col-span-2 text-right">Yield (APR)</div>
                    <div class="col-span-2 text-center">Exchange</div>
                    <div class="col-span-2 text-right">Mark Price</div>
                </div>

                <!-- List -->
                <div id="opp-list" class="flex-1 overflow-y-auto custom-scroll p-2">
                    <!-- Loading State -->
                    <div class="h-full flex flex-col items-center justify-center gap-4 text-gray-600">
                        <span class="loader"></span>
                        <span class="font-mono text-[10px] tracking-widest">AWAITING FEED...</span>
                    </div>
                </div>
            </div>

            <!-- SIDEBAR: CHART & TOP 5 LOG -->
            <div class="flex flex-col gap-6 overflow-hidden">
                
                <!-- Chart -->
                <div class="glass-card rounded-2xl p-5 flex flex-col h-1/2">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-[10px] font-mono text-gray-400 uppercase tracking-widest">Yield Distribution</h3>
                    </div>
                    <div class="flex-1 relative">
                        <canvas id="yieldChart"></canvas>
                    </div>
                </div>

                <!-- TOP 5 LOG -->
                <div class="glass-card rounded-2xl p-5 flex-1 flex flex-col relative overflow-hidden">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-[10px] font-mono text-gray-400 uppercase tracking-widest">Top 5 Leaders</h3>
                        <div class="px-2 py-0.5 bg-success/10 border border-success/20 rounded text-[9px] text-success font-mono">LIVE</div>
                    </div>
                    
                    <div id="top-5-list" class="flex-1 overflow-y-auto space-y-2 pr-1">
                        <!-- JS Injects Top 5 Here -->
                        <div class="text-[10px] font-mono text-gray-600">Waiting for data...</div>
                    </div>
                    
                    <!-- Footer -->
                    <div class="mt-auto pt-3 border-t border-white/5 flex justify-between items-center text-[9px] text-gray-600 font-mono">
                        <span>SYSTEM: OPTIMAL</span>
                        <span>LATENCY: LOW</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- SCRIPT -->
    <script>
        // CONFIG
        let chartInstance = null;

        const dom = {
            list: document.getElementById('opp-list'),
            stats: {
                rate: document.getElementById('stat-max-rate'),
                pairs: document.getElementById('stat-pairs-main'), // Updated ID
                count: document.getElementById('stat-count'),
                dom: document.getElementById('stat-dom-short')
            },
            search: document.getElementById('table-search'),
            timer: document.getElementById('funding-timer'),
            clock: document.getElementById('utc-clock'),
            topList: document.getElementById('top-5-list')
        };

        // CHART INIT
        function initChart() {
            const ctx = document.getElementById('yieldChart').getContext('2d');
            Chart.defaults.font.family = "'Space Grotesk', monospace";
            Chart.defaults.color = "#6b7280";
            
            const gradient = ctx.createLinearGradient(0, 0, 0, 300);
            gradient.addColorStop(0, '#00f0ff');
            gradient.addColorStop(1, 'rgba(0, 240, 255, 0.05)');

            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        data: [],
                        backgroundColor: gradient,
                        borderRadius: 3,
                        barThickness: 10,
                        hoverBackgroundColor: '#ffffff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { color: 'rgba(255, 255, 255, 0.03)' },
                            ticks: { font: { size: 9 }, color: '#4b5563' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { display: false }
                        }
                    },
                    animation: { duration: 400 }
                }
            });
        }

        // UTILS
        const fmtPct = (n) => (n).toFixed(4) + '%';
        const fmtApr = (n) => (n).toFixed(2) + '%';

        function updateTime() {
            const now = new Date();
            dom.clock.innerText = now.toISOString().split('T')[1].split('.')[0] + " UTC";

            const h = now.getUTCHours();
            const targetH = h < 8 ? 8 : h < 16 ? 16 : 24;
            const target = new Date(now);
            target.setUTCHours(targetH, 0, 0, 0);
            
            const diff = target - now;
            const hh = Math.floor(diff / 3600000).toString().padStart(2, '0');
            const mm = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
            const ss = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
            
            dom.timer.innerText = `${hh}:${mm}:${ss}`;
        }

        // CORE RENDER
        async function render() {
            try {
                const res = await fetch('/api/data');
                const data = await res.json();
                
                if (!data.metadata) return;

                const meta = data.metadata;
                const opps = data.opportunities;

                // Stats
                dom.stats.count.innerText = meta.count;
                dom.stats.dom.innerText = meta.top_short_exchange;
                dom.stats.pairs.innerText = meta.total_pairs_scanned.toLocaleString(); // Updated Pairs
                
                if (opps.length > 0) {
                    dom.stats.rate.innerText = fmtPct(opps[0].funding_rate);
                }

                // Table
                const filter = dom.search.value.toUpperCase();
                const filtered = opps.filter(o => o.symbol.includes(filter));

                let html = '';
                filtered.forEach((o, i) => {
                    let rankClass = "text-gray-600";
                    let rowClass = "hover:bg-white/5 transition-colors";
                    
                    if (i === 0) rankClass = "text-success font-bold";
                    if (i < 3) rowClass += " bg-gradient-to-r from-white/[0.02] to-transparent";

                    html += `
                    <div class="grid grid-cols-12 px-6 py-2.5 items-center border-b border-white/5 ${rowClass} group">
                        <div class="col-span-1 font-mono text-[10px] ${rankClass}">${i+1}</div>
                        
                        <div class="col-span-3 flex items-center gap-2">
                            <div class="w-1 h-1 rounded-full ${i < 3 ? 'bg-success shadow-[0_0_5px_#00f0ff]' : 'bg-gray-700'}"></div>
                            <span class="font-medium text-xs text-gray-200 group-hover:text-white">${o.symbol}</span>
                        </div>
                        
                        <div class="col-span-2 text-right">
                            <span class="font-mono text-xs text-white font-medium">${fmtPct(o.funding_rate)}</span>
                        </div>
                        
                        <div class="col-span-2 text-right">
                            <span class="font-mono text-xs text-gray-400">${fmtApr(o.apr)}</span>
                        </div>
                        
                        <div class="col-span-2 text-center">
                            <span class="px-1.5 py-0.5 rounded text-[8px] font-bold uppercase bg-white/5 text-gray-400 border border-white/10 group-hover:border-accent/30 group-hover:text-accent transition-all">
                                ${o.exchange}
                            </span>
                        </div>
                        
                        <div class="col-span-2 text-right font-mono text-[10px] text-gray-500">
                            ${o.price}
                        </div>
                    </div>
                    `;
                });

                if (html === '') html = '<div class="h-full flex items-center justify-center text-[10px] text-gray-600 font-mono tracking-widest">NO ASSETS DETECTED</div>';
                dom.list.innerHTML = html;

                // Chart Update
                if (chartInstance && filtered.length > 0) {
                    const top = filtered.slice(0, 15);
                    chartInstance.data.labels = top.map(o => o.symbol);
                    chartInstance.data.datasets[0].data = top.map(o => o.funding_rate);
                    chartInstance.update('none');
                }

                // Top 5 Log Update
                const top5 = opps.slice(0, 5);
                let logHtml = '';
                if (top5.length > 0) {
                    top5.forEach((o, i) => {
                        logHtml += `
                        <div class="flex justify-between items-center p-2.5 rounded-lg bg-white/5 border border-white/5 group hover:border-accent/30 transition-all">
                            <div class="flex items-center gap-3">
                                <div class="flex items-center justify-center w-5 h-5 rounded bg-void border border-white/10 text-[9px] font-mono text-accent font-bold">
                                    ${i+1}
                                </div>
                                <span class="text-xs text-gray-200 font-medium">${o.symbol}</span>
                            </div>
                            <div class="text-right">
                                <div class="text-xs text-success font-mono font-bold">${fmtPct(o.funding_rate)}</div>
                                <div class="text-[8px] text-gray-500 uppercase tracking-wide">${o.exchange}</div>
                            </div>
                        </div>
                        `;
                    });
                } else {
                    logHtml = '<div class="text-center py-4 text-[10px] text-gray-600">Scan pending...</div>';
                }
                dom.topList.innerHTML = logHtml;

            } catch (e) {
                console.error(e);
            }
        }

        // START
        initChart();
        setInterval(updateTime, 1000);
        setInterval(render, 2000);
        render();

    </script>
</body>
</html>
"""
