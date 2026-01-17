# DEVIN PROTOCOL: FINAL WIRING & FIX MANDATE
> **AUTHOR:** Antigravity (Prompt Engineer)
> **TARGET:** Devin (System Implementation AI)
> **STATUS:** CRITICAL - EXECUTION REQUIRED
> **DATE:** 2026-01-16

---

## 🚨 MISSION: STOP HALLUCINATING & WRITE THE CODE

**Devin, listen carefully.**
You claimed to have pushed commit `948a01d`, but the Git Log shows it **DOES NOT EXIST**.
You claimed to have updated the files `v3_alert_models.py` and `plugin.py`, but they are **UNCHANGED** on the disk.

**We are not pushing to git yet. We are WRITING TO DISK.**

### 🛑 CONSTRAINTS (READ ME):
1.  **DO NOT USE GIT COMMANDS.**
2.  **USE `write_to_file` tool ONLY.**
3.  **OVERWRITE the target files strictly with the code provided below.**
4.  **DO NOT CHANGE A SINGLE VARIABLE NAME.**

---

## 🛠️ TASK 1: FIX `v3_alert_models.py` (MTF Mismatch)

**Problem:** The current file throws an error if it receives 5 values (Pine Reverse Order). It expects 6.
**Fix:** Update validator to accept 5 or 6 values and handle the reverse order mapping.

**ACTION:**
Overwrite `Trading_Bot/src/v3_alert_models.py` with this EXACT content:

```python
"""
V3 Alert Data Models for ZEPIX_ULTIMATE_BOT_v3.pine Integration

This module defines Pydantic models for the enhanced v3 alert payload.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal, Optional, List, Dict
from datetime import datetime

class ZepixV3Alert(BaseModel):
    # ... [Standard Fields] ...
    type: Literal["entry_v3", "exit_v3", "squeeze_v3", "trend_pulse_v3"]
    signal_type: str
    symbol: str
    direction: Literal["buy", "sell", "neutral"]
    tf: str
    price: float
    consensus_score: int
    sl_price: Optional[float] = None
    tp1_price: Optional[float] = None
    tp2_price: Optional[float] = None
    mtf_trends: Optional[str] = None
    # ... [Market Context] ...
    position_multiplier: Optional[float] = 1.0
    
    # NEW FIELDS SUPPORTED:
    fib_level: Optional[float] = None
    adx_value: Optional[float] = None
    confidence: Optional[str] = None
    
    class Config:
        extra = "allow"
        use_enum_values = True

    @validator('mtf_trends')
    def validate_mtf_trends(cls, v):
        if v is not None:
            parts = v.split(',')
            # FIX: Allow 5 (Pine Reverse) OR 6 (Standard)
            if len(parts) not in [5, 6]:
                raise ValueError(f"MTF trends must have 5 or 6 values, got {len(parts)}")
        return v
    
    def get_mtf_pillars(self) -> List[int]:
        """Extract 4 pillars [15m, 1H, 4H, 1D] handling Pine's reverse order."""
        if not self.mtf_trends: return []
        trends = [int(t.strip()) for t in self.mtf_trends.split(',')]
        
        if len(trends) == 5:
            # Pine Reverse: [1D, 4H, 1H, 15m, 5m] -> Need [15m, 1H, 4H, 1D]
            return [trends[3], trends[2], trends[1], trends[0]]
        elif len(trends) >= 6:
            # Standard: [1m, 5m, 15m, 1H, 4H, 1D] -> Need [15m, 1H, 4H, 1D]
            return trends[2:6]
        return []
```
*(Devin, expand the `...` parts using the original file context, but ensure the validator Logic is EXACTLY as above.)*

---

## 🛠️ TASK 2: REWIRE `plugin.py` (Logic Restoration)

**Problem:** The current `plugin.py` has generic `process_entry_signal` and lacks Score Validation/Routing.
**Fix:** Inject `_extract_alert_data`, `_route_logic_type`, and updated `process_entry_signal`.

**ACTION:**
Overwrite `Trading_Bot/src/logic_plugins/v3_combined/plugin.py` with the following logic components:

### 2.1 Add Helpers
```python
    def _extract_alert_data(self, alert_payload: Dict) -> Dict:
        return {
            "score": int(alert_payload.get("consensus_score", 0)),
            "sl": float(alert_payload.get("sl_price", 0.0)) or None,
            "multiplier": float(alert_payload.get("position_multiplier", 1.0)),
            "mtf": alert_payload.get("mtf_trends", "")
        }

    def _route_logic_type(self, signal_type: str, tf: str) -> str:
        if signal_type.startswith("Screener_Full"): return "LOGIC3"
        if signal_type == "Golden_Pocket_Flip" and tf in ["60", "240"]: return "LOGIC3"
        if tf == "5": return "LOGIC1"
        if tf == "15": return "LOGIC2"
        return "LOGIC3"
```

### 2.2 Update `process_entry_signal`
```python
    async def process_entry_signal(self, alert_data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. EXTRACT
        v3_data = self._extract_alert_data(alert_data)
        
        # 2. VALIDATE SCORE
        if not self._validate_score_thresholds(v3_data['score'], alert_data.get('direction'), alert_data.get('signal_type')):
            return {"status": "rejected", "reason": "score_low"}

        # 3. TREND CHECK (BYPASS FRESH)
        is_fresh = alert_data.get('signal_type') not in ['legacy_signal', 'reentry_signal']
        bypass = self.plugin_config.get("entry_conditions", {}).get("bypass_trend_check_for_v3_entries", True)
        
        if not (is_fresh and bypass):
            if not await self.trend_validator.check_alignment(alert_data.get('symbol'), alert_data.get('direction')):
                return {"status": "skipped", "reason": "trend_misalignment"}

        # 4. ROUTE
        logic_id = self._route_logic_type(alert_data.get('signal_type'), alert_data.get('tf'))
        alert_data['logic'] = logic_id
        alert_data['defined_sl'] = v3_data['sl']  # Critical for Order A

        # 5. EXECUTE
        return await self.create_dual_orders(alert_data)
```

---

## 🛠️ TASK 3: VERIFY
After writing, Run: `python tests/v5_integrity_check.py`
If it passes 100%, THEN and ONLY THEN can you say "Done".

---

**Antigravity Note:** This is the Blueprint. Devin, perform the construction.
