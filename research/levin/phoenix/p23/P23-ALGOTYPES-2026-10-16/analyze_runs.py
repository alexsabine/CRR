#!/usr/bin/env python3
"""Aggregation curves exactly as the official analysis computes them
(cell_research analysis/cell_type_aggregation_analysis.py: get_aggregation_value_avg, get_average_aggregation_array):
per experiment, the snapshot at index int((len-1)*p) for p = 0, 0.01, ..., 1; aggregation = mean over positions of
[type(i) == type(i+1)] with the last position counted as 0; averaged across experiments; the "peak" is the maximum of
the averaged curve. Adds: bootstrap 95% intervals over experiments, the excess over the matched inert-label control,
final value, swaps per run, and the per-experiment time-averaged excess with a Welch test against the control.

Usage: python3 analyze_runs.py RUN_DIR OUT_JSON
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

import numpy as np


def agg(types_row):
    t = np.asarray(types_row)
    return float(np.sum(t[:-1] == t[1:]) / len(t))


def curve(types):
    L = len(types)
    return np.array([agg(types[int((L - 1) * (i / 100))]) for i in range(101)])


def main(run_dir, out):
    groups = defaultdict(list)
    for fn in sorted(glob.glob(os.path.join(run_dir, "*.npz"))):
        m = re.match(r"(.+)_exp\d+\.npz", os.path.basename(fn))
        groups[m.group(1)].append(fn)
    res = {}
    curves = {}
    for g, fns in sorted(groups.items()):
        C, swaps, ok = [], [], []
        for fn in fns:
            z = np.load(fn)
            C.append(curve(z["types"])); swaps.append(len(z["types"]) - 1); ok.append(bool(z["ok"]))
        C = np.array(C)
        mean = C.mean(0)
        rng = np.random.default_rng(0)
        boots = np.array([C[rng.integers(0, len(C), len(C))].mean(0) for _ in range(1000)])
        peak_i = int(mean.argmax())
        curves[g] = C
        res[g] = {"n": len(C), "sorted": int(sum(ok)), "swaps_mean": float(np.mean(swaps)),
                  "initial": float(mean[0]), "final": float(mean[-1]),
                  "peak_of_mean_curve": float(mean[peak_i]), "peak_at_pct": peak_i,
                  "peak_ci95": [float(np.percentile(boots[:, peak_i], 2.5)), float(np.percentile(boots[:, peak_i], 97.5))],
                  "time_avg": float(C.mean()), "mean_curve": [round(x, 4) for x in mean.tolist()]}
    # excess over the matched inert-label control (same values regime)
    for g in res:
        mix, regime = g.split("_", 1)
        ctrl = None
        cands = ("BBB", "SSS", "III") if len(mix) == 3 else ("BB", "SS", "II")
        for c in cands:
            if "%s_%s" % (c, regime) in curves and c != mix:
                ctrl = "%s_%s" % (c, regime); break
        if ctrl is None or len(set(mix)) == 1:
            continue
        a, b = curves[g].mean(1), curves[ctrl].mean(1)
        from math import sqrt
        se = sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
        res[g]["control"] = ctrl
        res[g]["time_avg_excess_over_control"] = float(a.mean() - b.mean())
        res[g]["welch_t"] = float((a.mean() - b.mean()) / se) if se > 0 else None
        res[g]["peak_excess_over_control"] = float(res[g]["peak_of_mean_curve"] - curves[ctrl].mean(0)[res[g]["peak_at_pct"]])
    json.dump(res, open(out, "w"), indent=1)
    print("%-16s %4s %6s %7s %7s %7s %5s %15s %8s %8s" % ("group", "n", "swaps", "init", "final", "peak", "@pct", "peak CI95", "excess", "t"))
    for g, r in res.items():
        print("%-16s %4d %6.0f %7.3f %7.3f %7.3f %5d   [%.3f, %.3f] %8s %8s" % (
            g, r["n"], r["swaps_mean"], r["initial"], r["final"], r["peak_of_mean_curve"], r["peak_at_pct"],
            *r["peak_ci95"], ("%.3f" % r["time_avg_excess_over_control"]) if "control" in r else "-",
            ("%.1f" % r["welch_t"]) if r.get("welch_t") is not None else "-"))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
