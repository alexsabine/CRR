#!/usr/bin/env python3
"""Divergence between paired runs (same seeds, so identical noise draws): for each pair of arms, per seed and step,
the largest absolute difference in any cell state channel and in any RNN memory value, the share of cells whose
expressed type differs, and the left-eye score. Used for the memory-duration check (PERTURB_* against NONE) and the
history check (LOST_* against NEVER_*).

Usage: python3 analyze_history.py OUT_JSON DIR PREFIX PAIR [PAIR ...] [--T 300] [--tol 0.01]
  PAIR is ARM_X:ARM_Y; files are DIR/PREFIX_ARM.npz written by aging_checks.py --save_states
"""
import argparse
import json
import os

import numpy as np

LEFT_EYE = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("dir"); ap.add_argument("prefix"); ap.add_argument("pairs", nargs="+")
    ap.add_argument("--T", type=int, default=300); ap.add_argument("--tol", type=float, default=0.01)
    a = ap.parse_args()
    res = {}
    load = lambda arm: np.load(os.path.join(a.dir, "%s_%s.npz" % (a.prefix, arm)))
    for pair in a.pairs:
        x, y = pair.split(":")
        zx, zy = load(x), load(y)
        common = sorted(set(zx["seeds"].tolist()) & set(zy["seeds"].tolist()))
        ix = [zx["seeds"].tolist().index(s) for s in common]; iy = [zy["seeds"].tolist().index(s) for s in common]
        T = a.T
        r = {"n": len(common), "T": T}
        if "states" in zx.files and "states" in zy.files:
            sx = zx["states"][ix].astype(np.float32); sy = zy["states"][iy].astype(np.float32)
            mx = zx["memory"][ix].astype(np.float32); my = zy["memory"][iy].astype(np.float32)
            ds = np.abs(sx - sy).max((2, 3, 4)); dm = np.abs(mx - my).max((2, 3, 4))
            L = ds.shape[1]
            # first step after T from which the state difference stays below tol to the end of the run
            conv = []
            for e in range(len(common)):
                above = np.where(ds[e, T + 1:] >= a.tol)[0]
                conv.append(None if len(above) and above[-1] == L - T - 2 else (int(above[-1]) + 2 if len(above) else 1))
            r["state_diff_max_at"] = {str(t): float(ds[:, t].max()) for t in (T - 1, T + 1, T + 10, T + 30, T + 50, T + 100, L - 1) if t < L}
            r["memory_diff_max_at"] = {str(t): float(dm[:, t].max()) for t in (T - 1, T + 1, T + 2, T + 10, T + 30, L - 1) if t < L}
            r["steps_to_converge_below_tol"] = conv
            r["converged_share"] = float(np.mean([c is not None for c in conv]))
            r["median_steps_to_converge"] = float(np.median([c for c in conv if c is not None])) if any(c is not None for c in conv) else None
        tx = zx["types"][ix]; ty = zy["types"][iy]
        dtyp = (tx != ty).mean((2, 3))
        L = dtyp.shape[1]
        r["type_diff_share_at"] = {str(t): float(dtyp[:, t].mean()) for t in (T + 1, T + 10, T + 50, T + 100, L - 1) if t < L}
        lex = (tx[..., LEFT_EYE[:, 1], LEFT_EYE[:, 0]] == 2).mean(-1); ley = (ty[..., LEFT_EYE[:, 1], LEFT_EYE[:, 0]] == 2).mean(-1)
        for t in (T + 10, T + 50, T + 100, L - 1):
            if t < L:
                r["left_eye_regrown_at_%d" % t] = [int((lex[:, t] >= 0.6).sum()), int((ley[:, t] >= 0.6).sum())]
        r["left_eye_mean_score_T1_T100"] = [float(lex[:, T + 1:T + 101].mean()), float(ley[:, T + 1:T + 101].mean())]
        res[pair] = r
        print(pair, json.dumps(r)[:900])
    json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
