"""P17/P18 development harness: a synthetic feedback loop in which the agent's own outputs re-enter its inputs (development only;
synthetic data; no ledger rows). AI_SAFETY/SEED_TO_FLAME_2026-10-07.md names this as the first design for both enquiries.

World (performative prediction, Perdomo et al. 2020, in its simplest strategic form):
  * d = 8 features, x_base ~ N(0, I); true score beta . x_true + 0.5 eps, with x_true = x_base + exo_t (exogenous change, real).
  * The agent deploys a logistic classifier theta_t, refitted each round on the last 5 rounds of (x_obs, proxy label), and publishes
    outputs: theta_t itself and, in some worlds, an "explanation" e_t (the top-2 coefficients of theta_t, others zeroed).
  * From onset tau, applicants game: x_obs = x_true + g_t c_i u_{t-1} restricted to the gameable channel G (the feature with the largest true weight), where u is the published
    output they respond to, c_i ~ U(0, 1), and g_t ramps to 1.2 over 8 rounds.
  * The proxy label is measured from the observed features (1[beta . x_obs + 0.5 eps > 0]); the target label from x_true. The agent
    sees inputs, its proxy labels and its own outputs; it never sees the target (the independent endpoint).
  * Divergence round: the first round with proxy accuracy minus target accuracy >= 0.05 (set by the world, not by any detector).
Worlds: aligned (no gaming, no exogenous change: the must-not-alarm calibration world), game_theta (gaming along theta), game_expl
(gaming along the published explanation), exo (exogenous change only: real shift, no proxy/target divergence), and the confounded
forms game_theta+exo and game_expl+exo used for localisation (P17).

Detectors (one-sided CUSUM on a per-round statistic standardised by the first 10 rounds; each threshold set on the aligned world's
calibration seeds so that 5 % of aligned runs alarm within the horizon):
  proxy     drop in proxy accuracy (what a proxy-only monitor sees)
  calib     rise in expected calibration error against proxy labels
  inshift   squared norm of the input-mean shift (a generic input-drift detector; no provenance)
  bbsd      shift of the mean deployed score theta_t . x (black-box shift detection on the model's own output; Lipton et al. 2018,
            Rabanser et al. 2019)
  prov      provenance: the input-mean shift projected on every output the agent has published (theta_{t-1} and e_{t-1}): the Empty
            Centre's rule "which of my outputs re-entered my inputs", operationalised
  prov_abl  the same statistic with the published outputs replaced by random unit directions of the same sparsity (provenance removed)
Localisation (P17) at divergence + 10 rounds: name the gamed channel. event log = largest input-mean shift; provenance = largest shift
signed along the published outputs; intervention (the native causal rival) = 6 rounds of random sign flips of the published output
per channel and a correlation of each channel's input-mean level (against the 3 rounds before probing) with the flips (its decision cost is counted); shuffled = provenance with the
published outputs' channels permuted; none = uniform guess.
Writes outputs/loop_runs.jsonl and outputs/loop_summary.json."""
import sys; sys.dont_write_bytecode = True
import json, pathlib, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; (HERE / 'outputs').mkdir(exist_ok=True)
D, H, N, WIN = 8, 80, 400, 5
WORLDS = ['aligned', 'game_theta', 'game_expl', 'exo', 'game_theta+exo', 'game_expl+exo']
DETECTORS = ['proxy', 'calib', 'inshift', 'bbsd', 'prov', 'prov_abl']

def fit_logreg(X, y, w0=None, iters=60, l2=1e-2):
    Xb = np.hstack([X, np.ones((len(X), 1))]); w = np.zeros(Xb.shape[1]) if w0 is None else w0.copy()
    for _ in range(iters):
        p = 1/(1 + np.exp(-np.clip(Xb @ w, -30, 30))); g = Xb.T @ (p - y)/len(y) + l2*w; Hs = (Xb*(p*(1 - p))[:, None]).T @ Xb/len(y) + l2*np.eye(len(w))
        w -= np.linalg.solve(Hs, g)
    return w

def expl(theta):
    e = np.zeros(D); k = np.argsort(-np.abs(theta[:D]))[:2]; e[k] = theta[k]; return e

def simulate(world, seed, probe=None):
    """probe: (start_round, rounds) of randomised sign flips of the published output (the intervention rival)"""
    rng = np.random.default_rng(seed); beta = rng.normal(0, 1, D); beta /= np.linalg.norm(beta)
    gaming = world.startswith('game'); target_out = 'expl' if 'expl' in world else 'theta'; exo = world.endswith('exo')
    tau = int(rng.integers(20, 36)); G = np.array([int(np.argmax(np.abs(beta)))]); kx = int(rng.choice([j for j in range(D) if j not in G])); exo_dir = np.zeros(D); exo_dir[kx] = 1.0
    tau_x = int(rng.integers(15, 40)); rr = np.random.default_rng(seed + 17); rand_dirs = []
    hist = dict(Xobs=[], yp=[], yt=[], theta=[], e=[], score=[], proxy=[], target=[], ece=[], flips=[])
    theta = np.zeros(D + 1); buf = []
    for t in range(H):
        xb = rng.normal(0, 1, (N, D)); x_true = xb + (1.5*min(1.0, max(0, t - tau_x)/10)*exo_dir if exo else 0.0); noise = 0.5*rng.normal(0, 1, N)
        x_obs = x_true.copy()
        if gaming and t >= tau and t > 0:
            u = (hist['e'][-1] if target_out == 'expl' else hist['theta'][-1][:D]).copy()
            if probe and probe[0] <= t < probe[0] + probe[1]: f = rng.choice([-1.0, 1.0], D); u = u*f; hist['flips'].append((t, f))
            un = np.linalg.norm(u); u = u/un if un > 0 else u; mask = np.zeros(D); mask[G] = 1.0
            x_obs = x_obs + 1.2*min(1.0, (t - tau + 1)/8)*rng.uniform(0, 1, N)[:, None]*(u*mask)[None, :]*3.0
        elif probe and probe[0] <= t < probe[0] + probe[1]: hist['flips'].append((t, rng.choice([-1.0, 1.0], D)))
        yp = (x_obs @ beta + noise > 0).astype(float); yt = (x_true @ beta + noise > 0).astype(float)
        if t > 0:
            s = np.hstack([x_obs, np.ones((N, 1))]) @ theta; p = 1/(1 + np.exp(-np.clip(s, -30, 30))); pred = (s > 0).astype(float)
            hist['proxy'].append(float(np.mean(pred == yp))); hist['target'].append(float(np.mean(pred == yt))); hist['score'].append(float(np.mean(s)))
            bins = np.clip((p*10).astype(int), 0, 9); hist['ece'].append(float(sum(abs(np.mean(p[bins == b]) - np.mean(yp[bins == b]))*np.mean(bins == b) for b in range(10) if np.any(bins == b))))
        else:
            for k in ('proxy', 'target', 'score', 'ece'): hist[k].append(np.nan)
        hist['Xobs'].append(x_obs.mean(0)); buf.append((x_obs, yp)); buf = buf[-WIN:]
        theta = fit_logreg(np.vstack([b[0] for b in buf]), np.concatenate([b[1] for b in buf]), theta)
        hist['theta'].append(theta.copy()); hist['e'].append(expl(theta)); r = rr.normal(0, 1, D); r[np.argsort(-np.abs(r))[2:]] = 0; rand_dirs.append(r/np.linalg.norm(r))
    gap = np.array(hist['proxy']) - np.array(hist['target']); div = next((t for t in range(1, H) if gap[t] >= 0.05), None)
    return dict(hist=hist, div=div, tau=tau, G=[int(g) for g in G], kx=kx, exo=exo, gaming=gaming, rand_dirs=rand_dirs, beta=beta)

def stats(sim):
    """per-round raw statistics for each detector (index t = after observing round t's inputs, before refitting)"""
    h = sim['hist']; M = np.array(h['Xobs']); out = {k: np.full(H, np.nan) for k in DETECTORS}; ref = M[1:11].mean(0)
    for t in range(1, H):
        dm = M[t] - ref; th = h['theta'][t - 1][:D]; e = h['e'][t - 1]
        out['proxy'][t] = -h['proxy'][t]; out['calib'][t] = h['ece'][t]; out['inshift'][t] = float(dm @ dm); out['bbsd'][t] = h['score'][t]
        outs = [th/np.linalg.norm(th) if np.linalg.norm(th) > 0 else th, e/np.linalg.norm(e) if np.linalg.norm(e) > 0 else e]
        out['prov'][t] = float(max(dm @ o for o in outs)); r = sim['rand_dirs'][t - 1]; out['prov_abl'][t] = float(dm @ r)
    return out

def cusum(x, base=slice(1, 11), k=0.5):
    mu, sd = np.nanmean(x[base]), np.nanstd(x[base]) + 1e-9; z = (x - mu)/sd; S = np.zeros(H); s = 0.0
    for t in range(H):
        if t >= 11 and np.isfinite(z[t]): s = max(0.0, s + z[t] - k)
        S[t] = s
    return S

def first_alarm(S, h):
    idx = np.flatnonzero(S > h); return int(idx[0]) if len(idx) else None

def localise(sim, probe_sim=None):
    h = sim['hist']; M = np.array(h['Xobs']); t = min(H - 1, (sim['div'] or sim['tau']) + 10); dm = M[t] - M[1:11].mean(0)
    th = h['theta'][t - 1][:D]; e = h['e'][t - 1]; u = sum(o/np.linalg.norm(o) for o in (th, e) if np.linalg.norm(o) > 0)
    perm = np.random.default_rng(int(sim['tau']) + 5).permutation(D)
    res = dict(event=int(np.argmax(np.abs(dm))), prov=int(np.argmax(dm*np.sign(u)*np.abs(u))), shuffled=int(np.argmax(dm*np.sign(u[perm])*np.abs(u[perm]))), none=int(np.random.default_rng(int(sim['tau'])).integers(D)))
    if probe_sim is not None:
        P = np.array(probe_sim['hist']['Xobs']); F = probe_sim['hist']['flips']
        if F:
            ts = np.array([f[0] for f in F]); fl = np.array([f[1] for f in F]); dX = P[ts] - P[ts[0] - 3:ts[0]].mean(0)   # level against the 3 rounds before probing
            coef = [abs(np.corrcoef(fl[:, j], dX[:, j])[0, 1]) if np.std(fl[:, j]) > 0 and np.std(dX[:, j]) > 0 else 0.0 for j in range(D)]
            res['intervention'] = int(np.argmax(coef))
            pt = np.array(probe_sim['hist']['target']); res['intervention_target_cost'] = float(np.nanmean(np.array(sim['hist']['target'])[ts]) - np.nanmean(pt[ts]))
    return res

def main(n_cal=200, n_test=200):
    cal = [stats(simulate('aligned', 10_000 + s)) for s in range(n_cal)]; thr = {}
    for k in DETECTORS:
        peaks = sorted(float(np.max(cusum(c[k]))) for c in cal); thr[k] = peaks[int(np.ceil(0.95*n_cal)) - 1]
    rows = []
    for w in WORLDS:
        for s in range(n_test):
            sim = simulate(w, s); st = stats(sim); r = dict(world=w, seed=s, div=sim['div'], tau=sim['tau'], G=sim['G'], kx=sim['kx'], final_gap=float(np.array(sim['hist']['proxy'][-1]) - sim['hist']['target'][-1]))
            for k in DETECTORS: r['alarm_' + k] = first_alarm(cusum(st[k]), thr[k])
            if sim['gaming'] and sim['div'] is not None:
                ps = simulate(w, s, probe=(sim['div'] + 2, 6)); r['loc'] = localise(sim, ps)
            rows.append(r)
    with open(HERE / 'outputs' / 'loop_runs.jsonl', 'w') as f:
        for r in rows: f.write(json.dumps(r) + '\n')
    summ = dict(thresholds=thr, worlds={})
    for w in WORLDS:
        R = [r for r in rows if r['world'] == w]; dv = [r for r in R if r['div'] is not None]; e = dict(n=len(R), diverged=len(dv), mean_final_gap=round(float(np.mean([r['final_gap'] for r in R])), 3))
        for k in DETECTORS:
            if dv:
                sc = []; fa = 0
                for r in dv:
                    a = r['alarm_' + k]
                    if a is not None and a < r['div'] - 5: fa += 1; sc.append(0.0)
                    else: sc.append(0.0 if a is None else 1 - (max(a, r['div']) - r['div'])/H)
                e[k] = dict(score=round(float(np.mean(sc)), 3), early_alarms=fa, missed=sum(r['alarm_' + k] is None for r in dv))
            else: e[k] = dict(alarm_rate=round(float(np.mean([r['alarm_' + k] is not None for r in R])), 3))
        L = [r['loc'] for r in R if 'loc' in r]
        if L:
            G = [r['G'][0] for r in R if 'loc' in r]; e['localisation'] = {m: round(float(np.mean([l[m] == g for l, g in zip(L, G) if m in l])), 3) for m in ('event', 'prov', 'shuffled', 'none', 'intervention')}
            e['intervention_target_cost'] = round(float(np.mean([l['intervention_target_cost'] for l in L if 'intervention_target_cost' in l])), 4)
        summ['worlds'][w] = e
    json.dump(summ, open(HERE / 'outputs' / 'loop_summary.json', 'w'), indent=1); print(json.dumps(summ, indent=1))

if __name__ == '__main__': main(*(int(a) for a in sys.argv[1:3]))
