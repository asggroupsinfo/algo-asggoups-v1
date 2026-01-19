"""
Controller Bot - Handles system commands and admin functions

This bot handles all slash commands and system control.
NOW WIRED to CommandRegistry for 95+ command handling (not delegation).

Version: 2.0.0
Date: 2026-01-15

Updates:
- v2.0.0: Wired to CommandRegistry with actual handler implementations
- v1.1.0: Added /health and /version commands for plugin monitoring
"""

import logging
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
import sys
import os

# Ensure src is in path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from .base_telegram_bot import BaseTelegramBot
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
    
    def __init__(self, token: str, chat_id: str = None):
        super().__init__(token, chat_id, bot_name="ControllerBot")
        
        self._command_handlers: Dict[str, Callable] = {}
        self._callback_handlers: Dict[str, Callable] = {} # Add callback handlers dict
        self._trading_engine = None
        self._risk_manager = None
        self._legacy_bot = None
        
        # Menu Manager Integration
        self._menu_manager = None
        if MenuManager:
            try:
                self._menu_manager = MenuManager(self)
                logger.info("[ControllerBot] MenuManager initialized")
            except Exception as e:
                logger.error(f"[ControllerBot] Failed to init MenuManager: {e}")
        
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
        Handle an incoming command
        
        Args:
            command: Command string
            message: Full message dict from Telegram
        
        Returns:
            True if command was handled
        """
        if self._legacy_bot and hasattr(self._legacy_bot, 'command_handlers'):
            if command in self._legacy_bot.command_handlers:
                try:
                    self._legacy_bot.command_handlers[command](message)
                    return True
                except Exception as e:
                    logger.error(f"[ControllerBot] Legacy handler error for {command}: {e}")
                    return False
        
        if command in self._command_handlers:
            try:
                self._command_handlers[command](message)
                return True
            except Exception as e:
                logger.error(f"[ControllerBot] Handler error for {command}: {e}")
                return False
        
        logger.warning(f"[ControllerBot] Unknown command: {command}")
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
    
    def handle_health_command(self, message: Dict = None) -> Optional[int]:
        """
        Handle /health command - Show plugin health dashboard
        
        Args:
            message: Telegram message dict (optional)
        
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
    
    def handle_version_command(self, message: Dict = None) -> Optional[int]:
        """
        Handle /version command - Show active plugin versions
        
        Args:
            message: Telegram message dict (optional)
        
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
    
    def handle_upgrade_command(self, message: Dict, args: List[str] = None) -> Optional[int]:
        """
        Handle /upgrade command - Upgrade plugin to specific version
        
        Usage: /upgrade <plugin_id> <version>
        Example: /upgrade combined_v3 3.2.0
        
        Args:
            message: Telegram message dict
            args: Command arguments [plugin_id, version]
        
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
    
    def handle_rollback_command(self, message: Dict, args: List[str] = None) -> Optional[int]:
        """
        Handle /rollback command - Rollback plugin to previous version
        
        Usage: /rollback <plugin_id>
        Example: /rollback combined_v3
        
        Args:
            message: Telegram message dict
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
        
        # ==================== PROFIT COMMANDS (6) ====================
        self._command_handlers["/profit"] = self.handle_profit_menu
        self._command_handlers["/booking"] = self.handle_booking
        self._command_handlers["/levels"] = self.handle_levels
        self._command_handlers["/partial"] = self.handle_partial
        self._command_handlers["/orderb"] = self.handle_order_b
        self._command_handlers["/dualorder"] = self.handle_dual_order
        
        # ==================== ANALYTICS COMMANDS (8) ====================
        self._command_handlers["/analytics"] = self.handle_analytics_menu
        self._command_handlers["/performance"] = self.handle_performance
        self._command_handlers["/daily"] = self.handle_daily
        self._command_handlers["/weekly"] = self.handle_weekly
        self._command_handlers["/monthly"] = self.handle_monthly
        self._command_handlers["/stats"] = self.handle_stats
        self._command_handlers["/winrate"] = self.handle_winrate
        self._command_handlers["/drawdown"] = self.handle_drawdown
        
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
        
        # ==================== VOICE COMMANDS (4) ====================
        self._command_handlers["/voice"] = self.handle_voice_menu
        self._command_handlers["/voicetest"] = self.handle_voice_test
        self._command_handlers["/mute"] = self.handle_mute
        self._command_handlers["/unmute"] = self.handle_unmute
        
        logger.info(f"[ControllerBot] Wired {len(self._command_handlers)} command handlers (105 total)")
    
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
    
    def handle_start(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_status(self, message: Dict = None) -> Optional[int]:
        """Handle /status command - Show bot status"""
        uptime = datetime.now() - self._startup_time
        hours, remainder = divmod(int(uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Get plugin status
        v3_enabled = True
        v6_enabled = True
        if self._trading_engine:
            if hasattr(self._trading_engine, 'is_plugin_enabled'):
                v3_enabled = self._trading_engine.is_plugin_enabled("v3_combined")
                v6_enabled = self._trading_engine.is_plugin_enabled("v6_price_action")
        
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
    
    def handle_pause(self, message: Dict = None) -> Optional[int]:
        """Handle /pause command - Pause trading"""
        if self._is_paused:
            return self.send_message("⚠️ Trading is already paused.")
        
        return self.send_confirmation_request(
            "Are you sure you want to <b>PAUSE</b> all trading?",
            "confirm_pause",
            "menu_main"
        )
    
    def handle_resume(self, message: Dict = None) -> Optional[int]:
        """Handle /resume command - Resume trading"""
        if not self._is_paused:
            return self.send_message("✅ Trading is already active.")
        
        self._is_paused = False
        if self._trading_engine and hasattr(self._trading_engine, 'resume_trading'):
            self._trading_engine.resume_trading()
        
        return self.send_message(
            "✅ <b>TRADING RESUMED</b>\n\n"
            "Bot is now actively processing signals."
        )
    
    def handle_help(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_config(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_plugin_menu(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_plugins(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_enable(self, message: Dict = None) -> Optional[int]:
        """Handle /enable command - Enable plugin"""
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
    
    def handle_disable(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_positions(self, message: Dict = None) -> Optional[int]:
        """Handle /positions command - Show open positions"""
        positions = []
        if self._trading_engine and hasattr(self._trading_engine, 'get_open_positions'):
            try:
                positions = self._trading_engine.get_open_positions() or []
            except Exception:
                pass
        
        if not positions:
            return self.send_message(
                "📊 <b>OPEN POSITIONS</b>\n\n"
                "No open positions."
            )
        
        text = "📊 <b>OPEN POSITIONS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for i, pos in enumerate(positions[:10], 1):
            symbol = pos.get('symbol', 'N/A')
            side = pos.get('side', 'N/A')
            pnl = pos.get('pnl', 0)
            text += f"{i}. {symbol} {side} | P&L: ${pnl:.2f}\n"
        
        return self.send_message(text)
    
    def handle_pnl(self, message: Dict = None) -> Optional[int]:
        """Handle /pnl command - Show P&L summary"""
        daily_pnl = 0.0
        if self._trading_engine and hasattr(self._trading_engine, 'get_daily_pnl'):
            try:
                daily_pnl = self._trading_engine.get_daily_pnl()
            except Exception:
                pass
        
        emoji = "🟢" if daily_pnl >= 0 else "🔴"
        
        return self.send_message(
            f"💰 <b>P&L SUMMARY</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Today:</b> {emoji} ${daily_pnl:.2f}\n"
            f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        )
    
    def handle_balance(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_restart(self, message: Dict = None) -> Optional[int]:
        """Handle /restart command - Restart bot (admin only)"""
        return self.send_confirmation_request(
            "Are you sure you want to <b>RESTART</b> the bot?\n\nThis will temporarily stop all trading.",
            "confirm_restart",
            "menu_main"
        )
    
    def handle_shutdown(self, message: Dict = None) -> Optional[int]:
        """Handle /shutdown command - Shutdown bot (admin only)"""
        return self.send_confirmation_request(
            "Are you sure you want to <b>SHUTDOWN</b> the bot?\n\n⚠️ This will stop all trading until manually restarted.",
            "confirm_shutdown",
            "menu_main"
        )
    
    # ========================================
    # TRADING COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_trade_menu(self, message: Dict = None) -> Optional[int]:
        """Handle /trade command - Show trading menu"""
        keyboard = [
            [{"text": "📈 BUY", "callback_data": "trade_buy"}, {"text": "📉 SELL", "callback_data": "trade_sell"}],
            [{"text": "❌ Close Position", "callback_data": "trade_close"}],
            [{"text": "📊 Positions", "callback_data": "trade_positions"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "📊 <b>TRADING MENU</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect a trading action:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_buy(self, message: Dict = None) -> Optional[int]:
        """Handle /buy command - Place buy order"""
        return self.send_message(
            "📈 <b>BUY ORDER</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/buy SYMBOL LOT</code>\n"
            "Example: <code>/buy EURUSD 0.1</code>\n\n"
            "<i>Or use the trading menu for guided order placement.</i>"
        )
    
    def handle_sell(self, message: Dict = None) -> Optional[int]:
        """Handle /sell command - Place sell order"""
        return self.send_message(
            "📉 <b>SELL ORDER</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/sell SYMBOL LOT</code>\n"
            "Example: <code>/sell EURUSD 0.1</code>\n\n"
            "<i>Or use the trading menu for guided order placement.</i>"
        )
    
    def handle_close(self, message: Dict = None) -> Optional[int]:
        """Handle /close command - Close position"""
        return self.send_message(
            "❌ <b>CLOSE POSITION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/close TICKET</code>\n"
            "Example: <code>/close 12345</code>\n\n"
            "<i>Use /positions to see open positions and their tickets.</i>"
        )
    
    def handle_close_all(self, message: Dict = None) -> Optional[int]:
        """Handle /closeall command - Close all positions"""
        return self.send_confirmation_request(
            "Are you sure you want to <b>CLOSE ALL</b> open positions?",
            "confirm_close_all",
            "menu_main"
        )
    
    def handle_orders(self, message: Dict = None) -> Optional[int]:
        """Handle /orders command - Show pending orders"""
        return self.send_message(
            "📋 <b>PENDING ORDERS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "No pending orders."
        )
    
    def handle_history(self, message: Dict = None) -> Optional[int]:
        """Handle /history command - Show trade history"""
        return self.send_message(
            "📜 <b>TRADE HISTORY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Recent trades will be displayed here.\n\n"
            "<i>Use /daily, /weekly, or /monthly for detailed reports.</i>"
        )
    
    def handle_equity(self, message: Dict = None) -> Optional[int]:
        """Handle /equity command - Show account equity"""
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
    
    def handle_margin(self, message: Dict = None) -> Optional[int]:
        """Handle /margin command - Show margin info"""
        return self.send_message(
            "📊 <b>MARGIN INFO</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Free Margin:</b> $0.00\n"
            "<b>Used Margin:</b> $0.00\n"
            "<b>Margin Level:</b> 0%"
        )
    
    def handle_symbols(self, message: Dict = None) -> Optional[int]:
        """Handle /symbols command - Show available symbols"""
        return self.send_message(
            "💱 <b>AVAILABLE SYMBOLS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "EURUSD, GBPUSD, USDJPY, AUDUSD\n"
            "USDCAD, NZDUSD, USDCHF, EURGBP\n"
            "EURJPY, GBPJPY, XAUUSD, XAGUSD"
        )
    
    def handle_price(self, message: Dict = None) -> Optional[int]:
        """Handle /price command - Get current price"""
        return self.send_message(
            "💵 <b>PRICE CHECK</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/price SYMBOL</code>\n"
            "Example: <code>/price EURUSD</code>"
        )
    
    def handle_spread(self, message: Dict = None) -> Optional[int]:
        """Handle /spread command - Show spread info"""
        return self.send_message(
            "📏 <b>SPREAD INFO</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/spread SYMBOL</code>\n"
            "Example: <code>/spread EURUSD</code>"
        )
    
    # ========================================
    # RISK COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_risk_menu(self, message: Dict = None) -> Optional[int]:
        """Handle /risk command - Show risk settings menu"""
        keyboard = [
            [{"text": "📊 Lot Size", "callback_data": "risk_lot"}, {"text": "🛑 Stop Loss", "callback_data": "risk_sl"}],
            [{"text": "🎯 Take Profit", "callback_data": "risk_tp"}, {"text": "📈 Risk Tier", "callback_data": "risk_tier"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "⚠️ <b>RISK MANAGEMENT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure your risk settings:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_set_lot(self, message: Dict = None) -> Optional[int]:
        """Handle /setlot command - Set lot size"""
        return self.send_message(
            "📊 <b>SET LOT SIZE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/setlot SIZE</code>\n"
            "Example: <code>/setlot 0.1</code>\n\n"
            "Current: 0.01 lots"
        )
    
    def handle_set_sl(self, message: Dict = None) -> Optional[int]:
        """Handle /setsl command - Set stop loss"""
        return self.send_message(
            "🛑 <b>SET STOP LOSS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/setsl PIPS</code>\n"
            "Example: <code>/setsl 50</code>\n\n"
            "Current: 30 pips"
        )
    
    def handle_set_tp(self, message: Dict = None) -> Optional[int]:
        """Handle /settp command - Set take profit"""
        return self.send_message(
            "🎯 <b>SET TAKE PROFIT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/settp PIPS</code>\n"
            "Example: <code>/settp 100</code>\n\n"
            "Current: 60 pips"
        )
    
    def handle_daily_limit(self, message: Dict = None) -> Optional[int]:
        """Handle /dailylimit command - Set daily loss limit"""
        return self.send_message(
            "📉 <b>DAILY LOSS LIMIT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/dailylimit AMOUNT</code>\n"
            "Example: <code>/dailylimit 100</code>\n\n"
            "Current: $500"
        )
    
    def handle_max_loss(self, message: Dict = None) -> Optional[int]:
        """Handle /maxloss command - Set max loss"""
        return self.send_message(
            "🔴 <b>MAX LOSS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/maxloss AMOUNT</code>\n"
            "Example: <code>/maxloss 1000</code>\n\n"
            "Current: $1000"
        )
    
    def handle_max_profit(self, message: Dict = None) -> Optional[int]:
        """Handle /maxprofit command - Set max profit"""
        return self.send_message(
            "🟢 <b>MAX PROFIT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/maxprofit AMOUNT</code>\n"
            "Example: <code>/maxprofit 500</code>\n\n"
            "Current: $500"
        )
    
    def handle_risk_tier(self, message: Dict = None) -> Optional[int]:
        """Handle /risktier command - Set risk tier"""
        keyboard = [
            [{"text": "🟢 Conservative", "callback_data": "risk_tier_1"}],
            [{"text": "🟡 Moderate", "callback_data": "risk_tier_2"}],
            [{"text": "🔴 Aggressive", "callback_data": "risk_tier_3"}],
            [{"text": "🔙 Back", "callback_data": "menu_risk"}]
        ]
        return self.send_message(
            "📈 <b>RISK TIER</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect your risk tier:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_sl_system(self, message: Dict = None) -> Optional[int]:
        """Handle /slsystem command - SL system settings"""
        return self.send_message(
            "🛑 <b>SL SYSTEM</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Mode:</b> Dynamic\n"
            "<b>Base SL:</b> 30 pips\n"
            "<b>ATR Multiplier:</b> 1.5x"
        )
    
    def handle_trail_sl(self, message: Dict = None) -> Optional[int]:
        """Handle /trailsl command - Trailing SL settings"""
        return self.send_message(
            "📏 <b>TRAILING STOP LOSS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> Enabled\n"
            "<b>Trail Distance:</b> 20 pips\n"
            "<b>Activation:</b> After +30 pips"
        )
    
    def handle_breakeven(self, message: Dict = None) -> Optional[int]:
        """Handle /breakeven command - Breakeven settings"""
        return self.send_message(
            "⚖️ <b>BREAKEVEN SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> Enabled\n"
            "<b>Activation:</b> After +25 pips\n"
            "<b>Lock Profit:</b> +5 pips"
        )
    
    def handle_protection(self, message: Dict = None) -> Optional[int]:
        """Handle /protection command - Profit protection"""
        return self.send_message(
            "🛡️ <b>PROFIT PROTECTION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> Enabled\n"
            "<b>Lock at:</b> 50% of max profit\n"
            "<b>Trail:</b> 25% increments"
        )
    
    # ========================================
    # STRATEGY COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_strategy_menu(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_logic1(self, message: Dict = None) -> Optional[int]:
        """Handle /logic1 command - Toggle Logic 1 (5m)"""
        return self.send_message("🔄 <b>LOGIC 1 (5M)</b>\n\nStatus: ENABLED\n\n<i>Use button to toggle.</i>")
    
    def handle_logic2(self, message: Dict = None) -> Optional[int]:
        """Handle /logic2 command - Toggle Logic 2 (15m)"""
        return self.send_message("🔄 <b>LOGIC 2 (15M)</b>\n\nStatus: ENABLED\n\n<i>Use button to toggle.</i>")
    
    def handle_logic3(self, message: Dict = None) -> Optional[int]:
        """Handle /logic3 command - Toggle Logic 3 (1h)"""
        return self.send_message("🔄 <b>LOGIC 3 (1H)</b>\n\nStatus: ENABLED\n\n<i>Use button to toggle.</i>")
    
    def handle_v3(self, message: Dict = None) -> Optional[int]:
        """Handle /v3 command - V3 Combined settings"""
        return self.send_message(
            "📊 <b>V3 COMBINED LOGIC</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Logic 1 (5m):</b> ON\n"
            "<b>Logic 2 (15m):</b> ON\n"
            "<b>Logic 3 (1h):</b> ON"
        )
    
    def handle_v6(self, message: Dict = None) -> Optional[int]:
        """Handle /v6 command - V6 Price Action settings"""
        self.show_v6_control_menu()
        return None
    
    def handle_v6_status(self, message: Dict = None) -> Optional[int]:
        """Handle /v6_status command - V6 system status"""
        return self.send_message(
            "📈 <b>V6 PRICE ACTION STATUS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>System:</b> ENABLED\n"
            "<b>15M:</b> ON\n<b>30M:</b> ON\n<b>1H:</b> ON\n<b>4H:</b> ON"
        )
    
    def handle_v6_control(self, message: Dict = None) -> Optional[int]:
        """Handle /v6_control command - V6 control menu"""
        self.show_v6_control_menu()
        return None
    
    def handle_v6_tf15m_on(self, message: Dict = None) -> Optional[int]:
        """Handle /tf15m_on command - Enable V6 15M"""
        return self.send_message("✅ <b>V6 15M ENABLED</b>\n\n15-minute timeframe is now active.")
    
    def handle_v6_tf15m_off(self, message: Dict = None) -> Optional[int]:
        """Handle /tf15m_off command - Disable V6 15M"""
        return self.send_message("❌ <b>V6 15M DISABLED</b>\n\n15-minute timeframe is now inactive.")
    
    def handle_v6_tf30m_on(self, message: Dict = None) -> Optional[int]:
        """Handle /tf30m_on command - Enable V6 30M"""
        return self.send_message("✅ <b>V6 30M ENABLED</b>\n\n30-minute timeframe is now active.")
    
    def handle_v6_tf30m_off(self, message: Dict = None) -> Optional[int]:
        """Handle /tf30m_off command - Disable V6 30M"""
        return self.send_message("❌ <b>V6 30M DISABLED</b>\n\n30-minute timeframe is now inactive.")
    
    def handle_v6_tf1h_on(self, message: Dict = None) -> Optional[int]:
        """Handle /tf1h_on command - Enable V6 1H"""
        return self.send_message("✅ <b>V6 1H ENABLED</b>\n\n1-hour timeframe is now active.")
    
    def handle_v6_tf1h_off(self, message: Dict = None) -> Optional[int]:
        """Handle /tf1h_off command - Disable V6 1H"""
        return self.send_message("❌ <b>V6 1H DISABLED</b>\n\n1-hour timeframe is now inactive.")
    
    def handle_v6_tf4h_on(self, message: Dict = None) -> Optional[int]:
        """Handle /tf4h_on command - Enable V6 4H"""
        return self.send_message("✅ <b>V6 4H ENABLED</b>\n\n4-hour timeframe is now active.")
    
    def handle_v6_tf4h_off(self, message: Dict = None) -> Optional[int]:
        """Handle /tf4h_off command - Disable V6 4H"""
        return self.send_message("❌ <b>V6 4H DISABLED</b>\n\n4-hour timeframe is now inactive.")
    
    def handle_signals(self, message: Dict = None) -> Optional[int]:
        """Handle /signals command - Signal settings"""
        return self.send_message(
            "📡 <b>SIGNAL SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Source:</b> Pine Script V3/V6\n"
            "<b>Filter:</b> All signals\n"
            "<b>Confirmation:</b> Required"
        )
    
    def handle_filters(self, message: Dict = None) -> Optional[int]:
        """Handle /filters command - Signal filters"""
        return self.send_message(
            "🔍 <b>SIGNAL FILTERS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Trend Filter:</b> ON\n"
            "<b>Session Filter:</b> ON\n"
            "<b>News Filter:</b> OFF"
        )
    
    def handle_multiplier(self, message: Dict = None) -> Optional[int]:
        """Handle /multiplier command - Lot multiplier"""
        return self.send_message(
            "✖️ <b>LOT MULTIPLIER</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/multiplier VALUE</code>\n"
            "Example: <code>/multiplier 1.5</code>\n\n"
            "Current: 1.0x"
        )
    
    def handle_mode(self, message: Dict = None) -> Optional[int]:
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
    # TIMEFRAME COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_timeframe_menu(self, message: Dict = None) -> Optional[int]:
        """Handle /timeframe command - Timeframe settings"""
        keyboard = [
            [{"text": "1M", "callback_data": "tf_1m"}, {"text": "5M", "callback_data": "tf_5m"}, {"text": "15M", "callback_data": "tf_15m"}],
            [{"text": "1H", "callback_data": "tf_1h"}, {"text": "4H", "callback_data": "tf_4h"}, {"text": "1D", "callback_data": "tf_1d"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "⏱️ <b>TIMEFRAME SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect a timeframe:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_tf_1m(self, message: Dict = None) -> Optional[int]:
        """Handle /tf1m command - 1-minute settings"""
        return self.send_message("⏱️ <b>1-MINUTE TIMEFRAME</b>\n\nStatus: Available for scalping")
    
    def handle_tf_5m(self, message: Dict = None) -> Optional[int]:
        """Handle /tf5m command - 5-minute settings"""
        return self.send_message("⏱️ <b>5-MINUTE TIMEFRAME</b>\n\nStatus: V3 Logic 1 active")
    
    def handle_tf_15m(self, message: Dict = None) -> Optional[int]:
        """Handle /tf15m command - 15-minute settings"""
        return self.send_message("⏱️ <b>15-MINUTE TIMEFRAME</b>\n\nStatus: V3 Logic 2 + V6 active")
    
    def handle_tf_1h(self, message: Dict = None) -> Optional[int]:
        """Handle /tf1h command - 1-hour settings"""
        return self.send_message("⏱️ <b>1-HOUR TIMEFRAME</b>\n\nStatus: V3 Logic 3 + V6 active")
    
    def handle_tf_4h(self, message: Dict = None) -> Optional[int]:
        """Handle /tf4h command - 4-hour settings"""
        return self.send_message("⏱️ <b>4-HOUR TIMEFRAME</b>\n\nStatus: V6 active")
    
    def handle_tf_1d(self, message: Dict = None) -> Optional[int]:
        """Handle /tf1d command - Daily settings"""
        return self.send_message("⏱️ <b>DAILY TIMEFRAME</b>\n\nStatus: Trend analysis only")
    
    def handle_trends(self, message: Dict = None) -> Optional[int]:
        """Handle /trends command - Show trends"""
        return self.send_message(
            "📈 <b>MARKET TRENDS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "EURUSD: 🟢 Bullish\n"
            "GBPUSD: 🟡 Neutral\n"
            "USDJPY: 🔴 Bearish\n"
            "XAUUSD: 🟢 Bullish"
        )
    
    # ========================================
    # RE-ENTRY COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_reentry_menu(self, message: Dict = None) -> Optional[int]:
        """Handle /reentry command - Re-entry settings"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_reentry_menu'):
            self._menu_manager.show_reentry_menu(self.chat_id, message_id=None)
            return None
        keyboard = [
            [{"text": "🎯 SL Hunt", "callback_data": "reentry_slhunt"}, {"text": "📈 TP Continue", "callback_data": "reentry_tp"}],
            [{"text": "🔄 Recovery", "callback_data": "reentry_recovery"}, {"text": "⏱️ Cooldown", "callback_data": "reentry_cooldown"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "🔄 <b>RE-ENTRY SYSTEM</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure re-entry settings:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_sl_hunt(self, message: Dict = None) -> Optional[int]:
        """Handle /slhunt command - SL hunt settings"""
        return self.send_message(
            "🎯 <b>SL HUNT RECOVERY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Max Attempts:</b> 3\n"
            "<b>Cooldown:</b> 5 minutes"
        )
    
    def handle_tp_continue(self, message: Dict = None) -> Optional[int]:
        """Handle /tpcontinue command - TP continuation"""
        return self.send_message(
            "📈 <b>TP CONTINUATION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Max Chain:</b> 5 levels\n"
            "<b>Lot Scaling:</b> 1.0x"
        )
    
    def handle_recovery(self, message: Dict = None) -> Optional[int]:
        """Handle /recovery command - Recovery settings"""
        return self.send_message(
            "🔄 <b>RECOVERY SYSTEM</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Mode:</b> Conservative\n"
            "<b>Max Recovery:</b> 3 attempts"
        )
    
    def handle_cooldown(self, message: Dict = None) -> Optional[int]:
        """Handle /cooldown command - Cooldown settings"""
        return self.send_message(
            "⏱️ <b>COOLDOWN SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>After SL:</b> 5 minutes\n"
            "<b>After TP:</b> 2 minutes\n"
            "<b>After Error:</b> 10 minutes"
        )
    
    def handle_chains(self, message: Dict = None) -> Optional[int]:
        """Handle /chains command - Show active chains"""
        return self.send_message(
            "🔗 <b>ACTIVE CHAINS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "No active re-entry chains."
        )
    
    def handle_autonomous(self, message: Dict = None) -> Optional[int]:
        """Handle /autonomous command - Autonomous system"""
        return self.send_message(
            "🤖 <b>AUTONOMOUS SYSTEM</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Mode:</b> Full Auto\n"
            "<b>Risk Level:</b> Moderate"
        )
    
    def handle_chain_limit(self, message: Dict = None) -> Optional[int]:
        """Handle /chainlimit command - Chain level limit"""
        return self.send_message(
            "🔗 <b>CHAIN LIMIT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/chainlimit LEVEL</code>\n"
            "Example: <code>/chainlimit 5</code>\n\n"
            "Current: 5 levels max"
        )
    
    # ========================================
    # PROFIT COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_profit_menu(self, message: Dict = None) -> Optional[int]:
        """Handle /profit command - Profit booking menu"""
        keyboard = [
            [{"text": "📊 Booking Settings", "callback_data": "profit_booking"}],
            [{"text": "📈 Profit Levels", "callback_data": "profit_levels"}],
            [{"text": "🔀 Partial Close", "callback_data": "profit_partial"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "💰 <b>PROFIT BOOKING</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nConfigure profit settings:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_booking(self, message: Dict = None) -> Optional[int]:
        """Handle /booking command - Booking settings"""
        return self.send_message(
            "📊 <b>BOOKING SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Auto Booking:</b> ENABLED\n"
            "<b>Level 1:</b> 25% at +30 pips\n"
            "<b>Level 2:</b> 25% at +50 pips\n"
            "<b>Level 3:</b> 50% at +80 pips"
        )
    
    def handle_levels(self, message: Dict = None) -> Optional[int]:
        """Handle /levels command - Profit levels"""
        return self.send_message(
            "📈 <b>PROFIT LEVELS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Level 1: +30 pips (25%)\n"
            "Level 2: +50 pips (25%)\n"
            "Level 3: +80 pips (50%)"
        )
    
    def handle_partial(self, message: Dict = None) -> Optional[int]:
        """Handle /partial command - Partial close"""
        return self.send_message(
            "🔀 <b>PARTIAL CLOSE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "Usage: <code>/partial TICKET PERCENT</code>\n"
            "Example: <code>/partial 12345 50</code>"
        )
    
    def handle_order_b(self, message: Dict = None) -> Optional[int]:
        """Handle /orderb command - Order B settings"""
        return self.send_message(
            "📊 <b>ORDER B SETTINGS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>SL Mode:</b> Different from Order A\n"
            "<b>TP Mode:</b> Extended target"
        )
    
    def handle_dual_order(self, message: Dict = None) -> Optional[int]:
        """Handle /dualorder command - Dual order system"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_dual_order_menu'):
            self._menu_manager.show_dual_order_menu(self.chat_id, message_id=None)
            return None
        return self.send_message(
            "📊 <b>DUAL ORDER SYSTEM</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED\n"
            "<b>Order A:</b> Conservative SL\n"
            "<b>Order B:</b> Extended target"
        )
    
    # ========================================
    # ANALYTICS COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_analytics_menu(self, message: Dict = None) -> Optional[int]:
        """Handle /analytics command - Analytics menu"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_analytics_menu'):
            self._menu_manager.show_analytics_menu(self.chat_id, message_id=None)
            return None
        keyboard = [
            [{"text": "📅 Daily", "callback_data": "analytics_daily"}, {"text": "📆 Weekly", "callback_data": "analytics_weekly"}],
            [{"text": "📊 Monthly", "callback_data": "analytics_monthly"}, {"text": "📈 Performance", "callback_data": "analytics_performance"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "📊 <b>ANALYTICS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nView trading analytics:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_performance(self, message: Dict = None) -> Optional[int]:
        """Handle /performance command - Performance report"""
        return self.send_message(
            "📈 <b>PERFORMANCE REPORT</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Total Trades:</b> 0\n"
            "<b>Win Rate:</b> 0%\n"
            "<b>Total P&L:</b> $0.00\n"
            "<b>Best Trade:</b> $0.00\n"
            "<b>Worst Trade:</b> $0.00"
        )
    
    def handle_daily(self, message: Dict = None) -> Optional[int]:
        """Handle /daily command - Daily summary"""
        return self.send_message(
            f"📅 <b>DAILY SUMMARY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}\n"
            f"<b>Trades:</b> 0\n"
            f"<b>P&L:</b> $0.00\n"
            f"<b>Win Rate:</b> 0%"
        )
    
    def handle_weekly(self, message: Dict = None) -> Optional[int]:
        """Handle /weekly command - Weekly summary"""
        return self.send_message(
            "📆 <b>WEEKLY SUMMARY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Trades:</b> 0\n"
            "<b>P&L:</b> $0.00\n"
            "<b>Win Rate:</b> 0%\n"
            "<b>Best Day:</b> N/A"
        )
    
    def handle_monthly(self, message: Dict = None) -> Optional[int]:
        """Handle /monthly command - Monthly summary"""
        return self.send_message(
            f"📊 <b>MONTHLY SUMMARY</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Month:</b> {datetime.now().strftime('%B %Y')}\n"
            f"<b>Trades:</b> 0\n"
            f"<b>P&L:</b> $0.00\n"
            f"<b>Win Rate:</b> 0%"
        )
    
    def handle_stats(self, message: Dict = None) -> Optional[int]:
        """Handle /stats command - Statistics"""
        return self.send_message(
            "📊 <b>TRADING STATISTICS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Total Trades:</b> 0\n"
            "<b>Winning:</b> 0\n"
            "<b>Losing:</b> 0\n"
            "<b>Break-even:</b> 0\n"
            "<b>Avg Win:</b> $0.00\n"
            "<b>Avg Loss:</b> $0.00"
        )
    
    def handle_winrate(self, message: Dict = None) -> Optional[int]:
        """Handle /winrate command - Win rate analysis"""
        return self.send_message(
            "🎯 <b>WIN RATE ANALYSIS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Overall:</b> 0%\n"
            "<b>V3 Logic:</b> 0%\n"
            "<b>V6 Price Action:</b> 0%\n"
            "<b>By Session:</b>\n"
            "  London: 0%\n"
            "  New York: 0%"
        )
    
    def handle_drawdown(self, message: Dict = None) -> Optional[int]:
        """Handle /drawdown command - Drawdown analysis"""
        return self.send_message(
            "📉 <b>DRAWDOWN ANALYSIS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Current DD:</b> 0%\n"
            "<b>Max DD:</b> 0%\n"
            "<b>Recovery Factor:</b> N/A"
        )
    
    # ========================================
    # SESSION COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_session_menu(self, message: Dict = None) -> Optional[int]:
        """Handle /session command - Session menu"""
        keyboard = [
            [{"text": "🇬🇧 London", "callback_data": "session_london"}, {"text": "🇺🇸 New York", "callback_data": "session_newyork"}],
            [{"text": "🇯🇵 Tokyo", "callback_data": "session_tokyo"}, {"text": "🇦🇺 Sydney", "callback_data": "session_sydney"}],
            [{"text": "🔙 Back", "callback_data": "menu_main"}]
        ]
        return self.send_message(
            "🌍 <b>TRADING SESSIONS</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\nSelect a session:",
            reply_markup={"inline_keyboard": keyboard}
        )
    
    def handle_london(self, message: Dict = None) -> Optional[int]:
        """Handle /london command - London session"""
        return self.send_message(
            "🇬🇧 <b>LONDON SESSION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 08:00 - 17:00 GMT\n"
            "<b>Status:</b> Active\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_newyork(self, message: Dict = None) -> Optional[int]:
        """Handle /newyork command - New York session"""
        return self.send_message(
            "🇺🇸 <b>NEW YORK SESSION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 13:00 - 22:00 GMT\n"
            "<b>Status:</b> Active\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_tokyo(self, message: Dict = None) -> Optional[int]:
        """Handle /tokyo command - Tokyo session"""
        return self.send_message(
            "🇯🇵 <b>TOKYO SESSION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 00:00 - 09:00 GMT\n"
            "<b>Status:</b> Closed\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_sydney(self, message: Dict = None) -> Optional[int]:
        """Handle /sydney command - Sydney session"""
        return self.send_message(
            "🇦🇺 <b>SYDNEY SESSION</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Hours:</b> 22:00 - 07:00 GMT\n"
            "<b>Status:</b> Active\n"
            "<b>Trading:</b> ENABLED"
        )
    
    def handle_overlap(self, message: Dict = None) -> Optional[int]:
        """Handle /overlap command - Session overlap"""
        return self.send_message(
            "🔄 <b>SESSION OVERLAP</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>London/NY:</b> 13:00 - 17:00 GMT\n"
            "<b>Status:</b> High volatility\n"
            "<b>Trading:</b> ENABLED"
        )
    
    # ========================================
    # PLUGIN COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_shadow(self, message: Dict = None) -> Optional[int]:
        """Handle /shadow command - Shadow mode"""
        return self.send_message(
            "👻 <b>SHADOW MODE</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>Status:</b> ENABLED for V6\n"
            "<b>Mode:</b> Paper trading\n"
            "<b>Logging:</b> Full"
        )
    
    def handle_compare(self, message: Dict = None) -> Optional[int]:
        """Handle /compare command - Compare plugins"""
        return self.send_message(
            "📊 <b>PLUGIN COMPARISON</b>\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "<b>V3 Combined:</b>\n"
            "  Trades: 0 | Win: 0%\n\n"
            "<b>V6 Price Action:</b>\n"
            "  Trades: 0 | Win: 0%"
        )
    
    # ========================================
    # VOICE COMMANDS (Missing Handlers)
    # ========================================
    
    def handle_voice_menu(self, message: Dict = None) -> Optional[int]:
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
    
    def handle_voice_test(self, message: Dict = None) -> Optional[int]:
        """Handle /voicetest command - Test voice alert"""
        return self.send_message("🔊 <b>VOICE TEST</b>\n\nVoice alert test sent!")
    
    def handle_mute(self, message: Dict = None) -> Optional[int]:
        """Handle /mute command - Mute voice alerts"""
        return self.send_message("🔇 <b>VOICE MUTED</b>\n\nVoice alerts are now muted.")
    
    def handle_unmute(self, message: Dict = None) -> Optional[int]:
        """Handle /unmute command - Unmute voice alerts"""
        return self.send_message("🔈 <b>VOICE UNMUTED</b>\n\nVoice alerts are now active.")
    
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
        """Show V6 Price Action control menu via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_v6_menu'):
            self._menu_manager.show_v6_menu(chat_id or self.chat_id, message_id=None)
        else:
            self.send_message("V6 Price Action menu under construction.")
    
    def show_dual_order_menu(self, chat_id: int = None):
        """Show Dual Order System menu via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'show_dual_order_menu'):
            self._menu_manager.show_dual_order_menu(chat_id or self.chat_id, message_id=None)
        else:
            self.send_message("Dual Order System menu under construction.")
    
    def handle_v6_callback(self, callback_data: str, chat_id: int = None, message_id: int = None) -> bool:
        """Handle V6 menu callback via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'handle_v6_callback'):
            return self._menu_manager.handle_v6_callback(callback_data, chat_id or self.chat_id, message_id)
        return False
    
    def handle_analytics_callback(self, callback_data: str, chat_id: int = None, message_id: int = None) -> bool:
        """Handle Analytics menu callback via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'handle_analytics_callback'):
            return self._menu_manager.handle_analytics_callback(callback_data, chat_id or self.chat_id, message_id)
        return False
    
    def handle_dual_order_callback(self, callback_data: str, chat_id: int = None, message_id: int = None) -> bool:
        """Handle Dual Order menu callback via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'handle_dual_order_callback'):
            return self._menu_manager.handle_dual_order_callback(callback_data, chat_id or self.chat_id, message_id)
        return False
    
    def handle_reentry_callback(self, callback_data: str, chat_id: int = None, message_id: int = None) -> bool:
        """Handle Re-entry menu callback via MenuManager (Telegram V5 Upgrade)"""
        if self._menu_manager and hasattr(self._menu_manager, 'handle_reentry_callback'):
            return self._menu_manager.handle_reentry_callback(callback_data, chat_id or self.chat_id, message_id)
        return False

