"""Recompute P14-EMPTY1's decision table from outcomes.json with the locked generic engine (scripts/guard.py).
Written for this reproduce area (not frozen; MIT). It calls guard.verify_freeze and guard.decision exactly as
guard.score does, but skips guard.score's receipt checks (OpenTimestamps verification, signed tag, reviewer name),
which an outside reader cannot complete. Usage, from the staged work tree:
    python3 -I -B decide.py <work>/studies/P14-EMPTY1-2026-10-07 <outcomes.json>"""
import json, pathlib, sys
study = pathlib.Path(sys.argv[1]).resolve(); sys.path.insert(0, str(study.parents[1] / 'scripts')); import guard
p = guard.verify_freeze(study); o = json.loads(pathlib.Path(sys.argv[2]).read_bytes())
d = guard.decision(p, o['units'])
print(f"primary: n {d['n']}  wins {d['wins']}  fraction {d['fraction']:.3f}  mean delta {d['mean_delta']:+.4f}  Hoeffding lower {d['lower_bound']:+.4f}  threshold met {d['threshold_met']}")
flips = 0
for c in o['sensitivity']:
    s = guard.decision(p, c['units']); flips += s['threshold_met'] != d['threshold_met']
    print(f"sensitivity {c['id']}: mean delta {s['mean_delta']:+.4f}  threshold met {s['threshold_met']}")
for c in o['controls']:
    s = guard.decision(p, c['units'])
    print(f"control {c['id']} (expected {c['expected']}): mean delta {s['mean_delta']:+.4f}  threshold met {s['threshold_met']}")
guard.control_metrics(p, o['controls'])
print(f"controls as registered: yes; sensitivity flips {flips} (limit {p['max_sensitivity_flips']}); exclusions {len(o['exclusions'])}")
print('verdict word the engine would record once receipts are complete:', 'PASS-0' if d['threshold_met'] else 'FAIL', '(ceiling PASS-0; the record claims no verdict word until a reviewer completes the receipt)')
