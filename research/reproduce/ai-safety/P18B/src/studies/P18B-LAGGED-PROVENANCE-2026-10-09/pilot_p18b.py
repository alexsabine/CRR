"""P18B-LAGGED-PROVENANCE pre-freeze pilot (DESIGN.md section 6.4) and the MP10 check (DESIGN HELPER; NOT FROZEN; development seeds only).

Imports pubworld_draft.py (the draft world) and power_plan_p18b.py (the registered n-rules) and changes neither's behaviour.

Modes (run from this folder; at most 4 worker processes):
  pilot --sealed-dir DIR   the section 6.4 pilot, exactly 6000 simulations on development world seeds 340000-346149:
                             cal 1000 (+ calA decision rounds U{31..69} on the same runs), far 500, main 1500 (route e) with probes on the
                             first 400 attribution-eligible, theta and open 400 each (index-paired with main i < 400) with probes on the
                             first 200 eligible each, det 300 (deterministic publisher; route e 150, theta 75, open 75, the section 4.3
                             2:1:1 mix scaled), nogame 500 (random decision rounds U{31..69}), pos 300 (route e 150, theta 75, open 75; probes
                             on every eligible unit; 600 simulations with the probes).
  tiny  --sealed-dir DIR   the same code paths at about 1/100 size (world seeds 390000-396003), plus a check that the two-phase split
                             reproduces pubworld_draft.run_unit exactly. Code paths only; its numbers mean nothing.
  verify | verify-tiny --sealed-dir DIR   recompute the commitment from the sealed files; prints only whether it matches.
  mp10                     S-noise and S-stale (DESIGN.md 5.5, D9, MP10): identities, access, both through the pilot's workers with
                             probes and attribution, and the MP1 equivalence re-run. World seeds 398000-398099. Writes outputs/mp10_check.json.

Blinding (DESIGN.md 6.4). The pilot prints and writes into this folder ONLY
  (a) the discordances D that the n-rules of section 6.2 need, rounded up to 0.05 as the rules use them (raw D's are sealed), and the n-update;
  (b) the control and surrogate checks (MP1-MP10, MF1-MF6, C1-C9 as far as the pilot computes them; MP1, MP2 and MP10 recomputed in-process);
  (c) the commitment sha256(salt + '|' + payload), payload = ';'.join(f'{name}:{sign}:{abs(estimate):.4f}') over
      A1, A2, A3, A4 and the H-D contrasts lag_ri - {pf_twin, bbsd, mobbsd, proj_rec, djump, lag_ri_ph}, in that order; sign is
      '+', '-' or '0' from the unrounded estimate.
  The salt (32 random bytes, hex) is written only to DIR/p18b_pilot_salt.txt (tiny: DIR/p18b_pilot_tiny_salt.txt); an existing salt file
  is reused. A rerun never overwrites earlier sealed files: they are renamed *.prev-<commitment prefix>-<UTC stamp>.* (with a copy of the
  earlier public JSON), so every earlier commitment stays verifiable. The estimates, intervals and per-unit rows go only to DIR/p18b_pilot_sealed.json and DIR/p18b_pilot_units.* (tiny: *_tiny_*).
  DIR must be outside the repository. outputs/pilot_public.json (tiny: outputs/pilot_tiny_public.json) holds (a)-(c), runtime and seeds.

Determinism. Every unit's world seed is a development integer; its generators are pubworld_draft.gen('DEVELOPMENT-ONLY',
'NOT-A-BLOCK-HASH', purpose, '<mode>:<arm>', world seed) with purpose pubpar, pub, nuis (keyed by the paired main/det/pos arm, so
paired units share world, publisher and nuisance), phantom, flip, ri (keyed by the unit's own arm), and boot for the bootstraps.
Phase 1 (unprobed simulation, statistics, attribution) saves the ri generator's state after attribution; phase 2 (the probed simulation
and intervention_ri) restores it, which is exactly pubworld_draft.run_unit's sequence (checked in tiny). Results are sorted by
(arm, index) before analysis, so the output does not depend on worker scheduling.

Review fixes (operator, 2026-10-09; see PILOT.md): raw D's sealed and a residual-leakage note in the public JSON; MP9 without C6;
MP7 reports the re-costed draw cap; C3d arm sizes by the registered rule (fraction-adjusted size as an owner option); MF1/MF5 cannot-fail
notes; MP1/MP2/MP10 recomputed in-process; earlier sealed files archived, never overwritten; implied theta/open arm sizes in n_update.

Run:  nice -n 19 env OMP_NUM_THREADS=1 python3 -I pilot_p18b.py pilot --sealed-dir DIR --workers 4
"""
import sys; sys.dont_write_bytecode = True
import os
for _v in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'): os.environ.setdefault(_v, '1')
import json, math, time, hashlib, secrets, pathlib, argparse, multiprocessing as mp, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
import pubworld_draft as P                              # noqa: E402
from pubworld_draft import L, H                         # noqa: E402
from power_plan_p18b import n_ba, n_tie, n_tost         # noqa: E402  the registered n-rules (section 6.2)
OUT = P.OUT
DEV_FC, DEV_BH = 'DEVELOPMENT-ONLY', 'NOT-A-BLOCK-HASH'
DETS = P.CUSUM_DET + P.SCAN_DET; DI = {k: i for i, k in enumerate(DETS)}
TWIN_KEYS = ('proxy', 'calib', 'inshift', 'bbsd', 'mobbsd', 'djump', 'pf_twin', 'pf_twin_T')
HD_RIVALS = ('pf_twin', 'bbsd', 'mobbsd', 'proj_rec', 'djump', 'lag_ri_ph')        # section 5.3 order
A_CONTRASTS = (('A1', 'intervention_ri'), ('A2', 'twin_jump'), ('A3', 'proj_attr'), ('A4', 'phantom_ri'))
DELTA_A, DELTA_D, ALPHA_RI, MAX_WORKERS = 0.05, 0.02, 0.05, 4
DEV_RANGE = (340_000, 399_999)
SIZES = dict(
    pilot=dict(base=340_000, cal=1000, far=500, main=1500, paired=400, det_e=150, det_pair=75, nogame=500, pos_e=150, pos_pair=75,
               probe_main=400, probe_pair=200, c5_main=200, B=4000),
    tiny=dict(base=390_000, cal=16, far=8, main=12, paired=6, det_e=4, det_pair=2, nogame=8, pos_e=4, pos_pair=2,
              probe_main=4, probe_pair=2, c5_main=4, B=200))
OFFS = dict(cal=0, far=1000, main=2000, det_e=4000, nogame=5000, pos_e=6000)

def G(purpose, tag, seed): return P.gen(DEV_FC, DEV_BH, purpose, tag, seed)
def thr_index(n, far=0.05): return int(np.ceil((1 - far)*n)) - 1          # as pubworld_draft.thresholds
def up05(x): return float('nan') if not np.isfinite(x) else math.ceil(round(x/0.05, 9))*0.05
def wilson(k, n, z=1.959964):
    if n == 0: return None
    p = k/n; den = 1 + z*z/n; c = p + z*z/(2*n); r = z*math.sqrt(p*(1 - p)/n + z*z/(4*n*n)); return [(c - r)/den, (c + r)/den]
def mean(x): x = np.asarray(x, float); return float(x.mean()) if x.size else float('nan')
def clean(o):
    if isinstance(o, dict): return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [clean(v) for v in o]
    if isinstance(o, (np.bool_, bool)): return bool(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (float, np.floating)): return float(o) if np.isfinite(o) else None
    if isinstance(o, np.ndarray): return clean(o.tolist())
    return o
def r4(x): return None if x is None or not np.isfinite(x) else round(float(x), 4)
def sha_file(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

# ------------------------------------------------------------------------------------------------------------------------------ plan
def plan(mode):
    z = SIZES[mode]; b = z['base']; tag = f'{mode}'; jobs = []
    def add(arm, route, idx, seed, pair, pubmode, nuis, dmode, c5=False):
        jobs.append(dict(tag=tag, arm=arm, route=route, idx=idx, seed=seed, pair=pair, pubmode=pubmode, nuis=nuis, dmode=dmode, c5=c5))
    for i in range(z['cal']): add('cal', 'none', i, b + OFFS['cal'] + i, 'cal', 'drawn', 'drawn', 'random')
    for i in range(z['far']): add('far', 'none', i, b + OFFS['far'] + i, 'far', 'drawn', 'drawn', None)
    for i in range(z['main']): add('main', 'e', i, b + OFFS['main'] + i, 'main', 'drawn', 'drawn', 'oracle', c5=i < z['c5_main'])
    for arm in ('theta', 'open'):
        for i in range(z['paired']): add(arm, arm, i, b + OFFS['main'] + i, 'main', 'drawn', 'drawn', 'oracle', c5=True)
    for i in range(z['det_e']): add('det_e', 'e', i, b + OFFS['det_e'] + i, 'det_e', 'det', 'drawn', 'oracle')
    for arm in ('theta', 'open'):
        for i in range(z['det_pair']): add('det_' + arm, arm, i, b + OFFS['det_e'] + i, 'det_e', 'det', 'drawn', 'oracle')
    for i in range(z['nogame']): add('nogame', 'none', i, b + OFFS['nogame'] + i, 'nogame', 'drawn', 'drawn', 'random', c5=True)
    for i in range(z['pos_e']): add('pos_e', 'e', i, b + OFFS['pos_e'] + i, 'pos_e', 'pos', 'none', 'oracle')
    for arm in ('theta', 'open'):
        for i in range(z['pos_pair']): add('pos_' + arm, arm, i, b + OFFS['pos_e'] + i, 'pos_e', 'pos', 'none', 'oracle')
    seeds = [j['seed'] for j in jobs]; assert DEV_RANGE[0] <= min(seeds) and max(seeds) <= DEV_RANGE[1]
    return jobs

def make_unit(job):
    seed, own, pair = job['seed'], f"{job['tag']}:{job['arm']}", f"{job['tag']}:{job['pair']}"
    pub = {'drawn': lambda: P.draw_publisher(G('pubpar', pair, seed)), 'pos': lambda: dict(P.POS_PUB), 'det': lambda: None,
           'noise': lambda: P.draw_publisher_noise(G('pubpar', pair, seed)), 'stale': lambda: P.draw_publisher_stale(G('pubpar', pair, seed)),
           }[job['pubmode']]()
    smooth, tele = P.draw_nuisance(G('nuis', pair, seed)) if job['nuis'] == 'drawn' else (None, None)
    return seed, own, pair, pub, smooth, tele

# ------------------------------------------------------------------------------------------------------------------------- workers
def phase1(job):
    """unprobed simulation, every statistic (with the phantom), detection paths, attribution, C5 and N1 identities, C6"""
    t0 = time.process_time(); seed, own, pair, pub, smooth, tele = make_unit(job)
    sim = P.simulate(seed, job['route'], smooth is not None, smooth, pub, G('pub', pair, seed), tele=tele)
    st = P.all_stats(sim, G('phantom', own, seed))
    paths = {k: L.cusum(st[k]) for k in P.CUSUM_DET}; paths.update({k: np.asarray(st[k], float) for k in P.SCAN_DET})
    M = np.array([np.maximum.accumulate(np.where(np.isnan(paths[k]), -np.inf, paths[k])) for k in DETS])
    c6 = dict(raw_finite=bool(all(np.all(np.isfinite(st[k][1:])) for k in P.CUSUM_DET if k != 'djump') and np.all(np.isfinite(st['djump'][2:]))),
              cusum_finite=bool(all(np.all(np.isfinite(paths[k])) for k in P.CUSUM_DET)),
              scan_no_nan=bool(all(not np.any(np.isnan(paths[k])) for k in P.SCAN_DET)))
    div = sim['div']; elig = bool(sim['gaming'] and div is not None and div + 10 < H); ri = G('ri', own, seed); d = None; attr = None
    if job['dmode'] == 'random': d = int(ri.integers(31, 70))
    elif job['dmode'] == 'oracle' and elig: d = div + 10
    if d is not None: attr = P.attribution(sim, st, d, ri)
    ri_state = ri.bit_generator.state if (job['dmode'] == 'oracle' and elig) else None
    c5 = None
    if job['c5']:
        fake = st['phantom_record']; sim2 = dict(sim, hist=dict(sim['hist'], ell=fake, e=fake)); tw = P.twin_stats(P.twin_view(sim2))
        dd = d if d is not None else 60
        c5 = dict(twin_identical=bool(all(P.same(st[k], tw[k]) for k in TWIN_KEYS) and P.twin_jump(P.twin_view(sim), dd) == P.twin_jump(P.twin_view(sim2), dd)),
                  lag_ri_changed=bool(not P.same(st['lag_ri_T'], P.record_stats(sim, fake, pub)['lag_ri_T'])))
    n1 = None
    if pub is None:
        eta, _ = P.record_innovations(sim['hist']['theta'], sim['hist']['ell'], None)
        n1 = dict(eta_zero=bool(np.all(eta == 0)), lag_undefined=bool(np.all(np.isinf(st['lag_ri'])) and np.all(np.isinf(st['lag_mb']))),
                  mobbsd_eq_proj_rec=bool(np.allclose(st['mobbsd'][1:], st['proj_rec'][1:], rtol=0, atol=1e-12)),
                  pf_twin_eq_lag_full=P.same(st['pf_twin'], st['lag_full']), passive_ri_p_is_1=bool(attr is None or attr['passive_ri_p'] == 1.0))
    return dict(arm=job['arm'], route=job['route'], idx=job['idx'], seed=seed, pair=job['pair'], pubmode=job['pubmode'], nuis=job['nuis'], tag=job['tag'],
                pub=pub, div=div, tau=sim['tau'], eligible=elig, d=d, attr=attr, ri_state=ri_state,
                target=list(sim['hist']['target']) if ri_state is not None else None, M=M, c5=c5, n1=n1, c6=c6,
                smooth=smooth is not None, tele=None if tele is None else dict(mag=tele['mag'], on_G=bool(sim['G'][0] in tele['support'])),
                n_published=int(sum(sim['hist']['published'])), cpu=time.process_time() - t0)

def phase2(job):
    """the probed simulation (flips from div + 2 for 6 rounds) and intervention_ri, continuing the unit's ri generator"""
    t0 = time.process_time(); seed, own, pair, pub, smooth, tele = make_unit(job)
    ri = np.random.default_rng(); ri.bit_generator.state = job['ri_state']
    ps = P.simulate(seed, job['route'], smooth is not None, smooth, pub, G('pub', pair, seed), probe=(job['div'] + 2, P.PROBE_LEN),
                    frng=G('flip', own, seed), tele=tele)
    iv = P.intervention_ri(dict(hist=dict(target=job['target'])), ps, ri)
    return dict(arm=job['arm'], idx=job['idx'], intervention=iv, cpu=time.process_time() - t0)

def run_pool(fn, jobs, workers, label):
    out = []; t0 = time.time(); n = len(jobs)
    if workers <= 1: it = map(fn, jobs); pool = None
    else: pool = mp.get_context('fork').Pool(workers); it = pool.imap_unordered(fn, jobs, chunksize=4)
    try:
        for r in it:
            out.append(r)
            if len(out) % 250 == 0 or len(out) == n: print(f'[{label}] {len(out)}/{n} units, {time.time() - t0:.0f} s wall', file=sys.stderr, flush=True)
    finally:
        if pool is not None: pool.close(); pool.join()
    return sorted(out, key=lambda r: (r['arm'], r['idx'])), time.time() - t0

def select_probes(units, mode):
    z = SIZES[mode]; want = dict(main=z['probe_main'], theta=z['probe_pair'], open=z['probe_pair'], pos_e=10**9, pos_theta=10**9, pos_open=10**9)
    sel = []
    for arm, k in want.items():
        el = [u for u in units if u['arm'] == arm and u['eligible']]; sel += el[:k]
    return sel

# ------------------------------------------------------------------------------------------------------------------------ analysis
def thresholds_from(Cp, far=0.05): return np.sort(Cp, axis=0)[thr_index(len(Cp), far)]

def det_hilo(us, window='timely'):
    """per unit and detector: hi = running max at the end of the window, lo = running max just before it (alarm iff hi > h >= lo)"""
    hi = np.zeros((len(us), len(DETS))); lo = np.full((len(us), len(DETS)), -np.inf)
    for i, u in enumerate(us):
        if window == 'any': hi[i] = u['M'][:, -1]
        else:
            dv = u['div']; hi[i] = u['M'][:, min(dv + P.W_PRIMARY, H - 1)]
            if dv - P.EARLY - 1 >= 0: lo[i] = u['M'][:, dv - P.EARLY - 1]
    return hi, lo

def det_T(hi, lo, h): return (hi > h) & (lo <= h)

def boot_det(hi, lo, Cp, pairs, B, g, levels):
    """two-level paired bootstrap of mean(T_a - T_b): resample cal (thresholds recomputed) and units"""
    n, nc = len(hi), len(Cp); est = {}; draws = {p: np.empty(B) for p in pairs}; h0 = thresholds_from(Cp); T0 = det_T(hi, lo, h0)
    for a, b in pairs: est[(a, b)] = mean(T0[:, DI[a]].astype(float) - T0[:, DI[b]]) if n else float('nan')
    if n == 0: return {p: dict(est=float('nan'), ci=None, D=float('nan')) for p in pairs}
    for k in range(B):
        h = thresholds_from(Cp[g.integers(nc, size=nc)]); iu = g.integers(n, size=n); T = det_T(hi[iu], lo[iu], h)
        for a, b in pairs: draws[(a, b)][k] = T[:, DI[a]].mean() - T[:, DI[b]].mean()
    return {p: dict(est=est[p], ci=[float(np.percentile(draws[p], 100*lv)) for lv in levels], D=mean(T0[:, DI[p[0]]] != T0[:, DI[p[1]]])) for p in pairs}

ATTR_LOC = ('passive_ri', 'intervention_ri', 'twin_jump', 'proj_attr', 'phantom_ri', 'lead_ri', 'passive_mb')
CAL_SCORE = ('twin_jump', 'proj_attr', 'passive_mb')

def attr_cols(us):
    def g(u, k):
        a = u['attr']
        return {'passive_ri': a['passive_ri_p'], 'phantom_ri': a['phantom_ri_p'], 'lead_ri': a['lead_ri_p'], 'twin_jump': a['twin_jump'],
                'proj_attr': a['proj_attr'], 'passive_mb': a['passive_mb_t'],
                'intervention_ri': (u.get('intervention') or {}).get('p_e', float('nan'))}[k]
    return {k: np.array([g(u, k) for u in us], float) for k in ATTR_LOC}

def yes(cols, h):
    out = {}
    for k in ATTR_LOC:
        x = cols[k]
        out[k] = (x > h[k]) if k in CAL_SCORE else (x < ALPHA_RI)
    return out

def cal_scores(cal):
    return np.array([[u['attr']['twin_jump'], u['attr']['proj_attr'], u['attr']['passive_mb_t']] for u in cal], float)

def ba(ye, yn): return 0.5*(ye.mean() + 1 - yn.mean()) if len(ye) and len(yn) else float('nan')

def attribution_mix(e_units, n_units, calS, B, g, contrasts, levels, extra_ba=()):
    """balanced-accuracy contrasts passive_ri - k, two-level stratified bootstrap (calA resampled and thresholds recomputed; units
    resampled within the route-e and non-e strata); also the BA of each localiser in extra_ba with a units-only interval"""
    ce, cn = attr_cols(e_units), attr_cols(n_units); h0 = dict(zip(CAL_SCORE, thresholds_from(calS))); ye, yn = yes(ce, h0), yes(cn, h0)
    res = dict(n_e=len(e_units), n_non_e=len(n_units), contrasts={}, ba={}, yes_rates={})
    for k in ATTR_LOC: res['ba'][k] = ba(ye[k], yn[k]); res['yes_rates'][k] = dict(route_e=mean(ye[k]), non_e=mean(yn[k]))
    if not len(e_units) or not len(n_units):
        for name, k in contrasts: res['contrasts'][name] = dict(rival=k, est=float('nan'), ci=None, D_e=float('nan'), D_n=float('nan'))
        for k in extra_ba: res['ba_ci_' + k] = None
        return res
    dr = {name: np.empty(B) for name, _ in contrasts}; dba = {k: np.empty(B) for k in extra_ba}; ne, nn, nc = len(e_units), len(n_units), len(calS)
    for b in range(B):
        h = dict(zip(CAL_SCORE, thresholds_from(calS[g.integers(nc, size=nc)]))); ie, i_n = g.integers(ne, size=ne), g.integers(nn, size=nn)
        Ye = yes({k: v[ie] for k, v in ce.items()}, h); Yn = yes({k: v[i_n] for k, v in cn.items()}, h)
        for name, k in contrasts: dr[name][b] = ba(Ye['passive_ri'], Yn['passive_ri']) - ba(Ye[k], Yn[k])
        for k in extra_ba: dba[k][b] = ba(Ye[k], Yn[k])
    for name, k in contrasts:
        res['contrasts'][name] = dict(rival=k, est=res['ba']['passive_ri'] - res['ba'][k], ci=[float(np.percentile(dr[name], 100*lv)) for lv in levels],
                                      D_e=mean(ye['passive_ri'] != ye[k]), D_n=mean(yn['passive_ri'] != yn[k]))
    for k in extra_ba: res['ba_ci_' + k] = [float(np.percentile(dba[k], 100*lv)) for lv in levels]
    return res

def payload_of(est):
    parts = []
    for name, x in est:
        if x is None or not np.isfinite(x): parts.append(f'{name}:nan:nan'); continue
        s = '+' if x > 0 else ('-' if x < 0 else '0'); parts.append(f'{name}:{s}:{abs(x):.4f}')
    return ';'.join(parts)

def analyse(mode, units, probes, B, timing, inproc):
    by = {}
    for u in units: by.setdefault(u['arm'], []).append(u)
    piv = {(p['arm'], p['idx']): p['intervention'] for p in probes}
    for u in units: u['intervention'] = piv.get((u['arm'], u['idx']))
    g = G('boot', f'{mode}:boot', 0); A = lambda a: by.get(a, [])
    cal = A('cal'); Cp = np.array([u['M'][:, -1] for u in cal]); h_det = thresholds_from(Cp); calS = cal_scores(cal); h_att = dict(zip(CAL_SCORE, thresholds_from(calS)))
    hd = dict(zip(DETS, h_det))
    def any_rate(us, k): return mean([u['M'][DI[k], -1] > hd[k] for u in us])
    def any_count(us, k): return int(sum(u['M'][DI[k], -1] > hd[k] for u in us))
    def timely_rate(us, k):
        dv = [u for u in us if u['div'] is not None]; hi, lo = det_hilo(dv); return mean(det_T(hi, lo, h_det)[:, DI[k]]) if dv else float('nan')
    pub, sealed = {}, {}
    # ---------------- divergence, eligibility, probes
    main = A('main'); main_div = [u for u in main if u['div'] is not None]; rate_main = mean([u['div'] is not None for u in main])
    mix_e = [u for u in main if u['eligible'] and u['intervention'] is not None]
    mix_n = [u for a in ('theta', 'open') for u in A(a) if u['eligible'] and u['intervention'] is not None]
    pub['arms'] = {a: dict(units=len(us), diverged=sum(u['div'] is not None for u in us), attribution_eligible=sum(u['eligible'] for u in us),
                          probed=sum(u['intervention'] is not None for u in us), world_seeds=[min(u['seed'] for u in us), max(u['seed'] for u in us)])
                   for a, us in sorted(by.items())}
    n_sims = len(units) + len(probes)
    pub['simulations'] = dict(unprobed=len(units), probed=len(probes), total=n_sims)
    dmt = [u['div'] - u['tau'] for u in main_div]
    pub['div_minus_tau_main'] = dict(n=len(dmt), quantiles_0_10_50_90_100=[float(q) for q in np.percentile(dmt, [0, 10, 50, 90, 100])] if dmt else None)
    pub['divergence_rate'] = {a: r4(mean([u['div'] is not None for u in A(a)])) for a in ('main', 'theta', 'open', 'det_e', 'pos_e', 'pos_theta', 'pos_open')}
    pub['thresholds'] = dict(detection_cal={k: r4(v) for k, v in hd.items()}, attribution_calA={k: r4(v) for k, v in h_att.items()}, n_cal=len(cal))
    # ---------------- primary attribution mix (SEALED estimates; public D only)
    mix = attribution_mix(mix_e, mix_n, calS, B, g, [(n, k) for n, k in A_CONTRASTS], (0.025, 0.975, 0.05, 0.95), extra_ba=('phantom_ri', 'lead_ri'))
    # ---------------- H-D detection contrasts over diverged main units (SEALED estimates; public D only)
    hi, lo = det_hilo(main_div)
    hdres = boot_det(hi, lo, Cp, [('lag_ri', k) for k in HD_RIVALS] + [('lag_mb', k) for k in ('pf_twin', 'bbsd', 'mobbsd', 'proj_rec', 'djump', 'lag_mb_ph')],
                     B, g, (0.025, 0.975))
    # ---------------- D's and the n-update (section 6.2)
    # review fix 2 (blinding): only the rounded-up D's that the n-rules use are public; the raw D's go to the sealed file
    Ds_A = {n: dict(D_e_rounded_up=up05(c['D_e']), D_n_rounded_up=up05(c['D_n']),
                    n_rule=n_ba(up05(c['D_e']), up05(c['D_n'])) if np.isfinite(c['D_e']) and np.isfinite(c['D_n']) else None)
            for n, c in mix['contrasts'].items()}
    Ds_D = {f'lag_ri-{k}': dict(D_rounded_up=up05(hdres[('lag_ri', k)]['D']),
                                n_rule=n_tie(up05(hdres[('lag_ri', k)]['D']), DELTA_D) if np.isfinite(hdres[('lag_ri', k)]['D']) else None) for k in HD_RIVALS}
    sealed['raw_D'] = dict(attribution={n: dict(D_e=r4(c['D_e']), D_n=r4(c['D_n'])) for n, c in mix['contrasts'].items()},
                           detection={f'lag_ri-{k}': r4(hdres[('lag_ri', k)]['D']) for k in HD_RIVALS})
    nA_raw = max([v['n_rule'] for v in Ds_A.values() if v['n_rule'] is not None] or [0]); nM_raw = max([v['n_rule'] for v in Ds_D.values() if v['n_rule'] is not None] or [0])
    n_A = min(6000, max(2000, nA_raw)); n_main = min(15000, max(6000, nM_raw))
    # ---------------- other-direction detection controls (C3d, C3e) and the TOST arms
    c3d, c3e_det = {}, {}
    for a in ('theta', 'open', 'nogame'):
        us = A(a) if a == 'nogame' else [u for u in A(a) if u['div'] is not None]; hi_a, lo_a = det_hilo(us, 'any' if a == 'nogame' else 'timely')
        r = boot_det(hi_a, lo_a, Cp, [('lag_ri', 'lag_ri_ph'), ('lag_ri', 'pf_twin')], B, g, (0.05, 0.95, 0.975))
        rp = r[('lag_ri', 'lag_ri_ph')]; frac = len(us)/max(1, len(A(a)))
        ntost = n_tost(rp['D'], DELTA_D) if np.isfinite(rp['D']) else None
        # review fix 5: the registered rule (section 6.2) is applied as written: 2000 units cover D up to about 0.055, larger D raises the arm
        # in proportion (n_tost(D) units), cap 4000. The in-contrast-fraction adjustment is reported as an owner option only.
        c3d[a] = dict(endpoint='alarm within 80 rounds, all units' if a == 'nogame' else 'timely detection, diverged units', n=len(us),
                      est=r4(rp['est']), ci90=[r4(x) for x in rp['ci'][:2]] if rp['ci'] else None, D=r4(rp['D']),
                      inside_pm_delta_D=bool(rp['ci'] is not None and -DELTA_D < rp['ci'][0] and rp['ci'][1] < DELTA_D),
                      tost_units_needed=ntost, in_contrast_fraction=r4(frac),
                      arm_size_update=None if ntost is None else int(min(4000, max(2000, ntost))),
                      owner_option_arm_size_if_divided_by_in_contrast_fraction=None if ntost is None else int(min(4000, max(2000, math.ceil(ntost/max(frac, 1e-9))))))
        if a != 'nogame':
            rf = r[('lag_ri', 'pf_twin')]
            c3e_det[a] = dict(est=r4(rf['est']), upper_97_5=r4(rf['ci'][2]) if rf['ci'] else None, D=r4(rf['D']),
                              pass_upper_below_delta_D=bool(rf['ci'] is not None and rf['ci'][2] < DELTA_D))
    det_e = [u for u in A('det_e') if u['eligible']]; det_n = [u for a in ('det_theta', 'det_open') for u in A(a) if u['eligible']]
    detmix = attribution_mix(det_e, det_n, calS, B, g, [('det', 'twin_jump')], (0.025, 0.975))
    dm = detmix['contrasts']['det']
    pub['n_update'] = dict(
        attribution=dict(D_by_contrast=Ds_A, n_rule_max=nA_raw, n_A=n_A, planning_n_A=2000, raised=n_A > 2000, cap_reached=nA_raw > 6000,
                         rule='n_A = max over A1-A4 of ceil((De + Dn)/2 * 1.15^2 * ((1.959964 + 1.281552)/0.05)^2), D rounded up to 0.05; floor 2000, cap 6000'),
        detection=dict(D_by_contrast=Ds_D, n_rule_max=nM_raw, n_main=n_main, planning_n_main=6000, raised=n_main > 6000, cap_reached=nM_raw > 15000,
                       rule='n_main = max over the H-D contrasts of ceil(D * 1.15^2 * ((1.959964 + 1.281552)/0.02)^2), D rounded up to 0.05; floor 6000, cap 15000'),
        draw_cap=dict(main_divergence_rate=r4(rate_main), draw_cap=math.ceil(n_main/(rate_main - 0.05)) if rate_main > 0.05 else None,
                      rule='ceil(n_main / (pilot divergence rate - 0.05))'),
        tost_arms={a: dict(D=v['D'], units_needed=v['tost_units_needed'], arm_size=v['arm_size_update'], in_contrast_fraction=v['in_contrast_fraction'],
                           owner_option_arm_size_if_divided_by_in_contrast_fraction=v['owner_option_arm_size_if_divided_by_in_contrast_fraction']) for a, v in c3d.items()},
        tost_rule=('registered (section 6.2): arm size = min(4000, max(2000, n_tost(D))), n_tost = ceil(D * 1.15^2 * (2 * 1.644854/0.02)^2); '
                   'the owner option divides n_tost by the share of the arm that enters the contrast (theta/open: diverged units) before the floor and cap'),
        implied_paired_arm_sizes=dict(
            note='theta and open must each supply n_A/4 attribution-eligible units; implied arm size = ceil(n_A/4 / eligible fraction). '
                 'The registered theta/open arms are index-paired with main i < 2000 (2000 units each)',
            **{a: dict(eligible_fraction=r4(mean([u['eligible'] for u in A(a)])),
                       implied_units=(math.ceil(n_A/4/mean([u['eligible'] for u in A(a)])) if A(a) and mean([u['eligible'] for u in A(a)]) > 0 else None))
               for a in ('theta', 'open')},
            main=dict(eligible_fraction=r4(mean([u['eligible'] for u in main])),
                      implied_units_for_n_A_over_2=(math.ceil(n_A/2/mean([u['eligible'] for u in main])) if main and mean([u['eligible'] for u in main]) > 0 else None))),
        attribution_equivalence='C3a/C3b need about 206 units (section 6.2); covered by n_A',
        note='the pilot may only raise n (section 6.2, 8.3); delta, windows, rules, distributions and arms are unchanged')
    # ---------------- controls and must-pass / must-fail
    def yes_rate(us, key):
        x = [u['attr'][key] < ALPHA_RI for u in us if u['attr'] is not None]; return dict(n=len(x), k=int(sum(x)), rate=r4(mean(x)), wilson95=[r4(v) for v in wilson(sum(x), len(x))] if x else None)
    def iv_rate(us):
        x = [u['intervention']['p_e'] < ALPHA_RI for u in us if u['intervention'] is not None]; return dict(n=len(x), k=int(sum(x)), rate=r4(mean(x)), wilson95=[r4(v) for v in wilson(sum(x), len(x))] if x else None)
    def wu_ok(r, lim=0.10): return bool(r['wilson95'] is not None and r['wilson95'][1] <= lim)
    el = lambda a: [u for u in A(a) if u['eligible']]
    C = {}
    C['MP4_C3c'] = dict(passive_ri_nogame_random_d=yes_rate(A('nogame'), 'passive_ri_p'), passive_ri_theta=yes_rate(el('theta'), 'passive_ri_p'),
                        passive_ri_open=yes_rate(el('open'), 'passive_ri_p'), phantom_ri_main=yes_rate(el('main'), 'phantom_ri_p'),
                        lead_ri_main=yes_rate(el('main'), 'lead_ri_p'),
                        info_passive_ri_cal_random_d=yes_rate(cal, 'passive_ri_p'), info_phantom_ri_theta_open=yes_rate(el('theta') + el('open'), 'phantom_ri_p'))
    C['MP4_C3c']['pass_C3c'] = all(wu_ok(C['MP4_C3c'][k]) for k in ('passive_ri_nogame_random_d', 'passive_ri_theta', 'passive_ri_open'))
    C['MP4_C3c']['pass_MP4'] = C['MP4_C3c']['pass_C3c'] and wu_ok(C['MP4_C3c']['phantom_ri_main']) and wu_ok(C['MP4_C3c']['lead_ri_main'])
    pos_all = A('pos_e') + A('pos_theta') + A('pos_open'); pos_div = [u for u in pos_all if u['div'] is not None]
    c1 = dict(divergence_rate=r4(mean([u['div'] is not None for u in pos_all])), n=len(pos_all),
              proxy_timely=r4(timely_rate(pos_div, 'proxy')), calib_timely=r4(timely_rate(pos_div, 'calib')),
              passive_ri_sensitivity=yes_rate(el('pos_e'), 'passive_ri_p'), passive_ri_false_yes=yes_rate(el('pos_theta') + el('pos_open'), 'passive_ri_p'))
    c1['pass'] = bool(c1['divergence_rate'] is not None and c1['divergence_rate'] >= 0.95 and c1['proxy_timely'] is not None and c1['proxy_timely'] <= 0.10
                      and c1['calib_timely'] is not None and c1['calib_timely'] <= 0.10 and (c1['passive_ri_sensitivity']['rate'] or 0) >= 0.80
                      and c1['passive_ri_false_yes']['rate'] is not None and c1['passive_ri_false_yes']['rate'] <= 0.10)
    C['MP5_C1'] = c1
    probed = lambda a: [u for u in A(a) if u['intervention'] is not None]
    c9 = dict(intervention_sensitivity=iv_rate(probed('pos_e')), intervention_false_yes=iv_rate(probed('pos_theta') + probed('pos_open')))
    c9['pass'] = bool((c9['intervention_sensitivity']['rate'] or 0) >= 0.80 and c9['intervention_false_yes']['rate'] is not None and c9['intervention_false_yes']['rate'] <= 0.10)
    C['MP6_C9'] = c9
    # review fix 4: section 8.1 MP7 says 'else the draw cap is re-costed', section 8.3 says any MP failure is NO-GO. The go/no-go follows
    # section 8.3 (the stricter reading); the re-costed draw cap is always reported so the owner can apply the section 8.1 reading.
    dcap = math.ceil(n_main/(rate_main - 0.05)) if rate_main > 0.05 else None
    C['MP7'] = dict(main_divergence_rate=r4(rate_main), n=len(main), limit=0.80, recosted_draw_cap=dcap,
                    recosted_main_cpu_hours_with_margin=None if dcap is None else round(dcap*0.6*1.5/3600, 2),
                    note='GO follows section 8.3 (MP7 below 0.80 is NO-GO); the section 8.1 parenthetical (re-cost the draw cap) is reported, not applied')
    C['MP7']['pass'] = bool(rate_main >= 0.80)
    cpu1 = sum(u['cpu'] for u in units); cpu2 = sum(p['cpu'] for p in probes)
    C['MP8'] = dict(cpu_s_per_simulation=r4((cpu1 + cpu2)/max(1, n_sims)), cpu_s_per_unprobed_unit=r4(cpu1/max(1, len(units))),
                    cpu_s_per_probed_simulation=r4(cpu2/max(1, len(probes))), limit=0.9)
    C['MP8']['pass'] = bool((cpu1 + cpu2)/max(1, n_sims) <= 0.9)
    C['C2_far'] = dict(n=len(A('far')), alarm_rate={k: r4(any_rate(A('far'), k)) for k in DETS})
    C['C2_far']['pass'] = bool(len(A('far')) and all(0.02 <= any_rate(A('far'), k) <= 0.08 for k in DETS))
    C['C3a_C3b_MF2_MF3'] = dict(phantom_ri_BA=r4(mix['ba']['phantom_ri']), phantom_ri_BA_ci90=[r4(x) for x in (mix['ba_ci_phantom_ri'] or [None]*4)[2:4]],
                                lead_ri_BA=r4(mix['ba']['lead_ri']), lead_ri_BA_ci90=[r4(x) for x in (mix['ba_ci_lead_ri'] or [None]*4)[2:4]],
                                mix_units=dict(route_e=mix['n_e'], non_e=mix['n_non_e']))
    inside = lambda ci: ci is not None and None not in ci and 0.45 < ci[0] and ci[1] < 0.55
    C['C3a_C3b_MF2_MF3']['pass_C3a'] = bool(inside(C['C3a_C3b_MF2_MF3']['phantom_ri_BA_ci90'])); C['C3a_C3b_MF2_MF3']['pass_C3b'] = bool(inside(C['C3a_C3b_MF2_MF3']['lead_ri_BA_ci90']))
    C['C3d'] = c3d; C['C3d']['pass'] = all(v['inside_pm_delta_D'] for v in c3d.values())
    C['C3e'] = dict(det_mix=dict(n_e=detmix['n_e'], n_non_e=detmix['n_non_e'], passive_ri_BA=r4(detmix['ba']['passive_ri']), twin_jump_BA=r4(detmix['ba']['twin_jump']),
                                 passive_minus_twin=r4(dm['est']), upper_97_5=r4(dm['ci'][1]) if dm['ci'] else None,
                                 pass_upper_below_delta_A=bool(dm['ci'] is not None and dm['ci'][1] < DELTA_A)),
                    theta_open_lag_ri_minus_pf_twin=c3e_det)
    C['C3e']['pass'] = C['C3e']['det_mix']['pass_upper_below_delta_A'] and all(v['pass_upper_below_delta_D'] for v in c3e_det.values())
    ng = A('nogame'); c4 = dict(n=len(ng), lag_ri_alarm=any_count(ng, 'lag_ri'))
    c4['lag_ri_alarm_rate'] = r4(any_rate(ng, 'lag_ri')); c4['wilson95'] = [r4(v) for v in wilson(c4['lag_ri_alarm'], len(ng))] if ng else None
    c4['pass_C4d'] = bool(c4['wilson95'] is not None and c4['wilson95'][1] <= 0.10)
    c4['C4l_level_rivals_alarm_rate_recorded'] = {k: r4(any_rate(ng, k)) for k in ('bbsd', 'mobbsd', 'proj_rec', 'djump', 'inshift', 'proxy', 'calib')}
    C['C4'] = c4
    c5u = [u for u in units if u['c5'] is not None]
    C['C5'] = dict(units_checked=len(c5u), twin_statistics_identical_under_record_swap=int(sum(u['c5']['twin_identical'] for u in c5u)),
                   lag_ri_changed_under_record_swap=int(sum(u['c5']['lag_ri_changed'] for u in c5u)),
                   note='record swap on fixed trajectories (theta, open, nogame: every unit; main: first units); the publisher-stream-swap rerun is not part of the 6000-simulation pilot (outputs/access_check.json covers it at development scale)')
    C['C5']['pass'] = bool(c5u and all(u['c5']['twin_identical'] for u in c5u))
    c6 = dict(raw_finite_after_round_0=int(sum(u['c6']['raw_finite'] for u in units)), cusum_paths_finite=int(sum(u['c6']['cusum_finite'] for u in units)),
              scan_paths_no_nan=int(sum(u['c6']['scan_no_nan'] for u in units)), units=len(units),
              note='djump is a second difference and is defined from round 2; it is checked from round 2')
    c6['pass'] = all(c6[k] == len(units) for k in ('raw_finite_after_round_0', 'cusum_paths_finite', 'scan_paths_no_nan'))
    C['C6'] = c6
    C['C8_MF4_open'] = dict(passive_ri=yes_rate(el('open'), 'passive_ri_p'), intervention_ri=iv_rate(probed('open')))
    C['C8_MF4_open']['pass'] = bool(all(C['C8_MF4_open'][k]['rate'] is not None and C['C8_MF4_open'][k]['rate'] <= 0.10 for k in ('passive_ri', 'intervention_ri')))
    n1u = [u for u in units if u['n1'] is not None]
    C['MP3_N1_at_scale_det'] = dict(units=len(n1u), **{k: int(sum(u['n1'][k] for u in n1u)) for k in ('eta_zero', 'lag_undefined', 'mobbsd_eq_proj_rec', 'pf_twin_eq_lag_full', 'passive_ri_p_is_1')})
    C['MP3_N1_at_scale_det']['pass'] = bool(n1u and all(all(u['n1'].values()) for u in n1u))
    nogame_arms = A('cal') + A('far') + A('nogame')
    C['MF1'] = dict(no_gaming_units=len(nogame_arms), diverged=int(sum(u['div'] is not None for u in nogame_arms)),
                    note='the pilot has no aligned arm; MF1 is evaluated on every no-gaming unit (cal, far, nogame: aligned plus label-consistent nuisance)')
    C['MF1']['pass'] = C['MF1']['diverged'] == 0 and len(nogame_arms) > 0
    C['MF1']['cannot_fail_by_construction'] = ('with no gaming x_obs equals x_true, so proxy and target accuracy coincide and the gap that defines divergence '
                                              'is identically 0; this check verifies the code path, it cannot fail in a correct build (review fix 6)')
    C['MF2'] = dict(phantom_ri_BA=C['C3a_C3b_MF2_MF3']['phantom_ri_BA'], lag_ri_ph_alarm_rate_main=r4(any_rate(main, 'lag_ri_ph')))
    C['MF2']['pass'] = bool(C['MF2']['phantom_ri_BA'] is not None and abs(C['MF2']['phantom_ri_BA'] - 0.5) <= 0.05 and C['MF2']['lag_ri_ph_alarm_rate_main'] is not None and C['MF2']['lag_ri_ph_alarm_rate_main'] <= 0.10)
    C['MF3'] = dict(lead_ri_BA=C['C3a_C3b_MF2_MF3']['lead_ri_BA']); C['MF3']['pass'] = bool(C['MF3']['lead_ri_BA'] is not None and abs(C['MF3']['lead_ri_BA'] - 0.5) <= 0.05)
    C['MF5'] = dict(nogame_diverged=int(sum(u['div'] is not None for u in ng)), lag_ri_alarm_rate=c4['lag_ri_alarm_rate'])
    C['MF5']['pass'] = bool(len(ng) and C['MF5']['nogame_diverged'] == 0 and c4['lag_ri_alarm_rate'] <= 0.10)
    C['MF5']['note'] = 'the no-divergence half cannot fail by construction (as MF1); the lag_ri alarm-rate half is a real check (review fix 6)'
    C['MF6'] = dict(lag_mb_ph_alarm_rate_main=r4(any_rate(main, 'lag_mb_ph')), note='wording only (section 8.2): a failure changes the S-mb wording, not the rules')
    C['MF6']['pass'] = bool(C['MF6']['lag_mb_ph_alarm_rate_main'] is not None and C['MF6']['lag_mb_ph_alarm_rate_main'] >= 0.50)
    expected = plan(mode); exp_counts = {}
    for j in expected: exp_counts[j['arm']] = exp_counts.get(j['arm'], 0) + 1
    # review fix 3: MP9 is the section 8.1 definition only (all arms, probes and attribution run); C6 is reported as its own control
    C['MP9'] = dict(arms_complete=bool(all(len(A(a)) == n for a, n in exp_counts.items())), probes_complete=bool(len(probes) == len(select_probes(units, mode))),
                    every_probe_has_intervention=bool(all(p['intervention'] is not None for p in probes)),
                    attribution_complete=bool(all(u['attr'] is not None for u in units if u['d'] is not None)
                                              and all(u['d'] is not None for u in units if u['eligible'] and u['arm'] not in ('cal', 'far'))))
    C['MP9']['pass'] = all(C['MP9'].values())
    # review fix 8: MP1, MP2 and MP10 are recomputed in this process with the current code (inproc), and compared with the committed files
    C['MP1_MP2_MP10_inprocess'] = inproc
    mp_ok = dict(MP1=inproc['MP1_equiv']['ok'], MP2=inproc['MP2_access']['ok'], MP3=inproc['MP1_equiv']['ok'] and C['MP3_N1_at_scale_det']['pass'],
                 MP4=C['MP4_C3c']['pass_MP4'], MP5=C['MP5_C1']['pass'], MP6=C['MP6_C9']['pass'], MP7=C['MP7']['pass'], MP8=C['MP8']['pass'], MP9=C['MP9']['pass'], MP10=inproc['MP10']['ok'])
    mf_ok = dict(MF1=C['MF1']['pass'], MF2=C['MF2']['pass'], MF3=C['MF3']['pass'], MF4=C['C8_MF4_open']['pass'], MF5=C['MF5']['pass'])
    ctl_ok = dict(C1=c1['pass'], C2=C['C2_far']['pass'], C3a=C['C3a_C3b_MF2_MF3']['pass_C3a'], C3b=C['C3a_C3b_MF2_MF3']['pass_C3b'], C3c=C['MP4_C3c']['pass_C3c'],
                  C3d=C['C3d']['pass'], C3e=C['C3e']['pass'], C4d=c4['pass_C4d'], C5=C['C5']['pass'], C6=c6['pass'], C8=C['C8_MF4_open']['pass'], C9=c9['pass'])
    pub['checks'] = C
    pub['go_no_go'] = dict(must_pass={k: bool(v) for k, v in mp_ok.items()}, must_fail={k: bool(v) for k, v in mf_ok.items()}, MF6_wording_only=bool(C['MF6']['pass']),
                           controls={k: bool(v) for k, v in ctl_ok.items()},
                           GO=bool(all(mp_ok.values()) and all(mf_ok.values())),
                           rule='GO to freeze if MP1-MP10 and MF1-MF5 pass (section 8.3); a NO-GO is recorded first (R14), fixed in development, and the pilot is rerun')
    pub['runtime'] = dict(timing, cpu_s_total=round(cpu1 + cpu2, 1), cpu_hours_total=round((cpu1 + cpu2)/3600, 3))
    # ---------------- sealed estimates and the commitment
    est_list = [(n, mix['contrasts'][n]['est']) for n, _ in A_CONTRASTS] + [(f'HD_{k}', hdres[('lag_ri', k)]['est']) for k in HD_RIVALS]
    sealed['attribution_mix'] = mix; sealed['detection_main'] = {f'{a}-{b}': v for (a, b), v in hdres.items()}
    sealed['detection_main_timely_rates'] = {k: r4(timely_rate(main_div, k)) for k in DETS}
    sealed['passive_ri_yes_main_eligible'] = yes_rate(el('main'), 'passive_ri_p')
    costs = [u['intervention']['target_cost'] for u in mix_e + mix_n]
    sealed['intervention_target_cost_mix'] = dict(mean=mean(costs), n=len(costs))
    sealed['det_mix'] = detmix
    return pub, sealed, est_list

def inprocess_checks():
    """MP1 (equivalence, with the N1 identities of MP3), MP2 (access) and MP10 recomputed with the current code; each is also compared with the
    committed output file (equal apart from CPU seconds)"""
    def cmp(name, fresh, drop=()):
        f = OUT / name
        if not f.exists(): return dict(file=name, present=False)
        def strip(o):   # CPU-second fields vary between runs
            if isinstance(o, dict): return {k: strip(v) for k, v in o.items() if k not in drop and not k.startswith('cpu')}
            if isinstance(o, list): return [strip(v) for v in o]
            return o
        old = json.load(open(f)); a = json.loads(json.dumps(fresh, default=float))
        return dict(file=name, present=True, sha256=sha_file(f), equal_to_inprocess_apart_from_cpu_seconds=strip(a) == strip(old))
    rows = P.equiv_rows(); eq_ok = all(all(v for v in r.values() if isinstance(v, bool)) for r in rows)
    acc = P.access_result(); m10 = mp10_result()
    return dict(MP1_equiv=dict(ok=bool(eq_ok), rows=len(rows), committed=cmp('equiv_check.json', dict(rows=rows, ok=bool(eq_ok)), drop=('mode', 'version', 'note'))),
                MP2_access=dict(ok=bool(acc['ok']), rows=len(acc['rows']), committed=cmp('access_check.json', acc)),
                MP10=dict(ok=bool(m10['ok']), committed=cmp('mp10_check.json', clean(m10), drop=('cpu_seconds',))))

# ----------------------------------------------------------------------------------------------------------------------- driver
def repo_root():
    for p in [HERE] + list(HERE.parents):
        if (p / '.git').exists(): return p
    return HERE.parents[2]

def seal_paths(mode, sealed_dir):
    d = pathlib.Path(sealed_dir).resolve(); root = repo_root().resolve()
    if d == root or root in d.parents: raise SystemExit(f'--sealed-dir must be outside the repository ({root})')
    d.mkdir(parents=True, exist_ok=True); sfx = '' if mode == 'pilot' else '_tiny'
    return d / f'p18b_pilot{sfx}_salt.txt', d / f'p18b_pilot{sfx}_sealed.json', d / f'p18b_pilot{sfx}_units.json', d / f'p18b_pilot{sfx}_paths.npz'

def get_salt(path):
    if path.exists(): return path.read_text().strip(), True
    salt = secrets.token_hex(32); fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as f: f.write(salt + '\n')
    return salt, False

def archive_previous(mode, sealed_files, pub_p):
    """review fix 9: a rerun never overwrites an earlier run's sealed files. Existing sealed, units and paths files are renamed with the
    earlier run's commitment prefix and a UTC stamp, and the earlier public JSON is copied next to them, so the earlier commitment stays
    verifiable with the (reused) salt. Returns the archived names (no content)."""
    if not any(f.exists() for f in sealed_files): return None
    prev = None
    try: prev = json.load(open(sealed_files[0]))['commitment'][:12]
    except Exception: prev = 'unknown'
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime()); names = []
    for f in sealed_files:
        if f.exists():
            g = f.with_name(f'{f.stem}.prev-{prev}-{stamp}{f.suffix}')
            if g.exists(): raise SystemExit(f'refusing to overwrite archive {g}')
            f.rename(g); names.append(g.name)
    if pub_p.exists():
        g = sealed_files[0].with_name(f'{pub_p.stem}.prev-{prev}-{stamp}{pub_p.suffix}'); g.write_bytes(pub_p.read_bytes()); names.append(g.name)
    print(f'[{mode}] earlier sealed files archived: {names}', file=sys.stderr, flush=True)
    return dict(previous_commitment_prefix=prev, archived_files=names)

def split_check(mode, units, probes):
    """tiny only: the two-phase split reproduces pubworld_draft.run_unit (attribution and intervention) for the first probed unit"""
    pr = {(p['arm'], p['idx']): p for p in probes}; u = next((u for u in units if u['arm'] == 'main' and (u['arm'], u['idx']) in pr), None)
    if u is None: return dict(checked=False)
    job = dict(tag=mode, arm=u['arm'], pair=u['pair'], seed=u['seed'], pubmode=u['pubmode'], nuis=u['nuis']); seed, own, pair, pub, smooth, tele = make_unit(job)
    key = lambda purpose, tag: P.sha_int(f'{DEV_FC}|{DEV_BH}|p18b|{purpose}|{tag}|{seed}', 16)
    r, _, _ = P.run_unit(seed, 'e', (smooth, tele), pub, key('pub', pair), key('phantom', own), None, probe_frng=G('flip', own, seed), ri_rng=G('ri', own, seed))
    return dict(checked=True, arm=u['arm'], seed=seed, attribution_identical=clean(r['attr']) == clean(u['attr']),
                intervention_identical=clean(r['intervention']) == clean(pr[(u['arm'], u['idx'])]['intervention']))

def mode_pilot(mode, sealed_dir, workers):
    workers = max(1, min(MAX_WORKERS, workers)); salt_p, sealed_p, units_p, paths_p = seal_paths(mode, sealed_dir)
    t_all = time.time(); jobs = plan(mode)
    units, w1 = run_pool(phase1, jobs, workers, f'{mode} phase 1')
    pj = [dict(tag=mode, arm=u['arm'], idx=u['idx'], route=u['route'], seed=u['seed'], pair=u['pair'], pubmode=u['pubmode'], nuis=u['nuis'],
               div=u['div'], ri_state=u['ri_state'], target=u['target']) for u in select_probes(units, mode)]
    probes, w2 = run_pool(phase2, pj, workers, f'{mode} phase 2')
    t_ip = time.time(); inproc = inprocess_checks(); w_ip = time.time() - t_ip
    t_an = time.time(); B = SIZES[mode]['B']
    pub, sealed, est = analyse(mode, units, probes, B, dict(workers=workers, wall_s_phase1=round(w1, 1), wall_s_phase2=round(w2, 1), wall_s_inprocess_MP1_MP2_MP10=round(w_ip, 1)), inproc)
    pub['runtime']['wall_s_analysis_and_bootstrap'] = round(time.time() - t_an, 1); pub['runtime']['wall_s_total'] = round(time.time() - t_all, 1)
    salt, reused = get_salt(salt_p); payload = payload_of(est); commitment = hashlib.sha256(f'{salt}|{payload}'.encode('utf-8')).hexdigest()
    head = dict(mode=mode, version=2, study='P18B-LAGGED-PROVENANCE (design draft; not frozen)', date_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                note=('DEVELOPMENT PILOT (DESIGN.md 6.4). Development world seeds only; dummy beacon strings; not evidence. The primary contrasts '
                      '(A1-A4 and the H-D contrasts) are SEALED: only their discordances D, the control and surrogate checks, and a commitment are '
                      'published here. The control rates reveal something about the primary; this is disclosed in DESIGN.md 6.4.'
                      ' Only D rounded up to 0.05 (what the n-rules use) is public; the raw D values are sealed.'
                      + (' TINY CONFIGURATION: code paths only; its numbers mean nothing.' if mode == 'tiny' else '')),
                seeds=dict(declared_development_range=list(DEV_RANGE), world_seeds_used=[min(j['seed'] for j in jobs), max(j['seed'] for j in jobs)],
                           generators="pubworld_draft.gen('DEVELOPMENT-ONLY', 'NOT-A-BLOCK-HASH', purpose, '<mode>:<arm>', world seed)"),
                code_sha256={f: sha_file(HERE / f) for f in ('pubworld_draft.py', 'pilot_p18b.py', 'power_plan_p18b.py')},
                commitment=dict(sha256=commitment, salt_reused_from_existing_file=reused,
                                construction="sha256(salt + '|' + payload); payload = ';'.join(name + ':' + sign + ':' + format(abs(estimate), '.4f')) over "
                                             + ', '.join(n for n, _ in est) + "; sign in {'+', '-', '0'} from the unrounded estimate; the salt is held outside the repository",
                                sealed_files=[sealed_p.name, units_p.name, paths_p.name, salt_p.name]))
    head['blinding_disclosure'] = (
        'Residual leakage, stated explicitly (review fix 2). The public phantom_ri and lead_ri yes-rates in main, the public phantom_ri and lead_ri '
        'balanced accuracies, and the rounded-up discordance D_e(A4) = P(passive_ri != phantom_ri | route e) together bound passive_ri\'s '
        'route-e yes-rate to within about +-(D_e(A4) rounded up) of the phantom_ri yes-rate, and hence bound the A4 estimate to within about '
        'half that width. The same holds for the non-e class through D_n(A4) and the theta/open passive_ri yes-rates. These rates are '
        'published because go/no-go needs them (MP4, MF2, MF3; DESIGN.md 6.4). No primary estimate, interval or raw D is published.')
    head['implementation_choices'] = [
        'det arm 300 split route e 150, theta 75, open 75 (the section 4.3 2:1:1 mix scaled; power_plan.json labels the pilot det arm route e only); '
        'C3e needs non-e det units. Recorded in DESIGN.md 6.4 (operator note); owner to confirm.',
        'MP7: GO follows section 8.3; the section 8.1 re-costed draw cap is reported, not applied.',
        'MP9 is the section 8.1 definition (arms, probes, attribution); C6 is reported separately as a control.',
        'C3d TOST arm sizes: the registered section 6.2 rule as written; the in-contrast-fraction version is reported as an owner option.',
        'C6: djump (a second difference) is checked from round 2; DESIGN.md 5.4 C6 wording clarified accordingly.',
        'MF1 (no aligned arm in the pilot) is evaluated on every no-gaming unit; MF1 and the divergence half of MF5 cannot fail by construction.',
        'C5: the publisher-stream-swap rerun is not part of the 6000 simulations; MP2 (access, recomputed in-process) covers it at development scale.',
        'MP1, MP2 and MP10 are recomputed in-process with the current code and compared with the committed files.']
    if mode == 'tiny': head['split_equals_run_unit'] = split_check(mode, units, probes)
    pub = dict(head, **pub)
    sealed = dict(mode=mode, commitment=commitment, payload=payload, estimates=dict(est), **sealed)
    pub_p = OUT / ('pilot_public.json' if mode == 'pilot' else 'pilot_tiny_public.json')
    archived = archive_previous(mode, [sealed_p, units_p, paths_p], pub_p)
    if archived: pub['commitment']['previous_run_archived'] = archived
    json.dump(clean(sealed), open(sealed_p, 'w'), indent=1)
    rows = [{k: v for k, v in u.items() if k not in ('M', 'ri_state', 'target')} for u in units]
    json.dump(clean(dict(units=rows, probes=probes)), open(units_p, 'w'))
    np.savez_compressed(paths_p, M=np.array([u['M'] for u in units]), arm=np.array([u['arm'] for u in units]), idx=np.array([u['idx'] for u in units]), detectors=np.array(DETS))
    json.dump(clean(pub), open(pub_p, 'w'), indent=1); print(json.dumps(clean(pub), indent=1))
    return 0

# ------------------------------------------------------------------------------------------------------------------------- MP10
def mode_mp10():
    out = mp10_result()
    json.dump(clean(out), open(OUT / 'mp10_check.json', 'w'), indent=1); print(json.dumps(clean(out), indent=1)); return 0 if out['ok'] else 1

def mp10_result():
    """S-noise and S-stale: (1) identities with the deterministic publisher at zero variation; (2) access (record swap and publisher-stream
    swap); (3) every arm type through the pilot's workers with probes and attribution; (4) MP1 equivalence re-run."""
    t0 = time.process_time(); out = dict(mode='mp10', version=1, note='development world seeds 398000-398099; dummy beacon strings; S-noise and S-stale parameter ranges are the builder\'s proposal (pubworld_draft.py docstring); not evidence')
    rows = P.equiv_rows(); out['MP1_equivalence_rerun'] = dict(ok=all(all(v for v in r.values() if isinstance(v, bool)) for r in rows), rows=len(rows))
    ident = []
    for kind, pz in (('noise', dict(kind='noise', q=1.0, s=0.0)), ('stale', dict(kind='stale', q=1.0, Lmax=0))):
        seed = 398_000 + (0 if kind == 'noise' else 1); sm, te = P.draw_nuisance(G('nuis', 'mp10:ident', seed))
        a = P.simulate(seed, 'e', sm is not None, sm, None, None, tele=te); b = P.simulate(seed, 'e', sm is not None, sm, pz, G('pub', 'mp10:ident', seed), tele=te)
        eta, var = P.record_innovations(b['hist']['theta'], b['hist']['ell'], pz)
        ident.append(dict(kind=kind, params=pz, world_identical_to_deterministic=bool(P.same(a['hist']['Xobs'], b['hist']['Xobs']) and all(np.array_equal(x, y) for x, y in zip(a['hist']['theta'], b['hist']['theta']))),
                          record_identical_to_deterministic=bool(all(np.array_equal(x, y) for x, y in zip(a['hist']['ell'], b['hist']['ell']))),
                          eta_max_abs=float(np.abs(eta).max()), var_max=float(var.max()), eta_near_zero=bool(np.abs(eta).max() < 1e-12 and var.max() < 1e-12)))
    out['identities_at_zero_variation'] = ident
    acc = []
    for kind in ('noise', 'stale'):
        for j, route in enumerate(('e', 'theta', 'open', 'none')):
            seed = 398_010 + 10*(kind == 'stale') + j; pub = getattr(P, f'draw_publisher_{kind}')(G('pubpar', f'mp10:acc-{kind}', seed))
            sm = P.PF.draw_geometry(G('geom', f'mp10:acc-{kind}', seed)); te = P.draw_telegraph(G('tele', f'mp10:acc-{kind}', seed))
            sim = P.simulate(seed, route, True, sm, pub, G('pub', f'mp10:acc-{kind}', seed), tele=te); base = P.all_stats(sim)
            fake = P.phantom_record(sim['hist']['theta'], pub, G('phantom', f'mp10:acc-{kind}', seed)); sim2 = dict(sim, hist=dict(sim['hist'], ell=fake, e=fake)); sw = P.all_stats(sim2)
            s3 = P.simulate(seed, route, True, sm, pub, G('pub2', f'mp10:acc-{kind}', seed), tele=te)
            traj_same = P.same(sim['hist']['Xobs'], s3['hist']['Xobs']) and all(np.array_equal(x, y) for x, y in zip(sim['hist']['theta'], s3['hist']['theta']))
            r = dict(kind=kind, route=route, seed=seed, twin_identical_under_record_swap=bool(all(P.same(base[k], sw[k]) for k in TWIN_KEYS) and P.twin_jump(P.twin_view(sim), 60) == P.twin_jump(P.twin_view(sim2), 60)),
                     lag_ri_changed_under_record_swap=bool(not P.same(base['lag_ri_T'], sw['lag_ri_T'])), world_identical_under_stream_swap=bool(traj_same), expected_world_identical=route != 'e')
            r['ok'] = r['twin_identical_under_record_swap'] and r['lag_ri_changed_under_record_swap'] and r['world_identical_under_stream_swap'] == r['expected_world_identical']; acc.append(r)
    out['access'] = acc
    jobs = []
    for kind in ('noise', 'stale'):
        for j in range(12):
            route = ('e', 'theta', 'open', 'none')[j % 4]; seed = 398_040 + 30*(kind == 'stale') + j
            jobs.append(dict(tag='mp10', arm=f'S-{kind}-{route}', route=route, idx=j, seed=seed, pair=f'S-{kind}', pubmode=kind, nuis='drawn',
                             dmode='oracle' if route != 'none' else 'random', c5=True))
    units = [phase1(j) for j in jobs]; probes = []
    for u in units:
        if u['eligible']:
            probes.append(phase2(dict(tag='mp10', arm=u['arm'], idx=u['idx'], route=u['route'], seed=u['seed'], pair=u['pair'], pubmode=u['pubmode'], nuis=u['nuis'],
                                      div=u['div'], ri_state=u['ri_state'], target=u['target'])))
    def p_ok(p): return p is not None and 0 < p <= 1
    comp = []
    for kind in ('noise', 'stale'):
        us = [u for u in units if u['pubmode'] == kind]; ps = [p for p in probes if p['arm'].startswith(f'S-{kind}')]
        comp.append(dict(kind=kind, units=len(us), attributed=sum(u['attr'] is not None for u in us), probed=len(ps),
                         attribution_p_values_valid=bool(all(p_ok(u['attr'][k]) for u in us if u['attr'] is not None for k in ('passive_ri_p', 'lead_ri_p', 'phantom_ri_p'))),
                         intervention_p_values_valid=bool(all(p_ok(p['intervention']['p_e']) and p_ok(p['intervention']['p_theta']) for p in ps)),
                         c5_twin_identical=bool(all(u['c5']['twin_identical'] for u in us)), c6=bool(all(all(u['c6'].values()) for u in us)),
                         every_route_attributed_and_probed=bool({u['route'] for u in us if u['attr'] is not None} >= {'e', 'theta', 'open', 'none'}
                                                                and {u['route'] for u in us if u['eligible']} >= {'e', 'theta', 'open'}),
                         mean_published_rounds=round(float(np.mean([u['n_published'] for u in us])), 2), diverged=sum(u['div'] is not None for u in us),
                         cpu_s_per_unit=round(float(np.mean([u['cpu'] for u in us])), 3)))
    out['run_to_completion'] = comp
    out['ok'] = bool(out['MP1_equivalence_rerun']['ok'] and all(r['world_identical_to_deterministic'] and r['record_identical_to_deterministic'] for r in ident)
                     and all(r['ok'] for r in acc) and all(c['attribution_p_values_valid'] and c['intervention_p_values_valid'] and c['c5_twin_identical'] and c['c6']
                                                          and c['every_route_attributed_and_probed'] for c in comp))
    out['cpu_seconds'] = round(time.process_time() - t0, 1)
    return out

def mode_verify(which, sealed_dir):
    """recompute sha256(salt|payload) from the sealed files and compare it with the public commitment; prints only the match"""
    salt_p, sealed_p, _, _ = seal_paths(which, sealed_dir); pub_p = OUT / ('pilot_public.json' if which == 'pilot' else 'pilot_tiny_public.json')
    sealed = json.load(open(sealed_p)); salt = salt_p.read_text().strip(); c = hashlib.sha256(f"{salt}|{sealed['payload']}".encode('utf-8')).hexdigest()
    pub_c = json.load(open(pub_p))['commitment']['sha256']; ok = c == pub_c == sealed['commitment']
    print(json.dumps(dict(which=which, public_commitment=pub_c, recomputed_matches=ok))); return 0 if ok else 1

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0]); ap.add_argument('mode', choices=('pilot', 'tiny', 'mp10', 'verify', 'verify-tiny'))
    ap.add_argument('--sealed-dir'); ap.add_argument('--workers', type=int, default=MAX_WORKERS); a = ap.parse_args(); OUT.mkdir(exist_ok=True)
    if a.mode == 'mp10': sys.exit(mode_mp10())
    if not a.sealed_dir: ap.error('--sealed-dir (outside the repository) is required for pilot, tiny and verify')
    if a.mode.startswith('verify'): sys.exit(mode_verify('tiny' if a.mode == 'verify-tiny' else 'pilot', a.sealed_dir))
    sys.exit(mode_pilot(a.mode, a.sealed_dir, a.workers))
