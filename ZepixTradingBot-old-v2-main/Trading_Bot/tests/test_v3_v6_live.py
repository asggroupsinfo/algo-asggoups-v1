"""
Comprehensive Test: V3 + V6 LIVE Mode + Re-entry Systems
Tests all plugins active together without conflicts
"""
import sys
sys.path.insert(0, '.')

from src.config import Config
from src.core.plugin_system.plugin_registry import PluginRegistry

def test_all_plugins_live():
    """Test that V3 and all V6 plugins are in LIVE mode"""
    
    print("\n" + "=" * 70)
    print("TESTING V3 + V6 PLUGINS - ALL LIVE MODE")
    print("=" * 70)
    
    config = Config()
    
    # Check plugin configurations
    plugins_config = config.get('plugins', {})
    
    print("\n🔍 PLUGIN STATUS CHECK:")
    print("-" * 70)
    
    results = {
        'v3_live': False,
        'v6_1m_live': False,
        'v6_5m_live': False,
        'v6_15m_live': False,
        'v6_1h_live': False
    }
    
    # Check V3
    v3_config = plugins_config.get('v3_combined', {})
    if v3_config.get('enabled') and not v3_config.get('shadow_mode'):
        print("✅ V3 Combined Logic: 🟢 LIVE MODE")
        results['v3_live'] = True
    else:
        print("❌ V3 Combined Logic: 🟡 SHADOW MODE or DISABLED")
    
    # Check V6 1m
    v6_1m_config = plugins_config.get('v6_price_action_1m', {})
    if v6_1m_config.get('enabled') and not v6_1m_config.get('shadow_mode'):
        print("✅ V6 Price Action 1m: 🟢 LIVE MODE")
        results['v6_1m_live'] = True
    else:
        print("❌ V6 Price Action 1m: 🟡 SHADOW MODE or DISABLED")
    
    # Check V6 5m
    v6_5m_config = plugins_config.get('v6_price_action_5m', {})
    if v6_5m_config.get('enabled') and not v6_5m_config.get('shadow_mode'):
        print("✅ V6 Price Action 5m: 🟢 LIVE MODE")
        results['v6_5m_live'] = True
    else:
        print("❌ V6 Price Action 5m: 🟡 SHADOW MODE or DISABLED")
    
    # Check V6 15m
    v6_15m_config = plugins_config.get('v6_price_action_15m', {})
    if v6_15m_config.get('enabled') and not v6_15m_config.get('shadow_mode'):
        print("✅ V6 Price Action 15m: 🟢 LIVE MODE")
        results['v6_15m_live'] = True
    else:
        print("❌ V6 Price Action 15m: 🟡 SHADOW MODE or DISABLED")
    
    # Check V6 1h
    v6_1h_config = plugins_config.get('v6_price_action_1h', {})
    if v6_1h_config.get('enabled') and not v6_1h_config.get('shadow_mode'):
        print("✅ V6 Price Action 1h: 🟢 LIVE MODE")
        results['v6_1h_live'] = True
    else:
        print("❌ V6 Price Action 1h: 🟡 SHADOW MODE or DISABLED")
    
    # Load plugin registry
    print("\n🔧 LOADING PLUGIN REGISTRY:")
    print("-" * 70)
    
    try:
        registry = PluginRegistry(config)
        registry.auto_load_plugins()
        loaded_plugins = registry.get_all_plugins()
        
        print(f"✅ Plugin Registry Loaded: {len(loaded_plugins)} plugins")
        
        for name, plugin_data in loaded_plugins.items():
            mode = "🟢 LIVE" if plugin_data['mode'] == 'live' else "🟡 SHADOW"
            priority = plugin_data.get('priority', 'N/A')
            print(f"   {mode} {name} (Priority: {priority})")
        
    except Exception as e:
        print(f"❌ Plugin Registry Error: {e}")
        return False
    
    # Check for conflicts
    print("\n⚙️  CHECKING FOR CONFLICTS:")
    print("-" * 70)
    
    # Both V3 and V6 should be able to coexist
    v3_plugins = [p for p in loaded_plugins.keys() if 'v3' in p]
    v6_plugins = [p for p in loaded_plugins.keys() if 'v6' in p]
    
    print(f"V3 Plugins: {len(v3_plugins)}")
    print(f"V6 Plugins: {len(v6_plugins)}")
    
    if len(v3_plugins) > 0 and len(v6_plugins) > 0:
        print("✅ V3 and V6 can coexist - no structural conflicts")
    
    # Check plugin delegation
    plugin_system = config.get('plugin_system', {})
    if plugin_system.get('use_delegation'):
        print("✅ Plugin delegation enabled - plugins work independently")
    else:
        print("⚠️  Plugin delegation disabled - may have conflicts")
    
    # Check re-entry configuration
    print("\n🔄 RE-ENTRY SYSTEM CONFIGURATION:")
    print("-" * 70)
    
    re_entry = config.get('re_entry_config', {})
    autonomous = re_entry.get('autonomous_config', {})
    
    print(f"SL Hunt Re-entry: {'✅ Enabled' if re_entry.get('sl_hunt_reentry_enabled') else '❌ Disabled'}")
    print(f"TP Re-entry: {'✅ Enabled' if re_entry.get('tp_reentry_enabled') else '❌ Disabled'}")
    print(f"Autonomous Mode: {'✅ Enabled' if re_entry.get('autonomous_enabled') else '❌ Disabled'}")
    print(f"Max Chain Levels: {re_entry.get('max_chain_levels', 'Not set')}")
    print(f"SL Reduction per Level: {re_entry.get('sl_reduction_per_level', 'Not set') * 100}%")
    
    # Check autonomous components
    if autonomous:
        sl_hunt = autonomous.get('sl_hunt_recovery', {})
        tp_cont = autonomous.get('tp_continuation', {})
        profit_sl = autonomous.get('profit_sl_hunt', {})
        
        print(f"\nAutonomous Components:")
        print(f"  SL Hunt Recovery: {'✅' if sl_hunt.get('enabled') else '❌'}")
        print(f"  TP Continuation: {'✅' if tp_cont.get('enabled') else '❌'}")
        print(f"  Profit SL Hunt: {'✅' if profit_sl.get('enabled') else '❌'}")
    
    # Check price monitoring
    print("\n📊 PRICE MONITORING:")
    print("-" * 70)
    
    recovery_monitoring = re_entry.get('recovery_monitoring', {})
    print(f"Price Monitor Enabled: {'✅' if recovery_monitoring.get('enabled') else '❌'}")
    print(f"Check Interval: {recovery_monitoring.get('check_interval_seconds', 'Not set')} seconds")
    print(f"Min SL Distance: {recovery_monitoring.get('min_sl_pips', 'Not set')} pips")
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    live_count = sum(results.values())
    total_plugins = len(results)
    
    print(f"\n✅ Live Plugins: {live_count}/{total_plugins}")
    print(f"✅ Total Plugins Loaded: {len(loaded_plugins)}")
    print(f"✅ V3 + V6 Active Together: {len(v3_plugins) > 0 and len(v6_plugins) > 0}")
    print(f"✅ Plugin Delegation: {plugin_system.get('use_delegation')}")
    print(f"✅ Re-entry System: {re_entry.get('autonomous_enabled')}")
    print(f"✅ Price Monitoring: {recovery_monitoring.get('enabled')}")
    
    if live_count == total_plugins:
        print("\n🎉 ALL PLUGINS ARE LIVE! READY FOR FULL TESTING!")
        return True
    else:
        print(f"\n⚠️  {total_plugins - live_count} plugin(s) not in LIVE mode")
        return False

if __name__ == "__main__":
    success = test_all_plugins_live()
    sys.exit(0 if success else 1)
