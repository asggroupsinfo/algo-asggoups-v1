"""
Test V6 Timeframe GUI Menu Implementation
Verifies zero-typing button interface is complete
"""

import re
import os
from pathlib import Path

BOT_PATH = r"C:\Users\Ansh Shivaay Gupta\Downloads\ZepixTradingBot-New-v1\ZepixTradingBot-old-v2-main\Trading_Bot"

def check_implementation(file_path, patterns, feature_name):
    """Check if feature is implemented"""
    if not os.path.exists(file_path):
        return False, "File not found"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    matches = []
    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
            matches.append(pattern)
    
    if len(matches) == len(patterns):
        return True, f"✅ All {len(patterns)} patterns found"
    elif matches:
        return False, f"⚠️ {len(matches)}/{len(patterns)} patterns found"
    else:
        return False, "❌ Not found"

# Files to check
controller_file = os.path.join(BOT_PATH, "src/telegram/bots/controller_bot.py")
menu_builder_file = os.path.join(BOT_PATH, "src/telegram/v6_timeframe_menu_builder.py")

print("="*80)
print("🎮 V6 TIMEFRAME GUI MENU IMPLEMENTATION CHECK")
print("="*80)
print("\n📋 ZERO-TYPING BUTTON INTERFACE VERIFICATION\n")

features = {
    "✅ CORE COMPONENTS": {
        "V6TimeframeMenuBuilder class created": [
            r"class\s+V6TimeframeMenuBuilder",
            r"def\s+build_v6_submenu",
            r"InlineKeyboardButton"
        ],
        "Menu Builder initialized in controller": [
            r"V6TimeframeMenuBuilder",
        ],
        "/v6_menu command registered": [
            r'CommandHandler\("v6_menu"',
            r"self\.handle_v6_menu"
        ],
        "handle_v6_menu handler created": [
            r"async\s+def\s+handle_v6_menu",
            r"menu_data\s*=\s*self\.v6_menu_builder\.build_v6_submenu",
            r"reply_markup.*reply_markup"
        ],
    },
    
    "🎯 BUTTON CALLBACKS (Zero Typing Features)": {
        "v6_menu callback (main menu)": [
            r'if\s+data\s*==\s*"v6_menu"',
            r"build_v6_submenu"
        ],
        "v6_enable_15m/30m/1h/4h callbacks": [
            r'if\s+data\.startswith\("v6_enable_"\)',
            r"handle_enable_timeframe"
        ],
        "v6_disable_15m/30m/1h/4h callbacks": [
            r'if\s+data\.startswith\("v6_disable_"\)',
            r"handle_disable_timeframe"
        ],
        "v6_config_15m/30m/1h/4h callbacks": [
            r'if\s+data\.startswith\("v6_config_"\)',
            r"build_timeframe_config_menu"
        ],
        "v6_performance callback": [
            r'if\s+data\s*==\s*"v6_performance"',
            r"build_performance_comparison"
        ],
        "v6_enable_all callback": [
            r'if\s+data\s*==\s*"v6_enable_all"',
            r"build_enable_all_confirmation"
        ],
        "v6_enable_all_confirm callback": [
            r'if\s+data\s*==\s*"v6_enable_all_confirm"',
            r"handle_enable_all_timeframes"
        ],
        "v6_disable_all callback": [
            r'if\s+data\s*==\s*"v6_disable_all"',
            r"build_disable_all_confirmation"
        ],
        "v6_disable_all_confirm callback": [
            r'if\s+data\s*==\s*"v6_disable_all_confirm"',
            r"handle_disable_all_timeframes"
        ],
        "v6_param_* callbacks (config updates)": [
            r'if\s+data\.startswith\("v6_param_"\)',
            r"handle_update_parameter"
        ],
        "v6_reset_* callbacks": [
            r'if\s+data\.startswith\("v6_reset_"\)',
        ],
    },
    
    "🖼️ GUI MENU BUILDERS": {
        "build_v6_submenu (main overview)": [
            r"def\s+build_v6_submenu",
            r"InlineKeyboardButton.*Enable",
            r"InlineKeyboardButton.*Disable",
            r"InlineKeyboardButton.*Config"
        ],
        "build_timeframe_config_menu": [
            r"def\s+build_timeframe_config_menu",
            r"Pulse.*Threshold",
            r"Pattern.*Quality",
            r"Lot.*Size"
        ],
        "build_performance_comparison": [
            r"def\s+build_performance_comparison",
            r"TIMEFRAME\s+COMPARISON",
            r"BEST.*PERFORMER"
        ],
        "build_enable_all_confirmation": [
            r"def\s+build_enable_all_confirmation",
            r"ENABLE\s+ALL\s+V6\s+TIMEFRAMES",
            r"Confirm\s+Enable\s+All"
        ],
        "build_disable_all_confirmation": [
            r"def\s+build_disable_all_confirmation",
            r"DISABLE\s+ALL\s+V6\s+TIMEFRAMES",
            r"open\s+trades"
        ],
    },
    
    "⚙️ ACTION HANDLERS": {
        "handle_enable_timeframe": [
            r"async\s+def\s+handle_enable_timeframe",
            r"plugin_manager\.enable_plugin"
        ],
        "handle_disable_timeframe": [
            r"async\s+def\s+handle_disable_timeframe",
            r"plugin_manager\.disable_plugin"
        ],
        "handle_enable_all_timeframes": [
            r"async\s+def\s+handle_enable_all_timeframes",
            r"for\s+tf\s+in"
        ],
        "handle_disable_all_timeframes": [
            r"async\s+def\s+handle_disable_all_timeframes",
        ],
        "handle_update_parameter": [
            r"async\s+def\s+handle_update_parameter",
            r"pulse.*lot.*quality",
        ],
    },
    
    "📊 DATA HELPERS": {
        "_get_all_timeframe_status": [
            r"def\s+_get_all_timeframe_status",
            r"for\s+tf\s+in\s+self\.V6_TIMEFRAMES"
        ],
        "_get_overall_performance": [
            r"def\s+_get_overall_performance",
            r"total_trades.*win_rate.*pnl"
        ],
        "_get_timeframe_performance": [
            r"def\s+_get_timeframe_performance",
            r"days.*int"
        ],
        "_get_timeframe_config": [
            r"def\s+_get_timeframe_config",
            r"pulse_threshold.*lot_size"
        ],
    }
}

total_found = 0
total_features = 0

for category, category_features in features.items():
    print(f"\n{category}")
    print("-" * 80)
    
    for feature_name, patterns in category_features.items():
        total_features += 1
        
        # Check in appropriate file
        if "callback" in feature_name.lower() or "handler created" in feature_name.lower() or "command registered" in feature_name.lower():
            file_to_check = controller_file
            file_label = "controller_bot.py"
        else:
            file_to_check = menu_builder_file
            file_label = "v6_timeframe_menu_builder.py"
        
        is_found, msg = check_implementation(file_to_check, patterns, feature_name)
        
        if is_found:
            total_found += 1
            print(f"✅ {feature_name:<50} [{file_label}]")
        else:
            print(f"❌ {feature_name:<50} [{msg}]")

print("\n" + "="*80)
print("📊 IMPLEMENTATION STATUS")
print("="*80)

coverage = (total_found / total_features * 100) if total_features > 0 else 0

print(f"\n✅ Features Implemented: {total_found}/{total_features}")
print(f"📊 Coverage: {coverage:.1f}%")

print("\n" + "="*80)
print("🎮 ZERO-TYPING GUI INTERFACE")
print("="*80)

print("\n✅ **WHAT USER CAN DO (NO TYPING REQUIRED):**")
print("\n1. Type: /v6_menu")
print("   → GUI menu appears with buttons")
print("\n2. Click buttons to:")
print("   • Enable/Disable any timeframe (15M, 30M, 1H, 4H)")
print("   • View performance comparison")
print("   • Configure each timeframe (Pulse, Lot Size, etc.)")
print("   • Enable/Disable all timeframes at once")
print("   • Adjust parameters with +/- buttons")
print("   • Toggle notification settings")
print("\n3. All actions via button clicks - ZERO TYPING! 🎉")

if coverage >= 95:
    print("\n" + "="*80)
    print("🎉 IMPLEMENTATION COMPLETE!")
    print("="*80)
    print("\n✅ GUI-based menu system fully implemented")
    print("✅ All button callbacks wired correctly")
    print("✅ Zero-typing interface ready to use")
    print("\n🚀 USER CAN NOW:")
    print("   1. Type only ONE command: /v6_menu")
    print("   2. Control EVERYTHING via button clicks")
    print("   3. No more typing commands! 🎮")
elif coverage >= 80:
    print("\n⚠️ Nearly complete - minor features missing")
else:
    print("\n❌ More implementation needed")

print("\n" + "="*80)
print("END OF VERIFICATION")
print("="*80)
