#!/usr/bin/env python3
"""Computed bottleneck challenges, biology and cognition, 2026-10-05. Frozen core only."""
import json, math
import numpy as np
from crr_instrument import *
rng = np.random.default_rng(11); R = {}

# =====================================================================
# B1  Raz ... Alon 2026 (Nature Aging): damage accumulation with saturating removal; death = first passage to threshold.
# Question: does the core's history variable C (arc of the damage trajectory) predict death beyond the current state X?
# Model (SR class): dX = eta - beta X/(X+kappa) dt + sqrt(2 eps) dW ; death when X >= Xc.
# Test: at a checkpoint age, condition on X in a narrow band; does per-individual accumulated arc C (sum |dX|) predict
# death within the next window? Markov dynamics predict NO. Must-pass control: X itself predicts death.
# =====================================================================
eta, beta, kappa, eps, Xc = 1.0, 1.2, 0.5, 0.6, 4.0   # steady state X* = 2.5; noise reaches Xc = 4
dt, n_ind, t_check, t_win = 0.01, 40000, 12.0, 4.0
X = np.zeros(n_ind); C = np.zeros(n_ind); alive = np.ones(n_ind, bool)
for i in range(int(t_check/dt)):
    dX = (eta - beta*X/(X+kappa))*dt + math.sqrt(2*eps*dt)*rng.normal(size=n_ind)
    X += dX*alive; C += np.abs(dX)*alive; alive &= X < Xc
Xchk, Cchk, alive_chk = X.copy(), C.copy(), alive.copy()
for i in range(int(t_win/dt)):
    dX = (eta - beta*X/(X+kappa))*dt + math.sqrt(2*eps*dt)*rng.normal(size=n_ind)
    X += dX*alive; alive &= X < Xc
died = alive_chk & ~alive
sel = alive_chk
def auc(score, label):
    s, l = score[sel], label[sel]; pos, neg = s[l], s[~l]
    if len(pos) == 0 or len(neg) == 0: return float('nan')
    return float(np.mean(pos[:, None] > neg[None, :]) + 0.5*np.mean(pos[:, None] == neg[None, :]))
auc_X = auc(Xchk, died)
# within a narrow X band, does C predict death?
band = sel & (np.abs(Xchk - np.quantile(Xchk[sel], 0.7)) < 0.1)
pos, neg = Cchk[band & died], Cchk[band & ~died]
auc_C_given_X = float(np.mean(pos[:, None] > neg[None, :])) if len(pos) and len(neg) else float('nan')
R["B1_RazAlon_damage_first_passage"] = {
    "n_alive_at_checkpoint": int(sel.sum()), "deaths_in_window": int(died.sum()),
    "AUC_state_X_predicts_death (must-pass)": auc_X,
    "AUC_arc_C_predicts_death_within_X_band": auc_C_given_X, "n_in_band": int(band.sum()),
    "outcome": ("NO CONTACT. The SR damage model is Markov in X; the paper's death event is already a first passage (of a level "
                "by a non-circular variable, not of arc on a circle). The core's history variable adds nothing once X is known "
                "(AUC near 0.5 within an X band), while X itself predicts death (AUC well above 0.5). The regime question the paper "
                "leaves open (ballistic vs quasi-steady tracking) is about the SR drift, not about path geometry.")}

# =====================================================================
# B3  Nguyen, Etzel, Bezdek, Zacks 2026 (eLife): error- and uncertainty-triggered boundaries leave ~16% of explainable variance.
# CRR candidate: a third trigger type, boundary at first passage of ACCUMULATED change (Fisher arc) since the last boundary,
# which fires under gradual drift that never produces an error spike. Toy: a 2-D observed feature stream with (i) abrupt
# regime jumps and (ii) slow drifts of the same total displacement. Detectors: error-peak (|prediction error| > thr),
# arc threshold (accumulated arc since last boundary > a). Which boundaries each marks.
# No-CRR reduction: an accumulated-change trigger is a CUSUM / cumulative-displacement change detector (prior-art fetch outstanding).
# =====================================================================
T_steps = 6000; mu_t = np.zeros((T_steps, 2)); truth_jump, truth_drift = [], []
cur = np.zeros(2)
for t in range(T_steps):
    if t % 1000 == 700:                     # abrupt jump of size 2
        cur = cur + rng.normal(size=2)/math.sqrt(2)*2; truth_jump.append(t)
    if 100 <= t % 1000 < 300:               # slow drift of total size 2 over 200 steps
        if t % 1000 == 100: d = rng.normal(size=2); d = d/np.linalg.norm(d)*2/200; truth_drift.append(t+200)
        cur = cur + d
    mu_t[t] = cur
obs = mu_t + 0.3*rng.normal(size=mu_t.shape)
# predictor: exponential moving average (the simplest 'event model')
pred = np.zeros_like(obs); m = obs[0].copy(); alpha = 0.1
for t in range(T_steps): pred[t] = m; m = (1-alpha)*m + alpha*obs[t]
err = np.linalg.norm(obs - pred, axis=1)
err_thr = np.quantile(err, 0.995); ev_err = np.flatnonzero(err > err_thr)
ev_err = ev_err[np.concatenate([[True], np.diff(ev_err) > 50])]    # merge bursts
# arc trigger on the smoothed (Gaussian-mean carrier, unit noise -> Euclidean) estimate
# carrier estimate must be smoothed enough that noise path length does not dominate the arc (core: sigma calibration);
# a slower EMA (alpha=0.02) as the carrier; threshold a chosen so that quiet segments do not trigger (a > noise arc per 1000 steps)
m2 = obs[0].copy(); sm = np.zeros_like(obs)
for t in range(T_steps): m2 = 0.98*m2 + 0.02*obs[t]; sm[t] = m2
arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(sm, axis=0), axis=1))])
quiet = slice(300, 700); noise_arc_per_1000 = float((arc[700]-arc[300])*2.5)
a_thr = 1.2; ev_arc = np.array(causal_first_passages(arc, a_thr))
# no-CRR rival: displacement (chord) since the last boundary on the same carrier, same threshold -> CUSUM-type detector
ev_disp = []; last = sm[0]
for t in range(T_steps):
    if np.linalg.norm(sm[t] - last) >= a_thr: ev_disp.append(t); last = sm[t]
ev_disp = np.array(ev_disp)
def hits(ev, truth, tol=60): return int(sum(any(abs(e - tr) <= tol for e in ev) for tr in truth))
def false_alarms(ev, tol=60): return int(sum(all(abs(e - tr) > tol for tr in truth_jump + truth_drift) for e in ev))
R["B3_NguyenZacks_event_triggers"] = {
    "n_true_jumps": len(truth_jump), "n_true_drift_ends": len(truth_drift),
    "noise_arc_per_1000_steps_on_carrier": noise_arc_per_1000, "arc_threshold_a": a_thr,
    "error_trigger": {"n_events": int(len(ev_err)), "jumps_hit": hits(ev_err, truth_jump), "drifts_hit": hits(ev_err, truth_drift), "false_alarms": false_alarms(ev_err)},
    "arc_trigger": {"n_events": int(len(ev_arc)), "jumps_hit": hits(ev_arc, truth_jump), "drifts_hit": hits(ev_arc, truth_drift), "false_alarms": false_alarms(ev_arc)},
    "displacement_trigger_rival": {"n_events": int(len(ev_disp)), "jumps_hit": hits(ev_disp, truth_jump), "drifts_hit": hits(ev_disp, truth_drift), "false_alarms": false_alarms(ev_disp)},
    "outcome": ("REDUCES, with the CRR-specific part WRONG for this purpose. A third trigger type (accumulated change since the "
                "last boundary, as opposed to an error peak) does mark slow-drift boundaries the error trigger misses, so the "
                "idea is live for the paper's residual variance. But the core's version of it, accumulated ARC, is dominated by "
                "noise path length on any real carrier and fires continuously (false alarms above), whereas the standard "
                "displacement-since-last-boundary (chord, CUSUM-type) trigger catches the same boundaries with few false alarms. "
                "What survives is the rival, not the core. A prospective test on OpenNeuro ds005551 would add a displacement "
                "trigger to the paper's model; the core contributes the question, not the detector.")}

# =====================================================================
# B4  Blattner 2026 (bioRxiv): excess-cost functional along an anatomical trajectory + baseline-relative endpoint displacement
#     as hidden regenerative state. Core MATHEMATICAL_OBJECT: S = C - D is exactly collinear with (C, D).
# Demonstration: random regeneration paths; fit death/penetrance outcome on (C, D) and on (C, D, S): identical fit.
# =====================================================================
n = 2000; Cs, Ds = [], []
for _ in range(n):
    steps = rng.normal(0.05, 0.1, 300); p = np.cumsum(steps); Cs.append(np.abs(steps).sum()); Ds.append(abs(p[-1]))
Cs, Ds = np.array(Cs), np.array(Ds); Ss = Cs - Ds
y = 0.3*Cs - 0.5*Ds + rng.normal(0, 0.5, n)
def lstsq_rss(Xm): b, rss, rk, sv = np.linalg.lstsq(Xm, y, rcond=None); return float(((y - Xm@b)**2).sum()), int(rk)
rss2, rk2 = lstsq_rss(np.column_stack([np.ones(n), Cs, Ds])); rss3, rk3 = lstsq_rss(np.column_stack([np.ones(n), Cs, Ds, Ss]))
R["B4_Blattner_excess_cost_identifiability"] = {
    "rss_with_C_D": rss2, "rank_C_D": rk2, "rss_with_C_D_S": rss3, "rank_C_D_S (3 means S is redundant)": rk3,
    "outcome": ("REPHRASE with one transferable constraint. The paper's 'excess cost along the trajectory' and 'baseline-relative "
                "endpoint displacement' are the core's surplus and chord in another vocabulary (independent formulation, not a "
                "CRR influence). The core's identifiability result transfers as a caution: excess cost cannot carry information "
                "beyond (path cost, displacement); a model that uses all three is rank-deficient. Whether hidden regenerative "
                "state is a path quantity at all is the paper's own open prediction and nothing in the core decides it.")}
print(json.dumps(R, indent=1, default=float))
