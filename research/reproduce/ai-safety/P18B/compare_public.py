"""Compare a re-run's public pilot JSON with the committed one, field by field. Written for this area (not part of the
study; MIT). Fields that cannot match by design are skipped and listed: run times, and the commitment, which hashes a
fresh random salt (pilot_p18b.py draws it with `secrets`; the original salt and sealed estimates were never committed).
    python3 compare_public.py <produced.json> <expected.json>"""
import json, sys
def skip(k): return k in ('runtime', 'commitment') or k.startswith(('cpu_s', 'wall_s')) or k.endswith('_utc')
def walk(a, b, path, out):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if skip(k): out['skipped'].add(k); continue
            walk(a.get(k), b.get(k), f'{path}.{k}', out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, f'{path}[{i}]', out)
    elif a != b: out['diff'].append(path)
    else: out['same'] += 1
out = dict(diff=[], same=0, skipped=set()); walk(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])), '', out)
print(f"{out['same']} fields equal; {len(out['diff'])} differ; skipped by design: {sorted(out['skipped'])}")
for p in out['diff'][:20]: print('  differs:', p)
sys.exit(1 if out['diff'] else 0)
