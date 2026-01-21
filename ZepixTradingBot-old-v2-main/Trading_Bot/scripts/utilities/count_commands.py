#!/usr/bin/env python3
"""Count commands"""
import re

with open('src/telegram/command_registry.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all command definitions
commands = re.findall(r'\"(/\w+)\":\s+CommandDefinition', content)

print(f"✅ Total Commands Found: {len(commands)}")
print(f"\nCommands List ({len(commands)}):")
for i, cmd in enumerate(sorted(commands), 1):
    print(f"{i:3d}. {cmd}")
