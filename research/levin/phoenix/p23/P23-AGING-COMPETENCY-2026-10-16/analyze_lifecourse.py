#!/usr/bin/env python3
"""Lifecourse analyses on levin_checks.py lifecourse output (unrepaired lifetimes).

Organ loss event: the first step t >= 150 at which the organ score (share of its cells typed as organ) falls below
0.6 and stays below for 20 consecutive steps. Organs: left eye, right eye, mouth.

Q1 senescence: discrete-time logistic hazard of organ loss, event ~ age; the age coefficient (per 1,000 steps) with a
   bootstrap 95% CI over lifetimes; also the hazard per age bin and the early (150-700) vs late (700-end) hazard ratio.
Q3 cascade: the same model with the number of other organs already lost as a second covariate.
Q4 early warning: at every 5th step t (t >= 200, t + 100 <= end) at which an organ is not yet lost and its score is
   >= 0.6, label = loss within (t, t + 100]. (Organs never go from fully intact to lost within 50 steps, so the first
   definition had no positives; see REPORT.) Signals over the window [t - 20, t]:
     arc     CRR coherence: Fisher-Rao arc of the organ cells' type distributions (softmax of the type channels)
     var     mean over organ cells of the temporal variance of the organ-type logit
     ac1     lag-1 autocorrelation of the organ's mean organ-type logit (critical slowing down)
     margin  minus the mean margin (organ logit - max other logit) at t (closeness to the tipping point)
     damage  1 - organ score at t (lesion size already present)
   AUC per signal (bootstrap 95% CI over lifetimes), and cross-validated (5 folds by lifetime) AUCs of logistic
   models: BASE = damage + margin; BASE + arc (CRR coherence); BASE + var + ac1 (classic early-warning signals);
   bootstrap CIs of the differences from BASE.

Usage: python3 analyze_lifecourse.py OUT_JSON LC.npz [LC2.npz ...]
"""
import json
import sys

import numpy as np

ORG_SLICES = {"left_eye": slice(0, 10), "right_eye": slice(10, 20), "mouth": slice(20, 42)}
W, H, STEP, START = 20, 100, 5, 200


def load(files):
    st, ty, seeds = [], [], []
    for f in files:
        z = np.load(f)
        st.append(z["organ_states"].astype(np.float32)); seeds += z["seeds"].tolist()
    return np.concatenate(st), seeds


def scores(st):
    typ = st[..., :3].argmax(-1)                                   # life, t, cell
    return {k: (typ[..., s] == 2).mean(-1) for k, s in ORG_SLICES.items()}


def loss_time(score, run=20, start=150):
    below = score < 0.6
    L = len(score)
    for t in range(start, L - run + 1):
        if below[t:t + run].all():
            return t
    return None


def softmax(x):
    z = x - x.max(-1, keepdims=True); e = np.exp(z); return e / e.sum(-1, keepdims=True)


def logit_fit(X, y, iters=50, ridge=1e-6):
    X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X1 @ b)); Wt = p * (1 - p) + 1e-9
        g = X1.T @ (y - p) - ridge * b
        Hm = (X1 * Wt[:, None]).T @ X1 + ridge * np.eye(len(b))
        step = np.linalg.solve(Hm, g); b += step
        if np.abs(step).max() < 1e-8:
            break
    return b


def auc(score, y):
    """Mann-Whitney AUC with average ranks for ties (scipy.stats.rankdata); same value as the original loop, O(n log n)."""
    from scipy.stats import rankdata
    y = np.asarray(y, bool); s = np.asarray(score, float)
    npos, nneg = int(y.sum()), int((~y).sum())
    if npos == 0 or nneg == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y].sum() - npos * (npos + 1) / 2) / (npos * nneg))


def main(out, files):
    st, seeds = load(files)
    nL, L = st.shape[0], st.shape[1]
    sc = scores(st)
    events = {k: [loss_time(sc[k][i]) for i in range(nL)] for k in ORG_SLICES}
    res = {"n_lifetimes": nL, "steps": L, "organ_lost_by_end": {k: int(sum(e is not None for e in v)) for k, v in events.items()}}
    # ---- Q1/Q3: discrete-time hazard rows (life, organ, t) while at risk ----
    rows = []
    for i in range(nL):
        for k in ORG_SLICES:
            et = events[k][i]
            end = et if et is not None else L - 20
            for t in range(150, end + 1):
                if t == et or t % 5 == 0:        # thin the at-risk steps (weight 5) to keep the model small
                    others = sum(1 for kk in ORG_SLICES if kk != k and events[kk][i] is not None and events[kk][i] < t)
                    rows.append((i, k, t, int(t == et), others, 1.0 if t == et else 5.0))
    R = np.array([(r[0], list(ORG_SLICES).index(r[1]), r[2], r[3], r[4], r[5]) for r in rows])
    life, org, age, ev, oth, wt = R[:, 0].astype(int), R[:, 1].astype(int), R[:, 2], R[:, 3], R[:, 4], R[:, 5]

    def hazard_fit(idx, with_others):
        X = [(age[idx] - 150) / 1000.0, (org[idx] == 1).astype(float), (org[idx] == 2).astype(float)]
        if with_others:
            X.append(oth[idx])
        X = np.array(X).T
        # weighted logistic via replication-free weights: expand by weight in the gradient
        y = ev[idx]; w = wt[idx]
        X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
        for _ in range(60):
            p = 1 / (1 + np.exp(-X1 @ b)); Wt = w * p * (1 - p) + 1e-12
            g = X1.T @ (w * (y - p)) - 1e-6 * b
            Hm = (X1 * Wt[:, None]).T @ X1 + 1e-6 * np.eye(len(b))
            stp = np.linalg.solve(Hm, g); b += stp
            if np.abs(stp).max() < 1e-9:
                break
        return b

    rng = np.random.default_rng(0)
    by_life = [np.where(life == i)[0] for i in range(nL)]
    b_age = hazard_fit(np.arange(len(R)), False); b_casc = hazard_fit(np.arange(len(R)), True)
    boots_age, boots_casc = [], []
    for _ in range(500):
        pick = rng.integers(0, nL, nL)
        idx = np.concatenate([by_life[p] for p in pick])
        boots_age.append(hazard_fit(idx, False)[1]); boots_casc.append(hazard_fit(idx, True)[4])
    res["Q1_log_hazard_per_1000_steps"] = {"coef": float(b_age[1]), "ci95": [float(np.percentile(boots_age, 2.5)), float(np.percentile(boots_age, 97.5))]}
    res["Q3_log_hazard_per_other_organ_lost"] = {"coef": float(b_casc[4]), "ci95": [float(np.percentile(boots_casc, 2.5)), float(np.percentile(boots_casc, 97.5))],
                                                 "age_coef_adjusted": float(b_casc[1])}
    bins = [(150, 400), (400, 700), (700, 1000), (1000, 1400), (1400, L)]
    hz = {}
    for lo, hi in bins:
        m = (age >= lo) & (age < hi)
        hz["%d-%d" % (lo, hi)] = {"events": int(ev[m].sum()), "organ_steps_at_risk": float(wt[m].sum()),
                                  "hazard_per_1000": float(1000 * ev[m].sum() / max(wt[m].sum(), 1))}
    res["hazard_by_age_bin"] = hz
    # ---- Q4: early warning ----
    feats, labels, lifes = [], [], []
    for i in range(nL):
        for k, sl in ORG_SLICES.items():
            et = events[k][i]
            x = st[i, :, sl, :]                                        # t, cells, 4
            p = softmax(x[..., :3])
            bc = np.clip(np.sqrt(p[1:] * p[:-1]).sum(-1), 0, 1)
            arc_step = np.sqrt(((2 * np.arccos(bc)) ** 2).sum(-1))     # t-1
            organ_logit = x[..., 2]
            margin = (x[..., 2] - np.maximum(x[..., 0], x[..., 1])).mean(-1)
            for t in range(START, L - H, STEP):
                if et is not None and et <= t:
                    break
                if sc[k][i][t] < 0.6:
                    continue
                win = slice(t - W, t + 1)
                arc = arc_step[t - W:t].sum()
                var = organ_logit[win].var(0).mean()
                m = organ_logit[win].mean(-1); m = m - m.mean()
                ac1 = float((m[1:] * m[:-1]).sum() / max((m * m).sum(), 1e-12))
                feats.append((arc, var, ac1, -margin[t], 1 - sc[k][i][t])); labels.append(int(et is not None and t < et <= t + H)); lifes.append(i)
    F = np.array(feats); y = np.array(labels); lf = np.array(lifes)
    res["Q4_samples"] = int(len(y)); res["Q4_positives"] = int(y.sum())
    names = ["arc", "var", "ac1", "margin", "damage"]
    q4_by_life = [np.where(lf == i)[0] for i in range(nL)]
    aucs = {}
    for j, nme in enumerate(names):
        base = auc(F[:, j], y); bs = []
        for _ in range(500):
            pick = rng.integers(0, nL, nL); idx = np.concatenate([q4_by_life[p] for p in pick])
            bs.append(auc(F[idx, j], y[idx]))
        aucs[nme] = {"auc": base, "ci95": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))]}
    res["Q4_auc"] = aucs
    # cross-validated incremental value over BASE = damage + margin (folds by lifetime)
    Z = (F - F.mean(0)) / (F.std(0) + 1e-12)
    folds = np.arange(nL) % 5
    models = {"base": [4, 3], "base_arc": [4, 3, 0], "base_ews": [4, 3, 1, 2], "arc_only": [0]}
    preds = {m: np.zeros(len(y)) for m in models}
    for f in range(5):
        tr = folds[lf] != f; te = ~tr
        for m, cols in models.items():
            b = logit_fit(Z[tr][:, cols], y[tr])
            preds[m][te] = np.c_[np.ones(te.sum()), Z[te][:, cols]] @ b
    cv = {m: auc(p, y) for m, p in preds.items()}
    diffs = {}
    for m in ("base_arc", "base_ews"):
        bs = []
        for _ in range(500):
            pick = rng.integers(0, nL, nL); idx = np.concatenate([q4_by_life[p] for p in pick])
            bs.append(auc(preds[m][idx], y[idx]) - auc(preds["base"][idx], y[idx]))
        diffs[m + "_minus_base"] = {"diff": cv[m] - cv["base"], "ci95": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))]}
    res["Q4_cv_auc"] = cv; res["Q4_cv_increment"] = diffs
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
