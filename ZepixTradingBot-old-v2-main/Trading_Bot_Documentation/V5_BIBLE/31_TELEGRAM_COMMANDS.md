# TELEGRAM COMMANDS REFERENCE - 105 Commands

**Version:** 5.2.0  
**Generated:** 2026-01-19  
**Source File:** `src/telegram/controller_bot.py` (1,801 lines)

This document provides a complete reference for all 105 Telegram commands available in the Trading Bot V5.

## Command Categories Overview

| Category | Count | Description |
|----------|-------|-------------|
| System | 10 | Bot control and status |
| Trading | 15 | Trade execution and monitoring |
| Risk | 12 | Risk management settings |
| Strategy | 20 | Trading strategy configuration |
| Timeframe | 8 | Timeframe settings |
| Re-entry | 8 | Re-entry system control |
| Profit | 6 | Profit booking settings |
| Analytics | 8 | Reports and statistics |
| Session | 6 | Session management |
| Plugin | 6 | Plugin control |
| Notification | 6 | Notification preferences |
| **Total** | **105** | |

## 1. System Commands (10)

| Command | Description | Handler |
|---------|-------------|---------|
| `/start` | Initialize bot and show main menu | `handle_start` |
| `/status` | Show current bot status and statistics | `handle_status` |
| `/pause` | Pause all trading operations | `handle_pause` |
| `/resume` | Resume trading operations | `handle_resume` |
| `/help` | Show help menu with all commands | `handle_help` |
| `/health` | Show plugin health dashboard | `handle_health_command` |
| `/version` | Show active plugin versions | `handle_version_command` |
| `/restart` | Restart the bot | `handle_restart` |
| `/shutdown` | Shutdown the bot | `handle_shutdown` |
| `/config` | Show/edit configuration | `handle_config` |

## 2. Trading Commands (15)

| Command | Description | Handler |
|---------|-------------|---------|
| `/trade` | Open trading menu | `handle_trade_menu` |
| `/buy` | Place a buy order | `handle_buy` |
| `/sell` | Place a sell order | `handle_sell` |
| `/close` | Close a specific position | `handle_close` |
| `/closeall` | Close all open positions | `handle_close_all` |
| `/positions` | Show all open positions | `handle_positions` |
| `/orders` | Show pending orders | `handle_orders` |
| `/history` | Show trade history | `handle_history` |
| `/pnl` | Show profit/loss summary | `handle_pnl` |
| `/balance` | Show account balance | `handle_balance` |
| `/equity` | Show account equity | `handle_equity` |
| `/margin` | Show margin information | `handle_margin` |
| `/symbols` | Show available symbols | `handle_symbols` |
| `/price` | Get current price for symbol | `handle_price` |
| `/spread` | Get current spread for symbol | `handle_spread` |

## 3. Risk Commands (12)

| Command | Description | Handler |
|---------|-------------|---------|
| `/risk` | Open risk management menu | `handle_risk_menu` |
| `/setlot` | Set lot size | `handle_set_lot` |
| `/setsl` | Set stop loss pips | `handle_set_sl` |
| `/settp` | Set take profit pips | `handle_set_tp` |
| `/dailylimit` | Set daily loss limit | `handle_daily_limit` |
| `/maxloss` | Set maximum loss per trade | `handle_max_loss` |
| `/maxprofit` | Set maximum profit target | `handle_max_profit` |
| `/risktier` | Set risk tier (1-5) | `handle_risk_tier` |
| `/slsystem` | Configure SL system | `handle_sl_system` |
| `/trailsl` | Configure trailing SL | `handle_trail_sl` |
| `/breakeven` | Configure breakeven settings | `handle_breakeven` |
| `/protection` | Configure profit protection | `handle_protection` |

## 4. Strategy Commands (20)

| Command | Description | Handler |
|---------|-------------|---------|
| `/strategy` | Open strategy menu | `handle_strategy_menu` |
| `/logic1` | Toggle Logic 1 | `handle_logic1` |
| `/logic2` | Toggle Logic 2 | `handle_logic2` |
| `/logic3` | Toggle Logic 3 | `handle_logic3` |
| `/v3` | V3 Combined Logic settings | `handle_v3` |
| `/v6` | V6 Price Action settings | `handle_v6` |
| `/v6_status` | Show V6 plugin status | `handle_v6_status` |
| `/v6_control` | Open V6 control menu | `handle_v6_control` |
| `/tf15m_on` | Enable V6 15M timeframe | `handle_v6_tf15m_on` |
| `/tf15m_off` | Disable V6 15M timeframe | `handle_v6_tf15m_off` |
| `/tf30m_on` | Enable V6 30M timeframe | `handle_v6_tf30m_on` |
| `/tf30m_off` | Disable V6 30M timeframe | `handle_v6_tf30m_off` |
| `/tf1h_on` | Enable V6 1H timeframe | `handle_v6_tf1h_on` |
| `/tf1h_off` | Disable V6 1H timeframe | `handle_v6_tf1h_off` |
| `/tf4h_on` | Enable V6 4H timeframe | `handle_v6_tf4h_on` |
| `/tf4h_off` | Disable V6 4H timeframe | `handle_v6_tf4h_off` |
| `/signals` | Configure signal settings | `handle_signals` |
| `/filters` | Configure signal filters | `handle_filters` |
| `/multiplier` | Set lot multiplier | `handle_multiplier` |
| `/mode` | Set trading mode | `handle_mode` |

## 5. Timeframe Commands (8)

| Command | Description | Handler |
|---------|-------------|---------|
| `/timeframe` | Open timeframe menu | `handle_timeframe_menu` |
| `/tf1m` | Set 1-minute timeframe | `handle_tf_1m` |
| `/tf5m` | Set 5-minute timeframe | `handle_tf_5m` |
| `/tf15m` | Set 15-minute timeframe | `handle_tf_15m` |
| `/tf1h` | Set 1-hour timeframe | `handle_tf_1h` |
| `/tf4h` | Set 4-hour timeframe | `handle_tf_4h` |
| `/tf1d` | Set daily timeframe | `handle_tf_1d` |
| `/trends` | Show current trend analysis | `handle_trends` |

## 6. Re-entry Commands (8)

| Command | Description | Handler |
|---------|-------------|---------|
| `/reentry` | Open re-entry menu | `handle_reentry_menu` |
| `/slhunt` | Configure SL Hunt recovery | `handle_sl_hunt` |
| `/tpcontinue` | Configure TP Continuation | `handle_tp_continue` |
| `/recovery` | Show recovery status | `handle_recovery` |
| `/cooldown` | Set recovery cooldown | `handle_cooldown` |
| `/chains` | Show active re-entry chains | `handle_chains` |
| `/autonomous` | Configure autonomous system | `handle_autonomous` |
| `/chain_limit` | Set maximum chain level | `handle_chain_limit` |

## 7. Profit Commands (6)

| Command | Description | Handler |
|---------|-------------|---------|
| `/profit` | Open profit booking menu | `handle_profit_menu` |
| `/booking` | Configure profit booking | `handle_booking` |
| `/levels` | Show pyramid levels | `handle_levels` |
| `/partial` | Configure partial close | `handle_partial` |
| `/order_b` | Configure Order B settings | `handle_order_b` |
| `/pyramid` | Configure pyramid compounding | `handle_pyramid` |

## 8. Analytics Commands (8)

| Command | Description | Handler |
|---------|-------------|---------|
| `/analytics` | Open analytics menu | `handle_analytics_menu` |
| `/report` | Generate performance report | `handle_report` |
| `/daily` | Show daily summary | `handle_daily` |
| `/weekly` | Show weekly summary | `handle_weekly` |
| `/performance` | Show performance metrics | `handle_performance` |
| `/stats` | Show trading statistics | `handle_stats` |
| `/export` | Export trade data | `handle_export` |
| `/compare` | Compare performance periods | `handle_compare` |

## 9. Session Commands (6)

| Command | Description | Handler |
|---------|-------------|---------|
| `/session` | Open session menu | `handle_session_menu` |
| `/toggle` | Toggle trading session | `handle_toggle` |
| `/force_close` | Force close at session end | `handle_force_close` |
| `/time_adjust` | Adjust session times | `handle_time_adjust` |
| `/symbol_filter` | Configure symbol filters | `handle_symbol_filter` |
| `/session_status` | Show session status | `handle_session_status` |

## 10. Plugin Commands (6)

| Command | Description | Handler |
|---------|-------------|---------|
| `/plugins` | Show all plugins | `handle_plugins` |
| `/enable` | Enable a plugin | `handle_enable` |
| `/disable` | Disable a plugin | `handle_disable` |
| `/shadow` | Toggle shadow mode | `handle_shadow` |
| `/upgrade` | Upgrade plugin version | `handle_upgrade_command` |
| `/rollback` | Rollback plugin version | `handle_rollback_command` |

## 11. Notification Commands (6)

| Command | Description | Handler |
|---------|-------------|---------|
| `/notifications` | Open notification menu | `handle_notifications_menu` |
| `/mute` | Mute notification type | `handle_mute` |
| `/unmute` | Unmute notification type | `handle_unmute` |
| `/voice` | Configure voice alerts | `handle_voice` |
| `/preferences` | Set notification preferences | `handle_preferences` |
| `/alerts` | Show alert settings | `handle_alerts` |

## Command Handler Implementation

All command handlers are wired in the `_wire_default_handlers()` method of `ControllerBot`:

```python
# src/telegram/controller_bot.py:411-540
def _wire_default_handlers(self):
    """Wire ALL 105 command handlers to CommandRegistry"""
    # System Commands (10)
    self._command_handlers["/start"] = self.handle_start
    self._command_handlers["/status"] = self.handle_status
    # ... (all 105 commands wired)
```

## Menu Integration

Commands that open menus integrate with the `MenuManager`:

```python
# src/menu/menu_manager.py
class MenuManager:
    def __init__(self, bot):
        self.bot = bot
        self.handlers = {
            'main': MainMenuHandler,
            'risk': RiskMenuHandler,
            'strategy': StrategyMenuHandler,
            # ... 15 menu handlers
        }
```

## Command Response Format

All commands return formatted responses using HTML:

```python
def send_status_response(self, status_data: Dict) -> Optional[int]:
    message = (
        f"<b>BOT STATUS</b>\n"
        f"Status: {bot_status}\n"
        f"Uptime: {status_data.get('uptime', 'N/A')}\n"
        f"Active Plugins: {status_data.get('active_plugins', 0)}\n"
        f"Open Trades: {status_data.get('open_trades', 0)}\n"
        f"Today's P&L: ${status_data.get('daily_pnl', 0):.2f}\n"
    )
    return self.send_message(message)
```

## Related Documentation

- [30_TELEGRAM_3BOT_SYSTEM.md](./30_TELEGRAM_3BOT_SYSTEM.md) - 3-bot architecture
- [32_TELEGRAM_NOTIFICATIONS.md](./32_TELEGRAM_NOTIFICATIONS.md) - 78 notification types
- [SOURCE_CODE_AUDIT.md](../SOURCE_CODE_AUDIT.md) - Complete source code audit

---

*Last Updated: 2026-01-19*
