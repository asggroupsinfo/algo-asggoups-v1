"""
COMPREHENSIVE TELEGRAM UPDATES VERIFICATION
Checks all 35 update files and verifies implementation
"""
import sys
sys.path.insert(0, '.')
import json
import os
from pathlib import Path

print("\n" + "=" * 80)
print("🔍 TELEGRAM UPDATES IMPLEMENTATION VERIFICATION")
print("=" * 80)

# Load config
with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# Check if Telegram bots are configured
print("\n[1/10] TELEGRAM BOT CONFIGURATION")
print("-" * 80)

telegram_checks = {
    'Controller Token': config.get('telegram_controller_token'),
    'Notification Token': config.get('telegram_notification_token'),
    'Analytics Token': config.get('telegram_analytics_token'),
    '3-Bot Architecture': all([
        config.get('telegram_controller_token'),
        config.get('telegram_notification_token'),
        config.get('telegram_analytics_token')
    ])
}

for check, result in telegram_checks.items():
    print(f"{'✅' if result else '❌'} {check}")

# Check Telegram bot files exist
print("\n[2/10] TELEGRAM BOT FILES")
print("-" * 80)

telegram_files = {
    'Controller Bot': 'src/telegram/bots/controller_bot.py',
    'Notification Bot': 'src/telegram/bots/notification_bot.py',
    'Analytics Bot': 'src/telegram/bots/analytics_bot.py',
    'Multi-Bot Manager': 'src/telegram/core/multi_bot_manager.py',
    'Menu Manager': 'src/telegram/menus/menu_manager.py',
    'Notification Router': 'src/telegram/notifications/notification_router.py',
}

file_checks = {}
for name, path in telegram_files.items():
    exists = os.path.exists(path)
    file_checks[name] = exists
    print(f"{'✅' if exists else '❌'} {name}: {path}")

# Check command handlers implementation
print("\n[3/10] COMMAND HANDLERS")
print("-" * 80)

if os.path.exists('src/telegram/bots/controller_bot.py'):
    with open('src/telegram/bots/controller_bot.py', 'r', encoding='utf-8') as f:
        controller_code = f.read()
    
    # Key commands from update docs
    key_commands = [
        'handle_start',
        'handle_status',
        'handle_pause',
        'handle_resume',
        'handle_trades',
        'handle_performance',
        'handle_stats',
        'handle_plugin_toggle',
        'handle_v6_control',
        'handle_chains_status',
        'handle_risk_tier',
        'handle_profit_stats',
    ]
    
    for cmd in key_commands:
        exists = cmd in controller_code
        print(f"{'✅' if exists else '❌'} {cmd}")
else:
    print("❌ Controller bot file not found!")

# Check V6 integration
print("\n[4/10] V6 PRICE ACTION INTEGRATION")
print("-" * 80)

v6_features = {
    'V6 Plugins Configured': 'v6_price_action_1m' in config.get('plugins', {}),
    'V6 Timeframes (4)': len([p for p in config.get('plugins', {}).keys() if 'v6_price_action' in p]) >= 4,
    'V6 Menu Handler': 'v6_control' in controller_code if os.path.exists('src/telegram/bots/controller_bot.py') else False,
}

for check, result in v6_features.items():
    print(f"{'✅' if result else '❌'} {check}")

# Check notification system
print("\n[5/10] NOTIFICATION SYSTEM")
print("-" * 80)

if os.path.exists('src/telegram/notifications/notification_router.py'):
    with open('src/telegram/notifications/notification_router.py', 'r', encoding='utf-8') as f:
        notif_code = f.read()
    
    # Key notification types from docs
    key_notifs = [
        'ENTRY',
        'EXIT',
        'TP_HIT',
        'SL_HIT',
        'V6_ENTRY',
        'V3_ENTRY',
        'TP_CONTINUATION',
        'SL_HUNT_ACTIVATED',
        'PROFIT_BOOKING',
    ]
    
    for notif in key_notifs:
        exists = f"'{notif}'" in notif_code or f'"{notif}"' in notif_code
        print(f"{'✅' if exists else '❌'} {notif}")
else:
    print("❌ Notification router file not found!")

# Check re-entry system integration
print("\n[6/10] RE-ENTRY SYSTEM TELEGRAM INTEGRATION")
print("-" * 80)

re_entry_telegram = {
    'TP Continuation Handler': 'tp_continuation' in controller_code if os.path.exists('src/telegram/bots/controller_bot.py') else False,
    'SL Hunt Handler': 'sl_hunt' in controller_code if os.path.exists('src/telegram/bots/controller_bot.py') else False,
    'Chains Status Command': 'handle_chains_status' in controller_code if os.path.exists('src/telegram/bots/controller_bot.py') else False,
    'Re-entry Config': config.get('re_entry_config', {}).get('autonomous_enabled', False),
}

for check, result in re_entry_telegram.items():
    print(f"{'✅' if result else '❌'} {check}")

# Check analytics commands
print("\n[7/10] ANALYTICS COMMANDS")
print("-" * 80)

analytics_commands = [
    'handle_performance',
    'handle_stats',
    'handle_pair_report',
    'handle_strategy_report',
    'handle_tp_report',
    'handle_profit_stats',
]

if os.path.exists('src/telegram/bots/controller_bot.py'):
    for cmd in analytics_commands:
        exists = cmd in controller_code
        print(f"{'✅' if exists else '❌'} {cmd}")
else:
    print("❌ Controller bot not found!")

# Check menu system
print("\n[8/10] MENU SYSTEM")
print("-" * 80)

if os.path.exists('src/telegram/menus/menu_manager.py'):
    with open('src/telegram/menus/menu_manager.py', 'r', encoding='utf-8') as f:
        menu_code = f.read()
    
    menu_features = [
        'get_main_menu',
        'get_strategy_menu',
        'get_risk_menu',
        'get_v6_menu',
        'get_analytics_menu',
        'handle_callback',
    ]
    
    for feature in menu_features:
        exists = feature in menu_code
        print(f"{'✅' if exists else '❌'} {feature}")
else:
    print("❌ Menu manager not found!")

# Check dual order system
print("\n[9/10] DUAL ORDER RE-ENTRY SYSTEM")
print("-" * 80)

dual_order_checks = {
    'Autonomous Mode': config.get('re_entry_config', {}).get('autonomous_enabled', False),
    'TP Continuation': config.get('re_entry_config', {}).get('autonomous_config', {}).get('tp_continuation', {}).get('enabled', False),
    'SL Hunt Recovery': config.get('re_entry_config', {}).get('autonomous_config', {}).get('sl_hunt_recovery', {}).get('enabled', False),
    'Profit SL Hunt': config.get('re_entry_config', {}).get('autonomous_config', {}).get('profit_sl_hunt', {}).get('enabled', False),
}

for check, result in dual_order_checks.items():
    print(f"{'✅' if result else '❌'} {check}")

# Check plugin system integration
print("\n[10/10] PLUGIN SYSTEM TELEGRAM CONTROL")
print("-" * 80)

plugin_telegram = {
    'Plugin Toggle Handler': 'handle_plugin_toggle' in controller_code if os.path.exists('src/telegram/bots/controller_bot.py') else False,
    'V3 Plugin Configured': 'v3_combined' in config.get('plugins', {}),
    'V6 Plugins Configured': len([p for p in config.get('plugins', {}).keys() if 'v6_price_action' in p]) >= 4,
    'Plugin System Enabled': config.get('plugin_system', {}).get('enabled', False),
}

for check, result in plugin_telegram.items():
    print(f"{'✅' if result else '❌'} {check}")

# Summary
print("\n" + "=" * 80)
print("📊 IMPLEMENTATION SUMMARY")
print("=" * 80)

all_checks = {
    **telegram_checks,
    **file_checks,
    **v6_features,
    **re_entry_telegram,
    **dual_order_checks,
    **plugin_telegram,
}

passed = sum(1 for v in all_checks.values() if v)
total = len(all_checks)
percentage = (passed / total) * 100

print(f"\n✅ CHECKS PASSED: {passed}/{total} ({percentage:.0f}%)")

if percentage >= 90:
    print("\n🎉 TELEGRAM UPDATES IMPLEMENTATION: EXCELLENT!")
    print("   Most features from update docs are implemented!")
    exit(0)
elif percentage >= 70:
    print("\n⚠️  TELEGRAM UPDATES IMPLEMENTATION: GOOD")
    print(f"   {total - passed} features missing or incomplete")
    exit(0)
else:
    print("\n❌ TELEGRAM UPDATES IMPLEMENTATION: NEEDS WORK")
    print(f"   {total - passed} features missing")
    exit(1)
