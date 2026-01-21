import json

def find_path(d, target, path=''):
    for k, v in d.items():
        if k == target:
            return path + k
        if isinstance(v, dict):
            r = find_path(v, target, path + k + '/')
            if r:
                return r
    return None

c = json.load(open('config/config.json', 'r', encoding='utf-8'))

rm_path = find_path(c, 'recovery_monitoring')
slo_path = find_path(c, 'sl_reduction_optimization')

print(f"recovery_monitoring path: {rm_path}")
print(f"sl_reduction_optimization path: {slo_path}")

# Now get the actual values
parts = rm_path.split('/')
obj = c
for part in parts[:-1]:
    obj = obj[part]
print(f"\nrecovery_monitoring config: {obj.get('recovery_monitoring', {})}")

parts = slo_path.split('/')
obj = c
for part in parts[:-1]:
    obj = obj[part]
print(f"\nsl_reduction_optimization config: {obj.get('sl_reduction_optimization', {})}")
