"""Frozen scorer for P14-EMPTY1. Usage: python -I score.py <study_dir>  -> prints outcomes JSON (deterministic bytes). Reads RUNS/<study>/raw/*.npz written by generate.py.
Candidate: EMPTY. Baselines: strong_simple = HOLD, native_standard = GATED (chi-square 0.99 innovation gate), CRR_ablation = FROZEN. Metric: worlds.score on the stale+5 evaluation set (registered); sensitivity cells: stale-only and all-steps."""
import json, pathlib, sys, numpy as np
HERE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE)); from worlds import kalman_run, score
RAW = HERE.parents[1] / 'RUNS' / HERE.name / 'raw'; ARMS = ['EMPTY', 'HOLD', 'GATED', 'FROZEN']; BASE = {'strong_simple': 'HOLD', 'native_standard': 'GATED', 'CRR_ablation': 'FROZEN'}
def load(uid):
    z = np.load(RAW / f'{uid}.npz'); return dict(family=str(z['family']), seed=int(z['seed']), x=z['x'], y=z['y'], stale=z['stale'])
def rows(prefix, n, mode):
    out = []; excl = []
    for i in range(n):
        uid = f'{prefix}{i+1:04d}'; w = load(uid); res = {}
        for a in ARMS:
            m, v = kalman_run(w, a); res[a] = score(w, m, v, mode)
        if any(res[a] is None for a in ARMS): excl.append(dict(id=uid, reason='fewer than 10 evaluation steps')); continue
        out.append(dict(id=uid, candidate=round(res['EMPTY'], 10), baselines={k: round(res[v], 10) for k, v in BASE.items()}))
    return out, excl
if __name__ == '__main__':
    units, excl = rows('W', 600, 'stale_plus5')
    s1, _ = rows('W', 600, 'stale'); s2, _ = rows('W', 600, 'all')
    cp, _ = rows('P', 600, 'stale_plus5'); cn, _ = rows('N', 600, 'stale_plus5'); cz, _ = rows('Z', 600, 'stale_plus5')
    out = dict(study_id='P14-EMPTY1-2026-10-07', admissibility_open=True, raw_ids=[f'W{i+1:04d}' for i in range(600)], exclusions=excl, units=units,
               controls=[dict(id='pos_long_stale', expected='PASS', units=cp), dict(id='neg_real_repeats', expected='FAIL', units=cn), dict(id='neg_frozen_world', expected='FAIL', units=cz)],
               sensitivity=[dict(id='eval_stale_only', units=s1), dict(id='eval_all_steps', units=s2)])
    sys.stdout.write(json.dumps(out, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n')
