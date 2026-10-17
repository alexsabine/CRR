#!/usr/bin/env python3
"""Summarise crr_repair.py outputs: per arm, mean fitness over steps 150-1000 (late), final fitness, organs intact at
the end, share of time all organs are intact, cell writes and write events (cost), CRR cuts after step 150; paired
contrasts by seed with the frozen rule (95% bootstrap CI of the mean difference, 10,000 resamples, seed 0;
equivalent if inside +/-margin, different if it excludes 0 and |mean| >= 2, else undetermined).

Usage: python3 analyze_crr.py OUT_JSON DIR [--contrasts X:Y,...] [--margin 2]
"""
import argparse
import glob
import json
import os

import numpy as np

LEFT_EYE = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])
RIGHT_EYE = [15, 0] + LEFT_EYE * [[-1, 1]]
MOUTH = np.concatenate([[[4 + i, 10] for i in range(8)], [[4 + i, 11] for i in range(8)], [[5 + i, 12] for i in range(6)]])


def paired(d, margin):
    rng = np.random.default_rng(0)
    b = d[rng.integers(0, len(d), (10000, len(d)))].mean(1)
    lo, hi = float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))
    v = "equivalent" if (-margin < lo and hi < margin) else ("different" if (lo > 0 or hi < 0) and abs(d.mean()) >= 2 else "undetermined")
    return {"n": len(d), "mean_diff": float(d.mean()), "ci95": [lo, hi], "wins": int((d > 0).sum()), "losses": int((d < 0).sum()), "verdict": v}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("dir"); ap.add_argument("--contrasts", default=""); ap.add_argument("--margin", type=float, default=2.0)
    a = ap.parse_args()
    arms = {}
    for fn in sorted(glob.glob(os.path.join(a.dir, "*.npz"))):
        k = os.path.basename(fn)[:-4]
        z = np.load(fn)
        f = z["fitness"]; t = z["types"]
        sc = np.stack([(t[..., m[:, 1], m[:, 0]] == 2).mean(-1) for m in (LEFT_EYE, np.asarray(RIGHT_EYE), MOUTH)], 1)
        arms[k] = dict(seeds=z["seeds"].tolist(), late=f[:, 150:].mean(1), final=f[:, -1],
                       intact_end=(sc[:, :, -1] >= 0.6).sum(1), t_all_intact=(sc[:, :, 150:] >= 0.6).all(1).mean(1),
                       writes=z["writes"].sum(1), events=z["write_events"].sum(1), cuts=z["cuts"].sum(1))
    res = {"arms": {}, "contrasts": {}}
    print("%-16s %3s %7s %7s %6s %6s %8s %7s %6s" % ("arm", "n", "late", "final", "intact", "t_all", "writes", "events", "cuts"))
    for k, v in arms.items():
        r = {m: float(np.mean(v[m])) for m in ("late", "final", "intact_end", "t_all_intact", "writes", "events", "cuts")}
        r["n"] = len(v["seeds"]); res["arms"][k] = r
        print("%-16s %3d %7.1f %7.1f %6.2f %6.2f %8.1f %7.1f %6.1f" % (k, r["n"], r["late"], r["final"], r["intact_end"],
              r["t_all_intact"], r["writes"], r["events"], r["cuts"]))
    for c in [x for x in a.contrasts.split(",") if x]:
        x, y = c.split(":")
        if x not in arms or y not in arms:
            continue
        assert arms[x]["seeds"] == arms[y]["seeds"], c
        out = paired(np.asarray(arms[x]["late"]) - np.asarray(arms[y]["late"]), a.margin)
        out["writes_diff"] = float(np.mean(arms[x]["writes"]) - np.mean(arms[y]["writes"]))
        res["contrasts"][c] = out
        print("%-28s late %+6.2f [%+.2f, %+.2f] W/L %d/%d -> %s; writes %+.1f" % (c, out["mean_diff"], *out["ci95"],
              out["wins"], out["losses"], out["verdict"], out["writes_diff"]))
    json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
