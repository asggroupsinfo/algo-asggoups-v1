#!/usr/bin/env python3
"""Find missing command"""

from src.telegram.command_registry import CommandRegistry

# Expected 144 commands
expected = [
    "/start", "/status", "/pause", "/resume", "/help", "/health", "/version", "/restart", "/shutdown", "/config",
    "/settings", "/info", "/theme",
    "/trade", "/buy", "/sell", "/close", "/closeall", "/positions", "/orders", "/history", "/balance", 
    "/equity", "/margin", "/floating", "/lot", "/symbol", "/spread", "/trades",
    "/risk", "/sl", "/tp", "/maxloss", "/maxdaily", "/trailing", "/breakeven", "/hedge", "/atr", "/percent", 
    "/drawdownlimit", "/protection", "/maxtrades",
    "/strategy", "/logic1", "/logic2", "/logic3", "/v3", "/v6", "/v6_status", "/v6_control",
    "/v3status", "/v3config", "/v3toggle", "/v3allon", "/v3alloff", "/v3config1", "/v3config2", "/v3config3",
    "/v6menu", "/v6config", "/v6allon", "/v6alloff",
    "/tf1m_on", "/tf1m_off", "/tf5m_on", "/tf5m_off", "/tf15m_on", "/tf15m_off", 
    "/tf30m_on", "/tf30m_off", "/tf1h_on", "/tf1h_off", "/tf4h_on", "/tf4h_off",
    "/signals", "/filters", "/multiplier", "/mode",
    "/timeframe", "/tf1m", "/tf5m", "/tf15m", "/tf30m", "/tf1h", "/tf4h", "/tf1d", "/trends",
    "/tfconfig15m", "/tfconfig30m",
    "/reentry", "/slhunt", "/tpcontinue", "/recovery", "/cooldown", "/chains", "/autonomous", "/chainlimit",
    "/reconfig", "/slstats", "/tpstats",
    "/profit", "/booking", "/levels", "/partial", "/orderb", "/dualorder",
    "/analytics", "/performance", "/daily", "/weekly", "/monthly", "/stats", "/winrate", "/drawdown",
    "/avgprofit", "/avgloss", "/bestday", "/worstday", "/correlation", "/dashboard", "/export", 
    "/pairreport", "/strategyreport", "/tpreport",
    "/session", "/london", "/newyork", "/tokyo", "/sydney", "/overlap",
    "/plugin", "/plugins", "/enable", "/disable", "/upgrade", "/rollback", "/shadow", "/compare",
    "/voice", "/voicetest", "/mute", "/unmute", "/notifications", "/clock"
]

cr = CommandRegistry()
registered = list(cr.COMMANDS.keys())

print(f"✅ Expected: {len(expected)} commands")
print(f"✅ Registered: {len(registered)} commands")
print(f"\nMISSING COMMANDS:")

missing = set(expected) - set(registered)
for cmd in sorted(missing):
    print(f"  ❌ {cmd}")

print(f"\nEXTRA COMMANDS (not in plan):")
extra = set(registered) - set(expected)
for cmd in sorted(extra):
    print(f"  ➕ {cmd}")
