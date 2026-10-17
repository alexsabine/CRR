#!/usr/bin/env python3
"""Where do the algotypes sit inside the final blocks of equal values (duplicate-value runs)?

For each final sorted array, each block of equal values, each cell: relative position within the block
(0 = left end, 1 = right end). Reports the mean relative position per type, the share of blocks that are split into
exactly one run per type (perfect two-run segregation), and the aggregation predicted by an "entry side" model in
which every block is ordered by type alone (all of one type, then all of the other) versus the observed aggregation.

Usage: python3 tie_blocks.py RUN_DIR GROUP [GROUP ...]
"""
import glob
import os
import sys

import numpy as np


def main(run_dir, groups):
    for g in groups:
        rel = {}; two_run = 0; blocks = 0; obs = []; pred = []
        for fn in sorted(glob.glob(os.path.join(run_dir, g + "_exp*.npz"))):
            z = np.load(fn)
            t = z["types"][-1]; v = z["values"][-1]
            n = len(t)
            obs.append(np.sum(t[:-1] == t[1:]) / n)
            # predicted aggregation if each block were ordered by type (keep block composition, sort types inside)
            tt = t.copy()
            i = 0
            while i < n:
                j = i
                while j < n and v[j] == v[i]:
                    j += 1
                blk = t[i:j]
                if j - i > 1:
                    blocks += 1
                    runs = 1 + int(np.sum(blk[:-1] != blk[1:]))
                    two_run += int(runs <= len(set(blk.tolist())))
                    for p, ty in enumerate(blk):
                        rel.setdefault(int(ty), []).append(p / (j - i - 1))
                tt[i:j] = np.sort(blk)
                i = j
            pred.append(np.sum(tt[:-1] == tt[1:]) / n)
        names = {0: "B", 1: "S", 2: "I", 9: "label9"}
        print("%-16s blocks %4d  one-run-per-type %.2f  mean rel. position %s  aggregation observed %.3f vs fully-segregated-blocks %.3f" % (
            g, blocks, two_run / max(1, blocks),
            {names.get(k, k): round(float(np.mean(v)), 3) for k, v in sorted(rel.items())}, np.mean(obs), np.mean(pred)))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
