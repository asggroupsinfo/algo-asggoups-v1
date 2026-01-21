"""
V6 Notification Templates
Centralized notification formatting for V6 Price Action plugins
"""

from typing import Dict, Any, Optional
from datetime import datetime


def create_progress_bar(current: int, total: int, length: int = 10, filled_char: str = "█", empty_char: str = "░") -> str:
    """
    Create visual progress bar
    
    Args:
        current: Current progress value
        total: Total/max value
        length: Bar length in characters
        filled_char: Character for filled portion
        empty_char: Character for empty portion
    
    Returns:
        Progress bar string
    
    Example:
        >>> create_progress_bar(7, 10)
        '███████░░░ 70%'
    """
    if total == 0:
        return f"{empty_char * length} 0%"
    
    percentage = min(100, int((current / total) * 100))
    filled_length = int((current / total) * length)
    empty_length = length - filled_length
    
    bar = filled_char * filled_length + empty_char * empty_length
    return f"{bar} {percentage}%"


def format_pnl(pnl: float, show_icon: bool = True) -> str:
    """
    Format P&L with color and icon
    
    Args:
        pnl: Profit/Loss value
        show_icon: Whether to include emoji icon
    
    Returns:
        Formatted P&L string
    """
    if pnl > 0:
        icon = "🟢" if show_icon else ""
        return f"{icon} +${abs(pnl):.2f}"
    elif pnl < 0:
        icon = "🔴" if show_icon else ""
        return f"{icon} -${abs(pnl):.2f}"
    else:
        icon = "⚪" if show_icon else ""
        return f"{icon} $0.00"


def format_win_rate(wins: int, total: int) -> str:
    """
    Format win rate with percentage and emoji
    
    Args:
        wins: Number of wins
        total: Total trades
    
    Returns:
        Formatted win rate string
    """
    if total == 0:
        return "N/A"
    
    rate = (wins / total) * 100
    
    if rate >= 70:
        emoji = "🟢"
    elif rate >= 50:
        emoji = "🟡"
    else:
        emoji = "🔴"
    
    return f"{emoji} {rate:.1f}% ({wins}/{total})"


def format_timeframe_badge(timeframe: str) -> str:
    """
    Get emoji badge for timeframe
    
    Args:
        timeframe: Timeframe string (1m, 5m, 15m, 1h, etc.)
    
    Returns:
        Emoji badge
    """
    badges = {
        "1m": "⚡",
        "5m": "⏱️",
        "15m": "⏱️",
        "30m": "🕐",
        "1h": "🕐",
        "4h": "🕓",
        "1d": "📅"
    }
    return badges.get(timeframe.lower(), "🔶")


def format_v6_entry_notification(trade_data: Dict[str, Any]) -> str:
    """
    Format V6 entry notification
    
    Args:
        trade_data: Trade entry data
    
    Returns:
        Formatted notification message
    """
    timeframe = trade_data.get("timeframe", "Unknown")
    symbol = trade_data.get("symbol", "UNKNOWN")
    direction = trade_data.get("direction", "UNKNOWN")
    entry_price = trade_data.get("entry_price", 0)
    sl = trade_data.get("sl", 0)
    tp = trade_data.get("tp", 0)
    lot = trade_data.get("lot_size", 0)
    ticket = trade_data.get("ticket", "N/A")
    
    badge = format_timeframe_badge(timeframe)
    direction_emoji = "🟢" if direction.upper() == "BUY" else "🔴"
    
    message = (
        f"{badge} <b>V6 {timeframe.upper()} ENTRY</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{direction_emoji} <b>{direction.upper()}</b> {symbol}\n"
        f"<b>Entry:</b> {entry_price:.5f}\n"
        f"<b>SL:</b> {sl:.5f}\n"
        f"<b>TP:</b> {tp:.5f}\n"
        f"<b>Lot:</b> {lot:.2f}\n"
        f"<b>Ticket:</b> #{ticket}\n\n"
        f"<b>Status:</b> Order placed ✅"
    )
    
    return message


def format_v6_exit_notification(trade_data: Dict[str, Any], result: Dict[str, Any]) -> str:
    """
    Format V6 exit notification
    
    Args:
        trade_data: Trade entry data
        result: Trade result data
    
    Returns:
        Formatted notification message
    """
    timeframe = trade_data.get("timeframe", "Unknown")
    symbol = trade_data.get("symbol", "UNKNOWN")
    direction = trade_data.get("direction", "UNKNOWN")
    entry_price = trade_data.get("entry_price", 0)
    exit_price = result.get("exit_price", 0)
    pnl = result.get("profit", 0)
    ticket = trade_data.get("ticket", "N/A")
    exit_reason = result.get("reason", "Manual Close")
    duration = result.get("duration_minutes", 0)
    
    badge = format_timeframe_badge(timeframe)
    direction_emoji = "🟢" if direction.upper() == "BUY" else "🔴"
    pnl_formatted = format_pnl(pnl)
    
    # Reason emoji
    reason_emoji = {
        "TP Hit": "🎯",
        "SL Hit": "🛑",
        "Manual Close": "✋",
        "Trailing Stop": "📉",
        "Time Exit": "⏰"
    }.get(exit_reason, "📊")
    
    message = (
        f"{badge} <b>V6 {timeframe.upper()} EXIT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{direction_emoji} <b>{direction.upper()}</b> {symbol}\n"
        f"<b>Entry:</b> {entry_price:.5f}\n"
        f"<b>Exit:</b> {exit_price:.5f}\n"
        f"<b>Result:</b> {pnl_formatted}\n"
        f"<b>Ticket:</b> #{ticket}\n"
        f"<b>Duration:</b> {duration} min\n\n"
        f"{reason_emoji} <b>Reason:</b> {exit_reason}"
    )
    
    return message


def format_v6_signal_notification(signal_data: Dict[str, Any]) -> str:
    """
    Format V6 signal notification
    
    Args:
        signal_data: Signal data from TradingView
    
    Returns:
        Formatted notification message
    """
    timeframe = signal_data.get("timeframe", "Unknown")
    symbol = signal_data.get("symbol", "UNKNOWN")
    direction = signal_data.get("direction", "UNKNOWN")
    confidence = signal_data.get("confidence", 0)
    
    badge = format_timeframe_badge(timeframe)
    direction_emoji = "🟢" if direction.upper() == "BUY" else "🔴"
    
    # Confidence bar
    confidence_bar = create_progress_bar(confidence, 100, length=10)
    
    message = (
        f"{badge} <b>V6 {timeframe.upper()} SIGNAL</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{direction_emoji} <b>{direction.upper()}</b> {symbol}\n"
        f"<b>Confidence:</b> {confidence_bar}\n\n"
        f"<b>💡 Tip:</b> Signal received, waiting for entry conditions"
    )
    
    return message


def format_v6_toggle_notification(timeframe: str, enabled: bool) -> str:
    """
    Format V6 timeframe toggle notification
    
    Args:
        timeframe: Timeframe that was toggled
        enabled: New state (True = enabled, False = disabled)
    
    Returns:
        Formatted notification message
    """
    badge = format_timeframe_badge(timeframe)
    status_emoji = "✅" if enabled else "❌"
    status_text = "ENABLED" if enabled else "DISABLED"
    
    message = (
        f"{badge} <b>V6 {timeframe.upper()} TOGGLED</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>Status:</b> {status_text} {status_emoji}\n\n"
        f"<b>💡 Tip:</b> Plugin {'will now process signals' if enabled else 'is now paused'}"
    )
    
    return message


def format_v6_tp_hit_notification(trade_data: Dict[str, Any], level: int, partial_pnl: float) -> str:
    """
    Format V6 TP level hit notification
    
    Args:
        trade_data: Trade data
        level: TP level hit (1, 2, 3, etc.)
        partial_pnl: Profit from this level
    
    Returns:
        Formatted notification message
    """
    timeframe = trade_data.get("timeframe", "Unknown")
    symbol = trade_data.get("symbol", "UNKNOWN")
    ticket = trade_data.get("ticket", "N/A")
    
    badge = format_timeframe_badge(timeframe)
    pnl_formatted = format_pnl(partial_pnl)
    
    message = (
        f"{badge} <b>V6 {timeframe.upper()} TP HIT</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🎯 <b>TP Level {level}</b>\n"
        f"<b>Symbol:</b> {symbol}\n"
        f"<b>Ticket:</b> #{ticket}\n"
        f"<b>Partial Profit:</b> {pnl_formatted}\n\n"
        f"<b>Status:</b> Position partially closed ✅"
    )
    
    return message


def format_v6_sl_adjusted_notification(trade_data: Dict[str, Any], old_sl: float, new_sl: float) -> str:
    """
    Format V6 SL adjustment notification
    
    Args:
        trade_data: Trade data
        old_sl: Previous SL value
        new_sl: New SL value
    
    Returns:
        Formatted notification message
    """
    timeframe = trade_data.get("timeframe", "Unknown")
    symbol = trade_data.get("symbol", "UNKNOWN")
    ticket = trade_data.get("ticket", "N/A")
    
    badge = format_timeframe_badge(timeframe)
    
    message = (
        f"{badge} <b>V6 {timeframe.upper()} SL ADJUSTED</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🛡️ <b>Trailing Stop Updated</b>\n"
        f"<b>Symbol:</b> {symbol}\n"
        f"<b>Ticket:</b> #{ticket}\n"
        f"<b>Old SL:</b> {old_sl:.5f}\n"
        f"<b>New SL:</b> {new_sl:.5f}\n\n"
        f"<b>Status:</b> Protection updated ✅"
    )
    
    return message


def create_inline_keyboard(buttons: list) -> Dict:
    """
    Create inline keyboard for notifications
    
    Args:
        buttons: List of button rows, each row is a list of dicts with 'text' and 'callback_data'
    
    Returns:
        Inline keyboard markup dict
    
    Example:
        buttons = [
            [{"text": "✅ Close", "callback_data": "close_trade_12345"}],
            [{"text": "📊 Info", "callback_data": "trade_info_12345"}]
        ]
    """
    return {"inline_keyboard": buttons}


def create_v6_trade_actions_keyboard(ticket: str) -> Dict:
    """
    Create standard action buttons for V6 trade notifications
    
    Args:
        ticket: Trade ticket number
    
    Returns:
        Inline keyboard with standard actions
    """
    buttons = [
        [
            {"text": "📊 Trade Info", "callback_data": f"v6_info_{ticket}"},
            {"text": "✅ Close Now", "callback_data": f"v6_close_{ticket}"}
        ],
        [
            {"text": "🛡️ Move to BE", "callback_data": f"v6_be_{ticket}"},
            {"text": "📉 Trail SL", "callback_data": f"v6_trail_{ticket}"}
        ]
    ]
    return create_inline_keyboard(buttons)


# Quick access helpers
def v6_entry(trade_data: Dict[str, Any]) -> str:
    """Shortcut for entry notification"""
    return format_v6_entry_notification(trade_data)


def v6_exit(trade_data: Dict[str, Any], result: Dict[str, Any]) -> str:
    """Shortcut for exit notification"""
    return format_v6_exit_notification(trade_data, result)


def v6_signal(signal_data: Dict[str, Any]) -> str:
    """Shortcut for signal notification"""
    return format_v6_signal_notification(signal_data)


def v6_toggle(timeframe: str, enabled: bool) -> str:
    """Shortcut for toggle notification"""
    return format_v6_toggle_notification(timeframe, enabled)


# Test/Example
if __name__ == "__main__":
    # Test progress bar
    print("Progress Bar Tests:")
    print(create_progress_bar(0, 10))
    print(create_progress_bar(3, 10))
    print(create_progress_bar(7, 10))
    print(create_progress_bar(10, 10))
    
    # Test PNL formatting
    print("\nP&L Tests:")
    print(format_pnl(45.50))
    print(format_pnl(-23.75))
    print(format_pnl(0))
    
    # Test win rate
    print("\nWin Rate Tests:")
    print(format_win_rate(8, 10))
    print(format_win_rate(5, 10))
    print(format_win_rate(3, 10))
    
    # Test entry notification
    print("\nEntry Notification Test:")
    test_trade = {
        "timeframe": "1m",
        "symbol": "XAUUSD",
        "direction": "BUY",
        "entry_price": 2050.50,
        "sl": 2048.00,
        "tp": 2055.00,
        "lot_size": 0.05,
        "ticket": "12345"
    }
    print(v6_entry(test_trade))
