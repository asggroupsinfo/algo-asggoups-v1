#!/usr/bin/env python3
"""Verify 144/144 commands"""

from src.telegram.command_registry import CommandRegistry

cr = CommandRegistry()
total = cr.get_command_count()

print(f"✅ TOTAL COMMANDS: {total}/144")
print(f"\nBREAKDOWN:")
for cat in cr.get_categories():
    cmds = cr.get_commands_by_category(cat)
    print(f"  {cat}: {len(cmds)} commands")

if total == 144:
    print(f"\n🎉 100% COMPLETE! ALL 144 COMMANDS REGISTERED!")
else:
    print(f"\n⚠️ Missing {144 - total} commands")
