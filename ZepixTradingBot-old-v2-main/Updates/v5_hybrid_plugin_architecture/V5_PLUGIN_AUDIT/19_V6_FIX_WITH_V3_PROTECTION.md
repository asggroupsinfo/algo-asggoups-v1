# 🛡️ V6 FIX WITH V3 PROTECTION MANDATE

**Mandate ID:** 19_V6_FIX_WITH_V3_PROTECTION  
**Date:** 2026-01-17  
**Priority:** 🔴 **CRITICAL - ZERO TOLERANCE**  
**Status:** **PENDING EXECUTION**

---

## 🎯 DUAL OBJECTIVE

1. **FIX V6** to 100% compliance (from current 60%)
2. **PROTECT V3** - Ensure V3 logic is UNTOUCHED and still works

**Critical Constraint:** V6 fix should NOT affect V3 AT ALL.

---

## 🚨 DEVIN'S AUDIT FINDINGS (Mandate 18)

Plugin | Compliance | Critical Issues
---|---|---
V6 1M | 70% | Trend Pulse ignored
V6 5M | 100% | ✅ COMPLIANT
V6 15M | 40% | ORDER_A_ONLY (should be DUAL_ORDERS), No ADX check
V6 1H | 30% | Risk 0.6x (should be 1.5x-2.0x), ORDER_A_ONLY, No ADX check

**Overall V6 Status:** 60% Compliant → **40% NON-COMPLIANT** ❌

---

## 📋 EXECUTION PROTOCOL

### **PHASE 1: V3 BASELINE CAPTURE (BEFORE V6 FIX)**

**Purpose:** Save V3's current working state as "golden baseline"

**Tasks:**

1. **Run V3 Test Signal:**
   ```bash
   python tests/live_activation/inject_v3_signal.py
   ```

2. **Capture V3 Baseline:**
   - Save logs: `logs/v3_baseline_before_v6_fix.log`
   - Save order details: Order A ticket, Order B ticket, SL/TP values
   - Save database state: `SELECT * FROM trading_sessions WHERE plugin_id='v3_combined';`

3. **Test V3 Features:**
   - Re-entry system
   - Profit booking
   - Dual orders (50/50 split)
   - Session validation
   
4. **Create V3 Baseline Report:**
   ```markdown
   # V3 Baseline (Before V6 Fix)
   
   ## Order Placement
   - Order A: Ticket #[X], Lot [Y], SL [Z], TP [W]
   - Order B: Ticket #[X], Lot [Y], SL [Z], TP [W]
   
   ## Features Working
   - [x] Dual Order Split (50/50)
   - [x] Session Manager validation
   - [x] Risk calculation
   - [x] Telegram notification
   
   ## Database State
   - Sessions created: [N]
   - Sessions active: [N]
   ```

**Deliverable:** `V3_BASELINE_REPORT.md`

---

### **PHASE 2: V6 FIX IMPLEMENTATION**

**Purpose:** Fix V6 discrepancies WITHOUT touching V3 code

**STRICT RULES:**
- ❌ **DO NOT modify** `src/plugins/v3_combined/` AT ALL
- ❌ **DO NOT modify** `ServiceAPI` methods used by V3
- ✅ **ONLY modify** `src/plugins/v6_price_action_*/`
- ✅ If ServiceAPI changes needed, make them **backward compatible**

**Fix List (From Audit):**

#### **V6 1H Plugin Fixes:**
1. **Risk Multiplier:** Change from 0.6x → 1.5x (Pine Script line reference?)
2. **Order Routing:** Change from ORDER_A_ONLY → DUAL_ORDERS
3. **ADX Check:** Implement ADX threshold check (ADX > 25 for entry)

#### **V6 15M Plugin Fixes:**
1. **Order Routing:** Change from ORDER_A_ONLY → DUAL_ORDERS
2. **ADX Check:** Implement ADX threshold check (ADX > 25 for entry)

#### **V6 1M Plugin Fixes:**
1. **Trend Pulse Integration:** Implement 5M trend alignment check (from docs)

**Implementation Steps:**

For EACH fix:
```python
# BEFORE (Example: 1H risk multiplier)
risk_multiplier = 0.6

# AFTER (Pine Script compliant)
risk_multiplier = 1.5  # Pine Script line X: "1H multiplier = 1.5-2.0x"
```

**Create Git Commits:**
```bash
git commit -m "fix(v6-1h): Correct risk multiplier to 1.5x (Pine Script compliance)"
git commit -m "fix(v6-1h): Add ORDER_B placement (DUAL_ORDERS routing)"
git commit -m "fix(v6-1h): Add ADX > 25 entry filter (Pine Script line Y)"
...
```

---

### **PHASE 3: V3 REGRESSION TEST (AFTER V6 FIX)**

**Purpose:** Prove V3 still works EXACTLY as before

**Tasks:**

1. **Run SAME V3 Test Signal:**
   ```bash
   python tests/live_activation/inject_v3_signal.py
   ```

2. **Capture V3 State After V6 Fix:**
   - Save logs: `logs/v3_after_v6_fix.log`
   - Save order details
   - Save database state

3. **Create Comparison Report:**
   ```markdown
   # V3 Regression Test Report
   
   ## Comparison (Before vs After V6 Fix)
   
   | Metric | BEFORE | AFTER | Status |
   |--------|--------|-------|--------|
   | Order A Ticket | #134976 | #[NEW] | ✅ (different ticket, same behavior) |
   | Order A Lot Size | 0.0050 | 0.0050 | ✅ SAME |
   | Order A SL | 1.09585 | 1.09585 | ✅ SAME |
   | Order A TP | 1.06872 | 1.06872 | ✅ SAME |
   | Order B Lot Size | 0.0050 | 0.0050 | ✅ SAME |
   | Order B SL | 1.28500 | 1.28500 | ✅ SAME |
   | Session Created | YES | YES | ✅ SAME |
   | Telegram Alert | YES | YES | ✅ SAME |
   
   ## Features Still Working
   - [x] Dual Order Split (50/50)
   - [x] Session Manager validation
   - [x] Risk calculation (UNCHANGED)
   - [x] Telegram notification
   
   ## VERDICT: V3 UNAFFECTED ✅
   ```

**Acceptance Criteria:**
- ✅ ALL V3 metrics must be IDENTICAL (except ticket numbers)
- ✅ NO errors in V3 logs
- ✅ V3 features still work 100%

**If ANY V3 feature breaks → REVERT V6 changes immediately.**

---

### **PHASE 4: V6 VERIFICATION (AFTER FIX)**

**Purpose:** Prove V6 is now 100% compliant

**Tasks:**

1. **Re-run V6 Compliance Tests:**
   ```bash
   python tests/v6_verification/test_v6_1m_compliance.py
   python tests/v6_verification/test_v6_5m_compliance.py
   python tests/v6_verification/test_v6_15m_compliance.py
   python tests/v6_verification/test_v6_1h_compliance.py
   ```

2. **Expected Results:**
   ```
   V6 1M Plugin: 100% Compliant ✅
   V6 5M Plugin: 100% Compliant ✅
   V6 15M Plugin: 100% Compliant ✅ (was 40%)
   V6 1H Plugin: 100% Compliant ✅ (was 30%)
   
   Overall: 100% Compliant
   ```

3. **Inject V6 Test Signals:**
   - Create `tests/live_activation/inject_v6_1h_signal.py`
   - Send test V6 1H signal
   - Verify:
     - DUAL orders placed (Order A + Order B)
     - Risk multiplier is 1.5x
     - ADX check passed

---

### **PHASE 5: ISOLATION PROOF**

**Purpose:** Prove V3 and V6 can run SIMULTANEOUSLY without conflict

**Tasks:**

1. **Start Bot**
2. **Send V3 Signal** → Verify V3 processes correctly
3. **Send V6 1H Signal** → Verify V6 processes correctly
4. **Check Database:**
   ```sql
   SELECT plugin_id, symbol, direction, lot_size, created_at 
   FROM trading_sessions 
   ORDER BY created_at DESC 
   LIMIT 10;
   ```
   
   **Expected:**
   ```
   | plugin_id | symbol | direction | lot_size | created_at |
   |-----------|--------|-----------|----------|------------|
   | v6_price_action_1h | EURUSD | BUY | 0.0075 | 2026-01-17 18:30:00 |
   | v3_combined | EURUSD | BUY | 0.0050 | 2026-01-17 18:25:00 |
   ```

5. **Verify NO Cross-Contamination:**
   - V3 sessions use `plugin_id='v3_combined'`
   - V6 sessions use `plugin_id='v6_price_action_1h'`
   - Different lot sizes (V3: 0.0050, V6: 0.0075 due to 1.5x multiplier)
   - Both coexist in database

**Isolation Checklist:**
- [ ] V3 and V6 use separate plugin instances
- [ ] V3 risk calculation NOT affected by V6 multiplier
- [ ] V3 order routing (always DUAL) NOT affected by V6 routing
- [ ] Database correctly isolates sessions by `plugin_id`
- [ ] Telegram notifications distinguish between V3 and V6

---

## 📊 DELIVERABLES (ALL MANDATORY)

1. **V3_BASELINE_REPORT.md** (V3 state before V6 fix)
2. **V6_FIX_CHANGELOG.md** (All V6 changes with Pine Script references)
3. **V3_REGRESSION_TEST_REPORT.md** (Proof V3 unchanged)
4. **V6_COMPLIANCE_RETEST_REPORT.md** (V6 now 100% compliant)
5. **ISOLATION_PROOF_REPORT.md** (V3 + V6 coexist without conflict)
6. **Git MR** with clean, documented commits

---

## 🚫 ACCEPTANCE CRITERIA

**V6 FIX is ACCEPTED only if:**
- ✅ V6 compliance: 100% (all 4 plugins)
- ✅ V3 regression test: PASS (100% unchanged)
- ✅ Isolation proof: PASS (V3 + V6 can run together)
- ✅ Zero cross-contamination

**If ANY criterion fails → REVERT and re-plan.**

---

## ⏱️ DEADLINE: 3 HOURS

**Start Time:** 2026-01-17 18:30  
**End Time:** 2026-01-17 21:30

---

## 📝 FINAL REPORT FORMAT

```markdown
# V6 Fix with V3 Protection - Final Report

## Executive Summary
- V6 Fixed: [YES/NO]
- V3 Protected: [YES/NO]
- Isolation Proven: [YES/NO]

## V6 Compliance (After Fix)
- 1M: [100%]
- 5M: [100%]
- 15M: [100%] (was 40%)
- 1H: [100%] (was 30%)

## V3 Regression Test
- All metrics: [SAME/DIFFERENT]
- Features: [WORKING/BROKEN]
- Verdict: [PASS/FAIL]

## Isolation Test
- V3 + V6 coexistence: [YES/NO]
- Cross-contamination: [NONE/DETECTED]

## Final Verdict
[APPROVED / REJECTED]
```

---

**REMEMBER:** V3 is **PRODUCTION-READY and WORKING**. Do NOT break it while fixing V6.

**IF IN DOUBT, ASK BEFORE TOUCHING SHARED CODE.** 🛡️
