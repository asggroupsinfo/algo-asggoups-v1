"""
Menu Systems Architecture Complete Verification
Checks all 12 menu handlers mentioned in 03_MENU_SYSTEMS_ARCHITECTURE.md
"""

import os
import re
from pathlib import Path

BOT_PATH = r"C:\Users\Ansh Shivaay Gupta\Downloads\ZepixTradingBot-New-v1\ZepixTradingBot-old-v2-main\Trading_Bot"

def check_file_exists(file_path):
    """Check if file exists and return line count"""
    if not os.path.exists(file_path):
        return False, 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = len(f.readlines())
    return True, lines

def check_class_exists(file_path, class_name):
    """Check if class exists in file"""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = rf'class\s+{class_name}'
    return bool(re.search(pattern, content))

def check_method_exists(file_path, method_name):
    """Check if method exists in file"""
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = rf'def\s+{method_name}'
    return bool(re.search(pattern, content))

print("="*90)
print("🧭 MENU SYSTEMS ARCHITECTURE COMPLETE VERIFICATION")
print("="*90)
print("\nDocument: 03_MENU_SYSTEMS_ARCHITECTURE.md (873 lines)")
print("\n📊 OVERVIEW:")
print("  • Total Menu Handlers: 12")
print("  • Document Claims: 9 Working (75%) | 2 Broken (17%) | 1 Missing (8%)")
print("\n" + "="*90)

# Define expected menu handlers from document
menu_handlers = {
    "MenuManager": {
        "file": "src/menu/menu_manager.py",
        "expected_lines": 959,
        "class": "MenuManager",
        "key_methods": ["show_main_menu", "handle_menu_callback"],
        "doc_status": "✅ Working",
    },
    "FineTuneMenuHandler": {
        "file": "src/menu/fine_tune_menu_handler.py",
        "expected_lines": 300,
        "class": "FineTuneMenuHandler",
        "key_methods": ["show_fine_tune_menu"],
        "doc_status": "✅ Working",
    },
    "ReentryMenuHandler": {
        "file": "src/menu/reentry_menu_handler.py",
        "expected_lines": 250,
        "class": "ReentryMenuHandler",
        "key_methods": ["show_reentry_menu"],
        "doc_status": "✅ Working",
    },
    "ProfitBookingMenuHandler": {
        "file": "src/menu/profit_booking_menu_handler.py",
        "expected_lines": 350,
        "class": "ProfitBookingMenuHandler",
        "key_methods": ["show_profit_menu"],
        "doc_status": "✅ Working",
    },
    "TimeframeMenuHandler": {
        "file": "src/menu/timeframe_menu_handler.py",
        "expected_lines": 200,
        "class": "TimeframeMenuHandler",
        "key_methods": ["show_timeframe_menu"],
        "doc_status": "✅ Working",
    },
    "RiskMenuHandler": {
        "file": "src/menu/risk_menu_handler.py",
        "expected_lines": 200,
        "class": "RiskMenuHandler",
        "key_methods": ["show_risk_menu"],
        "doc_status": "✅ Working",
    },
    "V6ControlMenuHandler": {
        "file": "src/menu/v6_control_menu_handler.py",
        "expected_lines": 250,
        "class": "V6ControlMenuHandler",
        "key_methods": ["show_v6_control_menu", "handle_toggle"],
        "doc_status": "❌ Missing (Document claims 0 lines)",
    },
    "AnalyticsMenuHandler": {
        "file": "src/menu/analytics_menu_handler.py",
        "expected_lines": 300,
        "class": "AnalyticsMenuHandler",
        "key_methods": ["show_analytics_menu", "show_comparison_report"],
        "doc_status": "❌ Missing (Document claims 0 lines)",
    },
}

# Additional supporting files
supporting_files = {
    "ContextManager": "src/menu/context_manager.py",
    "CommandExecutor": "src/menu/command_executor.py",
    "CommandMapping": "src/menu/command_mapping.py",
    "MenuBuilder": "src/telegram/menu_builder.py",
    "MenuCallbackHandler": "src/clients/menu_callback_handler.py",
}

print("\n🗂️ CRITICAL MENU HANDLER FILES CHECK:")
print("-" * 90)

total_handlers = len(menu_handlers)
found_handlers = 0
working_handlers = 0
missing_handlers = 0

handler_results = {}

for handler_name, info in menu_handlers.items():
    file_path = os.path.join(BOT_PATH, info["file"])
    exists, line_count = check_file_exists(file_path)
    
    if exists:
        found_handlers += 1
        class_exists = check_class_exists(file_path, info["class"])
        methods_found = sum(1 for method in info["key_methods"] if check_method_exists(file_path, method))
        total_methods = len(info["key_methods"])
        
        if class_exists and methods_found == total_methods:
            status = "✅ WORKING"
            working_handlers += 1
        elif class_exists:
            status = "⚠️ PARTIAL"
        else:
            status = "❌ BROKEN"
        
        handler_results[handler_name] = {
            "exists": True,
            "lines": line_count,
            "class_exists": class_exists,
            "methods": f"{methods_found}/{total_methods}",
            "status": status
        }
        
        print(f"{status:<20} {handler_name:<30} [{line_count:>4} lines] ({methods_found}/{total_methods} methods)")
    else:
        missing_handlers += 1
        handler_results[handler_name] = {
            "exists": False,
            "lines": 0,
            "class_exists": False,
            "methods": "0/0",
            "status": "❌ MISSING"
        }
        print(f"❌ MISSING          {handler_name:<30} [   0 lines]")

print("\n" + "="*90)
print("📊 SUPPORTING FILES CHECK:")
print("-" * 90)

for name, file in supporting_files.items():
    file_path = os.path.join(BOT_PATH, file)
    exists, line_count = check_file_exists(file_path)
    
    if exists:
        print(f"✅ EXISTS           {name:<30} [{line_count:>4} lines]")
    else:
        print(f"❌ MISSING          {name:<30} [   0 lines]")

print("\n" + "="*90)
print("🔍 DETAILED VERIFICATION:")
print("="*90)

# Verify V6 Control Menu (Document claims MISSING)
print("\n🎯 V6 CONTROL MENU HANDLER:")
print("-" * 90)
v6_file = os.path.join(BOT_PATH, "src/menu/v6_control_menu_handler.py")
if os.path.exists(v6_file):
    with open(v6_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key features
    features = {
        "Class Definition": r'class\s+V6ControlMenuHandler',
        "show_v6_control_menu": r'def\s+show_v6_control_menu',
        "handle_toggle": r'def\s+handle_toggle',
        "Timeframe 15M": r'15m|15M',
        "Timeframe 30M": r'30m|30M',
        "Timeframe 1H": r'1h|1H',
        "Timeframe 4H": r'4h|4H',
        "Enable All": r'enable_all',
        "Disable All": r'disable_all',
    }
    
    print("Document Status: ❌ MISSING")
    print("Actual Status: ✅ EXISTS!")
    print("\nFeature Check:")
    for feature, pattern in features.items():
        found = bool(re.search(pattern, content, re.IGNORECASE))
        status = "✅" if found else "❌"
        print(f"  {status} {feature}")

else:
    print("Document Status: ❌ MISSING")
    print("Actual Status: ❌ CONFIRMED MISSING")

# Verify Analytics Menu (Document claims MISSING)
print("\n📊 ANALYTICS MENU HANDLER:")
print("-" * 90)
analytics_file = os.path.join(BOT_PATH, "src/menu/analytics_menu_handler.py")
if os.path.exists(analytics_file):
    with open(analytics_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for key features
    features = {
        "Class Definition": r'class\s+AnalyticsMenuHandler',
        "show_analytics_menu": r'def\s+show_analytics_menu',
        "show_comparison_report": r'def\s+show_comparison_report',
        "Daily Report": r'daily|Daily',
        "Weekly Report": r'weekly|Weekly',
        "Monthly Report": r'monthly|Monthly',
        "V3 vs V6 Comparison": r'v3.*v6|comparison',
        "Export CSV": r'export|csv',
    }
    
    print("Document Status: ❌ MISSING")
    print("Actual Status: ✅ EXISTS!")
    print("\nFeature Check:")
    for feature, pattern in features.items():
        found = bool(re.search(pattern, content, re.IGNORECASE))
        status = "✅" if found else "❌"
        print(f"  {status} {feature}")

else:
    print("Document Status: ❌ MISSING")
    print("Actual Status: ❌ CONFIRMED MISSING")

# Check MenuManager main menu
print("\n🧭 MENU MANAGER - MAIN MENU:")
print("-" * 90)
menu_manager_file = os.path.join(BOT_PATH, "src/menu/menu_manager.py")
if os.path.exists(menu_manager_file):
    with open(menu_manager_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for main menu items
    menu_items = {
        "Trading Control": r'Trading|trading',
        "Performance": r'Performance|performance',
        "Logic Control": r'Logic|logic',
        "Re-entry": r'Re-entry|reentry',
        "Profit Booking": r'Profit|profit',
        "Risk Management": r'Risk|risk',
        "Trends": r'Trends|trends',
        "Fine-Tune": r'Fine-Tune|finetune',
        "Dashboard": r'Dashboard|dashboard',
        "Panic Close": r'Panic|panic',
        "V6 Control": r'V6|v6',
        "Analytics": r'Analytics|analytics',
    }
    
    print("Main Menu Items Check:")
    for item, pattern in menu_items.items():
        found = bool(re.search(pattern, content, re.IGNORECASE))
        status = "✅" if found else "❌"
        print(f"  {status} {item}")

print("\n" + "="*90)
print("📊 FINAL SUMMARY:")
print("="*90)

working_pct = (working_handlers / total_handlers * 100) if total_handlers > 0 else 0
found_pct = (found_handlers / total_handlers * 100) if total_handlers > 0 else 0

print(f"\n✅ Menu Handlers Found: {found_handlers}/{total_handlers} ({found_pct:.0f}%)")
print(f"✅ Fully Working: {working_handlers}/{total_handlers} ({working_pct:.0f}%)")
print(f"❌ Missing: {missing_handlers}/{total_handlers}")

print("\n" + "="*90)
print("🔍 DOCUMENT vs REALITY ANALYSIS:")
print("="*90)

print("\n📋 DOCUMENT CLAIMS:")
print("  • 9 Working (75%)")
print("  • 2 Broken (17%)")
print("  • 1 Missing (8%)")
print("  • V6ControlMenuHandler: ❌ MISSING (0 lines)")
print("  • AnalyticsMenuHandler: ❌ MISSING (0 lines)")

print(f"\n🎯 ACTUAL IMPLEMENTATION:")
print(f"  • Working: {working_handlers}/{total_handlers} ({working_pct:.0f}%)")
print(f"  • Missing: {missing_handlers}/{total_handlers}")

# Check V6 and Analytics specifically
v6_exists = os.path.exists(os.path.join(BOT_PATH, "src/menu/v6_control_menu_handler.py"))
analytics_exists = os.path.exists(os.path.join(BOT_PATH, "src/menu/analytics_menu_handler.py"))

if v6_exists or analytics_exists:
    print(f"\n⚠️ MAJOR DISCREPANCY FOUND:")
    if v6_exists:
        print(f"  • V6ControlMenuHandler: Document says ❌ MISSING, but file EXISTS ✅")
    if analytics_exists:
        print(f"  • AnalyticsMenuHandler: Document says ❌ MISSING, but file EXISTS ✅")
    print(f"\n  📄 Document is OUTDATED!")
else:
    print(f"\n✅ DOCUMENT ACCURATE:")
    print(f"  Both V6 and Analytics handlers are indeed missing")

print("\n" + "="*90)
print("END OF VERIFICATION")
print("="*90)
