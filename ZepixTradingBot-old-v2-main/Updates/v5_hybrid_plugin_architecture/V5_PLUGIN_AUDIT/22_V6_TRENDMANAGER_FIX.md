# MANDATE 22: FIX V6 TRENDMANAGER MISUSE
**Date:** 2026-01-17  
**Priority:** CRITICAL  
**Type:** Code Fix (Data-Driven Architecture Enforcement)  
**Objective:** Remove TrendManager calls from V6 5M, 15M, 1H plugins during FRESH ENTRY validation and replace with Alert Payload parsing.

---

## 🎯 AUDIT FINDINGS (From Mandate 21)

**CONFIRMED ISSUE:** V6 plugins (5M, 15M, 1H) are calling internal TrendManager methods during fresh entry validation, violating "Pine Script Supremacy" principle.

| Plugin | Issue | Line | Method Called |
|--------|-------|------|---------------|
| V6 5M | TrendManager misuse | 274 | `check_pulse_alignment()` |
| V6 15M | TrendManager misuse | 285 | `check_pulse_alignment()` |
| V6 1H | TrendManager misuse | 275 | `check_timeframe_alignment()` |

**Impact:** Bot may reject valid signals that Pine Script already approved because internal state is outdated/different from real-time Pine data.

---

## 🔧 FIX REQUIREMENTS

### **TARGET FILES:**
1. `Trading_Bot/src/logic_plugins/v6_price_action_5m/plugin.py`
2. `Trading_Bot/src/logic_plugins/v6_price_action_15m/plugin.py`
3. `Trading_Bot/src/logic_plugins/v6_price_action_1h/plugin.py`

### **CHANGES REQUIRED:**

#### **BEFORE (Current - WRONG):**
```python
# File: v6_price_action_1h/plugin.py, Line 275
if self.REQUIRE_4H_ALIGNMENT:
    is_aligned = await self.service_api.check_timeframe_alignment(
        symbol=alert.ticker,
        direction=alert.direction,
        higher_tf="240"
    )
    if not is_aligned:
        return {"valid": False, "reason": "4h_alignment_failed"}
```

#### **AFTER (Desired - CORRECT):**
```python
# Parse alignment from alert payload
if self.REQUIRE_4H_ALIGNMENT and hasattr(alert, 'mtf_string'):
    # Parse "3/0" format (BullishCount/BearishCount)
    try:
        bullish_count, bearish_count = map(int, alert.mtf_string.split('/'))
        
        # For BUY: Need strong bullish alignment (e.g., >= 2 TFs)
        # For SELL: Need strong bearish alignment (e.g., >= 2 TFs)
        if alert.direction == "BUY" and bullish_count < 2:
            return {"valid": False, "reason": "weak_bullish_alignment"}
        elif alert.direction == "SELL" and bearish_count < 2:
            return {"valid": False, "reason": "weak_bearish_alignment"}
    except (ValueError, AttributeError):
        # If parsing fails, log warning but don't reject
        self.logger.warning(f"[1H] Could not parse MTF alignment from alert")
```

---

## 📋 STEP-BY-STEP FIX PROTOCOL

### **STEP 1: Verify Alert Model**
Check `Trading_Bot/src/core/models.py` to confirm `ZepixV6Alert` has:
- `mtf_string` field (e.g., "3/0")
- OR `bullish_alignment` and `bearish_alignment` fields

**If missing:** Add the field to the model first.

### **STEP 2: Fix V6 5M Plugin**
File: `Trading_Bot/src/logic_plugins/v6_price_action_5m/plugin.py`

**Action:**
- Locate Line 274 (`check_pulse_alignment()` call)
- Replace with payload-based alignment parsing
- Use threshold: `bullish_count >= 2` for BUY, `bearish_count >= 2` for SELL

### **STEP 3: Fix V6 15M Plugin**
File: `Trading_Bot/src/logic_plugins/v6_price_action_15m/plugin.py`

**Action:**
- Locate Line 285 (`check_pulse_alignment()` call)
- Replace with payload-based alignment parsing
- Use threshold: `bullish_count >= 2` for BUY, `bearish_count >= 2` for SELL

### **STEP 4: Fix V6 1H Plugin**
File: `Trading_Bot/src/logic_plugins/v6_price_action_1h/plugin.py`

**Action:**
- Locate Line 275 (`check_timeframe_alignment()` call)
- Replace with payload-based alignment parsing
- Use threshold: `bullish_count >= 3` for BUY (stricter for swing), `bearish_count >= 3` for SELL

### **STEP 5: V3 Protection Verification**
**CRITICAL:** Ensure V3 plugins remain untouched.

**Verification:**
- Run checksums on V3 files (same as Mandate 19)
- Confirm 100% match (no accidental changes)

### **STEP 6: Testing**
Create test scenario:
1. **Packet says:** `MTF: 3/0` (Strong Bullish)
2. **Internal TrendManager says:** Bearish (outdated)
3. **Expected Result:** Order PLACED (because Packet wins)

**Test Command:**
```python
# Inject test signal
test_signal = {
    "type": "BULLISH_ENTRY",
    "ticker": "EURUSD",
    "tf": "60",
    "direction": "BUY",
    "adx": 28.5,
    "mtf_string": "3/0",  # Strong bullish
    "conf_score": 85
}
# Should PASS validation even if TrendManager says "Bearish"
```

---

## ✅ ACCEPTANCE CRITERIA

**Fix is COMPLETE only when:**
1. ✅ All 3 V6 plugins (5M, 15M, 1H) use `alert.mtf_string` for alignment
2. ✅ NO calls to `service_api.check_pulse_alignment()` or `check_timeframe_alignment()` in `_validate_entry()`
3. ✅ V3 plugins checksum 100% match (untouched)
4. ✅ Test signal with "3/0" alignment PASSES even if internal state differs
5. ✅ Code review confirms "Pine Supremacy" is restored

---

## 📊 DELIVERABLES

1. **Modified Files:**
   - `v6_price_action_5m/plugin.py`
   - `v6_price_action_15m/plugin.py`
   - `v6_price_action_1h/plugin.py`

2. **Verification Report:**
   - `22_V6_TRENDMANAGER_FIX_REPORT.md`
   - Include: Before/After code snippets, Test results, V3 checksum proof

3. **Git Commit:**
   - Message: "fix(v6): Remove TrendManager calls from fresh entry validation - Enforce Pine Supremacy"

---

## ⚠️ CRITICAL NOTES

1. **DO NOT remove TrendManager entirely** - it's still needed for RE-ENTRY logic
2. **DO NOT modify V3 plugins** - they are already correct
3. **DO NOT change ADX checks** - they are already using `alert.adx` correctly
4. **DO parse MTF alignment carefully** - handle missing/malformed data gracefully

---

**START FIX NOW. This is the final step to achieve 100% Data-Driven Architecture.**
