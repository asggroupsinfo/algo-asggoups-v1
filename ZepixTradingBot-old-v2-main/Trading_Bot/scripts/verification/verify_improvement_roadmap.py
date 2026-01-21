"""
Improvement Roadmap Verification Script

This script verifies implementation status of:
Updates/telegram_updates/07_IMPROVEMENT_ROADMAP.md

Checks all 5 Phases:
- Phase 1: V6 Telegram Foundation
- Phase 2: Analytics & Reports
- Phase 3: Per-Plugin Configuration
- Phase 4: Enhanced Visuals & UX
- Phase 5: Testing & Validation
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

print_header("IMPROVEMENT ROADMAP VERIFICATION")

# Track results
phases = {}

# ============================================================================
# PHASE 1: V6 TELEGRAM FOUNDATION
# ============================================================================

print_header("PHASE 1: V6 TELEGRAM FOUNDATION (Week 1 - CRITICAL)")

results = []

# Task 1.1: V6 Control Menu Handler
results.append(check_file(
    "src/menu/v6_control_menu_handler.py",
    "Task 1.1: V6 Control Menu Handler"
))

# Task 1.2: V6 Commands
commands = [
    ('handle_v6_status', 'Task 1.2: /v6_status command'),
    ('handle_v6_control', 'Task 1.2: /v6_control command'),
    ('handle_tf15m', 'Task 1.2: /tf15m command'),
    ('handle_v6_performance', 'Task 1.2: /v6_performance command'),
]

for handler, desc in commands:
    results.append(check_in_file(
        "src/telegram/controller_bot.py",
        handler,
        desc
    ))

# Task 1.3 & 1.4: Notification Types & Routing
results.append(check_in_file(
    "src/telegram/notification_router.py",
    'V6_ENTRY',
    "Task 1.3: V6 NotificationTypes added"
))

# Task 1.5: V6 Plugins send notifications
v6_plugins = ['v6_price_action_1m', 'v6_price_action_5m', 'v6_price_action_15m', 'v6_price_action_1h']
for plugin in v6_plugins:
    results.append(check_in_file(
        f"src/logic_plugins/{plugin}/plugin.py",
        'on_trade_entry',
        f"Task 1.5: {plugin} sends notifications"
    ))

# Task 1.6: Fix broken V6 callback
results.append(check_in_file(
    "src/menu/menu_manager.py",
    'menu_v6',
    "Task 1.6: V6 callback fixed"
))

# Task 1.7: V6 in main menu
results.append(check_in_file(
    "src/menu/menu_manager.py",
    'V6 Control',
    "Task 1.7: V6 in main menu"
))

phases['phase1'] = {'passed': sum(results), 'total': len(results)}
print(f"\nPhase 1: {phases['phase1']['passed']}/{phases['phase1']['total']} ({phases['phase1']['passed']*100//phases['phase1']['total'] if phases['phase1']['total'] > 0 else 0}%)")

# ============================================================================
# PHASE 2: ANALYTICS & REPORTS
# ============================================================================

print_header("PHASE 2: ANALYTICS & REPORTS (Week 2 - HIGH)")

results = []

# Task 2.1: Analytics Menu Handler
results.append(check_file(
    "src/menu/analytics_menu_handler.py",
    "Task 2.1: Analytics Menu Handler"
))

# Task 2.2-2.6: Analytics Commands
analytics_commands = [
    ('handle_daily', 'Task 2.2: /daily report'),
    ('handle_weekly', 'Task 2.3: /weekly report'),
    ('handle_monthly', 'Task 2.4: /monthly report'),
    ('handle_compare', 'Task 2.5: /compare command'),
    ('handle_v6_performance', 'Task 2.6: /v6_performance (already checked)'),
]

for handler, desc in analytics_commands:
    results.append(check_in_file(
        "src/telegram/controller_bot.py",
        handler,
        desc
    ))

# Task 2.7: CSV Export
results.append(check_in_file(
    "src/telegram/controller_bot.py",
    'handle_export',
    "Task 2.7: /export command"
))

phases['phase2'] = {'passed': sum(results), 'total': len(results)}
print(f"\nPhase 2: {phases['phase2']['passed']}/{phases['phase2']['total']} ({phases['phase2']['passed']*100//phases['phase2']['total'] if phases['phase2']['total'] > 0 else 0}%)")

# ============================================================================
# PHASE 3: PER-PLUGIN CONFIGURATION
# ============================================================================

print_header("PHASE 3: PER-PLUGIN CONFIGURATION (Week 3 - MEDIUM-HIGH)")

results = []

# Task 3.1: Updated config structure
results.append(check_in_file(
    "config/config.json",
    'per_plugin',
    "Task 3.1: Per-plugin config structure"
))

# Task 3.2: Updated ReentryMenuHandler
results.append(check_file(
    "src/menu/reentry_menu_handler.py",
    "Task 3.2: ReentryMenuHandler exists"
))

if results[-1]:
    results.append(check_in_file(
        "src/menu/reentry_menu_handler.py",
        'show_plugin_reentry_config',
        "Task 3.2: Per-plugin reentry methods"
    ))

# Task 3.3: Per-plugin commands
per_plugin_commands = [
    ('reentry_v3', 'Task 3.3: /reentry_v3 command'),
    ('reentry_v6', 'Task 3.3: /reentry_v6 command'),
    ('v3_config', 'Task 3.3: /v3_config command'),
    ('v6_config', 'Task 3.3: /v6_config command'),
]

for cmd, desc in per_plugin_commands:
    results.append(check_in_file(
        "src/telegram/controller_bot.py",
        cmd,
        desc
    ))

phases['phase3'] = {'passed': sum(results), 'total': len(results)}
print(f"\nPhase 3: {phases['phase3']['passed']}/{phases['phase3']['total']} ({phases['phase3']['passed']*100//phases['phase3']['total'] if phases['phase3']['total'] > 0 else 0}%)")

# ============================================================================
# PHASE 4: ENHANCED VISUALS & UX
# ============================================================================

print_header("PHASE 4: ENHANCED VISUALS & UX (Week 3-4 - MEDIUM)")

results = []

# Task 4.1: Progress bars
results.append(check_in_file(
    "src/telegram/v6_notification_templates.py",
    'create_progress_bar',
    "Task 4.1: Progress bar function"
))

# Task 4.2: Inline keyboards in notifications
results.append(check_in_file(
    "src/telegram/v6_notification_templates.py",
    'create_inline_keyboard',
    "Task 4.2: Inline keyboard helpers"
))

# Task 4.3: Chat actions
results.append(check_in_file(
    "src/telegram/base_telegram_bot.py",
    'send_chat_action',
    "Task 4.3: Chat actions"
))

# Task 4.4: Optimized command list
results.append(check_in_file(
    "src/telegram/base_telegram_bot.py",
    'set_my_commands',
    "Task 4.4: Command list optimization"
))

# Task 4.5: Persistent keyboard
results.append(check_in_file(
    "src/telegram/base_telegram_bot.py",
    'ReplyKeyboardMarkup',
    "Task 4.5: Persistent keyboard support"
))

phases['phase4'] = {'passed': sum(results), 'total': len(results)}
print(f"\nPhase 4: {phases['phase4']['passed']}/{phases['phase4']['total']} ({phases['phase4']['passed']*100//phases['phase4']['total'] if phases['phase4']['total'] > 0 else 0}%)")

# ============================================================================
# PHASE 5: TESTING CHECKLIST
# ============================================================================

print_header("PHASE 5: TESTING & VALIDATION (Week 4 - CRITICAL)")

print("This phase requires manual testing after implementation.")
print("Automated verification not applicable.\n")

phases['phase5'] = {'passed': 0, 'total': 0}  # Manual testing

# ============================================================================
# FILES TO CREATE (NEW)
# ============================================================================

print_header("FILES TO CREATE - STATUS")

new_files = [
    ("src/menu/v6_control_menu_handler.py", "V6 Control Menu Handler"),
    ("src/menu/analytics_menu_handler.py", "Analytics Menu Handler"),
    ("src/telegram/v6_notification_templates.py", "V6 Notification Templates"),
]

new_file_results = []
for filepath, desc in new_files:
    new_file_results.append(check_file(filepath, desc))

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print_header("VERIFICATION SUMMARY")

# Calculate totals (excluding Phase 5 manual testing)
total_passed = sum(p['passed'] for p in [phases['phase1'], phases['phase2'], phases['phase3'], phases['phase4']])
total_checks = sum(p['total'] for p in [phases['phase1'], phases['phase2'], phases['phase3'], phases['phase4']])
overall_pct = (total_passed * 100 // total_checks) if total_checks > 0 else 0

for name, scores in phases.items():
    if scores['total'] > 0:
        pct = (scores['passed'] * 100 // scores['total'])
        status = "✓" if pct >= 90 else "⚠" if pct >= 70 else "❌"
        print(f"{status} {name.upper():.<30} {scores['passed']}/{scores['total']} ({pct}%)")
    else:
        print(f"⏭ {name.upper():.<30} MANUAL TESTING REQUIRED")

print(f"\n{'='*80}")
print(f"OVERALL IMPLEMENTATION STATUS: {total_passed}/{total_checks} ({overall_pct}%)")
print(f"{'='*80}\n")

if overall_pct >= 90:
    print("🎉 EXCELLENT! Roadmap nearly complete!")
elif overall_pct >= 70:
    print("⚠️ GOOD PROGRESS! Some phases need work.")
elif overall_pct >= 50:
    print("⚠️ MODERATE! Significant implementation needed.")
else:
    print("❌ CRITICAL! Major implementation required.")

print(f"\n📝 New Files Created: {sum(new_file_results)}/{len(new_file_results)}")
print(f"📊 Files to Modify: Multiple files across all phases\n")
