#!/usr/bin/env python3
"""Mechanism behind the HISTORY/FRESH difference in crr_history.py: selection-cell pointers after sorting, after the
injury, and after the repair attempt (same seeds, injury and continuation seed as crr_history.py's first
continuation; round-robin scheduling). Values are unique 0..n-1, so a value's destination is the value itself.

Usage: python3 crr_mechanism.py OUT_JSON --mix BS --seeds 10 --window 20 --max_ticks 400000
"""
import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sim  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--mix", default="BS"); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--seeds", type=int, default=10); ap.add_argument("--window", type=int, default=20)
    ap.add_argument("--max_ticks", type=int, default=400_000)
    a = ap.parse_args()
    n = a.n
    c = {"selection_cells": 0, "pointer_equals_own_position_after_sort": 0, "displaced_selection_after_injury": 0,
         "pointer_at_destination": 0, "pointer_left_of_destination": 0, "pointer_right_of_destination": 0}
    for name in ("history", "fresh"):
        c[name] = {"resorted": 0, "overshot_pointers_at_end": 0, "misplaced_selection_at_end": 0}
    for e in range(a.seeds):
        v, k, l = sim.setup(n, a.mix, 0, e)
        r = sim.run(v, k, l, seed=20_000 + e, record=False, burst=-1)
        val, kind, lab, ideal = r["state"]
        c["selection_cells"] += sum(1 for i in range(n) if kind[i] == sim.S)
        c["pointer_equals_own_position_after_sort"] += sum(1 for i in range(n) if kind[i] == sim.S and ideal[i] == i)
        rng = random.Random(30_000 + e)
        start = rng.randrange(0, n - a.window)
        perm = list(range(start, start + a.window)); rng.shuffle(perm)
        idx = list(range(n)); idx[start:start + a.window] = perm
        pv, pk, pl, pi = [[x[i] for i in idx] for x in (val, kind, lab, ideal)]
        for i in range(n):
            if pk[i] == sim.S and pv[i] != i:
                c["displaced_selection_after_injury"] += 1
                c["pointer_at_destination" if pi[i] == pv[i] else
                  ("pointer_right_of_destination" if pi[i] > pv[i] else "pointer_left_of_destination")] += 1
        for name, ip in (("history", pi), ("fresh", [0] * n)):
            rr = sim.run(None, None, seed=40_000 + 97 * e, record=False, start_state=(pv, pk, pl, ip),
                         max_ticks=a.max_ticks, burst=-1)
            fv, fk, _, fi = rr["state"]
            c[name]["resorted"] += int(rr["sorted"])
            c[name]["overshot_pointers_at_end"] += sum(1 for i in range(n) if fk[i] == sim.S and fv[i] < fi[i] < n)
            c[name]["misplaced_selection_at_end"] += sum(1 for i in range(n) if fk[i] == sim.S and fv[i] != i)
    c.update({"mix": a.mix, "n": n, "seeds": a.seeds, "window": a.window, "max_ticks": a.max_ticks})
    json.dump(c, open(a.out, "w"), indent=1)
    print(json.dumps(c, indent=1))


if __name__ == "__main__":
    main()
