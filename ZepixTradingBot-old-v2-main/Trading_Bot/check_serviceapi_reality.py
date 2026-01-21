"""
ServiceAPI Implementation Reality Check
Check what's implemented vs 11_SERVICEAPI_DOCUMENTATION.md
"""
import sys
import inspect
from typing import Dict, Any, List

print("="*80)
print("SERVICEAPI IMPLEMENTATION REALITY CHECK")
print("Document: 11_SERVICEAPI_DOCUMENTATION.md")
print("="*80)

# Import ServiceAPI
try:
    from src.core.plugin_system.service_api import ServiceAPI, create_service_api
    print("\n✅ ServiceAPI module imported successfully")
except Exception as e:
    print(f"\n❌ Failed to import ServiceAPI: {e}")
    sys.exit(1)

# Expected methods from document (50+ methods documented)
EXPECTED_METHODS = {
    # Initialization (2)
    '__init__': 'Initialize ServiceAPI',
    
    # Service Registration (7)
    'register_service': 'Register a service',
    'get_service': 'Get registered service',
    'has_service': 'Check if service exists',
    'list_services': 'List all services',
    'discover_services': 'Discover service info',
    
    # Market Data (9)
    'get_price': 'Get current price',
    'get_symbol_info': 'Get symbol validation info',
    'get_current_spread': 'Get spread in pips (async)',
    'check_spread_acceptable': 'Check spread limit (async)',
    'get_current_price_data': 'Get comprehensive price data (async)',
    'get_volatility_state': 'Get volatility state (async)',
    'is_market_open': 'Check if market open (async)',
    'get_atr': 'Get ATR value (async)',
    
    # Account Methods (2)
    'get_balance': 'Get account balance',
    'get_equity': 'Get account equity',
    
    # Order Execution (14)
    'place_order': 'Place order (sync)',
    'place_order_async': 'Place order (async)',
    'place_dual_orders_v3': 'V3 dual orders (async)',
    'place_dual_orders_v6': 'V6 dual orders (async)',
    'place_single_order_a': 'Order A only (async)',
    'place_single_order_b': 'Order B only (async)',
    'close_trade': 'Close trade (sync)',
    'close_position': 'Close position with tracking (async)',
    'close_position_partial': 'Close partial position (async)',
    'close_positions': 'Close multiple positions (async)',
    'close_positions_by_direction': 'Close by direction (async)',
    'modify_order': 'Modify order SL/TP (sync)',
    'modify_order_async': 'Modify order (async)',
    'get_open_trades': 'Get all open trades',
    'get_plugin_orders': 'Get plugin orders (async)',
    
    # Risk Management (11)
    'calculate_lot_size': 'Calculate lot size (sync)',
    'calculate_lot_size_async': 'Calculate lot size (async)',
    'calculate_sl_price': 'Calculate SL price (async)',
    'calculate_atr_sl': 'Calculate ATR-based SL (async)',
    'calculate_atr_tp': 'Calculate ATR-based TP (async)',
    'check_daily_limit': 'Check daily loss limit (async)',
    'check_lifetime_limit': 'Check lifetime limit (async)',
    'check_risk_limits': 'Check all risk limits (async)',
    'validate_trade_risk': 'Validate trade risk (async)',
    'get_fixed_lot_size': 'Get fixed lot size (async)',
    'get_spread': 'Get spread (async alias)',
    
    # Trend Management (11)
    'get_timeframe_trend': 'Get V3 4-pillar trend (async)',
    'get_mtf_trends': 'Get all MTF trends (async)',
    'validate_v3_trend_alignment': 'Validate V3 alignment (async)',
    'check_logic_alignment': 'Check logic alignment (async)',
    'update_trend_pulse': 'Update Trend Pulse (async)',
    'get_market_state': 'Get market state (async)',
    'check_pulse_alignment': 'Check pulse alignment (async)',
    'get_pulse_data': 'Get pulse data (async)',
    'check_higher_tf_trend': 'Check higher TF trend (async)',
    'update_trend': 'Update trend (async)',
    
    # Communication (3)
    'send_notification': 'Send Telegram message (sync)',
    'send_notification_async': 'Send message (async)',
    'log': 'Log with plugin context',
    
    # Configuration (2)
    'get_config': 'Get configuration value',
    'get_plugin_config': 'Get plugin config value',
    
    # Service Metrics (4)
    'get_metrics': 'Get all metrics',
    'get_service_metrics': 'Get service metrics',
    'reset_metrics': 'Reset metrics',
    'check_health': 'Health checks (async)',
    'get_service_status': 'Get service status',
}

# Expected properties from document
EXPECTED_PROPERTIES = {
    'plugin_id': 'Plugin identifier',
    'services_available': 'Services available flag',
    'reentry_service': 'Re-entry service',
    'dual_order_service': 'Dual order service',
    'profit_booking_service': 'Profit booking service',
    'autonomous_service': 'Autonomous service',
    'telegram_service': 'Telegram service',
    'database_service': 'Database service',
}

print("\n📊 CHECKING METHODS")
print("-"*80)

# Get all methods from ServiceAPI class
actual_methods = {}
for name, obj in inspect.getmembers(ServiceAPI):
    if callable(obj) and not name.startswith('_'):
        actual_methods[name] = obj

implemented = 0
missing = 0

for method_name, description in EXPECTED_METHODS.items():
    if method_name == '__init__':
        exists = True  # Constructor always exists
    else:
        exists = method_name in actual_methods
    
    status = "✅" if exists else "❌"
    if not exists:
        print(f"{status} {method_name:35s} - {description}")
        missing += 1
    else:
        implemented += 1

print(f"\n📈 Methods Status:")
print(f"   Expected: {len(EXPECTED_METHODS)}")
print(f"   Implemented: {implemented}")
print(f"   Missing: {missing}")

# Check properties
print("\n📊 CHECKING PROPERTIES")
print("-"*80)

prop_implemented = 0
prop_missing = 0

for prop_name, description in EXPECTED_PROPERTIES.items():
    exists = hasattr(ServiceAPI, prop_name)
    status = "✅" if exists else "❌"
    if not exists:
        print(f"{status} {prop_name:35s} - {description}")
        prop_missing += 1
    else:
        prop_implemented += 1

print(f"\n📈 Properties Status:")
print(f"   Expected: {len(EXPECTED_PROPERTIES)}")
print(f"   Implemented: {prop_implemented}")
print(f"   Missing: {prop_missing}")

# Check factory function
print("\n🏭 CHECKING FACTORY FUNCTION")
print("-"*80)

try:
    from src.core.plugin_system.service_api import create_service_api
    print("✅ create_service_api factory function exists")
    factory_exists = True
except ImportError:
    print("❌ create_service_api factory function missing")
    factory_exists = False

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

total_expected = len(EXPECTED_METHODS) + len(EXPECTED_PROPERTIES) + 1  # +1 for factory
total_implemented = implemented + prop_implemented + (1 if factory_exists else 0)
total_missing = missing + prop_missing + (0 if factory_exists else 1)

percentage = (total_implemented / total_expected * 100) if total_expected > 0 else 0

print(f"\n📊 Implementation Status:")
print(f"   Total Expected Items: {total_expected}")
print(f"   Implemented: {total_implemented} ({percentage:.1f}%)")
print(f"   Missing: {total_missing}")

if missing > 0:
    print(f"\n❌ MISSING METHODS ({missing}):")
    for method_name, description in EXPECTED_METHODS.items():
        if method_name != '__init__' and method_name not in actual_methods:
            print(f"   - {method_name}: {description}")

if prop_missing > 0:
    print(f"\n❌ MISSING PROPERTIES ({prop_missing}):")
    for prop_name, description in EXPECTED_PROPERTIES.items():
        if not hasattr(ServiceAPI, prop_name):
            print(f"   - {prop_name}: {description}")

if percentage >= 95:
    print(f"\n✅ EXCELLENT - ServiceAPI is {percentage:.1f}% implemented!")
elif percentage >= 80:
    print(f"\n⚠️ GOOD - ServiceAPI is {percentage:.1f}% implemented, minor gaps")
else:
    print(f"\n❌ NEEDS WORK - ServiceAPI is only {percentage:.1f}% implemented")

print("\n" + "="*80)

sys.exit(0 if missing == 0 and prop_missing == 0 else 1)
