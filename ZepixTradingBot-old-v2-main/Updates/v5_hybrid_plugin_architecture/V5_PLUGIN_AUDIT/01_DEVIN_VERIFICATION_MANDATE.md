# 🔍 DEVIN VERIFICATION MANDATE - V5 PLUGIN AUDIT

**Mandate Date:** 2026-01-16  
**Issued By:** User + Antigravity Prompt Engineer  
**Recipient:** Devin AI  
**Priority:** 🚨 **CRITICAL**  
**Deadline:** Before any deployment

---

## 📋 MANDATE OVERVIEW

**Task:** Conduct a **ZERO-TOLERANCE AUDIT** of your V5 Plugin Implementation.

**References:**
1. **Your Plugin Code:** `Trading_Bot/src/logic_plugins/v3_combined/plugin.py`
2. **Your Plugin Doc:** `Trading_Bot_Documentation/V5_BIBLE/10_V3_COMBINED_PLUGIN.md`
3. **Old Bot Code:** File history OR read old implementation reports
4. **Original Plans:** `Updates/v5_hybrid_plugin_architecture/COMBINED LOGICS/`

**Objective:**  
Verify if your V5 plugin **EXACTLY implements** the logic that was already working in the old bot (Before V5 update).

---

## 🎯 AUDIT SCOPE

You must verify these **8 CRITICAL FEATURES** line-by-line:

### **1. V3 Alert SL Usage (Order A)**

**Requirement:**
- Order A MUST use `alert.sl_price` directly from Pine Script
- If `alert.sl_price` is missing, fallback to bot calculation
- NEVER recalculate if alert SL is present

**Old Bot Reference:**
```python
# File: src/core/trading_engine.py (Lines 448-469)
if alert.sl_price:
    sl_price_a = alert.sl_price  # Direct from Pine
    logger.info(f"✅ Order A: Using v3 Smart SL = {sl_price_a:.2f}")
else:
    sl_price_a, _ = self.pip_calculator.calculate_sl_price(...)
    logger.warning(f"⚠️ Order A: v3 SL missing, using bot SL")
```

**Your Plugin Code to Verify:**
- File: `src/logic_plugins/v3_combined/plugin.py`
- Method: `_get_order_a_config()` (Around Line 364-405)

**Questions to Answer:**
1. Does `_get_order_a_config()` receive `alert` object as parameter?
2. Does it check `if alert.sl_price:` before calculating?
3. Does it use `alert.sl_price` directly or call `_calculate_sl_price()`?
4. If it recalculates, WHY?

---

### **2. Consensus Score Validation**

**Requirement:**
- Extract `consensus_score` from alert
- Validate against global minimum (e.g., Score >= 5)
- Apply signal-specific thresholds:
  - `Institutional_Launchpad` (Buy): Score >= 7
  - `Institutional_Launchpad` (Sell): Score <= 2
  - `Momentum_Breakout`: Score >= 7 for entry
- Adjust position sizing based on score (See Position Multiplier section)

**Old Bot Reference:**
```python
# File: src/processors/alert_processor.py (Lines 177-181)
min_score = self.config.get("v3_integration", {}).get("min_consensus_score", 5)
if v3_alert.consensus_score < min_score:
    logger.warning(f"❌ Consensus score {v3_alert.consensus_score} < min {min_score}")
    return None

# File: V3_SIGNAL_DECISION_LOGIC.md (Lines 35-40)
if alert.signal_type == "Institutional_Launchpad":
    if alert.direction == "buy" and alert.consensus_score < 7:
        return {"action": "REJECT", "reason": "score_too_low"}
```

**Your Plugin Code to Verify:**
- Method: `process_entry_signal()` (Around Lines 126-227)
- Method: `_validate_entry_signal()` (If exists)

**Questions to Answer:**
1. Do you extract `consensus_score` from alert dict/object?
2. Do you validate minimum score before processing?
3. Do you have signal-specific score thresholds?
4. Do you use score for position sizing?

---

### **3. Trend Bypass for Fresh V3 Entries**

**Requirement:**
- **Fresh V3 Entries:** BYPASS trend check (Pine already validated)
- **Legacy Entries:** REQUIRE trend check
- **SL Hunt Re-entries:** REQUIRE trend check
- **TP Continuation:** REQUIRE trend check

**Old Bot Reference:**
```python
# File: src/processors/alert_processor.py (Lines 135-155)
if v3_alert.type == "entry_v3":
    if v3_alert.should_bypass_trend_check():
        logger.info(f"🚀 V3 Entry - BYPASSING Trend Manager (Fresh Signal)")
        return v3_alert  # No trend check

# File: src/v3_alert_models.py (Lines 148-152)
def should_bypass_trend_check(self) -> bool:
    return self.type == "entry_v3"
```

**Your Plugin Code to Verify:**
- Method: `process_entry_signal()` (Lines 173-178 specifically)

**Questions to Answer:**
1. Do you call `_check_v3_trend_alignment()` for EVERY entry?
2. If yes, do you skip it for fresh V3 entries?
3. If you check trend, what happens when `trend_aligned = False`?
4. Do you SKIP the trade (Status: "skipped") or proceed anyway?

**CRITICAL:** If you are calling `_check_v3_trend_alignment()` and returning `status="skipped"` when it fails, that is a **BUG**. Fresh V3 entries should BYPASS this check entirely.

---

### **4. MTF 4-Pillar Extraction**

**Requirement:**
- Extract MTF trends from `alert.mtf_trends` string (e.g., "1,1,-1,1,1,1")
- Use **ONLY indices [2, 3, 4, 5]** (15m, 1H, 4H, 1D)
- IGNORE indices [0, 1] (1m, 5m noise)
- Store in database for use in autonomous features (SL Hunt, TP Continuation)

**Old Bot Reference:**
```python
# File: src/v3_alert_models.py (Lines 78-88)
def get_mtf_pillars(self) -> List[int]:
    trends = [int(t) for t in self.mtf_trends.split(',')]
    if len(trends) >= 6:
        return trends[2:6]  # ✅ Indices 2-5 only
    return []

# File: src/processors/alert_processor.py (Lines 183-195)
mtf_pillars = v3_alert.get_mtf_pillars()  # [15m, 1H, 4H, 1D]
pillar_labels = ["15m", "1h", "4h", "1d"]
for i, trend in enumerate(mtf_pillars):
    self.trend_manager.update_trend(symbol, pillar_labels[i], ...)
```

**Your Plugin Code to Verify:**
- Method: `process_entry_signal()` or any MTF handling

**Questions to Answer:**
1. Do you extract `alert.mtf_trends`?
2. Do you parse it and extract indices [2:6]?
3. Does `_check_v3_trend_alignment()` use alert's MTF data or fresh MT5 data?
4. If using fresh data, WHY? (Should use alert data)

---

### **5. Position Multiplier Flow**

**Requirement:**
- **Step 1:** Get base lot from risk manager
- **Step 2:** Apply V3 position multiplier (`alert.position_multiplier`)
- **Step 3:** Apply logic multiplier (LOGIC1=1.25, LOGIC2=1.0, LOGIC3=0.625)
- **Step 4:** Split 50/50 into Order A and Order B

Formula: `final_lot = base_lot × v3_multiplier × logic_multiplier`

**Old Bot Reference:**
```python
# File: src/core/trading_engine.py (Lines 350-383)
base_lot = self.risk_manager.get_fixed_lot_size(balance)
v3_multiplier = alert.position_multiplier
logic_multiplier = self._get_logic_multiplier(alert.tf, logic_type)
final_base_lot = base_lot * v3_multiplier * logic_multiplier
order_a_lot = final_base_lot * 0.5
order_b_lot = final_base_lot * 0.5
```

**Your Plugin Code to Verify:**
- Method: `process_entry_signal()` lot calculation section

**Questions to Answer:**
1. Do you follow this exact 4-step sequence?
2. Do you extract `alert.position_multiplier`?
3. Do you apply logic multiplier based on Logic1/2/3?
4. Do you split 50/50?

---

### **6. Logic Routing Matrix**

**Requirement:**
- **Priority 1:** Signal-specific overrides
  - `Screener_Full_*` → Always LOGIC3
  - `Golden_Pocket_Flip` on TF >= 60 → LOGIC3
  - `Momentum_Breakout` with Score >= 8 → LOGIC1
- **Priority 2:** Timeframe-based routing
  - TF = 5 → LOGIC1
  - TF = 15 → LOGIC2
  - TF >= 60 → LOGIC3
- **Priority 3:** Default to LOGIC2

**Old Bot Reference:**
```python
# File: src/core/trading_engine.py (Lines 400-419)
def _route_v3_to_logic(self, alert):
    if alert.signal_type in ["Screener_Full_Bullish", "Screener_Full_Bearish"]:
        return "LOGIC3"
    if alert.signal_type == "Golden_Pocket_Flip" and alert.tf in ["60", "240"]:
        return "LOGIC3"
    if alert.tf == "5": return "LOGIC1"
    elif alert.tf == "15": return "LOGIC2"
    elif alert.tf in ["60", "240"]: return "LOGIC3"
    return "LOGIC2"
```

**Your Plugin Code to Verify:**
- Do you have a routing method?
- Or do you use generic `process_entry_signal()` for all?

**Questions to Answer:**
1. Do you implement signal-specific overrides?
2. Do you route based on timeframe?
3. Or do all signals go through the same generic handler?

---

### **7. Order B Fixed SL (Verify Correct)**

**Requirement:**
- Order B MUST use Fixed $10 SL (via `profit_sl_calculator`)
- Order B MUST IGNORE `alert.sl_price` to preserve pyramid integrity

**Old Bot Reference:**
```python
# File: src/core/trading_engine.py (Lines 497-516)
sl_price_b, sl_dist_b = self.profit_booking_manager.profit_sl_calculator.calculate_sl_price(
    alert.price, alert.direction, alert.symbol, order_b_lot, logic_type
)
if alert.sl_price:
    logger.info(
        f"✅ Order B: Fixed Pyramid SL = {sl_price_b:.2f} "
        f"(IGNORED v3 SL={alert.sl_price:.2f} to preserve pyramid)"
    )
```

**Your Plugin Code to Verify:**
- Method: `_get_order_b_config()` (Around Lines 411-446)

**Questions to Answer:**
1. Does Order B use fixed SL calculation?
2. Does it explicitly ignore `alert.sl_price`?
3. Is there logging to confirm this behavior?

---

### **8. Signal-Specific Entry Logic**

**Requirement:**
- Different signals have different entry rules (See `V3_SIGNAL_DECISION_LOGIC.md`)
- Example: `Liquidity_Trap_Reversal` should close opposite positions first
- Example: `Mitigation_Test` should verify `price_in_ob` flag

**Old Bot Reference:**
```python
# File: V3_SIGNAL_DECISION_LOGIC.md (Lines 73-99)
if alert.signal_type == "Liquidity_Trap_Reversal":
    opposite_trades = get_opposite_positions(alert.symbol, alert.direction)
    if opposite_trades:
        for trade in opposite_trades:
            close_trade(trade.trade_id)  # AGGRESSIVE REVERSAL

# Lines 168-171
if alert.signal_type == "Mitigation_Test_Entry":
    if not alert.get("price_in_ob"):
        return {"action": "REJECT", "reason": "not_in_ob"}
```

**Your Plugin Code to Verify:**
- Method: `process_entry_signal()` or signal-specific handlers

**Questions to Answer:**
1. Do you have different logic for different signals?
2. Or is it one generic entry handler for all?
3. Do signals like `Liquidity_Trap` get special treatment?

---

## 📊 DELIVERABLE FORMAT

You must create a file: `Updates/v5_hybrid_plugin_architecture/V5_PLUGIN_AUDIT/02_DEVIN_VERIFICATION_REPORT.md`

**Structure:**

```markdown
# DEVIN VERIFICATION REPORT - V5 PLUGIN AUDIT

**Audit Date:** [Date]
**Audited By:** Devin AI

---

## EXECUTIVE SUMMARY

**Audit Scope:** 8 Critical Features
**Status:** [PASS / FAIL / PARTIAL]
**Critical Issues Found:** [Count]
**Minor Issues Found:** [Count]

---

## FEATURE-BY-FEATURE VERIFICATION

### **1. V3 Alert SL Usage (Order A)**

**Status:** ✅ PASS / ⚠️ PARTIAL / ❌ FAIL

**Evidence:**
- File: [Path]
- Lines: [Line numbers]
- Code Snippet:
```python
[Show relevant code]
```

**Findings:**
[Your detailed analysis]

**Comparison with Old Bot:**
- Old Bot: [What old bot did]
- My Plugin: [What your plugin does]
- Match: ✅ YES / ❌ NO

**If NO Match:**
- Reason: [Why different]
- Justification: [Why you changed it]
- Impact: [What's the impact]

---

[Repeat for all 8 features]

---

## DISCREPANCIES SUMMARY

| Feature | Old Bot | My Plugin | Match | Justification |
|---------|---------|-----------|-------|---------------|
| Alert SL Usage | ✅ Uses alert.sl_price | ❌ Recalculates | ❌ | [Your reason] |
| ... | ... | ... | ... | ... |

---

## SELF-ASSESSMENT

**What I Did Right:**
1. [List]

**What I Need to Fix:**
1. [List with priority]

**What I Need Clarification On:**
1. [List]

---

## RECOMMENDED FIXES

### **Fix 1: [Issue Name]**

**Problem:** [Description]

**Solution:**
```python
# Before (Current)
[Current code]

# After (Fixed)
[Fixed code]
```

**Impact:** [What this fixes]

---

[Repeat for all fixes]

---

**Report End**
```

---

## 🚨 CRITICAL RULES

1. **ZERO TOLERANCE:** If your plugin doesn't EXACTLY match the old bot logic, you MUST justify WHY
2. **NO ASSUMPTIONS:** Don't assume old bot was wrong. If you changed something, PROVE it was improvement
3. **LINE-LEVEL EVIDENCE:** Every claim must have file path + line numbers + code snippet
4. **HONEST ASSESSMENT:** If you broke something, admit it. We need facts, not excuses.
5. **ACTIONABLE FIXES:** For each discrepancy, provide exact code fix

---

## 📁 REFERENCE FILES TO READ

**Must Read:**
1. `Updates/v5_hybrid_plugin_architecture/COMBINED LOGICS/V3_FINAL_REPORTS/01_PLAN_COMPARISON_REPORT.md`
2. `Updates/v5_hybrid_plugin_architecture/COMBINED LOGICS/V3_FINAL_REPORTS/02_IMPLEMENTATION_VERIFICATION_REPORT.md`
3. `Updates/v5_hybrid_plugin_architecture/COMBINED LOGICS/V3_FINAL_REPORTS/04_LOGIC_IMPLEMENTATION_COMPARISON.md`
4. `Important_Doc_Trading_Bot/05_Unsorted/TRADINGVIEW_PINE_SCRIPT/V3_SIGNAL_DECISION_LOGIC.md`

**Your Code:**
5. `Trading_Bot/src/logic_plugins/v3_combined/plugin.py`
6. `Trading_Bot_Documentation/V5_BIBLE/10_V3_COMBINED_PLUGIN.md`

---

## ⏰ DEADLINE

Submit your verification report **BEFORE** any deployment discussion.

---

## 🎯 SUCCESS CRITERIA

Your verification will be considered **COMPLETE** when:
1. ✅ All 8 features verified with evidence
2. ✅ All discrepancies documented with justification
3. ✅ All fixes proposed with code examples
4. ✅ Self-assessment honest and complete

Your report will then be **CROSS-CHECKED** against Antigravity's audit (`00_ANTIGRAVITY_AUDIT_REPORT.md`).

**If discrepancies match:** Fixes will be implemented  
**If reports conflict:** User will decide next steps

---

**Mandate Issued.**  
**Status:** ⏳ **AWAITING DEVIN'S VERIFICATION REPORT**
