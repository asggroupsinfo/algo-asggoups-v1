"""
Notification Bot - Handles trade alerts and notifications

This bot handles all trading-related notifications:
- Entry alerts
- Exit alerts
- Partial profit bookings
- SL/TP modifications
- Error alerts

Version: 1.0.0
Date: 2026-01-14
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime

from .base_telegram_bot import BaseTelegramBot
from .v6_notification_templates import (
    create_progress_bar, format_pnl, format_win_rate,
    create_v6_trade_actions_keyboard
)

logger = logging.getLogger(__name__)


class NotificationBot(BaseTelegramBot):
    """
    Notification Bot for trade alerts and updates.
    
    Responsibilities:
    - Entry alerts (when trade placed)
    - Exit alerts (when trade closed)
    - Partial profit bookings
    - SL/TP modifications
    - Error alerts
    - Daily summary notifications
    """
    
    def __init__(self, token: str, chat_id: str = None):
        super().__init__(token, chat_id, bot_name="NotificationBot")
        
        self._voice_alerts_enabled = False
        self._voice_alert_system = None
        
        logger.info("[NotificationBot] Initialized")
    
    def set_voice_alert_system(self, voice_system):
        """Set voice alert system for audio notifications"""
        self._voice_alert_system = voice_system
        self._voice_alerts_enabled = voice_system is not None
        logger.info(f"[NotificationBot] Voice alerts: {'enabled' if self._voice_alerts_enabled else 'disabled'}")
    
    async def send_notification(self, notification_type: str, message: str, **kwargs) -> Optional[int]:
        """
        Async handler for Router notifications.
        Delegates to specialized Sync methods for Rich Formatting + Voice.
        """
        trade_data = kwargs.get('trade_data')
        
        if notification_type == 'trade_opened' and trade_data:
            # Delegate to send_entry_alert (Sync)
            return self.send_entry_alert(trade_data)
            
        elif notification_type in ['trade_closed', 'position_closed'] and trade_data:
             return self.send_exit_alert(trade_data)
             
        elif notification_type == 'profit_booked' and isinstance(kwargs.get('booking_data'), dict):
             return self.send_profit_booking_alert(kwargs['booking_data'])
             
        elif notification_type == 'error_alert' and isinstance(kwargs.get('error_data'), dict):
             return self.send_error_alert(kwargs['error_data'])
             
        # Fallback: Just send the text message
        return self.send_message(message)
    
    def send_entry_alert(self, trade_data: Dict) -> Optional[int]:
        """
        Send entry notification for new trade
        
        Args:
            trade_data: Dict with trade details
                - plugin_name: Plugin that placed the trade
                - symbol: Trading symbol
                - direction: BUY or SELL
                - entry_price: Entry price
                - order_a_lot: Order A lot size
                - order_a_sl: Order A stop loss
                - order_a_tp: Order A take profit
                - order_b_lot: Order B lot size (optional)
                - order_b_sl: Order B stop loss (optional)
                - order_b_tp: Order B take profit (optional)
                - signal_type: Signal that triggered entry
                - timeframe: Timeframe
                - logic_route: Logic route (LOGIC1/2/3)
                - ticket_a: MT5 ticket for Order A
                - ticket_b: MT5 ticket for Order B (optional)
        
        Returns:
            Message ID if successful
        """
        message = self._format_entry_message(trade_data)
        result = self.send_message(message)
        
        if self._voice_alerts_enabled and self._voice_alert_system:
            try:
                voice_text = f"New {trade_data.get('direction', 'trade')} on {trade_data.get('symbol', 'unknown')} at {trade_data.get('entry_price', 0)}"
                self._voice_alert_system.speak(voice_text)
            except Exception as e:
                logger.error(f"[NotificationBot] Voice alert error: {e}")
        
        return result
    
    def _format_entry_message(self, trade_data: Dict) -> str:
        """Format entry notification message"""
        plugin_name = trade_data.get('plugin_name', 'Unknown Plugin')
        symbol = trade_data.get('symbol', 'N/A')
        direction = trade_data.get('direction', 'N/A')
        entry_price = trade_data.get('entry_price', 0)
        
        message = (
            f"🟢 <b>ENTRY ALERT</b> | {plugin_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Symbol:</b> {symbol}\n"
            f"<b>Direction:</b> {direction}\n"
            f"<b>Entry Price:</b> {entry_price}\n\n"
            f"<b>Order Details:</b>\n"
        )
        
        if trade_data.get('order_a_lot'):
            message += (
                f"├─ Order A: {trade_data.get('order_a_lot')} lots\n"
                f"│  SL: {trade_data.get('order_a_sl', 'N/A')}\n"
                f"│  TP: {trade_data.get('order_a_tp', 'N/A')}\n"
            )
        
        if trade_data.get('order_b_lot'):
            message += (
                f"├─ Order B: {trade_data.get('order_b_lot')} lots\n"
                f"│  SL: {trade_data.get('order_b_sl', 'N/A')}\n"
                f"│  TP: {trade_data.get('order_b_tp', 'N/A')}\n"
            )
        
        message += (
            f"\n<b>Signal:</b> {trade_data.get('signal_type', 'N/A')}\n"
            f"<b>Timeframe:</b> {trade_data.get('timeframe', 'N/A')}\n"
            f"<b>Logic Route:</b> {trade_data.get('logic_route', 'N/A')}\n\n"
        )
        
        tickets = []
        if trade_data.get('ticket_a'):
            tickets.append(f"#{trade_data['ticket_a']}")
        if trade_data.get('ticket_b'):
            tickets.append(f"#{trade_data['ticket_b']}")
        
        if tickets:
            message += f"<b>MT5 Tickets:</b> {', '.join(tickets)}\n"
        
        message += f"<b>Entry Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        return message
    
    def send_exit_alert(self, trade_data: Dict) -> Optional[int]:
        """
        Send exit notification for closed trade
        
        Args:
            trade_data: Dict with trade details
                - plugin_name: Plugin name
                - symbol: Trading symbol
                - direction: Original direction
                - entry_price: Entry price
                - exit_price: Exit price
                - hold_time: How long position was held
                - order_a_profit: Order A profit
                - order_a_pips: Order A pips
                - order_b_profit: Order B profit (optional)
                - order_b_pips: Order B pips (optional)
                - total_profit: Total profit
                - total_pips: Total pips
                - commission: Commission paid
                - reason: Close reason
        
        Returns:
            Message ID if successful
        """
        message = self._format_exit_message(trade_data)
        result = self.send_message(message)
        
        if self._voice_alerts_enabled and self._voice_alert_system:
            try:
                profit = trade_data.get('total_profit', 0)
                voice_text = f"Trade closed on {trade_data.get('symbol', 'unknown')}. {'Profit' if profit >= 0 else 'Loss'}: {abs(profit):.0f} dollars"
                self._voice_alert_system.speak(voice_text)
            except Exception as e:
                logger.error(f"[NotificationBot] Voice alert error: {e}")
        
        return result
    
    def _format_exit_message(self, trade_data: Dict) -> str:
        """Format exit notification message"""
        plugin_name = trade_data.get('plugin_name', 'Unknown Plugin')
        symbol = trade_data.get('symbol', 'N/A')
        direction = trade_data.get('direction', 'N/A')
        total_profit = trade_data.get('total_profit', 0)
        
        emoji = "🔴" if total_profit < 0 else "🟢"
        
        message = (
            f"{emoji} <b>EXIT ALERT</b> | {plugin_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Symbol:</b> {symbol}\n"
            f"<b>Direction:</b> {direction} → CLOSED\n\n"
            f"<b>Entry:</b> {trade_data.get('entry_price', 'N/A')} | "
            f"<b>Exit:</b> {trade_data.get('exit_price', 'N/A')}\n"
            f"<b>Hold Time:</b> {trade_data.get('hold_time', 'N/A')}\n\n"
            f"<b>Results:</b>\n"
        )
        
        if trade_data.get('order_a_profit') is not None:
            a_profit = trade_data['order_a_profit']
            a_pips = trade_data.get('order_a_pips', 0)
            a_emoji = "✅" if a_profit >= 0 else "❌"
            message += f"├─ Order A: {a_emoji} ${a_profit:+.2f} ({a_pips:+.1f} pips)\n"
        
        if trade_data.get('order_b_profit') is not None:
            b_profit = trade_data['order_b_profit']
            b_pips = trade_data.get('order_b_pips', 0)
            b_emoji = "✅" if b_profit >= 0 else "❌"
            message += f"├─ Order B: {b_emoji} ${b_profit:+.2f} ({b_pips:+.1f} pips)\n"
        
        total_pips = trade_data.get('total_pips', 0)
        commission = trade_data.get('commission', 0)
        net_profit = total_profit - abs(commission)
        
        message += (
            f"\n<b>Total P&L:</b> ${total_profit:+.2f} ({total_pips:+.1f} pips)\n"
            f"<b>Commission:</b> ${commission:.2f}\n"
            f"<b>Net Profit:</b> ${net_profit:+.2f}\n\n"
            f"<b>Reason:</b> {trade_data.get('reason', 'N/A')}\n"
            f"<b>Close Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        )
        
        return message
    
    def send_profit_booking_alert(self, booking_data: Dict) -> Optional[int]:
        """
        Send partial profit booking notification
        
        Args:
            booking_data: Dict with booking details
                - plugin_name: Plugin name
                - symbol: Trading symbol
                - direction: Trade direction
                - ticket: MT5 ticket
                - closed_percentage: Percentage closed
                - closed_lots: Lots closed
                - remaining_lots: Remaining lots
                - booking_profit: Profit from this booking
                - booking_pips: Pips from this booking
                - total_profit: Total position profit
                - action: What triggered booking (TP1, TP2, etc.)
                - next_target: Next TP target
        
        Returns:
            Message ID if successful
        """
        message = self._format_profit_booking_message(booking_data)
        return self.send_message(message)
    
    def _format_profit_booking_message(self, booking_data: Dict) -> str:
        """Format profit booking notification message"""
        plugin_name = booking_data.get('plugin_name', 'Unknown Plugin')
        symbol = booking_data.get('symbol', 'N/A')
        direction = booking_data.get('direction', 'N/A')
        
        message = (
            f"💰 <b>PROFIT BOOKED</b> | {plugin_name}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Symbol:</b> {symbol} {direction}\n"
            f"<b>Position:</b> #{booking_data.get('ticket', 'N/A')}\n\n"
            f"<b>Booking Details:</b>\n"
            f"• Closed: {booking_data.get('closed_percentage', 0)}% ({booking_data.get('closed_lots', 0)} lots)\n"
            f"• Remaining: {100 - booking_data.get('closed_percentage', 0)}% ({booking_data.get('remaining_lots', 0)} lots)\n\n"
            f"<b>P&L:</b>\n"
            f"• This Booking: ${booking_data.get('booking_profit', 0):+.2f} ({booking_data.get('booking_pips', 0):+.1f} pips)\n"
            f"• Total Position: ${booking_data.get('total_profit', 0):+.2f}\n\n"
            f"<b>Action:</b> {booking_data.get('action', 'N/A')}\n"
            f"<b>Next Target:</b> {booking_data.get('next_target', 'N/A')}"
        )
        
        return message
    
    def send_error_alert(self, error_data: Dict) -> Optional[int]:
        """
        Send error notification
        
        Args:
            error_data: Dict with error details
                - error_type: Type of error
                - severity: HIGH, MEDIUM, LOW
                - details: Error description
                - status: Current status
                - action_required: Whether manual action needed
        
        Returns:
            Message ID if successful
        """
        message = self._format_error_message(error_data)
        return self.send_message(message)
    
    def _format_error_message(self, error_data: Dict) -> str:
        """Format error notification message"""
        severity = error_data.get('severity', 'MEDIUM')
        severity_emoji = "🔴" if severity == "HIGH" else ("🟡" if severity == "MEDIUM" else "🟢")
        
        message = (
            f"❌ <b>ERROR ALERT</b> | System\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Error Type:</b> {error_data.get('error_type', 'Unknown')}\n"
            f"<b>Severity:</b> {severity_emoji} {severity}\n"
            f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}\n\n"
            f"<b>Details:</b>\n{error_data.get('details', 'No details available')}\n\n"
            f"<b>Status:</b> {error_data.get('status', 'N/A')}\n"
        )
        
        if error_data.get('action_required'):
            message += "\n📌 <b>Manual Action Required</b>"
        
        return message
    
    def send_daily_summary(self, summary_data: Dict) -> Optional[int]:
        """
        Send daily summary notification
        
        Args:
            summary_data: Dict with daily summary
                - date: Summary date
                - total_trades: Total trades
                - winning_trades: Winning trades
                - losing_trades: Losing trades
                - win_rate: Win rate percentage
                - total_profit: Total profit
                - best_trade: Best trade profit
                - worst_trade: Worst trade loss
        
        Returns:
            Message ID if successful
        """
        date = summary_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        total_trades = summary_data.get('total_trades', 0)
        winning = summary_data.get('winning_trades', 0)
        losing = summary_data.get('losing_trades', 0)
        win_rate = summary_data.get('win_rate', 0)
        total_profit = summary_data.get('total_profit', 0)
        
        emoji = "🟢" if total_profit >= 0 else "🔴"
        
        message = (
            f"📊 <b>DAILY SUMMARY</b> | {date}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>Trades:</b> {total_trades} total\n"
            f"• ✅ Winning: {winning}\n"
            f"• ❌ Losing: {losing}\n"
            f"• 📈 Win Rate: {win_rate:.1f}%\n\n"
            f"<b>P&L:</b>\n"
            f"• {emoji} Total: ${total_profit:+.2f}\n"
            f"• 🏆 Best: ${summary_data.get('best_trade', 0):+.2f}\n"
            f"• 📉 Worst: ${summary_data.get('worst_trade', 0):+.2f}"
        )
        
        return self.send_message(message)
    
    # ========================================
    # V6-Specific Notification Methods (Phase 1 Implementation)
    # ========================================
    
    def send_v6_entry_alert(self, trade_data: Dict) -> Optional[int]:
        """
        Send V6 Price Action entry alert with timeframe and pattern details
        
        Args:
            trade_data: Dict with V6-specific trade details
                - All standard fields from send_entry_alert()
                - timeframe: V6 timeframe (15M/30M/1H/4H) - REQUIRED
                - pattern_strength: Strong BUY/SELL strength
                - trend_pulse: Trend pulse strength (0-10)
                - shadow_mode: Whether this is shadow mode
                - pattern_type: Pattern that triggered entry
        
        Returns:
            Message ID if successful
        """
        message = self._format_v6_entry_message(trade_data)
        result = self.send_message(message)
        
        if self._voice_alerts_enabled and self._voice_alert_system:
            try:
                timeframe = trade_data.get('timeframe', 'unknown')
                voice_text = f"V6 {timeframe} {trade_data.get('direction', 'trade')} on {trade_data.get('symbol', 'unknown')}"
                if trade_data.get('shadow_mode'):
                    voice_text += " in shadow mode"
                self._voice_alert_system.speak(voice_text)
            except Exception as e:
                logger.error(f"[NotificationBot] V6 voice alert error: {e}")
        
        return result
    
    def _format_v6_entry_message(self, trade_data: Dict) -> str:
        """Format V6-specific entry notification with timeframe and pattern details"""
        symbol = trade_data.get('symbol', 'N/A')
        direction = trade_data.get('direction', 'N/A')
        entry_price = trade_data.get('entry_price', 0)
        timeframe = trade_data.get('timeframe', 'N/A').upper()
        shadow_mode = trade_data.get('shadow_mode', False)
        
        # V6-specific header
        header = "👻 <b>V6 SHADOW MODE ENTRY</b>" if shadow_mode else "🎯 <b>V6 PRICE ACTION ENTRY</b>"
        
        message = (
            f"{header}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⏱️ <b>Timeframe:</b> {timeframe}\n"
            f"📊 <b>Symbol:</b> {symbol}\n"
            f"📈 <b>Direction:</b> {direction}\n"
            f"💰 <b>Entry Price:</b> {entry_price}\n\n"
        )
        
        # Pattern details
        if trade_data.get('pattern_type'):
            message += f"🎨 <b>Pattern:</b> {trade_data['pattern_type']}\n"
        
        if trade_data.get('pattern_strength'):
            message += f"💪 <b>Strength:</b> {trade_data['pattern_strength']}\n"
        
        # Trend Pulse (if available)
        if trade_data.get('trend_pulse') is not None:
            pulse = trade_data['trend_pulse']
            pulse_emoji = "🟢" if pulse >= 7 else "🟡" if pulse >= 4 else "🔴"
            message += f"{pulse_emoji} <b>Trend Pulse:</b> {pulse}/10\n"
        
        message += "\n<b>Order Details:</b>\n"
        
        # Order details
        if trade_data.get('order_a_lot'):
            message += (
                f"├─ Order A: {trade_data.get('order_a_lot')} lots\n"
                f"│  SL: {trade_data.get('order_a_sl', 'N/A')}\n"
                f"│  TP: {trade_data.get('order_a_tp', 'N/A')}\n"
            )
        
        if trade_data.get('order_b_lot'):
            message += (
                f"├─ Order B: {trade_data.get('order_b_lot')} lots\n"
                f"│  SL: {trade_data.get('order_b_sl', 'N/A')}\n"
                f"│  TP: {trade_data.get('order_b_tp', 'N/A')}\n"
            )
        
        # Tickets
        tickets = []
        if trade_data.get('ticket_a'):
            tickets.append(f"#{trade_data['ticket_a']}")
        if trade_data.get('ticket_b'):
            tickets.append(f"#{trade_data['ticket_b']}")
        
        if tickets:
            message += f"\n<b>MT5 Tickets:</b> {', '.join(tickets)}\n"
        
        if shadow_mode:
            message += "\n👻 <b>Note:</b> Shadow mode - No real orders placed\n"
        
        message += f"<b>Entry Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        return message
    
    def send_v6_exit_alert(self, trade_data: Dict) -> Optional[int]:
        """
        Send V6 Price Action exit alert with pattern and timeframe details
        
        Args:
            trade_data: Dict with V6-specific exit details
                - All standard fields from send_exit_alert()
                - timeframe: V6 timeframe (15M/30M/1H/4H)
                - exit_pattern: Pattern that triggered exit
                - shadow_mode: Whether this was shadow mode
                - timeframe_pnl: P&L breakdown by timeframe (optional)
        
        Returns:
            Message ID if successful
        """
        message = self._format_v6_exit_message(trade_data)
        result = self.send_message(message)
        
        if self._voice_alerts_enabled and self._voice_alert_system:
            try:
                profit = trade_data.get('total_profit', 0)
                timeframe = trade_data.get('timeframe', 'unknown')
                voice_text = f"V6 {timeframe} closed. {'Profit' if profit >= 0 else 'Loss'}: {abs(profit):.0f} dollars"
                self._voice_alert_system.speak(voice_text)
            except Exception as e:
                logger.error(f"[NotificationBot] V6 voice alert error: {e}")
        
        return result
    
    def _format_v6_exit_message(self, trade_data: Dict) -> str:
        """Format V6-specific exit notification with pattern details"""
        symbol = trade_data.get('symbol', 'N/A')
        direction = trade_data.get('direction', 'N/A')
        total_profit = trade_data.get('total_profit', 0)
        total_pips = trade_data.get('total_pips', 0)
        timeframe = trade_data.get('timeframe', 'N/A').upper()
        shadow_mode = trade_data.get('shadow_mode', False)
        
        emoji = "🟢" if total_profit >= 0 else "🔴"
        header = "👻 <b>V6 SHADOW MODE EXIT</b>" if shadow_mode else f"{emoji} <b>V6 PRICE ACTION EXIT</b>"
        
        message = (
            f"{header}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⏱️ <b>Timeframe:</b> {timeframe}\n"
            f"📊 <b>Symbol:</b> {symbol}\n"
            f"📈 <b>Direction:</b> {direction}\n\n"
        )
        
        # Exit pattern
        if trade_data.get('exit_pattern'):
            message += f"🎨 <b>Exit Pattern:</b> {trade_data['exit_pattern']}\n"
        
        # Price details
        message += (
            f"💰 <b>Entry:</b> {trade_data.get('entry_price', 0)}\n"
            f"💰 <b>Exit:</b> {trade_data.get('exit_price', 0)}\n"
            f"⏰ <b>Duration:</b> {trade_data.get('hold_time', 'N/A')}\n\n"
        )
        
        # P&L breakdown
        message += "<b>P&L Results:</b>\n"
        
        if trade_data.get('order_a_profit') is not None:
            message += f"├─ Order A: ${trade_data['order_a_profit']:+.2f} ({trade_data.get('order_a_pips', 0):+.1f} pips)\n"
        
        if trade_data.get('order_b_profit') is not None:
            message += f"├─ Order B: ${trade_data['order_b_profit']:+.2f} ({trade_data.get('order_b_pips', 0):+.1f} pips)\n"
        
        message += (
            f"\n{emoji} <b>Total:</b> ${total_profit:+.2f} ({total_pips:+.1f} pips)\n"
        )
        
        if trade_data.get('commission'):
            message += f"💸 <b>Commission:</b> ${trade_data['commission']:.2f}\n"
        
        if trade_data.get('reason'):
            message += f"\n📌 <b>Close Reason:</b> {trade_data['reason']}\n"
        
        if shadow_mode:
            message += "\n👻 <b>Note:</b> Shadow mode - Virtual P&L only\n"
        
        message += f"<b>Exit Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        return message
    
    def send_trend_pulse_alert(self, pulse_data: Dict) -> Optional[int]:
        """
        Send Trend Pulse detection notification
        
        Args:
            pulse_data: Dict with trend pulse details
                - symbol: Trading symbol
                - timeframe: Affected timeframe
                - pulse_strength: Pulse strength (0-10)
                - direction: Trend direction (BULLISH/BEARISH)
                - previous_strength: Previous pulse strength
                - affected_timeframes: List of affected timeframes
        
        Returns:
            Message ID if successful
        """
        symbol = pulse_data.get('symbol', 'N/A')
        timeframe = pulse_data.get('timeframe', 'N/A').upper()
        strength = pulse_data.get('pulse_strength', 0)
        direction = pulse_data.get('direction', 'N/A')
        previous = pulse_data.get('previous_strength', 0)
        
        # Determine emoji based on strength
        if strength >= 8:
            strength_emoji = "🟢🟢🟢"
        elif strength >= 6:
            strength_emoji = "🟢🟢"
        elif strength >= 4:
            strength_emoji = "🟡"
        else:
            strength_emoji = "🔴"
        
        # Direction emoji
        dir_emoji = "📈" if direction == "BULLISH" else "📉" if direction == "BEARISH" else "➖"
        
        message = (
            f"🌊 <b>TREND PULSE DETECTION</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"📊 <b>Symbol:</b> {symbol}\n"
            f"⏱️ <b>Timeframe:</b> {timeframe}\n\n"
            f"{dir_emoji} <b>Direction:</b> {direction}\n"
            f"{strength_emoji} <b>Pulse Strength:</b> {strength}/10\n"
            f"📊 <b>Previous:</b> {previous}/10\n"
            f"📈 <b>Change:</b> {strength - previous:+.0f}\n"
        )
        
        # Affected timeframes
        if pulse_data.get('affected_timeframes'):
            tfs = ', '.join(pulse_data['affected_timeframes'])
            message += f"\n🎯 <b>Affected TFs:</b> {tfs}\n"
        
        # Trading recommendation
        if strength >= 7:
            message += "\n✅ <b>Signal:</b> Strong trend - High confidence entries\n"
        elif strength >= 5:
            message += "\n🟡 <b>Signal:</b> Moderate trend - Standard entries\n"
        else:
            message += "\n⚠️ <b>Signal:</b> Weak trend - Use caution\n"
        
        message += f"<b>Detection Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        
        return self.send_message(message)
    
    def send_shadow_mode_alert(self, shadow_data: Dict) -> Optional[int]:
        """
        Send Shadow Mode trade notification
        
        Args:
            shadow_data: Dict with shadow mode details
                - symbol: Trading symbol
                - timeframe: V6 timeframe
                - direction: Trade direction
                - entry_price: Virtual entry price
                - virtual_pnl: Current virtual P&L
                - pattern: Pattern that would trigger trade
                - message: Shadow mode message
        
        Returns:
            Message ID if successful
        """
        symbol = shadow_data.get('symbol', 'N/A')
        timeframe = shadow_data.get('timeframe', 'N/A').upper()
        direction = shadow_data.get('direction', 'N/A')
        entry_price = shadow_data.get('entry_price', 0)
        virtual_pnl = shadow_data.get('virtual_pnl', 0)
        
        pnl_emoji = "🟢" if virtual_pnl >= 0 else "🔴"
        
        message = (
            f"👻 <b>SHADOW MODE NOTIFICATION</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"⚠️ <b>NO REAL MONEY USED</b>\n\n"
            f"📊 <b>Symbol:</b> {symbol}\n"
            f"⏱️ <b>Timeframe:</b> {timeframe}\n"
            f"📈 <b>Direction:</b> {direction}\n"
            f"💰 <b>Entry Price:</b> {entry_price}\n"
        )
        
        if shadow_data.get('pattern'):
            message += f"🎨 <b>Pattern:</b> {shadow_data['pattern']}\n"
        
        if virtual_pnl != 0:
            message += f"\n{pnl_emoji} <b>Virtual P&L:</b> ${virtual_pnl:+.2f}\n"
        
        if shadow_data.get('message'):
            message += f"\n📝 <b>Details:</b> {shadow_data['message']}\n"
        
        message += (
            f"\n💡 <b>Purpose:</b> Testing V6 logic without risk\n"
            f"🔧 <b>Action:</b> Monitor performance, adjust if needed\n"
            f"<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}"
        )
        
        return self.send_message(message)

