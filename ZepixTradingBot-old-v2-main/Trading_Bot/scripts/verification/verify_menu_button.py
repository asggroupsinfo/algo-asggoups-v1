"""
SIMPLE TEST: Menu Button Command Count Verification
Checks telegram_bot.py source code directly without importing
"""

import re

def test_menu_button():
    """Parse telegram_bot.py and count menu button commands"""
    print("\n" + "="*70)
    print("🔍 MENU BUTTON SETUP VERIFICATION (Source Code Analysis)")
    print("="*70 + "\n")
    
    file_path = "src/clients/telegram_bot.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Test 1: Find setup_menu_button method
    print("📋 TEST 1: setup_menu_button Method")
    print("-" * 70)
    if "def setup_menu_button(self):" in content:
        print("✅ setup_menu_button method found")
    else:
        print("❌ setup_menu_button method NOT found")
        return False
    
    # Test 2: Count commands in setup_menu_button
    print("\n📋 TEST 2: Command Count in Menu Button")
    print("-" * 70)
    
    # Extract setup_menu_button method
    setup_start = content.find("def setup_menu_button(self):")
    setup_end = content.find("\n    def ", setup_start + 1)
    setup_method = content[setup_start:setup_end]
    
    # Count {"command": "xxx", "description": "yyy"} patterns
    command_pattern = r'\{"command":\s*"([^"]+)",\s*"description":\s*"([^"]+)"\}'
    commands = re.findall(command_pattern, setup_method)
    
    print(f"✅ Total commands in menu button: {len(commands)}")
    
    # Test 3: Verify categories
    print("\n📋 TEST 3: Categories in Menu Button")
    print("-" * 70)
    
    category_pattern = r'CATEGORY \d+:\s*([A-Z\s/&-]+)'
    categories = re.findall(category_pattern, setup_method)
    
    print(f"✅ Total categories: {len(categories)}")
    for i, cat in enumerate(categories, 1):
        print(f"   {i}. {cat.strip()}")
    
    # Test 4: Verify /help command in menu
    print("\n📋 TEST 4: /help Command in Menu")
    print("-" * 70)
    
    help_commands = [cmd for cmd, desc in commands if cmd == "help"]
    if help_commands:
        print("✅ /help command found in menu button")
        # Find description
        for cmd, desc in commands:
            if cmd == "help":
                print(f"   Description: {desc}")
    else:
        print("❌ /help command NOT in menu button")
    
    # Test 5: Check command_handlers dict
    print("\n📋 TEST 5: Command Handlers Dictionary")
    print("-" * 70)
    
    # Find command_handlers
    handlers_start = content.find("self.command_handlers = {")
    handlers_end = content.find("\n        }", handlers_start) + 10
    handlers_section = content[handlers_start:handlers_end]
    
    # Count handlers
    handler_pattern = r'"/([^"]+)":\s*self\.handle_'
    handlers = re.findall(handler_pattern, handlers_section)
    
    print(f"✅ Total command handlers: {len(handlers)}")
    
    # Check if /help is registered
    if "help" in handlers:
        print("✅ /help registered in command_handlers")
    else:
        print("❌ /help NOT registered in command_handlers")
    
    # Test 6: Verify handle_help method exists
    print("\n📋 TEST 6: handle_help Method")
    print("-" * 70)
    
    if "def handle_help(self, message):" in content:
        print("✅ handle_help method exists")
        
        # Extract help text to count commands shown
        help_start = content.find("def handle_help(self, message):")
        help_end = content.find("\n    def ", help_start + 1)
        help_method = content[help_start:help_end]
        
        # Count /commands in help text
        help_cmd_pattern = r'/(\w+)\s*-'
        help_commands_listed = re.findall(help_cmd_pattern, help_method)
        print(f"✅ Commands listed in help: {len(help_commands_listed)}")
        
    else:
        print("❌ handle_help method NOT found")
    
    # Test 7: Show command breakdown by category
    print("\n📋 TEST 7: Commands by Category")
    print("-" * 70)
    
    current_category = ""
    category_commands = {}
    
    lines = setup_method.split('\n')
    for line in lines:
        if "CATEGORY" in line:
            cat_match = re.search(r'CATEGORY \d+:\s*([A-Z\s/&-]+)', line)
            if cat_match:
                current_category = cat_match.group(1).strip()
                category_commands[current_category] = []
        
        cmd_match = re.search(r'\{"command":\s*"([^"]+)"', line)
        if cmd_match and current_category:
            category_commands[current_category].append(cmd_match.group(1))
    
    for cat, cmds in category_commands.items():
        print(f"✅ {cat}: {len(cmds)} commands")
    
    # Final Summary
    print("\n" + "="*70)
    print("📊 FINAL VERIFICATION RESULTS")
    print("="*70)
    print(f"✅ Menu Button Commands: {len(commands)}")
    print(f"✅ Command Handler Functions: {len(handlers)}")
    print(f"✅ Categories: {len(categories)}")
    print(f"✅ /help in Menu: {'YES' if help_commands else 'NO'}")
    print(f"✅ /help Handler: {'YES' if 'help' in handlers else 'NO'}")
    print(f"✅ handle_help Method: {'YES' if 'def handle_help' in content else 'NO'}")
    
    total_category_cmds = sum(len(cmds) for cmds in category_commands.values())
    print(f"\n📈 Total Commands Across Categories: {total_category_cmds}")
    
    # Calculate completeness
    if len(commands) >= 75 and len(categories) >= 12 and help_commands:
        print("\n🎉 MENU BUTTON IMPLEMENTATION: COMPLETE!")
        print("✅ All 12 categories present")
        print("✅ 75+ commands organized")
        print("✅ /help command integrated")
        return True
    else:
        print("\n⚠️ MENU BUTTON IMPLEMENTATION: NEEDS REVIEW")
        return False

if __name__ == "__main__":
    import sys
    success = test_menu_button()
    sys.exit(0 if success else 1)
