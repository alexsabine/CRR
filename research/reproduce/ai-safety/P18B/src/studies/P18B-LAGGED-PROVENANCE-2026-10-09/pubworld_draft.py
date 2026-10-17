"""P18B-LAGGED-PROVENANCE draft world, v2 (DESIGN DRAFT helper; NOT FROZEN; development seeds only; no ledger rows).

Why this world exists. In studies/P18-LOOP1-2026-10-08/loopworld.py the published explanation e_t is top2(theta_t), a deterministic
function of theta, so a monitor holding theta but no record of what was published reproduces every provenance statistic
(P18-PROV-FLAME DECLARATION_DRAFT.md section 1.4). Here the published explanation is NOT a function of the current theta: a publisher
with its own random stream decides WHEN to publish and WHICH explanation to publish. Only the record (what was published, and when)
carries that randomness. loopworld.py is imported unchanged; the world generator's call sequence is the same as loopworld.simulate's,
so the deterministic publisher with no telegraph (pub=None, tele=None) reproduces loopworld.simulate array for array.

v2 change (see DESIGN.md section 2.3; v1 output kept as outputs/surrogate_check_v1.json). The v1 surrogate showed that random publication
makes re-entry intermittent, and that a lag statistic with a model-based standard error then alarms just as often with a phantom record:
it detects jumps, not alignment with the record. v2 therefore (a) adds an exogenous telegraph confounder (label-consistent on/off shifts
with their own timing), so that jumpiness alone does not imply re-entry, and (b) makes the record-specific test an exact conditional
randomisation test that redraws the publisher's logged choices and timing (ri_pvalue), keeping the model-based form only as a
secondary detection statistic whose phantom ablation is expected to show that the realised record is not what gives it power.

Publisher (runs after each refit; separate generator; consumes 2 uniforms and one permutation every round, whatever it decides):
  publish now   with probability q (round 0 always publishes); otherwise the previous explanation stays live (delayed, batched release)
  which         with probability lam the deterministic top-2 explanation; otherwise 2 channels drawn uniformly from the top-K of |theta|
  family        K ~ U{3, 4, 5}, lam ~ U(0, 0.75), q ~ U(0.25, 1), drawn per unit (draw_publisher)
  deterministic pub=None: top2(theta_t) every round (the P18-LOOP1 publisher; the record adds nothing)
Nuisance (label-consistent real changes of x_true; drawn per unit from their own generators; neither reads the world generator):
  smooth   the P18-PROV-FLAME drawn confounder (provworld_draft.draw_geometry), present with probability 1/2 (onset tau_x and 10-round ramp
           from the world generator, as in loopworld)
  telegraph present with probability 1/2: support k ~ U{1..8} channels, direction w ~ N(0, I_k) normalised, magnitude log-uniform on
           [0.2, 1.0], per-round switching probability ~ U(0.1, 0.5), start state 0; the whole on/off path is drawn at unit start
Routes (what applicants respond to, from onset tau, on the gameable channel G): 'e' the live published explanation (re-entry through
the recorded output); 'theta' the published classifier (re-entry through a deterministic output); 'open' the fixed direction top2(beta)
(no re-entry); 'none' no gaming.
Probe (the intervention rival): for 6 rounds from div + 2 the monitor overrides publication; route 'e' applicants see top2(theta_{t-1})
with random signs f_e, route 'theta' applicants see theta_{t-1} with random signs f_th; flips from their own generator.

Statistics. a_s is the normalised live explanation after round s (applicants in round s+1 respond to it); eta_s = a_s - E[a_s | a_{s-1},
theta_s] is what neither theta nor the earlier record predicts, v_s its conditional variance under the policy; y_s = xbar_{s+1} - xbar_s.
  detection (per round t, after observing round t's inputs; window s in [t-6, t-1]; alarm at the first t >= 11 above the aligned threshold)
    lag_ri     max_j sum eta c / sqrt(sum v c^2), c the window-centred y (conditional mean 0, variance 1 under no re-entry)  [record]
    lag_mb     max_j regression t of y on eta with the model-based SE sigma/sqrt(Sxx), sigma from rounds 1..10           [record]
    lag_ri_ph, lag_mb_ph   the same with a phantom record (the policy rerun with an independent stream on the same theta path)
    proj_rec   max of the input-mean drift projected on theta_{t-1} and on a_{t-1} (CUSUM; loopworld's prov on the record) [record]
    pf_twin    the lag_mb regression on the change of ahat_t = E[a_t | theta_0..t] (the record-free twin of the lag statistic)
    mobbsd     max of the drift projected on theta_{t-1} and on ahat_{t-1} (CUSUM; record-free multi-output BBSD)
    djump      max_j |second difference of xbar_j| / (sqrt(3) sigma) (CUSUM; record-free jump detector)
    bbsd, inshift, proxy, calib   as in loopworld (record-free)
  attribution at decision round d ("did my published explanation re-enter my inputs?"; window s in [d-10, d-1])
    passive_ri exact conditional randomisation p-value of lag_ri's statistic, B redraws of the publisher inside the window   [record]
    lead_ri    the same with y_{s-1} paired with eta_s (a publication cannot move inputs observed before it): must be null      [record]
    phantom_ri passive_ri computed on a phantom record: must be null                                                         [ablation]
    passive_mb the model-based t at d (threshold calibrated on no-re-entry worlds)                                           [record]
    twin_jump  record-free: max over the policy's pool channels of sum (y - ybar)^2 / sigma^2 (threshold calibrated)
    proj_attr  lag-free: mean drift projected on the live explanation minus on theta (threshold calibrated)                  [record]
    intervention exact randomisation p-value on its own flips of each output (no publication log); its target-accuracy cost

Modes (each under 60 CPU-s; run with nice -n 19 and OMP_NUM_THREADS=1 while another experiment holds the CPU):
  equiv      deterministic publisher, no telegraph: reproduces loopworld.simulate (aligned, game_theta, game_expl, exo, game_expl+exo);
             N1 identities: eta == 0, lag statistics never defined, mobbsd == proj_rec, pf_twin == lag_full; passive_ri == 1
  access     record-free statistics never see the record (twin_view has no record field; swapping the stored record on a fixed trajectory
             leaves them byte-identical; swapping the publisher stream where nobody responds to the explanation leaves the world identical)
  surrogate  stylised surrogate WITHOUT the world (fixed theta, no refits): null behaviour under ramps and telegraph, phantom ablation,
             stylised timely detection, and stylised attribution for passive_ri, phantom_ri, lead_ri and twin_jump. Not evidence
  tiny       code-path check on a handful of development units, including probes and attribution; thresholds from 6 runs mean nothing
  timing     CPU seconds for one unit and one probed simulation
  (the pre-freeze pilot of DESIGN.md section 6.4, and the MP10 check of S-noise and S-stale, are in pilot_p18b.py, which imports this file)

Sensitivity mechanisms S-noise and S-stale (DESIGN.md section 5.5; descriptive arms only; implemented before the pilot per decision D9 /
MP10). DESIGN.md names the mechanisms but not their parameter ranges; the ranges below were fixed by the builder before any pilot data
existed and need the owner's confirmation. Both keep the declared timing (q ~ U(0.25, 1); round 0 always publishes) and replace only the
content rule. pub dicts carry 'kind'; a dict without 'kind' is the declared random-subset publisher, whose code path is unchanged.
  S-noise   kind 'noise': content = the deterministic top-2 support of theta_t with coefficients theta_j * exp(s * z_j), z ~ N(0, I_2);
            s ~ U(0.1, 1.0) per unit (continuous, sign-preserving perturbation of the published coefficients). Stream: 1 uniform and
            2 normals per round, whatever is decided. Moments of the normalised explanation by 9 x 9 Gauss-Hermite quadrature (deterministic);
            the randomisation test redraws z exactly, so its validity does not depend on the quadrature.
  S-stale   kind 'stale': content = top2(theta_{t-L}), L ~ U{0..5} per round, clamped at round 0 (theta_{max(0, t-L)}). Stream: 1 uniform
            and 1 integer per round. Moments are exact (6 equally likely versions).
"""
import sys; sys.dont_write_bytecode = True
import json, hashlib, pathlib, time, itertools, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; DEV = HERE.parent / 'P18-LOOP1-2026-10-08'; FLAME = HERE.parent / 'P18-PROV-FLAME-2026-10-09'
OUT = HERE / 'outputs'
sys.path.insert(0, str(DEV)); sys.path.insert(0, str(FLAME))
import loopworld as L            # noqa: E402  development harness, read only
import provworld_draft as PF     # noqa: E402  only for draw_geometry, the declared smooth-confounder distribution (read only)
D, H, N, WIN = L.D, L.H, L.N, L.WIN
R_LAG, R_LOC, N_MIN, EARLY, W_PRIMARY, B_RI, PROBE_LEN = 6, 10, 3, 5, 5, 999, 6
K_SET, LAM_HI, Q_LO = (3, 4, 5), 0.75, 0.25
TELE_MAG, TELE_SW, P_SMOOTH, P_TELE = (0.2, 1.0), (0.1, 0.5), 0.5, 0.5
POS_PUB = dict(K=3, lam=0.0, q=1.0)
NOISE_S, STALE_LMAX, GH_N = (0.1, 1.0), 5, 9
HELDOUT_BASE = 1_000_000
CUSUM_DET = ['proxy', 'calib', 'inshift', 'bbsd', 'mobbsd', 'proj_rec', 'djump']
SCAN_DET = ['pf_twin', 'lag_mb', 'lag_ri', 'lag_full', 'lag_mb_ph', 'lag_ri_ph']
TWIN_FIELDS = ('Xobs', 'theta', 'score', 'proxy', 'ece')

def sha_int(s, nhex): return int(hashlib.sha256(s.encode()).hexdigest()[:nhex], 16)
def unit_seed(fc, bh, tag, i): return HELDOUT_BASE + sha_int(f'{fc}|{bh}|p18b|{tag}|{i}', 15)
def gen(fc, bh, purpose, tag, i): return np.random.default_rng(sha_int(f'{fc}|{bh}|p18b|{purpose}|{tag}|{i}', 16))
def unit(x): n = np.linalg.norm(x); return x/n if n > 0 else x
def top_idx(theta, k): return np.argsort(-np.abs(theta[:D]))[:k]

def draw_publisher(g): return dict(K=int(g.choice(K_SET)), lam=float(g.uniform(0.0, LAM_HI)), q=float(g.uniform(Q_LO, 1.0)))
def draw_publisher_noise(g): return dict(kind='noise', q=float(g.uniform(Q_LO, 1.0)), s=float(g.uniform(*NOISE_S)))
def draw_publisher_stale(g): return dict(kind='stale', q=float(g.uniform(Q_LO, 1.0)), Lmax=STALE_LMAX)
def pub_kind(pub): return 'det' if pub is None else pub.get('kind', 'subset')

def draw_telegraph(g):
    """exogenous intermittency: label-consistent on/off shift of x_true with its own timing (the whole path is drawn here)"""
    k = int(g.integers(1, D + 1)); sup = np.sort(g.choice(D, k, replace=False)); w = g.normal(0, 1, k); v = np.zeros(D); v[sup] = w/np.linalg.norm(w)
    mag = float(np.exp(g.uniform(*np.log(TELE_MAG)))); p_sw = float(g.uniform(*TELE_SW)); s = 0; path = []
    for _ in range(H): s = 1 - s if g.random() < p_sw else s; path.append(s)
    return dict(k=k, support=[int(j) for j in sup], v=v, mag=mag, p_sw=p_sw, path=np.array(path, float))

def draw_nuisance(g):
    """smooth confounder (PF.draw_geometry) and telegraph, each present with probability 1/2; g is the nuisance generator"""
    smooth = PF.draw_geometry(g) if g.random() < P_SMOOTH else None
    tele = draw_telegraph(g) if g.random() < P_TELE else None
    return smooth, tele

def publish(theta, prev, t, pub, ps):
    """returns (explanation live after round t, whether a publication happened at t)"""
    if pub is None: return L.expl(theta), True
    u_pub, u_det = ps.random(), ps.random(); perm = ps.permutation(pub['K'])
    if t == 0 or u_pub < pub['q']:
        if u_det < pub['lam']: return L.expl(theta), True
        S = top_idx(theta, pub['K'])[perm[:2]]; e = np.zeros(D); e[S] = theta[S]; return e, True
    return prev.copy(), False

def publish_hist(theta_hist, prev, t, pub, ps):
    """publish() for every publisher kind; theta_hist holds theta_0..theta_t. The det and subset kinds call publish() unchanged."""
    kind = pub_kind(pub)
    if kind in ('det', 'subset'): return publish(theta_hist[t], prev, t, pub, ps)
    u_pub = ps.random(); now = t == 0 or u_pub < pub['q']
    if kind == 'noise':
        z = ps.normal(0, 1, 2)
        if now: th = theta_hist[t]; S = top_idx(th, 2); e = np.zeros(D); e[S] = th[S]*np.exp(pub['s']*z); return e, True
        return prev.copy(), False
    if kind == 'stale':
        lag = int(ps.integers(0, pub['Lmax'] + 1))
        if now: return L.expl(theta_hist[max(0, t - lag)]), True
        return prev.copy(), False
    raise ValueError(kind)

_GH = np.polynomial.hermite.hermgauss(GH_N)
GH_Z = np.sqrt(2.0)*np.array([(a, b) for a in _GH[0] for b in _GH[0]]); GH_W = np.array([wa*wb for wa in _GH[1] for wb in _GH[1]])/np.pi

def noise_expl(th, z):
    """normalised S-noise explanations for an array (M, 2) of scaled noise s*z; columns follow top_idx(th, 2), as in publish_hist"""
    S = top_idx(th, 2); E = np.zeros((len(z), D)); E[:, S] = th[S][None, :]*np.exp(z)
    return E/np.linalg.norm(E, axis=1, keepdims=True)

def pub_points(theta_hist, s, pub):
    """support points (M, D) and weights (M,) of the normalised explanation drawn at a publication round s (S-noise, S-stale)"""
    kind = pub_kind(pub)
    if kind == 'stale':
        P = np.array([unit(L.expl(theta_hist[max(0, s - lag)])) for lag in range(pub['Lmax'] + 1)]); return P, np.full(len(P), 1.0/len(P))
    if kind == 'noise': return noise_expl(theta_hist[s], pub['s']*GH_Z), GH_W
    raise ValueError(kind)

def pub_moments_s(theta_hist, s, pub):
    """pub_moments for every kind (det and subset: pub_moments unchanged)"""
    if pub_kind(pub) in ('det', 'subset'): return pub_moments(theta_hist[s], pub)
    P, w = pub_points(theta_hist, s, pub); A = w @ P; return A, np.maximum(w @ P**2 - A**2, 0.0)

def pub_sample(theta_hist, s, pub, rng, B):
    """B redraws of the normalised explanation at a publication round s from the logged policy (S-noise, S-stale)"""
    kind = pub_kind(pub)
    if kind == 'noise': return noise_expl(theta_hist[s], pub['s']*rng.normal(0, 1, (B, 2)))
    if kind == 'stale': P, _ = pub_points(theta_hist, s, pub); return P[rng.integers(len(P), size=B)]
    raise ValueError(kind)

def pool_channels(theta_hist, d, pub):
    """the policy's publishable channels at d (twin_jump's pool)"""
    kind = pub_kind(pub)
    if kind in ('det', 'subset'): return top_idx(theta_hist[d], 2 if pub is None else pub['K'])
    if kind == 'noise': return top_idx(theta_hist[d], 2)
    return np.unique(np.concatenate([top_idx(theta_hist[max(0, d - lag)], 2) for lag in range(pub['Lmax'] + 1)]))

def pub_options(theta, pub):
    """(normalised deterministic explanation, array of normalised random-subset explanations) given theta"""
    det = unit(L.expl(theta)); subs = []
    for a, b in itertools.combinations(top_idx(theta, pub['K']), 2):
        e = np.zeros(D); e[[a, b]] = theta[[a, b]]; subs.append(unit(e))
    return det, np.array(subs)

def pub_moments(theta, pub):
    """mean and variance, per channel, of the normalised explanation drawn at a publication round given theta (policy known)"""
    if pub is None: return unit(L.expl(theta)), np.zeros(D)
    det, subs = pub_options(theta, pub); A = pub['lam']*det + (1 - pub['lam'])*subs.mean(0); E2 = pub['lam']*det**2 + (1 - pub['lam'])*(subs**2).mean(0)
    return A, np.maximum(E2 - A**2, 0.0)

def record_innovations(theta_hist, ell_hist, pub):
    q = 1.0 if pub is None else pub['q']; eta = np.zeros((H, D)); var = np.zeros((H, D)); a_prev = None
    for s in range(H):
        A, V = pub_moments_s(theta_hist, s, pub); a = unit(ell_hist[s])
        if s == 0: m, v = A, V
        else: m = q*A + (1 - q)*a_prev; v = q*V + q*(1 - q)*(A - a_prev)**2
        eta[s] = a - m; var[s] = v; a_prev = a
    return eta, var

def twin_expected(theta_hist, pub):
    q = 1.0 if pub is None else pub['q']; ahat = np.zeros((H, D))
    for s in range(H):
        A, _ = pub_moments_s(theta_hist, s, pub); ahat[s] = A if s == 0 else q*A + (1 - q)*ahat[s - 1]
    return ahat

def diff_sigma(X):
    X = np.asarray(X, float); d = X[..., 2:11, :] - X[..., 1:10, :]; return d.reshape(*d.shape[:-2], -1).std(-1, ddof=1)

def lag_series(X, r, ok, sigma, R=R_LAG, nmin=N_MIN, se='floor', var=None):
    """X (..., H, D); r (..., H, D) regressor at round s acting on round s+1; ok usable rounds; sigma (...,). T[..., t, j] over s in
    [t-R, t-1]. se: 'floor' (model-based, lag_mb), 'selfnorm' (randomisation form, lag_ri; needs var), 'hc3+floor' and 'hc3' (v1 forms,
    kept for the surrogate's disclosure only)."""
    X = np.asarray(X, float); r = np.asarray(r, float); w_all = np.asarray(ok, float)
    y = np.zeros_like(X); y[..., :-1, :] = X[..., 1:, :] - X[..., :-1, :]
    T = np.full(X.shape, np.nan); sig = np.asarray(sigma, float)[..., None]
    with np.errstate(all='ignore'):
        for t in range(11, H):
            sl = slice(t - R, t); w = w_all[..., sl, :]; rr = r[..., sl, :]; yy = y[..., sl, :]; n = w.sum(-2)
            rb = (w*rr).sum(-2)/n; yb = (w*yy).sum(-2)/n; dr = rr - rb[..., None, :]; dy = yy - yb[..., None, :]
            sxx = (w*dr*dr).sum(-2); b = (w*dr*dy).sum(-2)/sxx
            if se == 'selfnorm':
                vv = np.asarray(var, float)[..., sl, :]; tt = (w*rr*dy).sum(-2)/np.sqrt((w*vv*dy*dy).sum(-2))
            else:
                e = dy - b[..., None, :]*dr; hlev = 1/n[..., None, :] + dr*dr/sxx[..., None, :]
                v_hc3 = (w*dr*dr*e*e/np.clip(1 - hlev, 1e-6, None)**2).sum(-2)/sxx**2; v_fl = sig**2/sxx
                v = {'hc3+floor': np.maximum(v_hc3, v_fl), 'floor': v_fl, 'hc3': v_hc3}[se]; tt = b/np.sqrt(v)
            tt = np.where((n >= nmin) & (sxx > 1e-18) & np.isfinite(tt), tt, np.nan); T[..., t, :] = tt
    return T

def chan_max(T): return np.where(np.isnan(T), -np.inf, T).max(-1)
def scan_alarm(S, h): idx = np.flatnonzero(S > h); return int(idx[0]) if len(idx) else None

def ri_pvalue(X, theta_hist, record, pub, d, rng, R=R_LOC, B=B_RI, lead=False):
    """exact conditional randomisation test at decision round d of 'inputs respond to the published explanation'. Statistic
    T = max_j sum_s eta_{s,j} c_{s,j} / sqrt(sum_s v_{s,j} c_{s,j}^2), s in [d-R, d-1], c = window-centred y_s = X_{s+1} - X_s (lead: X_s - X_{s-1}).
    Reference: B redraws of the publisher's choices and timing inside the window from the logged policy, holding theta and the record
    before the window fixed. Valid whatever the response series does, when nobody responds to the explanation. Returns (p, T_obs)."""
    if pub is None: return 1.0, float('nan')
    X = np.asarray(X, float); s0 = d - R; S = range(s0, d); q, lam = pub['q'], pub.get('lam'); subset = pub_kind(pub) == 'subset'
    y = np.array([X[s] - X[s - 1] if lead else X[s + 1] - X[s] for s in S]); c = y - y.mean(0)
    a_prev_obs = unit(record[s0 - 1]); a_prev = np.tile(a_prev_obs, (B, 1)); num_b = np.zeros((B, D)); den_b = np.zeros((B, D)); num = np.zeros(D); den = np.zeros(D)
    for i, s in enumerate(S):
        if subset: det, subs = pub_options(theta_hist[s], pub); A = lam*det + (1 - lam)*subs.mean(0); V = np.maximum(lam*det**2 + (1 - lam)*(subs**2).mean(0) - A**2, 0.0)
        else: A, V = pub_moments_s(theta_hist, s, pub)
        a = unit(record[s]); m = q*A + (1 - q)*a_prev_obs; v = q*V + q*(1 - q)*(A - a_prev_obs)**2; num += (a - m)*c[i]; den += v*c[i]**2; a_prev_obs = a
        pubm = rng.random(B) < q
        if subset: detm = rng.random(B) < lam; k = rng.integers(len(subs), size=B); anew = np.where(detm[:, None], det[None, :], subs[k])
        else: anew = pub_sample(theta_hist, s, pub, rng, B)
        ab = np.where(pubm[:, None], anew, a_prev)
        mb = q*A + (1 - q)*a_prev; vb = q*V + q*(1 - q)*(A - a_prev)**2; num_b += (ab - mb)*c[i]; den_b += vb*c[i]**2; a_prev = ab
    with np.errstate(all='ignore'):
        T = np.where(den > 1e-18, num/np.sqrt(den), -np.inf).max(); Tb = np.where(den_b > 1e-18, num_b/np.sqrt(den_b), -np.inf).max(1)
    if not np.isfinite(T): return 1.0, float('nan')
    return float((1 + np.sum(Tb >= T))/(B + 1)), float(T)

def simulate(seed, route='e', exo=False, geom=None, pub=None, ps=None, probe=None, frng=None, tele=None):
    """one 80-round world. exo with geom=None is the development (designed) smooth confounder; geom from PF.draw_geometry is drawn"""
    rng = np.random.default_rng(seed); beta = rng.normal(0, 1, D); beta /= np.linalg.norm(beta)
    tau = int(rng.integers(20, 36)); G = np.array([int(np.argmax(np.abs(beta)))]); kx = int(rng.choice([j for j in range(D) if j not in G]))
    tau_x = int(rng.integers(15, 40)); rr = np.random.default_rng(seed + 17); rand_dirs = []
    gaming = route in ('e', 'theta', 'open')
    if geom is None: v = np.zeros(D); v[kx] = 1.0; mag = 1.5
    else: v, mag = geom['v'], geom['mag']
    u_open = L.expl(np.append(beta, 0.0))
    hist = dict(Xobs=[], theta=[], ell=[], published=[], score=[], proxy=[], target=[], ece=[], flips=[])
    theta = np.zeros(D + 1); buf = []; ell = None
    for t in range(H):
        xb = rng.normal(0, 1, (N, D)); x_true = xb + (mag*min(1.0, max(0, t - tau_x)/10)*v if exo else 0.0); noise = 0.5*rng.normal(0, 1, N)
        if tele is not None: x_true = x_true + tele['mag']*tele['path'][t]*tele['v']
        x_obs = x_true.copy(); probing = probe is not None and probe[0] <= t < probe[0] + probe[1]
        if probing: f_th = frng.choice([-1.0, 1.0], D); f_e = frng.choice([-1.0, 1.0], D); hist['flips'].append((t, f_th, f_e))
        if gaming and t >= tau and t > 0:
            if route == 'open': u = u_open.copy()
            elif route == 'theta': u = hist['theta'][-1][:D].copy()*(f_th if probing else 1.0)
            else: u = L.expl(hist['theta'][-1])*f_e if probing else hist['ell'][-1].copy()
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
        hist['theta'].append(theta.copy()); ell, did = publish_hist(hist['theta'], ell, t, pub, ps); hist['ell'].append(ell.copy()); hist['published'].append(bool(did))
        r = rr.normal(0, 1, D); r[np.argsort(-np.abs(r))[2:]] = 0; rand_dirs.append(r/np.linalg.norm(r))
    hist['e'] = hist['ell']   # loopworld.stats' 'prov' is then the lag-free projection on theta and on the recorded live explanation
    gap = np.array(hist['proxy']) - np.array(hist['target']); div = next((t for t in range(1, H) if gap[t] >= 0.05), None)
    return dict(hist=hist, div=div, tau=tau, tau_x=tau_x, G=[int(g) for g in G], kx=kx, exo=exo, gaming=gaming, rand_dirs=rand_dirs,
                beta=beta, route=route, pub=pub)

def phantom_record(theta_hist, pub, ps2):
    ell, out = None, []
    for t in range(H): ell, _ = publish_hist(theta_hist, ell, t, pub, ps2); out.append(ell.copy())
    return out

def twin_view(sim):
    """everything a record-free monitor holds: inputs, theta, scores, its proxy metrics and the publisher's policy; no record"""
    return dict({k: sim['hist'][k] for k in TWIN_FIELDS}, pub=sim['pub'])

def twin_stats(view):
    X = np.array(view['Xobs']); th = view['theta']; pub = view['pub']; ref = X[1:11].mean(0); sig = float(diff_sigma(X))
    ahat = twin_expected(th, pub); out = {k: np.full(H, np.nan) for k in ('proxy', 'calib', 'inshift', 'bbsd', 'mobbsd', 'djump')}
    for t in range(1, H):
        dm = X[t] - ref; out['proxy'][t] = -view['proxy'][t]; out['calib'][t] = view['ece'][t]; out['inshift'][t] = float(dm @ dm)
        out['bbsd'][t] = view['score'][t]; out['mobbsd'][t] = float(max(dm @ unit(th[t - 1][:D]), dm @ unit(ahat[t - 1])))
        if t >= 2: out['djump'][t] = float(np.max(np.abs(X[t] - 2*X[t - 1] + X[t - 2])))/(np.sqrt(3)*sig)
    dah = np.zeros((H, D)); dah[1:] = ahat[1:] - ahat[:-1]; ok = np.zeros((H, D), bool); ok[1:] = True
    out['pf_twin_T'] = lag_series(X, dah, ok, sig); out['pf_twin'] = chan_max(out['pf_twin_T']); out['sigma'] = sig; return out

def twin_jump(view, d, R=R_LOC):
    """record-free attribution score at d: max over the policy's pool channels (top-K of theta_d; top-2 if deterministic) of the
    window sum of squared centred first differences over sigma^2. Returns (score, channel)."""
    X = np.array(view['Xobs']); pub = view['pub']; sig = float(diff_sigma(X)); pool = pool_channels(view['theta'], d, pub)
    y = X[d - R + 1:d + 1] - X[d - R:d]; ss = ((y - y.mean(0))**2).sum(0)/sig**2; j = int(pool[np.argmax(ss[pool])]); return float(ss[j]), j

def record_stats(sim, record, pub):
    X = np.array(sim['hist']['Xobs']); th = sim['hist']['theta']; ref = X[1:11].mean(0); sig = float(diff_sigma(X))
    eta, var = record_innovations(th, record, pub); ok = var > 1e-12
    a = np.array([unit(e) for e in record]); da = np.zeros((H, D)); da[1:] = a[1:] - a[:-1]; okf = np.zeros((H, D), bool); okf[1:] = True
    out = dict(lag_mb_T=lag_series(X, eta, ok, sig), lag_ri_T=lag_series(X, eta, ok, sig, se='selfnorm', var=var),
               lag_mb_loc_T=lag_series(X, eta, ok, sig, R=R_LOC), lag_full_T=lag_series(X, da, okf, sig))
    for k in ('lag_mb', 'lag_ri', 'lag_full'): out[k] = chan_max(out[k + '_T'])
    out['proj_rec'] = np.full(H, np.nan)
    for t in range(1, H): dm = X[t] - ref; out['proj_rec'][t] = float(max(dm @ unit(th[t - 1][:D]), dm @ unit(record[t - 1])))
    out['eta_energy'] = (eta**2).sum(-1); return out

def all_stats(sim, phantom_stream=None):
    out = twin_stats(twin_view(sim)); out.update(record_stats(sim, sim['hist']['ell'], sim['pub']))
    if phantom_stream is not None:
        ph_rec = phantom_record(sim['hist']['theta'], sim['pub'], phantom_stream); ph = record_stats(sim, ph_rec, sim['pub'])
        out['lag_mb_ph'] = ph['lag_mb']; out['lag_ri_ph'] = ph['lag_ri']; out['phantom_record'] = ph_rec
    return out

def proj_attr(sim, record, d, R=R_LOC):
    X = np.array(sim['hist']['Xobs']); th = sim['hist']['theta']; ref = X[1:11].mean(0)
    return float(np.mean([(X[s] - ref) @ unit(record[s - 1]) - (X[s] - ref) @ unit(th[s - 1][:D]) for s in range(d - R + 1, d + 1)]))

def attribution(sim, st, d, rng):
    """every localiser's raw score at decision round d (oracle timing: d = div + 10)"""
    X = sim['hist']['Xobs']; th = sim['hist']['theta']; rec = sim['hist']['ell']; pub = sim['pub']; Tm = st['lag_mb_loc_T'][d]
    p, T = ri_pvalue(X, th, rec, pub, d, rng); p_lead, _ = ri_pvalue(X, th, rec, pub, d, rng, lead=True)
    p_ph, _ = ri_pvalue(X, th, st['phantom_record'], pub, d, rng) if 'phantom_record' in st else (float('nan'), None)
    tj, tjc = twin_jump(twin_view(sim), d)
    return dict(d=d, passive_ri_p=p, passive_ri_T=T, lead_ri_p=p_lead, phantom_ri_p=p_ph, passive_mb_t=float(chan_max(Tm)),
                passive_chan=int(np.argmax(np.where(np.isnan(Tm), -np.inf, Tm))), twin_jump=tj, twin_chan=tjc, proj_attr=proj_attr(sim, rec, d))

def intervention_ri(sim, psim, rng, B=B_RI):
    """the intervention rival: exact randomisation p-value of each output's flips, statistic max_j sum r c / sqrt(sum sgn^2 c^2) with
    r = flip * sign of the published coefficient, c = centred level change against the 3 rounds before probing; and its cost"""
    P = np.array(psim['hist']['Xobs']); F = psim['hist']['flips']; ts = np.array([f[0] for f in F]); dX = P[ts] - P[ts[0] - 3:ts[0]].mean(0); c = dX - dX.mean(0); res = {}
    for name, idx in (('theta', 1), ('e', 2)):
        sgn = np.array([np.sign(L.expl(psim['hist']['theta'][t - 1]) if name == 'e' else psim['hist']['theta'][t - 1][:D]) for t in ts])
        den = ((sgn*c)**2).sum(0); f = np.array([fl[idx] for fl in F])
        with np.errstate(all='ignore'):
            T = np.where(den > 1e-18, (f*sgn*c).sum(0)/np.sqrt(den), -np.inf); fb = rng.choice([-1.0, 1.0], (B,) + f.shape)
            Tb = np.where(den > 1e-18, (fb*sgn*c).sum(1)/np.sqrt(den), -np.inf).max(1)
        res[f'p_{name}'] = float((1 + np.sum(Tb >= T.max()))/(B + 1)) if np.isfinite(T.max()) else 1.0; res[f'chan_{name}'] = int(np.argmax(T))
    res['target_cost'] = float(np.nanmean(np.array(sim['hist']['target'])[ts]) - np.nanmean(np.array(psim['hist']['target'])[ts])); return res

def run_unit(seed, route, nuis, pub, ps_seed, ph_seed, thr=None, probe_frng=None, ri_rng=None):
    smooth, tele = nuis
    sim = simulate(seed, route, smooth is not None, smooth, pub, np.random.default_rng(ps_seed), tele=tele); st = all_stats(sim, np.random.default_rng(ph_seed))
    r = dict(seed=seed, route=route, pub=pub, div=sim['div'], tau=sim['tau'], tau_x=sim['tau_x'], G=sim['G'], n_published=int(sum(sim['hist']['published'])),
             smooth=None if smooth is None else dict(k=smooth['k'], mag=round(smooth['mag'], 4)),
             tele=None if tele is None else dict(k=tele['k'], mag=round(tele['mag'], 4), p_sw=round(tele['p_sw'], 3)))
    if thr is not None:
        for k in CUSUM_DET: r['alarm_' + k] = L.first_alarm(L.cusum(st[k]), thr[k])
        for k in SCAN_DET: r['alarm_' + k] = scan_alarm(st[k], thr[k])
    if sim['gaming'] and sim['div'] is not None and sim['div'] + 10 < H:
        r['attr'] = attribution(sim, st, sim['div'] + 10, ri_rng or np.random.default_rng(0))
        if probe_frng is not None:
            ps = simulate(seed, route, smooth is not None, smooth, pub, np.random.default_rng(ps_seed), probe=(sim['div'] + 2, PROBE_LEN), frng=probe_frng, tele=tele)
            r['intervention'] = intervention_ri(sim, ps, ri_rng or np.random.default_rng(0))
    return r, sim, st

def thresholds(cal, far=0.05):
    n = len(cal); thr = {}
    for k in CUSUM_DET: thr[k] = sorted(float(np.max(L.cusum(c[k]))) for c in cal)[int(np.ceil((1 - far)*n)) - 1]
    for k in SCAN_DET: thr[k] = sorted(float(np.max(c[k])) for c in cal)[int(np.ceil((1 - far)*n)) - 1]
    return thr

# ----------------------------------------------------------------------------------------------------------------------------------
def same(a, b): return bool(np.array_equal(np.asarray(a, float), np.asarray(b, float), equal_nan=True))

def mode_equiv():
    rows = equiv_rows(); ok = all(all(v for k, v in r.items() if isinstance(v, bool)) for r in rows)
    out = dict(mode='equiv', version=2, note='development seeds; deterministic publisher (pub=None); no telegraph; designed smooth confounder; no probe', rows=rows, ok=ok)
    json.dump(out, open(OUT / 'equiv_check.json', 'w'), indent=1); print(json.dumps(out, indent=1)); return 0 if ok else 1

def equiv_rows():
    rows = []
    for w, s in (('aligned', 2), ('game_theta', 3), ('game_expl', 3), ('exo', 1), ('game_expl+exo', 0)):
        route = 'e' if 'expl' in w else ('theta' if 'theta' in w else 'none'); exo = w.endswith('exo')
        a = L.simulate(w, s); b = simulate(s, route, exo, None, None, None); ha, hb = a['hist'], b['hist']
        traj = all(same(ha[k], hb[k]) for k in ('Xobs', 'score', 'proxy', 'target', 'ece')) and all(np.array_equal(x, y) for x, y in zip(ha['theta'], hb['theta'])) and a['div'] == b['div']
        sa, sb = L.stats(a), L.stats(b); dev_stats = all(same(sa[k], sb[k]) for k in L.DETECTORS)
        st = all_stats(b, np.random.default_rng(1)); eta, _ = record_innovations(hb['theta'], hb['ell'], None)
        p, _ = ri_pvalue(hb['Xobs'], hb['theta'], hb['ell'], None, 50, np.random.default_rng(2))
        rows.append(dict(world=w, seed=s, trajectory_identical=bool(traj), loopworld_stats_identical=bool(dev_stats), div=b['div'],
                         N1_eta_identically_zero=bool(np.all(eta == 0)), N1_lag_statistics_never_defined=bool(np.all(np.isinf(st['lag_ri'])) and np.all(np.isinf(st['lag_mb']))),
                         N1_proj_rec_equals_loopworld_prov=same(st['proj_rec'][1:], sa['prov'][1:]),
                         N1_mobbsd_equals_proj_rec=bool(np.allclose(st['mobbsd'][1:], st['proj_rec'][1:], rtol=0, atol=1e-12)),
                         N1_pf_twin_equals_lag_full=same(st['pf_twin'], st['lag_full']), N1_passive_ri_p_is_1=bool(p == 1.0)))
    return rows

def mode_access():
    out = access_result(); ok = out['ok']
    json.dump(out, open(OUT / 'access_check.json', 'w'), indent=1, default=float); print(json.dumps(out, indent=1, default=float)); return 0 if ok else 1

def access_result():
    """the MP2 access check as a dict (mode_access writes it; pilot_p18b.py recomputes it in-process)"""
    fc, bh = 'DEVELOPMENT-ONLY', 'NOT-A-BLOCK-HASH'; rows = []; twin_keys = ('proxy', 'calib', 'inshift', 'bbsd', 'mobbsd', 'djump', 'pf_twin', 'pf_twin_T')
    view_keys = sorted(twin_view(simulate(0, 'none', False, None, None, None)).keys())
    static = dict(twin_view_keys=view_keys, record_fields_absent=not ({'ell', 'e', 'published', 'flips'} & set(view_keys)))
    for i, route in enumerate(('e', 'theta', 'open', 'none')):
        seed = 300_000 + i; pub = draw_publisher(gen(fc, bh, 'pubpar', 'access', i)); smooth = PF.draw_geometry(gen(fc, bh, 'geom', 'access', i))
        tele = draw_telegraph(gen(fc, bh, 'tele', 'access', i))
        ps1, ps2, ps3 = (sha_int(f'{fc}|{bh}|p18b|{p}|access|{i}', 16) for p in ('pub', 'pub2', 'phantom'))
        sim = simulate(seed, route, True, smooth, pub, np.random.default_rng(ps1), tele=tele); base = all_stats(sim)
        fake = phantom_record(sim['hist']['theta'], pub, np.random.default_rng(ps3)); sw = all_stats(dict(sim, hist=dict(sim['hist'], ell=fake, e=fake)))
        jt = twin_jump(twin_view(sim), 60) == twin_jump(twin_view(dict(sim, hist=dict(sim['hist'], ell=fake, e=fake))), 60)
        a = dict(route=route, seed=seed, pub=pub, telegraph=dict(k=tele['k'], mag=round(tele['mag'], 3), p_sw=round(tele['p_sw'], 3)),
                 record_swap_on_fixed_trajectory=dict(twin_statistics_identical=all(same(base[k], sw[k]) for k in twin_keys) and bool(jt),
                                                     lag_ri_changed=not same(base['lag_ri_T'], sw['lag_ri_T']), proj_rec_changed=not same(base['proj_rec'], sw['proj_rec'])))
        sim2 = simulate(seed, route, True, smooth, pub, np.random.default_rng(ps2), tele=tele); b2 = all_stats(sim2)
        traj_same = same(sim['hist']['Xobs'], sim2['hist']['Xobs']) and all(np.array_equal(x, y) for x, y in zip(sim['hist']['theta'], sim2['hist']['theta']))
        a['publisher_stream_swap'] = dict(world_trajectory_identical=bool(traj_same), twin_statistics_identical=all(same(base[k], b2[k]) for k in twin_keys),
                                          lag_ri_changed=not same(base['lag_ri_T'], b2['lag_ri_T']), expected_trajectory_identical=route != 'e')
        rows.append(a)
    ok = static['record_fields_absent'] and all(
        r['record_swap_on_fixed_trajectory']['twin_statistics_identical'] and r['record_swap_on_fixed_trajectory']['lag_ri_changed']
        and r['publisher_stream_swap']['world_trajectory_identical'] == r['publisher_stream_swap']['expected_trajectory_identical']
        and (r['route'] == 'e' or r['publisher_stream_swap']['twin_statistics_identical']) for r in rows)
    return dict(mode='access', version=2, note='development seeds 300000-300003; dummy beacon strings; drawn publisher, smooth confounder and telegraph', static=static, rows=rows, ok=bool(ok))

def surrogate_runs(n, g, route, nuisance):
    """stylised: xbar_t = N(0, I/N) + nuisance + route response on G (e: 1.8*ramp*a_{t-1,G}; theta: 1.8*ramp*theta_G/|theta|);
    theta_t = 2*beta + N(0, 0.05^2 I); nuisance 'none', 'drawn' (smooth and telegraph each w.p. 1/2), 'ramp' (smooth always), 'tele' (telegraph always)"""
    runs = []
    for _ in range(n):
        beta = unit(g.normal(0, 1, D)); G = int(np.argmax(np.abs(beta))); pub = draw_publisher(g); ps = np.random.default_rng(g.integers(2**62)); ps2 = np.random.default_rng(g.integers(2**62))
        th = [np.append(2*beta + 0.05*g.normal(0, 1, D), 0.0) for _ in range(H)]; tau = int(g.integers(20, 36)); tau_x = int(g.integers(15, 40))
        smooth, tele = draw_nuisance(g)
        if nuisance == 'none': smooth = tele = None
        elif nuisance == 'ramp': smooth = smooth or PF.draw_geometry(g); tele = None
        elif nuisance == 'tele': smooth = None; tele = tele or draw_telegraph(g)
        X = np.zeros((H, D)); ell, rec = None, []
        for t in range(H):
            x = g.normal(0, 1, D)/np.sqrt(N)
            if smooth is not None: x = x + smooth['mag']*min(1.0, max(0, t - tau_x)/10)*smooth['v']
            if tele is not None: x = x + tele['mag']*tele['path'][t]*tele['v']
            if route != 'none' and t >= tau and t > 0:
                x[G] += 1.8*min(1.0, (t - tau + 1)/8)*(unit(rec[-1])[G] if route == 'e' else unit(th[t - 1][:D])[G])
            X[t] = x; ell, _ = publish(th[t], ell, t, pub, ps); rec.append(ell.copy())
        runs.append(dict(X=X, th=th, rec=rec, ph=phantom_record(th, pub, ps2), pub=pub, tau=tau, G=G, tele=tele is not None))
    return runs

def mode_surrogate(n=400):
    t0 = time.process_time(); g = np.random.default_rng(424_243); rri = np.random.default_rng(7)
    out = dict(mode='surrogate', version=2, n_per_condition=n, B_ri=199,
               note='stylised surrogate without the world (no refits, fixed theta, no applicant heterogeneity); stylised divergence round = tau + 2 (the development median for game_expl); development only; not evidence about the world')
    conds = {k: surrogate_runs(n, g, *k) for k in (('none', 'none'), ('none', 'ramp'), ('none', 'tele'), ('e', 'drawn'), ('theta', 'drawn'), ('none', 'drawn'))}
    def arrays(runs, phantom=False):
        X = np.array([r['X'] for r in runs]); E = np.zeros_like(X); V = np.zeros_like(X)
        for i, r in enumerate(runs): E[i], V[i] = record_innovations(r['th'], r['ph'] if phantom else r['rec'], r['pub'])
        return X, E, V, diff_sigma(X)
    A = {k: arrays(v) for k, v in conds.items()}; Aph = arrays(conds[('e', 'drawn')], phantom=True)
    peak = lambda T: chan_max(T)[:, 11:].max(-1); det = {}
    for se in ('selfnorm', 'floor', 'hc3+floor'):
        T = {k: lag_series(X, E, V > 1e-12, s, se=se, var=V) for k, (X, E, V, s) in A.items()}; h = float(np.quantile(peak(T[('none', 'none')]), 0.95))
        X, E, V, s = Aph; Tph = lag_series(X, E, V > 1e-12, s, se=se, var=V)
        al = [scan_alarm(chan_max(T[('e', 'drawn')])[i], h) for i in range(n)]; div = np.array([r['tau'] + 2 for r in conds[('e', 'drawn')]])
        tim = np.array([a is not None and dv - EARLY <= a <= dv + W_PRIMARY for a, dv in zip(al, div)]); qs = np.array([r['pub']['q'] for r in conds[('e', 'drawn')]])
        det[se] = dict(threshold_null=round(h, 3), alarm_rate_smooth_ramp=round(float(np.mean(peak(T[('none', 'ramp')]) > h)), 4),
                       alarm_rate_telegraph=round(float(np.mean(peak(T[('none', 'tele')]) > h)), 4),
                       alarm_rate_drawn_nuisance_no_gaming=round(float(np.mean(peak(T[('none', 'drawn')]) > h)), 4),
                       alarm_rate_route_theta_drawn=round(float(np.mean(peak(T[('theta', 'drawn')]) > h)), 4),
                       phantom_alarm_rate_under_reentry=round(float(np.mean(peak(Tph) > h)), 4),
                       timely_rate_route_e_drawn=round(float(tim.mean()), 4),
                       timely_by_q_tertile=[round(float(tim[(qs >= lo) & (qs < hi)].mean()), 4) for lo, hi in ((0.25, 0.5), (0.5, 0.75), (0.75, 1.01))],
                       never_alarmed_route_e=round(float(np.mean([a is None for a in al])), 4))
    out['detection_by_statistic'] = det
    # attribution at stylised div + 10 = tau + 12; twin_jump threshold from the no-gaming drawn-nuisance condition
    def tj(r, d):
        pool = top_idx(r['th'][d], r['pub']['K']); X = r['X']; sig = float(diff_sigma(X)); y = X[d - R_LOC + 1:d + 1] - X[d - R_LOC:d]
        return float((((y - y.mean(0))**2).sum(0)/sig**2)[pool].max())
    cal_runs = conds[('none', 'drawn')]; dcal = [int(rri.integers(31, 70)) for _ in cal_runs]; c_tw = float(np.quantile([tj(r, d) for r, d in zip(cal_runs, dcal)], 0.95))
    att = {}
    for key in (('e', 'drawn'), ('theta', 'drawn'), ('none', 'drawn')):
        runs = conds[key]; ds = [min(H - 1, r['tau'] + 12) if key[0] != 'none' else dc for r, dc in zip(runs, dcal)]
        p = np.array([ri_pvalue(r['X'], r['th'], r['rec'], r['pub'], d, rri, B=199)[0] for r, d in zip(runs, ds)])
        pl = np.array([ri_pvalue(r['X'], r['th'], r['rec'], r['pub'], d, rri, B=199, lead=True)[0] for r, d in zip(runs, ds)])
        pp = np.array([ri_pvalue(r['X'], r['th'], r['ph'], r['pub'], d, rri, B=199)[0] for r, d in zip(runs, ds)])
        jt = np.array([tj(r, d) for r, d in zip(runs, ds)]); te = np.array([r['tele'] for r in runs])
        att['_'.join(key)] = dict(passive_ri_yes=round(float(np.mean(p < 0.05)), 4), lead_ri_yes=round(float(np.mean(pl < 0.05)), 4), phantom_ri_yes=round(float(np.mean(pp < 0.05)), 4),
                                  twin_jump_yes=round(float(np.mean(jt > c_tw)), 4), twin_jump_yes_with_telegraph=round(float(np.mean(jt[te] > c_tw)), 4) if te.any() else None,
                                  twin_jump_yes_without_telegraph=round(float(np.mean(jt[~te] > c_tw)), 4) if (~te).any() else None)
    ba = lambda k: round(0.5*(att['e_drawn'][k] + 1 - att['theta_drawn'][k]), 4)
    out['attribution'] = dict(twin_jump_threshold=round(c_tw, 3), by_condition=att, balanced_accuracy_e_vs_theta={k: ba(k) for k in ('passive_ri_yes', 'twin_jump_yes', 'phantom_ri_yes', 'lead_ri_yes')})
    out['cpu_seconds'] = round(time.process_time() - t0, 2)
    json.dump(out, open(OUT / 'surrogate_check.json', 'w'), indent=1); print(json.dumps(out, indent=1)); return 0

def mode_tiny():
    t0 = time.process_time(); fc, bh = 'DEVELOPMENT-ONLY', 'NOT-A-BLOCK-HASH'; cal = []
    for i in range(6):
        pub = draw_publisher(gen(fc, bh, 'pubpar', 'tcal', i)); sm, te = draw_nuisance(gen(fc, bh, 'nuis', 'tcal', i))
        sim = simulate(310_000 + i, 'none', sm is not None, sm, pub, gen(fc, bh, 'pub', 'tcal', i), tele=te); cal.append(all_stats(sim, gen(fc, bh, 'phantom', 'tcal', i)))
    thr = thresholds(cal); rows = []
    plan = [('main', 'e', 'drawn'), ('main', 'e', 'drawn'), ('pos', 'e', 'pos'), ('det', 'e', 'det'), ('theta', 'theta', 'drawn'), ('open', 'open', 'drawn'), ('nogame', 'none', 'drawn')]
    for i, (tag, route, pm) in enumerate(plan):
        nuis = draw_nuisance(gen(fc, bh, 'nuis', 'tiny', i)) if pm != 'pos' else (None, None)
        pub = {'drawn': draw_publisher(gen(fc, bh, 'pubpar', 'tiny', i)), 'pos': POS_PUB, 'det': None}[pm]
        r, sim, st = run_unit(320_000 + i, route, nuis, pub, sha_int(f'{fc}|{bh}|p18b|pub|tiny|{i}', 16), sha_int(f'{fc}|{bh}|p18b|phantom|tiny|{i}', 16), thr,
                              probe_frng=gen(fc, bh, 'flip', 'tiny', i) if route != 'none' else None, ri_rng=gen(fc, bh, 'ri', 'tiny', i))
        r['arm'] = tag; rows.append(r)
    out = dict(mode='tiny', version=2, cpu_seconds=round(time.process_time() - t0, 2), thresholds={k: round(v, 3) for k, v in thr.items()}, rows=rows,
               note='code paths only; 6 calibration runs; development seeds 310000-310005 and 320000-320006; not evidence')
    json.dump(out, open(OUT / 'tiny_check.json', 'w'), indent=1, default=float); print(json.dumps(out, indent=1, default=float)); return 0

def mode_timing():
    fc, bh = 'DEVELOPMENT-ONLY', 'NOT-A-BLOCK-HASH'; pub = draw_publisher(gen(fc, bh, 'pubpar', 'timing', 0)); sm = PF.draw_geometry(gen(fc, bh, 'geom', 'timing', 0))
    te = draw_telegraph(gen(fc, bh, 'tele', 'timing', 0))
    t0 = time.process_time(); sim = simulate(330_000, 'e', True, sm, pub, gen(fc, bh, 'pub', 'timing', 0), tele=te); t1 = time.process_time()
    st = all_stats(sim, gen(fc, bh, 'phantom', 'timing', 0)); t2 = time.process_time()
    d = min(H - 1, (sim['div'] or 40) + 10); attribution(sim, st, d, gen(fc, bh, 'ri', 'timing', 0)); t3 = time.process_time()
    ps = simulate(330_000, 'e', True, sm, pub, gen(fc, bh, 'pub', 'timing', 0), probe=((sim['div'] or 40) + 2, PROBE_LEN), frng=gen(fc, bh, 'flip', 'timing', 0), tele=te); t4 = time.process_time()
    intervention_ri(sim, ps, gen(fc, bh, 'ri', 'timing', 1)); t5 = time.process_time(); L.simulate('game_expl+exo', 0); t6 = time.process_time()
    out = dict(mode='timing', version=2, cpu_s_simulation=round(t1 - t0, 3), cpu_s_statistics_with_phantom=round(t2 - t1, 3), cpu_s_attribution_B999=round(t3 - t2, 3),
               cpu_s_probed_simulation=round(t4 - t3, 3), cpu_s_intervention_ri_B999=round(t5 - t4, 3), cpu_s_loopworld_simulation_same_machine=round(t6 - t5, 3),
               note='one unit each; nice 19, one thread, while another experiment held all 4 cores')
    json.dump(out, open(OUT / 'timing.json', 'w'), indent=1); print(json.dumps(out, indent=1)); return 0

if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    sys.exit({'equiv': mode_equiv, 'access': mode_access, 'surrogate': mode_surrogate, 'tiny': mode_tiny, 'timing': mode_timing}[sys.argv[1]]())
