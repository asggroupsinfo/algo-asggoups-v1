"""
Dual Order & Re-entry Menu Handler - Telegram V5 Upgrade

This module provides menu handlers for Dual Order System and Re-entry System
per-plugin configuration via Telegram menu interface.

Features:
- Per-plugin Dual Order configuration (Order A, Order B, Both)
- Per-plugin Re-entry configuration (TP Continuation, SL Hunt Recovery, Exit Continuation)
- Enable/disable per-plugin settings
- Parameter adjustment for each system

Version: 1.0.0
Date: 2026-01-19
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class DualOrderMenuHandler:
    """
    Menu Handler for Dual Order System per-plugin configuration.
    
    Provides:
    - Order A / Order B / Both selection per plugin
    - Lot size configuration for each order type
    - TP/SL configuration for each order type
    """
    
    # Order modes
    ORDER_MODES = ["order_a_only", "order_b_only", "dual_orders"]
    ORDER_MODE_LABELS = {
        "order_a_only": "📊 Order A Only (Quick Profit)",
        "order_b_only": "💎 Order B Only (Extended Profit)",
        "dual_orders": "🔀 Both Orders (Dual)"
    }
    
    # V3 Logics
    V3_LOGICS = ["LOGIC1", "LOGIC2", "LOGIC3"]
    V3_LOGIC_LABELS = {
        "LOGIC1": "🧠 V3 Logic 1 (5m)",
        "LOGIC2": "🧠 V3 Logic 2 (15m)",
        "LOGIC3": "🧠 V3 Logic 3 (1h)"
    }
    
    # V6 Timeframes
    V6_TIMEFRAMES = ["1M", "5M", "15M", "1H", "4H"]
    V6_TIMEFRAME_LABELS = {
        "1M": "📊 V6 1M",
        "5M": "📊 V6 5M",
        "15M": "📊 V6 15M",
        "1H": "📊 V6 1H",
        "4H": "📊 V6 4H"
    }
    
    def __init__(self, telegram_bot, config: Dict[str, Any] = None):
        """
        Initialize DualOrderMenuHandler.
        
        Args:
            telegram_bot: Telegram bot instance
            config: Bot configuration dictionary (Config object or dict)
        """
        self._bot = telegram_bot
        # Support both Config object and dict
        if hasattr(telegram_bot, 'config'):
            self._config_obj = telegram_bot.config  # Config object with save_config()
            self._config = telegram_bot.config.config if hasattr(telegram_bot.config, 'config') else telegram_bot.config
        else:
            self._config_obj = None
            self._config = config or {}
        logger.info("[DualOrderMenuHandler] Initialized")
    
    def set_config(self, config: Dict[str, Any]):
        """Update configuration reference"""
        if hasattr(config, 'config'):
            self._config_obj = config
            self._config = config.config
        else:
            self._config = config
    
    def _save_config(self):
        """Save config to file"""
        if self._config_obj and hasattr(self._config_obj, 'save_config'):
            self._config_obj.save_config()
            logger.info("[DualOrderMenuHandler] Config saved to file")
    
    def _get_dual_order_config(self, plugin: str = None, context: str = None) -> Dict[str, Any]:
        """
        Get dual order configuration.
        
        Args:
            plugin: "v3_combined" or "v6_price_action"
            context: For V3: "LOGIC1", "LOGIC2", "LOGIC3"
                    For V6: "1M", "5M", "15M", "1H", "4H"
        
        Returns:
            Dict with config
        """
        if "dual_order_config" not in self._config:
            self._config["dual_order_config"] = {
                "enabled": True,
                "v3_combined": {
                    "enabled": True,
                    "per_logic_routing": {
                        "LOGIC1": "dual_orders",
                        "LOGIC2": "dual_orders",
                        "LOGIC3": "dual_orders"
                    }
                },
                "v6_price_action": {
                    "enabled": True,
                    "per_timeframe_routing": {
                        "1M": "order_b_only",
                        "5M": "dual_orders",
                        "15M": "order_a_only",
                        "1H": "order_a_only",
                        "4H": "order_a_only"
                    }
                }
            }
        
        dual_config = self._config["dual_order_config"]
        
        if plugin and context:
            # Get specific timeframe/logic routing
            if plugin == "v3_combined":
                return dual_config.get("v3_combined", {}).get("per_logic_routing", {}).get(context, "dual_orders")
            elif plugin == "v6_price_action":
                return dual_config.get("v6_price_action", {}).get("per_timeframe_routing", {}).get(context, "dual_orders")
        elif plugin:
            # Get plugin-level config
            return dual_config.get(plugin, {})
        
        return dual_config
    
    def _send_message(self, text: str, reply_markup: Dict = None, message_id: int = None):
        """Send or edit message"""
        try:
            if message_id and hasattr(self._bot, 'edit_message'):
                self._bot.edit_message(text, message_id, reply_markup)
            elif hasattr(self._bot, 'send_message_with_keyboard') and reply_markup:
                self._bot.send_message_with_keyboard(text, reply_markup)
            elif hasattr(self._bot, 'send_message'):
                self._bot.send_message(text)
        except Exception as e:
            logger.error(f"[DualOrderMenuHandler] Error sending message: {e}")
    
    # =========================================================================
    # MAIN DUAL ORDER MENU
    # =========================================================================
    
    def show_dual_order_menu(self, user_id: int, message_id: int = None):
        """Show main dual order plugin selection menu"""
        logger.info(f"[DualOrderMenuHandler] Showing dual order menu for user {user_id}")
        
        dual_config = self._get_dual_order_config()
        system_enabled = dual_config.get("enabled", True)
        
        text = f"""💎 <b>DUAL ORDER SYSTEM</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🔌 <b>System Status:</b> {'✅ ENABLED' if system_enabled else '❌ DISABLED'}

📊 <b>Description:</b>
The Dual Order System allows placing two orders
simultaneously with different TP targets:
• <b>Order A:</b> Quick profit (smaller TP)
• <b>Order B:</b> Extended profit (larger TP)

━━━━━━━━━━━━━━━━━━━━━━━━
<i>Select a plugin to configure:</i>"""
        
        # Build keyboard with plugin options
        keyboard = [
            # System toggle
            [
                {"text": f"{'✅' if system_enabled else '❌'} Toggle System", "callback_data": "dual_toggle_system"}
            ],
            # Plugin selection
            [
                {"text": "🧠 V3 Combined Logic", "callback_data": "dual_select_v3"},
                {"text": "📊 V6 Price Action", "callback_data": "dual_select_v6"}
            ],
            # Navigation
            [
                {"text": "← Back to Orders Menu", "callback_data": "menu_orders"},
                {"text": "🏠 Main Menu", "callback_data": "menu_main"}
            ]
        ]
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v3_logic_selection(self, user_id: int, message_id: int = None):
        """Show V3 logic selection menu"""
        logger.info(f"[DualOrderMenuHandler] Showing V3 logic selection for user {user_id}")
        
        v3_config = self._get_dual_order_config("v3_combined")
        v3_enabled = v3_config.get("enabled", True)
        routing = v3_config.get("per_logic_routing", {})
        
        text = f"""🧠 <b>V3 COMBINED LOGIC - DUAL ORDER CONFIG</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🔌 <b>V3 Status:</b> {'✅ ENABLED' if v3_enabled else '❌ DISABLED'}

📊 <b>Current Routing:</b>
• LOGIC1 (5m):  {self.ORDER_MODE_LABELS.get(routing.get('LOGIC1', 'dual_orders'), 'Dual Orders')}
• LOGIC2 (15m): {self.ORDER_MODE_LABELS.get(routing.get('LOGIC2', 'dual_orders'), 'Dual Orders')}
• LOGIC3 (1h):  {self.ORDER_MODE_LABELS.get(routing.get('LOGIC3', 'dual_orders'), 'Dual Orders')}

━━━━━━━━━━━━━━━━━━━━━━━━
<i>Select a logic to configure:</i>"""
        
        keyboard = []
        
        # V3 enable/disable
        keyboard.append([
            {"text": f"{'✅' if v3_enabled else '❌'} Toggle V3", "callback_data": "dual_toggle_v3"}
        ])
        
        # Logic selection
        for logic in self.V3_LOGICS:
            current_mode = routing.get(logic, "dual_orders")
            status = self.ORDER_MODE_LABELS.get(current_mode, "Dual Orders")
            keyboard.append([
                {"text": f"{self.V3_LOGIC_LABELS[logic]} → {status}", "callback_data": f"dual_v3_{logic}"}
            ])
        
        # Navigation
        keyboard.append([
            {"text": "◀️ Back", "callback_data": "menu_dual_order_main"},
            {"text": "🏠 Main Menu", "callback_data": "menu_main"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v6_timeframe_selection(self, user_id: int, message_id: int = None):
        """Show V6 timeframe selection menu"""
        logger.info(f"[DualOrderMenuHandler] Showing V6 timeframe selection for user {user_id}")
        
        v6_config = self._get_dual_order_config("v6_price_action")
        v6_enabled = v6_config.get("enabled", True)
        routing = v6_config.get("per_timeframe_routing", {})
        
        text = f"""📊 <b>V6 PRICE ACTION - DUAL ORDER CONFIG</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🔌 <b>V6 Status:</b> {'✅ ENABLED' if v6_enabled else '❌ DISABLED'}

📊 <b>Current Routing:</b>
• 1M:  {self.ORDER_MODE_LABELS.get(routing.get('1M', 'order_b_only'), 'Order B Only')}
• 5M:  {self.ORDER_MODE_LABELS.get(routing.get('5M', 'dual_orders'), 'Dual Orders')}
• 15M: {self.ORDER_MODE_LABELS.get(routing.get('15M', 'order_a_only'), 'Order A Only')}
• 1H:  {self.ORDER_MODE_LABELS.get(routing.get('1H', 'order_a_only'), 'Order A Only')}
• 4H:  {self.ORDER_MODE_LABELS.get(routing.get('4H', 'order_a_only'), 'Order A Only')}

━━━━━━━━━━━━━━━━━━━━━━━━
<i>Select a timeframe to configure:</i>"""
        
        keyboard = []
        
        # V6 enable/disable
        keyboard.append([
            {"text": f"{'✅' if v6_enabled else '❌'} Toggle V6", "callback_data": "dual_toggle_v6"}
        ])
        
        # Timeframe selection (2 per row)
        row = []
        for idx, tf in enumerate(self.V6_TIMEFRAMES):
            current_mode = routing.get(tf, "dual_orders")
            status_icon = {"order_a_only": "📊", "order_b_only": "💎", "dual_orders": "🔀"}.get(current_mode, "🔀")
            row.append({"text": f"{status_icon} {tf}", "callback_data": f"dual_v6_{tf}"})
            if len(row) == 2 or idx == len(self.V6_TIMEFRAMES) - 1:
                keyboard.append(row)
                row = []
        
        # Navigation
        keyboard.append([
            {"text": "◀️ Back", "callback_data": "menu_dual_order_main"},
            {"text": "🏠 Main Menu", "callback_data": "menu_main"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v3_logic_mode_selection(self, logic: str, user_id: int, message_id: int = None):
        """Show mode selection for a V3 logic"""
        logger.info(f"[DualOrderMenuHandler] Showing mode selection for V3 {logic}")
        
        current_mode = self._get_dual_order_config("v3_combined", logic)
        
        text = f"""📋 <b>V3 {logic} - SELECT ORDER MODE</b>
━━━━━━━━━━━━━━━━━━━━━━━━

Current Mode: <b>{self.ORDER_MODE_LABELS.get(current_mode, 'Dual Orders')}</b>

Select new mode:"""
        
        keyboard = []
        for mode in self.ORDER_MODES:
            is_current = mode == current_mode
            label = self.ORDER_MODE_LABELS.get(mode, mode)
            emoji = "✅" if is_current else "⚪"
            keyboard.append([{"text": f"{emoji} {label}", "callback_data": f"dual_set_v3_{logic}_{mode}"}])
        
        keyboard.append([
            {"text": "◀️ Back", "callback_data": "dual_select_v3"},
            {"text": "🏠 Main Menu", "callback_data": "menu_main"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v6_timeframe_mode_selection(self, timeframe: str, user_id: int, message_id: int = None):
        """Show mode selection for a V6 timeframe"""
        logger.info(f"[DualOrderMenuHandler] Showing mode selection for V6 {timeframe}")
        
        current_mode = self._get_dual_order_config("v6_price_action", timeframe)
        
        text = f"""📋 <b>V6 {timeframe} - SELECT ORDER MODE</b>
━━━━━━━━━━━━━━━━━━━━━━━━

Current Mode: <b>{self.ORDER_MODE_LABELS.get(current_mode, 'Dual Orders')}</b>

Select new mode:"""
        
        keyboard = []
        for mode in self.ORDER_MODES:
            is_current = mode == current_mode
            label = self.ORDER_MODE_LABELS.get(mode, mode)
            emoji = "✅" if is_current else "⚪"
            keyboard.append([{"text": f"{emoji} {label}", "callback_data": f"dual_set_v6_{timeframe}_{mode}"}])
        
        keyboard.append([
            {"text": "◀️ Back", "callback_data": "dual_select_v6"},
            {"text": "🏠 Main Menu", "callback_data": "menu_main"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_plugin_dual_order_config(self, plugin: str, user_id: int, message_id: int = None):
        """Show dual order configuration for a specific plugin"""
        logger.info(f"[DualOrderMenuHandler] Showing config for plugin {plugin}")
        
        plugin_config = self._get_dual_order_config(plugin)
        enabled = plugin_config.get("enabled", False)
        mode = plugin_config.get("mode", "both")
        order_a = plugin_config.get("order_a", {})
        order_b = plugin_config.get("order_b", {})
        
        # Format plugin name
        plugin_names = {
            "v3_logic1": "V3 Logic 1 (5m)",
            "v3_logic2": "V3 Logic 2 (15m)",
            "v3_logic3": "V3 Logic 3 (1h)",
            "v6_15m": "V6 15M",
            "v6_30m": "V6 30M",
            "v6_1h": "V6 1H",
            "v6_4h": "V6 4H"
        }
        plugin_name = plugin_names.get(plugin, plugin)
        
        text = f"""💎 <b>DUAL ORDER: {plugin_name}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🔌 <b>Status:</b> {'✅ ENABLED' if enabled else '❌ DISABLED'}
📋 <b>Mode:</b> {self.ORDER_MODE_LABELS.get(mode, mode)}

📊 <b>Order A Configuration:</b>
  • Lot Multiplier: {order_a.get('lot_multiplier', 1.0)}x
  • TP: {order_a.get('tp_pips', 20)} pips
  • SL: {order_a.get('sl_pips', 15)} pips

📊 <b>Order B Configuration:</b>
  • Lot Multiplier: {order_b.get('lot_multiplier', 0.5)}x
  • TP: {order_b.get('tp_pips', 40)} pips
  • SL: {order_b.get('sl_pips', 15)} pips

━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # Build keyboard
        keyboard = [
            # Toggle and mode
            [
                {"text": f"{'✅' if enabled else '❌'} Toggle", "callback_data": f"dual_toggle_{plugin}"},
                {"text": "📋 Change Mode", "callback_data": f"dual_mode_{plugin}"}
            ],
            # Order A config
            [
                {"text": "⚙️ Order A Settings", "callback_data": f"dual_order_a_{plugin}"}
            ],
            # Order B config
            [
                {"text": "⚙️ Order B Settings", "callback_data": f"dual_order_b_{plugin}"}
            ],
            # Navigation
            [
                {"text": "◀️ Back", "callback_data": "menu_dual_order"},
                {"text": "🏠 Main Menu", "callback_data": "menu_main"}
            ]
        ]
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_mode_selection(self, plugin: str, user_id: int, message_id: int = None):
        """Show mode selection for a plugin"""
        plugin_config = self._get_dual_order_config(plugin)
        current_mode = plugin_config.get("mode", "both")
        
        text = f"""📋 <b>SELECT ORDER MODE</b>
━━━━━━━━━━━━━━━━━━━━━━━━

Current Mode: <b>{self.ORDER_MODE_LABELS.get(current_mode, current_mode)}</b>

Select new mode:"""
        
        keyboard = []
        for mode in self.ORDER_MODES:
            is_current = mode == current_mode
            label = self.ORDER_MODE_LABELS.get(mode, mode)
            emoji = "✅" if is_current else "⚪"
            keyboard.append([{"text": f"{emoji} {label}", "callback_data": f"dual_set_mode_{plugin}_{mode}"}])
        
        keyboard.append([
            {"text": "◀️ Back", "callback_data": f"dual_config_{plugin}"},
            {"text": "🏠 Main Menu", "callback_data": "menu_main"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    # =========================================================================
    # CALLBACK HANDLER
    # =========================================================================
    
    def handle_callback(self, callback_data: str, user_id: int, message_id: int = None) -> bool:
        """Handle dual order menu callback"""
        logger.info(f"[DualOrderMenuHandler] Handling callback: {callback_data}")
        
        if callback_data == "menu_dual_order" or callback_data == "menu_dual_order_main":
            self.show_dual_order_menu(user_id, message_id)
            return True
        
        # Plugin selection
        if callback_data == "dual_select_v3":
            self.show_v3_logic_selection(user_id, message_id)
            return True
        
        if callback_data == "dual_select_v6":
            self.show_v6_timeframe_selection(user_id, message_id)
            return True
        
        # V3 logic selection
        if callback_data.startswith("dual_v3_"):
            logic = callback_data.replace("dual_v3_", "")
            if logic in self.V3_LOGICS:
                self.show_v3_logic_mode_selection(logic, user_id, message_id)
                return True
        
        # V6 timeframe selection
        if callback_data.startswith("dual_v6_"):
            timeframe = callback_data.replace("dual_v6_", "")
            if timeframe in self.V6_TIMEFRAMES:
                self.show_v6_timeframe_mode_selection(timeframe, user_id, message_id)
                return True
        
        # Set V3 logic mode
        if callback_data.startswith("dual_set_v3_"):
            parts = callback_data.replace("dual_set_v3_", "").rsplit("_", 1)
            if len(parts) == 2:
                logic, mode = parts
                self._set_v3_logic_mode(logic, mode)
                self.show_v3_logic_selection(user_id, message_id)
                return True
        
        # Set V6 timeframe mode
        if callback_data.startswith("dual_set_v6_"):
            parts = callback_data.replace("dual_set_v6_", "").rsplit("_", 1)
            if len(parts) == 2:
                timeframe, mode = parts
                self._set_v6_timeframe_mode(timeframe, mode)
                self.show_v6_timeframe_selection(user_id, message_id)
                return True
        
        # Toggle system/V3/V6
        if callback_data == "dual_toggle_system":
            self._toggle_system()
            self.show_dual_order_menu(user_id, message_id)
            return True
        
        if callback_data == "dual_toggle_v3":
            self._toggle_v3()
            self.show_v3_logic_selection(user_id, message_id)
            return True
        
        if callback_data == "dual_toggle_v6":
            self._toggle_v6()
            self.show_v6_timeframe_selection(user_id, message_id)
            return True
        
        if callback_data.startswith("dual_set_mode_"):
            parts = callback_data.replace("dual_set_mode_", "").rsplit("_", 1)
            if len(parts) == 2:
                plugin, mode = parts
                self._set_mode(plugin, mode)
                self.show_plugin_dual_order_config(plugin, user_id, message_id)
            return True
        
        return False
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _toggle_system(self):
        """Toggle system enabled state"""
        if "dual_order_config" not in self._config:
            self._config["dual_order_config"] = {"enabled": False}
        current = self._config["dual_order_config"].get("enabled", True)
        self._config["dual_order_config"]["enabled"] = not current
        self._save_config()
        logger.info(f"[DualOrderMenuHandler] Toggled system: {not current}")
    
    def _toggle_v3(self):
        """Toggle V3 enabled state"""
        if "dual_order_config" not in self._config:
            self._config["dual_order_config"] = {}
        if "v3_combined" not in self._config["dual_order_config"]:
            self._config["dual_order_config"]["v3_combined"] = {"enabled": False}
        current = self._config["dual_order_config"]["v3_combined"].get("enabled", True)
        self._config["dual_order_config"]["v3_combined"]["enabled"] = not current
        self._save_config()
        logger.info(f"[DualOrderMenuHandler] Toggled V3: {not current}")
    
    def _toggle_v6(self):
        """Toggle V6 enabled state"""
        if "dual_order_config" not in self._config:
            self._config["dual_order_config"] = {}
        if "v6_price_action" not in self._config["dual_order_config"]:
            self._config["dual_order_config"]["v6_price_action"] = {"enabled": False}
        current = self._config["dual_order_config"]["v6_price_action"].get("enabled", True)
        self._config["dual_order_config"]["v6_price_action"]["enabled"] = not current
        self._save_config()
        logger.info(f"[DualOrderMenuHandler] Toggled V6: {not current}")
    
    def _set_v3_logic_mode(self, logic: str, mode: str):
        """Set order mode for a V3 logic"""
        if "dual_order_config" not in self._config:
            self._config["dual_order_config"] = {}
        if "v3_combined" not in self._config["dual_order_config"]:
            self._config["dual_order_config"]["v3_combined"] = {}
        if "per_logic_routing" not in self._config["dual_order_config"]["v3_combined"]:
            self._config["dual_order_config"]["v3_combined"]["per_logic_routing"] = {}
        
        self._config["dual_order_config"]["v3_combined"]["per_logic_routing"][logic] = mode
        self._save_config()
        logger.info(f"[DualOrderMenuHandler] Set V3 {logic} mode to {mode}")
    
    def _set_v6_timeframe_mode(self, timeframe: str, mode: str):
        """Set order mode for a V6 timeframe"""
        if "dual_order_config" not in self._config:
            self._config["dual_order_config"] = {}
        if "v6_price_action" not in self._config["dual_order_config"]:
            self._config["dual_order_config"]["v6_price_action"] = {}
        if "per_timeframe_routing" not in self._config["dual_order_config"]["v6_price_action"]:
            self._config["dual_order_config"]["v6_price_action"]["per_timeframe_routing"] = {}
        
        self._config["dual_order_config"]["v6_price_action"]["per_timeframe_routing"][timeframe] = mode
        self._save_config()
        logger.info(f"[DualOrderMenuHandler] Set V6 {timeframe} mode to {mode}")
    
    def _toggle_plugin(self, plugin: str):
        """Toggle plugin enabled state and save config"""
        if plugin == "system":
            if "dual_order_system" not in self._config:
                self._config["dual_order_system"] = {"enabled": False, "plugins": {}}
            current = self._config["dual_order_system"].get("enabled", False)
            self._config["dual_order_system"]["enabled"] = not current
        else:
            if "dual_order_system" not in self._config:
                self._config["dual_order_system"] = {"enabled": True, "plugins": {}}
            if "plugins" not in self._config["dual_order_system"]:
                self._config["dual_order_system"]["plugins"] = {}
            if plugin not in self._config["dual_order_system"]["plugins"]:
                self._config["dual_order_system"]["plugins"][plugin] = {"enabled": False}
            current = self._config["dual_order_system"]["plugins"][plugin].get("enabled", False)
            self._config["dual_order_system"]["plugins"][plugin]["enabled"] = not current
        
        # Save config to file
        self._save_config()
        logger.info(f"[DualOrderMenuHandler] Toggled {plugin}: {not current}")
    
    def _set_mode(self, plugin: str, mode: str):
        """Set order mode for a plugin and save config"""
        if "dual_order_system" not in self._config:
            self._config["dual_order_system"] = {"enabled": True, "plugins": {}}
        if "plugins" not in self._config["dual_order_system"]:
            self._config["dual_order_system"]["plugins"] = {}
        if plugin not in self._config["dual_order_system"]["plugins"]:
            self._config["dual_order_system"]["plugins"][plugin] = {"enabled": True}
        self._config["dual_order_system"]["plugins"][plugin]["mode"] = mode
        
        # Save config to file
        self._save_config()
        logger.info(f"[DualOrderMenuHandler] Set mode for {plugin}: {mode}")


class ReentryMenuHandler:
    """
    Menu Handler for Re-entry System per-plugin configuration.
    
    Provides:
    - TP Continuation configuration per plugin
    - SL Hunt Recovery configuration per plugin
    - Exit Continuation configuration per plugin
    - Cooldown and chain limit settings
    """
    
    # Re-entry types
    REENTRY_TYPES = ["tp_continuation", "sl_hunt_recovery", "exit_continuation"]
    REENTRY_TYPE_LABELS = {
        "tp_continuation": "🎯 TP Continuation",
        "sl_hunt_recovery": "🛡️ SL Hunt Recovery",
        "exit_continuation": "🔄 Exit Continuation"
    }
    
    # V3 Logics (same as DualOrderMenuHandler)
    V3_LOGICS = ["LOGIC1", "LOGIC2", "LOGIC3"]
    V3_LOGIC_LABELS = {
        "LOGIC1": "🧠 V3 Logic 1 (5m)",
        "LOGIC2": "🧠 V3 Logic 2 (15m)",
        "LOGIC3": "🧠 V3 Logic 3 (1h)"
    }
    
    # V6 Timeframes (same as DualOrderMenuHandler)
    V6_TIMEFRAMES = ["1M", "5M", "15M", "1H", "4H"]
    V6_TIMEFRAME_LABELS = {
        "1M": "📊 V6 1M",
        "5M": "📊 V6 5M",
        "15M": "📊 V6 15M",
        "1H": "📊 V6 1H",
        "4H": "📊 V6 4H"
    }
    
    def __init__(self, telegram_bot, config: Dict[str, Any] = None):
        """
        Initialize ReentryMenuHandler.
        
        Args:
            telegram_bot: Telegram bot instance
            config: Bot configuration dictionary (Config object or dict)
        """
        self._bot = telegram_bot
        # Support both Config object and dict
        if hasattr(telegram_bot, 'config'):
            self._config_obj = telegram_bot.config  # Config object with save_config()
            self._config = telegram_bot.config.config if hasattr(telegram_bot.config, 'config') else telegram_bot.config
        else:
            self._config_obj = None
            self._config = config or {}
        logger.info("[ReentryMenuHandler] Initialized (Per-Plugin Version)")
    
    def set_config(self, config: Dict[str, Any]):
        """Update configuration reference"""
        if hasattr(config, 'config'):
            self._config_obj = config
            self._config = config.config
        else:
            self._config = config
    
    def _save_config(self):
        """Save config to file"""
        if self._config_obj and hasattr(self._config_obj, 'save_config'):
            self._config_obj.save_config()
            logger.info("[ReentryMenuHandler] Config saved to file")
    
    def _get_reentry_config(self, plugin: str = None, context: str = None, feature: str = None) -> Dict[str, Any]:
        """
        Get re-entry configuration.
        
        Args:
            plugin: "v3_combined" or "v6_price_action"
            context: For V3: "LOGIC1", "LOGIC2", "LOGIC3"
                    For V6: "1M", "5M", "15M", "1H", "4H"
            feature: "tp_continuation", "sl_hunt_recovery", "exit_continuation"
        
        Returns:
            Dict with config or bool if feature specified
        """
        if "re_entry_config" not in self._config:
            self._config["re_entry_config"] = {
                "enabled": True,
                "global": {
                    "tp_reentry_enabled": True,
                    "sl_hunt_reentry_enabled": True,
                    "exit_continuation_enabled": True
                },
                "per_plugin": {
                    "v3_combined": {
                        "enabled": True,
                        "per_logic_routing": {
                            "LOGIC1": {
                                "tp_continuation": {"enabled": True},
                                "sl_hunt_recovery": {"enabled": True},
                                "exit_continuation": {"enabled": True}
                            },
                            "LOGIC2": {
                                "tp_continuation": {"enabled": True},
                                "sl_hunt_recovery": {"enabled": True},
                                "exit_continuation": {"enabled": True}
                            },
                            "LOGIC3": {
                                "tp_continuation": {"enabled": True},
                                "sl_hunt_recovery": {"enabled": False},
                                "exit_continuation": {"enabled": True}
                            }
                        }
                    },
                    "v6_price_action": {
                        "enabled": True,
                        "per_timeframe_routing": {
                            "1M": {
                                "tp_continuation": {"enabled": False},
                                "sl_hunt_recovery": {"enabled": True},
                                "exit_continuation": {"enabled": False}
                            },
                            "5M": {
                                "tp_continuation": {"enabled": True},
                                "sl_hunt_recovery": {"enabled": True},
                                "exit_continuation": {"enabled": True}
                            },
                            "15M": {
                                "tp_continuation": {"enabled": True},
                                "sl_hunt_recovery": {"enabled": False},
                                "exit_continuation": {"enabled": True}
                            },
                            "1H": {
                                "tp_continuation": {"enabled": True},
                                "sl_hunt_recovery": {"enabled": False},
                                "exit_continuation": {"enabled": True}
                            },
                            "4H": {
                                "tp_continuation": {"enabled": True},
                                "sl_hunt_recovery": {"enabled": False},
                                "exit_continuation": {"enabled": False}
                            }
                        }
                    }
                }
            }
        
        reentry_config = self._config["re_entry_config"]
        
        if plugin and context and feature:
            # Get specific feature status for timeframe/logic
            if plugin == "v3_combined":
                return reentry_config.get("per_plugin", {}).get("v3_combined", {}).get("per_logic_routing", {}).get(context, {}).get(feature, {}).get("enabled", True)
            elif plugin == "v6_price_action":
                return reentry_config.get("per_plugin", {}).get("v6_price_action", {}).get("per_timeframe_routing", {}).get(context, {}).get(feature, {}).get("enabled", True)
        elif plugin and context:
            # Get all features for specific timeframe/logic
            if plugin == "v3_combined":
                return reentry_config.get("per_plugin", {}).get("v3_combined", {}).get("per_logic_routing", {}).get(context, {})
            elif plugin == "v6_price_action":
                return reentry_config.get("per_plugin", {}).get("v6_price_action", {}).get("per_timeframe_routing", {}).get(context, {})
        elif plugin:
            # Get plugin-level config
            return reentry_config.get("per_plugin", {}).get(plugin, {})
        
        return reentry_config
    
    def _send_message(self, text: str, reply_markup: Dict = None, message_id: int = None):
        """Send or edit message"""
        try:
            if message_id and hasattr(self._bot, 'edit_message'):
                self._bot.edit_message(text, message_id, reply_markup)
            elif hasattr(self._bot, 'send_message_with_keyboard') and reply_markup:
                self._bot.send_message_with_keyboard(text, reply_markup)
            elif hasattr(self._bot, 'send_message'):
                self._bot.send_message(text)
        except Exception as e:
            logger.error(f"[ReentryMenuHandler] Error sending message: {e}")
    
    # =========================================================================
    # MAIN RE-ENTRY MENU
    # =========================================================================
    
    def show_reentry_menu(self, user_id: int, message_id: int = None):
        """Show main re-entry plugin selection menu"""
        logger.info(f"[ReentryMenuHandler] Showing re-entry menu for user {user_id}")
        
        reentry_config = self._get_reentry_config()
        system_enabled = reentry_config.get("enabled", True)
        
        text = f"""🔄 <b>RE-ENTRY SYSTEM MANAGEMENT</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🔌 <b>System Status:</b> {'✅ ENABLED' if system_enabled else '❌ DISABLED'}

📊 <b>Description:</b>
Configure re-entry behavior for different scenarios:
• <b>🎯 TP Continuation:</b> Re-enter after TP hit
• <b>🛡️ SL Hunt Recovery:</b> Recover from stop hunt
• <b>🔄 Exit Continuation:</b> Re-enter after manual exit

━━━━━━━━━━━━━━━━━━━━━━━━
<i>Select a plugin to configure:</i>"""
        
        # Build keyboard with plugin options
        keyboard = [
            # System toggle
            [
                {"text": f"{'✅' if system_enabled else '❌'} Toggle System", "callback_data": "reentry_toggle_system"}
            ],
            # Plugin selection
            [
                {"text": "🧠 V3 Combined Logic", "callback_data": "reentry_select_v3"},
                {"text": "📊 V6 Price Action", "callback_data": "reentry_select_v6"}
            ],
            # Navigation
            [
                {"text": "← Back to Orders Menu", "callback_data": "menu_orders"},
                {"text": "🏠 Main Menu", "callback_data": "menu_main"}
            ]
        ]
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v3_logic_reentry_selection(self, user_id: int, message_id: int = None):
        """Show V3 logic selection for re-entry config"""
        logger.info(f"[ReentryMenuHandler] Showing V3 logic selection for user {user_id}")
        
        v3_config = self._get_reentry_config("v3_combined")
        v3_enabled = v3_config.get("enabled", True)
        routing = v3_config.get("per_logic_routing", {})
        
        # Build status summary
        status_lines = []
        for logic in self.V3_LOGICS:
            logic_config = routing.get(logic, {})
            tp_on = logic_config.get("tp_continuation", {}).get("enabled", True)
            sl_on = logic_config.get("sl_hunt_recovery", {}).get("enabled", True)
            exit_on = logic_config.get("exit_continuation", {}).get("enabled", True)
            count = sum([tp_on, sl_on, exit_on])
            status_lines.append(f"• {logic}: {count}/3 enabled")
        
        text = f"""🧠 <b>V3 COMBINED LOGIC - RE-ENTRY CONFIG</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🔌 <b>V3 Status:</b> {'✅ ENABLED' if v3_enabled else '❌ DISABLED'}

📊 <b>Current Status:</b>
{chr(10).join(status_lines)}

━━━━━━━━━━━━━━━━━━━━━━━━
<i>Select a logic to configure:</i>"""
        
        keyboard = []
        
        # V3 enable/disable
        keyboard.append([
            {"text": f"{'✅' if v3_enabled else '❌'} Toggle V3", "callback_data": "reentry_toggle_v3"}
        ])
        
        # Logic selection
        for logic in self.V3_LOGICS:
            logic_config = routing.get(logic, {})
            tp_on = logic_config.get("tp_continuation", {}).get("enabled", True)
            sl_on = logic_config.get("sl_hunt_recovery", {}).get("enabled", True)
            exit_on = logic_config.get("exit_continuation", {}).get("enabled", True)
            count = sum([tp_on, sl_on, exit_on])
            status = f"{count}/3"
            keyboard.append([
                {"text": f"{self.V3_LOGIC_LABELS[logic]} [{status}]", "callback_data": f"reentry_v3_{logic}"}
            ])
        
        # Navigation
        keyboard.append([
            {"text": "◀️ Back", "callback_data": "menu_reentry_main"},
            {"text": "🏠 Main Menu", "callback_data": "menu_main"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v6_timeframe_reentry_selection(self, user_id: int, message_id: int = None):
        """Show V6 timeframe selection for re-entry config"""
        logger.info(f"[ReentryMenuHandler] Showing V6 timeframe selection for user {user_id}")
        
        v6_config = self._get_reentry_config("v6_price_action")
        v6_enabled = v6_config.get("enabled", True)
        routing = v6_config.get("per_timeframe_routing", {})
        
        # Build status summary
        status_lines = []
        for tf in self.V6_TIMEFRAMES:
            tf_config = routing.get(tf, {})
            tp_on = tf_config.get("tp_continuation", {}).get("enabled", True)
            sl_on = tf_config.get("sl_hunt_recovery", {}).get("enabled", True)
            exit_on = tf_config.get("exit_continuation", {}).get("enabled", True)
            count = sum([tp_on, sl_on, exit_on])
            status_lines.append(f"• {tf}: {count}/3 enabled")
        
        text = f"""📊 <b>V6 PRICE ACTION - RE-ENTRY CONFIG</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🔌 <b>V6 Status:</b> {'✅ ENABLED' if v6_enabled else '❌ DISABLED'}

📊 <b>Current Status:</b>
{chr(10).join(status_lines)}

━━━━━━━━━━━━━━━━━━━━━━━━
<i>Select a timeframe to configure:</i>"""
        
        keyboard = []
        
        # V6 enable/disable
        keyboard.append([
            {"text": f"{'✅' if v6_enabled else '❌'} Toggle V6", "callback_data": "reentry_toggle_v6"}
        ])
        
        # Timeframe selection (2 per row)
        row = []
        for idx, tf in enumerate(self.V6_TIMEFRAMES):
            tf_config = routing.get(tf, {})
            tp_on = tf_config.get("tp_continuation", {}).get("enabled", True)
            sl_on = tf_config.get("sl_hunt_recovery", {}).get("enabled", True)
            exit_on = tf_config.get("exit_continuation", {}).get("enabled", True)
            count = sum([tp_on, sl_on, exit_on])
            row.append({"text": f"{tf} [{count}/3]", "callback_data": f"reentry_v6_{tf}"})
            if len(row) == 2 or idx == len(self.V6_TIMEFRAMES) - 1:
                keyboard.append(row)
                row = []
        
        # Navigation
        keyboard.append([
            {"text": "◀️ Back", "callback_data": "menu_reentry_main"},
            {"text": "🏠 Main Menu", "callback_data": "menu_main"}
        ])
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v3_logic_feature_config(self, logic: str, user_id: int, message_id: int = None):
        """Show re-entry feature toggles for a specific V3 logic"""
        logger.info(f"[ReentryMenuHandler] Showing V3 {logic} feature config")
        
        # Get feature states
        tp_enabled = self._get_reentry_config("v3_combined", logic, "tp_continuation")
        sl_enabled = self._get_reentry_config("v3_combined", logic, "sl_hunt_recovery")
        exit_enabled = self._get_reentry_config("v3_combined", logic, "exit_continuation")
        
        # Count enabled features
        enabled_count = sum([tp_enabled, sl_enabled, exit_enabled])
        
        text = f"""🔄 <b>RE-ENTRY: V3 {logic}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

📊 <b>Features Active:</b> {enabled_count}/3

💡 <b>Click to toggle ON/OFF:</b>

🎯 <b>TP Continuation:</b> {'✅ ON' if tp_enabled else '❌ OFF'}
  Re-enter after TP hit to continue trend

🛡️ <b>SL Hunt Recovery:</b> {'✅ ON' if sl_enabled else '❌ OFF'}
  Recover from stop hunt spikes

🔄 <b>Exit Continuation:</b> {'✅ ON' if exit_enabled else '❌ OFF'}
  Re-enter after manual exit

━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # Build keyboard
        keyboard = [
            # Feature toggles
            [
                {"text": f"{'🎯 ✅' if tp_enabled else '🎯 ❌'} TP Continuation", 
                 "callback_data": f"reentry_toggle_v3_{logic}_tp_continuation"}
            ],
            [
                {"text": f"{'🛡️ ✅' if sl_enabled else '🛡️ ❌'} SL Hunt Recovery", 
                 "callback_data": f"reentry_toggle_v3_{logic}_sl_hunt_recovery"}
            ],
            [
                {"text": f"{'🔄 ✅' if exit_enabled else '🔄 ❌'} Exit Continuation", 
                 "callback_data": f"reentry_toggle_v3_{logic}_exit_continuation"}
            ],
            # Navigation
            [
                {"text": "◀️ Back to V3 Selection", "callback_data": "reentry_select_v3"},
                {"text": "🏠 Main Menu", "callback_data": "menu_main"}
            ]
        ]
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    def show_v6_timeframe_feature_config(self, timeframe: str, user_id: int, message_id: int = None):
        """Show re-entry feature toggles for a specific V6 timeframe"""
        logger.info(f"[ReentryMenuHandler] Showing V6 {timeframe} feature config")
        
        # Get feature states
        tp_enabled = self._get_reentry_config("v6_price_action", timeframe, "tp_continuation")
        sl_enabled = self._get_reentry_config("v6_price_action", timeframe, "sl_hunt_recovery")
        exit_enabled = self._get_reentry_config("v6_price_action", timeframe, "exit_continuation")
        
        # Count enabled features
        enabled_count = sum([tp_enabled, sl_enabled, exit_enabled])
        
        # Timeframe icons
        tf_icons = {
            "1M": "⚡",
            "5M": "🔥",
            "15M": "📊",
            "1H": "⏰",
            "4H": "🌊"
        }
        icon = tf_icons.get(timeframe, "📈")
        
        text = f"""🔄 <b>RE-ENTRY: V6 {icon} {timeframe}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

📊 <b>Features Active:</b> {enabled_count}/3

💡 <b>Click to toggle ON/OFF:</b>

🎯 <b>TP Continuation:</b> {'✅ ON' if tp_enabled else '❌ OFF'}
  Re-enter after TP hit to continue trend

🛡️ <b>SL Hunt Recovery:</b> {'✅ ON' if sl_enabled else '❌ OFF'}
  Recover from stop hunt spikes

🔄 <b>Exit Continuation:</b> {'✅ ON' if exit_enabled else '❌ OFF'}
  Re-enter after manual exit

━━━━━━━━━━━━━━━━━━━━━━━━"""
        
        # Build keyboard
        keyboard = [
            # Feature toggles
            [
                {"text": f"{'🎯 ✅' if tp_enabled else '🎯 ❌'} TP Continuation", 
                 "callback_data": f"reentry_toggle_v6_{timeframe}_tp_continuation"}
            ],
            [
                {"text": f"{'🛡️ ✅' if sl_enabled else '🛡️ ❌'} SL Hunt Recovery", 
                 "callback_data": f"reentry_toggle_v6_{timeframe}_sl_hunt_recovery"}
            ],
            [
                {"text": f"{'🔄 ✅' if exit_enabled else '🔄 ❌'} Exit Continuation", 
                 "callback_data": f"reentry_toggle_v6_{timeframe}_exit_continuation"}
            ],
            # Navigation
            [
                {"text": "◀️ Back to V6 Selection", "callback_data": "reentry_select_v6"},
                {"text": "🏠 Main Menu", "callback_data": "menu_main"}
            ]
        ]
        
        reply_markup = {"inline_keyboard": keyboard}
        self._send_message(text, reply_markup, message_id)
    
    # =========================================================================
    # CALLBACK HANDLER
    # =========================================================================
    
    def handle_callback(self, callback_data: str, user_id: int, message_id: int = None) -> bool:
        """Handle re-entry menu callback"""
        logger.info(f"[ReentryMenuHandler] Handling callback: {callback_data}")
        
        # Main menu
        if callback_data == "menu_reentry" or callback_data == "menu_reentry_main":
            self.show_reentry_menu(user_id, message_id)
            return True
        
        # Plugin selection
        if callback_data == "reentry_select_v3":
            self.show_v3_logic_reentry_selection(user_id, message_id)
            return True
        
        if callback_data == "reentry_select_v6":
            self.show_v6_timeframe_reentry_selection(user_id, message_id)
            return True
        
        # V3 logic selection -> feature config
        if callback_data.startswith("reentry_v3_"):
            logic = callback_data.replace("reentry_v3_", "")
            if logic in self.V3_LOGICS:
                self.show_v3_logic_feature_config(logic, user_id, message_id)
                return True
        
        # V6 timeframe selection -> feature config
        if callback_data.startswith("reentry_v6_"):
            timeframe = callback_data.replace("reentry_v6_", "")
            if timeframe in self.V6_TIMEFRAMES:
                self.show_v6_timeframe_feature_config(timeframe, user_id, message_id)
                return True
        
        # V3 feature toggles
        if callback_data.startswith("reentry_toggle_v3_"):
            # Format: reentry_toggle_v3_LOGIC1_tp_continuation
            parts = callback_data.replace("reentry_toggle_v3_", "").split("_")
            if len(parts) >= 2:
                logic = parts[0]  # LOGIC1, LOGIC2, LOGIC3
                feature = "_".join(parts[1:])  # tp_continuation, sl_hunt_recovery, exit_continuation
                self._toggle_v3_feature(logic, feature)
                self.show_v3_logic_feature_config(logic, user_id, message_id)
                return True
        
        # V6 feature toggles
        if callback_data.startswith("reentry_toggle_v6_"):
            # Format: reentry_toggle_v6_15M_tp_continuation
            parts = callback_data.replace("reentry_toggle_v6_", "").split("_")
            if len(parts) >= 2:
                timeframe = parts[0]  # 1M, 5M, 15M, 1H, 4H
                feature = "_".join(parts[1:])  # tp_continuation, sl_hunt_recovery, exit_continuation
                self._toggle_v6_feature(timeframe, feature)
                self.show_v6_timeframe_feature_config(timeframe, user_id, message_id)
                return True
        
        # System toggles
        if callback_data == "reentry_toggle_system":
            self._toggle_system()
            self.show_reentry_menu(user_id, message_id)
            return True
        
        if callback_data == "reentry_toggle_v3":
            self._toggle_v3()
            self.show_reentry_menu(user_id, message_id)
            return True
        
        if callback_data == "reentry_toggle_v6":
            self._toggle_v6()
            self.show_reentry_menu(user_id, message_id)
            return True
        
        return False
    
    def _toggle_system(self):
        """Toggle re-entry system on/off"""
        if "re_entry_config" not in self._config:
            self._config["re_entry_config"] = {"enabled": False}
        current = self._config["re_entry_config"].get("enabled", False)
        self._config["re_entry_config"]["enabled"] = not current
        self._save_config()
        logger.info(f"[ReentryMenuHandler] Toggled system: {not current}")
    
    def _toggle_v3(self):
        """Toggle V3 re-entry on/off"""
        if "re_entry_config" not in self._config:
            self._config["re_entry_config"] = {"per_plugin": {}}
        if "per_plugin" not in self._config["re_entry_config"]:
            self._config["re_entry_config"]["per_plugin"] = {}
        if "v3_combined" not in self._config["re_entry_config"]["per_plugin"]:
            self._config["re_entry_config"]["per_plugin"]["v3_combined"] = {"enabled": False}
        current = self._config["re_entry_config"]["per_plugin"]["v3_combined"].get("enabled", False)
        self._config["re_entry_config"]["per_plugin"]["v3_combined"]["enabled"] = not current
        self._save_config()
        logger.info(f"[ReentryMenuHandler] Toggled V3: {not current}")
    
    def _toggle_v6(self):
        """Toggle V6 re-entry on/off"""
        if "re_entry_config" not in self._config:
            self._config["re_entry_config"] = {"per_plugin": {}}
        if "per_plugin" not in self._config["re_entry_config"]:
            self._config["re_entry_config"]["per_plugin"] = {}
        if "v6_price_action" not in self._config["re_entry_config"]["per_plugin"]:
            self._config["re_entry_config"]["per_plugin"]["v6_price_action"] = {"enabled": False}
        current = self._config["re_entry_config"]["per_plugin"]["v6_price_action"].get("enabled", False)
        self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["enabled"] = not current
        self._save_config()
        logger.info(f"[ReentryMenuHandler] Toggled V6: {not current}")
    
    def _toggle_v3_feature(self, logic: str, feature: str):
        """Toggle a V3 logic re-entry feature"""
        # Initialize config structure
        if "re_entry_config" not in self._config:
            self._config["re_entry_config"] = {"per_plugin": {}}
        if "per_plugin" not in self._config["re_entry_config"]:
            self._config["re_entry_config"]["per_plugin"] = {}
        if "v3_combined" not in self._config["re_entry_config"]["per_plugin"]:
            self._config["re_entry_config"]["per_plugin"]["v3_combined"] = {"per_logic_routing": {}}
        if "per_logic_routing" not in self._config["re_entry_config"]["per_plugin"]["v3_combined"]:
            self._config["re_entry_config"]["per_plugin"]["v3_combined"]["per_logic_routing"] = {}
        if logic not in self._config["re_entry_config"]["per_plugin"]["v3_combined"]["per_logic_routing"]:
            self._config["re_entry_config"]["per_plugin"]["v3_combined"]["per_logic_routing"][logic] = {}
        if feature not in self._config["re_entry_config"]["per_plugin"]["v3_combined"]["per_logic_routing"][logic]:
            self._config["re_entry_config"]["per_plugin"]["v3_combined"]["per_logic_routing"][logic][feature] = {"enabled": False}
        
        # Toggle
        current = self._config["re_entry_config"]["per_plugin"]["v3_combined"]["per_logic_routing"][logic][feature].get("enabled", False)
        self._config["re_entry_config"]["per_plugin"]["v3_combined"]["per_logic_routing"][logic][feature]["enabled"] = not current
        self._save_config()
        logger.info(f"[ReentryMenuHandler] Toggled V3 {logic} {feature}: {not current}")
    
    def _toggle_v6_feature(self, timeframe: str, feature: str):
        """Toggle a V6 timeframe re-entry feature"""
        # Initialize config structure
        if "re_entry_config" not in self._config:
            self._config["re_entry_config"] = {"per_plugin": {}}
        if "per_plugin" not in self._config["re_entry_config"]:
            self._config["re_entry_config"]["per_plugin"] = {}
        if "v6_price_action" not in self._config["re_entry_config"]["per_plugin"]:
            self._config["re_entry_config"]["per_plugin"]["v6_price_action"] = {"per_timeframe_routing": {}}
        if "per_timeframe_routing" not in self._config["re_entry_config"]["per_plugin"]["v6_price_action"]:
            self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["per_timeframe_routing"] = {}
        if timeframe not in self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["per_timeframe_routing"]:
            self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["per_timeframe_routing"][timeframe] = {}
        if feature not in self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["per_timeframe_routing"][timeframe]:
            self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["per_timeframe_routing"][timeframe][feature] = {"enabled": False}
        
        # Toggle
        current = self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["per_timeframe_routing"][timeframe][feature].get("enabled", False)
        self._config["re_entry_config"]["per_plugin"]["v6_price_action"]["per_timeframe_routing"][timeframe][feature]["enabled"] = not current
        self._save_config()
        logger.info(f"[ReentryMenuHandler] Toggled V6 {timeframe} {feature}: {not current}")
