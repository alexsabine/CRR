#!/usr/bin/env python3
"""Batch runs of sim.py in the same file format as run_official.py (same seeds give the same initial arrays).

Usage: python3 run_sim.py OUT_DIR --mix BS --n 100 --exps 100 [--dup 10] [--rates 1,1,1] [--tag name]
  --rates: activation rates for B,S,I (speed null). --tag: suffix in the group name.
"""
import argparse
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--mix", default="BS"); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--exps", type=int, default=100); ap.add_argument("--dup", type=int, default=0)
    ap.add_argument("--rates", default=""); ap.add_argument("--tag", default=""); ap.add_argument("--seed0", type=int, default=0)
    ap.add_argument("--label_rates", default="", help="speed null: per-LABEL rates for an inert mix, e.g. '0:1,9:3'")
    ap.add_argument("--burst", type=int, default=1, help="-1 = round-robin (validated against the official code)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rates = [float(x) for x in a.rates.split(",")] if a.rates else None
    regime = ("dup%d" % a.dup if a.dup else "uniq") + ("-n%d" % a.n if a.n != 100 else "") + (("-" + a.tag) if a.tag else "")
    t0 = time.time()
    for e in range(a.seed0, a.seed0 + a.exps):
        fn = os.path.join(a.out, "%s_%s_exp%04d.npz" % (a.mix, regime, e))
        if os.path.exists(fn):
            continue
        v, k, l = sim.setup(a.n, a.mix, a.dup, e)
        r = sim.run(v, k, l, seed=10_000 + e, rates=rates, label_rates=a.label_rates or None, burst=a.burst)
        np.savez_compressed(fn, types=r["types"], values=r["values"], ok=r["sorted"], seconds=0.0)
    print("%s %s %d runs %.1fs" % (a.mix, regime, a.exps, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
