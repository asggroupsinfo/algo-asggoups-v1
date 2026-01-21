"""
VISUAL CAPABILITIES IMPLEMENTATION REALITY CHECK
Document: 12_VISUAL_CAPABILITIES_GUIDE.md

Checks all 10 visual features documented:
1. Rich Text Formatting (HTML)
2. Enhanced Inline Keyboards
3. Reply Keyboards
4. Menu Button Setup
5. Chat Actions
6. Rich Notification Templates
7. Media Messages
8. Progress Indicators
9. Template System
10. Menu Organization
"""

import sys
import os
from pathlib import Path

print("="*80)
print("VISUAL CAPABILITIES IMPLEMENTATION REALITY CHECK")
print("Document: 12_VISUAL_CAPABILITIES_GUIDE.md")
print("="*80)

# Test results
results = {
    "features_expected": 10,
    "features_found": 0,
    "features_missing": [],
    "features_partial": [],
    "details": {}
}

def check_feature(name: str, check_func, partial_ok=False):
    """Check if a feature is implemented"""
    try:
        result = check_func()
        if result == "FULL":
            print(f"✅ {name} - FULLY IMPLEMENTED")
            results["features_found"] += 1
            results["details"][name] = "FULL"
        elif result == "PARTIAL":
            print(f"⚠️  {name} - PARTIALLY IMPLEMENTED")
            results["features_partial"].append(name)
            results["details"][name] = "PARTIAL"
        else:
            print(f"❌ {name} - NOT FOUND")
            results["features_missing"].append(name)
            results["details"][name] = "MISSING"
        return result
    except Exception as e:
        print(f"❌ {name} - ERROR: {e}")
        results["features_missing"].append(name)
        results["details"][name] = f"ERROR: {e}"
        return "MISSING"

# Feature 1: Rich Text Formatting (HTML)
print("\n📝 FEATURE 1: RICH TEXT FORMATTING (HTML)")
print("-"*80)

def check_html_formatting():
    """Check if HTML formatting is used"""
    from src.telegram.notification_templates import NotificationTemplates
    
    # Check if templates use HTML tags
    entry_template = NotificationTemplates.ENTRY_TEMPLATE
    
    html_tags = ['<b>', '<i>', '<code>', '<pre>']
    found_tags = [tag for tag in html_tags if tag in entry_template]
    
    if len(found_tags) >= 2:
        print(f"  Found HTML tags: {', '.join(found_tags)}")
        return "FULL"
    return "MISSING"

check_feature("Rich HTML Formatting", check_html_formatting)

# Feature 2: Enhanced Inline Keyboards
print("\n🎹 FEATURE 2: ENHANCED INLINE KEYBOARDS")
print("-"*80)

def check_inline_keyboards():
    """Check inline keyboard implementation"""
    from src.telegram.menu_builder import MenuBuilder
    
    builder = MenuBuilder()
    
    # Check if builder has required methods
    required_methods = ['build_inline_keyboard', 'build_main_menu', 'build_confirmation_menu']
    found_methods = [m for m in required_methods if hasattr(builder, m)]
    
    print(f"  Found methods: {len(found_methods)}/{len(required_methods)}")
    
    if len(found_methods) >= 2:
        return "FULL"
    elif len(found_methods) >= 1:
        return "PARTIAL"
    return "MISSING"

check_feature("Enhanced Inline Keyboards", check_inline_keyboards)

# Feature 3: Reply Keyboards
print("\n⌨️ FEATURE 3: REPLY KEYBOARDS")
print("-"*80)

def check_reply_keyboards():
    """Check reply keyboard implementation"""
    try:
        # Re-import to get latest code
        import importlib
        import src.clients.telegram_bot
        importlib.reload(src.clients.telegram_bot)
        from src.clients.telegram_bot import TelegramBot
        
        # Check for reply keyboard methods
        if hasattr(TelegramBot, 'send_message_with_reply_keyboard'):
            print("  Found method: send_message_with_reply_keyboard")
            return "FULL"
        
        # Check for keyboard-related code
        import inspect
        source = inspect.getsource(TelegramBot)
        
        keywords = ['ReplyKeyboardMarkup', 'KeyboardButton', 'reply_keyboard', 'resize_keyboard']
        found = [kw for kw in keywords if kw in source]
        
        print(f"  Found keywords: {found}")
        
        if len(found) >= 3:
            return "FULL"
        elif len(found) >= 1:
            return "PARTIAL"
        return "MISSING"
    except Exception as e:
        print(f"  Error: {e}")
        return "MISSING"

check_feature("Reply Keyboards", check_reply_keyboards)

# Feature 4: Menu Button Setup
print("\n📱 FEATURE 4: MENU BUTTON SETUP")
print("-"*80)

def check_menu_button():
    """Check menu button setup"""
    try:
        # Re-import to get latest code
        import importlib
        import src.clients.telegram_bot
        importlib.reload(src.clients.telegram_bot)
        from src.clients.telegram_bot import TelegramBot
        
        # Check if setup_menu_button method exists
        if hasattr(TelegramBot, 'setup_menu_button'):
            print("  Found method: setup_menu_button")
            return "FULL"
        
        import inspect
        source = inspect.getsource(TelegramBot)
        
        keywords = ['set_my_commands', 'setMyCommands', 'BotCommand']
        found = [kw for kw in keywords if kw in source]
        
        print(f"  Found keywords: {found}")
        
        if len(found) >= 1:
            return "FULL"
        return "MISSING"
    except Exception as e:
        print(f"  Error: {e}")
        return "MISSING"

check_feature("Menu Button Setup", check_menu_button)

# Feature 5: Chat Actions
print("\n💬 FEATURE 5: CHAT ACTIONS")
print("-"*80)

def check_chat_actions():
    """Check chat action implementation"""
    try:
        from src.clients.telegram_bot import TelegramBot
        import inspect
        source = inspect.getsource(TelegramBot)
        
        keywords = ['send_chat_action', 'ChatAction', 'typing']
        found = [kw for kw in keywords if kw in source]
        
        print(f"  Found keywords: {found}")
        
        if 'send_chat_action' in source or 'sendChatAction' in source:
            return "FULL"
        return "MISSING"
    except:
        return "MISSING"

check_feature("Chat Actions", check_chat_actions)

# Feature 6: Rich Notification Templates
print("\n📋 FEATURE 6: RICH NOTIFICATION TEMPLATES")
print("-"*80)

def check_notification_templates():
    """Check notification template system"""
    from src.telegram.notification_templates import NotificationTemplates
    
    # Check for various templates
    templates = [
        'ENTRY_TEMPLATE',
        'EXIT_TEMPLATE',
        'TP_HIT_TEMPLATE',
        'SL_HIT_TEMPLATE'
    ]
    
    found = [t for t in templates if hasattr(NotificationTemplates, t)]
    
    print(f"  Found templates: {len(found)}/{len(templates)}")
    for t in found:
        print(f"    ✅ {t}")
    
    if len(found) >= 3:
        return "FULL"
    elif len(found) >= 1:
        return "PARTIAL"
    return "MISSING"

check_feature("Rich Notification Templates", check_notification_templates)

# Feature 7: Progress Indicators
print("\n📊 FEATURE 7: PROGRESS INDICATORS")
print("-"*80)

def check_progress_indicators():
    """Check progress indicator implementation"""
    try:
        from src.telegram.notification_templates import create_progress_bar
        
        # Test progress bar
        bar = create_progress_bar(50, 100)
        print(f"  Sample progress bar: {bar}")
        
        if bar and len(bar) > 0:
            return "FULL"
        return "MISSING"
    except Exception as e:
        print(f"  Error: {e}")
        return "MISSING"

check_feature("Progress Indicators", check_progress_indicators)

# Feature 8: Menu Organization
print("\n📂 FEATURE 8: MENU ORGANIZATION")
print("-"*80)

def check_menu_organization():
    """Check menu organization structure"""
    try:
        from src.menu.menu_manager import MenuManager
        import inspect
        
        # Check for menu hierarchy
        source = inspect.getsource(MenuManager)
        
        menu_types = ['main_menu', 'submenu', 'category', 'navigation']
        found = [m for m in menu_types if m in source.lower()]
        
        print(f"  Found menu types: {len(found)}")
        
        if len(found) >= 2:
            return "FULL"
        elif len(found) >= 1:
            return "PARTIAL"
        return "MISSING"
    except:
        return "MISSING"

check_feature("Menu Organization", check_menu_organization)

# Feature 9: Media Messages
print("\n🖼️ FEATURE 9: MEDIA MESSAGES")
print("-"*80)

def check_media_messages():
    """Check media message support"""
    try:
        from src.clients.telegram_bot import TelegramBot
        import inspect
        source = inspect.getsource(TelegramBot)
        
        media_keywords = ['send_photo', 'send_document', 'sendPhoto', 'sendDocument']
        found = [kw for kw in media_keywords if kw in source]
        
        print(f"  Found media methods: {found}")
        
        if len(found) >= 2:
            return "FULL"
        elif len(found) >= 1:
            return "PARTIAL"
        return "MISSING"
    except:
        return "MISSING"

check_feature("Media Messages", check_media_messages)

# Feature 10: Template Helper Functions
print("\n🛠️ FEATURE 10: TEMPLATE HELPER FUNCTIONS")
print("-"*80)

def check_template_helpers():
    """Check template helper functions"""
    try:
        from src.telegram import notification_templates
        import inspect
        
        # Check for helper functions
        members = inspect.getmembers(notification_templates, inspect.isfunction)
        helper_functions = [name for name, _ in members if not name.startswith('_')]
        
        print(f"  Found helper functions: {len(helper_functions)}")
        for func in helper_functions[:5]:  # Show first 5
            print(f"    • {func}")
        
        if len(helper_functions) >= 3:
            return "FULL"
        elif len(helper_functions) >= 1:
            return "PARTIAL"
        return "MISSING"
    except:
        return "MISSING"

check_feature("Template Helper Functions", check_template_helpers)

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)

total_features = results["features_expected"]
full_features = results["features_found"]
partial_features = len(results["features_partial"])
missing_features = len(results["features_missing"])

implementation_rate = (full_features / total_features * 100) if total_features > 0 else 0
partial_rate = (partial_features / total_features * 100) if total_features > 0 else 0

print(f"\n📊 Implementation Status:")
print(f"   Total Features: {total_features}")
print(f"   ✅ Fully Implemented: {full_features} ({implementation_rate:.1f}%)")
print(f"   ⚠️  Partially Implemented: {partial_features} ({partial_rate:.1f}%)")
print(f"   ❌ Missing: {missing_features}")

if missing_features > 0:
    print(f"\n❌ Missing Features:")
    for feature in results["features_missing"]:
        print(f"   • {feature}")

if partial_features > 0:
    print(f"\n⚠️  Partial Features (Need Enhancement):")
    for feature in results["features_partial"]:
        print(f"   • {feature}")

print("\n" + "="*80)

if full_features == total_features:
    print("✅ EXCELLENT - All visual features fully implemented!")
    sys.exit(0)
elif full_features + partial_features >= total_features * 0.7:
    print(f"⚠️  GOOD - {implementation_rate:.0f}% implemented, needs enhancement")
    sys.exit(0)
else:
    print(f"❌ INCOMPLETE - Only {implementation_rate:.0f}% implemented")
    sys.exit(1)
