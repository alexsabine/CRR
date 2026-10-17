#!/usr/bin/env python3
"""Apply the frozen PREREG.md decision rules to the test outputs (written after the freeze commit 14cbb5c and before
any test seed was run; it implements the rules as written, nothing else).

Q1/Q5: paired mean difference in fitness over steps 150-1000, 95% bootstrap CI (10,000 resamples, seed 0).
  equivalent if CI within +/-margin; different if CI excludes 0 and |mean| >= 2; else undetermined.
Q3(c): exact McNemar on left-eye regrowth at T+50 (LOST_INJ vs NEVER_INJ), paired Wilcoxon on mean eye score T+1..T+100.
Q4: decline (fitness[150] - fitness[1000]) and organs below 0.6 at step 1000, per noise level; Spearman over levels.

Usage: python3 decide.py OUT_JSON TEST_DIR
"""
import json
import os
import sys
from math import comb

import numpy as np
from scipy.stats import spearmanr, wilcoxon

LEFT_EYE = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])
RIGHT_EYE = [15, 0] + LEFT_EYE * [[-1, 1]]
MOUTH = np.concatenate([[[4 + i, 10] for i in range(8)], [[4 + i, 11] for i in range(8)], [[5 + i, 12] for i in range(6)]])


def late(z):
    return z["fitness"][:, 150:].mean(1)


def paired(x, y, margin):
    d = x - y
    rng = np.random.default_rng(0)
    b = d[rng.integers(0, len(d), (10000, len(d)))].mean(1)
    lo, hi = float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
    if -margin < lo and hi < margin:
        verdict = "equivalent"
    elif (lo > 0 or hi < 0) and abs(d.mean()) >= 2:
        verdict = "different"
    else:
        verdict = "undetermined"
    return {"n": len(d), "mean_diff": float(d.mean()), "ci95": [lo, hi], "margin": margin, "verdict": verdict}


def mcnemar_exact(a, b):
    n01 = int(np.sum(a & ~b)); n10 = int(np.sum(~a & b)); n = n01 + n10
    p = 1.0 if n == 0 else min(1.0, 2 * sum(comb(n, i) for i in range(min(n01, n10) + 1)) / 2 ** n)
    return {"x_only": n01, "y_only": n10, "p": p}


def main(out, d):
    L = lambda name: np.load(os.path.join(d, name + ".npz"))
    res = {}
    # Q1 and Q5
    for tag, x, y, m in (("Q1_A", "organ_A_RESET", "organ_A_KEEP", 2), ("Q1_B", "organ_B_RESET", "organ_B_KEEP", 2),
                         ("Q1_B_socket", "socket_B_RESET", "socket_B_KEEP", 2),
                         ("Q1_A_n0125", "n0125_A_RESET", "n0125_A_KEEP", 2), ("Q1_B_n0125", "n0125_B_RESET", "n0125_B_KEEP", 2),
                         ("Q5_B_vs_NONE", "organ_B_RESET", "organ_NONE", 2), ("Q5_A_vs_NONE", "organ_A_RESET", "organ_NONE", 5),
                         ("Q5_MEM_vs_NONE", "organ_MEM_ORGAN", "organ_NONE", 2)):
        if os.path.exists(os.path.join(d, x + ".npz")) and os.path.exists(os.path.join(d, y + ".npz")):
            zx, zy = L(x), L(y)
            assert (zx["seeds"] == zy["seeds"]).all()
            res[tag] = paired(late(zx), late(zy), m)
    # Q3 (c)
    for T, pre in ((300, "hist"), (600, "hist600")):
        try:
            li, ni = L(pre + "_LOST_INJ"), L(pre + "_NEVER_INJ")
        except FileNotFoundError:
            continue
        sc = lambda z: (z["types"][..., LEFT_EYE[:, 1], LEFT_EYE[:, 0]] == 2).mean(-1)
        sl, sn = sc(li), sc(ni)
        rl, rn = sl[:, T + 50] >= 0.6, sn[:, T + 50] >= 0.6
        ml, mn = sl[:, T + 1:T + 101].mean(1), sn[:, T + 1:T + 101].mean(1)
        dd = ml - mn
        res["Q3c_T%d" % T] = {"regrown_T+50": [int(rl.sum()), int(rn.sum())], "n": len(rl),
                              "mcnemar": mcnemar_exact(rl, rn), "mean_score_T1_T100": [float(ml.mean()), float(mn.mean())],
                              "wilcoxon_p": float(wilcoxon(dd).pvalue) if np.any(dd != 0) else 1.0}
        try:
            lo, no = L(pre + "_LOST_NOINJ"), L(pre + "_NEVER_NOINJ")
            res["Q3b_T%d" % T] = {"spontaneous_regrowth_T+50": [int((sc(lo)[:, T + 50] >= 0.6).sum()),
                                                               int((sc(no)[:, T + 50] >= 0.6).sum())], "n": len(rl)}
        except FileNotFoundError:
            pass
    # Q4
    q4 = {}
    xs, ys = [], []
    for lvl in ("0", "0.025", "0.05", "0.075", "0.1", "0.125", "0.15", "0.2"):
        fn = os.path.join(d, "noise_%s_NONE.npz" % lvl)
        if not os.path.exists(fn):
            continue
        z = np.load(fn); f = z["fitness"]; t = z["types"][:, -1]
        decl = f[:, 150] - f[:, 1000]
        lost = sum(((t[:, m[:, 1], m[:, 0]] == 2).mean(-1) < 0.6) for m in (LEFT_EYE, RIGHT_EYE, MOUTH))
        q4[lvl] = {"n": len(f), "decline_mean": float(decl.mean()), "decline_min": float(decl.min()),
                   "decline_max": float(decl.max()), "organs_lost_mean": float(lost.mean()),
                   "fitness_150": float(f[:, 150].mean()), "fitness_1000": float(f[:, 1000].mean())}
        xs += [float(lvl)] * len(decl); ys += decl.tolist()
    if q4:
        rho = spearmanr(xs, ys)
        res["Q4"] = {"levels": q4, "spearman_rho": float(rho.correlation), "spearman_p": float(rho.pvalue)}
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
