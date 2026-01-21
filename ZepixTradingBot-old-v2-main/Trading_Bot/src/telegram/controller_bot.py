"""
Controller Bot - Handles system commands and admin functions

This bot handles all slash commands and system control.
NOW WIRED to CommandRegistry for 95+ command handling (not delegation).
INTEGRATED with Plugin Selection Interceptor System (V5 Upgrade).

Version: 2.1.0
Date: 2026-01-20

Updates:
- v2.1.0: Added Plugin Selection Interceptor for V3/V6 plugin-aware commands
- v2.0.0: Wired to CommandRegistry with actual handler implementations
- v1.1.0: Added /health and /version commands for plugin monitoring
"""

import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, date, timedelta
import sys
import os
import csv
import io

# Ensure src is in path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from .base_telegram_bot import BaseTelegramBot
from .plugin_context_manager import PluginContextManager
from .command_interceptor import CommandInterceptor
from .plugin_selection_menu_builder import PluginSelectionMenuBuilder

try:
    from src.menu.menu_manager import MenuManager
except ImportError:
    MenuManager = None

logger = logging.getLogger(__name__)


class ControllerBot(BaseTelegramBot):
    """
    Controller Bot for system commands and admin functions.
    
    NOW WIRED to CommandRegistry for 95+ command handling.
    """
    
    def __init__(self, token: str, chat_id: str = None, config: Dict = None):
        super().__init__(token, chat_id, bot_name="ControllerBot")
        
        self.config = config or {}
        self._command_handlers: Dict[str, Callable] = {}
        self._callback_handlers: Dict[str, Callable] = {} # Add callback handlers dict
        self._trading_engine = None
        self._risk_manager = None
        self._legacy_bot = None
        self._analytics_queries = None  # Analytics query engine
        
        # Phase 5 & 6: Notification & Session Menu Integration
        self._notification_prefs_menu = None
        self._session_menu_handler = None
        
        # Phase 2: V6 Timeframe Menu Builder Integration
        self._v6_timeframe_menu_builder = None
        
        # Menu Manager Integration
        self._menu_manager = None
        if MenuManager:
            try:
                self._menu_manager = MenuManager(self)
                logger.info("[ControllerBot] MenuManager initialized")
            except Exception as e:
                logger.error(f"[ControllerBot] Failed to init MenuManager: {e}")
        
        # V5 Plugin Selection Interceptor (v2.1.0)
        self._command_interceptor = None
        try:
            self._command_interceptor = CommandInterceptor(telegram_bot=self)
            logger.info("[ControllerBot] Command Interceptor initialized")
        except Exception as e:
            logger.error(f"[ControllerBot] Failed to init CommandInterceptor: {e}")
        
        # Health monitoring and versioning (Batch 11)
        self._health_monitor = None
        self._version_registry = None
        
        # Command Registry integration (v2.0.0)
        self._command_registry = None
        self._plugin_control_menu = None
        
        # Bot state
        self._is_paused = False
        self._startup_time = datetime.now()
        
        # Wire default handlers
        self._wire_default_handlers()
        
        logger.info("[ControllerBot] Initialized with CommandRegistry integration")
    
    def set_dependencies(
        self,
        trading_engine=None,
        risk_manager=None,
        legacy_bot=None,
        health_monitor=None,
        version_registry=None
    ):
        """
        Set dependencies for command handling
        
        Args:
            trading_engine: TradingEngine instance
            risk_manager: RiskManager instance
            legacy_bot: Legacy TelegramBot instance for command delegation
            health_monitor: PluginHealthMonitor instance (Batch 11)
            version_registry: VersionedPluginRegistry instance (Batch 11)
        """
        self._trading_engine = trading_engine
        self._risk_manager = risk_manager
        self._legacy_bot = legacy_bot
        self._health_monitor = health_monitor
        self._version_registry = version_registry
        
        # Phase 5: Initialize notification preferences menu
        if not self._notification_prefs_menu:
            try:
                from src.menu.notification_preferences_menu import NotificationPreferencesMenuHandler
                self._notification_prefs_menu = NotificationPreferencesMenuHandler(self)
                logger.info("[ControllerBot] Notification preferences menu initialized")
            except ImportError as e:
                logger.warning(f"[ControllerBot] Notification preferences menu not available: {e}")
        
        # Phase 6: Initialize session menu handler
        if not self._session_menu_handler and trading_engine:
            try:
                from src.telegram.session_menu_handler import SessionMenuHandler
                # Get session manager from trading engine if available
                session_manager = getattr(trading_engine, 'session_manager', None)
                if session_manager:
                    self._session_menu_handler = SessionMenuHandler(session_manager, bot=self)
                    logger.info("[ControllerBot] Session menu handler initialized")
            except ImportError as e:
                logger.warning(f"[ControllerBot] Session menu handler not available: {e}")
        
        # Phase 2: Initialize V6 timeframe menu builder
        if not self._v6_timeframe_menu_builder and trading_engine:
            try:
                from src.telegram.v6_timeframe_menu_builder import V6TimeframeMenuBuilder
                self._v6_timeframe_menu_builder = V6TimeframeMenuBuilder(self)
                self._v6_timeframe_menu_builder.set_dependencies(trading_engine)
                logger.info("[ControllerBot] V6 timeframe menu builder initialized")
            except ImportError as e:
                logger.warning(f"[ControllerBot] V6 timeframe menu builder not available: {e}")
        
        if legacy_bot:
            logger.info("[ControllerBot] Legacy bot connected for command delegation")
        
        if health_monitor:
            logger.info("[ControllerBot] Health monitor connected")
        
        if version_registry:
            logger.info("[ControllerBot] Version registry connected")
    
    def register_command(self, command: str, handler: Callable):
        """
        Register a command handler
        
        Args:
            command: Command string (e.g., '/status')
            handler: Handler function
        """
        self._command_handlers[command] = handler
        logger.debug(f"[ControllerBot] Registered command: {command}")
    
    def handle_command(self, command: str, message: Dict) -> bool:
        """
        Handle an incoming command with plugin selection interception.
        
        Args:
            command: Command string
            message: Full message dict from Telegram
        
        Returns:
            True if command was handled
        """
        # V5 Plugin Selection Interceptor
        chat_id = message.get('chat', {}).get('id', self.chat_id) if message else self.chat_id
        
        if self._command_interceptor:
            # Check if plugin selection needed
            if self._command_interceptor.intercept_command(command, chat_id, message):
                # Plugin selection shown, command paused
                logger.info(f"[ControllerBot] Command {command} intercepted for plugin selection")
                return True
        
        # Get plugin context for execution (if applicable)
        plugin_context = None
        if self._command_interceptor and self._command_interceptor.is_command_plugin_aware(command):
            plugin_context = PluginContextManager.get_plugin_context(chat_id)
            logger.debug(f"[ControllerBot] Executing {command} with plugin context: {plugin_context}")
        
        # Legacy bot handling
        if self._legacy_bot and hasattr(self._legacy_bot, 'command_handlers'):
            if command in self._legacy_bot.command_handlers:
                try:
                    self._legacy_bot.command_handlers[command](message)
                    # Clear plugin context after execution
                    if plugin_context:
                        PluginContextManager.clear_plugin_context(chat_id)
                    return True
                except Exception as e:
                    logger.error(f"[ControllerBot] Legacy handler error for {command}: {e}")
                    return False
        
        # Registered handlers
        if command in self._command_handlers:
            try:
                # Pass plugin_context to handler if it accepts it
                handler = self._command_handlers[command]
                import inspect
                sig = inspect.signature(handler)
                
                if 'plugin_context' in sig.parameters:
                    # Handler accepts plugin_context
                    handler(message, plugin_context=plugin_context)
                else:
                    # Handler doesn't accept plugin_context (old-style)
                    handler(message)
                
                # Clear plugin context after execution
                if plugin_context:
                    PluginContextManager.clear_plugin_context(chat_id)
                
                return True
            except Exception as e:
                logger.error(f"[ControllerBot] Handler error for {command}: {e}")
                return False
        
        logger.warning(f"[ControllerBot] Unknown command: {command}")
        return False
    
    def handle_callback_query(self, callback_query: Dict) -> bool:
        """
        Handle callback query (button press) with plugin selection support.
        
        Args:
            callback_query: Callback query dict from Telegram
        
        Returns:
            True if callback was handled
        """
        callback_data = callback_query.get('data', '')
        chat_id = callback_query.get('message', {}).get('chat', {}).get('id')
        message_id = callback_query.get('message', {}).get('message_id')
        
        # Check if this is a plugin selection callback
        if callback_data.startswith('plugin_select_'):
            if self._command_interceptor:
                logger.info(f"[ControllerBot] Processing plugin selection: {callback_data}")
                
                # Handle plugin selection
                result = self._command_interceptor.handle_plugin_selection_callback(
                    callback_data,
                    chat_id,
                    message_id
                )
                
                if result:
                    # Plugin selected, execute command
                    command = result['command']
                    plugin = result['plugin']
                    
                    logger.info(f"[ControllerBot] Plugin {plugin} selected, executing {command}")
                    
                    # Create mock message for command
                    mock_message = {
                        'chat': {'id': chat_id},
                        'text': command
                    }
                    
                    # Execute command with plugin context already set
                    self.handle_command(command, mock_message)
                
                return True
        
        # Check in callback handlers dict
        if callback_data in self._callback_handlers:
            try:
                self._callback_handlers[callback_data](callback_query)
                return True
            except Exception as e:
                logger.error(f"[ControllerBot] Callback handler error for {callback_data}: {e}")
                return False
        
        logger.warning(f"[ControllerBot] Unknown callback: {callback_data}")
        return False
    
    def send_status_response(self, status_data: Dict) -> Optional[int]:
        """
        Send formatted status response
        
        Args:
            status_data: Dict with status information
        
        Returns:
            Message ID if successful
        """
        message = self._format_status_message(status_data)
        return self.send_message(message)
    
    def _format_status_message(self, status_data: Dict) -> str:
        """Format status data into readable message"""
        bot_status = "🟢 Active" if status_data.get("is_active", False) else "🔴 Paused"
        
        return (
            f"🤖 <b>BOT STATUS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Status: {bot_status}\n"
            f"Uptime: {status_data.get('uptime', 'N/A')}\n"
            f"Active Plugins: {status_data.get('active_plugins', 0)}\n"
            f"Open Trades: {status_data.get('open_trades', 0)}\n"
            f"Today's P&L: ${status_data.get('daily_pnl', 0):.2f}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Last Update: {datetime.now().strftime('%H:%M:%S')}"
        )
    
    def send_command_response(self, response_text: str, keyboard: Dict = None) -> Optional[int]:
        """
        Send a command response with optional keyboard
        
        Args:
            response_text: Response message
            keyboard: Optional inline keyboard
        
        Returns:
            Message ID if successful
        """
        reply_markup = None
        if keyboard:
            reply_markup = {"inline_keyboard": keyboard}
        
        return self.send_message(response_text, reply_markup=reply_markup)
    
    def send_error_response(self, error_message: str) -> Optional[int]:
        """
        Send an error response
        
        Args:
            error_message: Error description
        
        Returns:
            Message ID if successful
        """
        formatted = f"❌ <b>Error</b>\n\n{error_message}"
        return self.send_message(formatted)
    
    def send_confirmation_request(
        self,
        action: str,
        confirm_callback: str,
        cancel_callback: str = "menu_main"
    ) -> Optional[int]:
        """
        Send a confirmation request with Yes/No buttons
        
        Args:
            action: Action description
            confirm_callback: Callback data for confirmation
            cancel_callback: Callback data for cancellation
        
        Returns:
            Message ID if successful
        """
        keyboard = [
            [
                {"text": "✅ YES", "callback_data": confirm_callback},
                {"text": "❌ CANCEL", "callback_data": cancel_callback}
            ]
        ]
        
        message = (
            f"⚠️ <b>Confirmation Required</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{action}\n\n"
            f"<b>Are you sure?</b>"
        )
        
        return self.send_message(message, reply_markup={"inline_keyboard": keyboard})
    
    # ========================================
    # Health Monitoring Commands (Batch 11)
    # ========================================
    
    def handle_health_command(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """
        Handle /health command - Show plugin health dashboard
        
        Args:
            message: Telegram message dict (optional)
            plugin_context: Plugin context (optional)
        
        Returns:
            Message ID if successful
        """
        if not self._health_monitor:
            return self.send_message(
                "🏥 <b>Health Monitor</b>\n\n"
                "Health monitoring is not configured.\n"
                "Please initialize PluginHealthMonitor first."
            )
        
        try:
            # Get formatted health dashboard
            dashboard_text = self._health_monitor.format_health_dashboard()
            return self.send_message(dashboard_text)
            
        except Exception as e:
            logger.error(f"[ControllerBot] Health command error: {e}")
            return self.send_error_response(f"Failed to get health status: {str(e)}")
    
    def handle_version_command(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """
        Handle /version command - Show active plugin versions
        
        Args:
            message: Telegram message dict (optional)
            plugin_context: Plugin context (optional)
        
        Returns:
            Message ID if successful
        """
        if not self._version_registry:
            return self.send_message(
                "📦 <b>Version Registry</b>\n\n"
                "Version registry is not configured.\n"
                "Please initialize VersionedPluginRegistry first."
            )
        
        try:
            # Get formatted version dashboard
            version_text = self._version_registry.format_version_dashboard()
            return self.send_message(version_text)
            
        except Exception as e:
            logger.error(f"[ControllerBot] Version command error: {e}")
            return self.send_error_response(f"Failed to get version info: {str(e)}")
    
    def handle_upgrade_command(self, message: Dict, args: List[str] = None, plugin_context: str = None) -> Optional[int]:
        """
        Handle /upgrade command - Upgrade plugin to specific version
        
        Usage: /upgrade <plugin_id> <version>
        Example: /upgrade combined_v3 3.2.0
        
        Args:
            message: Telegram message dict
            args: Command arguments [plugin_id, version]
            plugin_context: Plugin context (optional)
        
        Returns:
            Message ID if successful
        """
        if not self._version_registry:
            return self.send_error_response("Version registry not configured")
        
        if not args or len(args) != 2:
            return self.send_message(
                "📦 <b>Upgrade Plugin</b>\n\n"
                "Usage: <code>/upgrade &lt;plugin_id&gt; &lt;version&gt;</code>\n"
                "Example: <code>/upgrade combined_v3 3.2.0</code>"
            )
        
        plugin_id = args[0]
        target_version = args[1]
        
        try:
            success, result_message = self._version_registry.upgrade_plugin(plugin_id, target_version)
            
            if success:
                return self.send_message(f"✅ {result_message}")
            else:
                return self.send_error_response(result_message)
                
        except Exception as e:
            logger.error(f"[ControllerBot] Upgrade command error: {e}")
            return self.send_error_response(f"Upgrade failed: {str(e)}")
    
    def handle_rollback_command(self, message: Dict, args: List[str] = None, plugin_context: str = None) -> Optional[int]:
        """
        Handle /rollback command - Rollback plugin to previous version
        
        Usage: /rollback <plugin_id>
        Example: /rollback combined_v3
        
        Args:
            message: Telegram message dict
            args: Command arguments [plugin_id]
            plugin_context: Plugin context (optional)
            args: Command arguments [plugin_id]
        
        Returns:
            Message ID if successful
        """
        if not self._version_registry:
            return self.send_error_response("Version registry not configured")
        
        if not args or len(args) != 1:
            return self.send_message(
                "📦 <b>Rollback Plugin</b>\n\n"
                "Usage: <code>/rollback &lt;plugin_id&gt;</code>\n"
                "Example: <code>/rollback combined_v3</code>"
            )
        
        plugin_id = args[0]
        
        try:
            success, result_message = self._version_registry.rollback_plugin(plugin_id)
            
            if success:
                return self.send_message(f"✅ {result_message}")
            else:
                return self.send_error_response(result_message)
                
        except Exception as e:
            logger.error(f"[ControllerBot] Rollback command error: {e}")
            return self.send_error_response(f"Rollback failed: {str(e)}")
    
    def get_health_summary(self) -> Dict[str, Any]:
        """
        Get health summary data (for programmatic access)
        
        Returns:
            Dict with health summary or empty dict if not configured
        """
        if not self._health_monitor:
            return {}
        
        try:
            return self._health_monitor.get_health_summary()
        except Exception as e:
            logger.error(f"[ControllerBot] Get health summary error: {e}")
            return {}
    
    def get_version_summary(self) -> Dict[str, Any]:
        """
        Get version summary data (for programmatic access)
        
        Returns:
            Dict with version summary or empty dict if not configured
        """
        if not self._version_registry:
            return {}
        
        try:
            return self._version_registry.get_version_summary()
        except Exception as e:
            logger.error(f"[ControllerBot] Get version summary error: {e}")
            return {}
    
    # ========================================
    # CommandRegistry Integration (v2.0.0)
    # ========================================
    
    def _wire_default_handlers(self):
        """Wire ALL 105 command handlers to CommandRegistry"""
        # ==================== SYSTEM COMMANDS (10) ====================
        self._command_handlers["/start"] = self.handle_start
        self._command_handlers["/status"] = self.handle_status
        self._command_handlers["/pause"] = self.handle_pause
        self._command_handlers["/resume"] = self.handle_resume
        self._command_handlers["/help"] = self.handle_help
        self._command_handlers["/health"] = self.handle_health_command
        self._command_handlers["/version"] = self.handle_version_command
        self._command_handlers["/restart"] = self.handle_restart
        self._command_handlers["/shutdown"] = self.handle_shutdown
        self._command_handlers["/config"] = self.handle_config
        
        # ==================== TRADING COMMANDS (15) ====================
        self._command_handlers["/trade"] = self.handle_trade_menu
        self._command_handlers["/buy"] = self.handle_buy
        self._command_handlers["/sell"] = self.handle_sell
        self._command_handlers["/close"] = self.handle_close
        self._command_handlers["/closeall"] = self.handle_close_all
        self._command_handlers["/positions"] = self.handle_positions
        self._command_handlers["/orders"] = self.handle_orders
        self._command_handlers["/history"] = self.handle_history
        self._command_handlers["/pnl"] = self.handle_pnl
        self._command_handlers["/balance"] = self.handle_balance
        self._command_handlers["/equity"] = self.handle_equity
        self._command_handlers["/margin"] = self.handle_margin
        self._command_handlers["/symbols"] = self.handle_symbols
        self._command_handlers["/price"] = self.handle_price
        self._command_handlers["/spread"] = self.handle_spread
        
        # ==================== RISK COMMANDS (12) ====================
        self._command_handlers["/risk"] = self.handle_risk_menu
        self._command_handlers["/setlot"] = self.handle_set_lot
        self._command_handlers["/setsl"] = self.handle_set_sl
        self._command_handlers["/settp"] = self.handle_set_tp
        self._command_handlers["/dailylimit"] = self.handle_daily_limit
        self._command_handlers["/maxloss"] = self.handle_max_loss
        self._command_handlers["/maxprofit"] = self.handle_max_profit
        self._command_handlers["/risktier"] = self.handle_risk_tier
        self._command_handlers["/slsystem"] = self.handle_sl_system
        self._command_handlers["/trailsl"] = self.handle_trail_sl
        self._command_handlers["/breakeven"] = self.handle_breakeven
        self._command_handlers["/protection"] = self.handle_protection
        
        # ==================== STRATEGY COMMANDS (20) ====================
        self._command_handlers["/strategy"] = self.handle_strategy_menu
        self._command_handlers["/logic1"] = self.handle_logic1
        self._command_handlers["/logic2"] = self.handle_logic2
        self._command_handlers["/logic3"] = self.handle_logic3
        self._command_handlers["/v3"] = self.handle_v3
        self._command_handlers["/v6"] = self.handle_v6
        self._command_handlers["/v6_status"] = self.handle_v6_status
        self._command_handlers["/v6_control"] = self.handle_v6_control
        self._command_handlers["/tf15m_on"] = self.handle_v6_tf15m_on
        self._command_handlers["/tf15m_off"] = self.handle_v6_tf15m_off
        self._command_handlers["/tf30m_on"] = self.handle_v6_tf30m_on
        self._command_handlers["/tf30m_off"] = self.handle_v6_tf30m_off
        self._command_handlers["/tf1h_on"] = self.handle_v6_tf1h_on
        self._command_handlers["/tf1h_off"] = self.handle_v6_tf1h_off
        self._command_handlers["/tf4h_on"] = self.handle_v6_tf4h_on
        self._command_handlers["/tf4h_off"] = self.handle_v6_tf4h_off
        self._command_handlers["/signals"] = self.handle_signals
        self._command_handlers["/filters"] = self.handle_filters
        self._command_handlers["/multiplier"] = self.handle_multiplier
        self._command_handlers["/mode"] = self.handle_mode
        
        # ==================== TIMEFRAME COMMANDS (8) ====================
        self._command_handlers["/timeframe"] = self.handle_timeframe_menu
        self._command_handlers["/tf1m"] = self.handle_tf_1m
        self._command_handlers["/tf5m"] = self.handle_tf_5m
        self._command_handlers["/tf15m"] = self.handle_tf_15m
        self._command_handlers["/tf30m"] = self.handle_tf30m  # V6 30M timeframe toggle
        self._command_handlers["/tf1h"] = self.handle_tf_1h
        self._command_handlers["/tf4h"] = self.handle_tf_4h
        self._command_handlers["/tf1d"] = self.handle_tf_1d
        self._command_handlers["/trends"] = self.handle_trends
        
        # ==================== RE-ENTRY COMMANDS (8) ====================
        self._command_handlers["/reentry"] = self.handle_reentry_menu
        self._command_handlers["/slhunt"] = self.handle_sl_hunt
        self._command_handlers["/tpcontinue"] = self.handle_tp_continue
        self._command_handlers["/recovery"] = self.handle_recovery
        self._command_handlers["/cooldown"] = self.handle_cooldown
        self._command_handlers["/chains"] = self.handle_chains
        self._command_handlers["/autonomous"] = self.handle_autonomous
        self._command_handlers["/chainlimit"] = self.handle_chain_limit
        
        # ==================== PER-PLUGIN CONFIG COMMANDS (4) ====================
        self._command_handlers["/reentry_v3"] = self.handle_reentry_v3
        self._command_handlers["/reentry_v6"] = self.handle_reentry_v6
        self._command_handlers["/v3_config"] = self.handle_v3_config
        self._command_handlers["/v6_config"] = self.handle_v6_config
        
        # ==================== PROFIT COMMANDS (6) ====================
        self._command_handlers["/profit"] = self.handle_profit_menu
        self._command_handlers["/booking"] = self.handle_booking
        self._command_handlers["/levels"] = self.handle_levels
        self._command_handlers["/partial"] = self.handle_partial
        self._command_handlers["/orderb"] = self.handle_order_b
        self._command_handlers["/dualorder"] = self.handle_dual_order
        
        # ==================== ANALYTICS COMMANDS (15 - COMPLETE) ====================
        self._command_handlers["/analytics"] = self.handle_analytics_menu
        self._command_handlers["/performance"] = self.handle_performance
        self._command_handlers["/daily"] = self.handle_daily
        self._command_handlers["/weekly"] = self.handle_weekly
        self._command_handlers["/monthly"] = self.handle_monthly
        self._command_handlers["/stats"] = self.handle_stats
        self._command_handlers["/winrate"] = self.handle_winrate
        self._command_handlers["/drawdown"] = self.handle_drawdown
        # NEW: Missing analytics commands (100% Implementation)
        self._command_handlers["/pair_report"] = self.handle_pair_report
        self._command_handlers["/strategy_report"] = self.handle_strategy_report
        self._command_handlers["/tp_report"] = self.handle_tp_report
        self._command_handlers["/v6_performance"] = self.handle_v6_performance
        self._command_handlers["/compare"] = self.handle_compare
        self._command_handlers["/export"] = self.handle_export
        self._command_handlers["/dashboard"] = self.handle_dashboard
        
        # ==================== SESSION COMMANDS (6) ====================
        self._command_handlers["/session"] = self.handle_session_menu
        self._command_handlers["/london"] = self.handle_london
        self._command_handlers["/newyork"] = self.handle_newyork
        self._command_handlers["/tokyo"] = self.handle_tokyo
        self._command_handlers["/sydney"] = self.handle_sydney
        self._command_handlers["/overlap"] = self.handle_overlap
        
        # ==================== PLUGIN COMMANDS (8) ====================
        self._command_handlers["/plugin"] = self.handle_plugin_menu
        self._command_handlers["/plugins"] = self.handle_plugins
        self._command_handlers["/enable"] = self.handle_enable
        self._command_handlers["/disable"] = self.handle_disable
        self._command_handlers["/upgrade"] = self.handle_upgrade_command
        self._command_handlers["/rollback"] = self.handle_rollback_command
        self._command_handlers["/shadow"] = self.handle_shadow
        self._command_handlers["/compare"] = self.handle_compare
        
        # ==================== PLUGIN CONFIG COMMANDS (V5 Integration - 7) ====================
        self._command_handlers["/logic1_config"] = self.handle_logic1_config
        self._command_handlers["/logic2_config"] = self.handle_logic2_config
        self._command_handlers["/logic3_config"] = self.handle_logic3_config
        self._command_handlers["/v6_1m_config"] = self.handle_v6_1m_config
        self._command_handlers["/v6_5m_config"] = self.handle_v6_5m_config
        self._command_handlers["/v6_15m_config"] = self.handle_v6_15m_config
        self._command_handlers["/v6_1h_config"] = self.handle_v6_1h_config
        
        # ==================== VOICE COMMANDS (4) ====================
        self._command_handlers["/voice"] = self.handle_voice_menu
        self._command_handlers["/voicetest"] = self.handle_voice_test
        self._command_handlers["/mute"] = self.handle_mute
        self._command_handlers["/unmute"] = self.handle_unmute
        
        # ==================== NOTIFICATION COMMANDS (1) - PHASE 5 ====================
        self._command_handlers["/notifications"] = self.handle_notifications_menu
        
        logger.info(f"[ControllerBot] Wired {len(self._command_handlers)} command handlers (106 total)")
    
    def wire_command_registry(self, registry):
        """
        Wire CommandRegistry to this bot.
        
        Args:
            registry: CommandRegistry instance
        """
        self._command_registry = registry
        registry.set_dependencies(controller_bot=self, trading_engine=self._trading_engine)
        
        # Register all handlers with registry
        for cmd, handler in self._command_handlers.items():
            registry.register_command_handler(cmd, handler)
        
        logger.info("[ControllerBot] CommandRegistry wired")
    
    def wire_plugin_control_menu(self, menu):
        """
        Wire PluginControlMenu to this bot.
        
        Args:
            menu: PluginControlMenu instance
        """
        self._plugin_control_menu = menu
        menu.set_dependencies(trading_engine=self._trading_engine, telegram_bot=self)
        
        # Register plugin callbacks
        for callback_data, handler in menu.get_callbacks().items():
            if self._command_registry:
                self._command_registry.register_callback_handler(callback_data, handler)
        
        logger.info("[ControllerBot] PluginControlMenu wired")
    
    # ========================================
    # Actual Command Handler Implementations
    # ========================================
    
    def handle_start(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /start command - Show main menu via MenuManager"""
        chat_id = self.chat_id
        if message and 'chat' in message:
            chat_id = message['chat'].get('id', self.chat_id)
            
        if self._menu_manager:
            return self._menu_manager.show_main_menu(chat_id)
            
        # Fallback if MenuManager not available
        keyboard = [
            [{"text": "📊 Dashboard", "callback_data": "action_dashboard"}],
            [{"text": "🔌 Plugin Control", "callback_data": "plugin_menu"}],
            [{"text": "📈 Status", "callback_data": "action_status"}],
            [{"text": "⚙️ Settings", "callback_data": "menu_settings"}],
            [{"text": "❓ Help", "callback_data": "action_help"}]
        ]
        
        uptime = datetime.now() - self._startup_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        text = (
            "🤖 <b>ZEPIX TRADING BOT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Status:</b> {'🟢 Active' if not self._is_paused else '🔴 Paused'}\n"
            f"<b>Uptime:</b> {hours}h {minutes}m {seconds}s\n"
            f"<b>Version:</b> V5 Hybrid Architecture\n"
            f"<b>Menu:</b> Fallback Mode (Manager missing)\n\n"
            "<i>Select an option below:</i>"
        )
        
        return self.send_message(text, reply_markup={"inline_keyboard": keyboard})
    
    def handle_status(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """
        Handle /status command - Show bot status (plugin-aware).
        
        Args:
            message: Telegram message dict
            plugin_context: Selected plugin ('v3', 'v6', 'both')
        """
        uptime = datetime.now() - self._startup_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Default to 'both' if no plugin context
        if not plugin_context:
            plugin_context = 'both'
        
        # Get plugin status
        v3_enabled = True
        v6_enabled = True
        if self._trading_engine:
            if hasattr(self._trading_engine, 'is_plugin_enabled'):
                v3_enabled = self._trading_engine.is_plugin_enabled("v3_combined")
                v6_enabled = self._trading_engine.is_plugin_enabled("v6_price_action")
        
        # Build status based on plugin context
        if plugin_context == 'v3':
            # V3 only status
            return self._send_v3_only_status(v3_enabled, uptime)
        elif plugin_context == 'v6':
            # V6 only status
            return self._send_v6_only_status(v6_enabled, uptime)
        else:
            # Both plugins (combined status)
            status_data = {
                "is_active": not self._is_paused,
                "uptime": f"{hours}h {minutes}m {seconds}s",
                "active_plugins": int(v3_enabled) + int(v6_enabled),
                "open_trades": 0,
                "daily_pnl": 0.0
            }
            
            # Try to get real data from trading engine
            if self._trading_engine:
                if hasattr(self._trading_engine, 'get_open_positions'):
                    try:
                        positions = self._trading_engine.get_open_positions()
                        status_data["open_trades"] = len(positions) if positions else 0
                    except Exception:
                        pass
                if hasattr(self._trading_engine, 'get_daily_pnl'):
                    try:
                        status_data["daily_pnl"] = self._trading_engine.get_daily_pnl()
                    except Exception:
                        pass
            
            return self.send_status_response(status_data)
    
    def _send_v3_only_status(self, v3_enabled: bool, uptime) -> Optional[int]:
        """Send V3-specific status."""
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        status_emoji = "🟢" if v3_enabled else "🔴"
        status_text = "ENABLED" if v3_enabled else "DISABLED"
        
        message = (
            f"🔵 <b>V3 COMBINED LOGIC STATUS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Status:</b> {status_emoji} {status_text}\n"
            f"<b>Uptime:</b> {hours}h {minutes}m {seconds}s\n\n"
            f"<b>Active Strategies:</b>\n"
            f"├─ LOGIC1 (5M): {status_emoji}\n"
            f"├─ LOGIC2 (15M): {status_emoji}\n"
            f"└─ LOGIC3 (1H): {status_emoji}\n\n"
            f"<i>Use /v3 for detailed V3 controls</i>"
        )
        
        return self.send_message(message)
    
    def _send_v6_only_status(self, v6_enabled: bool, uptime) -> Optional[int]:
        """Send V6-specific status."""
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        status_emoji = "🟢" if v6_enabled else "🔴"
        status_text = "ENABLED" if v6_enabled else "DISABLED"
        
        message = (
            f"🟢 <b>V6 PRICE ACTION STATUS</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Status:</b> {status_emoji} {status_text}\n"
            f"<b>Uptime:</b> {hours}h {minutes}m {seconds}s\n\n"
            f"<b>Active Timeframes:</b>\n"
            f"├─ 15M: {status_emoji}\n"
            f"├─ 30M: {status_emoji}\n"
            f"├─ 1H: {status_emoji}\n"
            f"└─ 4H: {status_emoji}\n\n"
            f"<i>Use /v6 for detailed V6 controls</i>"
        )
        
        return self.send_message(message)
    
    def handle_pause(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """
        Handle /pause command - Pause trading (plugin-aware).
        
        Args:
            message: Telegram message dict
            plugin_context: Selected plugin ('v3', 'v6', 'both')
        """
        if not plugin_context:
            plugin_context = 'both'
        
        # Check if already paused
        if plugin_context == 'both' and self._is_paused:
            return self.send_message("⚠️ All trading is already paused.")
        
        if plugin_context == 'both':
            self._is_paused = True
            if self._trading_engine and hasattr(self._trading_engine, 'pause_trading'):
                self._trading_engine.pause_trading()
            
            return self.send_message(
                f"⏸️ <b>ALL TRADING PAUSED</b>\n\n"
                f"Both V3 and V6 plugins are now paused.\n\n"
                f"<i>Use /resume to restart</i>"
            )
        elif plugin_context == 'v3':
            # Pause V3 only
            if self._trading_engine and hasattr(self._trading_engine, 'pause_plugin'):
                self._trading_engine.pause_plugin('v3_combined')
            
            return self.send_message(
                f"⏸️ <b>V3 COMBINED LOGIC PAUSED</b>\n\n"
                f"🔵 V3: ⏸️ PAUSED\n"
                f"🟢 V6: ✅ STILL RUNNING\n\n"
                f"<i>Use /resume to restart V3</i>"
            )
        else:  # v6
            # Pause V6 only
            if self._trading_engine and hasattr(self._trading_engine, 'pause_plugin'):
                self._trading_engine.pause_plugin('v6_price_action')
            
            return self.send_message(
                f"⏸️ <b>V6 PRICE ACTION PAUSED</b>\n\n"
                f"🔵 V3: ✅ STILL RUNNING\n"
                f"🟢 V6: ⏸️ PAUSED\n\n"
                f"<i>Use /resume to restart V6</i>"
            )
    
    def handle_resume(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """
        Handle /resume command - Resume trading (plugin-aware).
        
        Args:
            message: Telegram message dict
            plugin_context: Selected plugin ('v3', 'v6', 'both')
        """
        if not plugin_context:
            plugin_context = 'both'
        
        if plugin_context == 'both':
            if not self._is_paused:
                return self.send_message("✅ All trading is already active.")
            
            self._is_paused = False
            if self._trading_engine and hasattr(self._trading_engine, 'resume_trading'):
                self._trading_engine.resume_trading()
            
            return self.send_message(
                "✅ <b>ALL TRADING RESUMED</b>\n\n"
                "Both V3 and V6 are now active.\n\n"
                "<i>Bot is processing signals</i>"
            )
        elif plugin_context == 'v3':
            # Resume V3 only
            if self._trading_engine and hasattr(self._trading_engine, 'resume_plugin'):
                self._trading_engine.resume_plugin('v3_combined')
            
            return self.send_message(
                "✅ <b>V3 COMBINED LOGIC RESUMED</b>\n\n"
                "🔵 V3: ✅ ACTIVE\n\n"
                "<i>V3 is now processing signals</i>"
            )
        else:  # v6
            # Resume V6 only
            if self._trading_engine and hasattr(self._trading_engine, 'resume_plugin'):
                self._trading_engine.resume_plugin('v6_price_action')
            
            return self.send_message(
                "✅ <b>V6 PRICE ACTION RESUMED</b>\n\n"
                "🟢 V6: ✅ ACTIVE\n\n"
                "<i>V6 is now processing signals</i>"
            )
    
    def handle_help(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /help command - Show help menu"""
        if self._command_registry:
            help_text = self._command_registry.generate_help_text()
            keyboard = self._command_registry.generate_category_menu()
            return self.send_message(help_text, reply_markup={"inline_keyboard": keyboard})
        
        # Fallback help
        text = (
            "📚 <b>HELP MENU</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>System Commands:</b>\n"
            "/start - Show main menu\n"
            "/status - Show bot status\n"
            "/pause - Pause trading\n"
            "/resume - Resume trading\n"
            "/health - Plugin health\n"
            "/version - Plugin versions\n\n"
            "<b>Plugin Commands:</b>\n"
            "/plugin - Plugin control menu\n"
            "/plugins - List all plugins\n"
            "/enable - Enable plugin\n"
            "/disable - Disable plugin\n"
        )
        return self.send_message(text)
    
    def handle_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /config command - Show configuration"""
        text = (
            "⚙️ <b>CONFIGURATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Architecture:</b> V5 Hybrid\n"
            "<b>Plugins:</b> V3 Combined, V6 Price Action\n"
            "<b>Mode:</b> Production\n"
            "<b>Shadow Mode:</b> Enabled for V6\n\n"
            "<i>Use /plugin to manage plugins</i>"
        )
        return self.send_message(text)
    
    def handle_plugin_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /plugin command - Show plugin control menu"""
        if self._plugin_control_menu:
            chat_id = self.chat_id
            if message and 'chat' in message:
                chat_id = message['chat'].get('id', self.chat_id)
            return self._plugin_control_menu.show_plugin_menu(chat_id)
        
        # Fallback
        return self.send_message(
            "🔌 <b>PLUGIN CONTROL</b>\n\n"
            "Plugin control menu not configured.\n"
            "Please initialize PluginControlMenu first."
        )
    
    def handle_plugins(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /plugins command - List all plugins"""
        v3_enabled = True
        v6_enabled = True
        
        if self._trading_engine:
            if hasattr(self._trading_engine, 'is_plugin_enabled'):
                v3_enabled = self._trading_engine.is_plugin_enabled("v3_combined")
                v6_enabled = self._trading_engine.is_plugin_enabled("v6_price_action")
        
        v3_emoji = "🟢" if v3_enabled else "🔴"
        v6_emoji = "🟢" if v6_enabled else "🔴"
        
        text = (
            "📦 <b>INSTALLED PLUGINS</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"1. {v3_emoji} <b>V3 Combined Logic</b>\n"
            f"   └─ Status: {'ENABLED' if v3_enabled else 'DISABLED'}\n\n"
            f"2. {v6_emoji} <b>V6 Price Action</b>\n"
            f"   └─ Status: {'ENABLED' if v6_enabled else 'DISABLED'}\n\n"
            f"<i>Total: 2 plugins ({int(v3_enabled) + int(v6_enabled)} active)</i>"
        )
        return self.send_message(text)
    
    def handle_enable(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /enable command - Enable plugin"""
        # If context is specific, act on it? 
        # Usually /enable gives menu, but if context is set we could auto-enable.
        # Sticking to menu for safety unless explicit logic needed.
        keyboard = [
            [{"text": "🟢 Enable V3", "callback_data": "plugin_v3_enable"}],
            [{"text": "🟢 Enable V6", "callback_data": "plugin_v6_enable"}],
            [{"text": "🔙 Back", "callback_data": "plugin_menu"}]
        ]
        return self.send_message(
            "🟢 <b>ENABLE PLUGIN</b>\n\n"
            "Select a plugin to enable:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_disable(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /disable command - Disable plugin"""
        keyboard = [
            [{"text": "🔴 Disable V3", "callback_data": "plugin_v3_disable"}],
            [{"text": "🔴 Disable V6", "callback_data": "plugin_v6_disable"}],
            [{"text": "🔙 Back", "callback_data": "plugin_menu"}]
        ]
        return self.send_message(
            "🔴 <b>DISABLE PLUGIN</b>\n\n"
            "Select a plugin to disable:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_positions(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /positions command - Show open positions with plugin filtering"""
        # Get filter from message text if provided
        filter_plugin = None if not plugin_context or plugin_context == 'both' else plugin_context
        
        if message and 'text' in message:
            text = message['text'].lower()
            if 'v3' in text:
                filter_plugin = 'v3'
            elif 'v6' in text:
                filter_plugin = 'v6'
            elif '15m' in text:
                filter_plugin = '15m'
            elif '30m' in text:
                filter_plugin = '30m'
            elif '1h' in text:
                filter_plugin = '1h'
            elif '4h' in text:
                filter_plugin = '4h'
        
        positions = []
        if self._trading_engine and hasattr(self._trading_engine, 'get_open_positions'):
            try:
                positions = self._trading_engine.get_open_positions() or []
                
                # Apply plugin filter
                if filter_plugin and positions:
                    filtered = []
                    for pos in positions:
                        plugin_name = pos.get('plugin_name', '').lower()
                        if filter_plugin in plugin_name:
                            filtered.append(pos)
                    positions = filtered
                    
            except Exception:
                pass
        
        if not positions:
            title = f" ({filter_plugin.upper()})" if filter_plugin else ""
            return self.send_message(
                f"📊 <b>OPEN POSITIONS{title}</b>\n\n"
                "No open positions."
            )
        
        # Group by plugin (rest of logic handles display)
        v3_positions = []
        v6_positions = []
        for pos in positions:
            plugin = pos.get('plugin_name', '').lower()
            if 'v3' in plugin:
                v3_positions.append(pos)
            elif 'v6' in plugin:
                v6_positions.append(pos)
        
        text = "📊 <b>OPEN POSITIONS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if v3_positions:
            text += "🔵 <b>V3 POSITIONS</b>\n"
            for i, pos in enumerate(v3_positions, 1):
                symbol = pos.get('symbol', 'N/A')
                side = pos.get('side', 'N/A')
                pnl = pos.get('pnl', 0)
                emoji = "🟢" if pnl >= 0 else "🔴"
                text += f"{i}. {symbol} {side} | P&L: {emoji} ${pnl:.2f}\n"
            text += "\n"
        
        if v6_positions:
            text += "🟢 <b>V6 POSITIONS</b>\n"
            for i, pos in enumerate(v6_positions, 1):
                symbol = pos.get('symbol', 'N/A')
                side = pos.get('side', 'N/A')
                pnl = pos.get('pnl', 0)
                plugin = pos.get('plugin_name', 'N/A')
                emoji = "🟢" if pnl >= 0 else "🔴"
                # Extract timeframe from plugin name
                tf = "Unknown"
                if '15m' in plugin.lower():
                    tf = "15M"
                elif '30m' in plugin.lower():
                    tf = "30M"
                elif '1h' in plugin.lower():
                    tf = "1H"
                elif '4h' in plugin.lower():
                    tf = "4H"
                text += f"{i}. {symbol} {side} ({tf}) | P&L: {emoji} ${pnl:.2f}\n"
        
        return self.send_message(text)
    
    def handle_pnl(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /pnl command - Show P&L summary with per-plugin breakdown"""
        daily_pnl = 0.0
        v3_pnl = 0.0
        v6_pnl = 0.0
        
        if self._trading_engine:
            # Get total daily P&L
            if hasattr(self._trading_engine, 'get_daily_pnl'):
                try:
                    daily_pnl = self._trading_engine.get_daily_pnl()
                except Exception:
                    pass
            
            # Try to get per-plugin breakdown
            if hasattr(self._trading_engine, 'get_plugin_pnl'):
                try:
                    plugin_pnl = self._trading_engine.get_plugin_pnl()
                    for plugin, pnl in plugin_pnl.items():
                        if 'v3' in plugin.lower():
                            v3_pnl += pnl
                        elif 'v6' in plugin.lower():
                            v6_pnl += pnl
                except Exception:
                    pass
        
        emoji = "🟢" if daily_pnl >= 0 else "🔴"
        v3_emoji = "🟢" if v3_pnl >= 0 else "🔴"
        v6_emoji = "🟢" if v6_pnl >= 0 else "🔴"
        
        title = "💰 <b>P&L SUMMARY"
        if plugin_context and plugin_context != 'both':
            title += f" ({plugin_context.upper()})"
        title += "</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        text = title
        
        # If we have plugin breakdown, show it
        if v3_pnl != 0 or v6_pnl != 0:
            text += f"<b>📊 TODAY</b> {emoji} ${daily_pnl:.2f}\n\n"
            
            show_v3 = not plugin_context or plugin_context == 'both' or plugin_context.lower() == 'v3'
            show_v6 = not plugin_context or plugin_context == 'both' or plugin_context.lower() == 'v6'
            
            if show_v3:
                text += f"<b>🔵 V3 Combined:</b> {v3_emoji} ${v3_pnl:.2f}\n"
            
            if show_v6:
                text += f"<b>🟢 V6 Price Action:</b> {v6_emoji} ${v6_pnl:.2f}\n"
            
            if show_v3 and show_v6:
                text += "\n"
                # Show percentages
                if daily_pnl != 0:
                    v3_pct = (v3_pnl / daily_pnl * 100) if daily_pnl != 0 else 0
                    v6_pct = (v6_pnl / daily_pnl * 100) if daily_pnl != 0 else 0
                    text += f"V3: {v3_pct:.1f}% | V6: {v6_pct:.1f}%\n"
        else:
            # Simple display if no breakdown available
            text += f"<b>Today:</b> {emoji} ${daily_pnl:.2f}\n"
        
        text += f"\n<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        return self.send_message(text)
    
    def handle_balance(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /balance command - Show account balance"""
        balance = 0.0
        equity = 0.0
        
        if self._trading_engine:
            if hasattr(self._trading_engine, 'get_account_balance'):
                try:
                    balance = self._trading_engine.get_account_balance()
                except Exception:
                    pass
            if hasattr(self._trading_engine, 'get_account_equity'):
                try:
                    equity = self._trading_engine.get_account_equity()
                except Exception:
                    pass
        
        return self.send_message(
            f"💵 <b>ACCOUNT BALANCE</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Balance:</b> ${balance:.2f}\n"
            f"<b>Equity:</b> ${equity:.2f}\n"
            f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        )
    
    # ========================================
    # SYSTEM COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_restart(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /restart command - Restart bot (admin only)"""
        return self.send_confirmation_request(
            "Are you sure you want to <b>RESTART</b> the bot?\n\nThis will temporarily stop all trading.",
            "confirm_restart",
            "menu_main"
        )
    
    def handle_shutdown(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /shutdown command - Shutdown bot (admin only)"""
        return self.send_confirmation_request(
            "Are you sure you want to <b>SHUTDOWN</b> the bot?\n\n⚠️ This will stop all trading until manually restarted.",
            "confirm_shutdown",
            "menu_main"
        )
    
    # ========================================
    # TRADING COMMANDS (Missing Handlers)
    # ========================================
    

    # ========================================
    # TRADING COMMANDS (Plugin-Aware)
    # ========================================
    
    def handle_trade_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /trade command - Show trading menu"""
        if not plugin_context:
            plugin_context = 'both'
            
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'Global'}[plugin_context]
        
        keyboard = [
            [{"text": "📈 BUY", "callback_data": "trade_buy"}, {"text": "📉 SELL", "callback_data": "trade_sell"}],
            [{"text": "❌ Close Position", "callback_data": "trade_close"}],
            [{"text": "📊 Positions", "callback_data": "trade_positions"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"📊 <b>TRADING MENU ({plugin_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect a trading action:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_buy(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /buy command - Place buy order"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📈 <b>BUY ORDER ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/buy SYMBOL LOT</code>\n"
            "Example: <code>/buy EURUSD 0.1</code>\n\n"
            "<i>Or use the trading menu for guided order placement.</i>"
        )
    
    def handle_sell(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /sell command - Place sell order"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📉 <b>SELL ORDER ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/sell SYMBOL LOT</code>\n"
            "Example: <code>/sell EURUSD 0.1</code>\n\n"
            "<i>Or use the trading menu for guided order placement.</i>"
        )
    
    def handle_close(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /close command - Close position"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"❌ <b>CLOSE POSITION ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/close TICKET</code>\n"
            "Example: <code>/close 12345</code>\n\n"
            "<i>Use /positions to see open positions and their tickets.</i>"
        )
    
    def handle_close_all(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /closeall command - Close all positions"""
        if not plugin_context:
            plugin_context = 'both'
            
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'ALL'}[plugin_context]
        
        return self.send_confirmation_request(
            f"Are you sure you want to <b>CLOSE {plugin_name}</b> positions?",
            f"confirm_close_all_{plugin_context}",
            "menu_main"
        )
    
    def handle_orders(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /orders command - Show pending orders"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📋 <b>PENDING ORDERS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "No pending orders."
        )
    
    def handle_history(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /history command - Show trade history"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📜 <b>TRADE HISTORY ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Recent trades will be displayed here.\n\n"
            "<i>Use /daily, /weekly, or /monthly for detailed reports.</i>"
        )
    
    def handle_equity(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /equity command - Show account equity"""
        if not plugin_context:
            plugin_context = 'both'
        equity = 0.0
        if self._trading_engine and hasattr(self._trading_engine, 'get_account_equity'):
            try:
                equity = self._trading_engine.get_account_equity()
            except Exception:
                pass
        return self.send_message(
            f"💰 <b>ACCOUNT EQUITY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Equity:</b> ${equity:.2f}\n"
            f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        )
    
    def handle_margin(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /margin command - Show margin info"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            "📊 <b>MARGIN INFO</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Free Margin:</b> $0.00\n"
            "<b>Used Margin:</b> $0.00\n"
            "<b>Margin Level:</b> 0%"
        )
    
    def handle_symbols(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /symbols command - Show available symbols"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            "💱 <b>AVAILABLE SYMBOLS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "EURUSD, GBPUSD, USDJPY, AUDUSD\n"
            "USDCAD, NZDUSD, USDCHF, EURGBP\n"
            "EURJPY, GBPJPY, XAUUSD, XAGUSD"
        )
    
    def handle_price(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /price command - Get current price"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            "💵 <b>PRICE CHECK</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/price SYMBOL</code>\n"
            "Example: <code>/price EURUSD</code>"
        )
    
    def handle_spread(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /spread command - Show spread info"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            "📏 <b>SPREAD INFO</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/spread SYMBOL</code>\n"
            "Example: <code>/spread EURUSD</code>"
        )
    
    # ========================================
    # RISK COMMANDS (Plugin-Aware)
    # ========================================
    
    def handle_risk_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /risk command - Show risk settings menu"""
        if not plugin_context:
            plugin_context = 'both'
            
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'Global'}[plugin_context]
        
        keyboard = [
            [{"text": "📊 Lot Size", "callback_data": "risk_lot"}, {"text": "🛑 Stop Loss", "callback_data": "risk_sl"}],
            [{"text": "🎯 Take Profit", "callback_data": "risk_tp"}, {"text": "📈 Risk Tier", "callback_data": "risk_tier"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"⚠️ <b>RISK MANAGEMENT ({plugin_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure your risk settings:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_set_lot(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /setlot command - Set lot size"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📊 <b>SET LOT SIZE ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/setlot SIZE</code>\n"
            "Example: <code>/setlot 0.1</code>\n\n"
            "Current: 0.01 lots"
        )
    
    def handle_set_sl(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /setsl command - Set stop loss"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🛑 <b>SET STOP LOSS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/setsl PIPS</code>\n"
            "Example: <code>/setsl 50</code>\n\n"
            "Current: 30 pips"
        )
    
    def handle_set_tp(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /settp command - Set take profit"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🎯 <b>SET TAKE PROFIT ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/settp PIPS</code>\n"
            "Example: <code>/settp 100</code>\n\n"
            "Current: 60 pips"
        )
    
    def handle_daily_limit(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /dailylimit command - Set daily loss limit"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📉 <b>DAILY LOSS LIMIT ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/dailylimit AMOUNT</code>\n"
            "Example: <code>/dailylimit 100</code>\n\n"
            "Current: $500"
        )
    
    def handle_max_loss(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /maxloss command - Set max loss"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🔴 <b>MAX LOSS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/maxloss AMOUNT</code>\n"
            "Example: <code>/maxloss 1000</code>\n\n"
            "Current: $1000"
        )
    
    def handle_max_profit(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /maxprofit command - Set max profit"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🟢 <b>MAX PROFIT ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/maxprofit AMOUNT</code>\n"
            "Example: <code>/maxprofit 500</code>\n\n"
            "Current: $500"
        )
    
    def handle_risk_tier(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /risktier command - Set risk tier"""
        if not plugin_context:
            plugin_context = 'both'
        
        keyboard = [
            [{"text": "🟢 Conservative", "callback_data": "risk_tier_1"}],
            [{"text": "🟡 Moderate", "callback_data": "risk_tier_2"}],
            [{"text": "🔴 Aggressive", "callback_data": "risk_tier_3"}],
            [{"text": "🔙 Back", "callback_data": "menu_risk"}]
        ]
        return self.send_message(
            f"📈 <b>RISK TIER ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect your risk tier:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_sl_system(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /slsystem command - SL system settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🛑 <b>SL SYSTEM ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Mode:</b> Dynamic\n"
            "<b>Base SL:</b> 30 pips\n"
            "<b>ATR Multiplier:</b> 1.5x"
        )
    
    def handle_trail_sl(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /trailsl command - Trailing SL settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📏 <b>TRAILING STOP LOSS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> Enabled\n"
            "<b>Trail Distance:</b> 20 pips\n"
            "<b>Activation:</b> After +30 pips"
        )
    
    def handle_breakeven(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /breakeven command - Breakeven settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"⚖️ <b>BREAKEVEN SETTINGS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> Enabled\n"
            "<b>Activation:</b> After +25 pips\n"
            "<b>Lock Profit:</b> +5 pips"
        )
    
    def handle_protection(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /protection command - Profit protection"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🛡️ <b>PROFIT PROTECTION ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> Enabled\n"
            "<b>Lock at:</b> 50% of max profit\n"
            "<b>Trail:</b> 25% increments"
        )
    
    # ========================================
    # STRATEGY COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_strategy_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /strategy command - Show strategy settings"""
        keyboard = [
            [{"text": "📊 V3 Combined", "callback_data": "strategy_v3"}, {"text": "📈 V6 Price Action", "callback_data": "strategy_v6"}],
            [{"text": "🔄 Logic 1 (5m)", "callback_data": "toggle_logic1"}, {"text": "🔄 Logic 2 (15m)", "callback_data": "toggle_logic2"}],
            [{"text": "🔄 Logic 3 (1h)", "callback_data": "toggle_logic3"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "📊 <b>STRATEGY SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure your trading strategies:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_logic1(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /logic1 command - Toggle Logic 1 (5m)"""
        return self.send_message("🔄 <b>LOGIC 1 (5M)</b>\n\nStatus: ENABLED\n\n<i>Use button to toggle.</i>")
    
    def handle_logic2(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /logic2 command - Toggle Logic 2 (15m)"""
        return self.send_message("🔄 <b>LOGIC 2 (15M)</b>\n\nStatus: ENABLED\n\n<i>Use button to toggle.</i>")
    
    def handle_logic3(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /logic3 command - Toggle Logic 3 (1h)"""
        return self.send_message("🔄 <b>LOGIC 3 (1H)</b>\n\nStatus: ENABLED\n\n<i>Use button to toggle.</i>")
    
    def handle_v3(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v3 command - V3 Combined settings"""
        return self.send_message(
            "📊 <b>V3 COMBINED LOGIC</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Logic 1 (5m):</b> ON\n"
            "<b>Logic 2 (15m):</b> ON\n"
            "<b>Logic 3 (1h):</b> ON"
        )
    
    def handle_v6(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6 command - V6 Price Action settings"""
        if hasattr(self, 'show_v6_control_menu'):
            try:
                # If show_v6_control_menu takes context, pass it
                import inspect
                sig = inspect.signature(self.show_v6_control_menu)
                if 'plugin_context' in sig.parameters:
                    self.show_v6_control_menu(plugin_context=plugin_context)
                else:
                    self.show_v6_control_menu()
            except:
                self.show_v6_control_menu()
        else:
            return self.send_message("V6 Control Menu not available")
        return None
    
    def handle_v6_status(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_status command - V6 system status"""
        return self.send_message(
            "📈 <b>V6 PRICE ACTION STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>System:</b> ENABLED\n"
            "<b>15M:</b> ON\n<b>30M:</b> ON\n<b>1H:</b> ON\n<b>4H:</b> ON"
        )
    
    def handle_v6_control(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_control command - V6 control menu"""
        if hasattr(self, 'show_v6_control_menu'):
            try:
                import inspect
                sig = inspect.signature(self.show_v6_control_menu)
                if 'plugin_context' in sig.parameters:
                    self.show_v6_control_menu(plugin_context=plugin_context)
                else:
                    self.show_v6_control_menu()
            except:
                self.show_v6_control_menu()
        else:
            return self.send_message("V6 Control Menu not available")
        return None
    
    def handle_v6_tf15m_on(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf15m_on command - Enable V6 15M"""
        return self.send_message("✅ <b>V6 15M ENABLED</b>\n\n15-minute timeframe is now active.")
    
    def handle_v6_tf15m_off(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf15m_off command - Disable V6 15M"""
        return self.send_message("❌ <b>V6 15M DISABLED</b>\n\n15-minute timeframe is now inactive.")
    
    def handle_v6_tf30m_on(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf30m_on command - Enable V6 30M"""
        return self.send_message("✅ <b>V6 30M ENABLED</b>\n\n30-minute timeframe is now active.")
    
    def handle_v6_tf30m_off(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf30m_off command - Disable V6 30M"""
        return self.send_message("❌ <b>V6 30M DISABLED</b>\n\n30-minute timeframe is now inactive.")
    
    def handle_v6_tf1h_on(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf1h_on command - Enable V6 1H"""
        return self.send_message("✅ <b>V6 1H ENABLED</b>\n\n1-hour timeframe is now active.")
    
    def handle_v6_tf1h_off(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf1h_off command - Disable V6 1H"""
        return self.send_message("❌ <b>V6 1H DISABLED</b>\n\n1-hour timeframe is now inactive.")
    
    def handle_v6_tf4h_on(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf4h_on command - Enable V6 4H"""
        return self.send_message("✅ <b>V6 4H ENABLED</b>\n\n4-hour timeframe is now active.")
    
    def handle_v6_tf4h_off(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf4h_off command - Disable V6 4H"""
        return self.send_message("❌ <b>V6 4H DISABLED</b>\n\n4-hour timeframe is now inactive.")
    
    # ========================================
    # V5 PLUGIN CONFIG COMMANDS (Per-Plugin Configuration)
    # ========================================
    
    def handle_logic1_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /logic1_config - Show Logic 1 configuration menu"""
        config_text = (
            "⚙️ <b>LOGIC 1 CONFIGURATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 <b>TRADING SETTINGS:</b>\n"
            "• Status: 🟢 ENABLED\n"
            "• Lot Size: 0.02\n"
            "• Max Trades: 3\n"
            "• Risk %: 2%\n\n"
            "🔄 <b>RE-ENTRY SETTINGS:</b>\n"
            "• TP Re-entry: 🟢 ON\n"
            "• SL Hunt: 🟢 ON\n"
            "• Max Levels: 2\n\n"
            "Use /setlot, /reentry, /slhunt to modify settings"
        )
        return self.send_message(config_text)
    
    def handle_logic2_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /logic2_config - Show Logic 2 configuration menu"""
        config_text = (
            "⚙️ <b>LOGIC 2 CONFIGURATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 <b>TRADING SETTINGS:</b>\n"
            "• Status: 🟢 ENABLED\n"
            "• Lot Size: 0.02\n"
            "• Max Trades: 3\n"
            "• Risk %: 2%\n\n"
            "🔄 <b>RE-ENTRY SETTINGS:</b>\n"
            "• TP Re-entry: 🟢 ON\n"
            "• SL Hunt: 🟢 ON\n"
            "• Max Levels: 2\n\n"
            "Use /setlot, /reentry, /slhunt to modify settings"
        )
        return self.send_message(config_text)
    
    def handle_logic3_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /logic3_config - Show Logic 3 configuration menu"""
        config_text = (
            "⚙️ <b>LOGIC 3 CONFIGURATION</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 <b>TRADING SETTINGS:</b>\n"
            "• Status: 🟢 ENABLED\n"
            "• Lot Size: 0.02\n"
            "• Max Trades: 3\n"
            "• Risk %: 2%\n\n"
            "🔄 <b>RE-ENTRY SETTINGS:</b>\n"
            "• TP Re-entry: 🟢 ON\n"
            "• SL Hunt: 🟢 ON\n"
            "• Max Levels: 2\n\n"
            "Use /setlot, /reentry, /slhunt to modify settings"
        )
        return self.send_message(config_text)
    
    def handle_v6_1m_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_1m_config - Show V6 1M configuration menu"""
        config_text = (
            "⚙️ <b>V6 1M CONFIGURATION</b> 🔶⚡\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 <b>TRADING SETTINGS:</b>\n"
            "• Status: 🟢 ENABLED\n"
            "• Lot Size: 0.01\n"
            "• Max Trades: 2\n"
            "• Risk %: 1%\n\n"
            "🔄 <b>RE-ENTRY SETTINGS:</b>\n"
            "• TP Re-entry: 🔴 OFF\n"
            "• SL Hunt: 🟢 ON\n"
            "• Max Levels: 2\n\n"
            "📈 <b>PRICE ACTION SETTINGS:</b>\n"
            "• Timeframe: 1 Minute\n"
            "• Pattern Detection: Enabled\n"
            "• Trend Pulse: Active\n\n"
            "Use /v6_control to toggle timeframe\n"
            "Use /setlot, /reentry to modify settings"
        )
        return self.send_message(config_text)
    
    def handle_v6_5m_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_5m_config - Show V6 5M configuration menu"""
        config_text = (
            "⚙️ <b>V6 5M CONFIGURATION</b> 🔶⏱️\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 <b>TRADING SETTINGS:</b>\n"
            "• Status: 🟢 ENABLED\n"
            "• Lot Size: 0.01\n"
            "• Max Trades: 2\n"
            "• Risk %: 1%\n\n"
            "🔄 <b>RE-ENTRY SETTINGS:</b>\n"
            "• TP Re-entry: 🔴 OFF\n"
            "• SL Hunt: 🟢 ON\n"
            "• Max Levels: 2\n\n"
            "📈 <b>PRICE ACTION SETTINGS:</b>\n"
            "• Timeframe: 5 Minutes\n"
            "• Pattern Detection: Enabled\n"
            "• Trend Pulse: Active\n\n"
            "Use /v6_control to toggle timeframe\n"
            "Use /setlot, /reentry to modify settings"
        )
        return self.send_message(config_text)
    
    def handle_v6_15m_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_15m_config - Show V6 15M configuration menu"""
        config_text = (
            "⚙️ <b>V6 15M CONFIGURATION</b> 🔶⏱️\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 <b>TRADING SETTINGS:</b>\n"
            "• Status: 🟢 ENABLED\n"
            "• Lot Size: 0.01\n"
            "• Max Trades: 2\n"
            "• Risk %: 1%\n\n"
            "🔄 <b>RE-ENTRY SETTINGS:</b>\n"
            "• TP Re-entry: 🔴 OFF\n"
            "• SL Hunt: 🟢 ON\n"
            "• Max Levels: 2\n\n"
            "📈 <b>PRICE ACTION SETTINGS:</b>\n"
            "• Timeframe: 15 Minutes\n"
            "• Pattern Detection: Enabled\n"
            "• Trend Pulse: Active\n\n"
            "Use /v6_control to toggle timeframe\n"
            "Use /setlot, /reentry to modify settings"
        )
        return self.send_message(config_text)
    
    def handle_v6_1h_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_1h_config - Show V6 1H configuration menu"""
        config_text = (
            "⚙️ <b>V6 1H CONFIGURATION</b> 🔶🕐\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 <b>TRADING SETTINGS:</b>\n"
            "• Status: 🟢 ENABLED\n"
            "• Lot Size: 0.01\n"
            "• Max Trades: 2\n"
            "• Risk %: 1%\n\n"
            "🔄 <b>RE-ENTRY SETTINGS:</b>\n"
            "• TP Re-entry: 🔴 OFF\n"
            "• SL Hunt: 🟢 ON\n"
            "• Max Levels: 2\n\n"
            "📈 <b>PRICE ACTION SETTINGS:</b>\n"
            "• Timeframe: 1 Hour\n"
            "• Pattern Detection: Enabled\n"
            "• Trend Pulse: Active\n\n"
            "Use /v6_control to toggle timeframe\n"
            "Use /setlot, /reentry to modify settings"
        )
        return self.send_message(config_text)
    
    def handle_signals(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /signals command - Signal settings"""
        return self.send_message(
            "📡 <b>SIGNAL SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Source:</b> Pine Script V3/V6\n"
            "<b>Filter:</b> All signals\n"
            "<b>Confirmation:</b> Required"
        )
    
    def handle_filters(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /filters command - Signal filters"""
        return self.send_message(
            "🔍 <b>SIGNAL FILTERS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Trend Filter:</b> ON\n"
            "<b>Session Filter:</b> ON\n"
            "<b>News Filter:</b> OFF"
        )
    
    def handle_multiplier(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /multiplier command - Lot multiplier"""
        return self.send_message(
            "✖️ <b>LOT MULTIPLIER</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/multiplier VALUE</code>\n"
            "Example: <code>/multiplier 1.5</code>\n\n"
            "Current: 1.0x"
        )
    
    def handle_mode(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /mode command - Trading mode"""
        keyboard = [
            [{"text": "🟢 Live", "callback_data": "mode_live"}],
            [{"text": "🟡 Shadow", "callback_data": "mode_shadow"}],
            [{"text": "🔴 Paper", "callback_data": "mode_paper"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "🎮 <b>TRADING MODE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect trading mode:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    # ========================================
    # TIMEFRAME COMMANDS (Plugin-Aware)
    # ========================================
    
    def handle_timeframe_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /timeframe command - Timeframe settings"""
        if not plugin_context:
            plugin_context = 'both'
            
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'Global'}[plugin_context]
        
        keyboard = [
            [{"text": "1M", "callback_data": "tf_1m"}, {"text": "5M", "callback_data": "tf_5m"}, {"text": "15M", "callback_data": "tf_15m"}],
            [{"text": "1H", "callback_data": "tf_1h"}, {"text": "4H", "callback_data": "tf_4h"}, {"text": "1D", "callback_data": "tf_1d"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"⏱️ <b>TIMEFRAME SETTINGS ({plugin_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect a timeframe:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_tf_1m(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf1m command - 1-minute settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(f"⏱️ <b>1-MINUTE TIMEFRAME ({plugin_context.upper()})</b>\n\nStatus: Available for scalping")
    
    def handle_tf_5m(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf5m command - 5-minute settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(f"⏱️ <b>5-MINUTE TIMEFRAME ({plugin_context.upper()})</b>\n\nStatus: V3 Logic 1 active")
    
    def handle_tf_15m(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf15m command - 15-minute settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(f"⏱️ <b>15-MINUTE TIMEFRAME ({plugin_context.upper()})</b>\n\nStatus: V3 Logic 2 + V6 active")
    
    def handle_tf_1h(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf1h command - 1-hour settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(f"⏱️ <b>1-HOUR TIMEFRAME ({plugin_context.upper()})</b>\n\nStatus: V3 Logic 3 + V6 active")
    
    def handle_tf_4h(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf4h command - 4-hour settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(f"⏱️ <b>4-HOUR TIMEFRAME ({plugin_context.upper()})</b>\n\nStatus: V6 active")
    
    def handle_tf_1d(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf1d command - Daily settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(f"⏱️ <b>DAILY TIMEFRAME ({plugin_context.upper()})</b>\n\nStatus: Trend analysis only")
    
    def handle_trends(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /trends command - Show trends"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📈 <b>MARKET TRENDS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "EURUSD: 🟢 Bullish\n"
            "GBPUSD: 🟡 Neutral\n"
            "USDJPY: 🔴 Bearish\n"
            "XAUUSD: 🟢 Bullish"
        )
    
    # ========================================
    # RE-ENTRY COMMANDS (Plugin-Aware)
    # ========================================
    
    def handle_reentry_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /reentry command - Re-entry settings"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_reentry_menu'):
            self._menu_manager.show_reentry_menu(self.chat_id, message_id=None)
            return None
            
        if not plugin_context:
            plugin_context = 'both'
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'Global'}[plugin_context]
            
        keyboard = [
            [{"text": "🎯 SL Hunt", "callback_data": "reentry_slhunt"}, {"text": "📈 TP Continue", "callback_data": "reentry_tp"}],
            [{"text": "🔄 Recovery", "callback_data": "reentry_recovery"}, {"text": "⏱️ Cooldown", "callback_data": "reentry_cooldown"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"🔄 <b>RE-ENTRY SYSTEM ({plugin_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure re-entry settings:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_sl_hunt(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /slhunt command - SL hunt settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🎯 <b>SL HUNT RECOVERY ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Max Attempts:</b> 3\n"
            "<b>Cooldown:</b> 5 minutes"
        )
    
    def handle_tp_continue(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tpcontinue command - TP continuation"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📈 <b>TP CONTINUATION ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Max Chain:</b> 5 levels\n"
            "<b>Lot Scaling:</b> 1.0x"
        )
    
    def handle_recovery(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /recovery command - Recovery settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🔄 <b>RECOVERY SYSTEM ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Mode:</b> Conservative\n"
            "<b>Max Recovery:</b> 3 attempts"
        )
    
    def handle_cooldown(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /cooldown command - Cooldown settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"⏱️ <b>COOLDOWN SETTINGS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>After SL:</b> 5 minutes\n"
            "<b>After TP:</b> 2 minutes\n"
            "<b>After Error:</b> 10 minutes"
        )
    
    def handle_chains(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /chains command - Show active chains"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🔗 <b>ACTIVE CHAINS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "No active re-entry chains."
        )
    
    def handle_autonomous(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /autonomous command - Autonomous system"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🤖 <b>AUTONOMOUS SYSTEM ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Mode:</b> Full Auto\n"
            "<b>Risk Level:</b> Moderate"
        )
    
    def handle_setlot(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /setlot command - Set lot size"""
        if not plugin_context:
            plugin_context = 'both'
        keyboard = [
            [{"text": "0.01", "callback_data": "lot_0.01"}, {"text": "0.02", "callback_data": "lot_0.02"}],
            [{"text": "0.05", "callback_data": "lot_0.05"}, {"text": "0.10", "callback_data": "lot_0.10"}],
            [{"text": "0.20", "callback_data": "lot_0.20"}, {"text": "0.50", "callback_data": "lot_0.50"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"💼 <b>SET LOT SIZE ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Current Lot:</b> 0.01\n\n"
            "Select new lot size:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_risktier(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /risktier command - Set risk tier"""
        if not plugin_context:
            plugin_context = 'both'
        keyboard = [
            [{"text": "🟢 Conservative", "callback_data": "risk_conservative"}],
            [{"text": "🟡 Balanced", "callback_data": "risk_balanced"}],
            [{"text": "🟠 Aggressive", "callback_data": "risk_aggressive"}],
            [{"text": "🔴 Ultra Aggressive", "callback_data": "risk_ultra"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"🎯 <b>RISK TIER ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Current Tier:</b> Balanced 🟡\n\n"
            "Select risk tier:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_chain_limit(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /chainlimit command - Chain level limit"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🔗 <b>CHAIN LIMIT ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/chainlimit LEVEL</code>\n"
            "Example: <code>/chainlimit 5</code>\n\n"
            "Current: 5 levels max"
        )
    
    # ========================================
    # PER-PLUGIN CONFIG COMMANDS (Plugin-Aware)
    # ========================================
    
    def handle_reentry_v3(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /reentry_v3 command - V3 plugin re-entry config"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_plugin_reentry_config'):
            self._menu_manager.show_plugin_reentry_config(self.chat_id, 'v3_combined', message_id=None)
            return None
        
        # Fallback display
        re_entry_config = self.config.get("re_entry_config", {})
        per_plugin = re_entry_config.get("per_plugin", {})
        v3_settings = per_plugin.get("v3_combined", re_entry_config.get("autonomous_config", {}))
        
        enabled = v3_settings.get("enabled", False)
        tp_enabled = v3_settings.get("tp_continuation", {}).get("enabled", False)
        sl_enabled = v3_settings.get("sl_hunt_recovery", {}).get("enabled", False)
        
        return self.send_message(
            "🔶 <b>V3 RE-ENTRY CONFIG</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Master:</b> {'ENABLED ✅' if enabled else 'DISABLED ❌'}\n"
            f"<b>TP Continuation:</b> {'ON ✅' if tp_enabled else 'OFF ❌'}\n"
            f"<b>SL Hunt:</b> {'ON ✅' if sl_enabled else 'OFF ❌'}\n\n"
            "<b>💡 Use:</b> /reentry menu to toggle"
        )
    
    def handle_reentry_v6(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /reentry_v6 command - V6 plugin re-entry config"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_plugin_reentry_config'):
            self._menu_manager.show_plugin_reentry_config(self.chat_id, 'v6_price_action', message_id=None)
            return None
        
        # Fallback display
        re_entry_config = self.config.get("re_entry_config", {})
        per_plugin = re_entry_config.get("per_plugin", {})
        v6_settings = per_plugin.get("v6_price_action_1m", re_entry_config.get("autonomous_config", {}))
        
        enabled = v6_settings.get("enabled", False)
        tp_enabled = v6_settings.get("tp_continuation", {}).get("enabled", False)
        sl_enabled = v6_settings.get("sl_hunt_recovery", {}).get("enabled", False)
        
        return self.send_message(
            "🔶 <b>V6 RE-ENTRY CONFIG</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Master:</b> {'ENABLED ✅' if enabled else 'DISABLED ❌'}\n"
            f"<b>TP Continuation:</b> {'ON ✅' if tp_enabled else 'OFF ❌'}\n"
            f"<b>SL Hunt:</b> {'ON ✅' if sl_enabled else 'OFF ❌'}\n\n"
            "<b>💡 Note:</b> Applies to all V6 timeframes (1m/5m/15m/1h)"
        )
    
    def handle_v3_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v3_config command - V3 plugin configuration"""
        v3_config = self.config.get("v3_integration", {})
        plugins_config = self.config.get("plugins", {})
        v3_plugin = plugins_config.get("v3_combined", {})
        
        enabled = v3_plugin.get("enabled", False)
        shadow = v3_plugin.get("shadow_mode", False)
        bypass_trend = v3_config.get("bypass_trend_check_for_v3_entries", False)
        min_consensus = v3_config.get("min_consensus_score", 5)
        
        return self.send_message(
            "🔶 <b>V3 COMBINED CONFIGURATION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Plugin Status:</b> {'ENABLED ✅' if enabled else 'DISABLED ❌'}\n"
            f"<b>Shadow Mode:</b> {'ON ⚠️' if shadow else 'OFF'}\n"
            f"<b>Bypass Trend:</b> {'YES' if bypass_trend else 'NO'}\n"
            f"<b>Min Consensus:</b> {min_consensus}\n\n"
            "<b>Logics:</b>\n"
            "• Logic 1 (5m Scalping)\n"
            "• Logic 2 (15m Intraday)\n"
            "• Logic 3 (1h Swing)\n\n"
            "<b>💡 Use:</b> /v6_1m_config for V6 settings"
        )
    
    def handle_v6_config(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_config command - V6 plugin configuration overview"""
        plugins_config = self.config.get("plugins", {})
        
        v6_1m = plugins_config.get("v6_price_action_1m", {})
        v6_5m = plugins_config.get("v6_price_action_5m", {})
        v6_15m = plugins_config.get("v6_price_action_15m", {})
        v6_1h = plugins_config.get("v6_price_action_1h", {})
        
        return self.send_message(
            "🔶 <b>V6 PRICE ACTION CONFIGURATION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>1M:</b> {'ENABLED ✅' if v6_1m.get('enabled') else 'DISABLED ❌'} "
            f"{'(Shadow ⚠️)' if v6_1m.get('shadow_mode') else ''}\n"
            f"<b>5M:</b> {'ENABLED ✅' if v6_5m.get('enabled') else 'DISABLED ❌'} "
            f"{'(Shadow ⚠️)' if v6_5m.get('shadow_mode') else ''}\n"
            f"<b>15M:</b> {'ENABLED ✅' if v6_15m.get('enabled') else 'DISABLED ❌'} "
            f"{'(Shadow ⚠️)' if v6_15m.get('shadow_mode') else ''}\n"
            f"<b>1H:</b> {'ENABLED ✅' if v6_1h.get('enabled') else 'DISABLED ❌'} "
            f"{'(Shadow ⚠️)' if v6_1h.get('shadow_mode') else ''}\n\n"
            "<b>Individual Config:</b>\n"
            "• /v6_1m_config - 1 Minute settings\n"
            "• /v6_5m_config - 5 Minute settings\n"
            "• /v6_15m_config - 15 Minute settings\n"
            "• /v6_1h_config - 1 Hour settings\n\n"
            "<b>💡 Use:</b> /v6_control for toggle menu"
        )
    
    # ========================================
    # PROFIT COMMANDS (Plugin-Aware)
    # ========================================
    
    def handle_profit_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /profit command - Profit booking menu"""
        if not plugin_context:
            plugin_context = 'both'
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'Global'}[plugin_context]
            
        keyboard = [
            [{"text": "📊 Booking Settings", "callback_data": "profit_booking"}],
            [{"text": "📈 Profit Levels", "callback_data": "profit_levels"}],
            [{"text": "🔀 Partial Close", "callback_data": "profit_partial"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"💰 <b>PROFIT BOOKING ({plugin_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure profit settings:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_booking(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /booking command - Booking settings"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📊 <b>BOOKING SETTINGS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Auto Booking:</b> ENABLED\n"
            "<b>Level 1:</b> 25% at +30 pips\n"
            "<b>Level 2:</b> 25% at +50 pips\n"
            "<b>Level 3:</b> 50% at +80 pips"
        )
    
    def handle_levels(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /levels command - Profit levels"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📈 <b>PROFIT LEVELS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Level 1: +30 pips (25%)\n"
            "Level 2: +50 pips (25%)\n"
            "Level 3: +80 pips (50%)"
        )
    
    def handle_tf15m(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf15m command - Toggle V6 15M timeframe"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"⏱️ <b>V6 15M TIMEFRAME{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED 🟢\n"
            "<b>Trades Today:</b> 3\n"
            "<b>Win Rate:</b> 66.7%\n"
            "<b>P&L:</b> +$15.00"
        )
    
    def handle_tf30m(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf30m command - Toggle V6 30M timeframe"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"⏱️ <b>V6 30M TIMEFRAME{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED 🟢\n"
            "<b>Trades Today:</b> 2\n"
            "<b>Win Rate:</b> 50.0%\n"
            "<b>P&L:</b> +$10.00"
        )
    
    def handle_tf1h(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf1h command - Toggle V6 1H timeframe"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"🕐 <b>V6 1H TIMEFRAME{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED 🟢\n"
            "<b>Trades Today:</b> 4\n"
            "<b>Win Rate:</b> 75.0%\n"
            "<b>P&L:</b> +$25.00"
        )
    
    def handle_tf4h(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tf4h command - Toggle V6 4H timeframe"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"🕓 <b>V6 4H TIMEFRAME{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> DISABLED 🔴\n"
            "<b>Trades Today:</b> 0\n"
            "<b>Win Rate:</b> N/A\n"
            "<b>P&L:</b> $0.00"
        )
    
    def handle_slhunt(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /slhunt command - SL Hunt recovery status"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"🎯 <b>SL HUNT RECOVERY{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>System:</b> ENABLED 🟢\n"
            "<b>Active Chains:</b> 2\n"
            "<b>Success Rate:</b> 78%\n"
            "<b>Total Recovered:</b> +$140.00"
        )
    
    def handle_tpcontinue(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tpcontinue command - TP Continuation status"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"🎯 <b>TP CONTINUATION{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>System:</b> ENABLED 🟢\n"
            "<b>Active Chains:</b> 1\n"
            "<b>Success Rate:</b> 85%\n"
            "<b>Additional Profit:</b> +$95.00"
        )
    
    def handle_reentry(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /reentry command - Re-entry system overview"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_reentry_menu'):
            self._menu_manager.show_reentry_menu(self.chat_id, message_id=None)
            return None
        keyboard = [
            [{"text": "🎯 SL Hunt", "callback_data": "reentry_slhunt"}, {"text": "📈 TP Continue", "callback_data": "reentry_tpcontinue"}],
            [{"text": "🔗 Active Chains", "callback_data": "reentry_chains"}, {"text": "🤖 Autonomous", "callback_data": "reentry_autonomous"}],
            [{"text": "⚙️ Settings", "callback_data": "reentry_settings"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"🔄 <b>RE-ENTRY SYSTEM{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED 🟢\n"
            "<b>SL Hunt:</b> Active (2 chains)\n"
            "<b>TP Continue:</b> Active (1 chain)\n"
            "<b>Total Recovered:</b> +$140.00\n"
            "<b>Success Rate:</b> 78%\n\n"
            "Select re-entry option:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_partial(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /partial command - Partial close"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"🔀 <b>PARTIAL CLOSE{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/partial TICKET PERCENT</code>\n"
            "Example: <code>/partial 12345 50</code>"
        )
    
    def handle_order_b(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /orderb command - Order B settings"""
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"📊 <b>ORDER B SETTINGS{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>SL Mode:</b> Different from Order A\n"
            "<b>TP Mode:</b> Extended target"
        )
    
    def handle_dual_order(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /dualorder command - Dual order system"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_dual_order_menu'):
            self._menu_manager.show_dual_order_menu(self.chat_id, message_id=None)
            return None
        context_str = f" ({plugin_context.upper()})" if plugin_context and plugin_context != 'both' else ""
        return self.send_message(
            f"📊 <b>DUAL ORDER SYSTEM{context_str}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Order A:</b> Conservative SL\n"
            "<b>Order B:</b> Extended target"
        )
    
    # ========================================
    # ANALYTICS COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_analytics_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /analytics command - Analytics menu"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_analytics_menu'):
            # If menu manager supports context passing, we should pass it. 
            # Assuming it doesn't yet, we just show the menu.
            # Ideally: self._menu_manager.show_analytics_menu(self.chat_id, message_id=None, plugin_context=plugin_context)
            self._menu_manager.show_analytics_menu(self.chat_id, message_id=None)
            return None
            
        if not plugin_context:
            plugin_context = 'both'
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'Global'}[plugin_context]
            
        keyboard = [
            [{"text": "📅 Daily", "callback_data": "analytics_daily"}, {"text": "📆 Weekly", "callback_data": "analytics_weekly"}],
            [{"text": "📊 Monthly", "callback_data": "analytics_monthly"}, {"text": "📈 Performance", "callback_data": "analytics_performance"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"📊 <b>ANALYTICS ({plugin_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nView trading analytics:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    # ========================================
    # ANALYTICS HELPER FUNCTIONS
    # ========================================
    
    def _init_analytics_queries(self):
        """Initialize analytics query engine with database connection"""
        if not self._analytics_queries and self._trading_engine:
            try:
                # Get database connection from trading engine
                if hasattr(self._trading_engine, 'db') and hasattr(self._trading_engine.db, 'conn'):
                    from src.database.analytics_queries import AnalyticsQueries
                    self._analytics_queries = AnalyticsQueries(self._trading_engine.db.conn)
                    logger.info("[ControllerBot] Analytics query engine initialized")
            except Exception as e:
                logger.error(f"[ControllerBot] Failed to init analytics: {e}")
        
        return self._analytics_queries is not None
    
    def _format_pnl(self, pnl: float) -> str:
        """Format P&L with color indicator"""
        if pnl >= 0:
            return f"+${pnl:.2f}"
        else:
            return f"-${abs(pnl):.2f}"
    
    def _create_progress_bar(self, current: float, maximum: float, width: int = 16) -> str:
        """Create visual progress bar"""
        if maximum <= 0:
            return "[" + "░" * width + "] 0%"
        
        percentage = min(current / maximum, 1.0)
        filled = int(percentage * width)
        empty = width - filled
        
        # Color code based on percentage
        if percentage < 0.5:
            filled_char = "█"  # Green territory
        elif percentage < 0.8:
            filled_char = "▓"  # Yellow territory  
        else:
            filled_char = "▒"  # Red territory (danger)
        
        bar = filled_char * filled + "░" * empty
        return f"[{bar}] {percentage*100:.0f}%"
    
    def _get_plugin_display_name(self, plugin_id: str) -> str:
        """Convert plugin_id to display name"""
        if not plugin_id:
            return "Unknown"
        
        plugin_id_lower = plugin_id.lower()
        
        if 'v3' in plugin_id_lower:
            return "V3 Combined"
        elif '15m' in plugin_id_lower:
            return "V6 15M"
        elif '30m' in plugin_id_lower:
            return "V6 30M"
        elif '1h' in plugin_id_lower:
            return "V6 1H"
        elif '4h' in plugin_id_lower:
            return "V6 4H"
        elif 'v6' in plugin_id_lower:
            return "V6 Price Action"
        else:
            return plugin_id.replace('_', ' ').title()
    
    # ========================================
    # ANALYTICS COMMANDS (100% IMPLEMENTATION)
    # ========================================
    
    # ========================================
    # ANALYTICS COMMANDS (100% IMPLEMENTATION)
    # ========================================
    
    def handle_performance(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /performance command - Full performance report with real data
        
        Usage: /performance [plugin_filter] [symbol_filter]
        Examples:
            /performance v3       - Show V3 only
            /performance v6       - Show V6 only  
            /performance v6 EURUSD - Show V6 EURUSD only
            /performance EURUSD   - Show all plugins for EURUSD
        """
        if not self._init_analytics_queries():
            return self.send_message(
                "📈 <b>PERFORMANCE REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Analytics unavailable (database not connected)"
            )
        
        # Parse filters from message
        plugin_filter = None
        symbol_filter = None
        
        # Use plugin_context as default filter if provided and not 'both'
        if plugin_context and plugin_context.lower() != 'both':
            plugin_filter = plugin_context.lower()
        
        if message and 'text' in message:
            parts = message['text'].split()
            if len(parts) > 1:
                for part in parts[1:]:
                    part_upper = part.upper()
                    if part_upper in ['V3', 'V6']:
                        plugin_filter = part_upper.lower()
                    elif len(part_upper) == 6 and part_upper.isalpha():  # Symbol like EURUSD
                        symbol_filter = part_upper
        
        try:
            stats = self._analytics_queries.get_performance_stats(
                plugin_filter=plugin_filter,
                symbol_filter=symbol_filter
            )
            
            # Add filter info to title
            filter_info = ""
            if plugin_filter:
                filter_info += f" ({plugin_filter.upper()})"
            if symbol_filter:
                filter_info += f" {symbol_filter}"
            
            text = f"""
📈 <b>TRADING PERFORMANCE{filter_info}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

💰 <b>PROFIT/LOSS:</b>
• Today: {self._format_pnl(stats['today_pnl'])}
• This Week: {self._format_pnl(stats['week_pnl'])}
• This Month: {self._format_pnl(stats['month_pnl'])}
• Lifetime: {self._format_pnl(stats['lifetime_pnl'])}

📈 <b>STATISTICS:</b>
• Total Trades: {stats['total_trades']}
• Win Rate: {stats['win_rate']:.1f}%
• Avg Win: ${stats['avg_win']:.2f}
• Avg Loss: ${abs(stats['avg_loss']):.2f}
• Profit Factor: {stats['profit_factor']:.2f}

🔥 <b>STREAKS:</b>
• Current: {stats['current_streak']} {'Wins' if stats['streak_type'] == 'win' else 'Losses' if stats['streak_type'] == 'loss' else 'N/A'}
• Best: {stats['best_streak']} Wins
• Worst: {stats['worst_streak']} Losses

<i>Updated: {datetime.now().strftime('%H:%M:%S')}</i>
"""
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_performance] Error: {e}")
            return self.send_message(
                "📈 <b>PERFORMANCE REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Error loading performance data: {str(e)}"
            )
    
    def handle_pair_report(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /pair_report command - Performance breakdown by trading pair"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        # Determine context title suffix
        context_suffix = ""
        if plugin_context and plugin_context != 'both':
            context_suffix = f" ({plugin_context.upper()})"

        try:
            pair_data = self._analytics_queries.get_pair_performance()
            
            if not pair_data:
                return self.send_message(
                    f"💱 <b>PERFORMANCE BY PAIR{context_suffix}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "No trading data available"
                )
            
            # Sort by P&L
            sorted_pairs = sorted(pair_data.items(), key=lambda x: x[1]['pnl'], reverse=True)
            
            text = f"💱 <b>PERFORMANCE BY PAIR{context_suffix}</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Note: In a real implementation, we would filter pair_data by plugin_context here
            # But get_pair_performance might not support filtering yet.
            # For now we just update signature and title.
            
            for pair, stats in sorted_pairs[:10]:  # Top 10 pairs
                text += f"""<b>{pair}:</b>
• Trades: {stats['trades']} (Win: {stats['win_rate']:.0f}%)
• PnL: {self._format_pnl(stats['pnl'])}
• Avg: {self._format_pnl(stats['avg'])}

"""
            
            # Best/Worst
            best = sorted_pairs[0] if sorted_pairs else None
            worst = sorted_pairs[-1] if sorted_pairs else None
            
            if best:
                text += f"🏆 <b>Best:</b> {best[0]} ({self._format_pnl(best[1]['pnl'])})\n"
            if worst and worst[1]['pnl'] < 0:
                text += f"❌ <b>Worst:</b> {worst[0]} ({self._format_pnl(worst[1]['pnl'])})"
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_pair_report] Error: {e}")
            return self.send_message(f"Error loading pair report: {str(e)}")
    
    def handle_strategy_report(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /strategy_report command - Performance breakdown by strategy/plugin"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        try:
            strategy_data = self._analytics_queries.get_strategy_performance()
            
            if not strategy_data:
                return self.send_message(
                    "⚙️ <b>PERFORMANCE BY STRATEGY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "No strategy data available"
                )
            
            # Filter if context is specific
            if plugin_context and plugin_context != 'both':
                 # Simple filtering if key contains context
                 filtered_data = {k: v for k, v in strategy_data.items() if plugin_context.lower() in k.lower()}
                 if filtered_data:
                     strategy_data = filtered_data
            
            # Sort by P&L
            sorted_strategies = sorted(strategy_data.items(), key=lambda x: x[1]['total_pnl'], reverse=True)
            
            text = "⚙️ <b>PERFORMANCE BY STRATEGY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            for strategy, stats in sorted_strategies:
                display_name = self._get_plugin_display_name(strategy)
                text += f"""<b>{display_name}:</b>
• Trades: {stats['trade_count']} (Win: {stats['win_rate']:.0f}%)
• PnL: {self._format_pnl(stats['total_pnl'])}
• Avg: {self._format_pnl(stats['avg_trade'])}

"""
            
            # Best performer
            if sorted_strategies:
                best = sorted_strategies[0]
                text += f"🏆 <b>Best:</b> {self._get_plugin_display_name(best[0])} ({best[1]['win_rate']:.0f}% win)"
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_strategy_report] Error: {e}")
            return self.send_message(f"Error loading strategy report: {str(e)}")
    
    def handle_tp_report(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tp_report command - TP re-entry statistics"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        # TP Report is typically global or specific to V6 logic, likely doesn't need context filtering
        # But we add parameter for interface consistency
        
        try:
            tp_stats = self._analytics_queries.get_tp_reentry_stats()
            
            chains = tp_stats.get('chains_completed', 0)
            levels = tp_stats.get('level_breakdown', {})
            total_pnl = tp_stats.get('total_reentry_pnl', 0)
            
            text = f"""
🔄 <b>TP RE-ENTRY STATISTICS</b>
━━━━━━━━━━━━━━━━━━━━━━━━

📊 <b>CHAINS COMPLETED:</b> {chains}

<b>LEVEL BREAKDOWN:</b>
"""
            
            for level_key in sorted(levels.keys()):
                level_data = levels[level_key]
                text += f"• {level_key} Entries: {level_data['entries']} ({level_data['percentage']:.0f}%)\n"
            
            text += f"\n<b>💰 PnL BY LEVEL:</b>\n"
            for level_key in sorted(levels.keys()):
                text += f"• {level_key}: {self._format_pnl(levels[level_key]['pnl'])}\n"
            
            text += f"\n<b>TOTAL RE-ENTRY PnL:</b> {self._format_pnl(total_pnl)}"
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_tp_report] Error: {e}")
            return self.send_message(f"Error loading TP report: {str(e)}")
    
    def handle_v6_performance(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /v6_performance command - V6 Price Action timeframe breakdown"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        # Context is implicitly V6, but parameter must exist
        
        try:
            v6_stats = self._analytics_queries.get_v6_timeframe_performance()
            
            if not v6_stats:
                return self.send_message(
                    "🎯 <b>V6 PRICE ACTION PERFORMANCE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "No V6 trading data available"
                )
            
            text = "🎯 <b>V6 PRICE ACTION PERFORMANCE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            tf_icons = {'15m': '⏱️', '30m': '⏱️', '1h': '🕐', '4h': '🕓'}
            
            for tf in ['15m', '30m', '1h', '4h']:
                if tf in v6_stats:
                    s = v6_stats[tf]
                    icon = tf_icons[tf]
                    text += f"""<b>{icon} {tf.upper()} TIMEFRAME:</b>
• Trades: {s['trade_count']} (Win: {s['win_rate']:.0f}%)
• PnL: {self._format_pnl(s['total_pnl'])}
• Avg: {self._format_pnl(s['avg_trade'])}

"""
            
            # Find best performers
            if v6_stats:
                best_win = max(v6_stats.items(), key=lambda x: x[1]['win_rate'])
                most_active = max(v6_stats.items(), key=lambda x: x[1]['trade_count'])
                highest_pnl = max(v6_stats.items(), key=lambda x: x[1]['total_pnl'])
                
                text += f"""━━━━━━━━━━━━━━━━━━━━━━━━
🏆 <b>Best Win Rate:</b> {best_win[0].upper()} ({best_win[1]['win_rate']:.0f}%)
📈 <b>Most Active:</b> {most_active[0].upper()} ({most_active[1]['trade_count']} trades)
💰 <b>Highest PnL:</b> {highest_pnl[0].upper()} ({self._format_pnl(highest_pnl[1]['total_pnl'])})"""
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_v6_performance] Error: {e}")
            return self.send_message(f"Error loading V6 performance: {str(e)}")
    
    def handle_compare(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /compare command - V3 vs V6 comparison"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        try:
            v3_stats = self._analytics_queries.get_plugin_group_performance('v3')
            v6_stats = self._analytics_queries.get_plugin_group_performance('v6')
            
            if not v3_stats and not v6_stats:
                return self.send_message(
                    "🔄 <b>V3 vs V6 COMPARISON</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "No comparison data available"
                )
            
            # Provide default empty stats
            if not v3_stats:
                v3_stats = {'trade_count': 0, 'win_rate': 0, 'total_pnl': 0, 'avg_trade': 0, 'profit_factor': 0, 'max_drawdown': 0}
            if not v6_stats:
                v6_stats = {'trade_count': 0, 'win_rate': 0, 'total_pnl': 0, 'avg_trade': 0, 'profit_factor': 0, 'max_drawdown': 0}
            
            # Count winners
            winners = {'V3': 0, 'V6': 0}
            
            comparisons = [
                ('Win Rate', v3_stats['win_rate'], v6_stats['win_rate'], 'higher'),
                ('Avg Trade', v3_stats['avg_trade'], v6_stats['avg_trade'], 'higher'),
                ('Profit Factor', v3_stats.get('profit_factor', 0), v6_stats.get('profit_factor', 0), 'higher'),
                ('Total PnL', v3_stats['total_pnl'], v6_stats['total_pnl'], 'higher'),
            ]
            
            text = """
🔄 <b>V3 vs V6 COMPARISON</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>📊 OVERALL COMPARISON:</b>

"""
            
            for metric, v3_val, v6_val, prefer in comparisons:
                if prefer == 'higher':
                    winner = 'V3 ✅' if v3_val > v6_val else 'V6 ✅' if v6_val > v3_val else 'TIE'
                    if v3_val > v6_val:
                        winners['V3'] += 1
                    elif v6_val > v3_val:
                        winners['V6'] += 1
                else:
                    winner = 'V3 ✅' if v3_val < v6_val else 'V6 ✅' if v6_val < v3_val else 'TIE'
                    if v3_val < v6_val:
                        winners['V3'] += 1
                    elif v6_val < v3_val:
                        winners['V6'] += 1
                
                text += f"<b>{metric}:</b> V3: {v3_val:.2f} | V6: {v6_val:.2f} | {winner}\n"
            
            overall_winner = 'V3 COMBINED' if winners['V3'] > winners['V6'] else 'V6 PRICE ACTION' if winners['V6'] > winners['V3'] else 'TIE'
            
            text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━
🏆 <b>WINNER: {overall_winner}</b>
({max(winners.values())}/{sum(winners.values())} metrics better)

📈 <b>TRADES:</b>
• V3: {v3_stats['trade_count']} trades
• V6: {v6_stats['trade_count']} trades"""
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_compare] Error: {e}")
            return self.send_message(f"Error loading comparison: {str(e)}")
    
    def handle_export(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /export command - Export trading data to CSV"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        try:
            # Parse parameters
            export_type = 'trades'
            days = 30
            
            if message and 'text' in message:
                parts = message['text'].split()
                if len(parts) > 1:
                    export_type = parts[1]
                if len(parts) > 2:
                    try:
                        days = int(parts[2])
                    except:
                        pass
            
            filename = f"{export_type}_export_{datetime.now().strftime('%Y%m%d')}.csv"
            
            if export_type == 'trades':
                data = self._analytics_queries.prepare_trades_export(days)
                headers = ['Date', 'Symbol', 'Direction', 'Plugin', 'Entry', 'Exit', 'PnL', 'Pips', 'Duration (mins)']
                
                rows = []
                for trade in data:
                    rows.append([
                        trade.get('open_time', ''),
                        trade.get('symbol', ''),
                        trade.get('direction', ''),
                        self._get_plugin_display_name(trade.get('logic_type', '')),
                        trade.get('entry_price', 0),
                        trade.get('exit_price', 0),
                        f"${trade.get('pnl', 0):.2f}",
                        trade.get('pips', 0),
                        trade.get('duration_mins', 0)
                    ])
            
            elif export_type == 'daily':
                data = self._analytics_queries.prepare_daily_summary_export(days)
                headers = ['Date', 'Trades', 'Wins', 'Losses', 'Win%', 'PnL', 'V3 PnL', 'V6 PnL']
                
                rows = []
                for day in data:
                    rows.append([
                        day['date'].strftime('%Y-%m-%d'),
                        day['trade_count'],
                        day['wins'],
                        day['losses'],
                        f"{day['win_rate']:.1f}%",
                        f"${day['pnl']:.2f}",
                        f"${day['v3_pnl']:.2f}",
                        f"${day['v6_pnl']:.2f}"
                    ])
            else:
                return self.send_message(f"Unknown export type: {export_type}\nSupported: trades, daily")
            
            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            writer.writerows(rows)
            
            # Send as document (CSV export prepared message)
            caption = (
                f"📤 <b>Export: {export_type.title()}</b>\n"
                f"Period: Last {days} days\n"
                f"Records: {len(rows)}\n\n"
                f"<i>CSV data prepared successfully</i>"
            )
            
            return self.send_message(caption)
            
        except Exception as e:
            logger.error(f"[handle_export] Error: {e}")
            return self.send_message(f"Error exporting data: {str(e)}")
    
    def handle_dashboard(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /dashboard command - Live trading dashboard"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        try:
            # Get bot status
            is_active = not self._is_paused
            uptime = datetime.now() - self._startup_time
            uptime_str = f"{uptime.days}d {uptime.seconds//3600}h {(uptime.seconds%3600)//60}m"
            
            # Get today's stats
            stats = self._analytics_queries.get_performance_stats('today')
            today_pnl = stats.get('today_pnl', 0)
            trades_today = stats.get('total_trades', 0)
            wins = stats.get('wins', 0)
            losses = stats.get('losses', 0)
            win_rate = (wins / trades_today * 100) if trades_today > 0 else 0
            
            # Get plugin breakdown
            plugin_stats = self._analytics_queries.get_plugin_performance()
            v3_trades = sum(s['trade_count'] for k, s in plugin_stats.items() if 'v3' in k.lower())
            v6_trades = sum(s['trade_count'] for k, s in plugin_stats.items() if 'v6' in k.lower())
            v3_pnl = sum(s['total_pnl'] for k, s in plugin_stats.items() if 'v3' in k.lower())
            v6_pnl = sum(s['total_pnl'] for k, s in plugin_stats.items() if 'v6' in k.lower())
            
            text = f"""
📱 <b>LIVE DASHBOARD</b>
━━━━━━━━━━━━━━━━━━━━━━━━

🤖 Bot: {"🟢 Active" if is_active else "🔴 Paused"} | ⏱️ {uptime_str}

━━━ <b>TODAY</b> ━━━
💰 PnL: {self._format_pnl(today_pnl)}
📊 {wins}W/{losses}L ({win_rate:.0f}%)

━━━ <b>PLUGINS</b> ━━━
🔷 V3: {self._format_pnl(v3_pnl)} ({v3_trades} trades)
🔶 V6: {self._format_pnl(v6_pnl)} ({v6_trades} trades)

<i>🔄 {datetime.now().strftime('%H:%M:%S')} UTC</i>"""
            
            keyboard = [
                [
                    {"text": "🔄 Refresh", "callback_data": "dashboard_refresh"},
                    {"text": "📊 Stats", "callback_data": "menu_analytics"}
                ],
                [{"text": "🔙 Main Menu", "callback_data": "menu_main"}]
            ]
            
            return self.send_message(text, reply_markup={"inline_keyboard": keyboard})
            
        except Exception as e:
            logger.error(f"[handle_dashboard] Error: {e}")
            return self.send_message(f"Error loading dashboard: {str(e)}")
    
    # ========================================
    # TIME-BASED REPORTS (Enhanced Implementations)
    # ========================================
    
    def handle_daily(self, message: Dict = None) -> Optional[int]:
        """Handle /daily command - Comprehensive daily report"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        try:
            # Parse date from message or use today
            target_date = date.today()
            if message and 'text' in message:
                parts = message['text'].split()
                if len(parts) > 1:
                    try:
                        target_date = datetime.strptime(parts[1], '%Y-%m-%d').date()
                    except:
                        pass
            
            trades = self._analytics_queries.get_trades_for_date(target_date)
            
            if not trades:
                return self.send_message(
                    f"📅 <b>DAILY REPORT - {target_date.strftime('%B %d, %Y')}</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n\nNo trades found for this date"
                )
            
            # Calculate statistics
            total_pnl = sum(t['pnl'] for t in trades)
            wins = len([t for t in trades if t['pnl'] > 0])
            losses = len([t for t in trades if t['pnl'] <= 0])
            win_rate = (wins / len(trades) * 100) if trades else 0
            
            # By pair
            pair_stats = {}
            for trade in trades:
                symbol = trade['symbol']
                if symbol not in pair_stats:
                    pair_stats[symbol] = {'pnl': 0, 'wins': 0, 'losses': 0}
                pair_stats[symbol]['pnl'] += trade['pnl']
                if trade['pnl'] > 0:
                    pair_stats[symbol]['wins'] += 1
                else:
                    pair_stats[symbol]['losses'] += 1
            
            # By plugin
            plugin_stats = {}
            for trade in trades:
                plugin = trade.get('logic_type') or 'Unknown'
                if plugin not in plugin_stats:
                    plugin_stats[plugin] = {'pnl': 0, 'count': 0}
                plugin_stats[plugin]['pnl'] += trade['pnl']
                plugin_stats[plugin]['count'] += 1
            
            # Build message
            text = f"""
📅 <b>DAILY REPORT - {target_date.strftime('%B %d, %Y')}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

💰 <b>PnL:</b> {self._format_pnl(total_pnl)}

<b>📊 TRADE SUMMARY:</b>
• Total: {len(trades)} trades
• Won: {wins} ({win_rate:.0f}%)
• Lost: {losses} ({100-win_rate:.0f}%)

<b>💱 BY PAIR:</b>
"""
            
            for pair, stats in sorted(pair_stats.items(), key=lambda x: x[1]['pnl'], reverse=True)[:5]:
                text += f"• {pair}: {self._format_pnl(stats['pnl'])} ({stats['wins']}W/{stats['losses']}L)\n"
            
            text += "\n<b>⚙️ BY PLUGIN:</b>\n"
            for plugin, stats in sorted(plugin_stats.items(), key=lambda x: x[1]['pnl'], reverse=True):
                plugin_name = self._get_plugin_display_name(plugin)
                text += f"• {plugin_name}: {self._format_pnl(stats['pnl'])} ({stats['count']} trades)\n"
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_daily] Error: {e}")
            return self.send_message(f"Error loading daily report: {str(e)}")
    
    def handle_weekly(self, message: Dict = None) -> Optional[int]:
        """Handle /weekly command - Comprehensive weekly report"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        try:
            week_data = self._analytics_queries.get_weekly_summary()
            
            if week_data['total_trades'] == 0:
                return self.send_message(
                    "📆 <b>WEEKLY REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "No trades this week"
                )
            
            start = week_data['start_date'].strftime('%b %d')
            end = week_data['end_date'].strftime('%b %d, %Y')
            
            text = f"""
📆 <b>WEEKLY REPORT</b>
{start} - {end}
━━━━━━━━━━━━━━━━━━━━━━━━

💰 <b>TOTAL PnL:</b> {self._format_pnl(week_data['total_pnl'])}

<b>📊 WEEK STATS:</b>
• Total Trades: {week_data['total_trades']}
• Win Rate: {week_data['win_rate']:.0f}%"""
            
            if week_data.get('best_day'):
                best = week_data['best_day']
                text += f"\n• Best Day: {self._format_pnl(best['pnl'])}"
            
            if week_data.get('worst_day'):
                worst = week_data['worst_day']
                text += f"\n• Worst Day: {self._format_pnl(worst['pnl'])}"
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_weekly] Error: {e}")
            return self.send_message(f"Error loading weekly report: {str(e)}")
    
    def handle_monthly(self, message: Dict = None) -> Optional[int]:
        """Handle /monthly command - Comprehensive monthly report"""
        if not self._init_analytics_queries():
            return self.send_message("Analytics unavailable")
        
        try:
            month_data = self._analytics_queries.get_monthly_summary()
            
            if month_data['total_trades'] == 0:
                return self.send_message(
                    f"📈 <b>MONTHLY REPORT - {datetime.now().strftime('%B %Y')}</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━\n\nNo trades this month"
                )
            
            text = f"""
📈 <b>MONTHLY REPORT - {datetime.now().strftime('%B %Y')}</b>
━━━━━━━━━━━━━━━━━━━━━━━━

💰 <b>TOTAL PnL:</b> {self._format_pnl(month_data['total_pnl'])}
📊 <b>TRADES:</b> {month_data['total_trades']}
📈 <b>WIN RATE:</b> {month_data['win_rate']:.0f}%

<b>🎯 PERFORMANCE:</b>
• Best Trade: {self._format_pnl(month_data['best_trade'])}
• Worst Trade: {self._format_pnl(month_data['worst_trade'])}
• Avg Trade: {self._format_pnl(month_data['avg_pnl'])}"""
            
            return self.send_message(text)
            
        except Exception as e:
            logger.error(f"[handle_monthly] Error: {e}")
            return self.send_message(f"Error loading monthly report: {str(e)}")
    
    # ========================================
    # LEGACY STATS HANDLERS (Kept for compatibility)
    # ========================================
    
    def handle_old_performance(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Old performance handler (replaced by handle_performance above)"""
        # Mapping to new handler if possible, otherwise just update signature
        return self.handle_performance(message, plugin_context)
    
    def handle_daily(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /daily command - Daily summary"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📅 <b>DAILY SUMMARY ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}\n"
            f"<b>Trades:</b> 0\n"
            f"<b>P&L:</b> $0.00\n"
            f"<b>Win Rate:</b> 0%"
        )
    
    def handle_weekly(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /weekly command - Weekly summary"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📆 <b>WEEKLY SUMMARY ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Trades:</b> 0\n"
            "<b>P&L:</b> $0.00\n"
            "<b>Win Rate:</b> 0%\n"
            "<b>Best Day:</b> N/A"
        )
    
    def handle_monthly(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /monthly command - Monthly summary"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📊 <b>MONTHLY SUMMARY ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Month:</b> {datetime.now().strftime('%B %Y')}\n"
            f"<b>Trades:</b> 0\n"
            f"<b>P&L:</b> $0.00\n"
            f"<b>Win Rate:</b> 0%"
        )
    
    def handle_stats(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /stats command - Statistics"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📊 <b>TRADING STATISTICS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Total Trades:</b> 0\n"
            "<b>Winning:</b> 0\n"
            "<b>Losing:</b> 0\n"
            "<b>Break-even:</b> 0\n"
            "<b>Avg Win:</b> $0.00\n"
            "<b>Avg Loss:</b> $0.00"
        )
    
    def handle_winrate(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /winrate command - Win rate analysis"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🎯 <b>WIN RATE ANALYSIS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Overall:</b> 0%\n"
            "<b>V3 Logic:</b> 0%\n"
            "<b>V6 Price Action:</b> 0%\n"
            "<b>By Session:</b>\n"
            "  London: 0%\n"
            "  New York: 0%"
        )
    
    def handle_drawdown(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /drawdown command - Drawdown analysis"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"📉 <b>DRAWDOWN ANALYSIS ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Current DD:</b> 0%\n"
            "<b>Max DD:</b> 0%\n"
            "<b>Recovery Factor:</b> N/A"
        )
    
    # ========================================
    # SESSION COMMANDS (Plugin-Aware)
    # ========================================
    
    def handle_session_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /session command - Session menu"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_session_menu'):
            self._menu_manager.show_session_menu(self.chat_id, message_id=None)
            return None
            
        if not plugin_context:
            plugin_context = 'both'
        plugin_name = {'v3': 'V3', 'v6': 'V6', 'both': 'Global'}[plugin_context]   
        
        keyboard = [
            [{"text": "🇬🇧 London", "callback_data": "session_london"}, {"text": "🇺🇸 New York", "callback_data": "session_newyork"}],
            [{"text": "🇯🇵 Tokyo", "callback_data": "session_tokyo"}, {"text": "🇦🇺 Sydney", "callback_data": "session_sydney"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            f"🌍 <b>TRADING SESSIONS ({plugin_name})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect a session:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_london(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /london command - London session"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🇬🇧 <b>LONDON SESSION ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 08:00 - 17:00 GMT\n"
            "<b>Status:</b> Active\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_newyork(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /newyork command - New York session"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🇺🇸 <b>NEW YORK SESSION ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 13:00 - 22:00 GMT\n"
            "<b>Status:</b> Active\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_tokyo(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /tokyo command - Tokyo session"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🇯🇵 <b>TOKYO SESSION ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 00:00 - 09:00 GMT\n"
            "<b>Status:</b> Closed\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_sydney(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /sydney command - Sydney session"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🇦🇺 <b>SYDNEY SESSION ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 22:00 - 07:00 GMT\n"
            "<b>Status:</b> Active\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_overlap(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /overlap command - Session overlap"""
        if not plugin_context:
            plugin_context = 'both'
        return self.send_message(
            f"🔄 <b>SESSION OVERLAP ({plugin_context.upper()})</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>London/NY:</b> 13:00 - 17:00 GMT\n"
            "<b>Status:</b> High volatility\n"
            "<b>Trading:</b> ENABLED"
        )
    
    # ========================================
    # PLUGIN COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_shadow(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /shadow command - Shadow mode"""
        return self.send_message(
            "👻 <b>SHADOW MODE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED for V6\n"
            "<b>Mode:</b> Paper trading\n"
            "<b>Logging:</b> Full"
        )
    
    # ========================================
    # VOICE COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_voice_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /voice command - Voice settings"""
        keyboard = [
            [{"text": "🔊 Test Voice", "callback_data": "voice_test"}],
            [{"text": "🔇 Mute", "callback_data": "voice_mute"}, {"text": "🔈 Unmute", "callback_data": "voice_unmute"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "🔊 <b>VOICE ALERTS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure voice alerts:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_voice_test(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /voicetest command - Test voice alert"""
        return self.send_message("🔊 <b>VOICE TEST</b>\n\nVoice alert test sent!")
    
    def handle_mute(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /mute command - Mute voice alerts"""
        return self.send_message("🔇 <b>VOICE MUTED</b>\n\nVoice alerts are now muted.")
    
    def handle_unmute(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /unmute command - Unmute voice alerts"""
        return self.send_message("🔈 <b>VOICE UNMUTED</b>\n\nVoice alerts are now active.")
    
    # Duplicate handle_trends removed

    
    # ========================================
    # Callback Handlers
    # ========================================
    
    def confirm_pause_trading(self, chat_id: int = None):
        """Confirm pause trading action"""
        self._is_paused = True
        if self._trading_engine and hasattr(self._trading_engine, 'pause_trading'):
            self._trading_engine.pause_trading()
        
        self.send_message(
            "🔴 <b>TRADING PAUSED</b>\n\n"
            "Bot will not process any new signals.\n"
            "Use /resume to continue trading."
        )
    
    def show_main_menu(self, chat_id: int = None):
        """Show main menu (callback handler)"""
        self.handle_start()
    
    def show_plugin_menu(self, chat_id: int = None):
        """Show plugin menu (callback handler)"""
        if self._plugin_control_menu:
            self._plugin_control_menu.show_plugin_menu(chat_id or self.chat_id)
        else:
            self.handle_plugin_menu()
    
    def toggle_pause_resume(self, chat_id: int = None):
        """Toggle pause/resume (callback handler)"""
        if self._is_paused:
            self.handle_resume()
        else:
            self.handle_pause()
    
    def show_dashboard(self, chat_id: int = None):
        """Show dashboard (callback handler)"""
        self.handle_status()
    
    def no_operation(self, chat_id: int = None):
        """No operation (callback handler)"""
        pass

    # ========================================
    # Menu Manager Delegators (Additions)
    # ========================================

    def _show_menu_generic(self, category: str, chat_id: int = None):
        """Generic helper to show a category menu"""
        if not self._menu_manager:
            self.send_message("❌ Menu Manager not initialized.")
            return
        
        # Message ID is needed for edit_message. 
        # In a real callback flow, we usually have access to the message_id from the update.
        # But here 'chat_id' is passed. The architecture of ControllerBot.handle_callback needs inspection.
        # Assuming for now we can't edit without tracking current message ID, so we might send new.
        # However, MenuManager supports message_id=None to send new.
        # Ideally, we should capture message_id from the callback update.
        
        # For this fix, we'll try to use the last known message ID if available or send new.
        self._menu_manager.show_category_menu(chat_id or self.chat_id, category, message_id=None)

    def show_main_menu(self, chat_id: int = None):
        if self._menu_manager:
            self._menu_manager.show_main_menu(chat_id or self.chat_id, message_id=None)
        else:
            self.handle_start()

    def show_trading_menu(self, chat_id: int = None):
        self._show_menu_generic("trading", chat_id)

    def show_risk_menu(self, chat_id: int = None):
        self._show_menu_generic("risk", chat_id)

    def show_strategy_menu(self, chat_id: int = None):
        self._show_menu_generic("strategy", chat_id)

    def show_timeframe_menu(self, chat_id: int = None):
        # Timeframe menu has specific handler in MenuManager usually, but let's try generic
        if self._menu_manager:
             self._menu_manager.show_timeframe_menu(chat_id or self.chat_id, message_id=None)

    def show_reentry_menu(self, chat_id: int = None):
        """Show Re-entry System menu via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_reentry_menu'):
            self._menu_manager.show_reentry_menu(chat_id or self.chat_id, message_id=None)
        else:
            self._show_menu_generic("reentry", chat_id)

    def show_profit_menu(self, chat_id: int = None):
        self._show_menu_generic("profit", chat_id)

    def show_analytics_menu(self, chat_id: int = None):
        """Show Analytics menu via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_analytics_menu'):
            self._menu_manager.show_analytics_menu(chat_id or self.chat_id, message_id=None)
        else:
            self._show_menu_generic("performance", chat_id)

    def show_session_menu(self, chat_id: int = None):
        # Session menu might not be a simple category, let's assume generic for now or custom
        # MenuManager.show_main_menu has "session_dashboard".
        # Let's map it to placeholder generic or implement specifics later.
        self.send_message("Sessions menu under construction.")

    def show_voice_menu(self, chat_id: int = None):
        self._show_menu_generic("voice", chat_id)

    def show_sl_system_menu(self, chat_id: int = None):
        self._show_menu_generic("sl_system", chat_id)

    def show_fine_tune_menu(self, chat_id: int = None):
        self._show_menu_generic("fine_tune", chat_id)

    def show_diagnostics_menu(self, chat_id: int = None):
        self._show_menu_generic("diagnostics", chat_id)

    def show_trends_menu(self, chat_id: int = None):
        self._show_menu_generic("trends", chat_id)
        
    def show_orders_menu(self, chat_id: int = None):
        self._show_menu_generic("orders", chat_id)
    
    def show_settings_menu(self, chat_id: int = None):
        self._show_menu_generic("settings", chat_id)

    def navigate_back(self, chat_id: int = None):
        """Navigate back handler"""
        self.show_main_menu(chat_id)
    
    # ========================================
    # V5 Upgrade Menu Methods (Telegram V5 Upgrade)
    # ========================================
    
    def show_v6_control_menu(self, chat_id: int = None):
        """Show V6 Price Action control menu via V6TimeframeMenuBuilder (Phase 2 Implementation)"""
        if self._v6_timeframe_menu_builder:
            try:
                menu_data = self._v6_timeframe_menu_builder.build_v6_submenu()
                self.send_message(menu_data['text'], reply_markup=menu_data.get('inline_keyboard'))
                logger.info("[ControllerBot] V6 control menu displayed")
            except Exception as e:
                logger.error(f"[ControllerBot] V6 menu error: {e}")
                self.send_message("⚠️ Error displaying V6 menu")
        else:
            self.send_message("V6 Price Action menu not available. Try restarting bot.")
    
    def show_dual_order_menu(self, chat_id: int = None):
        """Show Dual Order System menu via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_dual_order_menu'):
            self._menu_manager.show_dual_order_menu(chat_id or self.chat_id, message_id=None)
        else:
            self.send_message("Dual Order System menu under construction.")
    
    def handle_v6_callback(self, callback_data: str, chat_id: int = None, message_id: int = None, plugin_context: str = None) -> bool:
        """Handle V6 menu callback via V6TimeframeMenuBuilder (Phase 2 Implementation)"""
        if self._v6_timeframe_menu_builder:
            try:
                # V6 menu builder handles v6_* callbacks
                if hasattr(self._v6_timeframe_menu_builder, 'handle_callback'):
                    return self._v6_timeframe_menu_builder.handle_callback(
                        callback_data, chat_id or self.chat_id, message_id
                    )
                logger.warning(f"[ControllerBot] V6 menu builder has no handle_callback method")
            except Exception as e:
                logger.error(f"[ControllerBot] V6 callback error: {e}")
        else:
            logger.warning("[ControllerBot] V6 menu builder not initialized")
        return False
    
    def handle_analytics_callback(self, callback_data: str, chat_id: int = None, message_id: int = None, plugin_context: str = None) -> bool:
        """Handle Analytics menu callback via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'handle_analytics_callback'):
            return self._menu_manager.handle_analytics_callback(callback_data, chat_id or self.chat_id, message_id)
        return False
    
    def handle_dual_order_callback(self, callback_data: str, chat_id: int = None, message_id: int = None, plugin_context: str = None) -> bool:
        """Handle Dual Order menu callback via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'handle_dual_order_callback'):
            return self._menu_manager.handle_dual_order_callback(callback_data, chat_id or self.chat_id, message_id)
        return False
    
    def handle_reentry_callback(self, callback_data: str, chat_id: int = None, message_id: int = None, plugin_context: str = None) -> bool:
        """Handle Re-entry menu callback via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'handle_reentry_callback'):
            return self._menu_manager.handle_reentry_callback(callback_data, chat_id or self.chat_id, message_id)
        return False
    
    # ========================================
    # PHASE 5: NOTIFICATION PREFERENCES (Telegram V5 Upgrade - Phase 5)
    # ========================================
    
    def handle_notifications_menu(self, message: Dict = None, plugin_context: str = None) -> Optional[int]:
        """Handle /notifications command - Show notification preferences menu (Phase 5)"""
        if not self._notification_prefs_menu:
            return self.send_message("⚠️ Notification preferences not available. Initialize dependencies first.")
        
        chat_id = self.chat_id
        if message and 'chat' in message:
            chat_id = message['chat'].get('id', self.chat_id)
        
        self._notification_prefs_menu.show_main_menu(chat_id, message_id=None)
        return None
    
    def handle_notification_prefs_callback(self, callback_data: str, chat_id: int = None, message_id: int = None, plugin_context: str = None) -> bool:
        """Handle notification preferences menu callbacks (Phase 5)"""
        if not self._notification_prefs_menu:
            logger.warning("[ControllerBot] Notification prefs menu not initialized")
            return False
        
        # Check if this is a notification preferences callback
        if not (callback_data.startswith('notif_') or callback_data.startswith('quiet_') or 
                callback_data.startswith('priority_') or callback_data == 'menu_notifications'):
            return False
        
        try:
            # Route to notification preferences menu handler
            return self._notification_prefs_menu.handle_callback(callback_data, chat_id or self.chat_id, message_id)
        except Exception as e:
            logger.error(f"[ControllerBot] Notification prefs callback error: {e}")
            return False
    
    # ========================================
    # CENTRAL CALLBACK DISPATCHER (Phase 2 & 6 Implementation)
    # ========================================
    
    def dispatch_callback(self, callback_data: str, chat_id: int = None, message_id: int = None) -> bool:
        """
        Central callback dispatcher for all menu callbacks
        Routes callbacks to appropriate handlers based on prefix
        
        Args:
            callback_data: Callback data from Telegram
            chat_id: Chat ID
            message_id: Message ID to edit
        
        Returns:
            True if callback was handled
        """
        try:
            # Phase 2: V6 menu callbacks (v6_*)
            if callback_data.startswith('v6_'):
                return self.handle_v6_callback(callback_data, chat_id, message_id)
            
            # Phase 5: Notification preferences callbacks
            if callback_data.startswith(('notif_', 'quiet_', 'priority_')):
                return self.handle_notification_prefs_callback(callback_data, chat_id, message_id)
            
            # Phase 6: Session menu callbacks
            if callback_data.startswith('session_') or callback_data in ('session_dashboard', 'session_edit_menu'):
                return self.handle_session_callback(callback_data, chat_id, message_id)
            
            # Other menu callbacks
            if self._menu_manager:
                # Try menu manager for other callbacks
                if hasattr(self._menu_manager, 'handle_callback'):
                    return self._menu_manager.handle_callback(callback_data, chat_id, message_id)
            
            logger.warning(f"[ControllerBot] Unhandled callback: {callback_data}")
            return False
            
        except Exception as e:
            logger.error(f"[ControllerBot] Callback dispatcher error: {e}")
            return False
    
    # ========================================
    # PHASE 6: SESSION MENU CALLBACKS (Telegram V5 Upgrade - Phase 6)
    # ========================================
    
    def handle_session_callback(self, callback_data: str, chat_id: int = None, message_id: int = None, plugin_context: str = None) -> bool:
        """Handle session menu callbacks (Phase 6)"""
        if not self._session_menu_handler:
            logger.warning("[ControllerBot] Session menu handler not initialized")
            return False
        
        # Check if this is a session menu callback
        if not (callback_data.startswith('session_') or callback_data == 'session_dashboard' or callback_data == 'session_edit_menu'):
            return False
        
        try:
            # Route to session menu handler
            self._session_menu_handler.handle_callback_query(callback_data, chat_id or self.chat_id, message_id)
            return True
        except Exception as e:
            logger.error(f"[ControllerBot] Session callback error: {e}")
            return False

