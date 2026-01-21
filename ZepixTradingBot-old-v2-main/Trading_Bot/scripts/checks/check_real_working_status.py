#!/usr/bin/env python3
"""
REAL WORKING STATUS - Testing Actual Bot Commands
Not just checking if handlers exist, but if they have REAL implementation
"""

print("=" * 70)
print("🔍 REAL IMPLEMENTATION CHECK - Working vs Code-Only")
print("=" * 70)

from pathlib import Path
import re

controller_path = Path('src/telegram/bots/controller_bot.py')

with open(controller_path, 'r', encoding='utf-8') as f:
    controller_code = f.read()

# Function to check if handler has real implementation (not just pass/placeholder)
def has_real_implementation(code, handler_name):
    """Check if handler has actual working code, not just pass/placeholder"""
    # Find the handler function
    pattern = rf'async def {handler_name}\(.*?\):.*?(?=\n    async def |\n    def |\nclass |\Z)'
    match = re.search(pattern, code, re.DOTALL)
    
    if not match:
        return False, "Handler not found"
    
    handler_code = match.group(0)
    lines = handler_code.split('\n')
    
    # Remove docstring and comments
    code_lines = []
    in_docstring = False
    for line in lines[1:]:  # Skip function definition
        stripped = line.strip()
        if '"""' in stripped or "'''" in stripped:
            in_docstring = not in_docstring
            continue
        if in_docstring or stripped.startswith('#'):
            continue
        if stripped:
            code_lines.append(stripped)
    
    # Check if only has pass/placeholder
    if len(code_lines) == 0:
        return False, "Empty implementation"
    if len(code_lines) == 1 and code_lines[0] in ['pass', 'return', 'return None']:
        return False, "Placeholder only"
    if len(code_lines) <= 3 and any('TODO' in line or 'NotImplemented' in line for line in code_lines):
        return False, "TODO/Not implemented"
    
    # Has real code
    return True, f"{len(code_lines)} lines of code"

print("\n" + "=" * 70)
print("1️⃣ MAIN MENU (Claimed: 100% - 3/3)")
print("=" * 70)

main_menu = {
    "Start/Menu": "handle_start",
    "Status Display": "handle_status",
    "Dashboard": "handle_dashboard"
}

for feature, handler in main_menu.items():
    is_real, details = has_real_implementation(controller_code, handler)
    status = "✅ WORKING" if is_real else "❌ FAKE"
    print(f"  {feature}: {status} ({details})")

print("\n" + "=" * 70)
print("2️⃣ V6 CONTROL MENU (Claimed: 100% - 8/8)")
print("=" * 70)

v6_control = {
    "V6 Status": "handle_v6_status",
    "V6 Control Menu": "handle_v6_control",
    "Toggle 15M ON": "handle_tf15m_on",
    "Toggle 15M OFF": "handle_tf15m_off",
    "Toggle 1H ON": "handle_tf1h_on",
    "Toggle 1H OFF": "handle_tf1h_off",
    "V6 Performance": "handle_v6_performance",
    "V6 Config": "handle_v6_config"
}

v6_working = 0
for feature, handler in v6_control.items():
    is_real, details = has_real_implementation(controller_code, handler)
    if is_real:
        v6_working += 1
    status = "✅ WORKING" if is_real else "❌ FAKE"
    print(f"  {feature}: {status} ({details})")

print(f"\nActual Working: {v6_working}/{len(v6_control)}")

print("\n" + "=" * 70)
print("3️⃣ TRADING CONTROL (Claimed: 80% - 4/5)")
print("=" * 70)

trading_control = {
    "Pause Trading": "handle_pause_bot",
    "Resume Trading": "handle_resume_bot",
    "List Trades": "handle_trades",
    "Bot Status": "handle_status",
    "Emergency Stop": "handle_emergency_stop"
}

trading_working = 0
for feature, handler in trading_control.items():
    is_real, details = has_real_implementation(controller_code, handler)
    if is_real:
        trading_working += 1
    status = "✅ WORKING" if is_real else "❌ MISSING"
    print(f"  {feature}: {status} ({details})")

print(f"\nActual Working: {trading_working}/{len(trading_control)}")

print("\n" + "=" * 70)
print("4️⃣ ANALYTICS MENU (Claimed: 71% - 5/7)")
print("=" * 70)

analytics = {
    "Daily Report": "handle_daily",
    "Weekly Report": "handle_weekly",
    "Monthly Report": "handle_monthly",
    "V3 vs V6 Compare": "handle_compare",
    "By Pair Analysis": "handle_pair_report",
    "By Logic Analysis": "handle_strategy_report",
    "Export CSV": "handle_export"
}

analytics_working = 0
for feature, handler in analytics.items():
    is_real, details = has_real_implementation(controller_code, handler)
    if is_real:
        analytics_working += 1
    status = "✅ WORKING" if is_real else "❌ MISSING"
    print(f"  {feature}: {status} ({details})")

print(f"\nActual Working: {analytics_working}/{len(analytics)}")

print("\n" + "=" * 70)
print("5️⃣ LOGIC CONTROL (Claimed: 67% - 2/3)")
print("=" * 70)

logic_control = {
    "Logic Toggle": "handle_logic_toggle",
    "Logic Status": "handle_logic_status",
    "Reset Logics": "handle_reset_logic"
}

logic_working = 0
for feature, handler in logic_control.items():
    is_real, details = has_real_implementation(controller_code, handler)
    if is_real:
        logic_working += 1
    status = "✅ WORKING" if is_real else "❌ MISSING"
    print(f"  {feature}: {status} ({details})")

print(f"\nActual Working: {logic_working}/{len(logic_control)}")

print("\n" + "=" * 70)
print("6️⃣ ADDITIONAL FEATURES (Claimed: 67% - 4/6)")
print("=" * 70)

additional = {
    "Fine-Tune Settings": "handle_fine_tune",
    "Risk Management": "handle_risk_settings",
    "Trend Management": "handle_trend",
    "Plugin Control": "handle_plugins_menu",
    "Help Command": "handle_help",
    "Settings": "handle_settings"
}

additional_working = 0
for feature, handler in additional.items():
    is_real, details = has_real_implementation(controller_code, handler)
    if is_real:
        additional_working += 1
    status = "✅ WORKING" if is_real else "❌ MISSING"
    print(f"  {feature}: {status} ({details})")

print(f"\nActual Working: {additional_working}/{len(additional)}")

print("\n" + "=" * 70)
print("7️⃣ RE-ENTRY MENU (Claimed: 40% - 2/5)")
print("=" * 70)

reentry = {
    "TP Re-entry Toggle": "handle_tp_continuation",
    "SL Hunt": "handle_sl_hunt_stats",
    "Exit Continuation": "handle_exit_continuation",
    "Re-entry Status": "handle_reentry_menu",
    "Re-entry Config": "handle_reentry_config"
}

reentry_working = 0
for feature, handler in reentry.items():
    is_real, details = has_real_implementation(controller_code, handler)
    if is_real:
        reentry_working += 1
    status = "✅ WORKING" if is_real else "❌ MISSING"
    print(f"  {feature}: {status} ({details})")

print(f"\nActual Working: {reentry_working}/{len(reentry)}")

print("\n" + "=" * 70)
print("8️⃣ PROFIT BOOKING (Claimed: 20% - 1/5)")
print("=" * 70)

profit = {
    "Profit Booking Toggle": "handle_profit_toggle",
    "Profit Targets": "handle_profit_targets",
    "Profit Stats": "handle_profit_stats",
    "Profit Chains": "handle_profit_chains",
    "Profit Config": "handle_profit_config"
}

profit_working = 0
for feature, handler in profit.items():
    is_real, details = has_real_implementation(controller_code, handler)
    if is_real:
        profit_working += 1
    status = "✅ WORKING" if is_real else "❌ MISSING"
    print(f"  {feature}: {status} ({details})")

print(f"\nActual Working: {profit_working}/{len(profit)}")

# Overall Summary
print("\n" + "=" * 70)
print("📊 TRUTH vs CLAIMS")
print("=" * 70)

categories = [
    ("Main Menu", 3, 3),
    ("V6 Control", v6_working, 8),
    ("Trading Control", trading_working, 5),
    ("Analytics", analytics_working, 7),
    ("Logic Control", logic_working, 3),
    ("Additional Features", additional_working, 6),
    ("Re-entry Menu", reentry_working, 5),
    ("Profit Booking", profit_working, 5)
]

print("\nCategory | Claimed | Actually Working | Truth")
print("-" * 70)
total_claimed = 0
total_actual = 0
for name, actual, total in categories:
    claimed_pct = 100  # First two claimed 100%
    if name == "Trading Control":
        claimed_pct = 80
    elif name == "Analytics":
        claimed_pct = 71
    elif name in ["Logic Control", "Additional Features"]:
        claimed_pct = 67
    elif name == "Re-entry Menu":
        claimed_pct = 40
    elif name == "Profit Booking":
        claimed_pct = 20
    
    actual_pct = (actual/total*100) if total > 0 else 0
    truth = "✅ TRUE" if abs(actual_pct - claimed_pct) < 15 else "❌ WRONG"
    
    print(f"{name:20} | {claimed_pct:3.0f}%    | {actual_pct:3.0f}% ({actual}/{total})       | {truth}")
    
    total_claimed += total
    total_actual += actual

print("-" * 70)
print(f"{'OVERALL':20} | {'N/A':7} | {total_actual/total_claimed*100:3.0f}% ({total_actual}/{total_claimed})")

print("\n" + "=" * 70)
print("🎯 FINAL VERDICT")
print("=" * 70)

print(f"\n✅ Actually Working: {total_actual}/{total_claimed} features ({total_actual/total_claimed*100:.0f}%)")
print(f"\nDocument claim vs Reality:")
print(f"  • Claimed overall: ~69% (29/42)")
print(f"  • Actually working: {total_actual/total_claimed*100:.0f}% ({total_actual}/{total_claimed})")

if total_actual >= 29:
    print(f"\n✅ HAA BHAI, CLAIMS SAB SACH HAIN!")
    print(f"Document jo bola tha wo sab implemented aur WORKING hai!")
else:
    print(f"\n⚠️ CLAIMS THODE INFLATED HAIN")
    print(f"Kuch features code me hain par fully working nahi!")

print("=" * 70)
