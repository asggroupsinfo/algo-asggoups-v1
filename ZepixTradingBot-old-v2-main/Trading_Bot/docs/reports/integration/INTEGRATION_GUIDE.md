# Quick Integration Guide
## Error Handling System → Main Bot

### 🚀 STEP 1: Update main.py (or bot startup file)

Add these imports at the top:
```python
from src.utils.logging_config import setup_error_logging
from src.utils.auto_recovery import initialize_auto_recovery
from src.utils.admin_notifier import initialize_admin_notifier
```

Add initialization code (after creating MT5/DB/Telegram instances):
```python
# Setup enhanced error logging
setup_error_logging()

# Initialize auto-recovery system
auto_recovery = initialize_auto_recovery(
    mt5_client=mt5_client,        # Your MT5 client instance
    database=database,              # Your database instance
    telegram_bot=controller_bot     # Your Telegram bot instance
)

# Initialize admin notifier (replace with your admin chat ID)
admin_notifier = initialize_admin_notifier(
    telegram_bot=controller_bot,
    admin_chat_id=123456789  # TODO: Replace with actual admin chat ID from config
)

# Link auto-recovery and admin notifier
auto_recovery.set_admin_notifier(admin_notifier)

# Start auto-recovery loop
await auto_recovery.start()
logger.info("✅ Error handling system initialized")
```

---

### 🚀 STEP 2: Update signal processing

In signal parser/handler, add:
```python
from src.utils.error_handlers import (
    validate_signal,
    signal_deduplicator,
    risk_limit_checker
)
from src.utils.error_codes import TE_001_INVALID_SIGNAL, TE_002_RISK_LIMIT_EXCEEDED, TE_003_DUPLICATE

async def process_signal(signal_data):
    # 1. Validate signal structure
    is_valid, error_msg = validate_signal(signal_data)
    if not is_valid:
        logger.warning(f"{TE_001_INVALID_SIGNAL}: {error_msg}")
        return False
    
    # 2. Check for duplicates
    if signal_deduplicator.is_duplicate(signal_data):
        logger.info(f"{TE_003_DUPLICATE}: Blocked duplicate signal")
        return False
    
    # 3. Check risk limits
    can_trade, reason = risk_limit_checker.check_risk_limits()
    if not can_trade:
        logger.critical(f"{TE_002_RISK_LIMIT_EXCEEDED}: {reason}")
        # Optionally notify admin
        if admin_error_notifier:
            await admin_error_notifier.notify_critical_system_error(
                "Trading Engine",
                reason
            )
        return False
    
    # Process trade...
    result = await execute_trade(signal_data)
    
    # 4. Update risk tracking
    if result['pnl']:
        risk_limit_checker.update_pnl(result['pnl'])
    
    return True
```

---

### 🚀 STEP 3: Update error handling in existing code

Replace generic error handling with error codes:

**Before:**
```python
try:
    await bot.send_message(chat_id, text)
except Exception as e:
    logger.error(f"Failed to send message: {e}")
```

**After:**
```python
from src.utils.error_handlers import split_long_message
from src.utils.error_codes import TG_005_MESSAGE_TOO_LONG

try:
    # Handle long messages automatically
    if len(text) > 4096:
        chunks = split_long_message(text)
        for chunk in chunks:
            await bot.send_message(chat_id, chunk)
    else:
        await bot.send_message(chat_id, text)
except Exception as e:
    logger.error(f"Failed to send message: {e}")
```

---

### 🚀 STEP 4: Add admin chat ID to config

In your config file (e.g., `config/settings.json` or `.env`):
```json
{
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN",
    "admin_chat_id": 123456789,  // ADD THIS
    ...
  }
}
```

Then load it:
```python
config = load_config()
admin_chat_id = config.get('telegram', {}).get('admin_chat_id')
```

---

### 🚀 STEP 5: Test auto-recovery

**Test MT5 Recovery:**
1. Start bot
2. Close MT5 terminal
3. Wait 60 seconds
4. Check logs for `MT-001: MT5 disconnected, attempting recovery`
5. Verify MT5 reconnects automatically

**Test Database Recovery:**
1. Lock database file externally
2. Wait 60 seconds
3. Check logs for `DB-001: Database disconnected, attempting recovery`
4. Unlock database
5. Verify reconnection

**Test Telegram Recovery:**
1. Start second bot instance (will trigger HTTP 409)
2. Check logs for `TG-001: HTTP 409 Conflict`
3. Stop second instance
4. Verify first bot recovers

---

### 🚀 STEP 6: Monitor logs

After integration, monitor two log files:

**logs/bot.log** - All activity (INFO+)
```
2025-01-XX 14:30:45 | INFO     | main | ✅ Error handling system initialized
2025-01-XX 14:31:00 | INFO     | auto_recovery | ✅ Auto-recovery system started
```

**logs/errors.log** - Errors only (ERROR+)
```
2025-01-XX 14:32:15 | ERROR    | telegram | TG-002: Rate limit exceeded - Retry after 30s
2025-01-XX 14:35:00 | ERROR    | trading_engine | TE-001: Invalid signal - Missing entry price
```

---

### 🚀 STEP 7: Add daily reset (optional)

If using risk limits, add daily reset at midnight:

```python
import schedule
import asyncio

async def reset_daily_limits():
    from src.utils.error_handlers import risk_limit_checker
    risk_limit_checker.reset_daily()
    logger.info("Daily risk limits reset")

# Schedule at 00:00
schedule.every().day.at("00:00").do(lambda: asyncio.create_task(reset_daily_limits()))
```

---

## 🎯 QUICK CHECKLIST

- [ ] Add imports to main.py
- [ ] Initialize error logging
- [ ] Initialize auto-recovery
- [ ] Initialize admin notifier
- [ ] Link auto-recovery + admin notifier
- [ ] Start auto-recovery loop
- [ ] Update signal processing with validation
- [ ] Update signal processing with deduplication
- [ ] Update signal processing with risk limits
- [ ] Add admin_chat_id to config
- [ ] Test MT5 auto-recovery
- [ ] Test DB auto-recovery
- [ ] Test Telegram auto-recovery
- [ ] Monitor logs/bot.log
- [ ] Monitor logs/errors.log
- [ ] (Optional) Add daily reset scheduler

---

## 📋 VERIFICATION

After integration, run:
```bash
python verify_error_handling.py
```

Expected output:
```
✓ SECTION1...................... 7/7 (100%)
✓ SECTION2...................... 11/11 (100%)
✓ SECTION3...................... 4/4 (100%)
✓ SECTION4...................... 3/3 (100%)
✓ SECTION5...................... 2/2 (100%)
✓ SECTION6...................... 5/5 (100%)

OVERALL ERROR HANDLING STATUS: 32/32 (100%)
```

---

## 🆘 TROUBLESHOOTING

**Auto-recovery not starting:**
- Check `auto_recovery.start()` is called
- Verify `running` flag is True
- Check for exceptions in logs

**Admin notifications not sending:**
- Verify `admin_chat_id` is configured
- Check admin_notifier is initialized
- Verify bot can send to admin chat

**Risk limits not working:**
- Check `update_pnl()` is called after trades
- Verify limits are set correctly
- Check `reset_daily()` is called

**Logs not appearing:**
- Verify `setup_error_logging()` is called
- Check `logs/` directory exists
- Verify file permissions

---

## 📞 SUPPORT

If issues occur:
1. Check `logs/errors.log` for error details
2. Run `verify_error_handling.py` to check status
3. Review ERROR_HANDLING_IMPLEMENTATION_REPORT.md
4. Check error code reference in report

---

**Status**: Ready for integration  
**Estimated Time**: 30-60 minutes  
**Difficulty**: Low (mostly copy-paste)
