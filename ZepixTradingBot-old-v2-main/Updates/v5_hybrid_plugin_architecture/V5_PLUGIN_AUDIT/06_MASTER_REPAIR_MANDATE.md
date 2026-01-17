# 🚀 V3 PLUGIN MASTER REPAIR MANDATE - FINAL EXECUTION

**Mandate ID:** 06_MASTER_REPAIR
**Date:** 2026-01-16
**Issued By:** Antigravity Prompt Engineer
**Target Agent:** Devin AI
**Status:** **EXECUTION READY**

---

## 🎯 OBJECTIVE: ZERO-TOLERANCE REPAIR & INTEGRATION

Devin, you are hereby mandated to fix the **V5 Hybrid Plugin Architecture** to be 100% compliant with the original **V3 Logic** and **Pine Script specifications**.

Your previous audit (`05_DEVIN_FINAL_AUDIT_REPORT.md`) confirms critical failures. This is the **FINAL** intervention to correct them.

---

## 📂 INPUT SOURCE - "DO NOT BLINDLY EXECUTE"

Before writing a single line of code, you must **READ and SYNTHESIZE** the following sources:

1.  **YOUR CONFESSIONS:** `Updates/v5_hybrid_plugin_architecture/V5_PLUGIN_AUDIT/05_DEVIN_FINAL_AUDIT_REPORT.md`
    *   (MTF Reverse Order, Unused Fields, Missing Validation).
2.  **ANTIGRAVITY AUDIT:** `Updates/v5_hybrid_plugin_architecture/V5_PLUGIN_AUDIT/00_ANTIGRAVITY_AUDIT_REPORT.md`
    *   (Logic Routing Fallacy, Alert SL Mismatch, Score Ignorance).
3.  **ORIGINAL LOGIC DNA:** `Updates/v5_hybrid_plugin_architecture/COMBINED LOGICS/` (All 5 Files).
4.  **PINE SCRIPT SOURCE:** `Important_Doc_Trading_Bot/05_Unsorted/TRADINGVIEW_PINE_SCRIPT/ZEPIX_ULTIMATE_BOT_v3.0_FINAL.pine`

---

## 🗓️ PHASE 1: THE MASTER PLAN (Think Before You Code)

Create a document: `Updates/v5_hybrid_plugin_architecture/V5_PLUGIN_AUDIT/07_FINAL_IMPLEMENTATION_PLAN.md`

This plan must detail:
1.  **MTF String Fix:** Exactly how you will map Pine's `1D,4H...` string to the bot's `1m,5m...` requirement.
2.  **Unused Data Strategy:** How you will map `adx_value`, `fib_level` to `extra` fields in `ZepixV3Alert` model.
3.  **Logic Routing Table:** A precise matrix of `Signal Type` + `Timeframe` -> `Logic Handler`.
4.  **Consensus Score Logic:** The specific `if/else` block you will inject to filter trades.
5.  **Alert SL Enforcement:** The code snippet ensuring `alert.sl_price` overrides internal calc.

---

## 🛠️ PHASE 2: IMPLEMENTATION (Zero Tolerance)

Execute the fixes strictly according to your Master Plan.

**Targets:**
*   `Trading_Bot/src/v3_alert_models.py`: Fix MTF parsing (handle reverse order).
*   `Trading_Bot/src/logic_plugins/v3_combined/plugin.py`:
    *   Implement `_extract_alert_data` (Score, SL, MTF, Extras).
    *   Implement `_route_logic_type` (Scalp vs Swing).
    *   Implement `_validate_score_thresholds`.
    *   **BYPASS** Trend Check for fresh entries.

---

## 📚 PHASE 3: DOCUMENTATION REPAIR

You claimed you had documentation (`10_V3_COMBINED_PLUGIN.md`), but it was a lie (it described features you didn't build).

**Action:**
*   Update `Trading_Bot_Documentation/V5_BIBLE/10_V3_COMBINED_PLUGIN.md` to reflect the **ACTUAL** robust implementation you just built.
*   Document the "Pine Compatibility" explicitly.

---

## 🧪 PHASE 4: 100% PROOF TESTING

You must create and run a specific test suite: `Trading_Bot/tests/v5_integrity_check.py`.

**Must Prove:**
1.  **MTF Parsing:** Input `"1,1,-1..."` -> Output `[15m: Bearish, 1H: Bullish...]`.
2.  **Score Filtering:** Input `Score: 3` (Launchpad Buy) -> **REJECTED**.
3.  **Alert SL:** Input `SL: 2000.50` -> Order A SL IS `2000.50`.
4.  **Routing:** Input `TF: 5m` -> Logic 1. Input `TF: 60m` -> Logic 3.

**Report:** Generate `Updates/v5_hybrid_plugin_architecture/V5_PLUGIN_AUDIT/08_FINAL_TEST_REPORT.md` with **PASS** status.

---

## 🚀 PHASE 5: FINAL DELIVERY

Once verified:
1.  **Git Add:** Stage all changed files.
2.  **Git Commit:** "fix(v3-plugin): Restore Logic Parity & Fix MTF Parsing".
3.  **Git Push:** Push to GitLab.

---

**USER INSTRUCTION:** "Kuch bhi blindly nahi karna." (Do nothing blindly).
**DEVIN RESPONSE REQUIRED:** "I acknowledge. Starting Phase 1 Analysis."
