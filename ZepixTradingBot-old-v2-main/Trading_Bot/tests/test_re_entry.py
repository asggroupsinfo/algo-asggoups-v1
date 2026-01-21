"""Test re-entry and profit booking configuration"""
import sys
sys.path.insert(0, '.')

from src.config import Config

# Load configuration
config = Config()

# Check re-entry configuration
re_entry = config.get('re_entry_config', {})
print("=" * 50)
print("RE-ENTRY SYSTEMS CONFIGURATION")
print("=" * 50)
print(f"SL Hunt Re-entry Enabled: {re_entry.get('sl_hunt_reentry_enabled')}")
print(f"TP Re-entry Enabled: {re_entry.get('tp_reentry_enabled')}")
print(f"Max Re-entries: {re_entry.get('max_reentries')}")
print(f"SL Hunt Buffer Pips: {re_entry.get('sl_hunt_buffer_pips')}")
print(f"TP Re-entry Buffer Pips: {re_entry.get('tp_reentry_buffer_pips')}")

# Check profit booking configuration
profit = config.get('profit_booking_config', {})
print("\n" + "=" * 50)
print("PROFIT BOOKING CHAIN CONFIGURATION")
print("=" * 50)
print(f"Enabled: {profit.get('enabled')}")
print(f"Max Chain Length: {profit.get('max_chain_length')}")
print(f"Auto Manage SL: {profit.get('auto_manage_sl')}")
print(f"Booking Percentage: {profit.get('booking_percentage')}")

# Check V3 integration
v3_config = config.get('v3_integration', {})
print("\n" + "=" * 50)
print("V3 INTEGRATION")
print("=" * 50)
print(f"Enabled: {v3_config.get('enabled')}")
print(f"Use Signal Routing: {v3_config.get('use_signal_routing')}")
print(f"Aggressive Reversal Signals: {v3_config.get('aggressive_reversal_signals')}")

# Check plugin system
plugin_config = config.get('plugin_system', {})
print("\n" + "=" * 50)
print("PLUGIN SYSTEM")
print("=" * 50)
print(f"Enabled: {plugin_config.get('enabled')}")
print(f"Use Delegation: {plugin_config.get('use_delegation')}")
print(f"Auto Load Plugins: {plugin_config.get('auto_load_plugins')}")

print("\n" + "=" * 50)
print("✅ Configuration verification complete!")
print("=" * 50)
