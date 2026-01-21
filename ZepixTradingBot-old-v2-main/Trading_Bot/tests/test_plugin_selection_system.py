"""
Plugin Selection System - Comprehensive Test Suite

Tests all components of the V5 Plugin Selection Interceptor System.

Version: 1.0.0
Created: 2026-01-20
Part of: TELEGRAM_V5_PLUGIN_SELECTION_UPGRADE
"""

import pytest
import time
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

# Import modules under test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.telegram.plugin_context_manager import PluginContextManager
from src.telegram.command_interceptor import CommandInterceptor
from src.telegram.plugin_selection_menu_builder import PluginSelectionMenuBuilder


class TestPluginContextManager:
    """Test PluginContextManager functionality."""
    
    def setup_method(self):
        """Reset context manager before each test."""
        PluginContextManager.reset_all_contexts()
    
    def test_set_and_get_context(self):
        """Test setting and retrieving plugin context."""
        chat_id = 123456
        plugin = 'v3'
        
        # Set context
        result = PluginContextManager.set_plugin_context(chat_id, plugin, '/status')
        assert result == True
        
        # Get context
        retrieved = PluginContextManager.get_plugin_context(chat_id)
        assert retrieved == plugin
    
    def test_invalid_plugin_rejected(self):
        """Test that invalid plugin names are rejected."""
        chat_id = 123456
        
        result = PluginContextManager.set_plugin_context(chat_id, 'invalid', '/status')
        assert result == False
        
        # Should not have context
        assert PluginContextManager.get_plugin_context(chat_id) is None
    
    def test_context_expiry(self):
        """Test that context expires after 5 minutes."""
        chat_id = 123456
        
        # Set context with 2 second expiry (for testing)
        PluginContextManager.set_plugin_context(chat_id, 'v3', '/status', expiry_seconds=2)
        
        # Should exist immediately
        assert PluginContextManager.get_plugin_context(chat_id) == 'v3'
        
        # Wait 3 seconds
        time.sleep(3)
        
        # Should be expired
        assert PluginContextManager.get_plugin_context(chat_id) is None
    
    def test_multiple_users(self):
        """Test that different users have independent contexts."""
        chat_id_1 = 111111
        chat_id_2 = 222222
        
        PluginContextManager.set_plugin_context(chat_id_1, 'v3', '/status')
        PluginContextManager.set_plugin_context(chat_id_2, 'v6', '/positions')
        
        assert PluginContextManager.get_plugin_context(chat_id_1) == 'v3'
        assert PluginContextManager.get_plugin_context(chat_id_2) == 'v6'
    
    def test_clear_context(self):
        """Test clearing plugin context."""
        chat_id = 123456
        
        PluginContextManager.set_plugin_context(chat_id, 'v3', '/status')
        assert PluginContextManager.has_active_context(chat_id) == True
        
        PluginContextManager.clear_plugin_context(chat_id)
        assert PluginContextManager.has_active_context(chat_id) == False
    
    def test_get_full_context(self):
        """Test retrieving full context information."""
        chat_id = 123456
        
        PluginContextManager.set_plugin_context(chat_id, 'v6', '/pnl')
        
        full_context = PluginContextManager.get_full_context(chat_id)
        assert full_context is not None
        assert full_context['plugin'] == 'v6'
        assert full_context['command'] == '/pnl'
        assert 'timestamp' in full_context
    
    def test_cleanup_expired_contexts(self):
        """Test automatic cleanup of expired contexts."""
        # Create multiple contexts with short expiry
        for i in range(5):
            PluginContextManager.set_plugin_context(
                100000 + i,
                'v3',
                '/status',
                expiry_seconds=1
            )
        
        # All active
        stats = PluginContextManager.get_stats()
        assert stats['active_contexts'] == 5
        
        # Wait for expiry
        time.sleep(2)
        
        # Cleanup
        cleaned = PluginContextManager.cleanup_expired_contexts()
        assert cleaned == 5
        
        # No active contexts
        stats = PluginContextManager.get_stats()
        assert stats['active_contexts'] == 0
    
    def test_get_stats(self):
        """Test context statistics."""
        PluginContextManager.set_plugin_context(111, 'v3', '/status')
        PluginContextManager.set_plugin_context(222, 'v6', '/positions')
        PluginContextManager.set_plugin_context(333, 'both', '/pnl')
        
        stats = PluginContextManager.get_stats()
        assert stats['total_contexts'] == 3
        assert stats['v3_contexts'] == 1
        assert stats['v6_contexts'] == 1
        assert stats['both_contexts'] == 1


class TestCommandInterceptor:
    """Test CommandInterceptor functionality."""
    
    def setup_method(self):
        """Setup mock telegram bot and reset context."""
        self.mock_bot = Mock()
        self.interceptor = CommandInterceptor(telegram_bot=self.mock_bot)
        PluginContextManager.reset_all_contexts()
    
    def test_intercept_plugin_aware_command(self):
        """Test intercepting plugin-aware commands."""
        chat_id = 123456
        command = '/status'
        
        # Should intercept (no existing context)
        result = self.interceptor.intercept_command(command, chat_id, {})
        assert result == True
        
        # Should have shown selection screen
        self.mock_bot.send_message.assert_called_once()
    
    def test_skip_system_command(self):
        """Test that system commands are not intercepted."""
        chat_id = 123456
        command = '/start'  # System command
        
        # Should NOT intercept
        result = self.interceptor.intercept_command(command, chat_id, {})
        assert result == False
        
        # Should not send message
        self.mock_bot.send_message.assert_not_called()
    
    def test_skip_if_context_exists(self):
        """Test that commands proceed if context already exists."""
        chat_id = 123456
        command = '/status'
        
        # Set context
        PluginContextManager.set_plugin_context(chat_id, 'v3', command)
        
        # Should NOT intercept (context exists)
        result = self.interceptor.intercept_command(command, chat_id, {})
        assert result == False
    
    def test_handle_plugin_selection_callback_v3(self):
        """Test handling V3 plugin selection."""
        chat_id = 123456
        callback_data = 'plugin_select_v3_status'
        
        result = self.interceptor.handle_plugin_selection_callback(
            callback_data,
            chat_id,
            message_id=1
        )
        
        assert result is not None
        assert result['plugin'] == 'v3'
        assert result['command'] == '/status'
        
        # Context should be set
        assert PluginContextManager.get_plugin_context(chat_id) == 'v3'
    
    def test_handle_plugin_selection_callback_v6(self):
        """Test handling V6 plugin selection."""
        chat_id = 123456
        callback_data = 'plugin_select_v6_positions'
        
        result = self.interceptor.handle_plugin_selection_callback(
            callback_data,
            chat_id
        )
        
        assert result['plugin'] == 'v6'
        assert result['command'] == '/positions'
    
    def test_handle_plugin_selection_callback_both(self):
        """Test handling 'Both' plugin selection."""
        chat_id = 123456
        callback_data = 'plugin_select_both_pnl'
        
        result = self.interceptor.handle_plugin_selection_callback(
            callback_data,
            chat_id
        )
        
        assert result['plugin'] == 'both'
        assert result['command'] == '/pnl'
    
    def test_handle_plugin_selection_cancel(self):
        """Test handling cancel action."""
        chat_id = 123456
        callback_data = 'plugin_select_cancel'
        
        result = self.interceptor.handle_plugin_selection_callback(
            callback_data,
            chat_id
        )
        
        assert result is None
        # No context should be set
        assert PluginContextManager.get_plugin_context(chat_id) is None
    
    def test_is_command_plugin_aware(self):
        """Test command classification."""
        # Plugin-aware commands
        assert self.interceptor.is_command_plugin_aware('/status') == True
        assert self.interceptor.is_command_plugin_aware('/pause') == True
        assert self.interceptor.is_command_plugin_aware('/positions') == True
        
        # System commands
        assert self.interceptor.is_command_plugin_aware('/start') == False
        assert self.interceptor.is_command_plugin_aware('/help') == False
    
    def test_get_stats(self):
        """Test getting interceptor statistics."""
        stats = self.interceptor.get_stats()
        
        assert 'plugin_aware_commands' in stats
        assert 'system_commands' in stats
        assert stats['plugin_aware_commands'] > 90  # Should have 95+ commands


class TestPluginSelectionMenuBuilder:
    """Test PluginSelectionMenuBuilder functionality."""
    
    def test_build_selection_message(self):
        """Test building selection message."""
        message = PluginSelectionMenuBuilder.build_selection_message('/status')
        
        assert '🔌' in message
        assert '/STATUS' in message
        assert 'V3 Combined Logic' in message
        assert 'V6 Price Action' in message
        assert 'Both Plugins' in message
    
    def test_build_selection_keyboard(self):
        """Test building selection keyboard."""
        keyboard = PluginSelectionMenuBuilder.build_selection_keyboard('/status')
        
        assert 'inline_keyboard' in keyboard
        buttons = keyboard['inline_keyboard']
        
        # First row: V3 and V6
        assert len(buttons[0]) == 2
        assert 'plugin_select_v3_status' in buttons[0][0]['callback_data']
        assert 'plugin_select_v6_status' in buttons[0][1]['callback_data']
        
        # Second row: Both
        assert 'plugin_select_both_status' in buttons[1][0]['callback_data']
        
        # Third row: Cancel
        assert 'plugin_select_cancel' in buttons[2][0]['callback_data']
    
    def test_build_full_selection_screen(self):
        """Test building complete selection screen."""
        message, keyboard = PluginSelectionMenuBuilder.build_full_selection_screen('/positions')
        
        assert message is not None
        assert keyboard is not None
        assert 'POSITIONS' in message
        assert 'inline_keyboard' in keyboard
    
    def test_build_confirmation_message(self):
        """Test building confirmation message."""
        message = PluginSelectionMenuBuilder.build_confirmation_message('v3', '/status')
        
        assert '✅' in message
        assert 'V3 Combined Logic' in message
        assert '/STATUS' in message
    
    def test_get_plugin_display_name(self):
        """Test getting plugin display names."""
        v3_name = PluginSelectionMenuBuilder.get_plugin_display_name('v3')
        assert '🔵' in v3_name
        assert 'V3 Combined Logic' in v3_name
        
        v6_name = PluginSelectionMenuBuilder.get_plugin_display_name('v6')
        assert '🟢' in v6_name
        assert 'V6 Price Action' in v6_name


class TestEndToEndFlow:
    """Test complete end-to-end flows."""
    
    def setup_method(self):
        """Setup test environment."""
        self.mock_bot = Mock()
        self.interceptor = CommandInterceptor(telegram_bot=self.mock_bot)
        PluginContextManager.reset_all_contexts()
    
    def test_complete_status_flow(self):
        """Test complete /status command flow."""
        chat_id = 123456
        
        # 1. User sends /status
        intercepted = self.interceptor.intercept_command('/status', chat_id, {})
        assert intercepted == True  # Selection shown
        
        # 2. User selects V3
        result = self.interceptor.handle_plugin_selection_callback(
            'plugin_select_v3_status',
            chat_id
        )
        assert result['plugin'] == 'v3'
        
        # 3. Context is set
        assert PluginContextManager.get_plugin_context(chat_id) == 'v3'
        
        # 4. Command can now proceed (no re-interception)
        intercepted_again = self.interceptor.intercept_command('/status', chat_id, {})
        assert intercepted_again == False  # Context exists, proceed
        
        # 5. After execution, context cleared
        PluginContextManager.clear_plugin_context(chat_id)
        assert PluginContextManager.get_plugin_context(chat_id) is None
    
    def test_different_plugins_for_different_commands(self):
        """Test selecting different plugins for different commands."""
        chat_id = 123456
        
        # Status with V3
        self.interceptor.intercept_command('/status', chat_id, {})
        self.interceptor.handle_plugin_selection_callback('plugin_select_v3_status', chat_id)
        assert PluginContextManager.get_plugin_context(chat_id) == 'v3'
        PluginContextManager.clear_plugin_context(chat_id)
        
        # Positions with V6
        self.interceptor.intercept_command('/positions', chat_id, {})
        self.interceptor.handle_plugin_selection_callback('plugin_select_v6_positions', chat_id)
        assert PluginContextManager.get_plugin_context(chat_id) == 'v6'
        PluginContextManager.clear_plugin_context(chat_id)
    
    def test_multiple_users_independent_contexts(self):
        """Test that multiple users maintain independent contexts."""
        chat_1 = 111111
        chat_2 = 222222
        
        # User 1 selects V3 for /status
        self.interceptor.intercept_command('/status', chat_1, {})
        self.interceptor.handle_plugin_selection_callback('plugin_select_v3_status', chat_1)
        
        # User 2 selects V6 for /positions
        self.interceptor.intercept_command('/positions', chat_2, {})
        self.interceptor.handle_plugin_selection_callback('plugin_select_v6_positions', chat_2)
        
        # Verify independence
        assert PluginContextManager.get_plugin_context(chat_1) == 'v3'
        assert PluginContextManager.get_plugin_context(chat_2) == 'v6'


def run_all_tests():
    """Run all tests and generate report."""
    print("=" * 60)
    print("PLUGIN SELECTION SYSTEM - TEST REPORT")
    print("=" * 60)
    print()
    
    # Run pytest
    result = pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--color=yes'
    ])
    
    print()
    print("=" * 60)
    if result == 0:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)
    
    return result


if __name__ == '__main__':
    run_all_tests()
