"""SEC-OBS1 episode runner (development and, unchanged once frozen, held-out).

One episode = one underlying history (random task pair with overlap o, task-A maturity m). Everything that trains is run once per history and is
therefore identical across the eight observation conditions; the conditions change only what the monitors (and the tuned sweep's task-A
validation) can see. Per episode the runner records:
  * true (territory) evaluations of every arm: none, frozen, head-only, GPM-only, SEC v2, SEC+GPM from the start, a constant-kappa grid
    (the sweep candidates and the transferred-constant candidates), and the decision-point branches at step k: SEC continued with
    kappa x {1/16, 1/4, 1, 4}, SEC + GPM from k, SEC + replay (64-sample clean buffer) from k;
  * per observation condition: native, observation-aware and CRR-path features at step k on the SEC trajectory; the tuned sweep's selection
    using that condition's task-A validation; and two direction-calibrated SEC branches (candidate 3) run from step k;
  * costs: seconds for every component and the stored floats.
No feature, selection rule or calibration below reads the territory test sets; `true_eval` is called only to record outcomes."""
import sys, json, time, math, argparse, pathlib, warnings, numpy as np, torch, torch.nn.functional as Fn
warnings.filterwarnings('ignore')
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
from secobs_lib import *

STEPS_B, K_DEC, CHECKS = 400, 100, (0, 25, 50, 75, 100)
MU = (1/16, 1/4, 1, 4)
GRID = (3, 10, 30, 100, 300, 1000, 3000)
CONDITIONS = ('full', 'proj', 'alias', 'missing', 'drift', 'concept', 'hideA', 'hideA+ref')
N_PROBE, N_BUF, ALPHA = 256, 64, 10.0

def model_fisher_diag(m, x, rng, task='A', merge=None, n_micro=64, micro=2):
    """label-free (model) Fisher diagonal: labels sampled from the model's own (observed) predictive distribution"""
    acc = torch.zeros_like(flat(m))
    for _ in range(n_micro):
        idx = rng.integers(0, len(x), micro); m.zero_grad()
        lp = log_probs(m, x[idx], task, merge); yy = torch.multinomial(lp.detach().exp(), 1).squeeze(1)
        Fn.nll_loss(lp, yy).backward(); g = grad_flat(m); acc += g*g
    m.zero_grad(); return acc/n_micro

def fr_dist(p, q):
    """Fisher-Rao distance between categorical rows (2 arccos of the Bhattacharyya coefficient)"""
    bc = np.clip(np.sqrt(p*q).sum(-1), 0.0, 1.0); return 2.0*np.arccos(bc)

def probs(theta, x, merge=None):
    m = Net(); set_flat(m, theta)
    with torch.no_grad(): return log_probs(m, x, 'A', merge).exp().numpy()

def trunk_feats(theta, x):
    m = Net(); set_flat(m, theta)
    with torch.no_grad(): return m.trunk(torch.as_tensor(x)).numpy()

def cka(X, Y):
    X = X - X.mean(0); Y = Y - Y.mean(0); num = np.linalg.norm(Y.T @ X)**2; den = np.linalg.norm(X.T @ X)*np.linalg.norm(Y.T @ Y)
    return float(num/den) if den > 0 else 0.0

def loss_grad(theta, x, y, task, merge=None, mask=None):
    m = Net(); set_flat(m, theta); m.zero_grad(); l = loss_fn(m, x, y, task, merge); l.backward(); g = grad_flat(m)
    return float(l.detach()), (g if mask is None else g*mask)

def eff_rank_grads(theta, x, y, merge, n=64):
    m = Net(); set_flat(m, theta); G = []
    for i in range(min(n, len(x))):
        m.zero_grad(); loss_fn(m, x[i:i + 1], y[i:i + 1], 'A', merge).backward(); G.append(grad_flat(m).numpy())
    G = np.array(G); ev = np.clip(np.linalg.eigvalsh(G @ G.T), 0, None); p = ev/ev.sum() if ev.sum() > 0 else ev
    p = p[p > 0]; return float(np.exp(-(p*np.log(p)).sum()))

def features(pre, hist, ck, x, y, merge, x0, y0, Fobs_emp, Fobs_mod, xB, yB, mask):
    """everything a monitor can compute at the decision step from: the anchor and stored end-of-A quantities (theta_A, F, model F, s, GPM
    bases, recorded clean loss/entropy), the SEC trajectory's checkpoints, the observed task-A probes (x, y, merge) at step k, the observed
    probes from step 0 (x0, y0; the monitor's own step-0 baseline), and current task-B data."""
    t0 = time.time(); thA, thk = ck[0], ck[K_DEC]; v = thk - thA; rec = pre['rec']
    m = Net(); set_flat(m, thk); Lk = eval_loss(m, x, y, 'A', merge); set_flat(m, thA); LA0 = eval_loss(m, x, y, 'A', merge); L00 = eval_loss(m, x0, y0, 'A', merge)
    Hobs = marginal_entropy(y, merge); f = {}
    # native (no CRR quantity)
    f['rise_rec'] = Lk - rec['L']                                         # observed loss now vs the recorded clean end-of-A loss
    f['rise_0'] = Lk - L00                                                # observed loss now vs the monitor's step-0 baseline
    _, gB = loss_grad(thk, xB, yB, 'B', None, mask); _, gA = loss_grad(thk, x, y, 'A', merge, mask)
    f['gconf'] = float(gB @ gA/(gB.norm()*gA.norm() + 1e-12))           # gradient conflict (trunk)
    e = subspace_energy(m, xB, pre['gpm']); f['ovl1'], f['ovl2'] = e        # B's input energy inside A's stored GPM subspaces (at the anchor)
    f['fdisp'] = 0.5*float((pre['F']*v*v).sum())                          # EWC-style predicted loss rise from SEC's stored Fisher
    f['fdisp_mod'] = 0.5*float((pre['F_mod']*v*v).sum())                  # same with the stored model Fisher
    f['cka'] = cka(trunk_feats(thA, x), trunk_feats(thk, x))               # representation similarity anchor vs now, on observed inputs
    f['erank'] = eff_rank_grads(thk, x, y, merge)                         # effective rank of the observed per-sample gradient Gram ("Fisher rank")
    set_flat(m, thk); f['LBk'] = eval_loss(m, xB, yB, 'B'); set_flat(m, thA); f['LB0'] = eval_loss(m, xB, yB, 'B'); f['Bprog'] = f['LB0'] - f['LBk']
    f['s'] = pre['s']; f['Lrec'] = rec['L']; f['logmat'] = math.log(pre['steps'])
    # observation-aware (CRR-motivated distinction; ordinary mathematics)
    f['d_anchor'] = Lk - LA0                                              # anchor re-evaluated on the same observed probes
    f['iota'] = (Hobs - LA0)/max(rec['H'] - rec['L'], 1e-6)                 # observable share of the anchor's task-A knowledge
    f['r_anchor'] = f['d_anchor']/max(Hobs - LA0, 0.05)
    vv = v*v; f['eta_mod'] = float((Fobs_mod*vv).sum()/max(float((pre['F_mod']*vv).sum()), 1e-30))   # direction-dependent visibility of the move
    f['eta_emp'] = float((Fobs_emp*vv).sum()/max(float((pre['F']*vv).sum()), 1e-30))
    f['d_corr'] = f['d_anchor']/max(f['eta_mod'], 0.05)
    # CRR path quantities on the observed probes (Fisher-Rao length of the output-distribution path across the checkpoints)
    P = [probs(ck[t], x, merge) for t in CHECKS]
    seg = [fr_dist(P[i], P[i + 1]).mean() for i in range(len(P) - 1)]; C = float(sum(seg)); chord = float(fr_dist(P[0], P[-1]).mean())
    f['coh'] = C; f['chord'] = chord; f['surplus'] = C - chord; f['surplus_frac'] = (C - chord)/C if C > 0 else 0.0
    f['kl_anchor'] = float((P[0]*(np.log(P[0] + 1e-12) - np.log(P[-1] + 1e-12))).sum(-1).mean())
    f['_seconds'] = time.time() - t0
    return f

def direction_secant(pre, ck, x, y, merge, Fobs_emp):
    """candidate 3: SEC's secant measured along the actual task-B displacement v = theta_k - theta_A on the observed probes;
    (a) c_v / rho_ref with SEC's stored Fisher; (b) c_v / rho_obs with the observed-probe Fisher (the eta-corrected form)"""
    thA, thk = ck[0], ck[K_DEC]; v = thk - thA; nv2 = float(v @ v)
    LA, g = loss_grad(thA, x, y, 'A', merge); m = Net(); set_flat(m, thk); Lk = eval_loss(m, x, y, 'A', merge)
    c = 2.0*(Lk - LA - float(g @ v))/nv2; rho_ref = float((pre['F']*v*v).sum())/nv2; rho_obs = float((Fobs_emp*v*v).sum())/nv2
    sa = float(np.clip(c/rho_ref, 1e-3, 1e6)) if (c > 0 and rho_ref > 0) else None
    sb = float(np.clip(c/rho_obs, 1e-3, 1e6)) if (c > 0 and rho_obs > 0) else None
    return dict(c_v=c, rho_ref=rho_ref, rho_obs=rho_obs, s_a=sa, s_b=sb)

def head_refit_A(theta, xbuf, ybuf, hist, seed):
    """recovery probe: refit task A's head on the 64-sample clean buffer (trunk fixed) and evaluate on the territory A set"""
    from sklearn.linear_model import LogisticRegression
    F_ = trunk_feats(theta, xbuf); clf = LogisticRegression(C=1.0, max_iter=2000).fit(F_, ybuf)
    rng = np.random.default_rng(seed + 99); xA, yA, _ = sample(hist, 'A', 4000, rng); P = clf.predict_proba(trunk_feats(theta, xA))
    full = np.full((len(yA), KCLS), 1e-6); full[:, clf.classes_] = P; full /= full.sum(1, keepdims=True)
    return float(-np.log(full[np.arange(len(yA)), yA]).mean())

def run_episode(ep):
    t_ep = time.time(); hs, ov, mat = ep['hseed'], ep['overlap'], ep['mat']; hist = make_history(hs, ov); out = dict(ep)
    pre = train_A(hist, mat, hs); kSEC = ALPHA*pre['s']
    xA_cal, _, _ = sample(hist, 'A', 2000, np.random.default_rng(hs + 5)); mA = Net(); set_flat(mA, pre['theta_A']); t1 = time.time()
    pre['F_mod'] = model_fisher_diag(mA, xA_cal, np.random.default_rng(hs + 6)); t_fmod = time.time() - t1
    xbuf, ybuf, _ = sample(hist, 'A', N_BUF, np.random.default_rng(hs + 20)); xbig, ybig, _ = sample(hist, 'A', 1000, np.random.default_rng(hs + 21))
    out['pre'] = dict(s=pre['s'], c=pre['c'], rho=pre['rho'], kSEC=kSEC, rec=pre['rec'], gpm_dims=pre['gpm_dims'], seconds_train=pre['seconds_train'],
                      seconds_calibration=pre['seconds_calibration'], seconds_gpm=pre['seconds_gpm'], seconds_fmod=t_fmod, frozen=true_eval(pre['theta_A'], hist, hs),
                      Fmean=float(pre['F'].mean()), Fmod_mean=float(pre['F_mod'].mean()))
    runs = {}
    def rec_run(name, **kw):
        r = continue_B(pre, hist, hs, steps=STEPS_B, **kw); runs[name] = dict(true=true_eval(r['theta'], hist, hs), seconds=r['seconds'], seconds_gpm=r['seconds_gpm'], seconds_prox=r['seconds_prox']); return r
    # whole-run arms
    rnone = rec_run('none'); rec_run('headonly', trunk_frozen=True); rec_run('gpm', gpm_from=0); rec_run('sec+gpm', kappa=kSEC, gpm_from=0)
    rec_run('replay64', replay=(xbuf, ybuf), replay_from=0); rec_run('replay1000', replay=(xbig, ybig), replay_from=0); rec_run('sec+replay1000', kappa=kSEC, replay=(xbig, ybig), replay_from=0)
    grid_theta = {0: rnone['theta']}
    for g in GRID: grid_theta[g] = rec_run(f'k{g}', kappa=g)['theta']
    # two decision designs: D1 = SEC from step 0 (diagnose SEC's own trajectory); D2 = plastic pilot at kSEC/16 (diagnose a trajectory that is allowed to move)
    traj = {}
    for D, k0 in (('D1', kSEC), ('D2', kSEC/16)):
        r = rec_run(f'{D}:pilot', kappa=k0, checkpoints=CHECKS); ck = r['checkpoints']; traj[D] = (k0, ck)
        for mu in MU:
            if abs(k0*1.0 - kSEC*mu) > 1e-9*kSEC: rec_run(f'{D}:mu{mu:g}', kappa=k0, kappa_from=(K_DEC, kSEC*mu))
        rec_run(f'{D}:gpm@k', kappa=k0, gpm_from=K_DEC); rec_run(f'{D}:replay64@k', kappa=k0, replay=(xbuf, ybuf), replay_from=K_DEC)
        rec_run(f'{D}:secgpm@k', kappa=k0, kappa_from=(K_DEC, kSEC), gpm_from=K_DEC)
        rchk = continue_B(pre, hist, hs, steps=K_DEC, kappa=k0); out[f'{D}_branch_identical'] = bool(torch.equal(rchk['theta'], ck[K_DEC]))
        out.setdefault('true_at_k', {})[D] = dict(anchor=out['pre']['frozen'], k=true_eval(ck[K_DEC], hist, hs))   # outcome record only (territory)
    runs['sec'] = runs['D1:pilot']
    out['refit_A'] = dict(none=head_refit_A(rnone['theta'], xbuf, ybuf, hist, hs))
    # monitoring data (task B is the current task and is fully observed)
    xB, yB, _ = sample(hist, 'B', 256, np.random.default_rng(hs + 30)); xBv, yBv, _ = sample(hist, 'B', 512, np.random.default_rng(hs + 31))
    mask = trunk_mask(Net()); cond = {}
    x0, y0, _ = Channel('full', hist, np.random.default_rng(hs + 40)).probes(hist, N_PROBE, np.random.default_rng(hs + 41))   # step-0 probes (clean)
    for ci, cname in enumerate(CONDITIONS):
        kind = 'hideA' if cname == 'hideA+ref' else cname; ch = Channel(kind, hist, np.random.default_rng(hs + 50 + ci))
        x, y, merge = ch.probes(hist, N_PROBE, np.random.default_rng(hs + 60 + ci))
        xv, yv, _ = ch.probes(hist, N_PROBE, np.random.default_rng(hs + 70 + ci))
        if cname == 'hideA+ref': x, y, merge, xv, yv = xbuf, ybuf, None, xbuf, ybuf     # the additional source: the clean reference buffer
        t1 = time.time(); mA = Net(); set_flat(mA, pre['theta_A'])
        Fo_emp = fisher_diag(mA, x, y, 'A', np.random.default_rng(hs + 80 + ci), merge=merge); Fo_mod = model_fisher_diag(mA, x, np.random.default_rng(hs + 90 + ci), merge=merge)
        t_fobs = time.time() - t1; cd = dict(seconds_fobs=t_fobs)
        # tuned sweep: choose kappa in {0} + GRID by observed validation J (task-A validation through this condition, task-B validation clean)
        mm = Net(); sel = {}
        for g, th in grid_theta.items():
            set_flat(mm, th); sel[g] = 0.5*(eval_loss(mm, xv, yv, 'A', merge) + eval_loss(mm, xBv, yBv, 'B'))
        cd['sweep'] = dict(kappa=min(sel, key=sel.get), obsJ=sel)
        for D, (k0, ck) in traj.items():
            f = features(pre, hist, ck, x, y, merge, x0, y0, Fo_emp, Fo_mod, xB, yB, mask)
            ds = direction_secant(pre, ck, x, y, merge, Fo_emp); c3 = {}
            for tag in ('a', 'b'):
                s_new = ds[f's_{tag}']
                if s_new is None: c3[tag] = dict(kappa=None, true=None); continue
                r = continue_B(pre, hist, hs, steps=STEPS_B, kappa=k0, kappa_from=(K_DEC, ALPHA*s_new)); c3[tag] = dict(kappa=ALPHA*s_new, true=true_eval(r['theta'], hist, hs), seconds=r['seconds'])
            cd[D] = dict(features=f, c3=dict(secant=ds, **c3))
        cond[cname] = cd
    out['runs'] = runs; out['conditions'] = cond; out['seconds_episode'] = time.time() - t_ep
    out['stored_floats'] = dict(params=int(flat(Net()).numel()), gpm=int(sum(DX*k if i == 0 else H*k for i, k in enumerate(pre['gpm_dims']))),
                                buffer64=int(N_BUF*(DX + 1)), buffer1000=int(1000*(DX + 1)), probes=int(N_PROBE*(DX + 1)), checkpoints=int((len(CHECKS) - 2)*flat(Net()).numel()))
    return out

def jsonable(o):
    if isinstance(o, dict): return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jsonable(v) for v in o]
    if isinstance(o, (np.floating, np.integer)): return o.item()
    if isinstance(o, torch.Tensor): return o.tolist()
    return o

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--seeds', required=True, help='first:count'); ap.add_argument('--out', required=True); ap.add_argument('--workers', type=int, default=3)
    ap.add_argument('--draw_seed', type=int, required=True, help='seed for drawing overlap and maturity per episode')
    a = ap.parse_args(); first, count = map(int, a.seeds.split(':')); rng = np.random.default_rng(a.draw_seed)
    eps = [dict(hseed=first + i, overlap=int(rng.integers(0, 9)), mat=int(rng.choice([300, 3000]))) for i in range(count)]
    outp = pathlib.Path(a.out); done = set()
    if outp.exists(): done = {json.loads(l)['hseed'] for l in outp.read_text().splitlines() if l.strip()}
    todo = [e for e in eps if e['hseed'] not in done]; print(f'{len(todo)} episodes to run ({len(done)} done)', flush=True)
    import multiprocessing as mp
    with mp.get_context('fork').Pool(a.workers) as pool, outp.open('a') as fh:
        for r in pool.imap_unordered(run_episode, todo):
            fh.write(json.dumps(jsonable(r)) + '\n'); fh.flush(); print(r['hseed'], r['overlap'], r['mat'], round(r['seconds_episode'], 1), flush=True)
