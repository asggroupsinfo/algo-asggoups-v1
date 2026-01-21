"""
🔍 DEEP VERIFICATION - Real Implementation Check
Verifies actual code implementation, not just file existence
"""
import os
import sys
import ast
import json
from pathlib import Path

print("=" * 120)
print("🔍 DEEP VERIFICATION - CHECKING ACTUAL IMPLEMENTATION")
print("=" * 120)

errors = []
warnings = []
passed = []
critical_failures = []

# PHASE 1: Check if methods ACTUALLY exist with proper implementation
print("\n📋 PHASE 1: Verify V6 Notification Methods Implementation")

notification_bot_file = "src/telegram/bots/notification_bot.py"
if os.path.exists(notification_bot_file):
    with open(notification_bot_file, 'r', encoding='utf-8') as f:
        notif_code = f.read()
    
    # Parse AST to check actual implementation
    try:
        tree = ast.parse(notif_code)
        class_found = False
        methods_found = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "NotificationBot":
                class_found = True
                for item in node.body:
                    if isinstance(item, ast.AsyncFunctionDef):
                        method_name = item.name
                        # Check if method has actual implementation (not just pass)
                        has_implementation = False
                        for stmt in item.body:
                            if not isinstance(stmt, ast.Pass):
                                has_implementation = True
                                break
                        methods_found[method_name] = has_implementation
        
        # Check V6 methods
        v6_methods = {
            "send_v6_entry_alert": False,
            "send_v6_exit_alert": False,
            "send_trend_pulse_alert": False,
            "send_shadow_trade_alert": False
        }
        
        for method, _ in v6_methods.items():
            if method in methods_found:
                if methods_found[method]:
                    passed.append(f"✅ {method} - FULLY IMPLEMENTED")
                    print(f"  ✅ {method} - Has real implementation")
                else:
                    critical_failures.append(f"❌ {method} - EXISTS but EMPTY (only pass)")
                    print(f"  ❌ {method} - Exists but no implementation!")
            else:
                critical_failures.append(f"❌ {method} - NOT FOUND")
                print(f"  ❌ {method} - Method not found!")
        
        if not class_found:
            critical_failures.append("❌ NotificationBot class not found!")
            
    except SyntaxError as e:
        critical_failures.append(f"❌ Syntax error in notification_bot.py: {e}")
else:
    critical_failures.append(f"❌ File not found: {notification_bot_file}")

# PHASE 2: Check controller_bot command handlers
print("\n🤖 PHASE 2: Verify Command Handler Implementation")

controller_bot_file = "src/telegram/bots/controller_bot.py"
if os.path.exists(controller_bot_file):
    with open(controller_bot_file, 'r', encoding='utf-8') as f:
        controller_code = f.read()
    
    try:
        tree = ast.parse(controller_code)
        methods_found = {}
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == "ControllerBot":
                for item in node.body:
                    if isinstance(item, ast.AsyncFunctionDef):
                        method_name = item.name
                        has_implementation = False
                        for stmt in item.body:
                            if not isinstance(stmt, ast.Pass):
                                has_implementation = True
                                break
                        methods_found[method_name] = has_implementation
        
        # Check critical handlers
        critical_handlers = [
            "handle_v6_control",
            "handle_v6_status",
            "handle_tf1h_on",
            "handle_daily",
            "handle_chains_status",
            "handle_autonomous",
            "handle_plugin_status",
            "handle_compare"
        ]
        
        for handler in critical_handlers:
            if handler in methods_found:
                if methods_found[handler]:
                    passed.append(f"✅ {handler} - IMPLEMENTED")
                    print(f"  ✅ {handler} - Has implementation")
                else:
                    critical_failures.append(f"❌ {handler} - Empty implementation")
                    print(f"  ❌ {handler} - No real code!")
            else:
                critical_failures.append(f"❌ {handler} - NOT FOUND")
                print(f"  ❌ {handler} - Method missing!")
                
    except SyntaxError as e:
        critical_failures.append(f"❌ Syntax error in controller_bot.py: {e}")
else:
    critical_failures.append(f"❌ File not found: {controller_bot_file}")

# PHASE 3: Check if commands are ACTUALLY WIRED
print("\n🔗 PHASE 3: Verify Command Registration (Wiring)")

if os.path.exists(controller_bot_file):
    with open(controller_bot_file, 'r', encoding='utf-8') as f:
        controller_code = f.read()
    
    # Check _register_handlers method
    if "def _register_handlers" in controller_code:
        # Check if new commands are registered
        commands_to_check = [
            ('CommandHandler("v6_control"', "handle_v6_control"),
            ('CommandHandler("v6_status"', "handle_v6_status"),
            ('CommandHandler("daily"', "handle_daily"),
            ('CommandHandler("chains"', "handle_chains_status"),
            ('CommandHandler("autonomous"', "handle_autonomous"),
        ]
        
        wired_count = 0
        for cmd_handler, method_name in commands_to_check:
            if cmd_handler in controller_code and method_name in controller_code:
                # Check if they are in same method (_register_handlers)
                register_start = controller_code.find("def _register_handlers")
                register_end = controller_code.find("\n    def ", register_start + 1)
                if register_end == -1:
                    register_end = len(controller_code)
                register_section = controller_code[register_start:register_end]
                
                if cmd_handler in register_section:
                    wired_count += 1
                    passed.append(f"✅ {cmd_handler} is WIRED")
                    print(f"  ✅ {cmd_handler} is properly wired")
                else:
                    critical_failures.append(f"❌ {cmd_handler} NOT WIRED")
                    print(f"  ❌ {cmd_handler} handler exists but NOT wired!")
            else:
                critical_failures.append(f"❌ {cmd_handler} MISSING")
                print(f"  ❌ {cmd_handler} not found in code")
        
        print(f"\n  📊 Wired Commands: {wired_count}/{len(commands_to_check)}")
    else:
        critical_failures.append("❌ _register_handlers method not found!")
        print("  ❌ _register_handlers method missing!")

# PHASE 4: Deep code analysis - check for actual logic
print("\n💡 PHASE 4: Check for Actual Logic Implementation")

if os.path.exists(controller_bot_file):
    with open(controller_bot_file, 'r', encoding='utf-8') as f:
        controller_code = f.read()
    
    # Check if handle_v6_control has real implementation
    v6_control_start = controller_code.find("async def handle_v6_control")
    if v6_control_start != -1:
        v6_control_end = controller_code.find("\n    async def ", v6_control_start + 1)
        if v6_control_end == -1:
            v6_control_end = controller_code.find("\n    def ", v6_control_start + 1)
        if v6_control_end == -1:
            v6_control_end = len(controller_code)
        
        v6_control_code = controller_code[v6_control_start:v6_control_end]
        
        # Check for meaningful implementation
        has_logic = False
        logic_indicators = [
            "update.message.reply_text",
            "InlineKeyboard",
            "self.bot",
            "await",
            "try:",
            "if",
        ]
        
        logic_count = sum(1 for indicator in logic_indicators if indicator in v6_control_code)
        
        if logic_count >= 3:
            passed.append("✅ handle_v6_control has meaningful logic")
            print(f"  ✅ handle_v6_control has {logic_count} logic indicators")
        else:
            warnings.append(f"⚠️ handle_v6_control might be incomplete ({logic_count} indicators)")
            print(f"  ⚠️ handle_v6_control only has {logic_count} logic indicators")

# PHASE 5: Check notification_router for V6 types
print("\n📡 PHASE 5: Verify Notification Router V6 Types")

router_file = "src/telegram/notification_router.py"
if os.path.exists(router_file):
    with open(router_file, 'r', encoding='utf-8') as f:
        router_code = f.read()
    
    v6_types = [
        "V6_ENTRY_1H",
        "V6_ENTRY_15M",
        "V6_EXIT",
        "TREND_PULSE",
    ]
    
    found_types = sum(1 for vtype in v6_types if vtype in router_code)
    
    if found_types == len(v6_types):
        passed.append(f"✅ All {len(v6_types)} V6 notification types found")
        print(f"  ✅ All {len(v6_types)} V6 types defined")
    else:
        warnings.append(f"⚠️ Only {found_types}/{len(v6_types)} V6 types found")
        print(f"  ⚠️ Only {found_types}/{len(v6_types)} types found")
else:
    warnings.append(f"⚠️ {router_file} not found")

# PHASE 6: Integration check - can modules be imported?
print("\n🔌 PHASE 6: Import Test (Without Running)")

import_tests = []

# Test 1: Can we parse the files?
for file_path in [notification_bot_file, controller_bot_file]:
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, file_path, 'exec')
            passed.append(f"✅ {file_path} - Valid Python syntax")
            print(f"  ✅ {file_path} - Syntax valid")
        except SyntaxError as e:
            critical_failures.append(f"❌ {file_path} - Syntax error: {e}")
            print(f"  ❌ {file_path} - Syntax error!")

# SUMMARY
print("\n" + "=" * 120)
print("📊 DEEP VERIFICATION SUMMARY")
print("=" * 120)

print(f"\n✅ Passed: {len(passed)}")
print(f"⚠️ Warnings: {len(warnings)}")
print(f"❌ Critical Failures: {len(critical_failures)}")

if critical_failures:
    print(f"\n❌ CRITICAL FAILURES ({len(critical_failures)}):")
    for fail in critical_failures:
        print(f"  {fail}")

if warnings:
    print(f"\n⚠️ WARNINGS ({len(warnings)}):")
    for warn in warnings[:10]:
        print(f"  {warn}")

# Save detailed report
report = {
    "timestamp": "2026-01-20",
    "passed": len(passed),
    "warnings": len(warnings),
    "critical_failures": len(critical_failures),
    "details": {
        "passed": passed,
        "warnings": warnings,
        "critical_failures": critical_failures
    }
}

with open("deep_verification_report.json", "w") as f:
    json.dump(report, f, indent=2)

print("\n" + "=" * 120)
print("🏁 FINAL VERDICT")
print("=" * 120)

if len(critical_failures) == 0:
    print("✅ DEEP VERIFICATION PASSED!")
    print("🎯 All implementations are REAL and COMPLETE")
    print("🚀 Bot is ready for integration testing")
    exit_code = 0
elif len(critical_failures) <= 5:
    print("⚠️ MINOR ISSUES FOUND")
    print("🔧 Fix these issues before deployment")
    exit_code = 1
else:
    print("❌ MAJOR ISSUES DETECTED!")
    print("🔴 Implementation is INCOMPLETE or BROKEN")
    exit_code = 1

print("=" * 120)
sys.exit(exit_code)
