"""P18-PROV-FLAME draft world (NOT FROZEN; a helper for DECLARATION_DRAFT.md; development seeds only; no ledger rows).

It generalises studies/P18-LOOP1-2026-10-08/loopworld.py (imported, not copied) in five ways:
  1. Drawn confounder geometry. In the '+exo' and 'exo' worlds the exogenous, label-consistent shift of x_true is mag * ramp(t) * v,
     where (support, v, mag) come from a geometry generator that is separate from the world generator, so the geometry knows nothing
     of beta, of the gameable channel G or of the published outputs:
       channel   k ~ U{1..8}; support = k channels drawn uniformly without replacement from all 8 (G and the published top-2 included)
       direction w ~ N(0, I_k) on the support, v = w / |w| (so k = 8 is isotropic on the sphere)
       magnitude mag = exp(U(log 0.75, log 3.0)) (log-uniform; geometric mean 1.5, the development magnitude)
     Onset tau_x and the 10-round ramp come from the world generator exactly as in loopworld.py. geom=None gives the development
     (designed) geometry: one-hot on a channel kx != G, magnitude 1.5.
  2. Three extra detectors, all thresholded on the aligned world like the others:
       prov_theta  input-mean shift projected on theta_{t-1}/|theta_{t-1}| only (prov without the published explanation)
       pf_twin     provenance-free twin: max of the projections on theta_{t-1} and on top2(theta_{t-1}), recomputed from theta alone
                   without reading the published-output record (identical to prov in this harness, because e = top2(theta))
       prov_shuf   prov with the published outputs' channels permuted (shuffled annotations, used for detection)
  3. The binary endpoint: timely detection = first alarm a with div - 5 <= a <= div + W (W = 5 registered; 3, 10, 20 sensitivity).
  4. Probe flips (the intervention rival) come from a separate generator, so the probed trajectory shares the world's random numbers
     until the flips act (common random numbers; loopworld.py drew them from the world generator).
  5. Optional drawn gameable channel (sensitivity S9): G uniform over the 8 channels instead of argmax |beta|.
  6. Two discriminating surrogate worlds:
       open_loop=True       applicants shift G along a fixed direction taken from beta (beta for the theta-type worlds, top2(beta)
                            for the expl-type worlds) instead of the agent's published output: a proxy/target divergence with no
                            re-entry of the agent's outputs. Probe flips change the published output but nobody responds to them.
                            The correct answer to "which of my outputs re-entered my inputs?" is "none".
       geom mode 'on_published'  the confounder lies on the signed top-2 support of beta (where the published explanation sits);
                            magnitude drawn as in the family. The ordinary (matched-filter) account predicts no prov edge here.

Draw rule (for the frozen study; here only demonstrated with a dummy string, never with a real block hash):
  unit seed  s(tag, i) = 1_000_000 + int(sha256('<freeze commit>|<block hash>|<tag>|<i>')[:15], 16)   (a 60-bit range: with about 16 000
             held-out units the chance of any repeated seed is about 1e-10; the frozen draw still asserts uniqueness)
  geometry   default_rng(int(sha256('<freeze commit>|<block hash>|geom|<tag>|<i>')[:16], 16))
  flips      default_rng(int(sha256('<freeze commit>|<block hash>|flip|<tag>|<i>')[:16], 16))
  All development seeds are below 1_000_000 (0..199, 10_000..10_199, their +17 offsets, and this file's 500..999 and 20_000..20_999),
  so no held-out unit can reuse a development world.

Usage (from anywhere; each mode is under 60 CPU-seconds):
  python3 -I provworld_draft.py equiv     with the development geometry and no probe, simulate() must reproduce loopworld.simulate()
                                          array for array; writes outputs/equiv_check.json
  python3 -I provworld_draft.py tiny      code-path check on a tiny configuration (development seeds); writes outputs/tiny_check.json
  python3 -I provworld_draft.py geomstats summary of the declared geometry distribution (no simulation); writes outputs/geom_stats.json
"""
import sys; sys.dont_write_bytecode = True
import json, hashlib, pathlib, time, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; DEV = HERE.parent / 'P18-LOOP1-2026-10-08'; (HERE / 'outputs').mkdir(exist_ok=True)
sys.path.insert(0, str(DEV)); import loopworld as L   # noqa: E402  (development harness; read only)
D, H, N, WIN = L.D, L.H, L.N, L.WIN
DETECTORS = L.DETECTORS + ['prov_theta', 'pf_twin', 'prov_shuf']
MAG_LO, MAG_HI, EARLY, W_PRIMARY = 0.75, 3.0, 5, 5
HELDOUT_BASE = 1_000_000

def sha_int(s, nhex): return int(hashlib.sha256(s.encode()).hexdigest()[:nhex], 16)
def unit_seed(fc, bh, tag, i): return HELDOUT_BASE + sha_int(f'{fc}|{bh}|{tag}|{i}', 15)
def geom_rng(fc, bh, tag, i): return np.random.default_rng(sha_int(f'{fc}|{bh}|geom|{tag}|{i}', 16))
def flip_rng(fc, bh, tag, i): return np.random.default_rng(sha_int(f'{fc}|{bh}|flip|{tag}|{i}', 16))

def draw_geometry(g):
    """the declared confounder distribution; g is the geometry generator (never the world generator)"""
    k = int(g.integers(1, D + 1)); sup = np.sort(g.choice(D, k, replace=False)); w = g.normal(0, 1, k); v = np.zeros(D); v[sup] = w/np.linalg.norm(w)
    mag = float(np.exp(g.uniform(np.log(MAG_LO), np.log(MAG_HI)))); gch = int(g.integers(D))   # gch used only by sensitivity S9
    return dict(k=k, support=[int(j) for j in sup], v=v, mag=mag, g_channel=gch)

def simulate(world, seed, geom=None, probe=None, frng=None, drawn_G=False, open_loop=False):
    """loopworld.simulate with a drawn confounder (geom), probe flips from frng, and an optional drawn gameable channel.
    The world generator's call sequence is the same as loopworld.simulate's, so geom=None and probe=None reproduce it exactly."""
    rng = np.random.default_rng(seed); beta = rng.normal(0, 1, D); beta /= np.linalg.norm(beta)
    gaming = world.startswith('game'); target_out = 'expl' if 'expl' in world else 'theta'; exo = world.endswith('exo')
    tau = int(rng.integers(20, 36)); G = np.array([int(np.argmax(np.abs(beta)))]); kx = int(rng.choice([j for j in range(D) if j not in G]))
    tau_x = int(rng.integers(15, 40)); rr = np.random.default_rng(seed + 17); rand_dirs = []
    if drawn_G and geom is not None: G = np.array([geom['g_channel']])
    if geom is None: v = np.zeros(D); v[kx] = 1.0; mag = 1.5
    elif geom.get('mode') == 'on_published': v = unit(L.expl(np.append(beta, 0.0))); mag = geom['mag']
    else: v, mag = geom['v'], geom['mag']
    u_open = (L.expl(np.append(beta, 0.0)) if target_out == 'expl' else beta).copy()
    hist = dict(Xobs=[], theta=[], e=[], score=[], proxy=[], target=[], ece=[], flips=[])
    theta = np.zeros(D + 1); buf = []
    for t in range(H):
        xb = rng.normal(0, 1, (N, D)); x_true = xb + (mag*min(1.0, max(0, t - tau_x)/10)*v if exo else 0.0); noise = 0.5*rng.normal(0, 1, N)
        x_obs = x_true.copy(); probing = probe is not None and probe[0] <= t < probe[0] + probe[1]
        if probing: f = frng.choice([-1.0, 1.0], D); hist['flips'].append((t, f))
        if gaming and t >= tau and t > 0:
            if open_loop: u = u_open.copy()          # no re-entry: the flips below are not seen by applicants
            else:
                u = (hist['e'][-1] if target_out == 'expl' else hist['theta'][-1][:D]).copy()
                if probing: u = u*f
            un = np.linalg.norm(u); u = u/un if un > 0 else u; mask = np.zeros(D); mask[G] = 1.0
            x_obs = x_obs + 1.2*min(1.0, (t - tau + 1)/8)*rng.uniform(0, 1, N)[:, None]*(u*mask)[None, :]*3.0
        yp = (x_obs @ beta + noise > 0).astype(float); yt = (x_true @ beta + noise > 0).astype(float)
        if t > 0:
            s = np.hstack([x_obs, np.ones((N, 1))]) @ theta; p = 1/(1 + np.exp(-np.clip(s, -30, 30))); pred = (s > 0).astype(float)
            hist['proxy'].append(float(np.mean(pred == yp))); hist['target'].append(float(np.mean(pred == yt))); hist['score'].append(float(np.mean(s)))
            bins = np.clip((p*10).astype(int), 0, 9); hist['ece'].append(float(sum(abs(np.mean(p[bins == b]) - np.mean(yp[bins == b]))*np.mean(bins == b) for b in range(10) if np.any(bins == b))))
        else:
            for k in ('proxy', 'target', 'score', 'ece'): hist[k].append(np.nan)
        hist['Xobs'].append(x_obs.mean(0)); buf.append((x_obs, yp)); buf = buf[-WIN:]
        theta = L.fit_logreg(np.vstack([b[0] for b in buf]), np.concatenate([b[1] for b in buf]), theta)
        hist['theta'].append(theta.copy()); hist['e'].append(L.expl(theta)); r = rr.normal(0, 1, D); r[np.argsort(-np.abs(r))[2:]] = 0; rand_dirs.append(r/np.linalg.norm(r))
    gap = np.array(hist['proxy']) - np.array(hist['target']); div = next((t for t in range(1, H) if gap[t] >= 0.05), None)
    return dict(hist=hist, div=div, tau=tau, G=[int(g) for g in G], kx=kx, exo=exo, gaming=gaming, rand_dirs=rand_dirs, beta=beta)

def unit(x): n = np.linalg.norm(x); return x/n if n > 0 else x

def stats(sim):
    """loopworld.stats plus prov_theta, pf_twin and prov_shuf"""
    out = L.stats(sim); h = sim['hist']; M = np.array(h['Xobs']); ref = M[1:11].mean(0); perm = np.random.default_rng(int(sim['tau']) + 5).permutation(D)
    for k in ('prov_theta', 'pf_twin', 'prov_shuf'): out[k] = np.full(H, np.nan)
    for t in range(1, H):
        dm = M[t] - ref; th = h['theta'][t - 1][:D]; e = h['e'][t - 1]
        out['prov_theta'][t] = float(dm @ unit(th))
        out['pf_twin'][t] = float(max(dm @ unit(th), dm @ unit(L.expl(h['theta'][t - 1]))))   # from theta only; never reads h['e']
        out['prov_shuf'][t] = float(max(dm @ unit(th[perm]), dm @ unit(e[perm])))
    return out

def timely(a, div, W=W_PRIMARY): return int(a is not None and div - EARLY <= a <= div + W)
def score(a, div): return 0.0 if a is None or a < div - EARLY else 1 - (max(a, div) - div)/H

def thresholds(cal_stats, far=0.05):
    n = len(cal_stats); return {k: sorted(float(np.max(L.cusum(c[k]))) for c in cal_stats)[int(np.ceil((1 - far)*n)) - 1] for k in DETECTORS}

def run_unit(world, seed, geom, thr, frng=None, probe_rounds=6, drawn_G=False, open_loop=False):
    sim = simulate(world, seed, geom, drawn_G=drawn_G, open_loop=open_loop); st = stats(sim)
    r = dict(world=world, seed=seed, open_loop=open_loop, div=sim['div'], tau=sim['tau'], G=sim['G'],
             geom=None if geom is None else dict(mode=geom.get('mode', 'drawn'), k=geom.get('k'), support=geom.get('support'), mag=round(geom['mag'], 4)))
    for k in DETECTORS: r['alarm_' + k] = L.first_alarm(L.cusum(st[k]), thr[k])
    r['pf_twin_equals_prov'] = bool(np.allclose(st['pf_twin'][1:], st['prov'][1:], rtol=0, atol=1e-12))
    if sim['gaming'] and sim['div'] is not None:
        r['timely'] = {k: timely(r['alarm_' + k], sim['div']) for k in DETECTORS}
        if frng is not None:
            ps = simulate(world, seed, geom, probe=(sim['div'] + 2, probe_rounds), frng=frng, drawn_G=drawn_G, open_loop=open_loop); r['loc'] = L.localise(sim, ps)
    return r

def mode_equiv():
    res = []
    for w, s in (('aligned', 2), ('game_theta+exo', 0), ('exo', 1), ('game_expl', 3)):
        a, b = L.simulate(w, s), simulate(w, s); ha, hb = a['hist'], b['hist']
        same = all(np.array_equal(np.asarray(ha[k], float), np.asarray(hb[k], float), equal_nan=True) for k in ('Xobs', 'score', 'proxy', 'target', 'ece')) \
            and all(np.array_equal(x, y) for x, y in zip(ha['theta'], hb['theta'])) and a['div'] == b['div']
        sa, sb = L.stats(a), stats(b); same_stats = all(np.array_equal(sa[k], sb[k], equal_nan=True) for k in L.DETECTORS)
        res.append(dict(world=w, seed=s, trajectory_identical=bool(same), dev_stats_identical=bool(same_stats), div=b['div'],
                        pf_twin_equals_prov=bool(np.allclose(sb['pf_twin'][1:], sb['prov'][1:], rtol=0, atol=1e-12))))
    out = dict(mode='equiv', note='development seeds; geom=None (designed geometry); no probe', rows=res, ok=all(r['trajectory_identical'] and r['dev_stats_identical'] for r in res))
    json.dump(out, open(HERE / 'outputs' / 'equiv_check.json', 'w'), indent=1); print(json.dumps(out, indent=1)); return 0 if out['ok'] else 1

def mode_tiny():
    """code paths only: thresholds from 6 aligned runs are far too coarse to mean anything; nothing here is evidence"""
    t0 = time.process_time(); fc, bh = 'DEVELOPMENT-ONLY', 'NOT-A-BLOCK-HASH'
    cal = [stats(simulate('aligned', 20_000 + s)) for s in range(6)]; thr = thresholds(cal)
    rows = []
    for j, w in enumerate(('game_theta+exo', 'game_expl+exo', 'exo')):
        i = j; s = 500 + i; g = draw_geometry(geom_rng(fc, bh, 'tiny', i))
        rows.append(run_unit(w, s, g, thr, frng=flip_rng(fc, bh, 'tiny', i)))
    g = draw_geometry(geom_rng(fc, bh, 'tiny', 9)); rows.append(run_unit('game_theta+exo', 509, g, thr, frng=flip_rng(fc, bh, 'tiny', 9), drawn_G=True))
    g = draw_geometry(geom_rng(fc, bh, 'tiny', 0)); rows.append(run_unit('game_theta+exo', 500, g, thr, frng=flip_rng(fc, bh, 'tiny', 0), open_loop=True))   # paired with unit 500
    g = dict(mode='on_published', mag=draw_geometry(geom_rng(fc, bh, 'tiny', 11))['mag']); rows.append(run_unit('game_expl+exo', 511, g, thr, frng=flip_rng(fc, bh, 'tiny', 11)))
    demo = [unit_seed('x', 'y', 't', i) for i in range(1000)]; seeds_ok = min(demo) >= HELDOUT_BASE and len(set(demo)) == len(demo)
    out = dict(mode='tiny', cpu_seconds=round(time.process_time() - t0, 2), sims=6 + len(rows) + sum('loc' in r for r in rows), thresholds={k: round(v, 3) for k, v in thr.items()},
               rows=rows, heldout_seed_range_ok=seeds_ok, note='code-path check; 6 calibration runs; development seeds 500..509 and 20000..20005; not evidence')
    json.dump(out, open(HERE / 'outputs' / 'tiny_check.json', 'w'), indent=1, default=float); print(json.dumps(out, indent=1, default=float)); return 0

def mode_geomstats(n=200_000):
    """Monte Carlo of the declared geometry distribution against the published top-2 support (no world simulation): how often the
    confounder lies wholly off a given 2-channel support, as the development geometry did whenever kx was not the second channel"""
    g = np.random.default_rng(12345); top2 = {0, 1}; off = 0; onG = []; frac_top2 = []; mags = []
    for _ in range(n):
        x = draw_geometry(g); s = set(x['support']); off += not (s & top2); onG.append(abs(x['v'][0])); frac_top2.append(float(np.sum(x['v'][[0, 1]]**2))); mags.append(x['mag'])
    out = dict(mode='geomstats', n=n, p_wholly_off_top2=round(off/n, 4), p_wholly_off_top2_exact=0.25, mean_energy_on_top2=round(float(np.mean(frac_top2)), 4),
               mean_abs_component_on_G=round(float(np.mean(onG)), 4), magnitude_quantiles=[round(float(q), 3) for q in np.percentile(mags, [5, 25, 50, 75, 95])],
               development_geometry=dict(p_wholly_off_top2=round(6/7, 4), note='one-hot on kx uniform over the 7 channels other than G; off the top-2 unless kx is the second channel'))
    json.dump(out, open(HERE / 'outputs' / 'geom_stats.json', 'w'), indent=1); print(json.dumps(out, indent=1)); return 0

if __name__ == '__main__': sys.exit({'equiv': mode_equiv, 'tiny': mode_tiny, 'geomstats': mode_geomstats}[sys.argv[1]]())
