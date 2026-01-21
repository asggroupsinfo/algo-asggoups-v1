"""
Simple Configuration Check - No complex imports
Just reads and displays config correctly
"""
import sys
sys.path.insert(0, '.')
import json

# Read config directly
with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

print("\n" + "=" * 70)
print("COMPLETE BOT CONFIGURATION CHECK")
print("=" * 70)

# Plugins
print("\n[1/5] PLUGIN STATUS")
print("-" * 70)
plugins = config.get('plugins', {})
for name, plugin_config in plugins.items():
    enabled = plugin_config.get('enabled', False)
    shadow = plugin_config.get('shadow_mode', True)
    mode = "🟢 LIVE" if enabled and not shadow else "🟡 SHADOW" if enabled else "❌ DISABLED"
    print(f"{mode} {name}")

# Re-entry Config
print("\n[2/5] RE-ENTRY CONFIGURATION")
print("-" * 70)
re_entry = config.get('re_entry_config', {})
print(f"✅ Max Chain Levels: {re_entry.get('max_chain_levels')}")
print(f"✅ SL Reduction per Level: {re_entry.get('sl_reduction_per_level') * 100}%")
print(f"✅ Recovery Window: {re_entry.get('recovery_window_minutes')} minutes")
print(f"✅ SL Hunt Re-entry: {'ENABLED' if re_entry.get('sl_hunt_reentry_enabled') else 'DISABLED'}")
print(f"✅ TP Re-entry: {'ENABLED' if re_entry.get('tp_reentry_enabled') else 'DISABLED'}")
print(f"✅ Autonomous Mode: {'ENABLED' if re_entry.get('autonomous_enabled') else 'DISABLED'}")
print(f"✅ Price Monitor Interval: {re_entry.get('price_monitor_interval_seconds')} seconds")

# Autonomous Config
print("\n[3/5] AUTONOMOUS RE-ENTRY COMPONENTS")
print("-" * 70)
autonomous = re_entry.get('autonomous_config', {})

sl_hunt = autonomous.get('sl_hunt_recovery', {})
print(f"\n📈 SL Hunt Recovery: {'✅ ENABLED' if sl_hunt.get('enabled') else '❌ DISABLED'}")
if sl_hunt.get('enabled'):
    print(f"   Max Attempts: {sl_hunt.get('max_attempts', 'Not set')}")
    print(f"   Recovery Window: {sl_hunt.get('recovery_window_minutes')} min")
    print(f"   Min Recovery Pips: {sl_hunt.get('min_recovery_pips')}")

tp_cont = autonomous.get('tp_continuation', {})
print(f"\n📊 TP Continuation: {'✅ ENABLED' if tp_cont.get('enabled') else '❌ DISABLED'}")
if tp_cont.get('enabled'):
    print(f"   Max Levels: {tp_cont.get('max_levels')}")
    print(f"   SL Reduction: {tp_cont.get('sl_reduction_per_level') * 100}%")
    print(f"   Trend Confidence: {tp_cont.get('trend_confidence_threshold') * 100}%")

profit_sl = autonomous.get('profit_sl_hunt', {})
print(f"\n💰 Profit SL Hunt: {'✅ ENABLED' if profit_sl.get('enabled') else '❌ DISABLED'}")
if profit_sl.get('enabled'):
    print(f"   Max Attempts: {profit_sl.get('max_attempts_per_order')}")
    print(f"   Recovery Window: {profit_sl.get('recovery_window_minutes')} min")
    print(f"   Stop Chain on Fail: {'YES' if profit_sl.get('stop_chain_on_fail') else 'NO'}")

exit_cont = autonomous.get('exit_continuation', {})
print(f"\n🚪 Exit Continuation: {'✅ ENABLED' if exit_cont.get('enabled') else '❌ DISABLED'}")
if exit_cont.get('enabled'):
    print(f"   Monitor Duration: {exit_cont.get('monitor_duration_seconds')} sec")

# Safety Limits
safety = autonomous.get('safety_limits', {})
print(f"\n🛡️ Safety Limits:")
print(f"   Daily Recovery Attempts: {safety.get('daily_recovery_attempts')}")
print(f"   Daily Recovery Losses: {safety.get('daily_recovery_losses')}")
print(f"   Max Concurrent Recoveries: {safety.get('max_concurrent_recoveries')}")
print(f"   Profit Protection: {safety.get('profit_protection_multiplier')}x")

# Price Monitoring (in re_entry_config root level)
print("\n[4/5] PRICE MONITORING")
print("-" * 70)
# Check both locations for recovery_monitoring
recovery_monitoring = re_entry.get('recovery_monitoring', {})
if not recovery_monitoring:
    # It might be at root level
    recovery_monitoring = config.get('recovery_monitoring', {})

enabled = recovery_monitoring.get('enabled', False)
interval = recovery_monitoring.get('check_interval_seconds', re_entry.get('price_monitor_interval_seconds', 'Not set'))
min_sl = recovery_monitoring.get('min_sl_pips', 'Not set')

print(f"✅ Price Monitor: {'ENABLED' if enabled else 'DISABLED'}")
print(f"✅ Check Interval: {interval} seconds")
print(f"✅ Min SL Distance: {min_sl} pips")

# SL Optimization
print("\n[5/5] SL REDUCTION OPTIMIZATION")
print("-" * 70)
sl_opt = re_entry.get('sl_reduction_optimization', {})
if not sl_opt:
    # Check root level
    sl_opt = config.get('sl_reduction_optimization', {})

opt_enabled = sl_opt.get('enabled', False)
print(f"✅ Optimization: {'ENABLED' if opt_enabled else 'DISABLED'}")
if sl_opt.get('enabled'):
    strategy = sl_opt.get('current_strategy', 'BALANCED')
    print(f"✅ Current Strategy: {strategy}")
    strategies = sl_opt.get('strategies', {})
    if strategy in strategies:
        info = strategies[strategy]
        print(f"   {info.get('emoji')} {info.get('description')}")
        if 'reduction_percent' in info:
            print(f"   Reduction: {info['reduction_percent']}%")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

live_plugins = sum(1 for p in plugins.values() if p.get('enabled') and not p.get('shadow_mode'))
total_plugins = sum(1 for p in plugins.values() if p.get('enabled'))

print(f"\n✅ Plugins Active: {total_plugins}")
print(f"   🟢 LIVE Mode: {live_plugins}")
print(f"   🟡 Shadow Mode: {total_plugins - live_plugins}")

checks = {
    'SL Hunt Recovery': sl_hunt.get('enabled', False),
    'TP Continuation': tp_cont.get('enabled', False),
    'Profit SL Hunt': profit_sl.get('enabled', False),
    'Price Monitor': enabled,
    'SL Optimization': opt_enabled,
    'Autonomous Mode': re_entry.get('autonomous_enabled', False)
}

active = sum(checks.values())
total = len(checks)

print(f"\n✅ Active Systems: {active}/{total}")
for name, status in checks.items():
    icon = "✅" if status else "❌"
    print(f"   {icon} {name}")

if active == total and live_plugins == total_plugins:
    print("\n🎉 ALL SYSTEMS FULLY OPERATIONAL!")
    print("   • All plugins in LIVE mode")
    print("   • All re-entry systems enabled")
    print("   • Price monitoring active")
    print("   • Bot ready for production!")
    exit(0)
else:
    print(f"\n⚠️  {total - active} system(s) not active or {total_plugins - live_plugins} plugin(s) in shadow mode")
    exit(1)
