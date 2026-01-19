"""
Tests for Telegram V5 Upgrade

This module provides comprehensive tests for all Telegram V5 Upgrade features:
- V6 Timeframe Control Menu Handler
- Analytics Menu Handler
- Dual Order & Re-entry Menu Handlers
- Menu Manager Integration
- Controller Bot Integration

Version: 1.0.0
Date: 2026-01-19
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Add src to path for imports
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)


class TestV6ControlMenuHandler:
    """Tests for V6 Control Menu Handler (Phase 2)"""
    
    def test_v6_control_menu_handler_init(self):
        """Test V6ControlMenuHandler initialization"""
        from menu.v6_control_menu_handler import V6ControlMenuHandler
        
        mock_bot = Mock()
        mock_bot.config = {"v6_price_action": {"enabled": True, "timeframes": {}}}
        handler = V6ControlMenuHandler(mock_bot)
        
        assert handler.bot == mock_bot
        assert handler.V6_TIMEFRAMES == ["15m", "30m", "1h", "4h"]
    
    def test_v6_control_menu_handler_has_required_methods(self):
        """Test V6ControlMenuHandler has all required methods"""
        from menu.v6_control_menu_handler import V6ControlMenuHandler
        
        mock_bot = Mock()
        handler = V6ControlMenuHandler(mock_bot)
        
        # Check required methods exist
        assert hasattr(handler, 'show_v6_main_menu')
        assert hasattr(handler, 'handle_toggle_system')
        assert hasattr(handler, 'handle_toggle_timeframe')
        assert hasattr(handler, 'handle_enable_all')
        assert hasattr(handler, 'handle_disable_all')
        assert hasattr(handler, 'show_v6_stats_menu')
        assert hasattr(handler, 'show_v6_configure_menu')
        assert hasattr(handler, 'handle_callback')
    
    def test_v6_control_menu_handler_callback_returns_false_for_invalid(self):
        """Test V6ControlMenuHandler callback handling returns False for invalid callbacks"""
        from menu.v6_control_menu_handler import V6ControlMenuHandler
        
        mock_bot = Mock()
        mock_bot.config = {"v6_price_action": {"enabled": True, "timeframes": {}}}
        handler = V6ControlMenuHandler(mock_bot)
        
        # Test callback handling returns False for invalid callbacks
        assert handler.handle_callback("invalid_callback", 123, 456) == False


class TestAnalyticsMenuHandler:
    """Tests for Analytics Menu Handler (Phase 4)"""
    
    def test_analytics_menu_handler_init(self):
        """Test AnalyticsMenuHandler initialization"""
        from menu.analytics_menu_handler import AnalyticsMenuHandler
        
        mock_bot = Mock()
        handler = AnalyticsMenuHandler(mock_bot)
        
        assert handler._bot == mock_bot
    
    def test_analytics_menu_handler_has_required_methods(self):
        """Test AnalyticsMenuHandler has all required methods"""
        from menu.analytics_menu_handler import AnalyticsMenuHandler
        
        mock_bot = Mock()
        handler = AnalyticsMenuHandler(mock_bot)
        
        # Check required methods exist
        assert hasattr(handler, 'show_analytics_menu')
        assert hasattr(handler, 'show_daily_analytics')
        assert hasattr(handler, 'show_weekly_analytics')
        assert hasattr(handler, 'show_monthly_analytics')
        assert hasattr(handler, 'show_analytics_by_pair')
        assert hasattr(handler, 'show_analytics_by_logic')
        assert hasattr(handler, 'export_analytics')
        assert hasattr(handler, 'handle_callback')
    
    def test_analytics_menu_handler_callback_returns_false_for_invalid(self):
        """Test AnalyticsMenuHandler callback handling returns False for invalid callbacks"""
        from menu.analytics_menu_handler import AnalyticsMenuHandler
        
        mock_bot = Mock()
        handler = AnalyticsMenuHandler(mock_bot)
        
        # Test callback handling returns False for invalid callbacks
        assert handler.handle_callback("invalid_callback", 123, 456) == False


class TestDualOrderMenuHandler:
    """Tests for Dual Order Menu Handler (Phase 5)"""
    
    def test_dual_order_menu_handler_init(self):
        """Test DualOrderMenuHandler initialization"""
        from menu.dual_order_menu_handler import DualOrderMenuHandler
        
        mock_bot = Mock()
        handler = DualOrderMenuHandler(mock_bot)
        
        assert handler._bot == mock_bot
        assert handler.ORDER_MODES == ["order_a", "order_b", "both"]
    
    def test_dual_order_menu_handler_has_required_methods(self):
        """Test DualOrderMenuHandler has all required methods"""
        from menu.dual_order_menu_handler import DualOrderMenuHandler
        
        mock_bot = Mock()
        handler = DualOrderMenuHandler(mock_bot)
        
        # Check required methods exist
        assert hasattr(handler, 'show_dual_order_menu')
        assert hasattr(handler, 'show_plugin_dual_order_config')
        assert hasattr(handler, 'show_mode_selection')
        assert hasattr(handler, 'handle_callback')
    
    def test_dual_order_menu_handler_callback_handling(self):
        """Test DualOrderMenuHandler callback handling"""
        from menu.dual_order_menu_handler import DualOrderMenuHandler
        
        mock_bot = Mock()
        handler = DualOrderMenuHandler(mock_bot)
        
        # Test callback handling returns True for valid callbacks
        assert handler.handle_callback("menu_dual_order", 123, 456) == True
        assert handler.handle_callback("dual_config_v3_logic1", 123, 456) == True
        
        # Test callback handling returns False for invalid callbacks
        assert handler.handle_callback("invalid_callback", 123, 456) == False


class TestReentryMenuHandler:
    """Tests for Re-entry Menu Handler (Phase 5)"""
    
    def test_reentry_menu_handler_init(self):
        """Test ReentryMenuHandler initialization"""
        from menu.dual_order_menu_handler import ReentryMenuHandler
        
        mock_bot = Mock()
        handler = ReentryMenuHandler(mock_bot)
        
        assert handler._bot == mock_bot
        assert handler.REENTRY_TYPES == ["tp_continuation", "sl_hunt_recovery", "exit_continuation"]
    
    def test_reentry_menu_handler_has_required_methods(self):
        """Test ReentryMenuHandler has all required methods"""
        from menu.dual_order_menu_handler import ReentryMenuHandler
        
        mock_bot = Mock()
        handler = ReentryMenuHandler(mock_bot)
        
        # Check required methods exist
        assert hasattr(handler, 'show_reentry_menu')
        assert hasattr(handler, 'show_plugin_reentry_config')
        assert hasattr(handler, 'handle_callback')
    
    def test_reentry_menu_handler_callback_handling(self):
        """Test ReentryMenuHandler callback handling"""
        from menu.dual_order_menu_handler import ReentryMenuHandler
        
        mock_bot = Mock()
        handler = ReentryMenuHandler(mock_bot)
        
        # Test callback handling returns True for valid callbacks
        assert handler.handle_callback("menu_reentry", 123, 456) == True
        assert handler.handle_callback("reentry_config_v3_logic1", 123, 456) == True
        
        # Test callback handling returns False for invalid callbacks
        assert handler.handle_callback("invalid_callback", 123, 456) == False


class TestMenuManagerIntegration:
    """Tests for MenuManager Integration (Phase 6)"""
    
    def test_menu_manager_has_v6_handler(self):
        """Test MenuManager has V6ControlMenuHandler"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, '_v6_handler')
        assert manager._v6_handler is not None
    
    def test_menu_manager_has_analytics_handler(self):
        """Test MenuManager has AnalyticsMenuHandler"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, '_analytics_handler')
        assert manager._analytics_handler is not None
    
    def test_menu_manager_has_dual_order_handler(self):
        """Test MenuManager has DualOrderMenuHandler"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, '_dual_order_handler')
        assert manager._dual_order_handler is not None
    
    def test_menu_manager_has_reentry_handler(self):
        """Test MenuManager has ReentryMenuHandler"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, '_reentry_handler')
        assert manager._reentry_handler is not None
    
    def test_menu_manager_has_v6_methods(self):
        """Test MenuManager has V6 menu methods"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, 'show_v6_menu')
        assert hasattr(manager, 'handle_v6_callback')
        assert hasattr(manager, 'is_v6_callback')
    
    def test_menu_manager_has_analytics_methods(self):
        """Test MenuManager has Analytics menu methods"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, 'show_analytics_menu')
        assert hasattr(manager, 'handle_analytics_callback')
        assert hasattr(manager, 'is_analytics_callback')
    
    def test_menu_manager_has_dual_order_methods(self):
        """Test MenuManager has Dual Order menu methods"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, 'show_dual_order_menu')
        assert hasattr(manager, 'handle_dual_order_callback')
        assert hasattr(manager, 'is_dual_order_callback')
    
    def test_menu_manager_has_reentry_methods(self):
        """Test MenuManager has Re-entry menu methods"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, 'show_reentry_menu')
        assert hasattr(manager, 'handle_reentry_callback')
        assert hasattr(manager, 'is_reentry_callback')
    
    def test_menu_manager_is_v6_callback(self):
        """Test MenuManager.is_v6_callback correctly identifies V6 callbacks"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        # V6 callbacks should return True
        assert manager.is_v6_callback("menu_v6") == True
        assert manager.is_v6_callback("v6_toggle_system") == True
        assert manager.is_v6_callback("v6_toggle_15m") == True
        
        # Non-V6 callbacks should return False
        assert manager.is_v6_callback("menu_main") == False
        assert manager.is_v6_callback("analytics_daily") == False
    
    def test_menu_manager_is_analytics_callback(self):
        """Test MenuManager.is_analytics_callback correctly identifies Analytics callbacks"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        # Analytics callbacks should return True
        assert manager.is_analytics_callback("menu_analytics") == True
        assert manager.is_analytics_callback("analytics_daily") == True
        assert manager.is_analytics_callback("analytics_weekly") == True
        
        # Non-Analytics callbacks should return False
        assert manager.is_analytics_callback("menu_main") == False
        assert manager.is_analytics_callback("v6_toggle_system") == False


class TestServiceAPIV6Methods:
    """Tests for ServiceAPI V6 Methods"""
    
    def test_service_api_has_v6_notification_methods(self):
        """Test ServiceAPI has V6 notification methods"""
        from core.plugin_system.service_api import ServiceAPI
        
        # Check V6 notification methods exist
        assert hasattr(ServiceAPI, 'send_v6_entry_notification')
        assert hasattr(ServiceAPI, 'send_v6_exit_notification')
        assert hasattr(ServiceAPI, 'send_v6_tp_notification')
        assert hasattr(ServiceAPI, 'send_v6_sl_notification')
        assert hasattr(ServiceAPI, 'send_v6_timeframe_toggle_notification')
        assert hasattr(ServiceAPI, 'send_v6_daily_summary')
        assert hasattr(ServiceAPI, 'send_v6_signal_notification')


class TestNotificationPreferences:
    """Tests for Notification Preferences System (Batch 1)"""
    
    @staticmethod
    def _get_notification_preferences_class():
        """Helper to import NotificationPreferences avoiding telegram package conflict"""
        import importlib.util
        import os
        spec = importlib.util.spec_from_file_location(
            "notification_preferences",
            os.path.join(os.path.dirname(__file__), '..', 'src', 'telegram', 'notification_preferences.py')
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.NotificationPreferences
    
    def test_notification_preferences_init(self):
        """Test NotificationPreferences initialization"""
        NotificationPreferences = self._get_notification_preferences_class()
        
        # Create with temp config path to avoid file system issues
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            prefs = NotificationPreferences(config_path=f.name)
        
        assert prefs is not None
        assert prefs.is_enabled() == True  # Default is enabled
    
    def test_notification_preferences_category_toggle(self):
        """Test NotificationPreferences category toggle"""
        NotificationPreferences = self._get_notification_preferences_class()
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            prefs = NotificationPreferences(config_path=f.name)
        
        # Test category toggle
        initial = prefs.is_category_enabled("trade_entry")
        prefs.toggle_category("trade_entry")
        assert prefs.is_category_enabled("trade_entry") != initial
    
    def test_notification_preferences_plugin_filter(self):
        """Test NotificationPreferences plugin filter"""
        NotificationPreferences = self._get_notification_preferences_class()
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            prefs = NotificationPreferences(config_path=f.name)
        
        # Test plugin filter
        prefs.set_plugin_filter("v3_only")
        assert prefs.get_plugin_filter() == "v3_only"
        
        prefs.set_plugin_filter("v6_only")
        assert prefs.get_plugin_filter() == "v6_only"
        
        prefs.set_plugin_filter("all")
        assert prefs.get_plugin_filter() == "all"
    
    def test_notification_preferences_priority_level(self):
        """Test NotificationPreferences priority level"""
        NotificationPreferences = self._get_notification_preferences_class()
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            prefs = NotificationPreferences(config_path=f.name)
        
        # Test priority level
        prefs.set_priority_level("critical_only")
        assert prefs.get_priority_level() == "critical_only"
        
        prefs.set_priority_level("high_and_above")
        assert prefs.get_priority_level() == "high_and_above"
    
    def test_notification_preferences_v6_timeframe_filter(self):
        """Test NotificationPreferences V6 timeframe filter"""
        NotificationPreferences = self._get_notification_preferences_class()
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            prefs = NotificationPreferences(config_path=f.name)
        
        # Test V6 timeframe filter
        prefs.set_v6_timeframe_enabled("15m", False)
        assert prefs.is_v6_timeframe_enabled("15m") == False
        
        prefs.set_v6_timeframe_enabled("15m", True)
        assert prefs.is_v6_timeframe_enabled("15m") == True
    
    def test_notification_preferences_should_send(self):
        """Test NotificationPreferences should_send_notification"""
        NotificationPreferences = self._get_notification_preferences_class()
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            prefs = NotificationPreferences(config_path=f.name)
        
        # Test should_send_notification
        assert prefs.should_send_notification("trade_entry") == True
        
        # Disable category and test
        prefs.set_category_enabled("trade_entry", False)
        assert prefs.should_send_notification("trade_entry") == False
    
    def test_notification_preferences_reset(self):
        """Test NotificationPreferences reset to defaults"""
        NotificationPreferences = self._get_notification_preferences_class()
        
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            prefs = NotificationPreferences(config_path=f.name)
        
        # Change some settings
        prefs.set_plugin_filter("v3_only")
        prefs.set_priority_level("critical_only")
        
        # Reset to defaults
        prefs.reset_to_defaults()
        
        assert prefs.get_plugin_filter() == "all"
        assert prefs.get_priority_level() == "all"


class TestNotificationPreferencesMenuHandler:
    """Tests for Notification Preferences Menu Handler (Batch 1)"""
    
    def test_notification_prefs_menu_handler_init(self):
        """Test NotificationPreferencesMenuHandler initialization"""
        from menu.notification_preferences_menu import NotificationPreferencesMenuHandler
        
        mock_bot = Mock()
        handler = NotificationPreferencesMenuHandler(mock_bot)
        
        assert handler.bot == mock_bot
    
    def test_notification_prefs_menu_handler_has_required_methods(self):
        """Test NotificationPreferencesMenuHandler has all required methods"""
        from menu.notification_preferences_menu import NotificationPreferencesMenuHandler
        
        mock_bot = Mock()
        handler = NotificationPreferencesMenuHandler(mock_bot)
        
        # Check required methods exist
        assert hasattr(handler, 'show_main_menu')
        assert hasattr(handler, 'show_categories_menu')
        assert hasattr(handler, 'show_plugin_filter_menu')
        assert hasattr(handler, 'show_priority_menu')
        assert hasattr(handler, 'show_quiet_hours_menu')
        assert hasattr(handler, 'show_v6_timeframes_menu')
        assert hasattr(handler, 'handle_callback')
    
    def test_notification_prefs_menu_handler_callback_returns_false_for_invalid(self):
        """Test NotificationPreferencesMenuHandler callback handling returns False for invalid callbacks"""
        from menu.notification_preferences_menu import NotificationPreferencesMenuHandler
        
        mock_bot = Mock()
        handler = NotificationPreferencesMenuHandler(mock_bot)
        
        # Test callback handling returns False for invalid callbacks
        assert handler.handle_callback("invalid_callback", 123, 456) == False


class TestMenuManagerNotificationPrefsIntegration:
    """Tests for MenuManager Notification Preferences Integration (Batch 1)"""
    
    def test_menu_manager_has_notification_prefs_handler(self):
        """Test MenuManager has NotificationPreferencesMenuHandler"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, '_notification_prefs_handler')
        assert manager._notification_prefs_handler is not None
    
    def test_menu_manager_has_notification_prefs_methods(self):
        """Test MenuManager has notification preferences menu methods"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        assert hasattr(manager, 'show_notification_prefs_menu')
        assert hasattr(manager, 'handle_notification_prefs_callback')


class TestControllerBot105Commands:
    """Tests for all 105 command handlers in ControllerBot (Final Testing)
    
    This test class verifies that all 105 commands are properly wired in controller_bot.py
    by analyzing the source code directly (avoiding import issues with relative imports).
    """
    
    # All 105 commands organized by category
    SYSTEM_COMMANDS = ["/start", "/status", "/pause", "/resume", "/help", "/health", "/version", "/restart", "/shutdown", "/config"]
    TRADING_COMMANDS = ["/trade", "/buy", "/sell", "/close", "/closeall", "/positions", "/orders", "/history", "/pnl", "/balance", "/equity", "/margin", "/symbols", "/price", "/spread"]
    RISK_COMMANDS = ["/risk", "/setlot", "/setsl", "/settp", "/dailylimit", "/maxloss", "/maxprofit", "/risktier", "/slsystem", "/trailsl", "/breakeven", "/protection"]
    STRATEGY_COMMANDS = ["/strategy", "/logic1", "/logic2", "/logic3", "/v3", "/v6", "/v6_status", "/v6_control", "/tf15m_on", "/tf15m_off", "/tf30m_on", "/tf30m_off", "/tf1h_on", "/tf1h_off", "/tf4h_on", "/tf4h_off", "/signals", "/filters", "/multiplier", "/mode"]
    TIMEFRAME_COMMANDS = ["/timeframe", "/tf1m", "/tf5m", "/tf15m", "/tf1h", "/tf4h", "/tf1d", "/trends"]
    REENTRY_COMMANDS = ["/reentry", "/slhunt", "/tpcontinue", "/recovery", "/cooldown", "/chains", "/autonomous", "/chainlimit"]
    PROFIT_COMMANDS = ["/profit", "/booking", "/levels", "/partial", "/orderb", "/dualorder"]
    ANALYTICS_COMMANDS = ["/analytics", "/performance", "/daily", "/weekly", "/monthly", "/stats", "/winrate", "/drawdown"]
    SESSION_COMMANDS = ["/session", "/london", "/newyork", "/tokyo", "/sydney", "/overlap"]
    PLUGIN_COMMANDS = ["/plugin", "/plugins", "/enable", "/disable", "/upgrade", "/rollback", "/shadow", "/compare"]
    VOICE_COMMANDS = ["/voice", "/voicetest", "/mute", "/unmute"]
    
    @staticmethod
    def _get_controller_bot_source():
        """Read controller_bot.py source code for analysis"""
        import os
        controller_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'telegram', 'controller_bot.py')
        with open(controller_path, 'r') as f:
            return f.read()
    
    def test_controller_bot_has_all_105_handlers_wired(self):
        """Test ControllerBot has all 105 command handlers wired in _wire_default_handlers"""
        source = self._get_controller_bot_source()
        
        all_commands = (
            self.SYSTEM_COMMANDS + self.TRADING_COMMANDS + self.RISK_COMMANDS +
            self.STRATEGY_COMMANDS + self.TIMEFRAME_COMMANDS + self.REENTRY_COMMANDS +
            self.PROFIT_COMMANDS + self.ANALYTICS_COMMANDS + self.SESSION_COMMANDS +
            self.PLUGIN_COMMANDS + self.VOICE_COMMANDS
        )
        
        # Verify total count
        assert len(all_commands) == 105, f"Expected 105 commands, got {len(all_commands)}"
        
        # Verify all handlers are wired by checking source code
        missing_handlers = []
        for cmd in all_commands:
            # Check if command is wired in _wire_default_handlers (e.g., self._command_handlers["/start"])
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            if wiring_pattern not in source:
                missing_handlers.append(cmd)
        
        assert len(missing_handlers) == 0, f"Missing handlers for: {missing_handlers}"
    
    def test_system_commands_wired(self):
        """Test all 10 system commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.SYSTEM_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_trading_commands_wired(self):
        """Test all 15 trading commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.TRADING_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_risk_commands_wired(self):
        """Test all 12 risk commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.RISK_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_strategy_commands_wired(self):
        """Test all 20 strategy commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.STRATEGY_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_timeframe_commands_wired(self):
        """Test all 8 timeframe commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.TIMEFRAME_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_reentry_commands_wired(self):
        """Test all 8 re-entry commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.REENTRY_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_profit_commands_wired(self):
        """Test all 6 profit commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.PROFIT_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_analytics_commands_wired(self):
        """Test all 8 analytics commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.ANALYTICS_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_session_commands_wired(self):
        """Test all 6 session commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.SESSION_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_plugin_commands_wired(self):
        """Test all 8 plugin commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.PLUGIN_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_voice_commands_wired(self):
        """Test all 4 voice commands are wired"""
        source = self._get_controller_bot_source()
        
        for cmd in self.VOICE_COMMANDS:
            wiring_pattern = f'self._command_handlers["{cmd}"]'
            assert wiring_pattern in source, f"Missing handler wiring for {cmd}"
    
    def test_all_handlers_have_implementations(self):
        """Test all command handlers have method implementations"""
        source = self._get_controller_bot_source()
        
        # Map commands to their expected handler method names
        handler_methods = [
            "handle_start", "handle_status", "handle_pause", "handle_resume", "handle_help",
            "handle_health_command", "handle_version_command", "handle_restart", "handle_shutdown", "handle_config",
            "handle_trade_menu", "handle_buy", "handle_sell", "handle_close", "handle_close_all",
            "handle_positions", "handle_orders", "handle_history", "handle_pnl", "handle_balance",
            "handle_equity", "handle_margin", "handle_symbols", "handle_price", "handle_spread",
            "handle_risk_menu", "handle_set_lot", "handle_set_sl", "handle_set_tp", "handle_daily_limit",
            "handle_max_loss", "handle_max_profit", "handle_risk_tier", "handle_sl_system", "handle_trail_sl",
            "handle_breakeven", "handle_protection", "handle_strategy_menu", "handle_logic1", "handle_logic2",
            "handle_logic3", "handle_v3", "handle_v6", "handle_v6_status", "handle_v6_control",
            "handle_v6_tf15m_on", "handle_v6_tf15m_off", "handle_v6_tf30m_on", "handle_v6_tf30m_off",
            "handle_v6_tf1h_on", "handle_v6_tf1h_off", "handle_v6_tf4h_on", "handle_v6_tf4h_off",
            "handle_signals", "handle_filters", "handle_multiplier", "handle_mode",
            "handle_timeframe_menu", "handle_tf_1m", "handle_tf_5m", "handle_tf_15m", "handle_tf_1h",
            "handle_tf_4h", "handle_tf_1d", "handle_trends", "handle_reentry_menu", "handle_sl_hunt",
            "handle_tp_continue", "handle_recovery", "handle_cooldown", "handle_chains", "handle_autonomous",
            "handle_chain_limit", "handle_profit_menu", "handle_booking", "handle_levels", "handle_partial",
            "handle_order_b", "handle_dual_order", "handle_analytics_menu", "handle_performance", "handle_daily",
            "handle_weekly", "handle_monthly", "handle_stats", "handle_winrate", "handle_drawdown",
            "handle_session_menu", "handle_london", "handle_newyork", "handle_tokyo", "handle_sydney",
            "handle_overlap", "handle_plugin_menu", "handle_plugins", "handle_enable", "handle_disable",
            "handle_upgrade_command", "handle_rollback_command", "handle_shadow", "handle_compare",
            "handle_voice_menu", "handle_voice_test", "handle_mute", "handle_unmute"
        ]
        
        missing_methods = []
        for method in handler_methods:
            # Check if method is defined (def method_name)
            method_pattern = f"def {method}(self"
            if method_pattern not in source:
                missing_methods.append(method)
        
        assert len(missing_methods) == 0, f"Missing handler method implementations: {missing_methods}"


class TestMenuManagerNotificationPrefsCallback:
    """Tests for MenuManager notification preferences callback"""
    
    def test_menu_manager_is_notification_prefs_callback(self):
        """Test MenuManager.is_notification_prefs_callback correctly identifies notification prefs callbacks"""
        from menu.menu_manager import MenuManager
        
        mock_bot = Mock()
        mock_bot.config = {}
        manager = MenuManager(mock_bot)
        
        # Notification prefs callbacks should return True
        assert manager.is_notification_prefs_callback("notif_main") == True
        assert manager.is_notification_prefs_callback("notif_categories") == True
        assert manager.is_notification_prefs_callback("menu_notifications") == True
        
        # Non-notification prefs callbacks should return False
        assert manager.is_notification_prefs_callback("menu_main") == False
        assert manager.is_notification_prefs_callback("v6_toggle_system") == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
