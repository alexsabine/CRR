"""P14-EMPTY1 world model and the four estimators. Frozen with the study. Pure numpy; every random draw comes from the world's own seed.
World: linear-Gaussian plant x_{t+1} = A x_t + w_t, w ~ N(0, Q); sensor y_t = H x_t + v_t, v ~ N(0, R).
Stale channel: with probability p_stale at each step a stale run begins; for a geometric(1/mean_run) number of steps the sensor re-emits its previous value bit-for-bit (a dropped update, unflagged).
Families (declared): F1 scalar AR(1) a=0.95, F2 position-velocity constant-velocity model, each at two stale rates. Control families: long-stale (positive), real-repeats (quantised low-noise sensor on a slow plant; repeats are genuine evidence), frozen-world (A=I, Q=0)."""
import numpy as np
FAMILIES = {
  'F1a': dict(dim=1, a=0.95, q=1.0, r=1.0, p_stale=0.05, mean_run=8, quant=None, T=1000),
  'F1b': dict(dim=1, a=0.95, q=1.0, r=1.0, p_stale=0.10, mean_run=12, quant=None, T=1000),
  'F2a': dict(dim=2, dt=1.0, q=0.05, r=4.0, p_stale=0.05, mean_run=8, quant=None, T=1000),
  'F2b': dict(dim=2, dt=1.0, q=0.05, r=4.0, p_stale=0.10, mean_run=12, quant=None, T=1000),
  'C_pos_long_stale': dict(dim=1, a=0.98, q=1.0, r=1.0, p_stale=0.10, mean_run=30, quant=None, T=1000),
  'C_neg_real_repeats': dict(dim=1, a=0.99, q=0.05, r=0.5**2/12, p_stale=0.0, mean_run=1, quant=0.5, T=1000),
  'C_neg_frozen_world': dict(dim=1, a=1.0, q=0.0, r=1.0, p_stale=0.15, mean_run=12, quant=None, T=1000),
}
def matrices(f):
    if f['dim'] == 1: A = np.array([[f['a']]]); Q = np.array([[f['q']]]); H = np.array([[1.0]]); R = np.array([[f['r']]])
    else:
        dt = f['dt']; A = np.array([[1.0, dt], [0.0, 1.0]]); Q = f['q']*np.array([[dt**3/3, dt**2/2], [dt**2/2, dt]]); H = np.array([[1.0, 0.0]]); R = np.array([[f['r']]])
    return A, Q, H, R
def generate(family, seed):
    f = FAMILIES[family]; A, Q, H, R = matrices(f); rng = np.random.default_rng(seed); T = f['T']; n = A.shape[0]
    x = np.zeros((T, n)); y = np.zeros(T); stale = np.zeros(T, bool); xt = np.zeros(n); run = 0; y_prev = None
    Lq = np.linalg.cholesky(Q + 1e-12*np.eye(n)) if np.any(Q) else np.zeros((n, n))
    for t in range(T):
        xt = A @ xt + Lq @ rng.standard_normal(n); x[t] = xt
        yt = float((H @ xt)[0]) + float(np.sqrt(R[0, 0]))*float(rng.standard_normal())
        if f['quant']: yt = np.round(yt/f['quant'])*f['quant']
        if run > 0 and y_prev is not None: y[t] = y_prev; stale[t] = True; run -= 1
        else:
            y[t] = yt
            if rng.random() < f['p_stale']: run = int(rng.geometric(1.0/f['mean_run']))
        y_prev = y[t]
    return dict(family=family, seed=seed, x=x, y=y, stale=stale)
def kalman_run(world, arm, gate_p=0.99):
    """arm: EMPTY (repeat -> no update, predict), HOLD (always update), GATED (chi-square innovation gate), FROZEN (repeat -> neither predict nor update)."""
    f = FAMILIES[world['family']]; A, Q, H, R = matrices(f); n = A.shape[0]; x = np.zeros(n); P = 10.0*np.eye(n); y = world['y']; T = len(y)
    from math import erf, sqrt
    gate = 2.5758293035489004 if gate_p == 0.99 else 1.959963984540054
    mean = np.zeros(T); var = np.zeros(T); y_prev = None
    for t in range(T):
        repeat = (y_prev is not None) and (y[t] == y_prev)
        if arm == 'FROZEN' and repeat: pass
        else: x = A @ x; P = A @ P @ A.T + Q
        S = float((H @ P @ H.T + R)[0, 0]); nu = float(y[t] - (H @ x)[0])
        do_update = True
        if arm == 'EMPTY' and repeat: do_update = False
        if arm == 'FROZEN' and repeat: do_update = False
        if arm == 'GATED' and abs(nu)/np.sqrt(S) > gate: do_update = False
        if do_update:
            K = (P @ H.T)/S; x = x + (K*nu).ravel(); P = (np.eye(n) - K @ H) @ P
        mean[t] = float((H @ x)[0]); var[t] = float((H @ P @ H.T)[0, 0]); y_prev = y[t]
    return mean, var
def observed_repeats(y):
    r = np.zeros(len(y), bool); r[1:] = (y[1:] == y[:-1]); return r
def evaluation_mask(y, mode):
    """evaluation set defined from the OBSERVABLE channel only: steps whose reading repeats the previous one bit-for-bit, plus the 5 steps after each such step (mode stale_plus5); stale-only; or all steps"""
    rep = observed_repeats(y); T = len(y)
    if mode == 'all': return np.ones(T, bool)
    if mode == 'stale': return rep
    m = rep.copy()
    for t in range(T):
        if rep[t]: m[t:min(T, t + 6)] = True
    return m
def score(world, mean, var, mode='stale_plus5'):
    """bounded [0,1]: 0.5*(1 - |coverage95 - 0.95|/0.95) + 0.5*(1 - min(1, RMSE/sigma_x)) on the evaluation set."""
    truth = world['x'][:, 0]; m = evaluation_mask(world['y'], mode)
    if m.sum() < 10: return None
    err = truth[m] - mean[m]; sd = np.sqrt(np.maximum(var[m], 1e-12)); cov = float(np.mean(np.abs(err) <= 1.959963984540054*sd))
    sigma_x = float(np.std(truth)) if np.std(truth) > 0 else 1.0; rmse = float(np.sqrt(np.mean(err**2)))
    return 0.5*(1.0 - abs(cov - 0.95)/0.95) + 0.5*(1.0 - min(1.0, rmse/sigma_x))
