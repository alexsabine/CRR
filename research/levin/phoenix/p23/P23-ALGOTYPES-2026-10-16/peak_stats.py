#!/usr/bin/env python3
"""Two readings of "peak aggregation" on the same runs: the maximum of the mean curve (what the official analysis
script plots) and the mean (sd) of each run's own maximum. A per-run maximum of a noisy curve exceeds its mean level
even when nothing aggregates, so only the first is a clustering measure; the paper's negative-control values
(0.57-0.65, sd 0.04-0.05) are compared against both.

Usage: python3 peak_stats.py OUT_JSON RUN_DIR:GROUP [RUN_DIR:GROUP ...]
"""
import glob
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_runs import curve  # noqa: E402


def main(out, specs):
    res = {}
    for spec in specs:
        d, g = spec.rsplit(":", 1)
        C = np.array([curve(np.load(f)["types"]) for f in sorted(glob.glob(os.path.join(d, g + "_exp*.npz")))])
        mx = C.max(1)
        res[g] = {"n": len(C), "max_of_mean_curve": float(C.mean(0).max()),
                  "mean_of_per_run_max": float(mx.mean()), "sd_of_per_run_max": float(mx.std(ddof=1)),
                  "median_pct_of_per_run_max": float(np.median(C.argmax(1)))}
        r = res[g]
        print("%-14s n=%3d  max of mean curve %.3f | per-run max %.3f (sd %.3f), median at %d%%" % (
            g, r["n"], r["max_of_mean_curve"], r["mean_of_per_run_max"], r["sd_of_per_run_max"], r["median_pct_of_per_run_max"]))
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
