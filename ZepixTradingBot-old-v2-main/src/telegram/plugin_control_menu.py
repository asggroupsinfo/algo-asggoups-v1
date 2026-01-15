"""
Plugin Control Menu - Live Plugin Management via Telegram

This module provides a Telegram menu interface for controlling plugins
at runtime without requiring a bot restart.

Features:
- Plugin selector: [V3 Logic] [V6 Logic] buttons
- Enable/Disable: Live plugin switching
- Status display: Show which plugins are active
- Per-plugin settings access

Version: 1.0.0
Date: 2026-01-15
"""

import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime

logger = logging.getLogger(__name__)


class PluginControlMenu:
    """
    Plugin control menu for Telegram.
    
    Provides live plugin management without restart.
    """
    
    def __init__(self, trading_engine=None, telegram_bot=None):
        """
        Initialize PluginControlMenu.
        
        Args:
            trading_engine: TradingEngine instance for plugin control
            telegram_bot: TelegramBot instance for sending messages
        """
        self._engine = trading_engine
        self._bot = telegram_bot
        
        # Callback handlers
        self._callbacks: Dict[str, Callable] = {
            "plugin_menu": self.show_plugin_menu,
            "plugin_v3_menu": self.show_v3_menu,
            "plugin_v6_menu": self.show_v6_menu,
            "plugin_v3_enable": lambda chat_id: self.toggle_plugin(chat_id, "v3_combined", True),
            "plugin_v3_disable": lambda chat_id: self.toggle_plugin(chat_id, "v3_combined", False),
            "plugin_v6_enable": lambda chat_id: self.toggle_plugin(chat_id, "v6_price_action", True),
            "plugin_v6_disable": lambda chat_id: self.toggle_plugin(chat_id, "v6_price_action", False),
            "plugin_status": self.show_status,
        }
        
        logger.info("[PluginControlMenu] Initialized")
    
    def set_dependencies(self, trading_engine=None, telegram_bot=None):
        """
        Set dependencies after initialization.
        
        Args:
            trading_engine: TradingEngine instance
            telegram_bot: TelegramBot instance
        """
        if trading_engine:
            self._engine = trading_engine
        if telegram_bot:
            self._bot = telegram_bot
        
        logger.info("[PluginControlMenu] Dependencies updated")
    
    def get_callbacks(self) -> Dict[str, Callable]:
        """Get callback handlers for registration"""
        return self._callbacks
    
    def handle_callback(self, callback_data: str, chat_id: int) -> bool:
        """
        Handle a callback from Telegram.
        
        Args:
            callback_data: Callback data string
            chat_id: Telegram chat ID
        
        Returns:
            True if callback was handled
        """
        if callback_data in self._callbacks:
            try:
                self._callbacks[callback_data](chat_id)
                return True
            except Exception as e:
                logger.error(f"[PluginControlMenu] Callback error: {e}")
                return False
        return False
    
    def _send_message(self, chat_id: int, text: str, keyboard: List[List[Dict]] = None) -> Optional[int]:
        """
        Send a message via Telegram bot.
        
        Args:
            chat_id: Telegram chat ID
            text: Message text
            keyboard: Optional inline keyboard
        
        Returns:
            Message ID if successful
        """
        if not self._bot:
            logger.error("[PluginControlMenu] No bot configured")
            return None
        
        reply_markup = None
        if keyboard:
            reply_markup = {"inline_keyboard": keyboard}
        
        return self._bot.send_message(text, chat_id=chat_id, reply_markup=reply_markup)
    
    def _get_plugin_status(self, plugin_id: str) -> bool:
        """
        Get plugin enabled status.
        
        Args:
            plugin_id: Plugin identifier
        
        Returns:
            True if plugin is enabled
        """
        if not self._engine:
            return False
        
        # Try different methods to check plugin status
        if hasattr(self._engine, 'is_plugin_enabled'):
            return self._engine.is_plugin_enabled(plugin_id)
        elif hasattr(self._engine, '_active_plugins'):
            return plugin_id in self._engine._active_plugins
        elif hasattr(self._engine, 'get_active_plugins'):
            return plugin_id in self._engine.get_active_plugins()
        
        # Fallback: check config
        return True  # Assume enabled if can't determine
    
    def show_plugin_menu(self, chat_id: int) -> Optional[int]:
        """
        Show main plugin control menu.
        
        Args:
            chat_id: Telegram chat ID
        
        Returns:
            Message ID if successful
        """
        v3_enabled = self._get_plugin_status("v3_combined")
        v6_enabled = self._get_plugin_status("v6_price_action")
        
        v3_status = "ENABLED" if v3_enabled else "DISABLED"
        v6_status = "ENABLED" if v6_enabled else "DISABLED"
        
        v3_emoji = "🟢" if v3_enabled else "🔴"
        v6_emoji = "🟢" if v6_enabled else "🔴"
        
        message = (
            "🔌 <b>PLUGIN CONTROL</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Active Plugins:</b>\n"
            f"├─ V3 Combined Logic: {v3_emoji} {v3_status}\n"
            f"└─ V6 Price Action: {v6_emoji} {v6_status}\n\n"
            "<i>Select a plugin to manage:</i>"
        )
        
        keyboard = [
            [{"text": f"{v3_emoji} V3 Combined Logic", "callback_data": "plugin_v3_menu"}],
            [{"text": f"{v6_emoji} V6 Price Action", "callback_data": "plugin_v6_menu"}],
            [{"text": "📊 Full Status", "callback_data": "plugin_status"}],
            [{"text": "🔙 Back to Main", "callback_data": "menu_main"}]
        ]
        
        return self._send_message(chat_id, message, keyboard)
    
    def show_v3_menu(self, chat_id: int) -> Optional[int]:
        """
        Show V3 plugin control menu.
        
        Args:
            chat_id: Telegram chat ID
        
        Returns:
            Message ID if successful
        """
        v3_enabled = self._get_plugin_status("v3_combined")
        status = "ENABLED" if v3_enabled else "DISABLED"
        emoji = "🟢" if v3_enabled else "🔴"
        
        message = (
            f"📦 <b>V3 COMBINED LOGIC</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Status:</b> {emoji} {status}\n\n"
            f"<b>Description:</b>\n"
            f"Pine Script V3 Combined Logic with:\n"
            f"├─ LOGIC1: 5m Scalping Mode\n"
            f"├─ LOGIC2: 15m Intraday Mode\n"
            f"└─ LOGIC3: 1h Swing Mode\n\n"
            f"<b>Features:</b>\n"
            f"├─ Multi-timeframe signal routing\n"
            f"├─ Dual order system (A+B)\n"
            f"├─ Re-entry & profit booking\n"
            f"└─ Autonomous recovery\n\n"
            f"<i>Select an action:</i>"
        )
        
        # Show opposite action button
        if v3_enabled:
            action_button = {"text": "🔴 Disable V3", "callback_data": "plugin_v3_disable"}
        else:
            action_button = {"text": "🟢 Enable V3", "callback_data": "plugin_v3_enable"}
        
        keyboard = [
            [action_button],
            [{"text": "⚙️ V3 Settings", "callback_data": "menu_strategy"}],
            [{"text": "🔙 Back to Plugins", "callback_data": "plugin_menu"}]
        ]
        
        return self._send_message(chat_id, message, keyboard)
    
    def show_v6_menu(self, chat_id: int) -> Optional[int]:
        """
        Show V6 plugin control menu.
        
        Args:
            chat_id: Telegram chat ID
        
        Returns:
            Message ID if successful
        """
        v6_enabled = self._get_plugin_status("v6_price_action")
        status = "ENABLED" if v6_enabled else "DISABLED"
        emoji = "🟢" if v6_enabled else "🔴"
        
        message = (
            f"📦 <b>V6 PRICE ACTION</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Status:</b> {emoji} {status}\n\n"
            f"<b>Description:</b>\n"
            f"Pine Script V6 Price Action Logic with:\n"
            f"├─ Trend Pulse Detection\n"
            f"├─ Price Action Patterns\n"
            f"└─ Advanced Signal Filtering\n\n"
            f"<b>Features:</b>\n"
            f"├─ Multi-timeframe trend analysis\n"
            f"├─ Pattern recognition\n"
            f"├─ Momentum confirmation\n"
            f"└─ Shadow mode testing\n\n"
            f"<i>Select an action:</i>"
        )
        
        # Show opposite action button
        if v6_enabled:
            action_button = {"text": "🔴 Disable V6", "callback_data": "plugin_v6_disable"}
        else:
            action_button = {"text": "🟢 Enable V6", "callback_data": "plugin_v6_enable"}
        
        keyboard = [
            [action_button],
            [{"text": "⚙️ V6 Settings", "callback_data": "menu_v6_settings"}],
            [{"text": "🔙 Back to Plugins", "callback_data": "plugin_menu"}]
        ]
        
        return self._send_message(chat_id, message, keyboard)
    
    def toggle_plugin(self, chat_id: int, plugin_id: str, enable: bool) -> Optional[int]:
        """
        Toggle a plugin on/off.
        
        Args:
            chat_id: Telegram chat ID
            plugin_id: Plugin identifier
            enable: True to enable, False to disable
        
        Returns:
            Message ID if successful
        """
        action = "ENABLE" if enable else "DISABLE"
        plugin_name = "V3 Combined Logic" if "v3" in plugin_id else "V6 Price Action"
        
        success = False
        
        if self._engine:
            try:
                if enable:
                    if hasattr(self._engine, 'enable_plugin'):
                        success = self._engine.enable_plugin(plugin_id)
                    elif hasattr(self._engine, '_active_plugins'):
                        self._engine._active_plugins.add(plugin_id)
                        success = True
                else:
                    if hasattr(self._engine, 'disable_plugin'):
                        success = self._engine.disable_plugin(plugin_id)
                    elif hasattr(self._engine, '_active_plugins'):
                        self._engine._active_plugins.discard(plugin_id)
                        success = True
            except Exception as e:
                logger.error(f"[PluginControlMenu] Toggle error: {e}")
                success = False
        
        if success:
            emoji = "✅" if enable else "🔴"
            message = (
                f"{emoji} <b>PLUGIN {action}D</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"<b>{plugin_name}</b> has been {action.lower()}d.\n\n"
                f"<i>Changes take effect immediately.</i>"
            )
            logger.info(f"[PluginControlMenu] {plugin_id} {action}D")
        else:
            message = (
                f"❌ <b>PLUGIN {action} FAILED</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Failed to {action.lower()} <b>{plugin_name}</b>.\n\n"
                f"<i>Please check logs for details.</i>"
            )
            logger.error(f"[PluginControlMenu] Failed to {action} {plugin_id}")
        
        keyboard = [
            [{"text": "🔙 Back to Plugins", "callback_data": "plugin_menu"}]
        ]
        
        return self._send_message(chat_id, message, keyboard)
    
    def show_status(self, chat_id: int) -> Optional[int]:
        """
        Show full plugin status.
        
        Args:
            chat_id: Telegram chat ID
        
        Returns:
            Message ID if successful
        """
        v3_enabled = self._get_plugin_status("v3_combined")
        v6_enabled = self._get_plugin_status("v6_price_action")
        
        v3_emoji = "🟢" if v3_enabled else "🔴"
        v6_emoji = "🟢" if v6_enabled else "🔴"
        
        # Get additional stats if available
        v3_trades = 0
        v6_trades = 0
        
        if self._engine and hasattr(self._engine, 'get_plugin_stats'):
            try:
                v3_stats = self._engine.get_plugin_stats("v3_combined")
                v6_stats = self._engine.get_plugin_stats("v6_price_action")
                v3_trades = v3_stats.get('trades_today', 0)
                v6_trades = v6_stats.get('trades_today', 0)
            except Exception:
                pass
        
        message = (
            "📊 <b>PLUGIN STATUS REPORT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>V3 Combined Logic</b>\n"
            f"├─ Status: {v3_emoji} {'ENABLED' if v3_enabled else 'DISABLED'}\n"
            f"├─ Trades Today: {v3_trades}\n"
            f"└─ Mode: Production\n\n"
            f"<b>V6 Price Action</b>\n"
            f"├─ Status: {v6_emoji} {'ENABLED' if v6_enabled else 'DISABLED'}\n"
            f"├─ Trades Today: {v6_trades}\n"
            f"└─ Mode: Shadow\n\n"
            f"<b>System Info:</b>\n"
            f"├─ Active Plugins: {int(v3_enabled) + int(v6_enabled)}/2\n"
            f"└─ Last Update: {datetime.now().strftime('%H:%M:%S')}\n"
        )
        
        keyboard = [
            [{"text": "🔄 Refresh", "callback_data": "plugin_status"}],
            [{"text": "🔙 Back to Plugins", "callback_data": "plugin_menu"}]
        ]
        
        return self._send_message(chat_id, message, keyboard)
    
    def get_main_menu_button(self) -> Dict[str, str]:
        """
        Get button for main menu integration.
        
        Returns:
            Button dict for inline keyboard
        """
        return {"text": "🔌 Plugin Control", "callback_data": "plugin_menu"}


# Singleton instance for global access
_plugin_control_menu: Optional[PluginControlMenu] = None


def get_plugin_control_menu() -> PluginControlMenu:
    """Get or create singleton PluginControlMenu instance"""
    global _plugin_control_menu
    if _plugin_control_menu is None:
        _plugin_control_menu = PluginControlMenu()
    return _plugin_control_menu


def init_plugin_control_menu(trading_engine=None, telegram_bot=None) -> PluginControlMenu:
    """Initialize PluginControlMenu with dependencies"""
    global _plugin_control_menu
    _plugin_control_menu = PluginControlMenu(trading_engine, telegram_bot)
    return _plugin_control_menu
