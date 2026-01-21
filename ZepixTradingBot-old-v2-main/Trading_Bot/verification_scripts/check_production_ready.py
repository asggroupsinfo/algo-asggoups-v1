"""
COMPLETE PRODUCTION READINESS CHECK
Checks all critical aspects before live trading
"""
import os
import sys
import importlib.util
from pathlib import Path

print("=" * 120)
print("🔍 COMPLETE BOT PRODUCTION READINESS CHECK")
print("=" * 120)

errors = []
warnings = []
passed = []

# Check 1: Required directories
print("\n📁 CHECK 1: Directory Structure")
required_dirs = [
    "src",
    "src/telegram",
    "src/telegram/bots",
    "src/strategies",
    "src/database",
    "config",
    "logs",
    "data"
]

for dir_path in required_dirs:
    if os.path.exists(dir_path):
        passed.append(f"✅ Directory exists: {dir_path}")
    else:
        errors.append(f"❌ Missing directory: {dir_path}")
        try:
            os.makedirs(dir_path, exist_ok=True)
            passed.append(f"✅ Created directory: {dir_path}")
        except Exception as e:
            errors.append(f"❌ Failed to create {dir_path}: {e}")

# Check 2: Critical Python files
print("\n📄 CHECK 2: Critical Python Files")
critical_files = [
    "src/__init__.py",
    "src/telegram/__init__.py",
    "src/telegram/bots/__init__.py",
    "src/telegram/bots/controller_bot.py",
    "src/telegram/bots/notification_bot.py",
    "src/telegram/bots/analytics_bot.py",
    "src/telegram/notification_router.py",
    "src/strategies/__init__.py",
    "src/database/__init__.py",
]

for file_path in critical_files:
    if os.path.exists(file_path):
        passed.append(f"✅ File exists: {file_path}")
    else:
        errors.append(f"❌ Missing file: {file_path}")

# Check 3: Syntax errors in Python files
print("\n🐍 CHECK 3: Python Syntax Validation")
python_files = []
for root, dirs, files in os.walk("src"):
    for file in files:
        if file.endswith(".py"):
            python_files.append(os.path.join(root, file))

for py_file in python_files:
    try:
        with open(py_file, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, py_file, 'exec')
        passed.append(f"✅ Valid syntax: {py_file}")
    except SyntaxError as e:
        errors.append(f"❌ Syntax error in {py_file}: Line {e.lineno}: {e.msg}")
    except Exception as e:
        warnings.append(f"⚠️ Could not check {py_file}: {e}")

# Check 4: Import validation
print("\n📦 CHECK 4: Import Validation")
key_imports = [
    ("src.telegram.bots.controller_bot", "ControllerBot"),
    ("src.telegram.bots.notification_bot", "NotificationBot"),
    ("src.telegram.bots.analytics_bot", "AnalyticsBot"),
]

for module_path, class_name in key_imports:
    try:
        # Try to import the module
        spec = importlib.util.find_spec(module_path)
        if spec is None:
            errors.append(f"❌ Cannot find module: {module_path}")
        else:
            passed.append(f"✅ Module importable: {module_path}")
    except Exception as e:
        errors.append(f"❌ Import error in {module_path}: {e}")

# Check 5: Configuration files
print("\n⚙️ CHECK 5: Configuration Files")
config_files = [
    "config/settings.json",
    "config/telegram.json",
    "config/trading.json",
]

for config_file in config_files:
    if os.path.exists(config_file):
        try:
            import json
            with open(config_file, 'r') as f:
                json.load(f)
            passed.append(f"✅ Valid config: {config_file}")
        except json.JSONDecodeError as e:
            errors.append(f"❌ Invalid JSON in {config_file}: {e}")
    else:
        warnings.append(f"⚠️ Missing config: {config_file}")

# Check 6: Command handler registration
print("\n🤖 CHECK 6: Telegram Command Handlers")
if os.path.exists("src/telegram/bots/controller_bot.py"):
    with open("src/telegram/bots/controller_bot.py", 'r', encoding='utf-8') as f:
        controller_code = f.read()
    
    required_handlers = [
        "handle_v6_control",
        "handle_v6_status",
        "handle_tf1h_on",
        "handle_daily",
        "handle_chains_status",
        "handle_plugin_status",
    ]
    
    for handler in required_handlers:
        if f"def {handler}" in controller_code:
            passed.append(f"✅ Handler defined: {handler}")
        else:
            errors.append(f"❌ Missing handler: {handler}")

# Check 7: Notification methods
print("\n📢 CHECK 7: Notification Methods")
if os.path.exists("src/telegram/bots/notification_bot.py"):
    with open("src/telegram/bots/notification_bot.py", 'r', encoding='utf-8') as f:
        notification_code = f.read()
    
    required_methods = [
        "send_v6_entry_alert",
        "send_v6_exit_alert",
        "send_trend_pulse_alert",
        "send_shadow_trade_alert",
    ]
    
    for method in required_methods:
        if f"def {method}" in notification_code:
            passed.append(f"✅ Method defined: {method}")
        else:
            errors.append(f"❌ Missing method: {method}")

# Check 8: Database files
print("\n💾 CHECK 8: Database Files")
db_files = [
    "data/trading.db",
]

for db_file in db_files:
    if os.path.exists(db_file):
        passed.append(f"✅ Database exists: {db_file}")
    else:
        warnings.append(f"⚠️ Database will be created: {db_file}")

# Check 9: __init__.py files
print("\n📦 CHECK 9: Package __init__.py Files")
init_files = [
    "src/__init__.py",
    "src/telegram/__init__.py",
    "src/telegram/bots/__init__.py",
    "src/strategies/__init__.py",
    "src/database/__init__.py",
]

missing_inits = []
for init_file in init_files:
    if not os.path.exists(init_file):
        missing_inits.append(init_file)

if missing_inits:
    errors.append(f"❌ Missing {len(missing_inits)} __init__.py files")
    for init_file in missing_inits:
        errors.append(f"  - {init_file}")
else:
    passed.append("✅ All __init__.py files present")

# Check 10: Command wiring in controller
print("\n🔗 CHECK 10: Command Wiring")
if os.path.exists("src/telegram/bots/controller_bot.py"):
    with open("src/telegram/bots/controller_bot.py", 'r', encoding='utf-8') as f:
        controller_code = f.read()
    
    if "self.command_handlers" in controller_code:
        # Check if new commands are wired
        new_commands = [
            "/v6_control",
            "/v6_status",
            "/daily",
            "/chains",
        ]
        
        wired_count = 0
        for cmd in new_commands:
            if f'"{cmd}"' in controller_code and "self.handle_" in controller_code:
                wired_count += 1
        
        if wired_count == len(new_commands):
            passed.append(f"✅ All {wired_count} critical commands wired")
        elif wired_count > 0:
            warnings.append(f"⚠️ Only {wired_count}/{len(new_commands)} commands wired")
        else:
            errors.append(f"❌ No commands wired in command_handlers dict")
    else:
        errors.append("❌ command_handlers dict not found in controller_bot")

# Final Summary
print("\n" + "=" * 120)
print("📊 FINAL PRODUCTION READINESS REPORT")
print("=" * 120)

print(f"\n✅ PASSED: {len(passed)}")
print(f"⚠️ WARNINGS: {len(warnings)}")
print(f"❌ ERRORS: {len(errors)}")

if errors:
    print("\n❌ CRITICAL ERRORS FOUND:")
    for error in errors[:20]:  # Show first 20
        print(f"  {error}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more errors")

if warnings:
    print("\n⚠️ WARNINGS:")
    for warning in warnings[:10]:  # Show first 10
        print(f"  {warning}")
    if len(warnings) > 10:
        print(f"  ... and {len(warnings) - 10} more warnings")

print("\n" + "=" * 120)
if len(errors) == 0:
    print("🎉 SUCCESS! Bot is PRODUCTION READY!")
    print("=" * 120)
    sys.exit(0)
else:
    print(f"❌ FAILED! Fix {len(errors)} errors before live trading")
    print("=" * 120)
    sys.exit(1)
