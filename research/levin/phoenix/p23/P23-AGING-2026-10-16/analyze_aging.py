#!/usr/bin/env python3
"""Summarise aging_checks.py outputs: per arm, lifetime fitness (the authors' cumulative-reward measure: number of
correctly typed cells, max 256), its mean over steps 150-1000 (after the first possible intervention), final
fitness, organ scores (share of organ cells of the organ type) and intervention counts; paired comparisons by seed
(exact Wilcoxon signed-rank via scipy, two-sided) for named contrasts.

Usage: python3 analyze_aging.py OUT_JSON DIR PREFIX [--contrasts A:B,C:D]
"""
import argparse
import glob
import json
import os

import numpy as np
from scipy.stats import wilcoxon

LEFT_EYE = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])
RIGHT_EYE = [15, 0] + LEFT_EYE * [[-1, 1]]
MOUTH = np.concatenate([[[4 + i, 10] for i in range(8)], [[4 + i, 11] for i in range(8)], [[5 + i, 12] for i in range(6)]])


def organ_score(types, mask):
    return (types[..., mask[:, 1], mask[:, 0]] == 2).mean(-1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("dir"); ap.add_argument("prefix")
    ap.add_argument("--contrasts", default="")
    a = ap.parse_args()
    arms = {}
    for fn in sorted(glob.glob(os.path.join(a.dir, a.prefix + "_*.npz"))):
        name = os.path.basename(fn)[len(a.prefix) + 1:-4]
        z = np.load(fn)
        fit = z["fitness"]; types = z["types"]; iv = z["interventions"]
        scores = np.stack([organ_score(types, m) for m in (LEFT_EYE, RIGHT_EYE, MOUTH)], axis=1)  # ep, organ, t
        arms[name] = dict(seeds=z["seeds"].tolist(), fit_mean_late=fit[:, 150:].mean(1), fit_final=fit[:, -1],
                          fit_peak=fit[:, :60].max(1), n_interventions=iv.sum((1, 2)),
                          organs_intact_final=(scores[:, :, -1] >= 0.6).sum(1),
                          share_time_all_intact=(scores[:, :, 150:] >= 0.6).all(1).mean(1),
                          mean_curve=fit.mean(0))
    res = {"arms": {}, "contrasts": {}}
    print("%-12s %3s %9s %9s %9s %7s %8s %9s" % ("arm", "n", "peak", "late", "final", "interv", "organs", "t_intact"))
    for k, v in arms.items():
        r = {m: float(np.mean(v[m])) for m in ("fit_peak", "fit_mean_late", "fit_final", "n_interventions",
                                                 "organs_intact_final", "share_time_all_intact")}
        r["n"] = len(v["seeds"]); r["fit_mean_late_sd"] = float(np.std(v["fit_mean_late"], ddof=1)) if r["n"] > 1 else 0
        r["mean_curve_every_50"] = [round(float(x), 1) for x in v["mean_curve"][::50]]
        res["arms"][k] = r
        print("%-12s %3d %9.1f %9.1f %9.1f %7.1f %8.2f %9.2f" % (k, r["n"], r["fit_peak"], r["fit_mean_late"],
              r["fit_final"], r["n_interventions"], r["organs_intact_final"], r["share_time_all_intact"]))
    for c in [x for x in a.contrasts.split(",") if x]:
        x, y = c.split(":")
        if x not in arms or y not in arms:
            continue
        sx, sy = arms[x]["seeds"], arms[y]["seeds"]
        common = sorted(set(sx) & set(sy))
        ix = [sx.index(s) for s in common]; iy = [sy.index(s) for s in common]
        out = {"n": len(common)}
        for m in ("fit_mean_late", "fit_final", "share_time_all_intact"):
            d = np.asarray(arms[x][m])[ix] - np.asarray(arms[y][m])[iy]
            p = float(wilcoxon(d).pvalue) if np.any(d != 0) else 1.0
            out[m] = {"mean_diff": float(d.mean()), "wins": int((d > 0).sum()), "losses": int((d < 0).sum()), "p": p}
        res["contrasts"][c] = out
        print("%-22s n=%d  late %+6.2f (W/L %d/%d, p=%.3g)  final %+6.2f (p=%.3g)  t_intact %+5.2f (p=%.3g)" % (
            c, out["n"], out["fit_mean_late"]["mean_diff"], out["fit_mean_late"]["wins"], out["fit_mean_late"]["losses"],
            out["fit_mean_late"]["p"], out["fit_final"]["mean_diff"], out["fit_final"]["p"],
            out["share_time_all_intact"]["mean_diff"], out["share_time_all_intact"]["p"]))
    json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
