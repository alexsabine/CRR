#!/usr/bin/env python3
"""Summarise dg_official.py outputs (files of the same kind are merged).

Per algorithm and frozen-cell count F: DG of the official cells and of the strategy-free null, with the official
statistic (mean and median) and the corrected statistic (mean); the share of runs whose trajectory ends on an error
increase (where the official statistic returns a sum instead of a mean); the paired official-minus-null difference;
the least-squares slope of DG on F with a bootstrap interval, for official and null; and the inversion check (runs in
which any step failed to reduce the inversion count by exactly 1).

Usage: python3 dg_analyze.py OUT_JSON DG_JSON [DG_JSON ...]
"""
import json
import sys
from collections import defaultdict

import numpy as np

PAPER = {"bubble": {0: 0.24, 1: 0.29, 2: 0.32, 3: 0.37}, "insertion": {0: 1.10, 1: 1.13, 2: 1.15, 3: 1.19}}


def boot_ci(x, f=np.mean, B=2000, seed=0):
    rng = np.random.default_rng(seed); x = np.asarray(x, float)
    b = [f(x[rng.integers(0, len(x), len(x))]) for _ in range(B)]
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


def slope(F, y):
    return float(np.polyfit(np.asarray(F, float), np.asarray(y, float), 1)[0])


def slope_ci(F, y, B=2000, seed=0):
    rng = np.random.default_rng(seed); F = np.asarray(F); y = np.asarray(y)
    b = []
    for _ in range(B):
        i = rng.integers(0, len(F), len(F))
        if len(set(F[i].tolist())) > 1:
            b.append(slope(F[i], y[i]))
    return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]


def main(out, files):
    by_kind = defaultdict(dict)
    for fn in files:
        d = json.load(open(fn))
        for F, rows in d["conditions"].items():
            by_kind[d["kind"]].setdefault(F, []).extend(x for x in rows if "dg" in x)
    res = {}
    for kind, conds in by_kind.items():
        r = {"conditions": {}}
        allrows = []
        for F in sorted(conds, key=int):
            rows = conds[F]
            if not rows:
                continue
            g = lambda k: np.array([x[k] for x in rows], float)
            dg, nd = g("dg"), g("null_dg")
            fx = g("dg_fixed") if "dg_fixed" in rows[0] else dg
            nfx = g("null_dg_fixed") if "null_dg_fixed" in rows[0] else nd
            r["conditions"][F] = {
                "n": len(rows), "paper_dg": PAPER.get(kind, {}).get(int(F)),
                "official_stat": {"dg_mean": float(dg.mean()), "dg_ci95": boot_ci(dg), "dg_median": float(np.median(dg)),
                                  "null_mean": float(nd.mean()), "null_ci95": boot_ci(nd), "null_median": float(np.median(nd))},
                "corrected_stat": {"dg_mean": float(fx.mean()), "dg_ci95": boot_ci(fx),
                                   "null_mean": float(nfx.mean()), "null_ci95": boot_ci(nfx),
                                   "diff_mean": float((fx - nfx).mean()), "diff_ci95": boot_ci(fx - nfx)},
                "ends_on_rise_share": float(np.mean([x.get("ends_on_rise", False) for x in rows])),
                "null_ends_on_rise_share": float(np.mean([x.get("null_ends_on_rise", False) for x in rows])),
                "swaps_mean": float(g("swaps").mean()), "null_swaps_mean": float(g("null_swaps").mean()),
                "sorted_share": float(np.mean([x["final_sorted"] for x in rows])),
                "null_sorted_share": float(np.mean([x.get("null_final_sorted", True) for x in rows])),
                "timed_out": int(sum(x["timed_out"] for x in rows)),
                "runs_with_any_step_not_reducing_inversions_by_1": int(sum(1 for x in rows if x["steps_not_minus1_inversion"] > 0)),
                "total_steps": int(g("swaps").sum())}
            allrows += [(int(F), a, b, c, e) for a, b, c, e in zip(dg, nd, fx, nfx)]
        A = np.array(allrows)
        for lab, cap in (("F0to3", 3), ("F0to5", 99)):
            sub = A[A[:, 0] <= cap]
            if len(set(sub[:, 0])) < 2:
                continue
            r["slope_" + lab] = {nm: {"slope": slope(sub[:, 0], sub[:, j]), "ci95": slope_ci(sub[:, 0], sub[:, j])}
                                 for nm, j in (("official_stat_official", 1), ("official_stat_null", 2),
                                               ("corrected_official", 3), ("corrected_null", 4))}
        res[kind] = r
    json.dump(res, open(out, "w"), indent=1)
    for kind, r in res.items():
        print("==", kind)
        print("%2s %4s | %-29s %6s | %-27s %-27s %-19s | %5s %5s | %5s %5s | %3s" % (
            "F", "n", "official stat: mean [CI]", "median", "corrected: official [CI]", "corrected: null [CI]",
            "diff CI", "rise", "nrise", "sort", "nsort", "inv"))
        for F, c in r["conditions"].items():
            o, k = c["official_stat"], c["corrected_stat"]
            print("%2s %4d | %7.3f [%7.3f, %7.3f] %6.3f | %6.3f [%6.3f, %6.3f]    %6.3f [%6.3f, %6.3f]    [%+.3f, %+.3f] | %5.2f %5.2f | %5.2f %5.2f | %3d   paper %s" % (
                F, c["n"], o["dg_mean"], *o["dg_ci95"], o["dg_median"], k["dg_mean"], *k["dg_ci95"], k["null_mean"], *k["null_ci95"],
                *k["diff_ci95"], c["ends_on_rise_share"], c["null_ends_on_rise_share"], c["sorted_share"], c["null_sorted_share"],
                c["runs_with_any_step_not_reducing_inversions_by_1"], c["paper_dg"]))
        for key in ("slope_F0to3", "slope_F0to5"):
            if key in r:
                print(key, {nm: "%+.4f [%+.4f, %+.4f]" % (v["slope"], *v["ci95"]) for nm, v in r[key].items()})


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
