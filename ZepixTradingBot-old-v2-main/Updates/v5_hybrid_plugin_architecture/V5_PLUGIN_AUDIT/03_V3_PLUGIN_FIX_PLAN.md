# 🛠 V3 PLUGIN FIX EXECUTION PLAN

**Plan Date:** 2026-01-16
**Status:** **READY FOR EXECUTION**
**Target File:** `Trading_Bot/logic_plugins/v3_combined/plugin.py`

---

## 🎯 OBJECTIVE
Patch the V5 Plugin to **EXACTLY** replicate the User's V3 Logic (Score Filtering, Alert SL, Trend Bypass, Logic Routing) found in the old `trading_engine.py` and `alert_processor.py`.

---

## 📋 STEP-BY-STEP FIXES

### **STEP 1: ADD HELPER METHODS (Data Parsing & Routing)**

We need to add these methods to the `V3CombinedPlugin` class:

1.  `_extract_alert_data(self, alert)`:
    *   To robustly extract `sl`, `tp`, `score`, `mtf`, `multiplier` from the raw alert dict/object.

2.  `_route_logic_type(self, signal_type, timeframe)`:
    *   To determine if the trade is `LOGIC1` (Scalp), `LOGIC2` (Day), or `LOGIC3` (Swing).
    *   *Rule:* 5m = L1, 15m = L2, 60m+ = L3. `Screener` = L3.

### **STEP 2: REWRITE `process_entry_signal`**

We must completely overhaul the main entry method to:

1.  **Extract Data:** Use the helper from Step 1.
2.  **Validate Score:**
    *   Refuse if `score < min_score` (Default 5).
    *   Check signal specific thresholds (Launchpad >= 7).
3.  **Trend Check Bypass:**
    *   `if request_type == "entry_v3": bypass = True`.
    *   Only check trend if it's a legacy or re-entry signal.
4.  **Route Logic:**
    *   Determine `logic_type`.
5.  **Pass Data to Configs:**
    *   Pass the extracted `sl_price` to `_get_order_a_config`.

### **STEP 3: FIX `_get_order_a_config`**

**Current:** Recalculates SL.
**Fix:**
```python
def _get_order_a_config(..., defined_sl_price=None):
    if defined_sl_price:
        sl_price = defined_sl_price
    else:
        sl_price = self._calculate_sl_price(...)
```

### **STEP 4: FIX `_get_order_b_config`**

**Current:** Correctly uses fixed risk.
**Fix:** Add explicit logging to confirm: *"Ignoring V3 SL ({v3_sl}) in favor of Fixed Pyramid SL ({fixed_sl})"*

---

## 💻 CODE BLUEPRINT (PREVIEW)

### **New `process_entry_signal` Logic Flow:**

```python
async def process_entry_signal(self, alert) -> Dict[str, Any]:
    # 1. EXTRACT
    data = self._extract_alert_data(alert)
    
    # 2. SCORE VALIDATION
    if data['score'] < self.config['min_score']:
        return {"status": "rejected", "reason": "low_score"}
        
    # 3. TREND BYPASS (The Regression Fix)
    is_fresh_v3 = (data['signal_type'] not in ['legacy'])
    if not is_fresh_v3:
        # Only check trend for legacy/re-entries
        if not await self._check_v3_trend_alignment(...):
            return {"status": "skipped", "reason": "trend_mismatch"}
            
    # 4. ROUTING
    logic_type = self._route_logic_type(data['signal_type'], data['tf'])
    
    # 5. LOT CALC (With V3 Multiplier)
    # Must apply: Base * V3_Mult * Logic_Mult
    lot_size = await self.service_api.calculate_v3_lot_size(
        ..., 
        v3_multiplier=data['multiplier'], 
        logic_type=logic_type
    )

    # 6. CONFIG ORDER A (With Alert SL)
    order_a = self._get_order_a_config(..., defined_sl_price=data['sl'])
    
    # ... Place Orders ...
```

---

## 🛡 VERIFICATION CHECKLIST (Post-Fix)

After applying the code, we will run the `tests/bible_suite/ultimate_bible_test.py` to ensure:
1.  **Fresh Entry:** Doesn't trigger Trend Manager.
2.  **Order A:** Has exact SL from "Alert".
3.  **Order B:** Has Fixed Risk SL.
4.  **Low Score Alert:** Is rejected.

---

**Next Action:**
The user just needs to give the command to **"APPLY FIX"** and this plan will be converted into actual code changes in `plugin.py`.
