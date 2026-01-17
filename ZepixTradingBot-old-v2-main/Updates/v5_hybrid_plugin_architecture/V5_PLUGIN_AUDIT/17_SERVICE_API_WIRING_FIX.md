# 🔧 SERVICE API WIRING FIX MANDATE

**Mandate ID:** 17_SERVICE_API_WIRING_FIX  
**Date:** 2026-01-17  
**Priority:** 🔴 **CRITICAL - BLOCKING TRADES**  
**Status:** **PENDING EXECUTION**

---

## 🎯 OBJECTIVE: FIX ServiceAPI METHOD SIGNATURES

**Current Issue:** V3 Plugin calls ServiceAPI methods with `plugin_id` parameter, but ServiceAPI doesn't accept it.

**Affected Methods:**
1. `ServiceAPI.place_order()` - Missing `plugin_id` parameter
2. `ServiceAPI.send_notification()` - Missing `plugin_id` parameter  
3. `ServiceAPI.calculate_lot_size()` - Missing `plugin_id` parameter
4. `ServiceAPI.calculate_sl_price()` - Method doesn't exist
5. `ServiceAPI.close_positions_by_direction()` - Method doesn't exist

---

## 📋 EXECUTION STEPS

### STEP 1: UPDATE ServiceAPI CLASS

**File:** `Trading_Bot/src/core/plugin_system/service_api.py`

**Add/Update these methods:**

```python
def place_order(
    self,
    symbol: str,
    direction: str,
    lot_size: float,
    sl: float,
    tp: float,
    order_type: str = "ORDER_A",
    plugin_id: str = None,  # ← ADD THIS
    **kwargs
) -> dict:
    """Place order with plugin tracking"""
    # Existing logic + add plugin_id to metadata
    pass

def send_notification(
    self,
    message: str,
    notification_type: str = "INFO",
    plugin_id: str = None,  # ← ADD THIS
    **kwargs
) -> bool:
    """Send Telegram notification with plugin source"""
    # Existing logic + add plugin_id to message metadata
    pass

def calculate_lot_size(
    self,
    symbol: str,
    risk_percent: float = None,
    plugin_id: str = None,  # ← ADD THIS
    **kwargs
) -> float:
    """Calculate lot size with plugin-specific multipliers"""
    # Existing logic
    pass

def calculate_sl_price(
    self,
    symbol: str,
    direction: str,
    entry_price: float,
    sl_pips: float,
    plugin_id: str = None,  # ← ADD THIS
) -> float:
    """Calculate SL price from pips"""
    # NEW METHOD - Implement pip-to-price conversion
    pip_value = 0.0001 if "JPY" not in symbol else 0.01
    if direction == "BUY":
        return entry_price - (sl_pips * pip_value)
    else:
        return entry_price + (sl_pips * pip_value)

def close_positions_by_direction(
    self,
    symbol: str,
    direction: str,
    plugin_id: str = None,  # ← ADD THIS
) -> dict:
    """Close all positions for symbol in given direction"""
    # NEW METHOD - Implement position closing logic
    # Use self.mt5_client.close_positions(...)
    pass
```

---

### STEP 2: VERIFY THE FIX

**Re-run the trade simulation:**
```bash
cd Trading_Bot
python tests/live_activation/inject_v3_signal.py
```

**Expected Output (NO ERRORS):**
```
✅ Signal received
✅ Plugin processed
✅ Order A placed: EURUSD BUY 0.0050 lots
✅ Order B placed: EURUSD BUY 0.0050 lots  
✅ Telegram notification sent
✅ Session created: SES_20260117_...
```

---

### STEP 3: DATABASE VERIFICATION

**Query:**
```sql
SELECT * FROM trading_sessions WHERE symbol='EURUSD' ORDER BY created_at DESC LIMIT 1;
```

**Expected Result:**
- 1 row with `session_id`, `symbol=EURUSD`, `direction=BUY`, `status=ACTIVE`

---

## 📊 DELIVERABLES

1. **Updated ServiceAPI code** (Git diff showing changes)
2. **Trade simulation logs** (Showing successful order placement)
3. **Database screenshot** (Showing session record)
4. **Telegram screenshot** (Showing entry alert notification)

---

## ⏱️ DEADLINE: 1 HOUR

**This is the FINAL BLOCKER.** Once fixed, the bot is 100% operational.

**NO EXCUSES. FIX THE WIRING.** 🔧
