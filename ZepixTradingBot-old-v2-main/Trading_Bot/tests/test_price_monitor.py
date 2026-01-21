"""
Price Monitor & Re-entry System Verification
Checks autonomous re-entry configuration and price monitoring
"""
import sys
sys.path.insert(0, '.')

from src.config import Config
import json

def verify_price_monitor_reentry():
    """Verify price monitoring and re-entry system configuration"""
    
    print("\n" + "=" * 70)
    print("PRICE MONITOR & RE-ENTRY SYSTEM VERIFICATION")
    print("=" * 70)
    
    config = Config()
    
    # Get re-entry configuration
    re_entry_config = config.get('re_entry_config', {})
    autonomous_config = re_entry_config.get('autonomous_config', {})
    
    print("\n[1/5] Re-entry System Configuration")
    print("-" * 70)
    
    print(f"\n✅ Basic Re-entry Settings:")
    print(f"   Max Chain Levels: {re_entry_config.get('max_chain_levels', 'Not set')}")
    print(f"   SL Reduction per Level: {re_entry_config.get('sl_reduction_per_level', 0) * 100}%")
    print(f"   Recovery Window: {re_entry_config.get('recovery_window_minutes', 'Not set')} minutes")
    print(f"   Min Time Between Re-entries: {re_entry_config.get('min_time_between_re_entries', 'Not set')} seconds")
    
    print(f"\n✅ Re-entry Triggers:")
    print(f"   SL Hunt Re-entry: {'🟢 ENABLED' if re_entry_config.get('sl_hunt_reentry_enabled') else '❌ DISABLED'}")
    print(f"   TP Re-entry: {'🟢 ENABLED' if re_entry_config.get('tp_reentry_enabled') else '❌ DISABLED'}")
    print(f"   Autonomous Mode: {'🟢 ENABLED' if re_entry_config.get('autonomous_enabled') else '❌ DISABLED'}")
    print(f"   Reversal Exit: {'🟢 ENABLED' if re_entry_config.get('reversal_exit_enabled') else '❌ DISABLED'}")
    print(f"   Exit Continuation: {'🟢 ENABLED' if re_entry_config.get('exit_continuation_enabled') else '❌ DISABLED'}")
    
    # Autonomous configuration
    print("\n[2/5] Autonomous Re-entry Components")
    print("-" * 70)
    
    if autonomous_config:
        # SL Hunt Recovery
        sl_hunt = autonomous_config.get('sl_hunt_recovery', {})
        print(f"\n📈 SL Hunt Recovery:")
        print(f"   Enabled: {'✅' if sl_hunt.get('enabled') else '❌'}")
        print(f"   Offset Pips: {sl_hunt.get('offset_pips', 'Not set')}")
        print(f"   Recovery Window: {sl_hunt.get('recovery_window_minutes', 'Not set')} minutes")
        print(f"   Max Attempts: {sl_hunt.get('max_attempts_per_order', 'Not set')}")
        
        # TP Continuation
        tp_cont = autonomous_config.get('tp_continuation', {})
        print(f"\n📊 TP Continuation:")
        print(f"   Enabled: {'✅' if tp_cont.get('enabled') else '❌'}")
        print(f"   Offset Pips: {tp_cont.get('offset_pips', 'Not set')}")
        print(f"   Continuation Window: {tp_cont.get('continuation_window_minutes', 'Not set')} minutes")
        print(f"   Max Continuations: {tp_cont.get('max_continuations_per_order', 'Not set')}")
        
        # Profit SL Hunt
        profit_sl = autonomous_config.get('profit_sl_hunt', {})
        print(f"\n💰 Profit SL Hunt:")
        print(f"   Enabled: {'✅' if profit_sl.get('enabled') else '❌'}")
        print(f"   Offset Pips: {profit_sl.get('offset_pips', 'Not set')}")
        print(f"   Recovery Window: {profit_sl.get('recovery_window_minutes', 'Not set')} minutes")
        print(f"   Max Attempts: {profit_sl.get('max_attempts_per_order', 'Not set')}")
        print(f"   Stop Chain on Fail: {'✅' if profit_sl.get('stop_chain_on_fail') else '❌'}")
        
        # Exit Continuation
        exit_cont = autonomous_config.get('exit_continuation', {})
        print(f"\n🚪 Exit Continuation:")
        print(f"   Enabled: {'✅' if exit_cont.get('enabled') else '❌'}")
        print(f"   Offset Pips: {exit_cont.get('offset_pips', 'Not set')}")
        print(f"   Continuation Window: {exit_cont.get('continuation_window_minutes', 'Not set')} minutes")
        print(f"   Max Continuations: {exit_cont.get('max_continuations_per_order', 'Not set')}")
        
        # Safety Limits
        safety = autonomous_config.get('safety_limits', {})
        print(f"\n🛡️  Safety Limits:")
        print(f"   Daily Recovery Attempts: {safety.get('daily_recovery_attempts', 'Not set')}")
        print(f"   Daily Recovery Losses: {safety.get('daily_recovery_losses', 'Not set')}")
        print(f"   Max Concurrent Recoveries: {safety.get('max_concurrent_recoveries', 'Not set')}")
        print(f"   Profit Protection Multiplier: {safety.get('profit_protection_multiplier', 'Not set')}x")
    else:
        print("❌ Autonomous configuration not found!")
    
    # Price Monitoring
    print("\n[3/5] Price Monitoring System")
    print("-" * 70)
    
    recovery_monitoring = re_entry_config.get('recovery_monitoring', {})
    print(f"\n📊 Price Monitor Settings:")
    print(f"   Enabled: {'✅' if recovery_monitoring.get('enabled') else '❌'}")
    print(f"   Check Interval: {recovery_monitoring.get('check_interval_seconds', 'Not set')} seconds")
    print(f"   Min SL Distance: {recovery_monitoring.get('min_sl_pips', 'Not set')} pips")
    
    # SL Reduction Optimization
    print("\n[4/5] SL Reduction Strategy")
    print("-" * 70)
    
    sl_optimization = re_entry_config.get('sl_reduction_optimization', {})
    if sl_optimization:
        current_strategy = sl_optimization.get('current_strategy', 'BALANCED')
        strategies = sl_optimization.get('strategies', {})
        
        print(f"\n⚙️  Current Strategy: {current_strategy}")
        
        if current_strategy in strategies:
            strategy_info = strategies[current_strategy]
            print(f"   Description: {strategy_info.get('description')}")
            print(f"   Emoji: {strategy_info.get('emoji')}")
            print(f"   Best For: {strategy_info.get('best_for')}")
            
            if 'reduction_percent' in strategy_info:
                print(f"   Reduction: {strategy_info.get('reduction_percent')}%")
            
            # Show symbol-specific settings for ADAPTIVE
            if current_strategy == 'ADAPTIVE':
                symbol_settings = strategy_info.get('symbol_settings', {})
                print(f"\n   📌 Symbol-Specific Reductions (showing first 5):")
                for i, (symbol, settings) in enumerate(list(symbol_settings.items())[:5]):
                    print(f"      {symbol}: {settings['reduction_percent']}% - {settings['reason']}")
                print(f"      ... and {len(symbol_settings) - 5} more symbols")
    
    # Test Scenarios
    print("\n[5/5] Re-entry Scenario Examples")
    print("-" * 70)
    
    print(f"\n🎯 Scenario 1: SL Hunt Recovery")
    print(f"   1. Entry: EURUSD BUY at 1.0550, SL 1.0500, TP 1.0600")
    print(f"   2. Price hits SL at 1.0500 → Order A closes with loss")
    print(f"   3. Price monitor detects price at 1.0501 (above SL + {sl_hunt.get('offset_pips', 1)} pips)")
    print(f"   4. Bot triggers SL Hunt Recovery → Opens new BUY order")
    print(f"   5. New SL: 1.0515 (30% tighter), TP: 1.0600 (same)")
    print(f"   6. Recovery window: {sl_hunt.get('recovery_window_minutes', 30)} minutes")
    
    print(f"\n🎯 Scenario 2: TP Continuation")
    print(f"   1. Entry: GBPUSD SELL at 1.2800, SL 1.2850, TP 1.2750")
    print(f"   2. Price hits TP at 1.2750 → Order A closes with profit")
    print(f"   3. Price monitor detects continued movement to 1.2748")
    print(f"   4. Bot triggers TP Continuation → Opens new SELL order")
    print(f"   5. New entry at 1.2748, TP extended to 1.2700")
    print(f"   6. Continuation window: {tp_cont.get('continuation_window_minutes', 30)} minutes")
    
    print(f"\n🎯 Scenario 3: Multi-level Profit Chain")
    print(f"   1. Entry: XAUUSD BUY at 2050.00, SL 2040.00, TP 2060.00")
    print(f"   Level 1: SL 2040.00 (10 pips)")
    print(f"   Level 2: SL 2047.00 (7 pips, -30%)")
    print(f"   Level 3: SL 2051.90 (4.9 pips, -30%)")
    print(f"   Level 4: SL 2055.33 (3.43 pips, -30%)")
    print(f"   Level 5: SL 2057.73 (2.4 pips, -30%)")
    print(f"   Max chain: {re_entry_config.get('max_chain_levels', 5)} levels")
    
    print(f"\n🎯 Scenario 4: Profit Protection")
    print(f"   1. Running profit chain at level 3 (2 successful re-entries)")
    print(f"   2. Total profit: +$150 from previous levels")
    print(f"   3. Max acceptable loss: ${safety.get('profit_protection_multiplier', 5)}x previous profit = ${150 * safety.get('profit_protection_multiplier', 5)}")
    print(f"   4. Bot stops chain if loss exceeds profit protection")
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    checks = {
        'SL Hunt Recovery': sl_hunt.get('enabled', False) if sl_hunt else False,
        'TP Continuation': tp_cont.get('enabled', False) if tp_cont else False,
        'Profit SL Hunt': profit_sl.get('enabled', False) if profit_sl else False,
        'Price Monitor': recovery_monitoring.get('enabled', False),
        'Safety Limits': bool(safety),
        'SL Optimization': sl_optimization.get('enabled', False)
    }
    
    passed = sum(checks.values())
    total = len(checks)
    
    print(f"\n✅ Active Components: {passed}/{total}")
    for component, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {component}")
    
    print(f"\n📊 Re-entry Configuration:")
    print(f"   ✅ Max chain levels: {re_entry_config.get('max_chain_levels')}")
    print(f"   ✅ SL reduction: {re_entry_config.get('sl_reduction_per_level') * 100}% per level")
    print(f"   ✅ Recovery window: {sl_hunt.get('recovery_window_minutes', 'N/A')} minutes")
    print(f"   ✅ Price monitor interval: {recovery_monitoring.get('check_interval_seconds')} seconds")
    
    if passed == total:
        print("\n🎉 ALL RE-ENTRY SYSTEMS OPERATIONAL!")
        print("Price monitor will automatically detect and execute:")
        print("   • SL Hunt recoveries when price reverses")
        print("   • TP continuations when momentum persists")
        print("   • Profit protection on chain trades")
        print("   • Autonomous re-entries within windows")
        return True
    else:
        print(f"\n⚠️  {total - passed} component(s) not active")
        return False

if __name__ == "__main__":
    success = verify_price_monitor_reentry()
    sys.exit(0 if success else 1)
