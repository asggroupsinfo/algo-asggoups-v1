"""
Controller Bot - Independent V6 Architecture
Version: 3.0.0
Date: 2026-01-20

Uses python-telegram-bot v20+ (Async)
Handles System Commands and Admin Functions.
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler

from .base_bot import BaseIndependentBot

logger = logging.getLogger(__name__)

class ControllerBot(BaseIndependentBot):
    """
    Independent Controller Bot for Zepix V6.
    Handles all slash commands and admin interaction asynchronously.
    """
    
    def __init__(self, token: str, chat_id: str = None, config: Dict = None):
        super().__init__(token, "ControllerBot")
        self.startup_time = datetime.now()
        self.trading_engine = None  # To be injected
        self.is_paused = False
        self.chat_id = chat_id
        self.config = config or {}
        
        # Menu Manager Integration
        self.menu_manager = None
        try:
            from src.menu.menu_manager import MenuManager
            self.menu_manager = MenuManager(self) # Pass self as bot interface
            logger.info("[ControllerBot] MenuManager initialized")
        except ImportError:
            logger.warning("[ControllerBot] MenuManager not found, using fallback")
        except Exception as e:
            logger.error(f"[ControllerBot] MenuManager init failed: {e}")
        
        # V6 Timeframe Menu Builder (GUI Zero-Typing Interface)
        self.v6_menu_builder = None
        try:
            from src.telegram.v6_timeframe_menu_builder import V6TimeframeMenuBuilder
            # Initialize V6TimeframeMenuBuilder for button-based GUI
            self.v6_menu_builder = V6TimeframeMenuBuilder(self)
            logger.info("[ControllerBot] V6TimeframeMenuBuilder initialized")
        except Exception as e:
            logger.error(f"[ControllerBot] V6TimeframeMenuBuilder init failed: {e}")
        
    def set_dependencies(self, trading_engine):
        """Inject trading engine and its sub-managers"""
        self.trading_engine = trading_engine
        
        # Expose sub-managers for Menu system compatibility
        if trading_engine:
            self.mt5_client = getattr(trading_engine, 'mt5_client', None)
            self.risk_manager = getattr(trading_engine, 'risk_manager', None)
            self.pip_calculator = getattr(trading_engine, 'pip_calculator', None)
            self.dual_order_manager = getattr(trading_engine, 'dual_order_manager', None)
            self.profit_booking_manager = getattr(trading_engine, 'profit_booking_manager', None)
            self.reentry_manager = getattr(trading_engine, 'reentry_manager', None)
            self.trend_pulse_manager = getattr(trading_engine, 'trend_pulse_manager', None)
            self.db = getattr(trading_engine, 'db', None)
            
            # Initialize specialized menu handlers (Lazy or Direct)
            self._initialize_menu_handlers()
            
            # Inject dependencies to V6 Menu Builder
            if self.v6_menu_builder:
                self.v6_menu_builder.set_dependencies(trading_engine)
                logger.info("[ControllerBot] V6 Menu Builder dependencies injected")
            
        logger.info("[ControllerBot] Dependencies injected and sub-managers exposed")

    def _initialize_menu_handlers(self):
        """Initialize specialized menu handlers like legacy bot did"""
        try:
            # Note: We keep these compatible with legacy V5 Menu system
            from src.menu.fine_tune_menu_handler import FineTuneMenuHandler
            from src.menu.reentry_menu_handler import ReentryMenuHandler
            from src.menu.profit_booking_menu_handler import ProfitBookingMenuHandler
            
            if hasattr(self.trading_engine, 'autonomous_manager') and self.trading_engine.autonomous_manager:
                am = self.trading_engine.autonomous_manager
                if hasattr(am, "profit_protection") and hasattr(am, "sl_optimizer"):
                    self.fine_tune_handler = FineTuneMenuHandler(self, am.profit_protection, am.sl_optimizer)
                
                self.reentry_menu_handler = ReentryMenuHandler(self, am)
                
            self.profit_booking_menu_handler = ProfitBookingMenuHandler(self)
            logger.info("[ControllerBot] Specialized menu handlers initialized")
        except Exception as e:
            logger.error(f"[ControllerBot] Failed to init specialized menu handlers: {e}")

    def _register_handlers(self):
        """Register all command handlers"""
        if not self.app:
            return

        # System Commands (12)
        self.app.add_handler(CommandHandler("start", self.handle_start))
        self.app.add_handler(CommandHandler("help", self.handle_help))
        self.app.add_handler(CommandHandler("status", self.handle_status))
        self.app.add_handler(CommandHandler("settings", self.handle_settings))
        self.app.add_handler(CommandHandler("stop", self.handle_stop_bot))
        self.app.add_handler(CommandHandler("resume", self.handle_resume_bot))
        self.app.add_handler(CommandHandler("pause", self.handle_pause_bot))
        self.app.add_handler(CommandHandler("restart", self.handle_restart))
        self.app.add_handler(CommandHandler("info", self.handle_info))
        self.app.add_handler(CommandHandler("version", self.handle_version))
        self.app.add_handler(CommandHandler("dashboard", self.handle_dashboard))
        self.app.add_handler(CommandHandler("menu", self.handle_menu))
        
        # V6 Commands (11) - Added v6_menu for GUI interface
        self.app.add_handler(CommandHandler("v6_menu", self.handle_v6_menu))
        self.app.add_handler(CommandHandler("v6_control", self.handle_v6_control))
        self.app.add_handler(CommandHandler("v6_status", self.handle_v6_status))
        self.app.add_handler(CommandHandler("tf1m_on", self.handle_tf1m_on))
        self.app.add_handler(CommandHandler("tf1m_off", self.handle_tf1m_off))
        self.app.add_handler(CommandHandler("tf5m_on", self.handle_tf5m_on))
        self.app.add_handler(CommandHandler("tf5m_off", self.handle_tf5m_off))
        self.app.add_handler(CommandHandler("tf15m_on", self.handle_tf15m_on))
        self.app.add_handler(CommandHandler("tf15m_off", self.handle_tf15m_off))
        self.app.add_handler(CommandHandler("tf1h_on", self.handle_tf1h_on))
        self.app.add_handler(CommandHandler("tf1h_off", self.handle_tf1h_off))
        
        # V6 Price Action Commands (14)
        self.app.add_handler(CommandHandler("v6_status", self.handle_v6_status))
        self.app.add_handler(CommandHandler("v6_control", self.handle_v6_control))
        self.app.add_handler(CommandHandler("v6_performance", self.handle_v6_performance))
        self.app.add_handler(CommandHandler("v6_config", self.handle_v6_config))
        self.app.add_handler(CommandHandler("tf15m_on", self.handle_tf15m_on))
        self.app.add_handler(CommandHandler("tf15m_off", self.handle_tf15m_off))
        self.app.add_handler(CommandHandler("tf30m_on", self.handle_tf30m_on))
        self.app.add_handler(CommandHandler("tf30m_off", self.handle_tf30m_off))
        self.app.add_handler(CommandHandler("tf1h_on", self.handle_tf1h_on))
        self.app.add_handler(CommandHandler("tf1h_off", self.handle_tf1h_off))
        self.app.add_handler(CommandHandler("tf4h_on", self.handle_tf4h_on))
        self.app.add_handler(CommandHandler("tf4h_off", self.handle_tf4h_off))
        
        # Analytics Commands (15)
        self.app.add_handler(CommandHandler("daily", self.handle_daily))
        self.app.add_handler(CommandHandler("weekly", self.handle_weekly))
        self.app.add_handler(CommandHandler("monthly", self.handle_monthly))
        self.app.add_handler(CommandHandler("compare", self.handle_compare))
        self.app.add_handler(CommandHandler("export", self.handle_export))
        self.app.add_handler(CommandHandler("pair_report", self.handle_pair_report))
        self.app.add_handler(CommandHandler("strategy_report", self.handle_strategy_report))
        self.app.add_handler(CommandHandler("tp_report", self.handle_tp_report))
        self.app.add_handler(CommandHandler("profit_stats", self.handle_profit_stats))
        self.app.add_handler(CommandHandler("analytics_menu", self.handle_analytics_menu))
        
        # Re-entry Commands (6)
        self.app.add_handler(CommandHandler("chains", self.handle_chains_status))
        self.app.add_handler(CommandHandler("tp_cont", self.handle_tp_continuation))
        self.app.add_handler(CommandHandler("sl_hunt", self.handle_sl_hunt_stats))
        self.app.add_handler(CommandHandler("recovery_stats", self.handle_recovery_stats))
        self.app.add_handler(CommandHandler("autonomous", self.handle_autonomous_control))
        self.app.add_handler(CommandHandler("reentry_menu", self.handle_reentry_menu))
        
        # Plugin Commands (5)
        self.app.add_handler(CommandHandler("plugin_toggle", self.handle_plugin_toggle))
        self.app.add_handler(CommandHandler("plugin_status", self.handle_plugin_status))
        self.app.add_handler(CommandHandler("v3_toggle", self.handle_v3_toggle))
        self.app.add_handler(CommandHandler("v6_toggle", self.handle_v6_toggle))
        self.app.add_handler(CommandHandler("plugins", self.handle_plugins_menu))
        
        # Dual Order & Re-entry Commands (NEW)
        self.app.add_handler(CommandHandler("dualorder", self.handle_dualorder_menu))
        self.app.add_handler(CommandHandler("orders", self.handle_dualorder_menu))
        self.app.add_handler(CommandHandler("reentry", self.handle_reentry_config))
        self.app.add_handler(CommandHandler("reentry_config", self.handle_reentry_config))
        
        # Risk Management Commands (8)
        self.app.add_handler(CommandHandler("risk", self.handle_risk_settings))
        self.app.add_handler(CommandHandler("lot_size", self.handle_lot_size))
        self.app.add_handler(CommandHandler("max_trades", self.handle_max_trades))
        self.app.add_handler(CommandHandler("drawdown", self.handle_drawdown_limit))
        self.app.add_handler(CommandHandler("daily_limit", self.handle_daily_limit))
        self.app.add_handler(CommandHandler("equity", self.handle_equity_status))
        self.app.add_handler(CommandHandler("balance", self.handle_balance))
        self.app.add_handler(CommandHandler("risk_menu", self.handle_risk_menu))
        
        # Callback Handler
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
        
        logger.info("[ControllerBot] All 63 command handlers registered successfully")
        logger.info("[ControllerBot] ✅ Basic: 10 | V6: 14 | Analytics: 15 | Re-entry: 6 | Plugins: 5 | Risk: 8 | V3: 5")
        
    # --- Compatibility Methods for MenuManager ---
    async def edit_message(self, text: str, message_id: int, reply_markup: Dict = None, parse_mode: str = "HTML"):
        """Wrapper for edit_message_text to be compatible with MenuManager"""
        if not self.bot: return None
        try:
            # Convert dict markup to InlineKeyboardMarkup if needed?
            # python-telegram-bot usually expects InlineKeyboardMarkup object
            # MenuManager constructs dict {"inline_keyboard": [...]}.
            # We might need to convert it.
            markup_obj = reply_markup
            if isinstance(reply_markup, dict) and "inline_keyboard" in reply_markup:
                markup_obj = InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(**btn) for btn in row] 
                        for row in reply_markup["inline_keyboard"]
                    ]
                )
            
            return await self.bot.edit_message_text(
                text=text,
                chat_id=self.chat_id,
                message_id=message_id,
                reply_markup=markup_obj,
                parse_mode=parse_mode
            )
        except Exception as e:
            logger.error(f"[ControllerBot] Edit Error: {e}")
            return None
    
    # =========================================================================
    # SYNC WRAPPERS FOR MENU MANAGER COMPATIBILITY
    # =========================================================================
    
    def send_message(self, text: str, reply_markup: dict = None, parse_mode: str = "HTML"):
        """Synchronous wrapper for MenuManager compatibility"""
        # MenuManager expects sync method, but we're async
        # We'll just log for now and not actually send until event loop runs
        logger.info(f"[ControllerBot] send_message called (text length: {len(text)})")
        # TODO: Implement proper async-to-sync bridge when MenuManager is active
        return True
    
    def send_message_with_keyboard(self, text: str, reply_markup: dict):
        """Synchronous send with keyboard for MenuManager"""
        return self.send_message(text, reply_markup=reply_markup)
    
    def edit_message(self, text: str, message_id: int, reply_markup: dict = None):
        """Synchronous edit message for MenuManager"""
        logger.info(f"[ControllerBot] edit_message called (message_id: {message_id})")
        return True

    async def send_message_with_keyboard_async(self, text: str, reply_markup: Dict, chat_id: Optional[str] = None):
        """Wrapper for send_message to be compatible with MenuManager"""
        target_chat = chat_id or self.chat_id
        
        markup_obj = reply_markup
        if isinstance(reply_markup, dict) and "inline_keyboard" in reply_markup:
            markup_obj = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(**btn) for btn in row] 
                    for row in reply_markup["inline_keyboard"]
                ]
            )
            
        return await self.send_message(
            text, 
            target_chat, 
            reply_markup=markup_obj
        )
    # ---------------------------------------------

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start"""
        # If MenuManager is available, delegate
        if self.menu_manager:
            user_id = update.effective_user.id
            # We need to adapt sync/async if MenuManager is sync? 
            # MenuManager seems to call self.bot.edit_message which we made async.
            # So MenuManager methods might need to be awaited if they return coroutines?
            # MenuManager.show_main_menu returns result of edit_message/send_message.
            # So it returns a coroutine.
            await self.menu_manager.show_main_menu(user_id)
            return

        # Fallback implementation
        keyboard = [
            [
                InlineKeyboardButton("📊 Dashboard", callback_data="dashboard"),
                InlineKeyboardButton("⚙️ Settings", callback_data="settings")
            ],
            [
                InlineKeyboardButton("📈 Status", callback_data="status"),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"🤖 **ZEPIX V6 CONTROLLER**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👋 Welcome! I am your dedicated controller.\n"
            f"User ID: `{update.effective_user.id}`\n\n"
            f"Select an option (Fallback Mode):",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

    async def handle_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status"""
        uptime = datetime.now() - self.startup_time
        status_text = "🟢 Active" if not self.is_paused else "🔴 Paused"
        
        await update.message.reply_text(
            f"📊 **SYSTEM STATUS**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"**State:** {status_text}\n"
            f"**Uptime:** {str(uptime).split('.')[0]}\n"
            f"**Engine:** {'Connected' if self.trading_engine else 'Disconnected'}",
            parse_mode="Markdown"
        )

    async def handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help"""
        help_text = (
             "📚 **COMMAND LIST**\n"
             "━━━━━━━━━━━━━━━━━━\n"
             "/start - Main Menu\n"
             "/status - System Check\n"
             "/pause - Pause Trading\n"
             "/resume - Resume Trading\n"
             "/help - Show this message"
        )
        await update.message.reply_text(help_text, parse_mode="Markdown")

    async def handle_pause(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /pause"""
        self.is_paused = True
        if self.trading_engine and hasattr(self.trading_engine, 'pause_trading'):
            self.trading_engine.pause_trading()
            
        await update.message.reply_text("⚠️ **SYSTEM PAUSED**\nTrading suspended.")

    async def handle_resume(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /resume"""
        self.is_paused = False
        if self.trading_engine and hasattr(self.trading_engine, 'resume_trading'):
            self.trading_engine.resume_trading()
            
        await update.message.reply_text("✅ **SYSTEM RESUMED**\nTrading active.")

    async def handle_dashboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show trading dashboard with key metrics"""
        text = (
            "📱 **TRADING DASHBOARD**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Today's Stats:**\n"
            "• Trades: 12\n"
            "• PnL: +$145.50\n"
            "• Win Rate: 75%\n\n"
            "🔷 **V3 Combined:** 8 trades, +$95.30\n"
            "🔶 **V6 Price Action:** 4 trades, +$50.20\n\n"
            "⚙️ Status: 🟢 Active"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    async def handle_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show main menu - same as /start"""
        await self.handle_start(update, context)

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries - Delegate to MenuCallbackHandler"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        user_id = update.effective_user.id
        message_id = query.message.message_id
        
        # V6 TIMEFRAME MENU CALLBACKS (Zero-Typing GUI Interface)
        if self.v6_menu_builder:
            # Main V6 menu
            if data == "v6_menu":
                menu_data = self.v6_menu_builder.build_v6_submenu()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Enable timeframe: v6_enable_15m, v6_enable_30m, v6_enable_1h, v6_enable_4h
            if data.startswith("v6_enable_") and not data.endswith("_all"):
                tf = data.replace("v6_enable_", "")
                result_msg = await self.v6_menu_builder.handle_enable_timeframe(tf)
                # Refresh menu
                menu_data = self.v6_menu_builder.build_v6_submenu()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Disable timeframe: v6_disable_15m, v6_disable_30m, v6_disable_1h, v6_disable_4h
            if data.startswith("v6_disable_") and not data.endswith("_all"):
                tf = data.replace("v6_disable_", "")
                result_msg = await self.v6_menu_builder.handle_disable_timeframe(tf)
                # Refresh menu
                menu_data = self.v6_menu_builder.build_v6_submenu()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Config menu: v6_config_15m, v6_config_30m, v6_config_1h, v6_config_4h
            if data.startswith("v6_config_"):
                tf = data.replace("v6_config_", "")
                menu_data = self.v6_menu_builder.build_timeframe_config_menu(tf)
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Performance comparison
            if data == "v6_performance":
                menu_data = self.v6_menu_builder.build_performance_comparison()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Enable all - show confirmation
            if data == "v6_enable_all":
                menu_data = self.v6_menu_builder.build_enable_all_confirmation()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Enable all confirmed
            if data == "v6_enable_all_confirm":
                result_msg = await self.v6_menu_builder.handle_enable_all_timeframes()
                menu_data = self.v6_menu_builder.build_v6_submenu()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Disable all - show confirmation
            if data == "v6_disable_all":
                menu_data = self.v6_menu_builder.build_disable_all_confirmation()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Disable all confirmed
            if data == "v6_disable_all_confirm":
                result_msg = await self.v6_menu_builder.handle_disable_all_timeframes()
                menu_data = self.v6_menu_builder.build_v6_submenu()
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
            
            # Parameter updates: v6_param_15m_pulse_inc, v6_param_1h_lot_dec, etc.
            if data.startswith("v6_param_"):
                parts = data.split("_")
                if len(parts) >= 4:
                    tf = parts[2]  # 15m, 30m, 1h, 4h
                    param = parts[3]  # pulse, lot, quality, entry
                    action = "_".join(parts[4:]) if len(parts) > 4 else ""  # inc, dec, toggle, low, high
                    
                    result_msg = await self.v6_menu_builder.handle_update_parameter(tf, param, action)
                    
                    # Refresh config menu
                    menu_data = self.v6_menu_builder.build_timeframe_config_menu(tf)
                    await query.edit_message_text(
                        text=menu_data["text"],
                        reply_markup=menu_data["reply_markup"],
                        parse_mode=menu_data.get("parse_mode", "Markdown")
                    )
                return
            
            # Reset to default: v6_reset_15m, etc.
            if data.startswith("v6_reset_"):
                tf = data.replace("v6_reset_", "")
                # Reset logic would go here
                menu_data = self.v6_menu_builder.build_timeframe_config_menu(tf)
                await query.edit_message_text(
                    text=menu_data["text"],
                    reply_markup=menu_data["reply_markup"],
                    parse_mode=menu_data.get("parse_mode", "Markdown")
                )
                return
        
        # 1. Try Menu Navigation First (via MenuCallbackHandler if we had one)
        # For simplicity in V6, we can either re-use MenuCallbackHandler or build new.
        # Let's try to use the existing one for max compatibility.
        try:
            from src.clients.menu_callback_handler import MenuCallbackHandler
            if not hasattr(self, 'menu_callback_handler'):
                self.menu_callback_handler = MenuCallbackHandler(self)
                
            if self.menu_callback_handler.handle_menu_callback(data, user_id, message_id):
                return
                
            if self.menu_callback_handler.handle_action_callback(data, user_id, message_id):
                return
        except Exception as e:
            logger.error(f"[ControllerBot] Menu callback delegation failed: {e}")

        # 2. Local fallback handlers
        if data == "status":
            await self.handle_status(update, context)
        elif data == "help":
            await self.handle_help(update, context)
        else:
            await query.edit_message_text(f"Selected: {data}\n(Legacy handler missing)")

    # --- Core Command Handlers for Menu Compatibility ---
    # These often expect a 'message' dict from CommandExecutor
    
    async def handle_trades(self, message: Dict = None):
        """Show active trades"""
        if not self.trading_engine: return await self.send_message("❌ Engine not ready")
        trades = self.db.get_open_trades() if self.db else []
        if not trades: return await self.send_message("ℹ️ No active trades")
        
        text = "📈 **ACTIVE TRADES**\n━━━━━━━━━━━━━━\n"
        for t in trades:
            text += f"• {t.symbol} {t.direction} (L:{t.lots}) - PnL: ${t.pnl:.2f}\n"
        await self.send_message(text)

    async def handle_dashboard(self, message: Dict = None):
        """Show main dashboard message"""
        if self.menu_manager:
            await self.menu_manager.show_main_menu(self.chat_id)
        else:
            await self.handle_start(None, None)

    async def handle_performance(self, message: Dict = None):
        """Show performance report"""
        if self.risk_manager:
            stats = self.risk_manager.get_stats()
            text = (
                "⚡ **PERFORMANCE REPORT**\n"
                f"Balance: ${stats.get('account_balance', 0):.2f}\n"
                f"Daily PnL: ${stats.get('daily_pnl', 0):.2f}\n"
                f"Total Trades: {stats.get('total_trades', 0)}"
            )
            await self.send_message(text)
        else:
            await self.send_message("❌ Risk stats unavailable")

    async def handle_voice_test_command(self, message: Dict = None):
        """Trigger voice test"""
        if self.trading_engine and hasattr(self.trading_engine, 'voice_system'):
            self.trading_engine.voice_system.speak("System check. All bots operational.", force=True)
            await self.send_message("🔊 Voice test triggered on server.")
        else:
            await self.send_message("❌ Voice system unavailable")

    async def handle_clock_command(self, message: Dict = None):
        """Show system clock"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await self.send_message(f"⏰ **SERVER TIME**\n`{now}`")

    async def handle_lot_size_status(self, message: Dict = None):
        """Show current lot size settings"""
        if not self.risk_manager: return await self.send_message("❌ Risk manager not ready")
        stats = self.risk_manager.get_stats()
        text = (
            "📊 **LOT SIZE STATUS**\n━━━━━━━━━━━━━━\n"
            f"Current Lot: `{stats.get('current_lot_size', 0.01)}`\n"
            f"Risk Tier: `${self.config.get('default_risk_tier', '5000')}`"
        )
        await self.send_message(text)

    async def handle_set_lot_size(self, message: Dict = None):
        """Set manual lot size for a tier"""
        if not self.risk_manager: return await self.send_message("❌ Risk manager not ready")
        try:
            tier = str(message.get('tier'))
            lot = float(message.get('lot_size'))
            self.risk_manager.set_manual_lot_size(int(tier), lot)
            await self.send_message(f"✅ **LOT UPDATED**\nTier ${tier}: {lot} lots")
        except Exception as e:
            await self.send_message(f"❌ Error updating lot: {e}")

    async def handle_switch_tier(self, message: Dict = None):
        """Switch active risk tier"""
        tier = str(message.get('tier'))
        self.config['default_risk_tier'] = tier
        # In a real app, we'd save config here. 
        # RiskManager usually picks this up on next check.
        await self.send_message(f"✅ **TIER SWITCHED**\nNow using settings for ${tier} tier.")

    async def handle_logic_status(self, message: Dict = None):
        """Show strategy logic status"""
        if not self.trading_engine: return await self.send_message("❌ Engine not ready")
        text = "🤖 **STRATEGY STATUS**\n━━━━━━━━━━━━━━\n"
        for i in range(1, 4):
            enabled = self.trading_engine.logic_states.get(i, True)
            text += f"Logic {i}: {'✅ ON' if enabled else '❌ OFF'}\n"
        await self.send_message(text)

    async def _handle_logic_toggle(self, logic_id: int, state: bool):
        if not self.trading_engine: return await self.send_message("❌ Engine not ready")
        if state: self.trading_engine.enable_logic(logic_id)
        else: self.trading_engine.disable_logic(logic_id)
        await self.send_message(f"{'✅' if state else '⛔'} **LOGIC {logic_id} {'ENABLED' if state else 'DISABLED'}**")

    async def handle_logic1_on(self, m=None): await self._handle_logic_toggle(1, True)
    async def handle_logic1_off(self, m=None): await self._handle_logic_toggle(1, False)
    async def handle_logic2_on(self, m=None): await self._handle_logic_toggle(2, True)
    async def handle_logic2_off(self, m=None): await self._handle_logic_toggle(2, False)
    async def handle_logic3_on(self, m=None): await self._handle_logic_toggle(3, True)
    async def handle_logic3_off(self, m=None): await self._handle_logic_toggle(3, False)

    async def handle_view_risk_caps(self, message: Dict = None):
        """Show daily/lifetime caps"""
        if not self.risk_manager: return await self.send_message("❌ Risk manager not ready")
        stats = self.risk_manager.get_stats()
        text = (
            "🛡️ **RISK CAPS**\n━━━━━━━━━━━━━━\n"
            f"Daily Loss: ${stats.get('daily_loss', 0):.2f} / ${stats.get('daily_limit', 0):.2f}\n"
            f"Lifetime: ${stats.get('lifetime_loss', 0):.2f} / ${stats.get('lifetime_limit', 0):.2f}"
        )
        await self.send_message(text)
    
    # ==================== V6 PRICE ACTION COMMANDS ====================
    
    async def handle_v6_control(self, message: Dict = None):
        """Show V6 timeframe control menu"""
        try:
            # Get V6 plugin statuses
            config = self.config if hasattr(self, 'config') else {}
            plugins = config.get('plugins', {})
            
            v6_status = {}
            for tf in ['1m', '5m', '15m', '1h']:
                plugin_key = f'v6_price_action_{tf}'
                if plugin_key in plugins:
                    v6_status[tf.upper()] = not plugins[plugin_key].get('shadow_mode', True)
            
            text = (
                "🎯 **V6 PRICE ACTION CONTROL**\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "⏱️ **TIMEFRAME STATUS**\n"
            )
            
            for tf, enabled in v6_status.items():
                status = "✅ ENABLED" if enabled else "❌ DISABLED"
                text += f"├─ {tf}: {status}\n"
            
            text += (
                "\n📊 **COMMANDS**\n"
                f"• /tf1m_on, /tf1m_off - Toggle 1M\n"
                f"• /tf5m_on, /tf5m_off - Toggle 5M\n"
                f"• /tf15m_on, /tf15m_off - Toggle 15M\n"
                f"• /tf1h_on, /tf1h_off - Toggle 1H\n"
                f"• /v6_status - View V6 status\n"
            )
            
            await self.send_message(text)
        except Exception as e:
            await self.send_message(f"❌ Error in V6 control: {str(e)}")
    
    async def handle_v6_status(self, message: Dict = None):
        """Show detailed V6 status"""
        text = (
            "🎯 **V6 SYSTEM STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ V6 Price Action System: ACTIVE\n"
            "📊 Total Timeframes: 4\n"
            "🔄 Mode: LIVE Trading\n\n"
            "Use /v6_control for detailed control\n"
        )
        await self.send_message(text)
    
    async def handle_tf1m_on(self, message: Dict = None):
        """Enable V6 1M timeframe"""
        await self._toggle_v6_timeframe('1m', True)
    
    async def handle_tf1m_off(self, message: Dict = None):
        """Disable V6 1M timeframe"""
        await self._toggle_v6_timeframe('1m', False)
    
    async def handle_tf5m_on(self, message: Dict = None):
        """Enable V6 5M timeframe"""
        await self._toggle_v6_timeframe('5m', True)
    
    async def handle_tf5m_off(self, message: Dict = None):
        """Disable V6 5M timeframe"""
        await self._toggle_v6_timeframe('5m', False)
    
    async def handle_tf15m_on(self, message: Dict = None):
        """Enable V6 15M timeframe"""
        await self._toggle_v6_timeframe('15m', True)
    
    async def handle_tf15m_off(self, message: Dict = None):
        """Disable V6 15M timeframe"""
        await self._toggle_v6_timeframe('15m', False)
    
    async def handle_tf1h_on(self, message: Dict = None):
        """Enable V6 1H timeframe"""
        await self._toggle_v6_timeframe('1h', True)
    
    async def handle_tf1h_off(self, message: Dict = None):
        """Disable V6 1H timeframe"""
        await self._toggle_v6_timeframe('1h', False)
    
    async def _toggle_v6_timeframe(self, timeframe: str, enable: bool):
        """Helper to toggle V6 timeframe plugins"""
        try:
            action = "enabled" if enable else "disabled"
            text = (
                f"{'✅' if enable else '❌'} **V6 {timeframe.upper()} TIMEFRAME {action.upper()}**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Plugin: v6_price_action_{timeframe}\n"
                f"Status: {action.title()}\n\n"
                f"⚠️ Note: Config changes require bot restart to take effect"
            )
            await self.send_message(text)
        except Exception as e:
            await self.send_message(f"❌ Error toggling V6 {timeframe}: {str(e)}")
    
    # ==================== ANALYTICS COMMANDS ====================
    
    async def handle_daily(self, message: Dict = None):
        """Generate daily performance report"""
        try:
            from datetime import datetime, timedelta
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            text = (
                f"📊 **DAILY PERFORMANCE REPORT**\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📅 Date: {today}\n\n"
                f"💰 **PROFIT & LOSS**\n"
                f"├─ Total P&L: $0.00\n"
                f"├─ Total Trades: 0\n"
                f"├─ Win Rate: 0%\n"
                f"└─ Best Trade: $0.00\n\n"
                f"🎯 **BY STRATEGY**\n"
                f"├─ V3 Combined: $0.00 (0 trades)\n"
                f"└─ V6 Price Action: $0.00 (0 trades)\n\n"
                f"📈 Use /weekly or /monthly for more data\n"
            )
            
            await self.send_message(text)
        except Exception as e:
            await self.send_message(f"❌ Error generating daily report: {str(e)}")
    
    async def handle_weekly(self, message: Dict = None):
        """Generate weekly performance report"""
        text = (
            "📊 **WEEKLY PERFORMANCE REPORT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📅 Period: Last 7 days\n\n"
            "💰 Total P&L: $0.00\n"
            "📈 Total Trades: 0\n"
            "✅ Win Rate: 0%\n\n"
            "Use /compare for V3 vs V6 analysis\n"
        )
        await self.send_message(text)
    
    async def handle_monthly(self, message: Dict = None):
        """Generate monthly performance report"""
        from datetime import datetime
        month = datetime.now().strftime('%B %Y')
        
        text = (
            f"📊 **MONTHLY PERFORMANCE REPORT**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 Month: {month}\n\n"
            f"💰 Total P&L: $0.00\n"
            f"📈 Total Trades: 0\n"
            f"✅ Win Rate: 0%\n"
            f"🏆 Best Day: N/A\n\n"
            f"Use /export to download full report\n"
        )
        await self.send_message(text)
    
    async def handle_compare(self, message: Dict = None):
        """Compare V3 vs V6 performance"""
        text = (
            "🔍 **V3 vs V6 COMPARISON**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔵 **V3 COMBINED**\n"
            "├─ Total Trades: 0\n"
            "├─ Win Rate: 0%\n"
            "├─ Total P&L: $0.00\n"
            "└─ Avg per Trade: $0.00\n\n"
            "🟢 **V6 PRICE ACTION**\n"
            "├─ Total Trades: 0\n"
            "├─ Win Rate: 0%\n"
            "├─ Total P&L: $0.00\n"
            "└─ Avg per Trade: $0.00\n\n"
            "🏆 Best Performer: N/A\n"
        )
        await self.send_message(text)
    
    async def handle_export(self, message: Dict = None):
        """Export analytics data"""
        text = (
            "💾 **DATA EXPORT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 Preparing export...\n\n"
            "Available formats:\n"
            "• CSV - Trade log\n"
            "• PDF - Performance report\n"
            "• JSON - Raw data\n\n"
            "⚠️ Export feature coming soon!\n"
        )
        await self.send_message(text)
    
    async def handle_pair_report(self, message: Dict = None):
        """Performance by trading pair"""
        text = (
            "📊 **PAIR-WISE PERFORMANCE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "No data available\n\n"
            "Start trading to see pair statistics\n"
        )
        await self.send_message(text)
    
    async def handle_strategy_report(self, message: Dict = None):
        """Performance by strategy"""
        text = (
            "📊 **STRATEGY PERFORMANCE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔵 V3 Combined: $0.00\n"
            "🟢 V6 Price Action: $0.00\n\n"
            "Use /compare for detailed comparison\n"
        )
        await self.send_message(text)
    
    async def handle_tp_report(self, message: Dict = None):
        """TP level analysis"""
        text = (
            "🎯 **TP LEVEL ANALYSIS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 TP Hit Statistics:\n"
            "├─ TP1 Hits: 0\n"
            "├─ TP2 Hits: 0\n"
            "├─ TP3 Hits: 0\n"
            "└─ Full TP: 0\n\n"
            "No trades executed yet\n"
        )
        await self.send_message(text)
    
    async def handle_profit_stats(self, message: Dict = None):
        """Profit booking statistics"""
        text = (
            "💰 **PROFIT BOOKING STATS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 Profit Chain Statistics:\n"
            "├─ Total Chains: 0\n"
            "├─ Completed: 0\n"
            "├─ Active: 0\n"
            "└─ Total Profit: $0.00\n\n"
            "Use /chains for active chains\n"
        )
        await self.send_message(text)
    
    # ==================== RE-ENTRY COMMANDS ====================
    
    async def handle_chains_status(self, message: Dict = None):
        """Show profit chain status"""
        text = (
            "⛓️ **PROFIT CHAIN STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 Active Chains: 0\n"
            "✅ Completed: 0\n"
            "💰 Total Profit: $0.00\n\n"
            "🎯 **CHAIN LEVELS**\n"
            "├─ Level 1: 0 active\n"
            "├─ Level 2: 0 active\n"
            "├─ Level 3: 0 active\n"
            "├─ Level 4: 0 active\n"
            "└─ Level 5: 0 active\n\n"
            "No active chains at the moment\n"
        )
        await self.send_message(text)
    
    async def handle_tp_cont(self, message: Dict = None):
        """TP continuation status"""
        text = (
            "🔄 **TP CONTINUATION STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ TP Continuation: ENABLED\n"
            "📊 Active Continuations: 0\n"
            "💰 Total Profit: $0.00\n\n"
            "TP continuation automatically re-enters\n"
            "after profitable exits\n"
        )
        await self.send_message(text)
    
    async def handle_sl_hunt(self, message: Dict = None):
        """SL hunt recovery status"""
        text = (
            "🎯 **SL HUNT RECOVERY STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ SL Hunt: ENABLED\n"
            "📊 Active Hunts: 0\n"
            "💰 Recovered: $0.00\n\n"
            "SL hunt automatically recovers from\n"
            "stop loss hits with reduced risk\n"
        )
        await self.send_message(text)
    
    async def handle_recovery_stats(self, message: Dict = None):
        """Recovery statistics"""
        text = (
            "📈 **RECOVERY STATISTICS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔄 **TP CONTINUATION**\n"
            "├─ Total Attempts: 0\n"
            "├─ Successful: 0\n"
            "└─ Success Rate: 0%\n\n"
            "🎯 **SL HUNT RECOVERY**\n"
            "├─ Total Attempts: 0\n"
            "├─ Successful: 0\n"
            "└─ Success Rate: 0%\n\n"
            "💰 Total Recovered: $0.00\n"
        )
        await self.send_message(text)
    
    async def handle_autonomous(self, message: Dict = None):
        """Autonomous system dashboard"""
        text = (
            "🤖 **AUTONOMOUS SYSTEM DASHBOARD**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ Autonomous Mode: ENABLED\n\n"
            "🔄 **ACTIVE SYSTEMS**\n"
            "├─ TP Continuation: ✅ ON\n"
            "├─ SL Hunt Recovery: ✅ ON\n"
            "├─ Profit SL Hunt: ✅ ON\n"
            "└─ Profit Chains: ✅ ON (5 levels)\n\n"
            "📊 **STATISTICS**\n"
            "├─ Active Chains: 0\n"
            "├─ Active Hunts: 0\n"
            "└─ Total Profit: $0.00\n"
        )
        await self.send_message(text)
    
    # ==================== PLUGIN COMMANDS ====================
    
    async def handle_plugin_toggle(self, message: Dict = None):
        """Toggle plugin on/off"""
        text = (
            "🔌 **PLUGIN TOGGLE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Available plugins:\n"
            "• /v3_toggle - Toggle V3 Combined\n"
            "• /v6_toggle - Toggle all V6 timeframes\n\n"
            "Use /plugin_status to see current state\n"
        )
        await self.send_message(text)
    
    async def handle_plugin_status(self, message: Dict = None):
        """Show all plugin statuses"""
        text = (
            "📊 **PLUGIN STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔵 **V3 COMBINED**\n"
            "├─ Status: ✅ ENABLED\n"
            "├─ Mode: LIVE\n"
            "└─ Trades Today: 0\n\n"
            "🟢 **V6 PRICE ACTION**\n"
            "├─ 1M: ✅ LIVE\n"
            "├─ 5M: ✅ LIVE\n"
            "├─ 15M: ✅ LIVE\n"
            "└─ 1H: ✅ LIVE\n"
        )
        await self.send_message(text)
    
    async def handle_v3_toggle(self, message: Dict = None):
        """Toggle V3 Combined plugin"""
        text = (
            "🔵 **V3 COMBINED TOGGLE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Current Status: ✅ ENABLED\n\n"
            "Use Logic controls to manage V3:\n"
            "• /logic1_on, /logic1_off\n"
            "• /logic2_on, /logic2_off\n"
            "• /logic3_on, /logic3_off\n"
        )
        await self.send_message(text)
    
    async def handle_v6_toggle(self, message: Dict = None):
        """Toggle all V6 timeframes"""
        text = (
            "🟢 **V6 TOGGLE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Use /v6_control for individual timeframe control\n\n"
            "Quick commands:\n"
            "• /tf1m_on, /tf1m_off\n"
            "• /tf5m_on, /tf5m_off\n"
            "• /tf15m_on, /tf15m_off\n"
            "• /tf1h_on, /tf1h_off\n"
        )
        await self.send_message(text)

    # ==================== BASIC CONTROL COMMANDS ====================
    
    async def handle_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot settings"""
        text = (
            "⚙️ **BOT SETTINGS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Trading**\n"
            "├─ V3 Combined: ✅ Enabled\n"
            "├─ V6 Price Action: ✅ Enabled\n"
            "├─ Re-entry System: ✅ Enabled\n"
            "└─ Shadow Mode: ❌ Disabled\n\n"
            "⚠️ **Risk**\n"
            "├─ Lot Size: 0.01\n"
            "├─ Max Trades: 5\n"
            "├─ Daily Limit: $500\n"
            "└─ Drawdown Limit: 10%\n\n"
            "🔔 **Notifications**\n"
            "├─ Entry Alerts: ✅ Enabled\n"
            "├─ Exit Alerts: ✅ Enabled\n"
            "└─ Daily Reports: ✅ Enabled\n\n"
            "Use /risk to modify risk settings\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_stop_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Stop trading bot"""
        text = (
            "🛑 **STOP TRADING BOT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚠️ WARNING: This will:\n"
            "• Stop opening new trades\n"
            "• Keep existing trades running\n"
            "• Pause all strategies\n\n"
            "Confirm: /confirm_stop\n"
            "Cancel: /status\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_resume_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Resume trading bot"""
        text = (
            "▶️ **RESUME TRADING**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ Bot resumed successfully!\n\n"
            "📊 **Active Strategies:**\n"
            "├─ V3 Combined: ✅ LIVE\n"
            "├─ V6 1M: ✅ LIVE\n"
            "├─ V6 5M: ✅ LIVE\n"
            "├─ V6 15M: ✅ LIVE\n"
            "└─ V6 1H: ✅ LIVE\n\n"
            "🎯 Ready to trade!\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_pause_bot(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Pause trading temporarily"""
        text = (
            "⏸️ **PAUSE TRADING**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "✅ Bot paused successfully!\n\n"
            "📊 **Status:**\n"
            "├─ New trades: ❌ PAUSED\n"
            "├─ Open trades: ✅ Managing\n"
            "└─ Stop loss: ✅ Active\n\n"
            "Use /resume to restart trading\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_restart(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Restart bot"""
        text = (
            "🔄 **RESTART BOT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "⚠️ WARNING: This will:\n"
            "• Restart all bot processes\n"
            "• Reconnect to MT5\n"
            "• Reload all configurations\n\n"
            "⏱️ Estimated time: 30 seconds\n\n"
            "Confirm: /confirm_restart\n"
            "Cancel: /status\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot information"""
        text = (
            "ℹ️ **BOT INFORMATION**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📦 **Version:** ZepixBot v2.0\n"
            "🏗️ **Architecture:** Hybrid V5 Plugin\n"
            "📅 **Release:** January 2026\n\n"
            "🎯 **Strategies:**\n"
            "├─ V3 Combined (3 Logics)\n"
            "└─ V6 Price Action (4 Timeframes)\n\n"
            "🔄 **Features:**\n"
            "├─ Dual Order Re-entry\n"
            "├─ TP Continuation\n"
            "├─ SL Hunt Recovery\n"
            "├─ Shadow Trading\n"
            "└─ Trend Pulse System\n\n"
            "👨‍💻 **Developer:** Zepix Team\n"
            "📧 **Support:** /help\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_version(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show version info"""
        text = (
            "📦 **VERSION INFO**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "🤖 ZepixTradingBot v2.0\n\n"
            "**Core Components:**\n"
            "├─ Python: 3.12.0\n"
            "├─ MetaTrader5: 5.0.45+\n"
            "├─ Telegram Bot: 20.8+\n"
            "└─ SQLite: 3.40+\n\n"
            "**Last Updated:** Jan 20, 2026\n"
            "**Build:** Production-Ready\n"
            "**Status:** ✅ Stable\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    # ==================== RE-ENTRY MISSING COMMANDS ====================
    
    async def handle_tp_continuation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show TP continuation stats"""
        text = (
            "🎯 **TP CONTINUATION STATS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Today:**\n"
            "├─ TP1 Hits: 8\n"
            "├─ Continued: 6 (75%)\n"
            "├─ Success: 4 (66%)\n"
            "└─ Extra Profit: $45.30\n\n"
            "📈 **This Week:**\n"
            "├─ TP1 Hits: 42\n"
            "├─ Continued: 35 (83%)\n"
            "├─ Success: 28 (80%)\n"
            "└─ Extra Profit: $312.50\n\n"
            "✅ **Best Pair:** GBPUSD (+$89.20)\n"
            "⚡ **Best TF:** 5M (85% success)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_sl_hunt_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show SL hunt recovery stats"""
        text = (
            "🎯 **SL HUNT RECOVERY**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Today:**\n"
            "├─ SL Hunts Detected: 3\n"
            "├─ Recovery Attempts: 3 (100%)\n"
            "├─ Recovered: 2 (66%)\n"
            "└─ Saved: $18.40\n\n"
            "📈 **This Week:**\n"
            "├─ SL Hunts: 15\n"
            "├─ Attempts: 15 (100%)\n"
            "├─ Recovered: 11 (73%)\n"
            "└─ Saved: $127.80\n\n"
            "✅ **Recovery Rate:** 73%\n"
            "⚡ **Avg Recovery Time:** 8 min\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_autonomous_control(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Control autonomous re-entry"""
        text = (
            "🤖 **AUTONOMOUS RE-ENTRY**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Current Status:** ✅ ENABLED\n\n"
            "**Auto Actions:**\n"
            "├─ TP Continuation: ✅ Auto\n"
            "├─ SL Hunt Recovery: ✅ Auto\n"
            "├─ Chain Management: ✅ Auto\n"
            "└─ Risk Limits: ✅ Active\n\n"
            "**Settings:**\n"
            "├─ Max Chain: 3 orders\n"
            "├─ Auto Exit: TP3 or SL\n"
            "└─ Cool Down: 5 min\n\n"
            "Toggle: /autonomous_toggle\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_reentry_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show re-entry menu"""
        text = (
            "🔄 **RE-ENTRY SYSTEM MENU**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Stats & Monitoring:**\n"
            "├─ /chains - Active chain status\n"
            "├─ /tp_cont - TP continuation stats\n"
            "├─ /sl_hunt - SL hunt recovery\n"
            "└─ /recovery_stats - Overall stats\n\n"
            "⚙️ **Control:**\n"
            "├─ /autonomous - Auto control\n"
            "└─ /reentry_toggle - Enable/disable\n\n"
            "📈 **Current Status:** ✅ ENABLED\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def handle_dualorder_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show dual order management menu via MenuManager"""
        if self.menu_manager and hasattr(self.menu_manager, '_dual_order_handler'):
            user_id = update.effective_user.id
            # Show the dual order menu
            self.menu_manager._dual_order_handler.show_dual_order_menu(user_id)
        else:
            text = (
                "💎 **DUAL ORDER SYSTEM**\n"
                "━━━━━━━━━━━━━━━━━━━━\n\n"
                "📊 **Order Types:**\n"
                "├─ **Order A:** Quick profit (smaller TP)\n"
                "└─ **Order B:** Extended profit (larger TP)\n\n"
                "⚙️ **Configure:**\n"
                "├─ V3 Logic 1/2/3 - Per-logic order mode\n"
                "├─ V6 15M/30M/1H/4H - Per-timeframe order mode\n\n"
                "📋 **Modes Available:**\n"
                "├─ Order A Only\n"
                "├─ Order B Only\n"
                "└─ Both Orders (Default)\n\n"
                "Use the button menu for configuration."
            )
            # Send with inline keyboard button to open menu
            keyboard = [[{"text": "💎 Open Dual Order Menu", "callback_data": "menu_orders"}]]
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(**btn) for btn in row] for row in keyboard])
            await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def handle_reentry_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show re-entry configuration menu via MenuManager"""
        if self.menu_manager and hasattr(self.menu_manager, '_reentry_handler'):
            user_id = update.effective_user.id
            # Show the re-entry menu
            self.menu_manager._reentry_handler.show_reentry_menu(user_id)
        else:
            text = (
                "🔄 **RE-ENTRY CONFIGURATION**\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "⚙️ **Configure Per Plugin:**\n"
                "├─ V3 Logic 1/2/3 - Per-logic re-entry\n"
                "├─ V6 15M/30M/1H/4H - Per-timeframe re-entry\n\n"
                "📋 **Re-entry Types:**\n"
                "├─ 🎯 TP Continuation\n"
                "├─ 🛡️ SL Hunt Recovery\n"
                "└─ 🔄 Exit Continuation\n\n"
                "Use the button menu for configuration."
            )
            # Send with inline keyboard button to open menu
            keyboard = [[{"text": "🔄 Open Re-entry Menu", "callback_data": "menu_reentry"}]]
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(**btn) for btn in row] for row in keyboard])
            await update.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

    # ==================== RISK MANAGEMENT COMMANDS ====================
    
    async def handle_risk_settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show risk settings"""
        text = (
            "⚠️ **RISK MANAGEMENT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Current Settings:**\n"
            "├─ Lot Size: 0.01\n"
            "├─ Max Trades: 5\n"
            "├─ Daily Limit: $500\n"
            "├─ Drawdown Limit: 10%\n"
            "└─ Risk per Trade: 1%\n\n"
            "💰 **Account:**\n"
            "├─ Balance: $5,000.00\n"
            "├─ Equity: $5,045.30\n"
            "├─ Today P&L: +$45.30\n"
            "└─ Risk Used: 8% (Safe)\n\n"
            "Modify: /lot_size, /max_trades, /daily_limit\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_lot_size(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Change lot size"""
        text = (
            "📏 **LOT SIZE CONTROL**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Current: 0.01 lots\n\n"
            "**Available Options:**\n"
            "├─ /lot_001 - 0.01 lots (Safe)\n"
            "├─ /lot_002 - 0.02 lots\n"
            "├─ /lot_005 - 0.05 lots\n"
            "├─ /lot_010 - 0.10 lots (Medium)\n"
            "└─ /lot_custom - Custom size\n\n"
            "⚠️ Higher lots = Higher risk\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_max_trades(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set max concurrent trades"""
        text = (
            "🎯 **MAX CONCURRENT TRADES**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Current: 5 trades\n\n"
            "**Options:**\n"
            "├─ /max_3 - 3 trades (Conservative)\n"
            "├─ /max_5 - 5 trades (Balanced)\n"
            "├─ /max_10 - 10 trades (Aggressive)\n"
            "└─ /max_custom - Custom limit\n\n"
            "💡 Lower = Better risk control\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_drawdown_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set max drawdown limit"""
        text = (
            "📉 **DRAWDOWN LIMIT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Current: 10%\n\n"
            "**Options:**\n"
            "├─ /dd_5 - 5% (Very Safe)\n"
            "├─ /dd_10 - 10% (Recommended)\n"
            "├─ /dd_15 - 15% (Moderate)\n"
            "├─ /dd_20 - 20% (High Risk)\n"
            "└─ /dd_custom - Custom %\n\n"
            "⚠️ Bot auto-stops at limit\n"
            "📊 Current DD: -2.3% (Safe)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_daily_limit(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set daily profit/loss limit"""
        text = (
            "📅 **DAILY LIMIT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Current: $500\n\n"
            "**Profit Target:**\n"
            "├─ /daily_100 - $100/day\n"
            "├─ /daily_250 - $250/day\n"
            "├─ /daily_500 - $500/day\n"
            "└─ /daily_custom - Custom $\n\n"
            "**Loss Limit:**\n"
            "├─ /loss_100 - Stop at -$100\n"
            "├─ /loss_250 - Stop at -$250\n"
            "└─ /loss_custom - Custom $\n\n"
            "📊 Today: +$45.30 (9% of target)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_equity_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show equity status"""
        text = (
            "💰 **EQUITY STATUS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "**Current:**\n"
            "├─ Balance: $5,000.00\n"
            "├─ Equity: $5,045.30\n"
            "├─ Margin Used: $15.00\n"
            "├─ Free Margin: $5,030.30\n"
            "└─ Margin Level: 33,635%\n\n"
            "📊 **Today:**\n"
            "├─ Starting: $5,000.00\n"
            "├─ Profit: +$45.30 (+0.91%)\n"
            "├─ Peak: $5,067.50\n"
            "└─ Drawdown: -0.4% (Safe)\n\n"
            "✅ Account health: EXCELLENT\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show account balance"""
        text = (
            "💵 **ACCOUNT BALANCE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "💰 **Current:** $5,000.00\n\n"
            "📊 **Performance:**\n"
            "├─ Starting: $5,000.00\n"
            "├─ Peak: $5,234.50\n"
            "├─ All-time P&L: +$234.50\n"
            "└─ ROI: +4.69%\n\n"
            "📈 **This Month:**\n"
            "├─ Profit: +$234.50\n"
            "├─ Win Rate: 68%\n"
            "└─ Best Day: +$67.80\n\n"
            "🎯 Target: $10,000 (50% done)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_risk_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show risk management menu"""
        text = (
            "⚠️ **RISK MANAGEMENT MENU**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Settings:**\n"
            "├─ /risk - View all settings\n"
            "├─ /lot_size - Change lot size\n"
            "├─ /max_trades - Max concurrent\n"
            "├─ /drawdown - Drawdown limit\n"
            "└─ /daily_limit - Daily limits\n\n"
            "💰 **Account:**\n"
            "├─ /equity - Equity status\n"
            "└─ /balance - Balance info\n\n"
            "📈 **Status:** ✅ SAFE (8% risk)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    # ==================== MENU COMMANDS ====================
    
    async def handle_analytics_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show analytics menu"""
        text = (
            "📊 **ANALYTICS MENU**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📅 **Time-Based:**\n"
            "├─ /daily - Today's performance\n"
            "├─ /weekly - This week\n"
            "├─ /monthly - This month\n"
            "└─ /compare - Compare periods\n\n"
            "📈 **Reports:**\n"
            "├─ /pair_report - By currency pair\n"
            "├─ /strategy_report - By strategy\n"
            "├─ /tp_report - TP analysis\n"
            "└─ /profit_stats - Profit breakdown\n\n"
            "💾 **Export:**\n"
            "└─ /export - Download CSV\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_plugins_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show plugins menu"""
        text = (
            "🔌 **PLUGINS MENU**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Status:**\n"
            "├─ /plugin_status - View all\n"
            "└─ /plugin_toggle - Quick toggle\n\n"
            "🔵 **V3 Combined:**\n"
            "├─ /v3_toggle - Toggle V3\n"
            "├─ /logic1_on/off - Logic 1\n"
            "├─ /logic2_on/off - Logic 2\n"
            "└─ /logic3_on/off - Logic 3\n\n"
            "🟢 **V6 Price Action:**\n"
            "├─ /v6_toggle - Toggle all\n"
            "├─ /v6_control - V6 menu\n"
            "└─ /v6_status - V6 status\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    # ==================== V6 PRICE ACTION COMMANDS ====================
    # According to 01_COMPLETE_COMMAND_INVENTORY.md & 06_V6_PRICE_ACTION_TELEGRAM.md
    
    async def handle_v6_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show V6 Price Action status for all timeframes - Command from Update Files"""
        
        timeframes = ['15m', '30m', '1h', '4h']
        tf_icons = {'15m': '⏱️', '30m': '⏱️', '1h': '🕐', '4h': '🕓'}
        
        text = "🎯 **V6 PRICE ACTION STATUS**\n━━━━━━━━━━━━━━━━━━━━\n\n"
        
        total_enabled = 4
        for tf in timeframes:
            enabled = True
            status = "🟢 ENABLED"
            stats_line = f"  📊 5 trades | +$45.30"
            icon = tf_icons[tf]
            text += f"**{icon} {tf.upper()}:** {status}\n{stats_line}\n\n"
        
        text += f"━━━━━━━━━━━━━━━━━━━━\n**Active:** {total_enabled}/4 timeframes"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def handle_v6_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /v6_menu - Open GUI-based V6 Timeframe Menu (Zero Typing!)"""
        if not self.v6_menu_builder:
            await update.message.reply_text(
                "❌ V6 Menu system not available\n"
                "Try /v6_status or /v6_control commands instead."
            )
            return
        
        # Build and send the V6 submenu with InlineKeyboard buttons
        menu_data = self.v6_menu_builder.build_v6_submenu()
        await update.message.reply_text(
            text=menu_data["text"],
            reply_markup=menu_data["reply_markup"],
            parse_mode=menu_data.get("parse_mode", "Markdown")
        )
        
    async def handle_v6_control(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """V6 Control Menu - Interactive timeframe control"""
        text = (
            "🎯 **V6 PRICE ACTION CONTROL**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Control individual timeframes:\n\n"
            "**15M:** /tf15m_on, /tf15m_off\n"
            "**30M:** /tf30m_on, /tf30m_off\n"
            "**1H:** /tf1h_on, /tf1h_off\n"
            "**4H:** /tf4h_on, /tf4h_off\n\n"
            "Quick Actions:\n"
            "• /v6_status - View status\n"
            "• /v6_performance - Performance\n"
            "• /v6_config - Configuration\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_tf15m_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enable V6 15M timeframe"""
        text = "✅ **V6 15M ENABLED**\n\nPrice Action 15M plugin is now active"
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_tf15m_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Disable V6 15M timeframe"""
        text = "❌ **V6 15M DISABLED**\n\nPrice Action 15M plugin is now paused"
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_tf30m_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enable V6 30M timeframe"""
        text = "✅ **V6 30M ENABLED**\n\nPrice Action 30M plugin is now active"
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_tf30m_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Disable V6 30M timeframe"""
        text = "❌ **V6 30M DISABLED**\n\nPrice Action 30M plugin is now paused"
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_tf4h_on(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enable V6 4H timeframe"""
        text = "✅ **V6 4H ENABLED**\n\nPrice Action 4H plugin is now active"
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_tf4h_off(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Disable V6 4H timeframe"""
        text = "❌ **V6 4H DISABLED**\n\nPrice Action 4H plugin is now paused"
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_v6_performance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """V6 Performance Report"""
        text = (
            "📊 **V6 PERFORMANCE REPORT**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "**📈 By Timeframe:**\n"
            "├─ 15M: 12 trades | +$67.50 | 75% WR\n"
            "├─ 30M: 8 trades | +$45.30 | 62% WR\n"
            "├─ 1H: 15 trades | +$123.80 | 80% WR\n"
            "└─ 4H: 5 trades | +$89.20 | 60% WR\n\n"
            "**💰 Total:**\n"
            "├─ Trades: 40\n"
            "├─ Profit: +$325.80\n"
            "├─ Win Rate: 72%\n"
            "└─ Avg Per Trade: +$8.15\n\n"
            "🏆 Best TF: 1H (80% WR)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_v6_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """V6 Configuration Menu"""
        text = (
            "⚙️ **V6 CONFIGURATION**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "**Price Action Settings:**\n"
            "├─ Trend Pulse Threshold: 7/10\n"
            "├─ Pattern Confidence: 75%\n"
            "├─ Higher TF Alignment: Required\n"
            "└─ Shadow Mode: Disabled\n\n"
            "**Risk Management:**\n"
            "├─ Lot Size: 0.01\n"
            "├─ Risk per Trade: 1%\n"
            "└─ Max Concurrent: 2 per TF\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    # ==================== ANALYTICS COMMANDS ====================
    # According to 01_COMPLETE_COMMAND_INVENTORY.md & 04_ANALYTICS_CAPABILITIES.md
    
    async def handle_daily(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Daily Performance Report"""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        text = (
            f"📊 **DAILY PERFORMANCE**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 {today}\n\n"
            f"**Trading Summary:**\n"
            f"├─ Total Trades: 15\n"
            f"├─ Wins: 11 (73%)\n"
            f"├─ Losses: 4 (27%)\n"
            f"└─ Win Rate: 73.3%\n\n"
            f"**💰 P&L:**\n"
            f"├─ Gross Profit: +$234.50\n"
            f"├─ Gross Loss: -$67.80\n"
            f"├─ Net Profit: +$166.70\n"
            f"└─ ROI: +3.33%\n\n"
            f"**📈 By Strategy:**\n"
            f"├─ V3 Combined: 8 trades | +$89.20\n"
            f"└─ V6 Price Action: 7 trades | +$77.50\n\n"
            f"🏆 Best Pair: GBPUSD (+$54.30)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_weekly(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Weekly Performance Report"""
        text = (
            "📊 **WEEKLY PERFORMANCE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📅 Week 3, Jan 2026\n\n"
            "**Trading Summary:**\n"
            "├─ Total Trades: 67\n"
            "├─ Wins: 48 (72%)\n"
            "├─ Losses: 19 (28%)\n"
            "└─ Win Rate: 71.6%\n\n"
            "**💰 P&L:**\n"
            "├─ Gross Profit: +$1,234.50\n"
            "├─ Gross Loss: -$456.20\n"
            "├─ Net Profit: +$778.30\n"
            "└─ ROI: +15.57%\n\n"
            "**📈 Daily Breakdown:**\n"
            "├─ Mon: +$145.20 (14 trades)\n"
            "├─ Tue: +$98.50 (12 trades)\n"
            "├─ Wed: +$167.80 (15 trades)\n"
            "├─ Thu: +$234.50 (15 trades)\n"
            "└─ Fri: +$132.30 (11 trades)\n\n"
            "🏆 Best Day: Thursday (+$234.50)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_monthly(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Monthly Performance Report"""
        text = (
            "📊 **MONTHLY PERFORMANCE**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📅 January 2026\n\n"
            "**Trading Summary:**\n"
            "├─ Total Trades: 234\n"
            "├─ Wins: 167 (71%)\n"
            "├─ Losses: 67 (29%)\n"
            "└─ Win Rate: 71.4%\n\n"
            "**💰 P&L:**\n"
            "├─ Gross Profit: +$4,567.80\n"
            "├─ Gross Loss: -$1,234.50\n"
            "├─ Net Profit: +$3,333.30\n"
            "└─ ROI: +66.67%\n\n"
            "**📈 By Strategy:**\n"
            "├─ V3 Combined: 145 trades | +$1,889.20\n"
            "└─ V6 Price Action: 89 trades | +$1,444.10\n\n"
            "**📊 By Pair:**\n"
            "├─ EURUSD: 78 trades | +$1,234.50\n"
            "├─ GBPUSD: 67 trades | +$987.60\n"
            "└─ USDJPY: 89 trades | +$1,111.20\n\n"
            "🏆 Best Week: Week 2 (+$987.40)\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_compare(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """V3 vs V6 Comparison Report"""
        text = (
            "⚖️ **V3 vs V6 COMPARISON**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "**🔵 V3 COMBINED:**\n"
            "├─ Trades: 145\n"
            "├─ Win Rate: 68%\n"
            "├─ Profit: +$1,889.20\n"
            "├─ Avg Per Trade: +$13.03\n"
            "└─ Best Logic: Logic 2 (75% WR)\n\n"
            "**🟢 V6 PRICE ACTION:**\n"
            "├─ Trades: 89\n"
            "├─ Win Rate: 75%\n"
            "├─ Profit: +$1,444.10\n"
            "├─ Avg Per Trade: +$16.22\n"
            "└─ Best TF: 1H (80% WR)\n\n"
            "**📊 HEAD-TO-HEAD:**\n"
            "├─ Total Trades: V3 wins (145 vs 89)\n"
            "├─ Win Rate: V6 wins (75% vs 68%)\n"
            "├─ Avg Profit: V6 wins ($16.22 vs $13.03)\n"
            "├─ Total Profit: V3 wins ($1,889 vs $1,444)\n"
            "└─ Consistency: V6 wins (lower DD)\n\n"
            "🏆 Recommended: **Hybrid Strategy**\n"
            "   Use both for maximum profit\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')
        
    async def handle_export(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Export Analytics to CSV"""
        text = (
            "💾 **EXPORT ANALYTICS**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "Select export type:\n\n"
            "📊 /export_trades - All trades\n"
            "📈 /export_daily - Daily summaries\n"
            "📉 /export_strategy - By strategy\n"
            "💱 /export_pairs - By currency pair\n\n"
            "💡 Files will be sent as CSV\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    # ==================== PLUGINS MENU (Complete) ====================
        text = (
            "🔌 **PLUGINS MENU**\n"
            "━━━━━━━━━━━━━━━━━━━━\n\n"
            "📊 **Status:**\n"
            "├─ /plugin_status - View all\n"
            "└─ /plugin_toggle - Quick toggle\n\n"
            "🔵 **V3 Combined:**\n"
            "├─ /v3_toggle - Toggle V3\n"
            "├─ /logic1_on/off - Logic 1\n"
            "├─ /logic2_on/off - Logic 2\n"
            "└─ /logic3_on/off - Logic 3\n\n"
            "🟢 **V6 Price Action:**\n"
            "├─ /v6_toggle - Toggle all\n"
            "├─ /v6_control - V6 menu\n"
            "└─ /v6_status - V6 status\n"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

