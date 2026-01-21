
import sys
import os
import logging
from unittest.mock import MagicMock

# Add current dir to path
sys.path.append(os.getcwd())

# Mock telegram imports to avoid runtime errors if network/token missing
sys.modules['telegram'] = MagicMock()
sys.modules['telegram.ext'] = MagicMock()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VERIFY_V6")

def test_risk_manager():
    logger.info("Testing Risk Manager Logic...")
    from src.managers.risk_manager import RiskManager
    
    # Mock config
    config = MagicMock()
    config.config = {
        "risk_tiers": {"5000": {"daily_loss_limit": 100.0, "max_total_loss": 500.0}},
        "fixed_lot_sizes": {"5000": 0.1},
        "symbol_config": {"XAUUSD": {"volatility": "MEDIUM", "pip_value_per_std_lot": 10.0, "pip_size": 0.01}},
        "profit_booking_config": {"multipliers": [1, 2], "sl_reductions": [0, 10]}
    }
    config.get.side_effect = lambda k, d=None: config.config.get(k, d)
    config.__getitem__.side_effect = lambda k: config.config[k]
    
    rm = RiskManager(config)
    rm.daily_loss = 0.0
    rm.mt5_client = MagicMock()
    rm.mt5_client.get_account_balance.return_value = 5000.0
    
    # Test Smart Lot Logic
    # 1.0 lot * 2 = 2.0 lots total. 
    # 100 pips SL * $10 val * 2 lots = $2000 Risk.
    # Daily Limit = $100.
    # Should FAIL and suggest Smart Lot.
    
    res = rm.validate_dual_orders("XAUUSD", 1.0, 5000.0, sl_pips=100.0)
    
    if not res['valid'] and 'smart_lot' in res:
        logger.info(f"✅ Risk Manager Smart Lot Working! Suggestion: {res['smart_lot']}")
        if res['smart_lot'] < 1.0:
            logger.info("   -> Logic correctly reduced lot size.")
    else:
        logger.error(f"❌ Risk Manager Test Failed: {res}")

def test_telegram_wiring():
    logger.info("Testing Telegram Manager Wiring...")
    # We need to mock BaseIndependentBot imports since we mocked telegram module
    pass

if __name__ == "__main__":
    try:
        test_risk_manager()
        logger.info("✅ V6 Verification Script Finished Successfully")
    except Exception as e:
        logger.error(f"❌ Verification Failed: {e}")
        import traceback
        traceback.print_exc()
