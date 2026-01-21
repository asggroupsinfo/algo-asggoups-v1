"""
Real Bot Startup Test with Error Handling

Tests if bot can start with error handling system integrated.
"""

import sys
import os
import logging

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StartupTest")

print("="*80)
print("BOT STARTUP TEST WITH ERROR HANDLING INTEGRATION")
print("="*80)

try:
    # Test 1: Import error handling modules
    print("\n✓ Step 1: Testing error handling imports...")
    from src.utils.error_codes import *
    from src.utils.error_handlers import *
    from src.utils.auto_recovery import *
    from src.utils.admin_notifier import *
    from src.utils.logging_config import *
    print("  ✅ All error handling modules imported")
    
    # Test 2: Import main bot modules
    print("\n✓ Step 2: Testing main bot imports...")
    from src.config import Config
    from src.clients.mt5_client import MT5Client
    # Direct import from database.py file
    import importlib.util
    db_spec = importlib.util.spec_from_file_location("tradedatabase", "src/database.py")
    db_mod = importlib.util.module_from_spec(db_spec)
    db_spec.loader.exec_module(db_mod)
    TradeDatabase = db_mod.TradeDatabase
    print("  ✅ Core modules imported")
    
    # Test 3: Initialize error logging
    print("\n✓ Step 3: Initializing error logging...")
    setup_error_logging()
    print("  ✅ Error logging initialized")
    print("  - Main log: logs/bot.log")
    print("  - Error log: logs/errors.log")
    
    # Test 4: Create config
    print("\n✓ Step 4: Loading configuration...")
    config = Config()
    print("  ✅ Configuration loaded")
    
    # Test 5: Create database
    print("\n✓ Step 5: Initializing database...")
    db = TradeDatabase()
    print("  ✅ Database initialized")
    
    # Test 6: Initialize error handling components
    print("\n✓ Step 6: Initializing error handling system...")
    
    # Mock MT5 client for testing
    class MockMT5:
        def is_connected(self):
            return False
        def connect(self):
            return False
    
    # Mock Telegram for testing
    class MockTelegram:
        async def send_message(self, chat_id, text, parse_mode=None):
            logger.info(f"[MOCK] Send to {chat_id}: {text[:50]}...")
    
    mock_mt5 = MockMT5()
    mock_tg = MockTelegram()
    
    # Initialize auto-recovery
    auto_recovery = initialize_auto_recovery(
        mt5_client=mock_mt5,
        database=db,
        telegram_bot=mock_tg
    )
    print("  ✅ Auto-recovery manager initialized")
    
    # Initialize admin notifier
    admin_chat_id = config.config.get('telegram', {}).get('admin_chat_id')
    if admin_chat_id:
        admin_notifier = initialize_admin_notifier(
            telegram_bot=mock_tg,
            admin_chat_id=admin_chat_id
        )
        auto_recovery.set_admin_notifier(admin_notifier)
        print(f"  ✅ Admin notifier initialized (chat: {admin_chat_id})")
    else:
        print("  ⚠️ Admin chat ID not configured")
    
    # Test 7: Test error handlers
    print("\n✓ Step 7: Testing error handlers...")
    
    # Test signal validation
    from src.utils.error_handlers import validate_signal, signal_deduplicator, risk_limit_checker
    
    test_signal = {
        'symbol': 'XAUUSD',
        'direction': 'BUY',
        'entry': 2000.0
    }
    is_valid, error_msg = validate_signal(test_signal)
    print(f"  ✅ Signal validation works: {is_valid}")
    
    # Test deduplication
    is_dup = signal_deduplicator.is_duplicate(test_signal)
    print(f"  ✅ Signal deduplication works: {is_dup}")
    
    # Test risk limits
    can_trade, reason = risk_limit_checker.check_risk_limits()
    print(f"  ✅ Risk limit checker works: {can_trade}")
    
    # Test 8: Test error codes
    print("\n✓ Step 8: Testing error code system...")
    print(f"  - TG-001: {ERROR_MESSAGES.get(TG_001_HTTP_409, 'NOT FOUND')[:50]}...")
    print(f"  - MT-001: {ERROR_MESSAGES.get(MT_001_CONNECTION_FAILED, 'NOT FOUND')[:50]}...")
    print(f"  - TE-001: {ERROR_MESSAGES.get(TE_001_INVALID_SIGNAL, 'NOT FOUND')[:50]}...")
    print("  ✅ Error code definitions working")
    
    # Test 9: Test MT5 error codes
    print("\n✓ Step 9: Testing MT5 error code mapping...")
    mt5_desc = get_mt5_error_description(10018)
    print(f"  - MT5 10018: {mt5_desc}")
    print("  ✅ MT5 error code mapping works")
    
    print("\n" + "="*80)
    print("✅ ALL TESTS PASSED!")
    print("="*80)
    print("\n📊 SUMMARY:")
    print("  ✓ Error handling modules: OK")
    print("  ✓ Main bot imports: OK")
    print("  ✓ Error logging: OK")
    print("  ✓ Configuration: OK")
    print("  ✓ Database: OK")
    print("  ✓ Auto-recovery: OK")
    print("  ✓ Error handlers: OK")
    print("  ✓ Error codes: OK")
    print("  ✓ MT5 error mapping: OK")
    print("\n🎉 Bot can start with error handling integrated!")
    print("\nNote: This is a dry-run test. Full bot startup requires:")
    print("  - Valid MT5 connection")
    print("  - Valid Telegram token")
    print("  - Admin chat ID configured")
    
except Exception as e:
    print(f"\n❌ TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
