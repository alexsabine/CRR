"""Generate the P14-EMPTY1 worlds AFTER the freeze and anchor (step 6 of PREREG/README_FIRE.md). Writes RUNS/P14-EMPTY1-2026-10-07/raw/<id>.npz and prints the manifest records.
Target units W0001..W0600: families F1a, F1b, F2a, F2b x 150 seeds each (seed = 100000 + index). Control units: C_pos_long_stale P0001..P0600 (seed 200000+), C_neg_real_repeats N0001..N0600 (300000+), C_neg_frozen_world Z0001..Z0600 (400000+)."""
import json, pathlib, hashlib, sys, numpy as np
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); from worlds import generate, FAMILIES
HERE = pathlib.Path(__file__).resolve().parent; RAW = HERE.parents[1] / 'RUNS' / HERE.name / 'raw'; RAW.mkdir(parents=True, exist_ok=True)
def units():
    out = []
    fams = ['F1a', 'F1b', 'F2a', 'F2b']
    for i in range(600): out.append((f'W{i+1:04d}', fams[i // 150], 100000 + i))
    for i in range(600): out.append((f'P{i+1:04d}', 'C_pos_long_stale', 200000 + i))
    for i in range(600): out.append((f'N{i+1:04d}', 'C_neg_real_repeats', 300000 + i))
    for i in range(600): out.append((f'Z{i+1:04d}', 'C_neg_frozen_world', 400000 + i))
    return out
if __name__ == '__main__':
    recs = []
    for uid, fam, seed in units():
        w = generate(fam, seed); p = RAW / f'{uid}.npz'; np.savez(p, x=w['x'], y=w['y'], stale=w['stale'], family=fam, seed=seed)
        recs.append(dict(id=uid, path=str(p.relative_to(HERE.parents[1])), sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    print(json.dumps(dict(version='P14-EMPTY1 worlds v1 (generate.py frozen)', records=recs), indent=0))
