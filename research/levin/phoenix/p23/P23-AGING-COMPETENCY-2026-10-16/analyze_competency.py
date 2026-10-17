#!/usr/bin/env python3
"""Competency (repair capacity) by age from levin_checks.py competency output.

Eligible injury: the injured cells all had the intended healthy type in the uninjured baseline at step t-1
(organ type for eye cells, face type for face cells), and, for eye injuries, the baseline left-eye score at t-1 was
>= 0.9. Outcomes at step t + 60 (index 61 of the saved window):
  repaired   every injured cell has the baseline's type again (region_match == 1)
  converged  the whole grid equals the baseline (type_diff == 0)
  spread     the injured run differs from the baseline in more cells than were injured
             (type_diff * 256 > number of injured cells)
Per age: counts with Wilson 95% intervals; trend: young (ages <= 100) vs mature (ages >= 400), Fisher exact test.

Usage: python3 analyze_competency.py OUT_JSON CP.npz [CP2.npz ...]
"""
import json
import os
import sys
from math import comb, sqrt

import numpy as np

LEFT_EYE = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])


def wilson(k, n):
    if n == 0:
        return [None, None]
    p = k / n; z = 1.96; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def fisher_two_sided(a, b, c, d):
    n = a + b + c + d; r1 = a + b; c1 = a + c
    def pr(x): return comb(r1, x) * comb(n - r1, c1 - x) / comb(n, c1)
    p0 = pr(a); lo = max(0, c1 - (n - r1)); hi = min(r1, c1)
    return float(min(1.0, sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p0 + 1e-12)))


def main(out, files):
    res = {}
    for f in files:
        z = np.load(f); meta = json.loads(str(z["meta"]))
        ages = z["ages"].tolist()
        cells = np.array([[int(v) for v in c.split(",")] for c in meta["injury_cells"].split(";")])
        eye_injury = meta.get("injury_state", "face") == "face"
        n_inj = len(cells)
        name = os.path.basename(f)[:-4]
        per_age = {}
        young = [0, 0, 0, 0]; old = [0, 0, 0, 0]       # repaired, n for young; repaired, n for old (indices 0,1 / 2,3)
        for j, t in enumerate(ages):
            rep = conv = spr = n = 0
            for i in range(len(z["seeds"])):
                pre_ok = z["region_match"][i, j, 0] == 1.0            # at t-1 injured and baseline runs are identical
                if "base_region" in z.files:                            # injured cells healthy in the baseline at t-1
                    healthy = 1 if not eye_injury else 2
                    pre_ok = pre_ok and bool((z["base_region"][i, j] == healthy).all())
                base_eye = z["base_eye"][i][t - 1]
                if eye_injury and base_eye < 0.9:
                    continue
                if not pre_ok:
                    continue
                n += 1
                rep += int(z["region_match"][i, j, 61] == 1.0)
                conv += int(z["type_diff"][i, j, 61] == 0.0)
                spr += int(z["type_diff"][i, j, 61] * 256 > n_inj + 1e-9)
            per_age[str(t)] = {"eligible": n, "repaired": rep, "repaired_ci95": wilson(rep, n), "converged": conv,
                               "spread": spr, "spread_ci95": wilson(spr, n)}
            if t <= 100:
                young[0] += rep; young[1] += n
            if t >= 400:
                old[0] += rep; old[1] += n
        p = fisher_two_sided(young[0], young[1] - young[0], old[0], old[1] - old[0]) if young[1] and old[1] else None
        res[name] = {"injury_cells": meta["injury_cells"], "injury_state": meta.get("injury_state", "face"), "noise": meta["noise"],
                     "per_age": per_age, "young_repaired": [young[0], young[1]], "mature_repaired": [old[0], old[1]], "fisher_p": p}
        print("==", name, meta["injury_cells"], meta.get("injury_state", "face"), "noise", meta["noise"])
        for t, r in per_age.items():
            print("  age %5s eligible %3d repaired %3d %s spread %3d converged %3d" % (t, r["eligible"], r["repaired"],
                  r["repaired_ci95"], r["spread"], r["converged"]))
        print("  young (<=100) repaired %d/%d vs mature (>=400) %d/%d, Fisher p = %s" % (young[0], young[1], old[0], old[1], p))
    json.dump(res, open(out, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
