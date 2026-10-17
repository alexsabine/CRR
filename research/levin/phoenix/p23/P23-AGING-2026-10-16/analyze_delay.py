#!/usr/bin/env python3
"""Exploratory (after the freeze): LOST_INJ vs NEVER_INJ with the regenerative injection given `delay` steps after
the loss (T = 300). Regrowth (left-eye score >= 0.6) 50 steps after the injection, exact McNemar, and mean eye score
over the 100 steps after injection. Delay 0 is the frozen Q3c run.

Usage: python3 analyze_delay.py OUT_JSON EXPLORE_DIR TEST_DIR
"""
import json
import os
import sys
from math import comb

import numpy as np

LEFT_EYE = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])


def mcnemar(a, b):
    n01, n10 = int(np.sum(a & ~b)), int(np.sum(~a & b)); n = n01 + n10
    return 1.0 if n == 0 else min(1.0, 2 * sum(comb(n, i) for i in range(min(n01, n10) + 1)) / 2 ** n)


def main(out, ed, td):
    T = 300
    res = {}
    for d in (0, 10, 25, 50, 100, 200):
        fl = os.path.join(td, "hist_LOST_INJ.npz") if d == 0 else os.path.join(ed, "delay%d_LOST_INJ.npz" % d)
        fn = os.path.join(td, "hist_NEVER_INJ.npz") if d == 0 else os.path.join(ed, "delay%d_NEVER_INJ.npz" % d)
        if not (os.path.exists(fl) and os.path.exists(fn)):
            continue
        sc = lambda z: (z["types"][..., LEFT_EYE[:, 1], LEFT_EYE[:, 0]] == 2).mean(-1)
        sl, sn = sc(np.load(fl)), sc(np.load(fn))
        ti = T + d
        rl, rn = sl[:, ti + 50] >= 0.6, sn[:, ti + 50] >= 0.6
        same = float(np.mean((np.load(fl)["types"][:, ti] == np.load(fn)["types"][:, ti]).all((1, 2))))
        res[str(d)] = {"n": len(rl), "regrown_50_after_injection": [int(rl.sum()), int(rn.sum())], "mcnemar_p": mcnemar(rl, rn),
                       "mean_score_100_after": [float(sl[:, ti + 1:ti + 101].mean()), float(sn[:, ti + 1:ti + 101].mean())],
                       "share_identical_types_at_injection": same}
        print("delay %3d: regrown LOST %2d / NEVER %2d of %d (p=%.3g); mean score %.3f vs %.3f; identical cell types at injection in %.0f%% of seeds" % (
            d, rl.sum(), rn.sum(), len(rl), res[str(d)]["mcnemar_p"], *res[str(d)]["mean_score_100_after"], 100 * same))
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(*sys.argv[1:4])
