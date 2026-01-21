# Test Report: 04_ANALYTICS_CAPABILITIES.md

**File Number**: 8/35
**Category**: main
**Test Date**: 2026-01-20 15:43:27

---

## 📊 Test Summary

- **Total Tests**: 9
- **Passed**: 9 ✅
- **Failed**: 0 ❌
- **Pass Rate**: 100.0%
- **Status**: ✅ PASSED

---

## 📋 Test Details

### ✅ PASS V6 Command: /v6_control

- **Search String**: `handle_v6_control`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS V6 Command: /v6_status

- **Search String**: `handle_v6_status`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS V6 Command: /tf1h_on

- **Search String**: `handle_tf1h_on`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS Analytics: /daily

- **Search String**: `handle_daily`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS Analytics: /weekly

- **Search String**: `handle_weekly`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS Analytics: /compare

- **Search String**: `handle_compare`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS Re-entry: /chains

- **Search String**: `handle_chains_status`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS Re-entry: /autonomous

- **Search String**: `handle_autonomous`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

### ✅ PASS Plugin: /plugin_status

- **Search String**: `handle_plugin_status`
- **Source File**: `src/telegram/bots/controller_bot.py`
- **Implemented**: Yes

---

## 🔍 File Analysis

**Keywords Found**:

- ✅ V6
- ✅ Analytics
- ✅ Re Entry
- ✅ Plugin
- ❌ Notification
- ✅ Command

---

*Report generated automatically by test_each_file.py*
