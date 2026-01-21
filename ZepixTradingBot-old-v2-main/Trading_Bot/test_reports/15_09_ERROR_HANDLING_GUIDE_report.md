# Test Report: 09_ERROR_HANDLING_GUIDE.md

**File Number**: 15/35
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

### ✅ PASS V6 Notification: send_v6_entry_alert

- **Search String**: `send_v6_entry_alert`
- **Source File**: `src/telegram/bots/notification_bot.py`
- **Implemented**: Yes

### ✅ PASS V6 Notification: send_v6_exit_alert

- **Search String**: `send_v6_exit_alert`
- **Source File**: `src/telegram/bots/notification_bot.py`
- **Implemented**: Yes

### ✅ PASS V6 Type: V6_ENTRY_1H

- **Search String**: `V6_ENTRY_1H`
- **Source File**: `src/telegram/notification_router.py`
- **Implemented**: Yes

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
- ❌ Analytics
- ✅ Re Entry
- ✅ Plugin
- ✅ Notification
- ✅ Command

---

*Report generated automatically by test_each_file.py*
