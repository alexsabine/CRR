#!/usr/bin/env python3
"""Q2b/Q2c (lesion size and position) and Q5 (lesion-size-triggered repair) summaries for P23-AGING-COMPETENCY.

Q2b/Q2c: for competency files with --follow 300 at age 300: eligible if the baseline left eye was >= 0.9 at step 299
and every injured cell was organ-typed in the baseline; eye lost = injured-run eye score < 0.6 at +300 (index 301);
also the uninjured baseline's loss rate at the same step. Wilson 95% intervals.
Q5: per k, late fitness (steps 150-1000), writes, events; paired differences between k values by seed with a 95%
bootstrap CI (10,000 resamples, seed 0).

Usage: python3 analyze_q2b_q5.py OUT_JSON --dose F1 F2 ... --position F1 ... --kthresh F1 ...
"""
import argparse
import json
import os
from math import sqrt

import numpy as np


def wilson(k, n):
    if n == 0:
        return [None, None]
    p = k / n; z = 1.96; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def lesion(f):
    z = np.load(f)
    ok = (z["base_eye"][:, 299] >= 0.9) & (z["base_region"][:, 0] == 2).all(-1)
    inj_lost = (z["inj_eye"][:, 0, 301] < 0.6)[ok]; base_lost = (z["base_eye"][:, 600] < 0.6)[ok]
    rep = (z["region_match"][:, 0, 61] == 1)[ok]
    meta = json.loads(str(z["meta"]))
    return {"injury": meta["injury_cells"], "eligible": int(ok.sum()), "repaired_at_60": int(rep.sum()),
            "eye_lost_at_300_injured": int(inj_lost.sum()), "lost_ci95": wilson(int(inj_lost.sum()), int(ok.sum())),
            "eye_lost_at_300_uninjured": int(base_lost.sum())}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--dose", nargs="*", default=[]); ap.add_argument("--position", nargs="*", default=[])
    ap.add_argument("--kthresh", nargs="*", default=[])
    a = ap.parse_args()
    res = {"Q2b": {}, "Q2c": {}, "Q5": {}}
    for f in a.dose:
        res["Q2b"][os.path.basename(f)[:-4]] = r = lesion(f)
        print("Q2b", os.path.basename(f), r)
    for f in a.position:
        res["Q2c"][os.path.basename(f)[:-4]] = r = lesion(f)
        print("Q2c", os.path.basename(f), r)
    ks = {}
    for f in a.kthresh:
        z = np.load(f); meta = json.loads(str(z["meta"]))
        key = "k%d_noise%s" % (meta["k"], meta["noise"])
        ks[key] = z
        res["Q5"][key] = {"n": len(z["seeds"]), "late": float(z["fitness"][:, 150:].mean()), "final": float(z["fitness"][:, -1].mean()),
                          "writes": float(z["writes"].mean()), "events": float(z["events"].mean())}
        print("Q5", key, res["Q5"][key])
    rng = np.random.default_rng(0)
    for noise in sorted(set(k.split("_noise")[1] for k in ks)):
        for x, y in (("k1", "k3"), ("k1", "k2"), ("k2", "k3"), ("k3", "k5")):
            kx, ky = "%s_noise%s" % (x, noise), "%s_noise%s" % (y, noise)
            if kx in ks and ky in ks:
                d = ks[kx]["fitness"][:, 150:].mean(1) - ks[ky]["fitness"][:, 150:].mean(1)
                b = d[rng.integers(0, len(d), (10000, len(d)))].mean(1)
                lo, hi = float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
                v = "equivalent" if (-2 < lo and hi < 2) else ("different" if (lo > 0 or hi < 0) and abs(d.mean()) >= 2 else "undetermined")
                res["Q5"]["%s-%s_noise%s" % (x, y, noise)] = {"mean_diff": float(d.mean()), "ci95": [lo, hi], "verdict": v}
                print("Q5 %s-%s noise %s: %+.2f [%+.2f, %+.2f] %s" % (x, y, noise, d.mean(), lo, hi, v))
    json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
