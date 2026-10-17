"""Paired seed-level contrasts for outputs/loop_runs.jsonl (development): per-seed detection score (1 - delay/H; 0 for a miss or an
alarm more than 5 rounds before divergence), differences prov - rival with 95 % percentile bootstrap intervals (B 4000,
default_rng(0)); localisation accuracy differences prov - event and prov - intervention. Writes outputs/loop_contrasts.json."""
import sys; sys.dont_write_bytecode = True
import json, pathlib, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; H = 80
R = [json.loads(l) for l in open(HERE / 'outputs' / 'loop_runs.jsonl')]
def score(r, k):
    a, d = r['alarm_' + k], r['div']
    return 0.0 if a is None or a < d - 5 else 1 - (max(a, d) - d)/H
def boot(x, B=4000):
    x = np.asarray(x, float); rng = np.random.default_rng(0); m = [float(np.mean(x[rng.integers(0, len(x), len(x))])) for _ in range(B)]
    return [round(float(np.mean(x)), 4), round(float(np.percentile(m, 2.5)), 4), round(float(np.percentile(m, 97.5)), 4)]
out = {}
for w in sorted({r['world'] for r in R}):
    rr = [r for r in R if r['world'] == w and r['div'] is not None]
    if not rr: continue
    e = {f'prov-{k}': boot([score(r, 'prov') - score(r, k) for r in rr]) for k in ('bbsd', 'inshift', 'prov_abl')}
    L = [r for r in rr if 'loc' in r]
    if L:
        e['loc prov-event'] = boot([(r['loc']['prov'] == r['G'][0]) - (r['loc']['event'] == r['G'][0]) for r in L])
        e['loc prov-intervention'] = boot([(r['loc']['prov'] == r['G'][0]) - (r['loc']['intervention'] == r['G'][0]) for r in L if 'intervention' in r['loc']])
    out[w] = e
json.dump(out, open(HERE / 'outputs' / 'loop_contrasts.json', 'w'), indent=1); print(json.dumps(out, indent=1))
