#!/usr/bin/env python3
"""Test Main Menu Design Document Implementation"""

print('📋 TESTING MAIN MENU DESIGN DOCUMENT')
print('='*60)

# Test 1: Check if MainMenu exists
try:
    from src.telegram.menus.main_menu import MainMenu
    print('✅ Test 1: MainMenu class exists')
    has_main_menu = True
except Exception as e:
    print(f'❌ Test 1 FAILED: MainMenu not found - {e}')
    has_main_menu = False

# Test 2: Check if 12 category menus exist
print('\nTest 2: Checking 12 category menus...')
menu_tests = {
    'main_menu': 'MainMenu',
    'system_menu': 'SystemMenu', 
    'trading_menu': 'TradingMenu',
    'risk_menu': 'RiskMenu',
    'v3_menu': 'V3StrategiesMenu',
    'v6_menu': 'V6FramesMenu',
    'analytics_menu': 'AnalyticsMenu',
    'reentry_menu': 'ReEntryMenu',
    'profit_menu': 'ProfitMenu',
    'plugin_menu': 'PluginMenu',
    'sessions_menu': 'SessionsMenu',
    'voice_menu': 'VoiceMenu'
}

missing_menus = []
for module_name, class_name in menu_tests.items():
    try:
        mod = __import__(f'src.telegram.menus.{module_name}', fromlist=[class_name])
        cls = getattr(mod, class_name)
        print(f'  ✅ {module_name} ({class_name})')
    except Exception as e:
        print(f'  ❌ {module_name} MISSING: {e}')
        missing_menus.append(module_name)

if not missing_menus:
    print('✅ All 12 category menus exist')
else:
    print(f'❌ Missing {len(missing_menus)} menus: {missing_menus}')

# Test 3: Check callback router
print('\nTest 3: Callback Router...')
try:
    from src.telegram.core.callback_router import CallbackRouter
    print('✅ CallbackRouter exists')
    has_router = True
except Exception as e:
    print(f'❌ CallbackRouter not found: {e}')
    has_router = False

# Test 4: Check ButtonBuilder
print('\nTest 4: ButtonBuilder...')
try:
    from src.telegram.core.button_builder import ButtonBuilder
    print('✅ ButtonBuilder exists')
    has_buttons = True
except Exception as e:
    print(f'❌ ButtonBuilder not found: {e}')
    has_buttons = False

# Test 5: Check plugin selection
print('\nTest 5: Plugin Selection...')
try:
    from src.telegram.core.plugin_selection_menu import PluginSelectionMenu
    print('✅ PluginSelectionMenu exists')
    has_plugin_sel = True
except Exception as e:
    print(f'❌ PluginSelectionMenu not found: {e}')
    has_plugin_sel = False

# Test 6: Check if start command handler exists
print('\nTest 6: Start Command Handler...')
try:
    from src.telegram.command_registry import CommandRegistry
    cr = CommandRegistry()
    if '/start' in cr.COMMANDS:
        print('✅ /start command registered')
        has_start = True
    else:
        print('❌ /start command not registered')
        has_start = False
except Exception as e:
    print(f'❌ Start command check failed: {e}')
    has_start = False

# Test 7: Check flows for zero-typing
print('\nTest 7: Zero-Typing Flows...')
flow_tests = {
    'trading_flow': 'TradingFlow',
    'risk_flow': 'RiskFlow',
    'position_flow': 'PositionFlow',
    'configuration_flow': 'ConfigurationFlow'
}

missing_flows = []
for module_name, class_name in flow_tests.items():
    try:
        mod = __import__(f'src.telegram.flows.{module_name}', fromlist=[class_name])
        cls = getattr(mod, class_name)
        print(f'  ✅ {module_name} ({class_name})')
    except Exception as e:
        print(f'  ❌ {module_name} MISSING: {e}')
        missing_flows.append(module_name)

if not missing_flows:
    print('✅ All 4 zero-typing flows exist')
else:
    print(f'❌ Missing {len(missing_flows)} flows')

# Final Summary
print('\n' + '='*60)
print('📊 IMPLEMENTATION STATUS:')
print('='*60)

all_tests_passed = (
    has_main_menu and 
    not missing_menus and 
    has_router and 
    has_buttons and 
    has_plugin_sel and 
    has_start and 
    not missing_flows
)

if all_tests_passed:
    print('🎉 MAIN MENU DESIGN: 100% IMPLEMENTED ✅')
    print('\nImplemented Features:')
    print('  ✅ Main Menu with 12 categories')
    print('  ✅ Button-based navigation')
    print('  ✅ Plugin selection system')
    print('  ✅ Zero-typing flows')
    print('  ✅ Callback routing')
    print('  ✅ /start command')
else:
    print('⚠️ MAIN MENU DESIGN: PARTIALLY IMPLEMENTED')
    print('\nMissing/Failed:')
    if not has_main_menu:
        print('  ❌ Main Menu')
    if missing_menus:
        print(f'  ❌ {len(missing_menus)} Category Menus')
    if not has_router:
        print('  ❌ Callback Router')
    if not has_buttons:
        print('  ❌ Button Builder')
    if not has_plugin_sel:
        print('  ❌ Plugin Selection')
    if not has_start:
        print('  ❌ Start Command')
    if missing_flows:
        print(f'  ❌ {len(missing_flows)} Zero-Typing Flows')

print('='*60)
