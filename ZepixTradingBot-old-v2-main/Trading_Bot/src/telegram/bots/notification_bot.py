"""
Notification Bot - Independent V6 Architecture
Version: 3.0.0
Date: 2026-01-20

Uses python-telegram-bot v20+ (Async)
Handles Trade Alerts and Broadcasts.
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from .base_bot import BaseIndependentBot

logger = logging.getLogger(__name__)

class NotificationBot(BaseIndependentBot):
    """
    Dedicated Notification Bot for Trade Alerts.
    PRIORITY: High
    """
    
    def __init__(self, token: str, chat_id: str = None, config: Dict = None):
        super().__init__(token, "NotificationBot")
        self.default_chat_id = chat_id
        self.config = config or {}
        
    def _register_handlers(self):
        """Register handlers (Minimal for Notification Bot)"""
        if self.app:
            self.app.add_handler(CommandHandler("start", self.handle_start))
            
    async def handle_start(self, update, context):
        """Simple start message"""
        await update.message.reply_text(
            "🔔 **NOTIFICATION BOT ACTIVE**\n"
            "I am purely for sending alerts. I ignore commands."
        )

    async def send_alert(self, message: str, chat_id: str = None, parse_mode: str = "HTML", disable_notification: bool = False):
        """
        Send a high-priority trade alert with enhanced formatting.
        
        Args:
            message: Alert message (supports HTML/Markdown)
            chat_id: Target chat ID
            parse_mode: "HTML" or "Markdown" (default: HTML)
            disable_notification: True = silent, False = sound (default: False)
        """
        target = chat_id or self.default_chat_id
        if not target:
            logger.error("[NotificationBot] No Chat ID provided for alert")
            return

        try:
            await self.broadcast_message(
                target, 
                message,
                parse_mode=parse_mode,
                disable_notification=disable_notification
            )
            logger.info(f"[NotificationBot] Sent alert to {target}")
        except Exception as e:
            logger.error(f"[NotificationBot] Failed to send alert: {e}")

    async def send_trade_event(self, trade_data: dict, chat_id: str = None):
        """
        Format and send a trade event with inline keyboard for quick actions.
        """
        symbol = trade_data.get('symbol', 'UNKNOWN')
        action = trade_data.get('action', 'INFO')
        price = trade_data.get('price', 0)
        ticket = trade_data.get('ticket', None)
        
        msg = (
            f"⚡ <b>TRADE ALERT</b>\n"
            f"━━━━━━━━━━━━━━\n"
            f"<b>Symbol:</b> <code>{symbol}</code>\n"
            f"<b>Action:</b> {action}\n"
            f"<b>Price:</b> {price}\n"
        )
        
        # Add inline keyboard for quick actions if ticket exists
        keyboard = None
        if ticket:
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🛑 Close Trade", callback_data=f"close_trade_{ticket}"),
                    InlineKeyboardButton("📊 Details", callback_data=f"trade_details_{ticket}")
                ],
                [
                    InlineKeyboardButton("🎯 Modify TP", callback_data=f"modify_tp_{ticket}"),
                    InlineKeyboardButton("🛑 Modify SL", callback_data=f"modify_sl_{ticket}")
                ]
            ])
        
        await self.send_alert(msg, chat_id, parse_mode="HTML")
        
        # Send keyboard separately if exists (to maintain compatibility)
        if keyboard:
            try:
                target = chat_id or self.default_chat_id
                if self.app and self.app.bot:
                    await self.app.bot.send_message(
                        chat_id=target,
                        text="⚡ Quick Actions:",
                        reply_markup=keyboard
                    )
            except Exception as e:
                logger.error(f"[NotificationBot] Failed to send inline keyboard: {e}")
    
    # ==================== V6 NOTIFICATION METHODS ====================
    
    async def send_v6_entry_alert(self, trade_data: dict, chat_id: str = None):
        """
        V6 PRICE ACTION ENTRY - According to Update File 06_V6_PRICE_ACTION_TELEGRAM.md
        
        Features:
        - Timeframe badges: [15M] [30M] [1H] [4H]
        - Price Action pattern details
        - Trend Pulse visualization bars
        - Higher TF trend alignment
        - Shadow mode indicator 👻
        - Dual order details (A + B)
        - Risk:Reward ratio
        """
        timeframe = trade_data.get('timeframe', '??')
        symbol = trade_data.get('symbol', 'UNKNOWN')
        direction = trade_data.get('direction', 'BUY')
        entry_price = trade_data.get('entry_price', 0)
        pattern = trade_data.get('price_action_pattern', 'UNKNOWN')
        pulse_strength = trade_data.get('trend_pulse_strength', 0)
        higher_tf_trend = trade_data.get('higher_tf_trend', 'NEUTRAL')
        is_shadow = trade_data.get('is_shadow_mode', False)
        
        # Timeframe badges according to spec
        tf_badges = {
            '15M': '[15M]', '15m': '[15M]',
            '30M': '[30M]', '30m': '[30M]',
            '1H': '[1H]', '1h': '[1H]',
            '4H': '[4H]', '4h': '[4H]',
            '1M': '[1M]', '1m': '[1M]',
            '5M': '[5M]', '5m': '[5M]'
        }
        tf_badge = tf_badges.get(timeframe, f'[{timeframe}]')
        
        # Timeframe emojis
        tf_emojis = {
            '15M': '⏱️', '30M': '⏱️', '1H': '🕐', '4H': '🕓',
            '1M': '⏱️', '5M': '⏱️'
        }
        tf_emoji = tf_emojis.get(timeframe, '⏱️')
        
        # Trend Pulse bars (according to spec)
        full_blocks = pulse_strength
        empty_blocks = 10 - pulse_strength
        pulse_bar = "█" * full_blocks + "░" * empty_blocks
        
        # Direction emoji
        dir_emoji = "📈" if direction == "BUY" else "📉"
        
        # Higher TF alignment icon
        trend_icon = "🟢" if higher_tf_trend == "BULLISH" else "🔴" if higher_tf_trend == "BEARISH" else "⚪"
        
        # Shadow mode flag
        shadow_icon = "👻 SHADOW" if is_shadow else "🎯 LIVE"
        
        # Calculate R:R
        sl_pips = trade_data.get('sl_pips', 0)
        tp_pips = trade_data.get('tp_pips', 0)
        rr_ratio = (tp_pips / sl_pips) if sl_pips > 0 else 0
        
        # Build notification according to Update File template
        msg = (
            f"🎯 **V6 ENTRY {tf_badge}** {shadow_icon}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"**Symbol:** {symbol}\n"
            f"**Direction:** {dir_emoji} {direction}\n"
            f"**Timeframe:** {tf_emoji} {timeframe}\n\n"
            f"📍 **Entry:** `{entry_price}`\n"
            f"🛑 **SL:** `{trade_data.get('order_a_sl', 0)}` ({sl_pips:.1f} pips)\n"
            f"🎯 **TP:** `{trade_data.get('order_a_tp', 0)}` ({tp_pips:.1f} pips)\n\n"
            f"💰 **Lot:** {trade_data.get('order_a_lot', 0)}\n"
            f"📊 **R:R:** 1:{rr_ratio:.1f}\n\n"
            f"**🎯 PRICE ACTION ANALYSIS**\n"
            f"├─ Pattern: {pattern}\n"
            f"├─ Trend Pulse: {pulse_bar} ({pulse_strength}/10)\n"
            f"├─ Higher TF: {trend_icon} {higher_tf_trend}\n"
            f"└─ Trigger: {trade_data.get('signal_type', 'TREND_PULSE')}\n\n"
        )
        
        # Dual Order details
        if trade_data.get('order_b_lot'):
            msg += (
                f"**💼 DUAL ORDER:**\n"
                f"├─ Order A: {trade_data.get('order_a_lot', 0)} lot (Main)\n"
                f"└─ Order B: {trade_data.get('order_b_lot', 0)} lot (Runner)\n\n"
            )
        
        msg += (
            f"🔶 Plugin: V6 Price Action\n"
            f"⏰ {trade_data.get('timestamp', 'N/A')}\n"
        )
        
        await self.send_alert(msg, chat_id)
        logger.info(f"[NotificationBot] V6 Entry: {symbol} {tf_badge} {direction}")
    
    async def send_v6_exit_alert(self, trade_data: dict, chat_id: str = None):
        """
        V6 PRICE ACTION EXIT - According to Update File 06_V6_PRICE_ACTION_TELEGRAM.md
        
        Features:
        - Timeframe badges: [15M] [30M] [1H] [4H]
        - Exit type icons: ✅TP ❌SL 🔧Manual 🔄Reversal
        - P&L in USD/pips/%
        - Trade duration
        - ROI calculation
        - Entry pattern recap
        """
        timeframe = trade_data.get('timeframe', '??')
        symbol = trade_data.get('symbol', 'UNKNOWN')
        direction = trade_data.get('direction', 'BUY')
        exit_type = trade_data.get('exit_type', 'EXIT')
        pattern = trade_data.get('entry_pattern', 'UNKNOWN')
        pnl = trade_data.get('pnl_usd', 0)
        pips = trade_data.get('pnl_pips', 0)
        roi = trade_data.get('pnl_percentage', 0)
        duration = trade_data.get('duration_minutes', 0)
        is_shadow = trade_data.get('is_shadow_mode', False)
        
        # Timeframe badge
        tf_badges = {'15M': '[15M]', '30M': '[30M]', '1H': '[1H]', '4H': '[4H]', '1M': '[1M]', '5M': '[5M]'}
        tf_badge = tf_badges.get(timeframe, f'[{timeframe}]')
        
        # Exit type icon
        exit_icons = {'TP_HIT': '✅', 'SL_HIT': '❌', 'MANUAL': '🔧', 'REVERSAL': '🔄'}
        exit_icon = exit_icons.get(exit_type, '🔔')
        
        # P&L color
        pnl_icon = "💚" if pnl > 0 else "💔" if pnl < 0 else "💛"
        shadow_flag = "👻 [SHADOW MODE]" if is_shadow else ""
        
        msg = (
            f"🟢 **V6 PRICE ACTION EXIT [{timeframe}]** {shadow_flag}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📍 **Symbol:** `{symbol}` | {exit_icon} {exit_type}\n"
            f"📊 **Direction:** {direction}\n"
            f"🎯 **Entry Pattern:** {pattern}\n\n"
            f"{pnl_icon} **PROFIT & LOSS**\n"
            f"├─ P&L: {'+'if pnl > 0 else ''}{pnl:.2f} USD\n"
            f"├─ Pips: {'+'if pips > 0 else ''}{pips:.1f} pips\n"
            f"├─ ROI: {'+'if roi > 0 else ''}{roi:.1f}%\n"
            f"└─ Duration: {duration} minutes\n\n"
            f"📈 **TRADE SUMMARY**\n"
            f"├─ Entry: {trade_data.get('entry_price', 0)}\n"
            f"├─ Exit: {trade_data.get('exit_price', 0)}\n"
            f"└─ Reason: {trade_data.get('exit_reason_detail', 'N/A')}\n\n"
            f"🎫 **Ticket:** #{trade_data.get('ticket', 0)}\n"
            f"🔖 **Plugin:** V6-{timeframe}\n"
        )
        
        await self.send_alert(msg, chat_id)
        logger.info(f"[NotificationBot] Sent V6 exit alert for {symbol} [{timeframe}]")
    
    async def send_trend_pulse_alert(self, pulse_data: dict, chat_id: str = None):
        """
        Send Trend Pulse detection alert.
        
        Required fields:
        - symbol: str
        - timeframe: str
        - pulse_strength: int (1-10)
        - trend_direction: str ('BULLISH', 'BEARISH')
        - price: float
        - higher_tf_aligned: bool
        """
        symbol = pulse_data.get('symbol', 'UNKNOWN')
        timeframe = pulse_data.get('timeframe', '??')
        strength = pulse_data.get('pulse_strength', 0)
        direction = pulse_data.get('trend_direction', 'UNKNOWN')
        price = pulse_data.get('price', 0)
        aligned = pulse_data.get('higher_tf_aligned', False)
        
        pulse_bar = "█" * strength + "░" * (10 - strength)
        direction_icon = "🟢" if direction == "BULLISH" else "🔴"
        align_icon = "✅" if aligned else "⚠️"
        
        msg = (
            f"🎯 **TREND PULSE DETECTED**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📍 **Symbol:** `{symbol}`\n"
            f"⏱️ **Timeframe:** {timeframe}\n"
            f"📊 **Price:** {price}\n\n"
            f"💫 **PULSE ANALYSIS**\n"
            f"├─ Direction: {direction_icon} {direction}\n"
            f"├─ Strength: {pulse_bar} ({strength}/10)\n"
            f"└─ Higher TF Aligned: {align_icon}\n\n"
            f"{'⚡ Strong pulse detected!' if strength >= 8 else '📊 Moderate pulse'}\n"
        )
        
        await self.send_alert(msg, chat_id)
        logger.info(f"[NotificationBot] Sent trend pulse alert for {symbol} [{timeframe}]")
    
    async def send_shadow_trade_alert(self, trade_data: dict, chat_id: str = None):
        """
        Send shadow mode trade notification.
        
        Required fields:
        - plugin_name: str
        - timeframe: str
        - symbol: str
        - direction: str
        - entry_price: float
        - would_have_traded: bool
        - rejection_reason: str (if would_have_traded=False)
        """
        plugin = trade_data.get('plugin_name', 'UNKNOWN')
        timeframe = trade_data.get('timeframe', '??')
        symbol = trade_data.get('symbol', 'UNKNOWN')
        direction = trade_data.get('direction', '??')
        price = trade_data.get('entry_price', 0)
        would_trade = trade_data.get('would_have_traded', False)
        reason = trade_data.get('rejection_reason', 'N/A')
        
        status_icon = "✅" if would_trade else "❌"
        
        msg = (
            f"👻 **SHADOW MODE TRADE**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔖 **Plugin:** {plugin} [{timeframe}]\n"
            f"📍 **Symbol:** `{symbol}`\n"
            f"📊 **Direction:** {direction} @ {price}\n\n"
            f"{status_icon} **Would Have Traded:** {'YES' if would_trade else 'NO'}\n"
        )
        
        if not would_trade:
            msg += f"❌ **Rejection Reason:** {reason}\n"
        else:
            msg += (
                f"\n💼 **Shadow Order Details:**\n"
                f"├─ Lot: {trade_data.get('lot_size', 0)}\n"
                f"├─ SL: {trade_data.get('sl', 0)}\n"
                f"└─ TP: {trade_data.get('tp', 0)}\n"
            )
        
        msg += f"\n💡 Shadow mode - No real trade executed\n"
        
        await self.send_alert(msg, chat_id)
        logger.info(f"[NotificationBot] Sent shadow trade alert for {symbol} [{timeframe}]")

    # ==================== STANDARD TRADE NOTIFICATIONS ====================
    
    async def send_trade_entry(self, trade_data: Dict, chat_id: int = None):
        """Send standard trade entry notification"""
        symbol = trade_data.get("symbol", "UNKNOWN")
        direction = trade_data.get("direction", "BUY")
        entry = trade_data.get("entry_price", 0.0)
        sl = trade_data.get("sl", 0.0)
        tp = trade_data.get("tp", 0.0)
        lot_size = trade_data.get("lot_size", 0.01)
        
        msg = (
            f"🔔 **TRADE ENTRY**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💱 {symbol}\n"
            f"{'📈 BUY' if direction == 'BUY' else '📉 SELL'}\n\n"
            f"💰 Entry: {entry:.5f}\n"
            f"🎯 TP: {tp:.5f}\n"
            f"🛡️ SL: {sl:.5f}\n"
            f"📊 Lot: {lot_size}\n"
        )
        
        await self.send_alert(msg, chat_id)
        logger.info(f"[NotificationBot] Sent trade entry: {symbol} {direction}")
        
    async def send_trade_exit(self, trade_data: Dict, chat_id: int = None):
        """Send trade exit notification"""
        symbol = trade_data.get("symbol", "UNKNOWN")
        direction = trade_data.get("direction", "BUY")
        entry = trade_data.get("entry_price", 0.0)
        exit_price = trade_data.get("exit_price", 0.0)
        profit = trade_data.get("profit", 0.0)
        pips = trade_data.get("pips", 0.0)
        reason = trade_data.get("reason", "TP")
        
        icon = "✅" if profit > 0 else "❌"
        
        msg = (
            f"{icon} **TRADE CLOSED**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💱 {symbol}\n"
            f"{'📈 BUY' if direction == 'BUY' else '📉 SELL'}\n\n"
            f"💰 Entry: {entry:.5f}\n"
            f"🚪 Exit: {exit_price:.5f}\n"
            f"💵 Profit: ${profit:.2f}\n"
            f"📊 Pips: {pips:+.1f}\n"
            f"🔚 Reason: {reason}\n"
        )
        
        await self.send_alert(msg, chat_id)
        logger.info(f"[NotificationBot] Sent trade exit: {symbol} ${profit:.2f}")
        
    async def send_trade_update(self, trade_data: Dict, chat_id: int = None):
        """Send trade update notification"""
        symbol = trade_data.get("symbol", "UNKNOWN")
        current_price = trade_data.get("current_price", 0.0)
        unrealized_pnl = trade_data.get("unrealized_pnl", 0.0)
        pips = trade_data.get("pips", 0.0)
        
        icon = "🟢" if unrealized_pnl > 0 else "🔴"
        
        msg = (
            f"{icon} **TRADE UPDATE**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"💱 {symbol}\n"
            f"💰 Current: {current_price:.5f}\n"
            f"💵 P&L: ${unrealized_pnl:+.2f}\n"
            f"📊 Pips: {pips:+.1f}\n"
        )
        
        await self.send_alert(msg, chat_id)
        
    async def send_error_alert(self, error_msg: str, details: str = "", chat_id: int = None):
        """Send error alert"""
        msg = (
            f"🔴 **ERROR ALERT**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⚠️ {error_msg}\n"
        )
        
        if details:
            msg += f"\n📝 Details:\n{details}\n"
            
        await self.send_alert(msg, chat_id)
        logger.error(f"[NotificationBot] Error alert: {error_msg}")
        
    async def send_status_update(self, status_data: Dict, chat_id: int = None):
        """Send status update"""
        bot_status = status_data.get("bot_status", "UNKNOWN")
        active_trades = status_data.get("active_trades", 0)
        today_pnl = status_data.get("today_pnl", 0.0)
        
        icon = "✅" if bot_status == "RUNNING" else "⚠️"
        
        msg = (
            f"{icon} **STATUS UPDATE**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🤖 Bot: {bot_status}\n"
            f"📊 Active Trades: {active_trades}\n"
            f"💰 Today P&L: ${today_pnl:+.2f}\n"
        )
        
        await self.send_alert(msg, chat_id)
        
    async def send_daily_summary(self, summary_data: Dict, chat_id: int = None):
        """Send daily summary"""
        total_trades = summary_data.get("total_trades", 0)
        wins = summary_data.get("wins", 0)
        losses = summary_data.get("losses", 0)
        profit = summary_data.get("profit", 0.0)
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        
        msg = (
            f"📊 **DAILY SUMMARY**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 {summary_data.get('date', 'Today')}\n\n"
            f"📈 Total Trades: {total_trades}\n"
            f"✅ Wins: {wins}\n"
            f"❌ Losses: {losses}\n"
            f"📊 Win Rate: {win_rate:.1f}%\n"
            f"💰 Profit: ${profit:+.2f}\n"
        )
        
        await self.send_alert(msg, chat_id)
        logger.info(f"[NotificationBot] Sent daily summary: {total_trades} trades, ${profit:.2f}")
        
    async def send_weekly_report(self, report_data: Dict, chat_id: int = None):
        """Send weekly report"""
        week = report_data.get("week", "This Week")
        total_trades = report_data.get("total_trades", 0)
        profit = report_data.get("profit", 0.0)
        best_day = report_data.get("best_day", {})
        
        msg = (
            f"📊 **WEEKLY REPORT**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📅 {week}\n\n"
            f"📈 Total Trades: {total_trades}\n"
            f"💰 Profit: ${profit:+.2f}\n"
            f"🏆 Best Day: ${best_day.get('profit', 0):.2f}\n"
        )
        
        await self.send_alert(msg, chat_id)
        
    async def send_performance_alert(self, alert_data: Dict, chat_id: int = None):
        """Send performance alert"""
        alert_type = alert_data.get("type", "INFO")
        message = alert_data.get("message", "")
        
        icons = {"INFO": "ℹ️", "WARNING": "⚠️", "SUCCESS": "✅", "DANGER": "🔴"}
        icon = icons.get(alert_type, "ℹ️")
        
        msg = (
            f"{icon} **PERFORMANCE ALERT**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{message}\n"
        )
        
        await self.send_alert(msg, chat_id)
        
    async def send_risk_warning(self, warning_data: Dict, chat_id: int = None):
        """Send risk warning"""
        risk_level = warning_data.get("risk_level", "MEDIUM")
        message = warning_data.get("message", "")
        current_dd = warning_data.get("drawdown", 0.0)
        
        msg = (
            f"⚠️ **RISK WARNING**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"🔴 Risk Level: {risk_level}\n"
            f"📉 Drawdown: {current_dd:.1f}%\n\n"
            f"{message}\n"
        )
        
        await self.send_alert(msg, chat_id)
        logger.warning(f"[NotificationBot] Risk warning: {risk_level} - DD {current_dd}%")
        
    async def send_system_alert(self, alert_msg: str, chat_id: int = None):
        """Send system alert"""
        msg = (
            f"🔔 **SYSTEM ALERT**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{alert_msg}\n"
        )
        
        await self.send_alert(msg, chat_id)
        
    async def send_custom_message(self, message: str, chat_id: int = None):
        """Send custom message"""
        await self.send_alert(message, chat_id)
