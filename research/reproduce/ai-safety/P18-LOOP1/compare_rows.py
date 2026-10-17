"""Compare a (possibly reduced) loopworld.py run with the committed rows. Written for this area (not part of the study; MIT).
A run with n_cal = 200 uses the same detector thresholds as the committed run, and test seed s of world w is simulated
identically whatever n_test is, so every produced row must equal the committed row with the same (world, seed).
    python3 compare_rows.py <produced loop_runs.jsonl> <expected loop_runs.jsonl>"""
import json, sys
prod = [json.loads(l) for l in open(sys.argv[1])]; exp = {(r['world'], r['seed']): r for r in map(json.loads, open(sys.argv[2]))}
diff = [(r['world'], r['seed']) for r in prod if exp.get((r['world'], r['seed'])) != r]
print(f'{len(prod)} produced rows; {len(prod) - len(diff)} identical to the committed row with the same (world, seed); {len(diff)} differ')
if diff: print('first differing:', diff[:5]); sys.exit(1)
