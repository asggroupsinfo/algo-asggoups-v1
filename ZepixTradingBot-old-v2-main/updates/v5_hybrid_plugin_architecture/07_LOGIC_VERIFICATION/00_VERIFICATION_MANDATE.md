# 🕵️‍♂️ MISSION: V3 & V6 LOGIC INTEGRITY & CONFLICT VERIFICATION

## 🔴 CRITICAL CONTEXT
The user demands a **"Logic Scanning Phase"**.
We must prove that:
1.  **V3 Implementation** matches the V3 Planning/Rules exactly.
2.  **V6 Implementation** matches the V6 Planning/Rules exactly.
3.  **NO CONFLICTS:** If V3 and V6 alerts arrive simultaneously, the system MUST handle them independently. No cross-talk.

## 📂 TRUTH SOURCES (The "Standard")

### V3 Logic (Legacy Combined)
- **Path:** `updates/v5_hybrid_plugin_architecture/COMBINED LOGICS/V3_FINAL_REPORTS/`
- **Key Files:**
  - `04_LOGIC_IMPLEMENTATION_COMPARISON.md` (Logic Rules)
  - `02_IMPLEMENTATION_VERIFICATION_REPORT.md` (Features)

### V6 Logic (Price Action)
- **Path:** `updates/v5_hybrid_plugin_architecture/V6_INTEGRATION_PROJECT/02_PLANNING PRICE ACTION LOGIC/`
- **Key Files:**
  - `01_INTEGRATION_MASTER_PLAN.md` (Architecture)
  - `02_PRICE_ACTION_LOGIC_1M.md` through `05_PRICE_ACTION_LOGIC_1H.md` (Timeframe specific rules)

## 🎯 YOUR TASK: DEEP SCAN & CROSS-EXAMINATION

### 1. V3 Integrity Check
- Compare `src/logic_plugins/v3_combined/` code against V3 Truth Source.
- **Verify:** Are ALL 12 signal types handled? Are the specific V3 Re-entry/Profit Booking rules active?

### 2. V6 Integrity Check
- Compare `src/logic_plugins/v6_price_action_*/` code against V6 Truth Source.
- **Verify:** Are the 4-Pillar Trend Validation checks present? Is the entry criteria matching the Pine Script plan?

### 3. The "Mixed Fire" Conflict Test (CRITICAL)
You must verify the **Router Logic** (`src/core/plugin_router.py` & `src/utils/signal_parser.py`).
- **Scenario:**
  1.  V3 Alert (`LOGIC1`) arrives.
  2.  V6 Alert (`PRICE_ACTION_1M`) arrives 1 second later.
- **Question:** Does V3 Alert go ONLY to V3 Plugin? Does V6 go ONLY to V6 Plugin?
- **Features Check:**
  - Does V3 trigger *V3 Smart SL*?
  - Does V6 trigger *V6 SL Logic* (if defined)?
  - Do they share or separate the "Daily Loss Limit"? (They should likely share the Autonomous System but have separate strategies).

## 🚀 EXECUTION PLAN
1.  **Read Truth Files:** Absorb the requirements from the paths above.
2.  **Scan Plugin Code:** Check `plugin.py`, `signal_handlers.py` in both plugin logic folders.
3.  **Analyze Routing:** detailed check of `process_alert` flow.
4.  **Report Generation:** Create `updates/v5_hybrid_plugin_architecture/07_LOGIC_VERIFICATION/01_LOGIC_INTEGRITY_REPORT.md`.

**The Report Must Answer:**
- "Does V3 match docs?" (Yes/No + Proof)
- "Does V6 match docs?" (Yes/No + Proof)
- "Conflict Test Result:" (Pass/Fail)

**START NOW.**
