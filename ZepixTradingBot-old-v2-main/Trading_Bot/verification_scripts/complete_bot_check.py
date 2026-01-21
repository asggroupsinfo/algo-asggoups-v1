"""
COMPLETE BOT PRODUCTION READINESS CHECK
Checks everything before live trading
"""
import os
import sys
import json
import importlib.util
from pathlib import Path
from datetime import datetime

print("=" * 120)
print("🔍 COMPLETE BOT PRODUCTION READINESS CHECK")
print("=" * 120)

# Test Results
all_checks = []
critical_errors = []
warnings = []

def check_pass(name, details=""):
    all_checks.append({"name": name, "status": "✅ PASS", "details": details})
    print(f"✅ {name}")
    if details:
        print(f"   {details}")

def check_fail(name, error, critical=True):
    status = "❌ CRITICAL" if critical else "⚠️ WARNING"
    all_checks.append({"name": name, "status": status, "details": error})
    print(f"{status}: {name}")
    print(f"   {error}")
    if critical:
        critical_errors.append({"check": name, "error": error})
    else:
        warnings.append({"check": name, "warning": error})

# ==================== CHECK 1: FILE STRUCTURE ====================
print("\n" + "=" * 120)
print("📁 CHECK 1: FILE STRUCTURE")
print("=" * 120)

required_files = [
    "src/main.py",
    "src/core/trading_engine.py",
    "src/telegram/telegram_service.py",
    "src/telegram/bots/controller_bot.py",
    "src/telegram/bots/notification_bot.py",
    "src/telegram/bots/analytics_bot.py",
    "src/telegram/notification_router.py",
    "config/config.yaml",
    "config/.env",
]

for file_path in required_files:
    if os.path.exists(file_path):
        check_pass(f"File exists: {file_path}")
    else:
        check_fail(f"Missing file: {file_path}", f"Required file not found", critical=True)

# ==================== CHECK 2: PYTHON SYNTAX ====================
print("\n" + "=" * 120)
print("🐍 CHECK 2: PYTHON SYNTAX")
print("=" * 120)

python_files = [
    "src/main.py",
    "src/core/trading_engine.py",
    "src/telegram/telegram_service.py",
    "src/telegram/bots/controller_bot.py",
    "src/telegram/bots/notification_bot.py",
    "src/telegram/bots/analytics_bot.py",
    "src/telegram/notification_router.py",
]

for file_path in python_files:
    if not os.path.exists(file_path):
        continue
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        check_pass(f"Syntax OK: {file_path}")
    except SyntaxError as e:
        check_fail(f"Syntax error in {file_path}", f"Line {e.lineno}: {e.msg}", critical=True)
    except Exception as e:
        check_fail(f"Error reading {file_path}", str(e), critical=True)

# ==================== CHECK 3: IMPORTS ====================
print("\n" + "=" * 120)
print("📦 CHECK 3: IMPORTS & DEPENDENCIES")
print("=" * 120)

required_imports = {
    "MetaTrader5": "MetaTrader5",
    "telegram": "python-telegram-bot",
    "yaml": "pyyaml",
    "pandas": "pandas",
    "numpy": "numpy",
    "loguru": "loguru",
}

for module, package in required_imports.items():
    try:
        __import__(module)
        check_pass(f"Import OK: {module} ({package})")
    except ImportError:
        check_fail(f"Missing package: {package}", f"Run: pip install {package}", critical=True)

# ==================== CHECK 4: CONFIGURATION ====================
print("\n" + "=" * 120)
print("⚙️ CHECK 4: CONFIGURATION")
print("=" * 120)

# Check .env file
env_file = "config/.env"
if os.path.exists(env_file):
    with open(env_file, 'r') as f:
        env_content = f.read()
    
    required_env_vars = [
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_ADMIN_CHAT_ID",
        "MT5_LOGIN",
        "MT5_PASSWORD",
        "MT5_SERVER",
    ]
    
    for var in required_env_vars:
        if var in env_content and not f"{var}=" in env_content:
            check_pass(f"ENV variable exists: {var}")
        elif f"{var}=your_" in env_content or f"{var}=" not in env_content:
            check_fail(f"ENV not configured: {var}", f"Please set {var} in config/.env", critical=True)
        else:
            check_pass(f"ENV configured: {var}")
else:
    check_fail("Missing .env file", "Create config/.env with required variables", critical=True)

# Check config.yaml
config_file = "config/config.yaml"
if os.path.exists(config_file):
    try:
        import yaml
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check critical config sections
        critical_sections = ['trading', 'telegram', 'risk_management']
        for section in critical_sections:
            if section in config:
                check_pass(f"Config section exists: {section}")
            else:
                check_fail(f"Missing config section: {section}", f"Add {section} to config.yaml", critical=False)
        
        # Check V6 plugin config
        if 'plugins' in config and 'v6_price_action' in config['plugins']:
            v6_config = config['plugins']['v6_price_action']
            if v6_config.get('enabled'):
                check_pass("V6 Plugin: Enabled")
            else:
                check_fail("V6 Plugin: Disabled", "V6 is disabled in config", critical=False)
            
            # Check timeframes
            timeframes = v6_config.get('timeframes', {})
            active_tfs = [tf for tf, enabled in timeframes.items() if enabled]
            if active_tfs:
                check_pass(f"V6 Active Timeframes: {', '.join(active_tfs)}")
            else:
                check_fail("V6 Timeframes", "No timeframes enabled", critical=False)
        else:
            check_fail("V6 Plugin config missing", "Add v6_price_action to config.yaml", critical=False)
            
    except Exception as e:
        check_fail("Config YAML error", str(e), critical=True)
else:
    check_fail("Missing config.yaml", "Create config/config.yaml", critical=True)

# ==================== CHECK 5: TELEGRAM IMPLEMENTATION ====================
print("\n" + "=" * 120)
print("💬 CHECK 5: TELEGRAM IMPLEMENTATION")
print("=" * 120)

# Check notification_bot.py for V6 methods
notification_bot_file = "src/telegram/bots/notification_bot.py"
if os.path.exists(notification_bot_file):
    with open(notification_bot_file, 'r', encoding='utf-8') as f:
        notification_code = f.read()
    
    v6_methods = [
        "send_v6_entry_alert",
        "send_v6_exit_alert",
        "send_trend_pulse_alert",
        "send_shadow_trade_alert",
    ]
    
    for method in v6_methods:
        if f"def {method}" in notification_code or f"async def {method}" in notification_code:
            check_pass(f"V6 Notification method: {method}")
        else:
            check_fail(f"Missing V6 method: {method}", f"Implement {method} in notification_bot.py", critical=True)

# Check controller_bot.py for command handlers
controller_bot_file = "src/telegram/bots/controller_bot.py"
if os.path.exists(controller_bot_file):
    with open(controller_bot_file, 'r', encoding='utf-8') as f:
        controller_code = f.read()
    
    v6_commands = [
        "handle_v6_control",
        "handle_v6_status",
        "handle_tf1m_on",
        "handle_tf5m_on",
        "handle_tf15m_on",
        "handle_tf1h_on",
    ]
    
    analytics_commands = [
        "handle_daily",
        "handle_weekly",
        "handle_monthly",
        "handle_compare",
    ]
    
    reentry_commands = [
        "handle_chains_status",
        "handle_autonomous",
    ]
    
    all_commands = v6_commands + analytics_commands + reentry_commands
    
    for cmd in all_commands:
        if f"def {cmd}" in controller_code or f"async def {cmd}" in controller_code:
            check_pass(f"Command handler: {cmd}")
        else:
            check_fail(f"Missing handler: {cmd}", f"Implement {cmd} in controller_bot.py", critical=True)

# Check notification_router.py for V6 types
router_file = "src/telegram/notification_router.py"
if os.path.exists(router_file):
    with open(router_file, 'r', encoding='utf-8') as f:
        router_code = f.read()
    
    v6_types = ["V6_ENTRY_1M", "V6_ENTRY_5M", "V6_ENTRY_15M", "V6_ENTRY_1H"]
    
    for ntype in v6_types:
        if ntype in router_code:
            check_pass(f"Notification type: {ntype}")
        else:
            check_fail(f"Missing notification type: {ntype}", f"Add {ntype} to notification_router.py", critical=True)

# ==================== CHECK 6: TRADING ENGINE ====================
print("\n" + "=" * 120)
print("🤖 CHECK 6: TRADING ENGINE")
print("=" * 120)

engine_file = "src/core/trading_engine.py"
if os.path.exists(engine_file):
    with open(engine_file, 'r', encoding='utf-8') as f:
        engine_code = f.read()
    
    critical_methods = [
        "execute_trade",
        "check_exit_conditions",
        "update_trailing_stop",
        "handle_trade_exit",
    ]
    
    for method in critical_methods:
        if f"def {method}" in engine_code:
            check_pass(f"Trading method: {method}")
        else:
            check_fail(f"Missing trading method: {method}", f"Critical method not found", critical=True)
    
    # Check for V6 integration
    if "v6_price_action" in engine_code or "V6PriceAction" in engine_code:
        check_pass("V6 Plugin integration detected")
    else:
        check_fail("V6 integration", "V6 plugin not integrated in trading engine", critical=False)
    
    # Check for re-entry system
    if "re_entry" in engine_code or "reentry" in engine_code or "profit_chain" in engine_code:
        check_pass("Re-entry system detected")
    else:
        check_fail("Re-entry system", "Re-entry logic not found", critical=False)

# ==================== CHECK 7: DATABASE ====================
print("\n" + "=" * 120)
print("💾 CHECK 7: DATABASE")
print("=" * 120)

db_file = "data/trading.db"
if os.path.exists(db_file):
    check_pass(f"Database file exists: {db_file}")
    
    # Check database size
    db_size = os.path.getsize(db_file)
    check_pass(f"Database size: {db_size:,} bytes")
else:
    check_fail("Database not initialized", "Run bot first to create database", critical=False)

# ==================== CHECK 8: LOGS ====================
print("\n" + "=" * 120)
print("📝 CHECK 8: LOGGING SYSTEM")
print("=" * 120)

log_dir = "logs"
if os.path.exists(log_dir):
    check_pass(f"Log directory exists: {log_dir}")
    
    # Check for recent log files
    log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
    if log_files:
        check_pass(f"Log files found: {len(log_files)}")
    else:
        check_fail("No log files", "Bot has not been run yet", critical=False)
else:
    os.makedirs(log_dir)
    check_pass("Created log directory")

# ==================== CHECK 9: IMPORT TEST ====================
print("\n" + "=" * 120)
print("🔌 CHECK 9: IMPORT TEST")
print("=" * 120)

# Add src to path
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

try:
    # Try importing main modules
    from core import trading_engine
    check_pass("Import: trading_engine")
except Exception as e:
    check_fail("Import trading_engine", str(e), critical=True)

try:
    from telegram import telegram_service
    check_pass("Import: telegram_service")
except Exception as e:
    check_fail("Import telegram_service", str(e), critical=True)

try:
    from telegram.bots import controller_bot
    check_pass("Import: controller_bot")
except Exception as e:
    check_fail("Import controller_bot", str(e), critical=True)

try:
    from telegram.bots import notification_bot
    check_pass("Import: notification_bot")
except Exception as e:
    check_fail("Import notification_bot", str(e), critical=True)

# ==================== SUMMARY ====================
print("\n" + "=" * 120)
print("📊 FINAL SUMMARY")
print("=" * 120)

total_checks = len(all_checks)
passed_checks = len([c for c in all_checks if "✅" in c['status']])
failed_checks = len([c for c in all_checks if "❌" in c['status']])
warning_checks = len([c for c in all_checks if "⚠️" in c['status']])

print(f"\nTotal Checks: {total_checks}")
print(f"✅ Passed: {passed_checks}")
print(f"❌ Failed: {failed_checks}")
print(f"⚠️ Warnings: {warning_checks}")

pass_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
print(f"\n📈 Pass Rate: {pass_rate:.1f}%")

# Critical errors
if critical_errors:
    print(f"\n{'=' * 120}")
    print("❌ CRITICAL ERRORS - MUST FIX BEFORE LIVE TRADING:")
    print(f"{'=' * 120}")
    for i, error in enumerate(critical_errors, 1):
        print(f"\n{i}. {error['check']}")
        print(f"   Error: {error['error']}")

# Warnings
if warnings:
    print(f"\n{'=' * 120}")
    print("⚠️ WARNINGS - SHOULD BE REVIEWED:")
    print(f"{'=' * 120}")
    for i, warn in enumerate(warnings, 1):
        print(f"\n{i}. {warn['check']}")
        print(f"   Warning: {warn['warning']}")

# Save results
results = {
    'timestamp': datetime.now().isoformat(),
    'total_checks': total_checks,
    'passed': passed_checks,
    'failed': failed_checks,
    'warnings': warning_checks,
    'pass_rate': pass_rate,
    'all_checks': all_checks,
    'critical_errors': critical_errors,
    'warnings': warnings,
}

with open('bot_readiness_report.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n📄 Full report saved to: bot_readiness_report.json")

# Final verdict
print(f"\n{'=' * 120}")
if failed_checks == 0:
    print("🎉 BOT IS READY FOR LIVE TRADING!")
    print("   All critical checks passed. Review warnings if any.")
    exit(0)
elif failed_checks <= 5 and len(critical_errors) == 0:
    print("⚠️ BOT NEEDS MINOR FIXES")
    print("   No critical errors, but some checks failed. Review and fix.")
    exit(1)
else:
    print("❌ BOT NOT READY FOR LIVE TRADING")
    print("   Critical errors found. Fix all issues before going live.")
    exit(1)
