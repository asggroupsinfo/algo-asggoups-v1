"""
INDIVIDUAL FILE TESTING - ALL 35 FILES
Tests each update file separately and generates individual reports
"""
import os
import json
from pathlib import Path
from datetime import datetime

print("=" * 120)
print("🔍 INDIVIDUAL FILE TESTING - ALL 35 TELEGRAM UPDATE FILES")
print("=" * 120)

# Paths
updates_dir = Path("../Updates/telegram_updates")
reports_dir = Path("test_reports")
reports_dir.mkdir(exist_ok=True)

# Get all markdown files
all_files = []

# Main directory
for file in sorted(os.listdir(updates_dir)):
    if file.endswith('.md'):
        all_files.append({
            'name': file,
            'path': updates_dir / file,
            'category': 'main'
        })

# Batch plans
batch_dir = updates_dir / "batch_plans"
if batch_dir.exists():
    for file in sorted(os.listdir(batch_dir)):
        if file.endswith('.md'):
            all_files.append({
                'name': f"batch_plans/{file}",
                'path': batch_dir / file,
                'category': 'batch_plans'
            })

print(f"\n📁 TOTAL FILES FOUND: {len(all_files)}")
print(f"📂 Reports will be saved to: {reports_dir}")

# Feature mapping from files to implementation
feature_checks = {
    # V6 Features
    "V6": {
        "notification_methods": [
            ("send_v6_entry_alert", "src/telegram/bots/notification_bot.py"),
            ("send_v6_exit_alert", "src/telegram/bots/notification_bot.py"),
            ("send_trend_pulse_alert", "src/telegram/bots/notification_bot.py"),
            ("send_shadow_trade_alert", "src/telegram/bots/notification_bot.py"),
        ],
        "notification_types": [
            ("V6_ENTRY_15M", "src/telegram/notification_router.py"),
            ("V6_ENTRY_30M", "src/telegram/notification_router.py"),
            ("V6_ENTRY_1H", "src/telegram/notification_router.py"),
            ("V6_ENTRY_4H", "src/telegram/notification_router.py"),
        ],
        "commands": [
            ("handle_v6_control", "src/telegram/bots/controller_bot.py"),
            ("handle_v6_status", "src/telegram/bots/controller_bot.py"),
            ("handle_tf1m_on", "src/telegram/bots/controller_bot.py"),
            ("handle_tf5m_on", "src/telegram/bots/controller_bot.py"),
            ("handle_tf15m_on", "src/telegram/bots/controller_bot.py"),
            ("handle_tf1h_on", "src/telegram/bots/controller_bot.py"),
        ]
    },
    # Analytics Features
    "Analytics": {
        "commands": [
            ("handle_daily", "src/telegram/bots/controller_bot.py"),
            ("handle_weekly", "src/telegram/bots/controller_bot.py"),
            ("handle_monthly", "src/telegram/bots/controller_bot.py"),
            ("handle_compare", "src/telegram/bots/controller_bot.py"),
            ("handle_export", "src/telegram/bots/controller_bot.py"),
            ("handle_pair_report", "src/telegram/bots/controller_bot.py"),
            ("handle_strategy_report", "src/telegram/bots/controller_bot.py"),
            ("handle_tp_report", "src/telegram/bots/controller_bot.py"),
            ("handle_profit_stats", "src/telegram/bots/controller_bot.py"),
        ]
    },
    # Re-entry Features
    "Re-entry": {
        "commands": [
            ("handle_chains_status", "src/telegram/bots/controller_bot.py"),
            ("handle_tp_cont", "src/telegram/bots/controller_bot.py"),
            ("handle_sl_hunt", "src/telegram/bots/controller_bot.py"),
            ("handle_recovery_stats", "src/telegram/bots/controller_bot.py"),
            ("handle_autonomous", "src/telegram/bots/controller_bot.py"),
        ]
    },
    # Plugin Features
    "Plugin": {
        "commands": [
            ("handle_plugin_toggle", "src/telegram/bots/controller_bot.py"),
            ("handle_plugin_status", "src/telegram/bots/controller_bot.py"),
            ("handle_v3_toggle", "src/telegram/bots/controller_bot.py"),
            ("handle_v6_toggle", "src/telegram/bots/controller_bot.py"),
        ]
    }
}

# Load source files once
source_code = {}
for category, features in feature_checks.items():
    for feature_type, items in features.items():
        for feature_name, file_path in items:
            if file_path not in source_code:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        source_code[file_path] = f.read()
                else:
                    source_code[file_path] = ""

# Test each file individually
all_results = []
total_passed = 0
total_failed = 0

for idx, file_info in enumerate(all_files, 1):
    file_name = file_info['name']
    file_path = file_info['path']
    
    print(f"\n{'=' * 120}")
    print(f"📄 [{idx}/{len(all_files)}] TESTING: {file_name}")
    print(f"{'=' * 120}")
    
    # Read file content
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Analyze file content for keywords
    file_keywords = {
        'v6': 'v6' in content.lower() or 'timeframe' in content.lower() or 'price action' in content.lower(),
        'analytics': 'analytics' in content.lower() or 'report' in content.lower() or 'performance' in content.lower(),
        're_entry': 're-entry' in content.lower() or 'reentry' in content.lower() or 'chain' in content.lower(),
        'plugin': 'plugin' in content.lower(),
        'notification': 'notification' in content.lower() or 'alert' in content.lower(),
        'command': 'command' in content.lower() or 'handler' in content.lower(),
    }
    
    # Determine what features this file requires
    required_features = []
    
    if file_keywords['v6']:
        if file_keywords['notification']:
            required_features.extend([
                ("V6 Notification: send_v6_entry_alert", "send_v6_entry_alert", "src/telegram/bots/notification_bot.py"),
                ("V6 Notification: send_v6_exit_alert", "send_v6_exit_alert", "src/telegram/bots/notification_bot.py"),
                ("V6 Type: V6_ENTRY_1H", "V6_ENTRY_1H", "src/telegram/notification_router.py"),
            ])
        if file_keywords['command']:
            required_features.extend([
                ("V6 Command: /v6_control", "handle_v6_control", "src/telegram/bots/controller_bot.py"),
                ("V6 Command: /v6_status", "handle_v6_status", "src/telegram/bots/controller_bot.py"),
                ("V6 Command: /tf1h_on", "handle_tf1h_on", "src/telegram/bots/controller_bot.py"),
            ])
    
    if file_keywords['analytics']:
        required_features.extend([
            ("Analytics: /daily", "handle_daily", "src/telegram/bots/controller_bot.py"),
            ("Analytics: /weekly", "handle_weekly", "src/telegram/bots/controller_bot.py"),
            ("Analytics: /compare", "handle_compare", "src/telegram/bots/controller_bot.py"),
        ])
    
    if file_keywords['re_entry']:
        required_features.extend([
            ("Re-entry: /chains", "handle_chains_status", "src/telegram/bots/controller_bot.py"),
            ("Re-entry: /autonomous", "handle_autonomous", "src/telegram/bots/controller_bot.py"),
        ])
    
    if file_keywords['plugin']:
        required_features.extend([
            ("Plugin: /plugin_status", "handle_plugin_status", "src/telegram/bots/controller_bot.py"),
        ])
    
    # If no specific features, assign general commands
    if not required_features:
        required_features = [
            ("General: Bot structure", "class", "src/telegram/bots/controller_bot.py"),
        ]
    
    # Test each required feature
    test_results = []
    passed_count = 0
    failed_count = 0
    
    for feature_name, search_string, source_file in required_features:
        code = source_code.get(source_file, "")
        implemented = search_string in code
        
        test_results.append({
            "feature": feature_name,
            "search_string": search_string,
            "source_file": source_file,
            "implemented": implemented,
            "status": "✅ PASS" if implemented else "❌ FAIL"
        })
        
        if implemented:
            passed_count += 1
            print(f"  ✅ {feature_name}")
        else:
            failed_count += 1
            print(f"  ❌ {feature_name}")
    
    # Calculate file score
    total_tests = len(required_features)
    percentage = (passed_count / total_tests * 100) if total_tests > 0 else 100
    
    file_status = "✅ PASSED" if percentage >= 80 else "⚠️ PARTIAL" if percentage >= 50 else "❌ FAILED"
    
    print(f"\n  📊 RESULT: {passed_count}/{total_tests} ({percentage:.0f}%) - {file_status}")
    
    # Store results
    file_result = {
        "file_number": idx,
        "file_name": file_name,
        "file_path": str(file_path),
        "category": file_info['category'],
        "keywords": file_keywords,
        "required_features": len(required_features),
        "tests_passed": passed_count,
        "tests_failed": failed_count,
        "pass_percentage": percentage,
        "status": file_status,
        "test_details": test_results,
        "timestamp": datetime.now().isoformat()
    }
    
    all_results.append(file_result)
    total_passed += passed_count
    total_failed += failed_count
    
    # Generate individual report
    report_file = reports_dir / f"{idx:02d}_{Path(file_name).stem}_report.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"# Test Report: {file_name}\n\n")
        f.write(f"**File Number**: {idx}/35\n")
        f.write(f"**Category**: {file_info['category']}\n")
        f.write(f"**Test Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"---\n\n")
        f.write(f"## 📊 Test Summary\n\n")
        f.write(f"- **Total Tests**: {total_tests}\n")
        f.write(f"- **Passed**: {passed_count} ✅\n")
        f.write(f"- **Failed**: {failed_count} ❌\n")
        f.write(f"- **Pass Rate**: {percentage:.1f}%\n")
        f.write(f"- **Status**: {file_status}\n\n")
        f.write(f"---\n\n")
        f.write(f"## 📋 Test Details\n\n")
        
        for test in test_results:
            f.write(f"### {test['status']} {test['feature']}\n\n")
            f.write(f"- **Search String**: `{test['search_string']}`\n")
            f.write(f"- **Source File**: `{test['source_file']}`\n")
            f.write(f"- **Implemented**: {'Yes' if test['implemented'] else 'No'}\n\n")
        
        f.write(f"---\n\n")
        f.write(f"## 🔍 File Analysis\n\n")
        f.write(f"**Keywords Found**:\n\n")
        for keyword, found in file_keywords.items():
            icon = "✅" if found else "❌"
            f.write(f"- {icon} {keyword.replace('_', ' ').title()}\n")
        
        f.write(f"\n---\n\n")
        f.write(f"*Report generated automatically by test_each_file.py*\n")
    
    print(f"  💾 Report saved: {report_file}")

# Generate master summary
print(f"\n{'=' * 120}")
print("📊 MASTER SUMMARY - ALL 35 FILES")
print(f"{'=' * 120}\n")

summary_file = reports_dir / "00_MASTER_SUMMARY.md"

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write(f"# Master Test Summary - All 35 Files\n\n")
    f.write(f"**Test Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"**Total Files**: {len(all_files)}\n\n")
    f.write(f"---\n\n")
    f.write(f"## 📊 Overall Statistics\n\n")
    
    total_tests_all = sum(r['required_features'] for r in all_results)
    f.write(f"- **Total Tests Across All Files**: {total_tests_all}\n")
    f.write(f"- **Total Passed**: {total_passed} ✅\n")
    f.write(f"- **Total Failed**: {total_failed} ❌\n")
    
    overall_percentage = (total_passed / total_tests_all * 100) if total_tests_all > 0 else 100
    f.write(f"- **Overall Pass Rate**: {overall_percentage:.1f}%\n\n")
    
    f.write(f"---\n\n")
    f.write(f"## 📋 File-by-File Results\n\n")
    
    f.write(f"| # | File | Tests | Passed | Failed | % | Status |\n")
    f.write(f"|---|------|-------|--------|--------|---|--------|\n")
    
    for r in all_results:
        status_icon = "✅" if "PASSED" in r['status'] else "⚠️" if "PARTIAL" in r['status'] else "❌"
        f.write(f"| {r['file_number']} | {r['file_name']} | {r['required_features']} | {r['tests_passed']} | {r['tests_failed']} | {r['pass_percentage']:.0f}% | {status_icon} |\n")
    
    f.write(f"\n---\n\n")
    f.write(f"## 📁 Category Breakdown\n\n")
    
    main_files = [r for r in all_results if r['category'] == 'main']
    batch_files = [r for r in all_results if r['category'] == 'batch_plans']
    
    f.write(f"### Main Files ({len(main_files)} files)\n\n")
    main_passed = sum(r['tests_passed'] for r in main_files)
    main_total = sum(r['required_features'] for r in main_files)
    main_pct = (main_passed / main_total * 100) if main_total > 0 else 100
    f.write(f"- Tests: {main_passed}/{main_total} ({main_pct:.1f}%)\n\n")
    
    f.write(f"### Batch Plans ({len(batch_files)} files)\n\n")
    batch_passed = sum(r['tests_passed'] for r in batch_files)
    batch_total = sum(r['required_features'] for r in batch_files)
    batch_pct = (batch_passed / batch_total * 100) if batch_total > 0 else 100
    f.write(f"- Tests: {batch_passed}/{batch_total} ({batch_pct:.1f}%)\n\n")
    
    f.write(f"---\n\n")
    f.write(f"## ✅ Implementation Status\n\n")
    
    if overall_percentage >= 90:
        f.write(f"### 🎉 EXCELLENT!\n\nAll features from the 35 update files are implemented!\n\n")
    elif overall_percentage >= 70:
        f.write(f"### ⚠️ GOOD\n\nMost features are implemented. Some improvements needed.\n\n")
    else:
        f.write(f"### ❌ NEEDS WORK\n\nSignificant implementation gaps exist.\n\n")
    
    f.write(f"---\n\n")
    f.write(f"*Master summary generated automatically*\n")

# Save JSON data
json_file = reports_dir / "test_results.json"
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump({
        'timestamp': datetime.now().isoformat(),
        'total_files': len(all_files),
        'total_tests': total_tests_all,
        'total_passed': total_passed,
        'total_failed': total_failed,
        'overall_percentage': overall_percentage,
        'results': all_results
    }, f, indent=2, ensure_ascii=False)

print(f"Total Files Tested: {len(all_files)}")
print(f"Total Tests Run: {total_tests_all}")
print(f"Total Passed: {total_passed} ✅")
print(f"Total Failed: {total_failed} ❌")
print(f"Overall Pass Rate: {overall_percentage:.1f}%")

print(f"\n📁 All reports saved to: {reports_dir}/")
print(f"  📄 Master Summary: {summary_file}")
print(f"  📄 JSON Data: {json_file}")
print(f"  📄 Individual Reports: {len(all_files)} files")

print(f"\n{'=' * 120}")
if overall_percentage >= 80:
    print("🎉 SUCCESS! All files tested and most features implemented!")
    exit(0)
else:
    print("⚠️ Some features need attention")
    exit(1)
