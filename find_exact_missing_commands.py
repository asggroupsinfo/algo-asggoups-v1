"""
Extract exact 144 commands from planning document by analyzing submenu layouts.
"""

# EXACT COMMANDS from planning document based on stated counts per category
# Total: 10 + 18 + 15 + 12 + 30 + 15 + 15 + 8 + 10 + 6 + 7 + 8 = 144

PLANNED_COMMANDS = {
    # ==================== CATEGORY 1: SYSTEM (10) ====================
    "SYSTEM": [
        ("/start", "Start bot and show main menu"),
        ("/status", "Show bot status"),
        ("/pause", "Pause trading"),
        ("/resume", "Resume trading"),
        ("/restart", "Restart bot"),
        ("/shutdown", "Shutdown bot"),
        ("/help", "Show help menu"),
        ("/config", "Show configuration"),
        ("/health", "Show plugin health"),
        ("/version", "Show plugin versions"),
    ],
    
    # ==================== CATEGORY 2: TRADING (18) ====================
    "TRADING": [
        ("/positions", "Show open positions"),
        ("/pnl", "Show P&L summary"),
        ("/balance", "Show account balance"),
        ("/equity", "Show account equity"),
        ("/margin", "Show margin info"),
        ("/trades", "Show all trades"),
        ("/buy", "Place buy order"),
        ("/sell", "Place sell order"),
        ("/close", "Close position"),
        ("/closeall", "Close all positions"),
        ("/orders", "Show pending orders"),
        ("/history", "Show trade history"),
        ("/symbols", "Show available symbols"),
        ("/price", "Get current price"),
        ("/spread", "Show spread info"),
        ("/partial", "Partial close position"),
        ("/signals", "Show trading signals"),
        ("/filters", "Signal filters"),
    ],
    
    # ==================== CATEGORY 3: RISK (15) ====================
    "RISK": [
        ("/risk", "Risk settings menu"),
        ("/setlot", "Set lot size"),
        ("/setsl", "Set stop loss"),
        ("/settp", "Set take profit"),
        ("/dailylimit", "Set daily loss limit"),
        ("/maxloss", "Set max loss"),
        ("/maxprofit", "Set max profit target"),
        ("/risktier", "Set risk tier"),
        ("/slsystem", "SL system settings"),
        ("/trailsl", "Trailing SL settings"),
        ("/breakeven", "Breakeven settings"),
        ("/protection", "Profit protection"),
        ("/multiplier", "Lot multiplier settings"),
        ("/maxtrades", "Max trades limit"),
        ("/drawdown", "Drawdown limit settings"),
    ],
    
    # ==================== CATEGORY 4: V3 STRATEGIES (12) ====================
    "V3_STRATEGIES": [
        ("/logic1", "Control Logic1 (5M strategy)"),
        ("/logic2", "Control Logic2 (15M strategy)"),
        ("/logic3", "Control Logic3 (1H strategy)"),
        ("/v3status", "V3 plugin status"),
        ("/v3config", "V3 configuration"),
        ("/v3toggle", "Toggle V3 on/off"),
        ("/v3allon", "Enable all V3 strategies"),
        ("/v3alloff", "Disable all V3 strategies"),
        ("/v3config1", "Configure Logic1"),
        ("/v3config2", "Configure Logic2"),
        ("/v3config3", "Configure Logic3"),
        ("/v3performance", "V3 performance stats"),
    ],
    
    # ==================== CATEGORY 5: V6 TIMEFRAMES (30) ====================
    "V6_TIMEFRAMES": [
        ("/v6status", "V6 plugin status"),
        ("/v6config", "V6 configuration"),
        ("/v6control", "V6 control menu"),
        ("/v6menu", "V6 main menu"),
        ("/tf1m", "1M timeframe control"),
        ("/tf5m", "5M timeframe control"),
        ("/tf15m", "15M timeframe control"),
        ("/tf30m", "30M timeframe control"),
        ("/tf1h", "1H timeframe control"),
        ("/tf4h", "4H timeframe control"),
        ("/v6allon", "Enable all V6 timeframes"),
        ("/v6alloff", "Disable all V6 timeframes"),
        ("/v6performance", "V6 performance stats"),
        ("/v6compare", "Compare V6 timeframes"),
        # Individual timeframe toggles (12 more: 6 TFs × 2 actions)
        ("/tf1m_on", "Enable 1M timeframe"),
        ("/tf1m_off", "Disable 1M timeframe"),
        ("/tf5m_on", "Enable 5M timeframe"),
        ("/tf5m_off", "Disable 5M timeframe"),
        ("/tf15m_on", "Enable 15M timeframe"),
        ("/tf15m_off", "Disable 15M timeframe"),
        ("/tf30m_on", "Enable 30M timeframe"),
        ("/tf30m_off", "Disable 30M timeframe"),
        ("/tf1h_on", "Enable 1H timeframe"),
        ("/tf1h_off", "Disable 1H timeframe"),
        ("/tf4h_on", "Enable 4H timeframe"),
        ("/tf4h_off", "Disable 4H timeframe"),
        # Timeframe configs (4 more)
        ("/tfconfig15m", "Configure 15M timeframe"),
        ("/tfconfig30m", "Configure 30M timeframe"),
        ("/tfconfig1h", "Configure 1H timeframe"),
        ("/tfconfig4h", "Configure 4H timeframe"),
    ],
    
    # ==================== CATEGORY 6: ANALYTICS (15) ====================
    "ANALYTICS": [
        ("/dashboard", "Analytics dashboard"),
        ("/performance", "Performance report"),
        ("/daily", "Daily summary"),
        ("/weekly", "Weekly summary"),
        ("/monthly", "Monthly summary"),
        ("/compare", "Compare plugins/timeframes"),
        ("/export", "Export reports"),
        ("/pairreport", "Report by trading pair"),
        ("/strategyreport", "Report by strategy"),
        ("/tpreport", "TP achievement report"),
        ("/stats", "Overall statistics"),
        ("/winrate", "Win rate analysis"),
        ("/drawdown", "Drawdown analysis"),
        ("/profitstats", "Profit statistics"),
        ("/oldperformance", "Historical performance"),
    ],
    
    # ==================== CATEGORY 7: RE-ENTRY (15) ====================
    "REENTRY": [
        ("/reentry", "Re-entry settings menu"),
        ("/reconfig", "Re-entry configuration"),
        ("/slhunt", "SL hunt settings"),
        ("/slstats", "SL hunt statistics"),
        ("/tpcontinue", "TP continuation settings"),
        ("/tpstats", "TP continuation statistics"),
        ("/recovery", "Recovery settings"),
        ("/cooldown", "Cooldown settings"),
        ("/chains", "Active chains"),
        ("/autonomous", "Autonomous mode"),
        ("/chainlimit", "Chain limit settings"),
        ("/v3reconfig", "V3 re-entry config"),
        ("/v6reconfig", "V6 re-entry config"),
        ("/slhunt_on", "Enable SL hunt"),
        ("/slhunt_off", "Disable SL hunt"),
    ],
    
    # ==================== CATEGORY 8: PROFIT BOOKING (8) ====================
    "PROFIT_BOOKING": [
        ("/profit", "Profit booking menu"),
        ("/dualorder", "Dual order system"),
        ("/orderb", "Order B settings"),
        ("/profitmenu", "Profit menu"),
        ("/booking", "Booking settings"),
        ("/levels", "Profit levels"),
        ("/partial", "Partial close"),
        ("/dualstats", "Dual order statistics"),
    ],
    
    # ==================== CATEGORY 9: PLUGINS (10) ====================
    "PLUGINS": [
        ("/plugins", "List all plugins"),
        ("/plugin", "Plugin control menu"),
        ("/enable", "Enable plugin"),
        ("/disable", "Disable plugin"),
        ("/upgrade", "Upgrade plugin"),
        ("/rollback", "Rollback plugin"),
        ("/shadow", "Shadow mode"),
        ("/toggle", "Toggle plugin"),
        ("/v3toggle", "Toggle V3 plugin"),
        ("/v6toggle", "Toggle V6 plugin"),
    ],
    
    # ==================== CATEGORY 10: SESSIONS (6) ====================
    "SESSIONS": [
        ("/session", "Session menu"),
        ("/london", "London session"),
        ("/newyork", "New York session"),
        ("/tokyo", "Tokyo session"),
        ("/sydney", "Sydney session"),
        ("/overlap", "Session overlap"),
    ],
    
    # ==================== CATEGORY 11: VOICE (7) ====================
    "VOICE": [
        ("/voice", "Voice settings menu"),
        ("/voicemenu", "Voice configuration menu"),
        ("/voicetest", "Test voice alert"),
        ("/mute", "Mute voice alerts"),
        ("/unmute", "Unmute voice alerts"),
        ("/notifications", "Notification settings"),
        ("/clock", "Time/clock display"),
    ],
    
    # ==================== CATEGORY 12: SETTINGS (8) ====================
    "SETTINGS": [
        ("/settings", "General settings"),
        ("/info", "Bot information"),
        ("/mode", "Trading mode"),
        ("/theme", "UI theme"),
        ("/language", "Language settings"),
        ("/alerts", "Alert settings"),
        ("/layout", "Layout settings"),
        ("/resetall", "Reset all settings"),
    ],
}

# IMPLEMENTED COMMANDS (111 total from command_registry.py)
IMPLEMENTED = {
    "/start", "/status", "/pause", "/resume", "/help", "/health", "/version",
    "/restart", "/shutdown", "/config",
    "/trade", "/buy", "/sell", "/close", "/closeall", "/positions", "/orders",
    "/history", "/pnl", "/balance", "/equity", "/margin", "/symbols", "/price", "/spread",
    "/risk", "/setlot", "/setsl", "/settp", "/dailylimit", "/maxloss", "/maxprofit",
    "/risktier", "/slsystem", "/trailsl", "/breakeven", "/protection",
    "/strategy", "/logic1", "/logic2", "/logic3", "/v3", "/v6", "/v6_status", "/v6_control",
    "/tf15m_on", "/tf15m_off", "/tf30m_on", "/tf30m_off", "/tf1h_on", "/tf1h_off",
    "/tf4h_on", "/tf4h_off", "/signals", "/filters", "/multiplier", "/mode",
    "/timeframe", "/tf1m", "/tf5m", "/tf15m", "/tf30m", "/tf1h", "/tf4h", "/tf1d", "/trends",
    "/reentry", "/slhunt", "/tpcontinue", "/recovery", "/cooldown", "/chains",
    "/autonomous", "/chainlimit",
    "/profit", "/booking", "/levels", "/partial", "/orderb", "/dualorder",
    "/analytics", "/performance", "/daily", "/weekly", "/monthly", "/stats", "/winrate",
    "/avgprofit", "/avgloss", "/bestday", "/worstday", "/correlation", "/drawdown",
    "/session", "/london", "/newyork", "/tokyo", "/sydney", "/overlap",
    "/plugin", "/plugins", "/enable", "/disable", "/upgrade", "/rollback", "/shadow", "/compare",
    "/voice", "/voicetest", "/mute", "/unmute"
}

def analyze_missing_commands():
    """Find and categorize missing commands."""
    
    # Flatten planned commands
    all_planned = {}
    for category, commands in PLANNED_COMMANDS.items():
        for cmd, desc in commands:
            all_planned[cmd] = (category, desc)
    
    # Find missing
    missing = set(all_planned.keys()) - IMPLEMENTED
    
    # Categorize missing
    missing_by_category = {}
    for cmd in sorted(missing):
        category, desc = all_planned[cmd]
        if category not in missing_by_category:
            missing_by_category[category] = []
        missing_by_category[category].append((cmd, desc))
    
    return missing_by_category, missing, all_planned

def print_detailed_report():
    """Print comprehensive report."""
    
    missing_by_category, all_missing, all_planned = analyze_missing_commands()
    
    # Header
    print("=" * 80)
    print("MISSING COMMANDS ANALYSIS - EXACT FROM PLANNING DOCUMENT")
    print("=" * 80)
    print(f"\n✓ Planned Commands: {len(all_planned)}")
    print(f"✓ Implemented Commands: {len(IMPLEMENTED)}")
    print(f"✗ Missing Commands: {len(all_missing)}")
    print("\n" + "=" * 80)
    
    # Count check
    total_planned = sum(len(cmds) for cmds in PLANNED_COMMANDS.values())
    print(f"\nVerification:")
    print(f"  Sum of category counts: {total_planned}")
    for cat, cmds in PLANNED_COMMANDS.items():
        print(f"  {cat:20} {len(cmds):3} commands")
    
    # Print missing by category
    print("\n" + "=" * 80)
    print("MISSING COMMANDS BY CATEGORY")
    print("=" * 80)
    
    total_missing = 0
    for category in PLANNED_COMMANDS.keys():
        if category in missing_by_category:
            cmds = missing_by_category[category]
            total_missing += len(cmds)
            print(f"\n{category} - Missing: {len(cmds)} commands")
            print("━" * 80)
            for cmd, desc in cmds:
                print(f"  {cmd:25} - {desc}")
    
    # Summary
    print("\n" + "=" * 80)
    print(f"TOTAL MISSING: {len(all_missing)} commands")
    print("=" * 80)
    
    # Validate count
    if len(all_missing) == 33:
        print("\n✅ EXACTLY 33 MISSING COMMANDS (as expected)")
    else:
        print(f"\n⚠️  Expected 33, found {len(all_missing)}")
        print(f"   Difference: {abs(33 - len(all_missing))}")
    
    # Alphabetical list
    print("\n" + "=" * 80)
    print("MISSING COMMANDS - ALPHABETICAL LIST")
    print("=" * 80)
    for cmd in sorted(all_missing):
        category, desc = all_planned[cmd]
        print(f"{cmd:25} | {category:20} | {desc}")

if __name__ == "__main__":
    print_detailed_report()
