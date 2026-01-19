# TELEGRAM NOTIFICATIONS REFERENCE - 78 Notification Types

**Version:** 5.2.0  
**Generated:** 2026-01-19  
**Source File:** `src/telegram/notification_router.py` (1,695 lines)

This document provides a complete reference for all 78 notification types available in the Trading Bot V5.

## Notification Categories Overview

| Category | Count | Description |
|----------|-------|-------------|
| Trade Events | 7 | Entry, exit, TP/SL hit |
| System Events | 6 | Bot status, MT5 connection |
| Plugin Events | 3 | Plugin loading and errors |
| Alert Events | 4 | Alert processing status |
| Analytics Events | 4 | Reports and summaries |
| Generic Events | 3 | Info, warning, error |
| V6 Price Action | 12 | V6-specific notifications |
| V3 Combined | 5 | V3-specific notifications |
| Autonomous System | 5 | Safety and recovery |
| Re-entry System | 5 | Recovery operations |
| Signal Events | 4 | Signal processing |
| Trade Events (Extended) | 3 | Partial close, manual exit |
| System Events (Extended) | 6 | Connection, limits, errors |
| Session Events | 4 | Session management |
| Voice Alert Events | 5 | Voice notifications |
| Dashboard Events | 2 | Dashboard updates |
| **Total** | **78** | |

## Notification Priority Levels

```python
class NotificationPriority(Enum):
    CRITICAL = 5  # Emergency stop, daily loss limit, MT5 disconnect
    HIGH = 4      # Trade entry/exit, SL/TP hit
    MEDIUM = 3    # Partial profit, SL modification
    LOW = 2       # Daily summary, config reload
    INFO = 1      # Bot started, plugin loaded
```

## Target Bot Routing

```python
class TargetBot(Enum):
    CONTROLLER = "controller"    # System commands, admin
    NOTIFICATION = "notification" # Trade alerts
    ANALYTICS = "analytics"      # Reports, summaries
    ALL = "all"                  # Broadcast to all bots
```

## 1. Trade Events (7)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `ENTRY` | HIGH | Notification | Yes | Trade entry notification |
| `EXIT` | HIGH | Notification | Yes | Trade exit notification |
| `TP_HIT` | HIGH | Notification | Yes | Take profit hit |
| `SL_HIT` | HIGH | Notification | Yes | Stop loss hit |
| `PROFIT_BOOKING` | MEDIUM | Notification | No | Profit booking executed |
| `SL_MODIFIED` | MEDIUM | Notification | No | Stop loss modified |
| `BREAKEVEN` | MEDIUM | Notification | No | Breakeven set |

## 2. System Events (6)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `BOT_STARTED` | INFO | Controller | No | Bot started |
| `BOT_STOPPED` | CRITICAL | All | Yes | Bot stopped |
| `EMERGENCY_STOP` | CRITICAL | All | Yes | Emergency stop triggered |
| `MT5_DISCONNECT` | CRITICAL | All | Yes | MT5 disconnected |
| `MT5_RECONNECT` | HIGH | Notification | No | MT5 reconnected |
| `DAILY_LOSS_LIMIT` | CRITICAL | All | Yes | Daily loss limit reached |

## 3. Plugin Events (3)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `PLUGIN_LOADED` | INFO | Controller | No | Plugin loaded |
| `PLUGIN_ERROR` | HIGH | Notification | No | Plugin error |
| `CONFIG_RELOAD` | LOW | Analytics | No | Config reloaded |

## 4. Alert Events (4)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `ALERT_RECEIVED` | INFO | Controller | No | Alert received |
| `ALERT_PROCESSED` | MEDIUM | Notification | No | Alert processed |
| `ALERT_IGNORED` | LOW | Analytics | No | Alert ignored |
| `ALERT_ERROR` | HIGH | Notification | No | Alert processing error |

## 5. Analytics Events (4)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `DAILY_SUMMARY` | LOW | Analytics | No | Daily summary report |
| `WEEKLY_SUMMARY` | LOW | Analytics | No | Weekly summary report |
| `PERFORMANCE_REPORT` | LOW | Analytics | No | Performance report |
| `RISK_ALERT` | HIGH | Notification | Yes | Risk alert |

## 6. Generic Events (3)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `INFO` | INFO | Controller | No | General info |
| `WARNING` | MEDIUM | Notification | No | Warning message |
| `ERROR` | HIGH | Notification | No | Error message |

## 7. V6 Price Action Events (12)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `V6_ENTRY_15M` | HIGH | Notification | Yes | V6 15M entry |
| `V6_ENTRY_30M` | HIGH | Notification | Yes | V6 30M entry |
| `V6_ENTRY_1H` | HIGH | Notification | Yes | V6 1H entry |
| `V6_ENTRY_4H` | HIGH | Notification | Yes | V6 4H entry |
| `V6_EXIT` | HIGH | Notification | Yes | V6 exit |
| `V6_TP_HIT` | HIGH | Notification | Yes | V6 TP hit |
| `V6_SL_HIT` | HIGH | Notification | Yes | V6 SL hit |
| `V6_TIMEFRAME_ENABLED` | MEDIUM | Controller | No | V6 timeframe enabled |
| `V6_TIMEFRAME_DISABLED` | MEDIUM | Controller | No | V6 timeframe disabled |
| `V6_DAILY_SUMMARY` | LOW | Analytics | No | V6 daily summary |
| `V6_SIGNAL` | HIGH | Notification | No | V6 signal received |
| `V6_BREAKEVEN` | MEDIUM | Notification | No | V6 breakeven set |

## 8. V3 Combined Events (5)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `V3_ENTRY` | HIGH | Notification | Yes | V3 entry |
| `V3_EXIT` | HIGH | Notification | Yes | V3 exit |
| `V3_TP_HIT` | HIGH | Notification | Yes | V3 TP hit |
| `V3_SL_HIT` | HIGH | Notification | Yes | V3 SL hit |
| `V3_LOGIC_TOGGLED` | MEDIUM | Controller | No | V3 logic toggled |

## 9. Autonomous System Events (5)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `TP_CONTINUATION` | HIGH | Notification | Yes | TP continuation started |
| `SL_HUNT_ACTIVATED` | HIGH | Notification | Yes | SL Hunt activated |
| `RECOVERY_SUCCESS` | HIGH | Notification | Yes | Recovery successful |
| `RECOVERY_FAILED` | HIGH | Notification | Yes | Recovery failed |
| `PROFIT_ORDER_PROTECTION` | MEDIUM | Notification | No | Profit order protected |

## 10. Re-entry System Events (5)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `TP_REENTRY_STARTED` | MEDIUM | Notification | No | TP re-entry started |
| `TP_REENTRY_EXECUTED` | HIGH | Notification | Yes | TP re-entry executed |
| `TP_REENTRY_COMPLETED` | MEDIUM | Notification | No | TP re-entry completed |
| `SL_HUNT_RECOVERY` | HIGH | Notification | Yes | SL Hunt recovery |
| `EXIT_CONTINUATION` | HIGH | Notification | Yes | Exit continuation |

## 11. Signal Events (4)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `SIGNAL_RECEIVED` | HIGH | Notification | No | Signal received |
| `SIGNAL_IGNORED` | INFO | Analytics | No | Signal ignored |
| `SIGNAL_FILTERED` | INFO | Analytics | No | Signal filtered |
| `TREND_CHANGED` | HIGH | Notification | No | Trend changed |

## 12. Trade Events Extended (3)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `PARTIAL_CLOSE` | MEDIUM | Notification | No | Partial close executed |
| `MANUAL_EXIT` | HIGH | Notification | Yes | Manual exit |
| `REVERSAL_EXIT` | HIGH | Notification | Yes | Reversal exit |

## 13. System Events Extended (6)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `MT5_CONNECTED` | HIGH | Controller | No | MT5 connected |
| `LIFETIME_LOSS_LIMIT` | CRITICAL | All | Yes | Lifetime loss limit |
| `DAILY_LOSS_WARNING` | HIGH | Notification | Yes | Daily loss warning |
| `CONFIG_ERROR` | HIGH | Controller | No | Config error |
| `DATABASE_ERROR` | HIGH | Controller | No | Database error |
| `ORDER_FAILED` | HIGH | Notification | Yes | Order failed |

## 14. Session Events (4)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `SESSION_TOGGLE` | MEDIUM | Controller | No | Session toggled |
| `SYMBOL_TOGGLE` | MEDIUM | Controller | No | Symbol toggled |
| `TIME_ADJUSTMENT` | MEDIUM | Controller | No | Time adjusted |
| `FORCE_CLOSE_TOGGLE` | MEDIUM | Controller | No | Force close toggled |

## 15. Voice Alert Events (5)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `VOICE_TRADE_ENTRY` | HIGH | Notification | Yes | Voice trade entry |
| `VOICE_TP_HIT` | HIGH | Notification | Yes | Voice TP hit |
| `VOICE_SL_HIT` | CRITICAL | Notification | Yes | Voice SL hit |
| `VOICE_RISK_LIMIT` | CRITICAL | All | Yes | Voice risk limit |
| `VOICE_RECOVERY` | MEDIUM | Notification | Yes | Voice recovery |

## 16. Dashboard Events (2)

| Type | Priority | Target | Voice | Description |
|------|----------|--------|-------|-------------|
| `DASHBOARD_UPDATE` | LOW | Controller | No | Dashboard update |
| `AUTONOMOUS_DASHBOARD` | LOW | Controller | No | Autonomous dashboard |

## NotificationFormatter Class

The `NotificationFormatter` class provides 40+ formatter methods for creating formatted notification messages:

```python
class NotificationFormatter:
    @staticmethod
    def format_entry(data: Dict) -> str:
        """Format trade entry notification"""
        return (
            f"<b>TRADE ENTRY</b>\n"
            f"Symbol: {data.get('symbol', 'N/A')}\n"
            f"Direction: {data.get('direction', 'N/A')}\n"
            f"Price: {data.get('price', 'N/A')}\n"
            f"Lot: {data.get('lot_size', 'N/A')}\n"
            f"SL: {data.get('sl', 'N/A')}\n"
            f"TP: {data.get('tp', 'N/A')}"
        )
    
    @staticmethod
    def format_tp_hit(data: Dict) -> str:
        """Format TP hit notification"""
        return (
            f"<b>TP HIT</b>\n"
            f"Symbol: {data.get('symbol', 'N/A')}\n"
            f"Profit: ${data.get('profit', 0):.2f}\n"
            f"Pips: {data.get('pips', 0):.1f}"
        )
    
    @staticmethod
    def format_sl_hit(data: Dict) -> str:
        """Format SL hit notification"""
        return (
            f"<b>SL HIT</b>\n"
            f"Symbol: {data.get('symbol', 'N/A')}\n"
            f"Loss: ${data.get('loss', 0):.2f}\n"
            f"Pips: {data.get('pips', 0):.1f}"
        )
    # ... 40+ more formatters
```

## NotificationRouter Class

The `NotificationRouter` handles smart routing of notifications:

```python
class NotificationRouter:
    def __init__(
        self,
        controller_callback: Optional[Callable] = None,
        notification_callback: Optional[Callable] = None,
        analytics_callback: Optional[Callable] = None,
        voice_callback: Optional[Callable] = None
    ):
        self.routing_rules = DEFAULT_ROUTING_RULES.copy()
        self.muted_types: Set[NotificationType] = set()
        self.voice_muted = False
    
    def send(self, notification: Notification) -> bool:
        """Send notification to appropriate bot(s)"""
        if self.is_muted(notification.notification_type):
            return False
        
        rule = self.routing_rules.get(notification.notification_type)
        target = rule.get("target", TargetBot.NOTIFICATION)
        
        # Route to target bot(s)
        if target == TargetBot.ALL:
            self._send_to_all(notification)
        else:
            self._send_to_target(target, notification)
        
        # Trigger voice alert if enabled
        if rule.get("voice") and notification.voice_enabled:
            self._trigger_voice(notification)
        
        return True
```

## Mute/Unmute Functionality

Users can mute specific notification types:

```python
# Mute a notification type
router.mute(NotificationType.ALERT_IGNORED)

# Unmute a notification type
router.unmute(NotificationType.ALERT_IGNORED)

# Mute all notifications
router.mute_all()

# Unmute all notifications
router.unmute_all()

# Mute voice alerts only
router.mute_voice()
```

## Related Documentation

- [30_TELEGRAM_3BOT_SYSTEM.md](./30_TELEGRAM_3BOT_SYSTEM.md) - 3-bot architecture
- [31_TELEGRAM_COMMANDS.md](./31_TELEGRAM_COMMANDS.md) - 105 commands
- [SOURCE_CODE_AUDIT.md](../SOURCE_CODE_AUDIT.md) - Complete source code audit

---

*Last Updated: 2026-01-19*
