"""SEC-PG-LLM-H runner (frozen). From Phoenix_Egg/: python3 -I studies/SEC-PG-LLM-H-2026-10-08/run_heldout.py <workers> [stage]
stage: pretrain | main | sens | rerun | all (default all, in that order). Every job appends one JSON line to RUNS/<id>/units_<stage>.jsonl
and is skipped if already present, so an interrupted run resumes without re-running completed jobs (a truncated line is ignored and its
job re-run; a pretraining cache file left truncated by an interruption is rebuilt from scratch, which is deterministic).
Refuses to start unless the frozen folder is unchanged (data_step.frozen_ok) and the draw succeeded (draw_log.json ok).

Learner: T4's byte-level Transformer and library, byte-identical copies in llm/ (cl.py, model.py, data.py), with data.ROOT and data.DOMAINS
pointed at the drawn books (draw_log.json; sha256 checked) and the pretraining cache moved to RUNS/<id>/raw/cache. (Importing llm/cl.py
creates an empty directory outputs/cache in this folder, as it does in T4's; nothing is written there.)
Cells: seeds from draw_log.json x widths (64 with 2 layers, 128 and 192 with 4) x pretraining tokens {1, 2, 8} M (T4's pretrain, one run per
cell from initialisation). Task B: 1 M tokens, AdamW lr 3e-4, adaptive-metric proximal anchor step (T4's continue_on_B).
Arms per cell (stage main): frozen; none; fixed lambda in T4's grid {1e3, 2e3, 5e3, 1e4, 2e4, 5e4}; SEC v2 (alpha 10); SEC-PG with the
configuration in config.json ('pg'); the same without GPM ('light'); the same GPM schedule with a constant anchor whose lambda is the
median over this study's 72 cells of SEC-PG's own multiplier alpha s kappa_mult, computed from units_pretrain.jsonl after the pretrain stage
and written to pgconst_lambda.json ('pgconst': the constant SEC-PG's weight reduces to, R7); GPM as published, with projection from the first
task-B step and no anchor, on the same four maps ('gpm_only'). Stage sens: 'pg' under each sensitivity override in config.json.
Stage rerun: (a) one width-128, 2 M-token cell pretrained again from scratch into a separate cache, then 'pg' on it; (b) 'sec' on the
first width-64, 1 M-token cell; the scorer compares both with the main units (R9)."""
import sys; sys.dont_write_bytecode = True
import os, json, time, hashlib, pathlib, multiprocessing as mp
for k in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'): os.environ[k] = '1'
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; SID = HERE.name; RUN = ROOT / 'RUNS' / SID; RAW = RUN / 'raw'
sys.path.insert(0, str(HERE / 'llm')); sys.path.insert(1, str(HERE))
import data_step
ok, bad, _ = data_step.frozen_ok()
if not ok: sys.exit(f'frozen files changed: {bad}')
DRAW = json.load(open(RUN / 'draw_log.json')); CFG = json.load(open(HERE / 'config.json'))
if not DRAW.get('ok'): sys.exit('draw failed: NOT DECIDABLE; nothing run')
sys.path.insert(2, str(ROOT / 'scripts')); import seen_register
unreg = sorted({f"gutenberg/pg{a['ebook']}.txt" for a in DRAW['attempts'] if a.get('sha256')} - seen_register.seen_ids())
if unreg: sys.exit(f'fetched files not in DATA/SEEN.md (run data_step.py register first): {unreg}')
for a in DRAW['attempts']:
    if a['admitted']: assert hashlib.sha256((RAW / 'books' / f"pg{a['ebook']}.txt").read_bytes()).hexdigest() == a['sha256'], f"book pg{a['ebook']} changed"
USED = {'kappa_mult': CFG['sec_pg']['anchor'] == 'sec', 'const': CFG['sec_pg']['anchor'] == 'const', 'switch': CFG['sec_pg']['gpm'], 'threshold': CFG['sec_pg']['gpm'], 'maps': CFG['sec_pg']['gpm'], 'basis_seqs': CFG['sec_pg']['gpm']}
for k, o in CFG['sensitivity'].items():
    assert all(USED.get(f) for f in o) and all(CFG['sec_pg'][f] != v for f, v in o.items()), f'sensitivity override {k} does not change a parameter the configuration uses'
import data
data.ROOT = RAW / 'books'; data.DOMAINS = {'A': DRAW['domain_A_files'], 'B': DRAW['domain_B_files']}
import torch, cl, sec_pg
torch.set_num_threads(1); CACHE = RAW / 'cache'; cl.CACHE = CACHE; CACHE.mkdir(parents=True, exist_ok=True)
GRID = [1e3, 2e3, 5e3, 1e4, 2e4, 5e4]; ALPHA = 10.0; TOK = 1_000_000; PGCONST = RUN / 'pgconst_lambda.json'
WIDTHS = [(64, 2), (128, 4), (192, 4)]; MAT = [1_000_000, 2_000_000, 8_000_000]; SEEDS = DRAW['seeds']
CELLS = [(s, d, L, t) for s in SEEDS for d, L in WIDTHS for t in MAT]
COST = {64: 1, 128: 4, 192: 12}; PRE_KEYS = ('s', 'c', 'rho', 'nd2', 'params', 'final_train_loss', 'path_length', 'kl_chord', 'loss_slope_window')
MAIN_ARMS = ['frozen', 'none'] + [f'grid_{int(l)}' for l in GRID] + ['sec', 'pg', 'light', 'pgconst', 'gpm_only']
def slim(r): return {k: v for k, v in r.items() if k not in ('curve', 'diag_D', 'controller_lam_hist')}
def pre_of(cell, force=False):
    s, d, L, t = cell
    try: return cl.pretrain(s, d=d, layers=L, tokens=t, force=force)
    except Exception: return cl.pretrain(s, d=d, layers=L, tokens=t, force=True)
def job(args):
    stage, cell, arm = args; s, d, L, t = cell; t0 = time.time()
    if stage == 'pretrain': p = pre_of(cell); out = {k: p.get(k) for k in PRE_KEYS + ('seconds',)}
    elif stage == 'rerun' and arm == 'pretrain+pg':
        cl.CACHE = RAW / 'cache_rerun'; cl.CACHE.mkdir(parents=True, exist_ok=True)
        try: p = cl.pretrain(s, d=d, layers=L, tokens=t, force=True)
        finally: cl.CACHE = CACHE
        out = dict(pre={k: p.get(k) for k in PRE_KEYS}, pg=sec_pg.run(p, s, **CFG['sec_pg']))
    else:
        p = pre_of(cell)
        if arm == 'frozen': out = cl.frozen_metrics(p, s)
        elif arm == 'none': out = slim(cl.continue_on_B(p, s, tokens=TOK, rule='none'))
        elif arm.startswith('grid_'): out = slim(cl.continue_on_B(p, s, tokens=TOK, rule='fixed', lam=float(arm[5:]), safeguard='adaptive'))
        elif arm == 'sec': out = slim(cl.continue_on_B(p, s, tokens=TOK, rule='sec', rho_pref=ALPHA, safeguard='adaptive'))
        elif arm == 'pg': out = sec_pg.run(p, s, **CFG['sec_pg'])
        elif arm == 'light': out = sec_pg.run(p, s, **dict(CFG['sec_pg'], gpm=False))
        elif arm == 'pgconst': out = sec_pg.run(p, s, **dict(CFG['sec_pg'], anchor='const', const=json.load(open(PGCONST))['lambda']))
        elif arm == 'gpm_only': out = sec_pg.run(p, s, **dict(CFG['sec_pg'], anchor='const', const=0.0, switch=0.0))
        elif arm.startswith('sens_'): out = sec_pg.run(p, s, **dict(CFG['sec_pg'], **CFG['sensitivity'][arm[5:]]))
        else: raise ValueError(arm)
    return dict(stage=stage, seed=s, d=d, layers=L, tokens=t, arm=arm, result=out, wall=time.time() - t0)
def jobs_for(stage):
    if stage == 'pretrain': return [('pretrain', c, 'pre') for c in CELLS]
    if stage == 'main': return [('main', c, a) for c in CELLS for a in MAIN_ARMS]
    if stage == 'sens': return [('sens', c, f'sens_{k}') for c in CELLS for k in CFG['sensitivity']]
    if stage == 'rerun': return [('rerun', (SEEDS[0], 128, 4, 2_000_000), 'pretrain+pg'), ('rerun', (SEEDS[0], 64, 2, 1_000_000), 'sec')]
def read_units(path):
    out = []
    if path.exists():
        for line in path.read_text().splitlines():
            try: out.append(json.loads(line))
            except ValueError: print('ignoring a truncated line in', path.name, flush=True)
    return out
def run_stage(stage, workers):
    out = RUN / f'units_{stage}.jsonl'; done = {(r['seed'], r['d'], r['tokens'], r['arm']) for r in read_units(out)}
    todo = sorted([j for j in jobs_for(stage) if (j[1][0], j[1][1], j[1][3], j[2]) not in done], key=lambda j: (-COST[j[1][1]]*j[1][3], j[1][0], j[2]))
    print(stage, len(todo), 'jobs to run', flush=True)
    if out.exists() and out.read_bytes() and not out.read_bytes().endswith(b'\n'):
        with open(out, 'a') as fh: fh.write('\n')
    with mp.get_context('fork').Pool(workers) as pool, open(out, 'a') as fh:
        for r in pool.imap_unordered(job, todo):
            fh.write(json.dumps(r) + '\n'); fh.flush(); x = r['result']
            print(stage, r['seed'], r['d'], r['tokens'], r['arm'], ' '.join(f'{k} {x[k]:.4f}' for k in ('A_test', 'B_test') if k in x), '%.0fs' % r['wall'], flush=True)
    print(stage, 'DONE', flush=True)
if __name__ == '__main__':
    W = int(sys.argv[1]); stages = ['pretrain', 'main', 'sens', 'rerun'] if len(sys.argv) < 3 or sys.argv[2] == 'all' else [sys.argv[2]]
    print('torch', torch.__version__, 'environment.lock sha256', hashlib.sha256((HERE / 'environment.lock').read_bytes()).hexdigest(), 'cells', len(CELLS), 'seeds', SEEDS, 'A', data.DOMAINS['A'], 'B', data.DOMAINS['B'], flush=True)
    for st in stages:
        if st == 'main' and not PGCONST.exists():
            import numpy as np
            pre = {(r['seed'], r['d'], r['tokens']): r['result'] for r in read_units(RUN / 'units_pretrain.jsonl')}
            if len(pre) != len(CELLS): sys.exit('pretrain stage incomplete: run it first')
            mult = [ALPHA*pre[(c[0], c[1], c[3])]['s']*CFG['sec_pg']['kappa_mult'] for c in CELLS]
            json.dump({'lambda': float(np.median(mult)), 'rule': 'median over cells of alpha*s*kappa_mult', 'n': len(mult)}, open(PGCONST, 'w'), indent=1)
        run_stage(st, W)
    print('ALL STAGES DONE', flush=True)
