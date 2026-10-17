"""Build the numerically scored control battery BEFORE the freeze (README_FIRE step 3; the locked guard.protocol runs decision() on controls.json).
Generates the control worlds (seeds 200000+, 300000+, 400000+) into RUNS/<study>/raw/ and writes controls.json with one unit row per control world, scored exactly as score.py scores the targets.
The target worlds (seeds 100000+) are NOT generated here; generate.py writes them after the freeze and anchor (and rewrites the control worlds byte-identically)."""
import json, pathlib, sys, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); from worlds import generate, kalman_run, score
RAW = HERE.parents[1] / 'RUNS' / HERE.name / 'raw'; RAW.mkdir(parents=True, exist_ok=True)
ARMS = ['EMPTY', 'HOLD', 'GATED', 'FROZEN']; BASE = {'strong_simple': 'HOLD', 'native_standard': 'GATED', 'CRR_ablation': 'FROZEN'}
SPEC = [('pos_long_stale', 'PASS', 'P', 'C_pos_long_stale', 200000), ('neg_real_repeats', 'FAIL', 'N', 'C_neg_real_repeats', 300000), ('neg_frozen_world', 'FAIL', 'Z', 'C_neg_frozen_world', 400000)]
out = []
for cid, exp, prefix, fam, base in SPEC:
    units = []
    for i in range(600):
        uid = f'{prefix}{i+1:04d}'; w = generate(fam, base + i); np.savez(RAW / f'{uid}.npz', x=w['x'], y=w['y'], stale=w['stale'], family=fam, seed=base + i)
        res = {a: score(w, *kalman_run(w, a), 'stale_plus5') for a in ARMS}
        if any(res[a] is None for a in ARMS): continue
        units.append(dict(id=uid, candidate=round(res['EMPTY'], 10), baselines={k: round(res[v], 10) for k, v in BASE.items()}))
    out.append(dict(id=cid, expected=exp, units=units)); print(cid, exp, len(units), 'mean delta %.4f' % np.mean([u['candidate'] - max(u['baselines'].values()) for u in units]))
json.dump(out, open(HERE / 'controls.json', 'w'), separators=(',', ':'))
