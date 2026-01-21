"""
Notification Templates - Rich message templates for Telegram notifications

Provides formatted templates for all notification types with:
- HTML formatting for bold, italic, code
- Emoji indicators
- Progress bars
- Structured layout

Version: 1.0.0
Date: 2026-01-20
"""

from typing import Dict, Any
from datetime import datetime


def create_progress_bar(current: float, target: float, width: int = 10) -> str:
    """Create visual progress bar using Unicode characters"""
    percentage = min(current / target, 1.0) if target > 0 else 0
    filled = int(percentage * width)
    empty = width - filled
    
    bar = "█" * filled + "░" * empty
    return f"[{bar}] {percentage*100:.1f}%"


class NotificationTemplates:
    """All notification message templates with HTML formatting"""
    
    # ==================== TRADING TEMPLATES ====================
    
    ENTRY_TEMPLATE = """🟢 <b>TRADE ENTRY</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
<b>Direction:</b> {direction_emoji} {direction}
{plugin_badge}

📍 <b>Entry:</b> <code>{entry_price}</code>
🛑 <b>SL:</b> <code>{sl_price}</code> ({sl_pips} pips)
🎯 <b>TP:</b> <code>{tp_price}</code> ({tp_pips} pips)

💰 <b>Risk:</b> {lot_size} lot (${risk_amount:.2f})
📊 <b>R:R:</b> 1:{risk_reward:.1f}

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    EXIT_TEMPLATE = """{result_emoji} <b>TRADE EXIT</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
{plugin_badge}

📍 <b>Entry:</b> <code>{entry_price}</code>
📍 <b>Exit:</b> <code>{exit_price}</code>

💰 <b>Result:</b> {result_emoji} {pnl_sign}${pnl:.2f}
📊 <b>Pips:</b> {pips_sign}{pips:.1f}
⏱️ <b>Duration:</b> {duration}

📈 <b>Daily PnL:</b> ${daily_pnl:.2f}
━━━━━━━━━━━━━━━━━━━━━━"""

    TP_HIT_TEMPLATE = """🎯 <b>TP HIT</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
{plugin_badge}

📍 <b>Entry:</b> <code>{entry_price}</code>
🎯 <b>TP:</b> <code>{tp_price}</code>

💰 <b>Profit:</b> ✅ +${profit:.2f}
📊 <b>Pips:</b> +{pips:.1f}
⏱️ <b>Duration:</b> {duration}

🎉 <b>Target achieved!</b>
━━━━━━━━━━━━━━━━━━━━━━"""

    SL_HIT_TEMPLATE = """🛑 <b>SL HIT</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
{plugin_badge}

📍 <b>Entry:</b> <code>{entry_price}</code>
🛑 <b>SL:</b> <code>{sl_price}</code>

💰 <b>Loss:</b> ❌ -${loss:.2f}
📊 <b>Pips:</b> -{pips:.1f}
⏱️ <b>Duration:</b> {duration}

⚠️ <b>Risk managed</b>
━━━━━━━━━━━━━━━━━━━━━━"""

    BREAKEVEN_TEMPLATE = """⚖️ <b>BREAKEVEN MOVE</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
{plugin_badge}

📍 <b>Entry:</b> <code>{entry_price}</code>
🛑 <b>New SL:</b> <code>{new_sl}</code> (BE)

✅ <b>Trade now risk-free</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    SL_MODIFIED_TEMPLATE = """🔧 <b>SL MODIFIED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
{plugin_badge}

🛑 <b>Old SL:</b> <code>{old_sl}</code>
🛑 <b>New SL:</b> <code>{new_sl}</code>

📊 <b>Change:</b> {change_pips:+.1f} pips
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    PARTIAL_CLOSE_TEMPLATE = """💰 <b>PARTIAL CLOSE</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
{plugin_badge}

📊 <b>Closed:</b> {closed_lots} lot
📊 <b>Remaining:</b> {remaining_lots} lot

💰 <b>Profit:</b> +${profit:.2f}
📈 <b>Pips:</b> +{pips:.1f}

✅ <b>Profit booking</b>
━━━━━━━━━━━━━━━━━━━━━━"""

    # ==================== V6 PRICE ACTION TEMPLATES ====================
    
    V6_ENTRY_TEMPLATE = """🎯 <b>V6 ENTRY ({timeframe})</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
<b>Direction:</b> {direction_emoji} {direction}
<b>Timeframe:</b> {timeframe_emoji} {timeframe}

📍 <b>Entry:</b> <code>{entry_price}</code>
🛑 <b>SL:</b> <code>{sl_price}</code> ({sl_pips} pips)
🎯 <b>TP:</b> <code>{tp_price}</code> ({tp_pips} pips)

💰 <b>Risk:</b> {lot_size} lot
📊 <b>R:R:</b> 1:{risk_reward:.1f}

🔷 <b>Logic:</b> V6 Price Action
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    V6_EXIT_TEMPLATE = """{result_emoji} <b>V6 EXIT ({timeframe})</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
<b>Timeframe:</b> {timeframe_emoji} {timeframe}

📍 <b>Entry:</b> <code>{entry_price}</code>
📍 <b>Exit:</b> <code>{exit_price}</code>

💰 <b>Result:</b> {result_emoji} {pnl_sign}${pnl:.2f}
📊 <b>Pips:</b> {pips_sign}{pips:.1f}

🔷 <b>V6 Stats:</b>
  • Today: {v6_today_count} trades, ${v6_today_pnl:.2f}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    V6_TP_HIT_TEMPLATE = """🎯 <b>V6 TP HIT ({timeframe})</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
<b>Timeframe:</b> {timeframe_emoji} {timeframe}

📍 <b>Entry:</b> <code>{entry_price}</code>
🎯 <b>TP:</b> <code>{tp_price}</code>

💰 <b>Profit:</b> ✅ +${profit:.2f}
📊 <b>Pips:</b> +{pips:.1f}

🎉 <b>V6 Target achieved!</b>
━━━━━━━━━━━━━━━━━━━━━━━━"""

    V6_SL_HIT_TEMPLATE = """🛑 <b>V6 SL HIT ({timeframe})</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
<b>Timeframe:</b> {timeframe_emoji} {timeframe}

📍 <b>Entry:</b> <code>{entry_price}</code>
🛑 <b>SL:</b> <code>{sl_price}</code>

💰 <b>Loss:</b> ❌ -${loss:.2f}
📊 <b>Pips:</b> -{pips:.1f}

⚠️ <b>V6 Risk managed</b>
━━━━━━━━━━━━━━━━━━━━━━━━"""

    V6_TIMEFRAME_ENABLED_TEMPLATE = """✅ <b>V6 TIMEFRAME ENABLED</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Timeframe:</b> {timeframe_emoji} {timeframe}

🔷 <b>V6 Price Action</b>
✅ Now active and trading

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    V6_TIMEFRAME_DISABLED_TEMPLATE = """⏸️ <b>V6 TIMEFRAME DISABLED</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Timeframe:</b> {timeframe_emoji} {timeframe}

🔷 <b>V6 Price Action</b>
⏸️ Now paused

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━━━"""

    V6_DAILY_SUMMARY_TEMPLATE = """📊 <b>V6 DAILY SUMMARY</b>
━━━━━━━━━━━━━━━━━━━━━━━━

<b>Date:</b> {date}

<b>🎯 V6 Price Action Performance:</b>

<b>15M Timeframe:</b>
  • Trades: {tf_15m_trades}
  • PnL: ${tf_15m_pnl:+.2f}
  • Win Rate: {tf_15m_winrate:.1f}%

<b>30M Timeframe:</b>
  • Trades: {tf_30m_trades}
  • PnL: ${tf_30m_pnl:+.2f}
  • Win Rate: {tf_30m_winrate:.1f}%

<b>1H Timeframe:</b>
  • Trades: {tf_1h_trades}
  • PnL: ${tf_1h_pnl:+.2f}
  • Win Rate: {tf_1h_winrate:.1f}%

<b>4H Timeframe:</b>
  • Trades: {tf_4h_trades}
  • PnL: ${tf_4h_pnl:+.2f}
  • Win Rate: {tf_4h_winrate:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━
<b>📈 Total V6 PnL:</b> ${total_pnl:+.2f}
<b>🎯 Total Trades:</b> {total_trades}
<b>✅ Overall Win Rate:</b> {overall_winrate:.1f}%
━━━━━━━━━━━━━━━━━━━━━━━━"""

    # ==================== SIGNAL TEMPLATES ====================
    
    SIGNAL_RECEIVED_TEMPLATE = """📡 <b>SIGNAL RECEIVED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
<b>Direction:</b> {direction_emoji} {direction}
{plugin_badge}

<b>Entry Zone:</b> {entry_zone}
<b>SL:</b> {sl}
<b>TP:</b> {tp}

✅ <b>Signal accepted</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    TREND_CHANGED_TEMPLATE = """📊 <b>TREND CHANGED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}
{plugin_badge}

<b>Old Trend:</b> {old_trend}
<b>New Trend:</b> {new_trend_emoji} {new_trend}

⚠️ <b>Trading direction updated</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    TREND_MANUAL_SET_TEMPLATE = """🔧 <b>TREND MANUALLY SET</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Symbol:</b> {symbol}

<b>New Trend:</b> {trend_emoji} {trend}

✅ <b>Manual override active</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    # ==================== SYSTEM TEMPLATES ====================
    
    BOT_STARTED_TEMPLATE = """🟢 <b>BOT STARTED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Version:</b> {version}
<b>Mode:</b> {mode}

✅ <b>All systems operational</b>
✅ <b>MT5 connected</b>
✅ <b>Telegram connected</b>

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    BOT_STOPPED_TEMPLATE = """🔴 <b>BOT STOPPED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Reason:</b> {reason}

⏸️ <b>Trading halted</b>
⏸️ <b>All systems down</b>

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    EMERGENCY_STOP_TEMPLATE = """🚨 <b>EMERGENCY STOP</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Trigger:</b> {trigger}
<b>Reason:</b> {reason}

⚠️ <b>All trading STOPPED</b>
⚠️ <b>Manual intervention required</b>

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    MT5_DISCONNECT_TEMPLATE = """⚠️ <b>MT5 DISCONNECTED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Status:</b> Connection lost
<b>Attempt:</b> Reconnecting...

⏸️ <b>Trading paused</b>

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    MT5_RECONNECT_TEMPLATE = """✅ <b>MT5 RECONNECTED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Status:</b> Connection restored
<b>Downtime:</b> {downtime}

✅ <b>Trading resumed</b>

⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    # ==================== PLUGIN TEMPLATES (V5) ====================
    
    PLUGIN_LOADED_TEMPLATE = """🔌 <b>PLUGIN LOADED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Plugin:</b> {plugin_name}
<b>Version:</b> {version}
<b>Type:</b> {plugin_type}

✅ <b>Initialized successfully</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    PLUGIN_DISABLED_TEMPLATE = """⏸️ <b>PLUGIN DISABLED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Plugin:</b> {plugin_name}

⏸️ <b>Plugin stopped</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    PLUGIN_RELOADED_TEMPLATE = """🔄 <b>PLUGIN RELOADED</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Plugin:</b> {plugin_name}
<b>New Version:</b> {version}

✅ <b>Reload successful</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    PLUGIN_ERROR_TEMPLATE = """❌ <b>PLUGIN ERROR</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Plugin:</b> {plugin_name}
<b>Error:</b> {error_message}

⚠️ <b>Plugin may be unstable</b>
⏰ <b>Time:</b> {timestamp}
━━━━━━━━━━━━━━━━━━━━━━"""

    PLUGIN_COMPARISON_TEMPLATE = """📊 <b>PLUGIN COMPARISON</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Period:</b> {period}

<b>V3 Combined Logic:</b>
  • Trades: {v3_trades}
  • PnL: ${v3_pnl:+.2f}
  • Win Rate: {v3_winrate:.1f}%

<b>V5 Plugins Total:</b>
  • Trades: {v5_trades}
  • PnL: ${v5_pnl:+.2f}
  • Win Rate: {v5_winrate:.1f}%

<b>V6 Price Action:</b>
  • Trades: {v6_trades}
  • PnL: ${v6_pnl:+.2f}
  • Win Rate: {v6_winrate:.1f}%

━━━━━━━━━━━━━━━━━━━━━━
<b>🏆 Best Performer:</b> {best_performer}
━━━━━━━━━━━━━━━━━━━━━━"""

    # ==================== ANALYTICS TEMPLATES ====================
    
    DAILY_SUMMARY_TEMPLATE = """📊 <b>DAILY SUMMARY</b>
━━━━━━━━━━━━━━━━━━━━━━

<b>Date:</b> {date}

<b>📈 Trading Performance:</b>
  • Total Trades: {total_trades}
  • Winners: {winners} ({win_rate:.1f}%)
  • Losers: {losers}

<b>💰 Profit & Loss:</b>
  • Total PnL: ${total_pnl:+.2f}
  • Profit: +${total_profit:.2f}
  • Loss: -${total_loss:.2f}

<b>📊 Statistics:</b>
  • Best Trade: +${best_trade:.2f}
  • Worst Trade: -${worst_trade:.2f}
  • Avg Trade: ${avg_trade:+.2f}

━━━━━━━━━━━━━━━━━━━━━━
<b>🎯 Day Result:</b> {day_result}
━━━━━━━━━━━━━━━━━━━━━━"""

    # ==================== HELPER METHODS ====================
    
    @staticmethod
    def get_direction_emoji(direction: str) -> str:
        """Get emoji for trade direction"""
        return "📈" if direction.upper() == "BUY" else "📉"
    
    @staticmethod
    def get_result_emoji(pnl: float) -> str:
        """Get emoji for trade result"""
        if pnl > 0:
            return "✅"
        elif pnl < 0:
            return "❌"
        return "⚖️"
    
    @staticmethod
    def get_timeframe_emoji(timeframe: str) -> str:
        """Get emoji for timeframe"""
        tf_emojis = {
            "15M": "⏱️",
            "30M": "⏱️",
            "1H": "🕐",
            "4H": "🕓"
        }
        return tf_emojis.get(timeframe, "⏰")
    
    @staticmethod
    def get_trend_emoji(trend: str) -> str:
        """Get emoji for trend"""
        if "UP" in trend.upper() or "BULL" in trend.upper():
            return "📈"
        elif "DOWN" in trend.upper() or "BEAR" in trend.upper():
            return "📉"
        return "↔️"
    
    @staticmethod
    def format_template(template: str, data: Dict[str, Any]) -> str:
        """Format template with data, adding helper values"""
        # Add emoji helpers
        if "direction" in data:
            data["direction_emoji"] = NotificationTemplates.get_direction_emoji(data["direction"])
        
        if "pnl" in data:
            data["result_emoji"] = NotificationTemplates.get_result_emoji(data["pnl"])
            data["pnl_sign"] = "+" if data["pnl"] >= 0 else ""
        
        if "pips" in data:
            data["pips_sign"] = "+" if data["pips"] >= 0 else ""
        
        if "timeframe" in data:
            data["timeframe_emoji"] = NotificationTemplates.get_timeframe_emoji(data["timeframe"])
        
        if "new_trend" in data:
            data["new_trend_emoji"] = NotificationTemplates.get_trend_emoji(data["new_trend"])
        
        if "trend" in data:
            data["trend_emoji"] = NotificationTemplates.get_trend_emoji(data["trend"])
        
        # Format timestamp if exists
        if "timestamp" in data and isinstance(data["timestamp"], datetime):
            data["timestamp"] = data["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        
        # Add plugin badge if plugin_id exists
        if "plugin_id" in data:
            badges = {
                "v3_combined": "🔷 V3 Combined",
                "v6_price_action_15m": "🎯 V6 15M",
                "v6_price_action_30m": "🎯 V6 30M",
                "v6_price_action_1h": "🎯 V6 1H",
                "v6_price_action_4h": "🎯 V6 4H",
            }
            data["plugin_badge"] = f"<b>Plugin:</b> {badges.get(data['plugin_id'], data['plugin_id'])}"
        else:
            data["plugin_badge"] = ""
        
        try:
            return template.format(**data)
        except KeyError as e:
            # Missing key, return template with error note
            return f"{template}\n\n⚠️ <i>Missing data: {e}</i>"


# Export templates instance
templates = NotificationTemplates()


# ==================== ADDITIONAL HELPER FUNCTIONS ====================

def format_price(price: float, symbol: str = "XAUUSD") -> str:
    """Format price with appropriate decimals"""
    if symbol in ["XAUUSD", "XAGUSD"]:
        return f"${price:,.2f}"
    return f"{price:.5f}"


def format_duration(seconds: int) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    elif seconds < 86400:
        hours = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hours}h {mins}m"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        return f"{days}d {hours}h"


def format_percentage(value: float) -> str:
    """Format percentage with sign"""
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def create_table_row(items: list, widths: list) -> str:
    """Create formatted table row"""
    row = ""
    for item, width in zip(items, widths):
        row += f"{str(item):<{width}} "
    return row.strip()


def build_persistent_reply_keyboard() -> dict:
    """Build always-visible bottom keyboard"""
    keyboard = [
        [
            {"text": "📊 Status"},
            {"text": "📈 Positions"},
            {"text": "💰 PnL"}
        ],
        [
            {"text": "⏸️ Pause"},
            {"text": "▶️ Resume"},
            {"text": "🔄 Refresh"}
        ],
        [
            {"text": "📱 Menu"},
            {"text": "🆘 Help"}
        ]
    ]
    
    return {
        "keyboard": keyboard,
        "resize_keyboard": True,
        "is_persistent": True,
        "input_field_placeholder": "Tap a button or type..."
    }


def build_confirmation_keyboard(action: str, action_label: str = "Proceed") -> dict:
    """Build confirmation inline keyboard"""
    keyboard = [
        [{"text": f"─── ⚠️ Confirm {action_label}? ───", "callback_data": "noop"}],
        [
            {"text": f"✅ Yes, {action_label}", "callback_data": f"confirm_{action}"},
            {"text": "❌ Cancel", "callback_data": "cancel"}
        ]
    ]
    return {"inline_keyboard": keyboard}
