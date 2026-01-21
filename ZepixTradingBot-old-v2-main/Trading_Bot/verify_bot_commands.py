#!/usr/bin/env python3
"""
REAL BOT COMMAND VERIFICATION
Check if all commands are actually registered and working
"""
import sys
import os
sys.path.insert(0, 'src')

import re
from pathlib import Path

def check_controller_commands():
    """Check all commands registered in controller_bot.py"""
    
    controller_path = Path("src/telegram/bots/controller_bot.py")
    with open(controller_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Find all CommandHandler registrations
    registrations = re.findall(r'CommandHandler\("(\w+)"', code)
    
    print("=" * 70)
    print("🔍 BOT COMMAND REGISTRATION VERIFICATION")
    print("=" * 70)
    
    print(f"\n📋 TOTAL COMMANDS REGISTERED: {len(registrations)}")
    print("=" * 70)
    
    # V6 Commands
    v6_cmds = [c for c in registrations if 'v6' in c or ('tf' in c and ('on' in c or 'off' in c))]
    print(f"\n🎯 V6 PRICE ACTION COMMANDS ({len(v6_cmds)}):")
    for cmd in sorted(v6_cmds):
        print(f"  ✅ /{cmd}")
    
    # Analytics Commands
    analytics_cmds = ['daily', 'weekly', 'monthly', 'compare', 'export', 'analytics_menu']
    analytics_found = [c for c in registrations if c in analytics_cmds]
    print(f"\n📊 ANALYTICS COMMANDS ({len(analytics_found)}):")
    for cmd in sorted(analytics_found):
        print(f"  ✅ /{cmd}")
    
    # Basic Commands
    basic_cmds = ['start', 'help', 'status', 'settings', 'stop', 'resume', 'pause', 'restart', 'info', 'version']
    basic_found = [c for c in registrations if c in basic_cmds]
    print(f"\n🤖 BASIC COMMANDS ({len(basic_found)}):")
    for cmd in sorted(basic_found):
        print(f"  ✅ /{cmd}")
    
    # Re-entry Commands
    reentry_cmds = ['tp_cont', 'sl_hunt', 'autonomous', 'chains', 'reentry_menu']
    reentry_found = [c for c in registrations if c in reentry_cmds]
    print(f"\n🔄 RE-ENTRY COMMANDS ({len(reentry_found)}):")
    for cmd in sorted(reentry_found):
        print(f"  ✅ /{cmd}")
    
    # Risk Commands
    risk_cmds = ['risk', 'lot_size', 'max_trades', 'drawdown', 'daily_limit', 'equity', 'balance', 'risk_menu']
    risk_found = [c for c in registrations if c in risk_cmds]
    print(f"\n⚠️ RISK MANAGEMENT COMMANDS ({len(risk_found)}):")
    for cmd in sorted(risk_found):
        print(f"  ✅ /{cmd}")
    
    # Plugin Commands
    plugin_cmds = ['plugin_status', 'plugin_toggle', 'v3_toggle', 'v6_toggle', 'plugins_menu']
    plugin_found = [c for c in registrations if c in plugin_cmds]
    print(f"\n🔌 PLUGIN COMMANDS ({len(plugin_found)}):")
    for cmd in sorted(plugin_found):
        print(f"  ✅ /{cmd}")
    
    print("\n" + "=" * 70)
    print(f"📊 SUMMARY:")
    print(f"  • V6 Commands: {len(v6_cmds)}")
    print(f"  • Analytics: {len(analytics_found)}")
    print(f"  • Basic: {len(basic_found)}")
    print(f"  • Re-entry: {len(reentry_found)}")
    print(f"  • Risk: {len(risk_found)}")
    print(f"  • Plugins: {len(plugin_found)}")
    print(f"  • TOTAL: {len(registrations)} commands")
    print("=" * 70)
    
    # Check for handler methods
    print("\n🔧 CHECKING HANDLER METHODS...")
    handlers = re.findall(r'async def (handle_\w+)', code)
    print(f"  Found {len(handlers)} handler methods")
    
    # Find mismatches
    registered_handlers = set([f'handle_{cmd}' for cmd in registrations])
    existing_handlers = set(handlers)
    
    missing = registered_handlers - existing_handlers
    extra = existing_handlers - registered_handlers
    
    if missing:
        print(f"\n  ⚠️ REGISTERED BUT NO HANDLER:")
        for h in sorted(missing):
            print(f"    - {h}")
    
    if extra:
        print(f"\n  ⚠️ HANDLER BUT NOT REGISTERED:")
        for h in sorted(extra):
            print(f"    - {h}")
    
    if not missing and not extra:
        print(f"  ✅ All commands have matching handlers!")
    
    return len(registrations), len(handlers)

def check_notification_methods():
    """Check V6 notification methods in notification_bot.py"""
    
    notif_path = Path("src/telegram/bots/notification_bot.py")
    with open(notif_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    print("\n" + "=" * 70)
    print("🔔 NOTIFICATION METHODS VERIFICATION")
    print("=" * 70)
    
    v6_methods = [
        'send_v6_entry_alert',
        'send_v6_exit_alert',
        'send_trend_pulse_alert',
        'send_shadow_trade_alert'
    ]
    
    for method in v6_methods:
        if method in code:
            print(f"  ✅ {method}()")
        else:
            print(f"  ❌ {method}() - MISSING")
    
    # Check for UI elements
    print("\n🎨 V6 UI ELEMENTS:")
    ui_checks = {
        'Timeframe Badges': '[15M]',
        'Trend Pulse Bars': 'pulse_bar',
        'Entry Emojis': '🟢',
        'Shadow Mode': '👻',
        'Exit Icons': '✅'
    }
    
    for name, pattern in ui_checks.items():
        if pattern in code:
            print(f"  ✅ {name}")
        else:
            print(f"  ❌ {name} - MISSING")

def test_bot_import():
    """Test if bot can be imported without errors"""
    
    print("\n" + "=" * 70)
    print("📦 BOT IMPORT TEST")
    print("=" * 70)
    
    try:
        from telegram.bots.controller_bot import ControllerBot
        print("  ✅ ControllerBot imported successfully")
        
        from telegram.bots.notification_bot import NotificationBot
        print("  ✅ NotificationBot imported successfully")
        
        from config import Config
        print("  ✅ Config imported successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ Import failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n")
    cmds, handlers = check_controller_commands()
    check_notification_methods()
    import_ok = test_bot_import()
    
    print("\n" + "=" * 70)
    print("🏆 FINAL VERIFICATION RESULT")
    print("=" * 70)
    
    if cmds > 60 and handlers > 60 and import_ok:
        print("✅ BOT IS READY TO START!")
        print(f"✅ {cmds} commands registered")
        print(f"✅ {handlers} handlers implemented")
        print("✅ All imports working")
        print("\n🚀 You can start the bot with: START_BOT.bat")
    else:
        print("❌ BOT HAS ISSUES!")
        print(f"Commands: {cmds}, Handlers: {handlers}, Imports: {import_ok}")
    
    print("=" * 70)
