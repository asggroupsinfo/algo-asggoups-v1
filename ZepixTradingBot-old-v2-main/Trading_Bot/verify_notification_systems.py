"""
Notification Systems Complete Verification
Checks all 50+ notification types mentioned in 02_NOTIFICATION_SYSTEMS_COMPLETE.md
"""

import re
import os
from pathlib import Path

BOT_PATH = r"C:\Users\Ansh Shivaay Gupta\Downloads\ZepixTradingBot-New-v1\ZepixTradingBot-old-v2-main\Trading_Bot"

def check_file_exists(file_path):
    """Check if file exists"""
    return os.path.exists(file_path)

def check_patterns_in_file(file_path, patterns):
    """Check if all patterns exist in file"""
    if not os.path.exists(file_path):
        return 0, len(patterns), []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    found = []
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            found.append(pattern)
    
    return len(found), len(patterns), found

print("="*90)
print("📨 NOTIFICATION SYSTEMS COMPLETE VERIFICATION")
print("="*90)
print("\nDocument: 02_NOTIFICATION_SYSTEMS_COMPLETE.md (753 lines)")
print("\n📊 OVERVIEW:")
print("  • Legacy (V3): 25 notification types")
print("  • V5 Plugin System: 15 notification types")
print("  • V6 Price Action: 10 notification types (Document claims MISSING)")
print("  • Total: 50+ notification types")
print("\n" + "="*90)

# File paths
notification_router_file = os.path.join(BOT_PATH, "src/telegram/notification_router.py")
notification_bot_file = os.path.join(BOT_PATH, "src/telegram/bots/notification_bot.py")
notification_templates_file = os.path.join(BOT_PATH, "src/telegram/notification_templates.py")
controller_bot_file = os.path.join(BOT_PATH, "src/telegram/bots/controller_bot.py")

# Check critical files
print("\n🗂️ CRITICAL FILES CHECK:")
print("-" * 90)

critical_files = {
    "notification_router.py": notification_router_file,
    "notification_bot.py": notification_bot_file,
    "notification_templates.py": notification_templates_file,
    "controller_bot.py": controller_bot_file,
}

for name, path in critical_files.items():
    exists = "✅" if check_file_exists(path) else "❌"
    print(f"{exists} {name:<35} {'EXISTS' if check_file_exists(path) else 'NOT FOUND'}")

# SECTION 1: LEGACY NOTIFICATION TYPES (25 Types)
print("\n" + "="*90)
print("🔷 SECTION 1: LEGACY NOTIFICATION TYPES (25 Types)")
print("="*90)

legacy_types = {
    "Trading Notifications (7)": [
        r"ENTRY",
        r"EXIT",
        r"TP_HIT",
        r"SL_HIT",
        r"BREAKEVEN",
        r"SL_MODIFIED",
        r"PARTIAL_CLOSE",
    ],
    "Signal Notifications (5)": [
        r"SIGNAL_RECEIVED",
        r"SIGNAL_IGNORED",
        r"SIGNAL_FILTERED",
        r"TREND_CHANGED",
        r"TREND_MANUAL_SET",
    ],
    "Re-entry Notifications (6)": [
        r"TP_REENTRY_STARTED",
        r"TP_REENTRY_EXECUTED",
        r"TP_REENTRY_COMPLETED",
        r"SL_HUNT_STARTED",
        r"SL_HUNT_RECOVERY",
        r"EXIT_CONTINUATION",
    ],
    "System Notifications (6)": [
        r"BOT_STARTED",
        r"BOT_STOPPED",
        r"EMERGENCY_STOP",
        r"MT5_CONNECTED|MT5_DISCONNECT",
        r"MT5_RECONNECT",
    ],
    "Analytics Notifications (1)": [
        r"DAILY_SUMMARY",
    ],
}

legacy_total_found = 0
legacy_total_types = 0

for category, patterns in legacy_types.items():
    print(f"\n{category}")
    print("-" * 90)
    found, total, _ = check_patterns_in_file(notification_router_file, patterns)
    legacy_total_found += found
    legacy_total_types += total
    status = "✅" if found == total else "⚠️" if found > 0 else "❌"
    print(f"{status} Found: {found}/{total} notification types in NotificationRouter")

legacy_coverage = (legacy_total_found / legacy_total_types * 100) if legacy_total_types > 0 else 0

# SECTION 2: V5 PLUGIN NOTIFICATION TYPES (15 Types)
print("\n" + "="*90)
print("🔶 SECTION 2: V5 PLUGIN NOTIFICATION TYPES (15 Types)")
print("="*90)

v5_types = {
    "Plugin Lifecycle (5)": [
        r"PLUGIN_ENABLED|PLUGIN_LOADED",
        r"PLUGIN_DISABLED",
        r"PLUGIN_ERROR",
        r"PLUGIN_CONFIG|CONFIG_RELOAD",
        r"PLUGIN_RELOAD",
    ],
    "V5 Trading (5)": [
        r"PLUGIN_SIGNAL|SIGNAL",
        r"PLUGIN_ENTRY|ENTRY",
        r"PLUGIN_EXIT|EXIT",
        r"PLUGIN_TP|TP_HIT",
        r"PLUGIN_SL|SL_HIT",
    ],
    "V5 Performance (5)": [
        r"PLUGIN_PERFORMANCE|PERFORMANCE",
        r"PLUGIN_DAILY|DAILY_SUMMARY",
        r"PLUGIN_COMPARISON|COMPARISON",
        r"PLUGIN_WEEKLY|WEEKLY",
        r"PLUGIN_STATS|STATS",
    ],
}

v5_total_found = 0
v5_total_types = 0

for category, patterns in v5_types.items():
    print(f"\n{category}")
    print("-" * 90)
    found, total, _ = check_patterns_in_file(notification_router_file, patterns)
    v5_total_found += found
    v5_total_types += total
    status = "✅" if found == total else "⚠️" if found > 0 else "❌"
    print(f"{status} Found: {found}/{total} notification types in NotificationRouter")

v5_coverage = (v5_total_found / v5_total_types * 100) if v5_total_types > 0 else 0

# SECTION 3: V6 PRICE ACTION NOTIFICATIONS (10 Types - Document claims MISSING)
print("\n" + "="*90)
print("🎯 SECTION 3: V6 PRICE ACTION NOTIFICATIONS (10 Types)")
print("="*90)
print("Document Status: ❌ MISSING (0%)")
print("Let's verify actual implementation...")
print("-" * 90)

v6_types = {
    "V6 Entry Notifications (4)": [
        r"V6_ENTRY_15M",
        r"V6_ENTRY_30M",
        r"V6_ENTRY_1H",
        r"V6_ENTRY_4H",
    ],
    "V6 Trade Events (3)": [
        r"V6_EXIT",
        r"V6_TP_HIT",
        r"V6_SL_HIT",
    ],
    "V6 Timeframe Control (2)": [
        r"V6_TIMEFRAME_ENABLED",
        r"V6_TIMEFRAME_DISABLED",
    ],
    "V6 Analytics (1)": [
        r"V6_DAILY_SUMMARY",
    ],
}

v6_total_found = 0
v6_total_types = 0

for category, patterns in v6_types.items():
    print(f"\n{category}")
    print("-" * 90)
    found, total, _ = check_patterns_in_file(notification_router_file, patterns)
    v6_total_found += found
    v6_total_types += total
    status = "✅" if found == total else "⚠️" if found > 0 else "❌"
    print(f"{status} Found: {found}/{total} notification types in NotificationRouter")

v6_coverage = (v6_total_found / v6_total_types * 100) if v6_total_types > 0 else 0

# SECTION 4: NOTIFICATION TEMPLATES
print("\n" + "="*90)
print("📱 SECTION 4: NOTIFICATION TEMPLATES")
print("="*90)

template_patterns = {
    "Basic Templates": [
        r"ENTRY_TEMPLATE|entry.*template",
        r"EXIT_TEMPLATE|exit.*template",
        r"TP.*TEMPLATE|tp.*template",
        r"SL.*TEMPLATE|sl.*template",
    ],
    "V6 Templates (Document claims MISSING)": [
        r"V6_ENTRY_TEMPLATE",
        r"V6_EXIT_TEMPLATE",
        r"V6_TP.*TEMPLATE",
        r"V6_SL.*TEMPLATE",
    ],
}

template_total_found = 0
template_total_types = 0

for category, patterns in template_patterns.items():
    print(f"\n{category}")
    print("-" * 90)
    
    # Check in both notification_templates.py and notification_bot.py
    found1, _, _ = check_patterns_in_file(notification_templates_file, patterns)
    found2, total, _ = check_patterns_in_file(notification_bot_file, patterns)
    
    found = max(found1, found2)  # Use best result
    template_total_found += found
    template_total_types += total
    
    status = "✅" if found == total else "⚠️" if found > 0 else "❌"
    file_used = "notification_templates.py" if found1 > found2 else "notification_bot.py"
    print(f"{status} Found: {found}/{total} templates in {file_used}")

# SECTION 5: NOTIFICATION ROUTER (3-Bot Architecture)
print("\n" + "="*90)
print("🏗️ SECTION 5: NOTIFICATION ROUTER (3-Bot Architecture)")
print("="*90)

router_features = {
    "NotificationRouter Class": [
        r"class\s+NotificationRouter",
    ],
    "NotificationType Enum": [
        r"class\s+NotificationType.*Enum",
    ],
    "3-Bot References": [
        r"controller.*notification.*analytics",
        r"CONTROLLER.*NOTIFICATION.*ANALYTICS",
    ],
    "Routing Table": [
        r"routing_table|ROUTING_RULES",
    ],
}

router_total_found = 0
router_total_types = 0

for feature, patterns in router_features.items():
    found, total, _ = check_patterns_in_file(notification_router_file, patterns)
    router_total_found += found
    router_total_types += total
    status = "✅" if found == total else "❌"
    print(f"{status} {feature:<40} [{found}/{total}]")

# SECTION 6: PRIORITY SYSTEM
print("\n" + "="*90)
print("📊 SECTION 6: NOTIFICATION PRIORITY SYSTEM")
print("="*90)

priority_features = {
    "Priority Levels": [
        r"CRITICAL",
        r"HIGH",
        r"MEDIUM",
        r"LOW",
        r"INFO",
    ],
    "Priority Config": [
        r"PRIORITY_CONFIG|priority.*config",
        r"disable_notification",
        r"delay",
    ],
}

priority_total_found = 0
priority_total_types = 0

for feature, patterns in priority_features.items():
    found, total, _ = check_patterns_in_file(notification_router_file, patterns)
    priority_total_found += found
    priority_total_types += total
    status = "✅" if found == total else "⚠️" if found > 0 else "❌"
    print(f"{status} {feature:<40} [{found}/{total}]")

# SECTION 7: ENHANCED VISUAL NOTIFICATIONS
print("\n" + "="*90)
print("🎨 SECTION 7: ENHANCED VISUAL NOTIFICATIONS (Telegram Features)")
print("="*90)

visual_features = {
    "Feature": [
        "InlineKeyboardButton",
        "InlineKeyboardMarkup",
        "parse_mode.*HTML",
        "parse_mode.*Markdown",
        "disable_notification",
    ],
    "Status": []
}

for feature in visual_features["Feature"]:
    found, total, _ = check_patterns_in_file(notification_bot_file, [feature])
    status = "✅ Used" if found > 0 else "❌ Not Used"
    print(f"{status:<20} {feature}")

# FINAL SUMMARY
print("\n" + "="*90)
print("📊 FINAL SUMMARY")
print("="*90)

total_found = legacy_total_found + v5_total_found + v6_total_found
total_types = legacy_total_types + v5_total_types + v6_total_types
overall_coverage = (total_found / total_types * 100) if total_types > 0 else 0

print(f"\n✅ Legacy (V3) Notifications:")
print(f"   Found: {legacy_total_found}/{legacy_total_types}")
print(f"   Coverage: {legacy_coverage:.1f}%")
print(f"   Document Status: ✅ Working 100% (claimed)")

print(f"\n✅ V5 Plugin Notifications:")
print(f"   Found: {v5_total_found}/{v5_total_types}")
print(f"   Coverage: {v5_coverage:.1f}%")
print(f"   Document Status: ✅ Working 100% (claimed)")

print(f"\n🎯 V6 Price Action Notifications:")
print(f"   Found: {v6_total_found}/{v6_total_types}")
print(f"   Coverage: {v6_coverage:.1f}%")
print(f"   Document Status: ❌ MISSING 0% (claimed)")

print(f"\n📱 Notification Templates:")
print(f"   Found: {template_total_found}/{template_total_types}")
print(f"   Coverage: {(template_total_found/template_total_types*100) if template_total_types > 0 else 0:.1f}%")

print(f"\n🏗️ Router Architecture:")
print(f"   Found: {router_total_found}/{router_total_types}")
print(f"   Coverage: {(router_total_found/router_total_types*100) if router_total_types > 0 else 0:.1f}%")

print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"📊 OVERALL NOTIFICATION SYSTEM COVERAGE")
print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"\n   Total Notification Types Found: {total_found}/{total_types}")
print(f"   Overall Coverage: {overall_coverage:.1f}%")

if overall_coverage >= 90:
    print(f"\n   ✅ Status: EXCELLENT - Nearly complete implementation")
elif overall_coverage >= 70:
    print(f"\n   ⚠️ Status: GOOD - Most features implemented")
elif overall_coverage >= 50:
    print(f"\n   ⚠️ Status: PARTIAL - Half implemented")
else:
    print(f"\n   ❌ Status: INCOMPLETE - Major work needed")

print("\n" + "="*90)
print("🔍 DOCUMENT vs REALITY ANALYSIS")
print("="*90)

print("\n📋 DOCUMENT CLAIMS:")
print("  • Legacy (V3): ✅ 100% Working (25 types)")
print("  • V5 Plugin: ✅ 100% Working (15 types)")
print("  • V6 Price Action: ❌ 0% Missing (10 types)")

print(f"\n🎯 ACTUAL IMPLEMENTATION:")
print(f"  • Legacy (V3): {legacy_coverage:.0f}% ({legacy_total_found}/{legacy_total_types} types)")
print(f"  • V5 Plugin: {v5_coverage:.0f}% ({v5_total_found}/{v5_total_types} types)")
print(f"  • V6 Price Action: {v6_coverage:.0f}% ({v6_total_found}/{v6_total_types} types)")

if v6_coverage > 0:
    print(f"\n⚠️ DISCREPANCY FOUND:")
    print(f"  Document claims V6 is 0% implemented")
    print(f"  But {v6_total_found}/{v6_total_types} V6 types exist in code!")
elif v6_coverage == 0:
    print(f"\n✅ DOCUMENT ACCURATE:")
    print(f"  V6 notifications are indeed missing as document states")

print("\n" + "="*90)
print("END OF VERIFICATION")
print("="*90)
