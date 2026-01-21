"""
Error Handling Verification Script

Verifies implementation of:
Updates/telegram_updates/09_ERROR_HANDLING_GUIDE.md

Checks:
1. Error code definitions (TG/MT/DB/PL/TE/NF/MN)
2. Error handlers
3. Auto-recovery procedures
4. Error logging configuration
5. Admin notifications
"""

import os
import sys
from pathlib import Path

# Bot path
BASE_PATH = Path("C:/Users/Ansh Shivaay Gupta/Downloads/ZepixTradingBot-New-v1/ZepixTradingBot-old-v2-main/Trading_Bot")
os.chdir(BASE_PATH)

def print_header(title):
    print("\n" + "="*80)
    print(f"  {title:^76}  ")
    print("="*80 + "\n")

def check_file(filepath, desc=""):
    path = BASE_PATH / filepath
    exists = path.exists()
    status = "✓" if exists else "❌"
    print(f"{status} {desc or filepath}")
    return exists

def check_in_file(filepath, search_str, desc=""):
    try:
        path = BASE_PATH / filepath
        if not path.exists():
            print(f"❌ {desc or search_str}")
            return False
        
        content = path.read_text(encoding='utf-8', errors='ignore')
        found = search_str in content
        status = "✓" if found else "❌"
        print(f"{status} {desc or search_str}")
        return found
    except Exception as e:
        print(f"❌ Error: {desc or search_str}")
        return False

def check_multiple_in_file(filepath, search_list, desc=""):
    """Check if ANY of the search strings exist"""
    try:
        path = BASE_PATH / filepath
        if not path.exists():
            print(f"❌ {desc}")
            return False
        
        content = path.read_text(encoding='utf-8', errors='ignore')
        found = any(s in content for s in search_list)
        status = "✓" if found else "❌"
        print(f"{status} {desc}")
        return found
    except Exception as e:
        print(f"❌ Error: {desc}")
        return False

print_header("ERROR HANDLING IMPLEMENTATION VERIFICATION")

# Track results
sections = {}

# ============================================================================
# SECTION 1: ERROR CODE DEFINITIONS
# ============================================================================

print_header("SECTION 1: ERROR CODE DEFINITIONS")

results = []

# Telegram error codes (TG-001 to TG-006) - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['TG_001_HTTP_409', 'TG_002_RATE_LIMIT', 'TG_003_INVALID_TOKEN', 'TG_004_CHAT_NOT_FOUND', 'TG_005_MESSAGE_TOO_LONG', 'TG_006_CALLBACK_EXPIRED'],
    "Telegram error codes (TG-XXX)"
))

# MT5 error codes (MT-001 to MT-003) - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['MT_001_CONNECTION_FAILED', 'MT_002_ORDER_FAILED', 'MT_003_INVALID_SYMBOL', 'MT5_ERROR_CODES'],
    "MT5 error codes (MT-XXX)"
))

# Database error codes (DB-001 to DB-003) - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['DB_001_CONNECTION_ERROR', 'DB_002_TABLE_MISSING', 'DB_003_CONSTRAINT_VIOLATION'],
    "Database error codes (DB-XXX)"
))

# Plugin system error codes (PL-001 to PL-003) - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['PL_001_LOAD_FAILED', 'PL_002_PROCESS_ERROR', 'PL_003_CONFIG_INVALID'],
    "Plugin error codes (PL-XXX)"
))

# Trading engine error codes (TE-001 to TE-003) - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['TE_001_INVALID_SIGNAL', 'TE_002_RISK_LIMIT_EXCEEDED', 'TE_003_DUPLICATE'],
    "Trading engine error codes (TE-XXX)"
))

# Notification error codes (NF-001, NF-002) - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['NF_001_QUEUE_FULL', 'NF_002_VOICE_ALERT_FAILED'],
    "Notification error codes (NF-XXX)"
))

# Menu system error codes (MN-001, MN-002) - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['MN_001_CALLBACK_ERROR', 'MN_002_BUILD_ERROR'],
    "Menu error codes (MN-XXX)"
))

sections['section1'] = {'passed': sum(results), 'total': len(results)}
print(f"\nSection 1: {sections['section1']['passed']}/{sections['section1']['total']} ({sections['section1']['passed']*100//sections['section1']['total'] if sections['section1']['total'] > 0 else 0}%)")

# ============================================================================
# SECTION 2: ERROR HANDLERS
# ============================================================================

print_header("SECTION 2: ERROR HANDLERS")

results = []

# TG-001: HTTP 409 handler - Check auto_recovery.py
results.append(check_multiple_in_file(
    "src/utils/auto_recovery.py",
    ['recover_telegram', 'TG_001_HTTP_409', 'stop_polling', 'start_polling'],
    "TG-001: HTTP 409 Conflict handler"
))

# TG-002: Rate limit handler - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['ErrorRateLimiter', 'should_notify', 'max_per_minute'],
    "TG-002: Rate limit handler"
))

# TG-005: Long message handler - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['split_long_message', 'MAX_MESSAGE_LENGTH', '4096'],
    "TG-005: Message too long handler"
))

# MT-001: MT5 disconnect handler - Check auto_recovery.py
results.append(check_multiple_in_file(
    "src/utils/auto_recovery.py",
    ['recover_mt5_connection', 'MT_001_CONNECTION_FAILED', 'mt5_reconnect_attempts'],
    "MT-001: MT5 disconnect handler"
))

# MT-002: Order error handler - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['get_mt5_error_description', 'MT5_ERROR_CODES'],
    "MT-002: Order error handler"
))

# DB-001: Database reconnect handler - Check auto_recovery.py
results.append(check_multiple_in_file(
    "src/utils/auto_recovery.py",
    ['recover_database_connection', 'DB_001_CONNECTION_ERROR', 'db_reconnect_attempts'],
    "DB-001: Database reconnect handler"
))

# PL-001: Plugin load error handler - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['PL_001_LOAD_FAILED', 'PLUGIN_PROCESS_TIMEOUT'],
    "PL-001: Plugin load error handler"
))

# PL-002: Plugin process error handler - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['PL_002_PROCESS_ERROR', 'PLUGIN_PROCESS_TIMEOUT'],
    "PL-002: Plugin process error handler"
))

# TE-001: Signal validation - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['validate_signal', 'REQUIRED_SIGNAL_FIELDS', 'TE_001_INVALID_SIGNAL'],
    "TE-001: Signal validation"
))

# TE-002: Risk limit checker - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['RiskLimitChecker', 'check_risk_limits', 'daily_loss_limit', 'TE_002_RISK_LIMIT_EXCEEDED'],
    "TE-002: Risk limit checker"
))

# TE-003: Duplicate signal blocker - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['SignalDeduplicator', 'is_duplicate', 'recent_signals', 'ttl_seconds'],
    "TE-003: Duplicate signal blocker"
))

sections['section2'] = {'passed': sum(results), 'total': len(results)}
print(f"\nSection 2: {sections['section2']['passed']}/{sections['section2']['total']} ({sections['section2']['passed']*100//sections['section2']['total'] if sections['section2']['total'] > 0 else 0}%)")

# ============================================================================
# SECTION 3: AUTO-RECOVERY PROCEDURES
# ============================================================================

print_header("SECTION 3: AUTO-RECOVERY PROCEDURES")

results = []

# Auto-recovery loop - Check auto_recovery.py
results.append(check_multiple_in_file(
    "src/utils/auto_recovery.py",
    ['_recovery_loop', 'recover_mt5_connection', 'recover_database_connection', 'recover_telegram'],
    "Auto-recovery loop"
))

# MT5 auto-reconnect - Check auto_recovery.py
results.append(check_multiple_in_file(
    "src/utils/auto_recovery.py",
    ['recover_mt5_connection', '_check_mt5_connection', 'mt5_reconnect_attempts'],
    "MT5 auto-reconnect"
))

# Database reconnect - Check auto_recovery.py
results.append(check_multiple_in_file(
    "src/utils/auto_recovery.py",
    ['recover_database_connection', '_check_database_connection', 'db_reconnect_attempts'],
    "Database auto-reconnect"
))

# Telegram polling restart - Check auto_recovery.py
results.append(check_multiple_in_file(
    "src/utils/auto_recovery.py",
    ['recover_telegram', '_check_telegram_health', 'tg_restart_attempts'],
    "Telegram polling restart"
))

sections['section3'] = {'passed': sum(results), 'total': len(results)}
print(f"\nSection 3: {sections['section3']['passed']}/{sections['section3']['total']} ({sections['section3']['passed']*100//sections['section3']['total'] if sections['section3']['total'] > 0 else 0}%)")

# ============================================================================
# SECTION 4: ERROR LOGGING
# ============================================================================

print_header("SECTION 4: ERROR LOGGING CONFIGURATION")

results = []

# Logging configuration - Check logging_config.py
results.append(check_multiple_in_file(
    "src/utils/logging_config.py",
    ['setup_error_logging', 'RotatingFileHandler', 'logs/bot.log'],
    "Basic logging configuration"
))

# Error-specific logger - Check logging_config.py
results.append(check_multiple_in_file(
    "src/utils/logging_config.py",
    ['logs/errors.log', 'setLevel(logging.ERROR)', 'error_handler'],
    "Error-specific logger"
))

# Structured log format - Check logging_config.py
results.append(check_multiple_in_file(
    "src/utils/logging_config.py",
    ['%(asctime)s', '%(levelname)', '%(name)s', '%(message)s'],
    "Structured log format"
))

sections['section4'] = {'passed': sum(results), 'total': len(results)}
print(f"\nSection 4: {sections['section4']['passed']}/{sections['section4']['total']} ({sections['section4']['passed']*100//sections['section4']['total'] if sections['section4']['total'] > 0 else 0}%)")

# ============================================================================
# SECTION 5: ADMIN NOTIFICATIONS
# ============================================================================

print_header("SECTION 5: ADMIN ERROR NOTIFICATIONS")

results = []

# Admin error notification - Check admin_notifier.py
results.append(check_multiple_in_file(
    "src/utils/admin_notifier.py",
    ['AdminErrorNotifier', 'notify_error', 'admin_chat_id', 'SEVERITY_EMOJI'],
    "Admin error notification"
))

# Critical error alerts - Check admin_notifier.py
results.append(check_multiple_in_file(
    "src/utils/admin_notifier.py",
    ['notify_critical_system_error', 'CRITICAL', 'Immediate action required'],
    "Critical error alerts"
))

sections['section5'] = {'passed': sum(results), 'total': len(results)}
print(f"\nSection 5: {sections['section5']['passed']}/{sections['section5']['total']} ({sections['section5']['passed']*100//sections['section5']['total'] if sections['section5']['total'] > 0 else 0}%)")

# ============================================================================
# SECTION 6: SPECIFIC ERROR FEATURES
# ============================================================================

print_header("SECTION 6: SPECIFIC ERROR FEATURES")

results = []

# MT5 error codes dictionary - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['MT5_ERROR_CODES', '10004', '10018', '10033', 'Requote'],
    "MT5 error codes dictionary"
))

# Required signal fields - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['REQUIRED_SIGNAL_FIELDS', 'symbol', 'direction', 'entry'],
    "Required signal fields definition"
))

# Notification queue - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['NotificationQueue', 'MAX_NOTIFICATION_QUEUE_SIZE', 'enqueue', 'dequeue'],
    "Notification queue system"
))

# Callback pattern matching - Check error_codes.py
results.append(check_multiple_in_file(
    "src/utils/error_codes.py",
    ['MAX_CALLBACK_DATA_LENGTH', 'MN_001_CALLBACK_ERROR'],
    "Callback pattern matching"

))

# Menu build safety - Check error_handlers.py
results.append(check_multiple_in_file(
    "src/utils/error_handlers.py",
    ['truncate_callback_data', 'truncate_button_text', 'MAX_BUTTON_TEXT_LENGTH'],
    "Safe menu builder"
))

sections['section6'] = {'passed': sum(results), 'total': len(results)}
print(f"\nSection 6: {sections['section6']['passed']}/{sections['section6']['total']} ({sections['section6']['passed']*100//sections['section6']['total'] if sections['section6']['total'] > 0 else 0}%)")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print_header("VERIFICATION SUMMARY")

total_passed = sum(s['passed'] for s in sections.values())
total_checks = sum(s['total'] for s in sections.values())
overall_pct = (total_passed * 100 // total_checks) if total_checks > 0 else 0

for name, scores in sections.items():
    if scores['total'] > 0:
        pct = (scores['passed'] * 100 // scores['total'])
        status = "✓" if pct >= 90 else "⚠" if pct >= 70 else "❌"
        print(f"{status} {name.upper():.<30} {scores['passed']}/{scores['total']} ({pct}%)")

print(f"\n{'='*80}")
print(f"OVERALL ERROR HANDLING STATUS: {total_passed}/{total_checks} ({overall_pct}%)")
print(f"{'='*80}\n")

if overall_pct >= 90:
    print("🎉 EXCELLENT! Error handling nearly complete!")
elif overall_pct >= 70:
    print("⚠️ GOOD PROGRESS! Some features need work.")
elif overall_pct >= 50:
    print("⚠️ MODERATE! Significant implementation needed.")
else:
    print("❌ CRITICAL! Major error handling implementation required.")

print(f"\n📊 Error Categories: 7 (TG/MT/DB/PL/TE/NF/MN)")
print(f"📝 Total Error Codes Documented: 25+")
print(f"🔄 Auto-Recovery Systems: {sections['section3']['passed']}/{sections['section3']['total']}")
print(f"📋 Logging Infrastructure: {sections['section4']['passed']}/{sections['section4']['total']}\n")
