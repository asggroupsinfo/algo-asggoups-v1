# DEVIN: MANDATE 22 EXECUTION PROMPT

## 📋 TASK OVERVIEW
Execute Mandate 22 to fix V6 TrendManager misuse in 5M, 15M, 1H plugins.

**File:** `updates/v5_hybrid_plugin_architecture/V5_PLUGIN_AUDIT/22_V6_TRENDMANAGER_FIX.md`

---

## 🎯 OBJECTIVE
Replace internal TrendManager calls with Alert Payload parsing to enforce "Pine Script Supremacy" - where Bot uses Pine's calculated data (ADX, MTF Alignment, Confidence) to make intelligent filtering decisions WITHOUT calling outdated internal state.

---

## 🔧 IMPLEMENTATION STEPS

### **STEP 1: Code Fixes (3 Files)**

**Files to modify:**
1. `Trading_Bot/src/logic_plugins/v6_price_action_5m/plugin.py` (Line 274)
2. `Trading_Bot/src/logic_plugins/v6_price_action_15m/plugin.py` (Line 285)
3. `Trading_Bot/src/logic_plugins/v6_price_action_1h/plugin.py` (Line 275)

**Action:**
- Remove `service_api.check_pulse_alignment()` / `check_timeframe_alignment()` calls
- Replace with `alert.mtf_string` parsing (as shown in Mandate 22, lines 45-62)
- Ensure thresholds are applied to **Pine's data**, not internal state

### **STEP 2: Alert Model Verification**

Check `Trading_Bot/src/core/models.py`:
- Confirm `ZepixV6Alert` has `mtf_string` field
- If missing, add it to the model
- Ensure it's populated during signal parsing

### **STEP 3: V3 Protection**

**CRITICAL:** Run MD5 checksums on V3 files:
```bash
md5sum Trading_Bot/src/logic_plugins/v3_combined/*.py
```
Compare with baseline from Mandate 19. Must be 100% match.

### **STEP 4: Testing**

Create test file: `Trading_Bot/tests/test_v6_payload_filtering.py`

**Test Case 1: Strong Alignment (Should PASS)**
```python
test_signal = {
    "type": "BULLISH_ENTRY",
    "ticker": "EURUSD",
    "tf": "60",
    "direction": "BUY",
    "adx": 28.5,
    "mtf_string": "3/0",  # Strong bullish
    "conf_score": 85,
    "sl": 1.0800,
    "tp1": 1.0900
}
# Expected: Order PLACED (even if internal TrendManager says "Bearish")
```

**Test Case 2: Weak Alignment (Should REJECT)**
```python
test_signal = {
    "type": "BULLISH_ENTRY",
    "ticker": "EURUSD",
    "tf": "60",
    "direction": "BUY",
    "adx": 28.5,
    "mtf_string": "1/2",  # Weak/conflicting
    "conf_score": 85
}
# Expected: Order REJECTED (because Pine's MTF data shows weakness)
```

**Test Case 3: Missing MTF Field (Should handle gracefully)**
```python
test_signal = {
    "type": "BULLISH_ENTRY",
    "ticker": "EURUSD",
    "tf": "60",
    "direction": "BUY",
    "adx": 28.5,
    # mtf_string missing
    "conf_score": 85
}
# Expected: Log warning, proceed with caution (or reject based on config)
```

Run tests:
```bash
cd Trading_Bot
pytest tests/test_v6_payload_filtering.py -v
```

---

## 📊 DOCUMENTATION UPDATES REQUIRED

### **1. Update Planning Documents**

**File:** `Updates/v5_hybrid_plugin_architecture/V6_INTEGRATION_PROJECT/02_PLANNING PRICE ACTION LOGIC/05_PRICE_ACTION_LOGIC_1H.md`

**Change Lines 56-66:**

**BEFORE (Incorrect):**
```python
def validate_entry(self, alert: ZepixV6Alert, trend_state: TrendState) -> bool:
    tf_4h_trend = trend_state.get_trend("240")  # ❌ WRONG
```

**AFTER (Correct):**
```python
def validate_entry(self, alert: ZepixV6Alert) -> bool:
    # Parse MTF alignment from Pine's payload
    bullish_count, bearish_count = map(int, alert.mtf_string.split('/'))
    
    # Use Pine's data for filtering (Trader Brain)
    if alert.direction == "BUY" and bullish_count < 3:
        return False  # Reject weak alignment
```

**Repeat for:**
- `02_PRICE_ACTION_LOGIC_1M.md`
- `03_PRICE_ACTION_LOGIC_5M.md`
- `04_PRICE_ACTION_LOGIC_15M.md`

### **2. Update Master Plan**

**File:** `Updates/v5_hybrid_plugin_architecture/V6_INTEGRATION_PROJECT/02_PLANNING PRICE ACTION LOGIC/01_INTEGRATION_MASTER_PLAN.md`

**Add Section 6: DATA-DRIVEN FILTERING**
```markdown
## 6. DATA-DRIVEN FILTERING (Pine Supremacy)

V6 plugins use Pine Script's calculated data for intelligent filtering:

| Data Field | Source | Usage |
|------------|--------|-------|
| ADX Value | `alert.adx` | Trend strength check |
| MTF Alignment | `alert.mtf_string` | Multi-timeframe validation |
| Confidence | `alert.conf_score` | Signal quality filter |

**CRITICAL:** Plugins do NOT use internal TrendManager for fresh entry validation.
TrendManager is ONLY used for Re-entry decisions (when no new signal exists).
```

### **3. Create Fix Report**

**File:** `updates/v5_hybrid_plugin_architecture/V5_PLUGIN_AUDIT/22_V6_TRENDMANAGER_FIX_REPORT.md`

**Structure:**
```markdown
# MANDATE 22: V6 TRENDMANAGER FIX - EXECUTION REPORT

## CHANGES MADE

### V6 5M Plugin
- **Line 274:** Removed `check_pulse_alignment()` call
- **Replacement:** MTF parsing from `alert.mtf_string`
- **Code Diff:** [Paste before/after]

### V6 15M Plugin
[Same structure]

### V6 1H Plugin
[Same structure]

## VERIFICATION

### V3 Protection
- Checksum Match: ✅ 100%
- Files Verified: combinedlogic_1.py, combinedlogic_2.py, combinedlogic_3.py

### Test Results
- Test Case 1 (Strong Alignment): ✅ PASS
- Test Case 2 (Weak Alignment): ✅ PASS (Correctly rejected)
- Test Case 3 (Missing Field): ✅ PASS (Handled gracefully)

## CONCLUSION
Pine Supremacy restored. Bot now uses Pine's data for filtering without calling internal TrendManager.
```

---

## ✅ ACCEPTANCE CRITERIA

**Task is COMPLETE only when:**
1. ✅ All 3 V6 plugins modified (5M, 15M, 1H)
2. ✅ NO `service_api.check_*_alignment()` calls in `_validate_entry()`
3. ✅ V3 checksums 100% match
4. ✅ All 3 test cases pass
5. ✅ Planning documents updated (5 files)
6. ✅ Fix report created with evidence
7. ✅ Git commit with message: `fix(v6): Enforce Pine Supremacy - Use payload data for filtering`

---

## 🚨 CRITICAL REMINDERS

1. **DO NOT remove TrendManager entirely** - needed for Re-entry
2. **DO NOT modify V3 plugins**
3. **DO parse MTF carefully** - handle missing data gracefully
4. **DO update ALL planning docs** - keep them in sync with code

---

**START EXECUTION NOW.**
