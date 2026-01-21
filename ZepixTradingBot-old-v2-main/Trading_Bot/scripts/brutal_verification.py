"""
BRUTAL HONEST VERIFICATION SCRIPT
Complete handler scan and plugin_context verification
"""

import re
import os

def scan_controller_bot():
    """Scan controller_bot.py for all registered command handlers."""
    
    filepath = r"Trading_Bot\src\telegram\controller_bot.py"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all command registrations
    command_registrations = re.findall(r'self\._command_handlers\["(/\w+)"\]\s*=\s*self\.(handle_\w+)', content)
    
    # Find all handler definitions with plugin_context
    plugin_aware_handlers = re.findall(r'def (handle_\w+)\([^)]*plugin_context[^)]*\)', content)
    
    # Find all handler definitions (total)
    all_handlers = re.findall(r'def (handle_\w+)\(', content)
    
    print("=" * 80)
    print("🚨 BRUTAL HONEST VERIFICATION REPORT")
    print("=" * 80)
    print()
    
    print(f"📊 COMMAND REGISTRATION COUNT:")
    print(f"   Total Registered Commands: {len(command_registrations)}")
    print()
    
    print(f"📊 HANDLER IMPLEMENTATION COUNT:")
    print(f"   Total Handler Functions: {len(set(all_handlers))}")
    print(f"   With plugin_context Parameter: {len(set(plugin_aware_handlers))}")
    print(f"   WITHOUT plugin_context: {len(set(all_handlers)) - len(set(plugin_aware_handlers))}")
    print()
    
    print("=" * 80)
    print("✅ HANDLERS WITH PLUGIN_CONTEXT (FULLY IMPLEMENTED):")
    print("=" * 80)
    for i, handler in enumerate(sorted(set(plugin_aware_handlers)), 1):
        print(f"   {i}. {handler}")
    
    print()
    print("=" * 80)
    print("❌ HANDLERS WITHOUT PLUGIN_CONTEXT (NOT IMPLEMENTED):")
    print("=" * 80)
    
    without_plugin = set(all_handlers) - set(plugin_aware_handlers)
    without_plugin = [h for h in without_plugin if h.startswith('handle_') and 'helper' not in h and 'send_' not in h and '_v3_' not in h and '_v6_' not in h]
    
    for i, handler in enumerate(sorted(without_plugin), 1):
        print(f"   {i}. {handler}")
    
    print()
    print("=" * 80)
    print("📋 ALL REGISTERED COMMANDS:")
    print("=" * 80)
    
    commands = sorted(set([cmd for cmd, handler in command_registrations]))
    for i, cmd in enumerate(commands, 1):
        # Check if handler has plugin_context
        handler_name = [h for c, h in command_registrations if c == cmd][0]
        status = "✅" if handler_name in plugin_aware_handlers else "❌"
        print(f"   {i}. {cmd:30s} {status}")
    
    print()
    print("=" * 80)
    print("🎯 SUMMARY:")
    print("=" * 80)
    print(f"   Total Commands: {len(commands)}")
    print(f"   Fully Implemented: {len([h for c, h in command_registrations if h in plugin_aware_handlers])}")
    print(f"   Missing Implementation: {len([h for c, h in command_registrations if h not in plugin_aware_handlers])}")
    print(f"   Implementation Rate: {(len([h for c, h in command_registrations if h in plugin_aware_handlers]) / len(commands) * 100):.1f}%")
    print()
    
    return {
        'total_commands': len(commands),
        'implemented': len([h for c, h in command_registrations if h in plugin_aware_handlers]),
        'missing': len([h for c, h in command_registrations if h not in plugin_aware_handlers])
    }

if __name__ == '__main__':
    result = scan_controller_bot()
    
    if result['missing'] > 0:
        print("🚨 WARNING: NOT ALL COMMANDS HAVE PLUGIN SELECTION IMPLEMENTED!")
        print(f"   Need to update: {result['missing']} handlers")
    else:
        print("✅ SUCCESS: ALL COMMANDS HAVE PLUGIN SELECTION!")

