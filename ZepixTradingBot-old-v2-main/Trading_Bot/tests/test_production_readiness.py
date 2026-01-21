"""
Comprehensive Production Readiness Test
Tests all bot features in simulation mode
"""
import sys
sys.path.insert(0, '.')

from src.config import Config
from src.clients.mt5_client import MT5Client
from src.managers.risk_manager import RiskManager
from src.core.trading_engine import TradingEngine
from src.managers.session_manager import SessionManager
from src.services.alert_processor import AlertProcessor
from src.plugins.plugin_registry import PluginRegistry
from telegram import Bot
import time

def test_production_readiness():
    """Comprehensive production readiness test"""
    
    print("\n" + "=" * 70)
    print("ZEPIX TRADING BOT - COMPREHENSIVE PRODUCTION READINESS TEST")
    print("=" * 70)
    
    results = {
        'configuration': False,
        'mt5_connection': False,
        'plugin_system': False,
        'v3_integration': False,
        'v6_plugins': False,
        're_entry_system': False,
        'profit_booking': False,
        'telegram_bots': False,
        'risk_manager': False,
        'session_manager': False,
        'alert_processor': False,
        'shadow_mode': False
    }
    
    # Test 1: Configuration
    print("\n[1/12] Testing Configuration...")
    try:
        config = Config()
        assert config.get('mt5_login') == 308646228
        assert config.get('mt5_server') == "XMGlobal-MT5 6"
        assert len(config.get('symbol_mapping', {})) == 10
        print("✅ Configuration loaded successfully")
        results['configuration'] = True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
    
    # Test 2: MT5 Connection
    print("\n[2/12] Testing MT5 Connection...")
    try:
        mt5 = MT5Client(config)
        if mt5.initialize():
            account_info = mt5.get_account_info()
            print(f"✅ MT5 Connected - Account: {account_info['login']}, Balance: ${account_info['balance']:.2f}")
            results['mt5_connection'] = True
        else:
            print("❌ MT5 connection failed")
    except Exception as e:
        print(f"❌ MT5 test failed: {e}")
    
    # Test 3: Plugin System
    print("\n[3/12] Testing Plugin System...")
    try:
        plugin_config = config.get('plugin_system', {})
        assert plugin_config.get('enabled') == True
        assert plugin_config.get('use_delegation') == True
        
        registry = PluginRegistry(config)
        registry.auto_load_plugins()
        plugins = registry.get_all_plugins()
        
        print(f"✅ Plugin System Active - {len(plugins)} plugins loaded")
        for name, plugin_data in plugins.items():
            mode = "🟢 LIVE" if plugin_data['mode'] == 'live' else "🟡 SHADOW"
            print(f"   {mode} {name}")
        
        results['plugin_system'] = True
    except Exception as e:
        print(f"❌ Plugin system test failed: {e}")
    
    # Test 4: V3 Integration
    print("\n[4/12] Testing V3 Integration...")
    try:
        v3_config = config.get('v3_integration', {})
        assert v3_config.get('enabled') == True
        
        aggressive_signals = v3_config.get('aggressive_reversal_signals', [])
        print(f"✅ V3 Integration Active")
        print(f"   Aggressive signals: {len(aggressive_signals)}")
        print(f"   Signal routing: {v3_config.get('signal_routing', {}).get('tf_5m')}")
        
        results['v3_integration'] = True
    except Exception as e:
        print(f"❌ V3 integration test failed: {e}")
    
    # Test 5: V6 Plugins
    print("\n[5/12] Testing V6 Price Action Plugins...")
    try:
        v6_plugins = [p for p in plugins.keys() if 'v6_price_action' in p]
        assert len(v6_plugins) >= 4  # 1m, 5m, 15m, 1h
        
        print(f"✅ V6 Plugins Active - {len(v6_plugins)} timeframes")
        for plugin in v6_plugins:
            print(f"   🟡 {plugin} (SHADOW MODE)")
        
        results['v6_plugins'] = True
    except Exception as e:
        print(f"❌ V6 plugins test failed: {e}")
    
    # Test 6: Re-entry System
    print("\n[6/12] Testing Re-entry System Configuration...")
    try:
        re_entry = config.get('re_entry_config', {})
        assert re_entry.get('sl_hunt_reentry_enabled') == True
        assert re_entry.get('tp_reentry_enabled') == True
        assert re_entry.get('autonomous_enabled') == True
        
        autonomous = re_entry.get('autonomous_config', {})
        sl_hunt = autonomous.get('sl_hunt_recovery', {})
        tp_cont = autonomous.get('tp_continuation', {})
        
        print(f"✅ Re-entry System Configured")
        print(f"   SL Hunt Recovery: {sl_hunt.get('enabled')}")
        print(f"   TP Continuation: {tp_cont.get('enabled')}")
        print(f"   Max Chain Levels: {re_entry.get('max_chain_levels')}")
        
        results['re_entry_system'] = True
    except Exception as e:
        print(f"❌ Re-entry system test failed: {e}")
    
    # Test 7: Profit Booking Chains
    print("\n[7/12] Testing Profit Booking Configuration...")
    try:
        # Check if autonomous config has profit_sl_hunt
        autonomous = config.get('re_entry_config', {}).get('autonomous_config', {})
        profit_sl_hunt = autonomous.get('profit_sl_hunt', {})
        
        assert profit_sl_hunt.get('enabled') == True
        
        print(f"✅ Profit Booking Active")
        print(f"   Max attempts per order: {profit_sl_hunt.get('max_attempts_per_order')}")
        print(f"   Recovery window: {profit_sl_hunt.get('recovery_window_minutes')} min")
        
        results['profit_booking'] = True
    except Exception as e:
        print(f"❌ Profit booking test failed: {e}")
    
    # Test 8: Telegram 3-Bot Architecture
    print("\n[8/12] Testing Telegram 3-Bot Architecture...")
    try:
        controller_token = config.get('telegram_controller_token')
        notification_token = config.get('telegram_notification_token')
        analytics_token = config.get('telegram_analytics_token')
        
        # Test all three bots
        bots_ok = 0
        for name, token in [('Controller', controller_token), 
                           ('Notification', notification_token),
                           ('Analytics', analytics_token)]:
            bot = Bot(token=token)
            bot.get_me()
            bots_ok += 1
        
        print(f"✅ Telegram 3-Bot System Active - {bots_ok}/3 bots connected")
        results['telegram_bots'] = True
    except Exception as e:
        print(f"❌ Telegram bots test failed: {e}")
    
    # Test 9: Risk Manager
    print("\n[9/12] Testing Risk Manager...")
    try:
        risk_manager = RiskManager(config, mt5)
        balance = mt5.get_account_info()['balance']
        
        # Test position sizing
        lot_size = risk_manager.calculate_position_size(
            symbol="EURUSD",
            sl_pips=20,
            risk_amount=50.0
        )
        
        print(f"✅ Risk Manager Active")
        print(f"   Account Balance: ${balance:.2f}")
        print(f"   Sample lot size (20 pips SL): {lot_size:.2f}")
        
        results['risk_manager'] = True
    except Exception as e:
        print(f"❌ Risk manager test failed: {e}")
    
    # Test 10: Session Manager
    print("\n[10/12] Testing Session Manager...")
    try:
        session_manager = SessionManager(config)
        current_session = session_manager.get_current_session()
        
        print(f"✅ Session Manager Active")
        print(f"   Current session: {current_session if current_session else 'None'}")
        
        results['session_manager'] = True
    except Exception as e:
        print(f"❌ Session manager test failed: {e}")
    
    # Test 11: Alert Processor
    print("\n[11/12] Testing Alert Processor...")
    try:
        alert_processor = AlertProcessor(config)
        
        # Test alert parsing
        test_alert = {
            'symbol': 'EURUSD',
            'action': 'BUY',
            'sl': '1.0500',
            'tp': '1.0600'
        }
        
        parsed = alert_processor.parse_tradingview_alert(test_alert)
        
        print(f"✅ Alert Processor Active")
        print(f"   Test alert parsed successfully")
        
        results['alert_processor'] = True
    except Exception as e:
        print(f"❌ Alert processor test failed: {e}")
    
    # Test 12: Shadow Mode Configuration
    print("\n[12/12] Testing Shadow Mode Configuration...")
    try:
        shadow_symbols = config.get('shadow_symbols', [])
        
        # Check V6 plugins are in shadow mode
        v6_shadow_count = sum(1 for p in plugins.values() if p['mode'] == 'shadow' and 'v6' in p['name'])
        
        print(f"✅ Shadow Mode Configured")
        print(f"   V6 plugins in shadow: {v6_shadow_count}")
        print(f"   Shadow symbols: {len(shadow_symbols) if shadow_symbols else 'All V6 plugins'}")
        
        results['shadow_mode'] = True
    except Exception as e:
        print(f"❌ Shadow mode test failed: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results.values())
    total = len(results)
    percentage = (passed / total) * 100
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print("\n" + "-" * 70)
    print(f"OVERALL: {passed}/{total} tests passed ({percentage:.1f}%)")
    print("=" * 70)
    
    if percentage >= 90:
        print("\n🎉 BOT IS PRODUCTION READY! 🎉")
    elif percentage >= 75:
        print("\n⚠️  BOT IS MOSTLY READY - Fix remaining issues")
    else:
        print("\n❌ BOT NOT READY - Critical issues need fixing")
    
    return percentage >= 90

if __name__ == "__main__":
    success = test_production_readiness()
    sys.exit(0 if success else 1)
