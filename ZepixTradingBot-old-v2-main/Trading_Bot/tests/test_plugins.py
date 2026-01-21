import sys
sys.path.insert(0, '.')

from src.config import Config

config = Config()

print("=" * 60)
print("PLUGIN CONFIGURATION CHECK")
print("=" * 60)

plugins = config.get('plugins', {})
print(f"\nFound {len([p for p in plugins if p != '_template'])} plugins:")

for name, cfg in plugins.items():
    if name != '_template':
        enabled = cfg.get('enabled', False)
        shadow = cfg.get('shadow_mode', False)
        status = "✅ ACTIVE" if enabled else "⏸️  DISABLED"
        mode = "(SHADOW)" if shadow else "(LIVE)"
        print(f"  {status} {name} {mode}")

print("\nV3 Integration:")
v3_config = config.get('v3_integration', {})
print(f"  Enabled: {v3_config.get('enabled', False)}")

print("\nPlugin System:")
plugin_system = config.get('plugin_system', {})
print(f"  Enabled: {plugin_system.get('enabled', False)}")
print(f"  Use Delegation: {plugin_system.get('use_delegation', False)}")

print("\n" + "=" * 60)
