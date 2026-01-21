#!/usr/bin/env python3
"""Full breakdown"""
from src.telegram.command_registry import CommandRegistry
from collections import defaultdict

cr = CommandRegistry()

# Group by category
by_category = defaultdict(list)
for cmd_name, cmd_def in cr.COMMANDS.items():
    by_category[cmd_def.category.value].append(cmd_name)

print(f"TOTAL: {len(cr.COMMANDS)}/144\n")
print("BY CATEGORY:")
for cat in sorted(by_category.keys()):
    cmds = sorted(by_category[cat])
    print(f"\n{cat}: {len(cmds)} commands")
    for cmd in cmds:
        print(f"  {cmd}")

print(f"\n{'='*60}")
print(f"TOTAL: {len(cr.COMMANDS)}/144")
if len(cr.COMMANDS) == 144:
    print("🎉 100% COMPLETE!")
else:
    print(f"⚠️  Missing {144 - len(cr.COMMANDS)} command(s)")
