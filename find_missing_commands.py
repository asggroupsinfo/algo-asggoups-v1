"""
Find Missing Commands - Compare Planning Doc vs Implementation

This script extracts all 144 commands from the planning document and compares
them with the 111 currently implemented commands to identify the 33 missing ones.
"""

import re
from pathlib import Path

# Path to planning document
PLANNING_DOC = Path(r"c:\Users\Ansh Shivaay Gupta\Downloads\ZepixTradingBot-New-v1\ZepixTradingBot-old-v2-main\Updates\V5 COMMAND TELEGRAM\01_MAIN_MENU_CATEGORY_DESIGN.md")

# Implemented commands (from command_registry.py - 111 total)
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

def extract_commands_from_planning_doc():
    """Extract all command names from the planning document."""
    
    # Read the planning document
    with open(PLANNING_DOC, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Category mapping with expected commands based on planning doc
    categories = {
        "SYSTEM": {
            "count": 10,
            "commands": {
                "/start": "Start bot and show main menu",
                "/status": "Show bot status",
                "/pause": "Pause trading",
                "/resume": "Resume trading",
                "/restart": "Restart bot",
                "/shutdown": "Shutdown bot",
                "/help": "Show help menu",
                "/config": "Show configuration",
                "/health": "Show plugin health",
                "/version": "Show plugin versions"
            }
        },
        "TRADING": {
            "count": 18,
            "commands": {
                "/positions": "Show open positions",
                "/pnl": "Show P&L summary",
                "/balance": "Show account balance",
                "/equity": "Show account equity",
                "/margin": "Show margin info",
                "/trades": "Show all trades",
                "/buy": "Place buy order",
                "/sell": "Place sell order",
                "/close": "Close position",
                "/closeall": "Close all positions",
                "/orders": "Show pending orders",
                "/history": "Show trade history",
                "/symbols": "Show available symbols",
                "/price": "Get current price",
                "/spread": "Show spread info",
                "/partial": "Partial close position",
                "/signals": "Show trading signals",
                "/filters": "Signal filters"
            }
        },
        "RISK": {
            "count": 15,
            "commands": {
                "/risk": "Risk settings menu",
                "/setlot": "Set lot size",
                "/setsl": "Set stop loss",
                "/settp": "Set take profit",
                "/dailylimit": "Set daily loss limit",
                "/maxloss": "Set max loss",
                "/maxprofit": "Set max profit target",
                "/risktier": "Set risk tier",
                "/slsystem": "SL system settings",
                "/trailsl": "Trailing SL settings",
                "/breakeven": "Breakeven settings",
                "/protection": "Profit protection",
                "/multiplier": "Lot multiplier settings",
                "/maxtrades": "Max trades limit",
                "/drawdown": "Drawdown limit settings"
            }
        },
        "V3_STRATEGIES": {
            "count": 12,
            "commands": {
                "/logic1": "Control Logic1 (5M strategy)",
                "/logic2": "Control Logic2 (15M strategy)",
                "/logic3": "Control Logic3 (1H strategy)",
                "/v3status": "V3 plugin status",
                "/v3config": "V3 configuration",
                "/v3toggle": "Toggle V3 on/off",
                "/v3allon": "Enable all V3 strategies",
                "/v3alloff": "Disable all V3 strategies",
                "/v3config1": "Configure Logic1",
                "/v3config2": "Configure Logic2",
                "/v3config3": "Configure Logic3",
                "/v3performance": "V3 performance stats"
            }
        },
        "V6_TIMEFRAMES": {
            "count": 30,
            "commands": {
                "/v6status": "V6 plugin status",
                "/v6config": "V6 configuration",
                "/v6control": "V6 control menu",
                "/v6menu": "V6 main menu",
                "/tf1m": "1M timeframe control",
                "/tf5m": "5M timeframe control",
                "/tf15m": "15M timeframe control",
                "/tf30m": "30M timeframe control",
                "/tf1h": "1H timeframe control",
                "/tf4h": "4H timeframe control",
                "/v6allon": "Enable all V6 timeframes",
                "/v6alloff": "Disable all V6 timeframes",
                "/v6performance": "V6 performance stats",
                "/v6compare": "Compare V6 timeframes",
                "/tf1m_on": "Enable 1M timeframe",
                "/tf1m_off": "Disable 1M timeframe",
                "/tf5m_on": "Enable 5M timeframe",
                "/tf5m_off": "Disable 5M timeframe",
                "/tf15m_on": "Enable 15M timeframe",
                "/tf15m_off": "Disable 15M timeframe",
                "/tf30m_on": "Enable 30M timeframe",
                "/tf30m_off": "Disable 30M timeframe",
                "/tf1h_on": "Enable 1H timeframe",
                "/tf1h_off": "Disable 1H timeframe",
                "/tf4h_on": "Enable 4H timeframe",
                "/tf4h_off": "Disable 4H timeframe",
                "/tfconfig15m": "Configure 15M timeframe",
                "/tfconfig30m": "Configure 30M timeframe",
                "/tfconfig1h": "Configure 1H timeframe",
                "/tfconfig4h": "Configure 4H timeframe"
            }
        },
        "ANALYTICS": {
            "count": 15,
            "commands": {
                "/dashboard": "Analytics dashboard",
                "/performance": "Performance report",
                "/daily": "Daily summary",
                "/weekly": "Weekly summary",
                "/monthly": "Monthly summary",
                "/compare": "Compare plugins/timeframes",
                "/export": "Export reports",
                "/pairreport": "Report by trading pair",
                "/strategyreport": "Report by strategy",
                "/tpreport": "TP achievement report",
                "/stats": "Overall statistics",
                "/winrate": "Win rate analysis",
                "/drawdown": "Drawdown analysis",
                "/profitstats": "Profit statistics",
                "/oldperformance": "Historical performance"
            }
        },
        "REENTRY": {
            "count": 15,
            "commands": {
                "/reentry": "Re-entry settings menu",
                "/reconfig": "Re-entry configuration",
                "/slhunt": "SL hunt settings",
                "/slstats": "SL hunt statistics",
                "/tpcontinue": "TP continuation settings",
                "/tpstats": "TP continuation statistics",
                "/recovery": "Recovery settings",
                "/cooldown": "Cooldown settings",
                "/chains": "Active chains",
                "/autonomous": "Autonomous mode",
                "/chainlimit": "Chain limit settings",
                "/v3reconfig": "V3 re-entry config",
                "/v6reconfig": "V6 re-entry config",
                "/slhunt_on": "Enable SL hunt",
                "/slhunt_off": "Disable SL hunt"
            }
        },
        "PROFIT_BOOKING": {
            "count": 8,
            "commands": {
                "/profit": "Profit booking menu",
                "/dualorder": "Dual order system",
                "/orderb": "Order B settings",
                "/profitmenu": "Profit menu",
                "/booking": "Booking settings",
                "/levels": "Profit levels",
                "/partial": "Partial close",
                "/dualstats": "Dual order statistics"
            }
        },
        "PLUGINS": {
            "count": 10,
            "commands": {
                "/plugins": "List all plugins",
                "/plugin": "Plugin control menu",
                "/enable": "Enable plugin",
                "/disable": "Disable plugin",
                "/upgrade": "Upgrade plugin",
                "/rollback": "Rollback plugin",
                "/shadow": "Shadow mode",
                "/toggle": "Toggle plugin",
                "/v3toggle": "Toggle V3 plugin",
                "/v6toggle": "Toggle V6 plugin"
            }
        },
        "SESSIONS": {
            "count": 6,
            "commands": {
                "/session": "Session menu",
                "/london": "London session",
                "/newyork": "New York session",
                "/tokyo": "Tokyo session",
                "/sydney": "Sydney session",
                "/overlap": "Session overlap"
            }
        },
        "VOICE": {
            "count": 7,
            "commands": {
                "/voice": "Voice settings menu",
                "/voicemenu": "Voice configuration menu",
                "/voicetest": "Test voice alert",
                "/mute": "Mute voice alerts",
                "/unmute": "Unmute voice alerts",
                "/notifications": "Notification settings",
                "/clock": "Time/clock display"
            }
        },
        "SETTINGS": {
            "count": 8,
            "commands": {
                "/settings": "General settings",
                "/info": "Bot information",
                "/mode": "Trading mode",
                "/theme": "UI theme",
                "/language": "Language settings",
                "/alerts": "Alert settings",
                "/layout": "Layout settings",
                "/resetall": "Reset all settings"
            }
        }
    }
    
    # Flatten all commands
    all_planned_commands = {}
    for category_name, category_data in categories.items():
        all_planned_commands.update(category_data["commands"])
    
    return categories, all_planned_commands

def find_missing_commands():
    """Find commands that are in planning but not implemented."""
    
    categories, planned_commands = extract_commands_from_planning_doc()
    
    # Find missing commands
    missing = set(planned_commands.keys()) - IMPLEMENTED
    
    # Organize by category
    missing_by_category = {}
    for category_name, category_data in categories.items():
        category_missing = []
        for cmd, desc in category_data["commands"].items():
            if cmd in missing:
                category_missing.append((cmd, desc))
        
        if category_missing:
            missing_by_category[category_name] = {
                "count": len(category_missing),
                "commands": category_missing
            }
    
    return missing_by_category, missing, planned_commands

def print_report():
    """Print detailed missing commands report."""
    
    missing_by_category, all_missing, planned_commands = find_missing_commands()
    
    print("=" * 80)
    print("MISSING COMMANDS ANALYSIS")
    print("=" * 80)
    print(f"\nPlanned Commands: {len(planned_commands)}")
    print(f"Implemented Commands: {len(IMPLEMENTED)}")
    print(f"Missing Commands: {len(all_missing)}")
    print("\n" + "=" * 80)
    
    # Print by category
    for category_name, data in missing_by_category.items():
        print(f"\n{'━' * 80}")
        print(f"{category_name} - Missing: {data['count']} commands")
        print(f"{'━' * 80}")
        for cmd, desc in sorted(data['commands']):
            print(f"  {cmd:25} - {desc}")
    
    print("\n" + "=" * 80)
    print(f"\nTOTAL MISSING: {len(all_missing)} commands")
    print("=" * 80)
    
    # Verify the count
    if len(all_missing) == 33:
        print("\n✅ Exactly 33 missing commands found (as expected)")
    else:
        print(f"\n⚠️ Expected 33 missing commands, but found {len(all_missing)}")
        print(f"   Difference: {33 - len(all_missing)}")
    
    print("\n" + "=" * 80)
    print("MISSING COMMANDS LIST (Alphabetical)")
    print("=" * 80)
    for cmd in sorted(all_missing):
        desc = planned_commands.get(cmd, "No description")
        print(f"{cmd:25} - {desc}")

if __name__ == "__main__":
    print_report()
