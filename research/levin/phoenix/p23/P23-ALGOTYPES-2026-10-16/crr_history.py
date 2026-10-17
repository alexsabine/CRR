#!/usr/bin/env python3
"""CRR-explicit check (Phoenix commitment M7 / ledger PLATONIC-HIST): does a settled form carry its realised history
beyond its visible configuration?

Same visible form, two histories. For each seed: sort a chimeric array to completion (the "settled form"); copy it
three times. HISTORY keeps every cell's internal state as the sorting left it (selection cells' ideal-position pointers).
FRESH has the identical configuration of values and algotypes but cells newly made (pointers at the left boundary),
as if the form had been assembled without that history. LOCAL renews the pointers only of the cells inside the
injured window (memory reset where the cut fell, history kept elsewhere). Apply the identical injury to both (shuffle a contiguous
window of W cells) and let each re-sort, with K continuation seeds per copy. Compare repair swaps, final aggregation
and (with duplicates) final arrangement.

Markov reading (ordinary): history acts only through stored state; HISTORY and FRESH differ iff the stored pointers
change the dynamics. Nothing beyond the full state (configuration + pointers) is needed.

Usage: python3 crr_history.py OUT_JSON --mix BS --n 100 --dup 0 --seeds 100 --window 20 --k 10
"""
import argparse
import json
import os
import random
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim  # noqa: E402


def agg(lab):
    t = np.asarray(lab)
    return float(np.sum(t[:-1] == t[1:]) / len(t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--mix", default="BS"); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--dup", type=int, default=0); ap.add_argument("--seeds", type=int, default=100)
    ap.add_argument("--window", type=int, default=20); ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--max_ticks", type=int, default=2_000_000)
    ap.add_argument("--burst", type=int, default=-1, help="-1 = round-robin (validated); 1 = random activation")
    a = ap.parse_args()
    rows = []
    for e in range(a.seeds):
        v, k, l = sim.setup(a.n, a.mix, a.dup, e)
        r = sim.run(v, k, l, seed=20_000 + e, record=False, burst=a.burst)
        val, kind, lab, ideal = r["state"]
        rng = random.Random(30_000 + e)
        start = rng.randrange(0, a.n - a.window)
        perm = list(range(start, start + a.window)); rng.shuffle(perm)
        idx = list(range(a.n)); idx[start:start + a.window] = perm
        inj = lambda xs: [xs[i] for i in idx]
        pv, pk, pl, pi = inj(val), inj(kind), inj(lab), inj(ideal)
        fresh_ideal = [0] * a.n
        # LOCAL: renew memory only where the cut fell (cells inside the injured window get the fresh pointer)
        local_ideal = [0 if start <= i < start + a.window else pi[i] for i in range(a.n)]
        out = {"seed": e, "window_start": start, "selection_pointers_nonzero": int(sum(1 for i, kk in zip(pi, pk) if kk == sim.S and i > 0))}
        for name, ip in (("history", pi), ("fresh", fresh_ideal), ("local", local_ideal)):
            sw, ag, finals, ok = [], [], [], []
            for c in range(a.k):
                rr = sim.run(None, None, seed=40_000 + 97 * e + c, record=False, start_state=(pv, pk, pl, ip),
                             max_ticks=a.max_ticks, burst=a.burst)
                sw.append(rr["swaps"]); ag.append(agg(rr["final_labels"])); finals.append(tuple(rr["final_labels"]))
                ok.append(rr["sorted"])
            out[name] = {"swaps_mean": float(np.mean(sw)), "agg_mean": float(np.mean(ag)),
                         "sorted_share": float(np.mean(ok)), "distinct_final_arrangements": len(set(finals))}
        rows.append(out)
    d_sw = np.array([r["history"]["swaps_mean"] - r["fresh"]["swaps_mean"] for r in rows])
    d_ag = np.array([r["history"]["agg_mean"] - r["fresh"]["agg_mean"] for r in rows])

    def boot(x):
        rng = np.random.default_rng(0)
        b = [x[rng.integers(0, len(x), len(x))].mean() for _ in range(2000)]
        return [float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))]

    def sign_p(x):
        from math import comb
        pos, neg = int(np.sum(x > 0)), int(np.sum(x < 0)); n = pos + neg
        return 1.0 if n == 0 else min(1.0, 2 * sum(comb(n, i) for i in range(min(pos, neg) + 1)) / 2 ** n)

    summ = {"mix": a.mix, "n": a.n, "dup": a.dup, "seeds": a.seeds, "window": a.window, "k": a.k,
            "repair_swaps_history_mean": float(np.mean([r["history"]["swaps_mean"] for r in rows])),
            "repair_swaps_fresh_mean": float(np.mean([r["fresh"]["swaps_mean"] for r in rows])),
            "repair_swaps_diff_mean": float(d_sw.mean()), "repair_swaps_diff_ci95": boot(d_sw), "repair_swaps_sign_p": sign_p(d_sw),
            "final_agg_history_mean": float(np.mean([r["history"]["agg_mean"] for r in rows])),
            "final_agg_fresh_mean": float(np.mean([r["fresh"]["agg_mean"] for r in rows])),
            "final_agg_diff_mean": float(d_ag.mean()), "final_agg_diff_ci95": boot(d_ag), "final_agg_sign_p": sign_p(d_ag),
            "selection_pointers_nonzero_mean": float(np.mean([r["selection_pointers_nonzero"] for r in rows])),
            "repair_completed_history": float(np.mean([r["history"]["sorted_share"] for r in rows])),
            "repair_completed_fresh": float(np.mean([r["fresh"]["sorted_share"] for r in rows])),
            "seeds_with_any_stuck_history": int(sum(1 for r in rows if r["history"]["sorted_share"] < 1)),
            "seeds_with_any_stuck_fresh": int(sum(1 for r in rows if r["fresh"]["sorted_share"] < 1)),
            "repair_swaps_local_mean": float(np.mean([r["local"]["swaps_mean"] for r in rows])),
            "repair_completed_local": float(np.mean([r["local"]["sorted_share"] for r in rows])),
            "final_agg_local_mean": float(np.mean([r["local"]["agg_mean"] for r in rows])),
            "local_minus_fresh_swaps_sign_p": sign_p(np.array([r["local"]["swaps_mean"] - r["fresh"]["swaps_mean"] for r in rows])),
            "max_ticks": a.max_ticks, "burst": a.burst}
    json.dump({"summary": summ, "rows": rows}, open(a.out, "w"), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
