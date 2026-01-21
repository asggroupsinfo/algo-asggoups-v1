
import pytest
from unittest.mock import MagicMock, patch
from src.managers.risk_manager import RiskManager
from src.telegram.core.multi_bot_manager import MultiBotManager
from src.config import Config

class TestV6Architecture:
    
    @pytest.fixture
    def mock_config(self):
        config = MagicMock(spec=Config)
        config.config = {
            "risk_tiers": {
                "5000": {
                    "daily_loss_limit": 100.0, 
                    "max_total_loss": 500.0
                }
            },
            "fixed_lot_sizes": {"5000": 0.1},
            "symbol_config": {
                "XAUUSD": {
                    "volatility": "MEDIUM",
                    "pip_value_per_std_lot": 10.0,
                    "pip_size": 0.01
                }
            },
            "profit_booking_config": {
                "multipliers": [1, 2],
                "sl_reductions": [0, 10]
            },
            "telegram": {
                "controller_token": "123:test",
                "notification_token": "456:test",
                "analytics_token": "789:test"
            }
        }
        config.get.side_effect = lambda k, default=None: config.config.get(k, default)
        config.__getitem__.side_effect = lambda k: config.config[k]
        return config

    def test_risk_manager_smart_lot_adjustment(self, mock_config):
        """Test that validate_dual_orders adjusts lot size when risk is too high"""
        risk_manager = RiskManager(mock_config)
        risk_manager.daily_loss = 0.0
        risk_manager.mt5_client = MagicMock()
        risk_manager.mt5_client.get_account_balance.return_value = 5000.0
        
        # Scenario: 
        # Daily Limit = $100
        # Trade: 1.0 lots (Total 2.0 lots for dual)
        # SL: 100 pips
        # Pip Value: $10/std lot
        # Expected Loss = 100 pips * $10 * 2.0 lots = $2000
        # This EXCEEDS daily limit of $100 massively.
        
        # Should return valid=False but with smart_lot suggestion
        result = risk_manager.validate_dual_orders(
            symbol="XAUUSD", 
            lot_size=1.0, 
            account_balance=5000.0,
            sl_pips=100.0 # Explicit SL
        )
        
        assert result['valid'] is False
        assert "Risk exceeds daily limit" in result['reason']
        assert 'smart_lot' in result
        
        # Verify smart lot calculation
        # Max Safe Loss = $100 * 0.95 = $95
        # Max Total Lots = $95 / (100 pips * $10) = 0.095 lots
        # Split per order = 0.095 / 2 = 0.0475 -> round to 0.05
        
        expected_lot = round((95.0 / (100.0 * 10.0)) / 2, 2)
        assert result['smart_lot'] == expected_lot

    def test_multi_bot_manager_initialization(self, mock_config):
        """Test that MultiBotManager initializes 3 bots with config"""
        with patch('src.telegram.core.multi_bot_manager.ControllerBot') as MockController, \
             patch('src.telegram.core.multi_bot_manager.NotificationBot') as MockNotification, \
             patch('src.telegram.core.multi_bot_manager.AnalyticsBot') as MockAnalytics:
            
            manager = MultiBotManager(mock_config.config)
            
            assert manager.controller_bot is not None
            assert manager.notification_bot is not None
            assert manager.analytics_bot is not None
            
            MockController.assert_called_once()
