"""Generate the P16-PAUSE1 worlds after the freeze and anchor: writes RUNS/<study>/raw/<id>.npz and prints the manifest. Cells (declared): perfect-restart main cells M1 (p 0.3, L 5, c 0), M2 (p 0.1, L 1, c 0), M3 (p 0.3, L 5, c 0.05); controls C_restart (q 0.2), C_deadline (kappa 0.1), C_trivial (p 0: no interruptions, the capability gate must close there). 100 seeds per cell, seed = base + i."""
import json, pathlib, hashlib, sys, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE)); from worlds_p16 import make_world
RAW = HERE.parents[1] / 'RUNS' / HERE.name / 'raw'; RAW.mkdir(parents=True, exist_ok=True)
CELLS = {'M1': (dict(p=0.3, L=5, c=0.0), 100000), 'M2': (dict(p=0.1, L=1, c=0.0), 110000), 'M3': (dict(p=0.3, L=5, c=0.05), 120000), 'C_restart': (dict(p=0.3, L=5, q=0.2), 200000), 'C_deadline': (dict(p=0.3, L=5, kappa=0.1), 210000), 'C_trivial': (dict(p=0.0, L=5), 220000)}
def units():
    return [(f'{cell}-{i+1:03d}', cell, base + i, cfg) for cell, (cfg, base) in CELLS.items() for i in range(100)]
if __name__ == '__main__':
    recs = []
    for uid, cell, seed, cfg in units():
        w = make_world(seed, **cfg); p = RAW / f'{uid}.npz'; np.savez(p, P=w['P'], R=w['R'], intr=w['intr'], seed=seed, cell=cell, cfg=json.dumps(cfg))
        recs.append(dict(id=uid, path=f'raw/{uid}.npz', sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    print(json.dumps(dict(version='P16-PAUSE1 worlds v1 (generate_p16.py frozen)', records=recs), indent=0))
