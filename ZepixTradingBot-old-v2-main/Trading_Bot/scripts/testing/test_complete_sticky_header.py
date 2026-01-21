#!/usr/bin/env python3
"""
COMPLETE STICKY HEADER IMPLEMENTATION TEST
Tests all features from sticky_header_builder.py
"""
import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

print('='*70)
print('🧪 COMPLETE STICKY HEADER IMPLEMENTATION TEST')
print('='*70)

passed = []
failed = []

def test(name):
    def decorator(func):
        try:
            if asyncio.iscoroutinefunction(func):
                result = asyncio.run(func())
            else:
                result = func()
            
            if result:
                passed.append(name)
                print(f'✅ {name}')
            else:
                failed.append(f'{name}: Returned False')
                print(f'❌ {name}: Failed')
        except Exception as e:
            failed.append(f'{name}: {str(e)[:80]}')
            print(f'⚠️ {name}: {str(e)[:80]}')
        return func
    return decorator

print('\n' + '='*70)
print('📦 SECTION 1: MODULE IMPORTS')
print('='*70)

@test('1.1: Import sticky_header_builder module')
def _():
    from src.telegram import sticky_header_builder
    return sticky_header_builder is not None

@test('1.2: Import StickyHeaderBuilder class')
def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    return StickyHeaderBuilder is not None

@test('1.3: Import session functions')
def _():
    from src.telegram.sticky_header_builder import get_current_session, get_session_time_remaining
    return get_current_session is not None and get_session_time_remaining is not None

@test('1.4: Import price functions')
def _():
    from src.telegram.sticky_header_builder import get_live_symbol_prices, format_symbol_prices
    return get_live_symbol_prices is not None and format_symbol_prices is not None

@test('1.5: Import status function')
def _():
    from src.telegram.sticky_header_builder import get_bot_status
    return get_bot_status is not None

@test('1.6: Import clock function')
def _():
    from src.telegram.sticky_header_builder import get_current_time_display
    return get_current_time_display is not None

print('\n' + '='*70)
print('🕐 SECTION 2: CLOCK COMPONENT')
print('='*70)

@test('2.1: Clock displays GMT time')
def _():
    from src.telegram.sticky_header_builder import get_current_time_display
    time_display = get_current_time_display()
    return '🕐' in time_display and 'GMT' in time_display and ':' in time_display

@test('2.2: Clock format is HH:MM:SS')
def _():
    from src.telegram.sticky_header_builder import get_current_time_display
    from datetime import datetime
    time_display = get_current_time_display()
    # Should contain something like "14:35:22"
    return time_display.count(':') >= 2

print('\n' + '='*70)
print('📈 SECTION 3: SESSION MANAGEMENT')
print('='*70)

@test('3.1: Session detection works')
def _():
    from src.telegram.sticky_header_builder import get_current_session
    session_text, active_list = get_current_session()
    return session_text is not None and isinstance(active_list, list)

@test('3.2: Session data structure exists')
def _():
    from src.telegram.sticky_header_builder import TRADING_SESSIONS
    return len(TRADING_SESSIONS) == 4

@test('3.3: All 4 sessions defined')
def _():
    from src.telegram.sticky_header_builder import TRADING_SESSIONS
    required = ['SYDNEY', 'TOKYO', 'LONDON', 'NEW YORK']
    return all(session in TRADING_SESSIONS for session in required)

@test('3.4: Session time remaining works')
def _():
    from src.telegram.sticky_header_builder import get_session_time_remaining
    time_remaining = get_session_time_remaining()
    return time_remaining is not None and len(time_remaining) > 0

print('\n' + '='*70)
print('💱 SECTION 4: SYMBOL PRICES')
print('='*70)

@test('4.1: Default symbols defined')
async def _():
    from src.telegram.sticky_header_builder import DEFAULT_HEADER_SYMBOLS
    return len(DEFAULT_HEADER_SYMBOLS) == 4

@test('4.2: Get live prices works')
async def _():
    from src.telegram.sticky_header_builder import get_live_symbol_prices
    prices = await get_live_symbol_prices()
    return isinstance(prices, dict) and len(prices) > 0

@test('4.3: Price formatting works')
async def _():
    from src.telegram.sticky_header_builder import format_symbol_prices
    test_prices = {'EURUSD': 1.08245, 'GBPUSD': 1.26450}
    formatted = format_symbol_prices(test_prices)
    return 'EUR' in formatted and 'GBP' in formatted

@test('4.4: Price formatting uses 4 decimals for EUR')
async def _():
    from src.telegram.sticky_header_builder import format_symbol_prices
    test_prices = {'EURUSD': 1.08245}
    formatted = format_symbol_prices(test_prices)
    # Should have exactly 4 decimal places (check the format, not exact value due to rounding)
    import re
    # Pattern: EUR:X.XXXX (4 digits after decimal)
    pattern = r'EUR:\d+\.\d{4}'
    return re.search(pattern, formatted) is not None

@test('4.5: Price formatting uses 2 decimals for JPY')
async def _():
    from src.telegram.sticky_header_builder import format_symbol_prices
    test_prices = {'USDJPY': 151.205}
    formatted = format_symbol_prices(test_prices)
    # Should have exactly 2 decimal places
    return '151.21' in formatted or '151.20' in formatted

@test('4.6: Price change indicators work')
def _():
    from src.telegram.sticky_header_builder import get_price_with_change
    # Test upward change
    result = get_price_with_change('EURUSD', 1.0825, 1.0800)
    return '🟢' in result or '⬆' in result

print('\n' + '='*70)
print('🤖 SECTION 5: BOT STATUS')
print('='*70)

@test('5.1: Bot status function works')
def _():
    from src.telegram.sticky_header_builder import get_bot_status
    status_text, status_type = get_bot_status()
    return status_text is not None and status_type is not None

@test('5.2: Status returns expected format')
def _():
    from src.telegram.sticky_header_builder import get_bot_status
    status_text, status_type = get_bot_status()
    # Should contain one of the status indicators
    indicators = ['✅', '⏸️', '⚠️', '❌', '⛔']
    return any(ind in status_text for ind in indicators)

print('\n' + '='*70)
print('🎨 SECTION 6: HEADER BUILDER')
print('='*70)

@test('6.1: StickyHeaderBuilder initializes')
def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    return builder is not None

@test('6.2: Full header builds successfully')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_full_header()
    return header is not None and len(header) > 0

@test('6.3: Full header contains all components')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_full_header()
    # Check for key elements
    return all(elem in header for elem in ['🤖', '📊', '🕐', '📈', '💱'])

@test('6.4: Full header is 8-line box')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_full_header()
    lines = header.strip().split('\n')
    return len(lines) == 8

@test('6.5: Full header has box borders')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_full_header()
    # Check for box drawing characters
    return '╔' in header and '╚' in header and '║' in header

@test('6.6: Compact header builds successfully')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_compact_header()
    return header is not None and len(header) > 0

@test('6.7: Compact header is 3 lines')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_compact_header()
    lines = header.strip().split('\n')
    return len(lines) == 3

@test('6.8: Compact header has separator')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_compact_header()
    return '━' in header

@test('6.9: Minimal header builds successfully')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_minimal_header()
    return header is not None and len(header) > 0

@test('6.10: Minimal header is 1 line')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    header = await builder.build_minimal_header()
    lines = header.strip().split('\n')
    return len(lines) == 1

@test('6.11: build_header method with style parameter')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    full = await builder.build_header('full')
    compact = await builder.build_header('compact')
    minimal = await builder.build_header('minimal')
    return all([full, compact, minimal])

print('\n' + '='*70)
print('✨ SECTION 7: INTEGRATION TEST')
print('='*70)

@test('7.1: StickyHeader class has build_header method')
def _():
    from src.telegram.sticky_headers import StickyHeader
    return hasattr(StickyHeader, 'build_header')

@test('7.2: Send message helper function exists')
def _():
    from src.telegram.sticky_header_builder import send_message_with_header
    return send_message_with_header is not None

@test('7.3: All header templates work together')
async def _():
    from src.telegram.sticky_header_builder import StickyHeaderBuilder
    builder = StickyHeaderBuilder()
    
    full = await builder.build_full_header()
    compact = await builder.build_compact_header()
    minimal = await builder.build_minimal_header()
    
    # All should be different
    return full != compact and compact != minimal and full != minimal

print('\n' + '='*70)
print('📊 FINAL RESULTS')
print('='*70)

total = len(passed) + len(failed)
pass_rate = (len(passed) / total * 100) if total > 0 else 0

print(f'\n✅ PASSED: {len(passed)}/{total} ({pass_rate:.1f}%)')
print(f'❌ FAILED: {len(failed)}/{total}')

if failed:
    print('\n' + '='*70)
    print('❌ FAILED TESTS:')
    print('='*70)
    for failure in failed:
        print(f'  • {failure}')

print('\n' + '='*70)
if pass_rate == 100:
    print('🎉 ALL TESTS PASSED - IMPLEMENTATION COMPLETE!')
elif pass_rate >= 90:
    print('✨ EXCELLENT - Implementation nearly complete!')
elif pass_rate >= 75:
    print('👍 GOOD - Most features implemented!')
else:
    print('⚠️ NEEDS WORK - More implementation required')
print('='*70)

sys.exit(0 if pass_rate == 100 else 1)
