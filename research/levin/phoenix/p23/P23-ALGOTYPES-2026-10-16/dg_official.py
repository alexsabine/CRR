#!/usr/bin/env python3
"""Delayed Gratification (DG) with the OFFICIAL code (cell_research 1fd2bd59, unchanged), plus two ordinary checks.

Set-up as the official `multithread_cell_sorting_with_frozen_steps.py`: values 0..99 shuffled, one group, F cells set
to FREEZE by random.randint (threads of frozen cells not started), run until no cell should move (or timeout).
DG is computed with the official functions get_monotonicity / dedup / get_discrepency_arr / get_first_pos /
avg_wandering_range / get_max_delay_gratification, extracted verbatim (ast) from
analysis/delay_gratification_analysis.py, applied to the per-swap value snapshots (status_probe.sorting_steps).

Checks added here:
  inversions  Kendall distance to the sorted array after every swap. Every swap the official bubble and insertion
              cells make (including passive moves of a frozen cell) exchanges an adjacent out-of-order pair, so
              inversions should fall by exactly 1 at every step: the process never moves away from the goal in the
              goal's own distance. The script counts steps where inversions do not fall by 1.
  null        a strategy-free sorter: at each step swap one adjacent out-of-order pair chosen uniformly at random
              among those a non-frozen cell could initiate under the same frozen rule (frozen cells never initiate,
              can be moved by a neighbour), stopped by the official rule (no non-frozen cell "should move").
  dg_fixed    the official statistic with one correction: avg_wandering_range returns the running SUM instead of
              the mean when a trajectory ends on an error increase (only runs that stop unsorted can); the
              corrected copy returns the mean on every exit. Both values are recorded.

Usage: python3 dg_official.py OFFICIAL_DIR OUT_JSON --kind bubble --frozen 0,1,2,3 --exps 100 --timeout 120
"""
import argparse
import ast
import json
import os
import random
import sys
import threading
import time


def load_official_dg(official):
    src = open(os.path.join(official, "analysis", "delay_gratification_analysis.py")).read()
    tree = ast.parse(src)
    keep = {"get_monotonicity", "dedup", "get_discrepency_arr", "get_first_pos", "avg_wandering_range",
            "get_max_delay_gratification"}
    mod = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in keep], type_ignores=[])
    ns = {}
    exec(compile(mod, "official_dg", "exec"), ns)
    ns["print"] = lambda *a, **k: None          # avg_wandering_range prints negative segments; silence only
    # corrected copy: the official avg_wandering_range returns the running SUM (not the mean) when the trajectory ends
    # on an error increase (its early `return res`); here every exit returns the mean. Nothing else is changed.
    fx = ast.parse(src)
    for node in ast.walk(fx):
        if isinstance(node, ast.FunctionDef) and node.name == "avg_wandering_range":
            for sub in ast.walk(node):
                if isinstance(sub, ast.If) and sub.body and isinstance(sub.body[0], ast.Return) \
                        and isinstance(sub.body[0].value, ast.Name) and sub.body[0].value.id == "res":
                    sub.body[0].value = ast.parse("(res / n if n else 0)", mode="eval").body
            node.name = "avg_wandering_range_fixed"
            fixed = ast.Module(body=[node], type_ignores=[])
            ast.fix_missing_locations(fixed)
            exec(compile(fixed, "official_dg_fixed", "exec"), ns)
    return ns


def dg_both(dg, steps):
    """(official DG, corrected DG, trajectory ends on an error increase, number of rise/fall episodes)."""
    if not steps:
        return 0.0, 0.0, False, 0
    mono = [dg["get_monotonicity"](s) for s in steps if len(s) > 0]
    d = dg["get_discrepency_arr"](mono)
    return (float(dg["avg_wandering_range"](mono)), float(dg["avg_wandering_range_fixed"](mono)),
            bool(d and d[-1] > 0), int(sum(1 for x in d if x > 0)))


def inversions(a):
    n = len(a); c = 0
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            c += ai > a[j]
    return c


def null_sort(values, frozen_idx, kind, rng, stop_official=True):
    """Strategy-free sorter under the official frozen rule. Returns list of snapshots after each swap."""
    a = list(values); frz = [False] * len(a)
    for i in frozen_idx:
        frz[i] = True
    snaps = []
    n = len(a)

    def any_should_move():
        # official should_move: an out-of-order neighbour counts only if BOTH cells are non-frozen (ACTIVE);
        # insertion additionally needs its left part (frozen cells reset the check) to be in order
        for p in range(n - 1):
            if a[p] > a[p + 1] and not frz[p] and not frz[p + 1]:
                if kind != "insertion" or enabled(p + 1):
                    return True
        return False

    def enabled(q):
        prev = -1
        for i in range(0, q):
            if frz[i]:
                prev = -1; continue
            if a[i] < prev:
                return False
            prev = a[i]
        return True

    while True:
        if stop_official and not any_should_move():
            return snaps
        cand = []
        for p in range(n - 1):
            if a[p] > a[p + 1] and (not frz[p] or not frz[p + 1]):
                if kind == "insertion":
                    # insertion: the right cell initiates, only if non-frozen and its left part (frozen reset) is sorted
                    if frz[p + 1]:
                        continue
                    ok = True; prev = -1
                    for i in range(0, p + 1):
                        if frz[i]:
                            prev = -1; continue
                        if a[i] < prev:
                            ok = False; break
                        prev = a[i]
                    if not ok:
                        continue
                cand.append(p)
        if not cand:
            return snaps
        p = cand[rng.randrange(len(cand))]
        a[p], a[p + 1] = a[p + 1], a[p]; frz[p], frz[p + 1] = frz[p + 1], frz[p]
        snaps.append(list(a))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("official"); ap.add_argument("out"); ap.add_argument("--kind", default="bubble")
    ap.add_argument("--frozen", default="0,1,2,3"); ap.add_argument("--exps", type=int, default=100)
    ap.add_argument("--timeout", type=float, default=120); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--null_only", action="store_true")
    a = ap.parse_args()
    off = os.path.abspath(a.official)
    sys.path.insert(0, off)
    dg = load_official_dg(off)
    from modules.multithread.BubbleSortCell import BubbleSortCell
    from modules.multithread.InsertionSortCell import InsertionSortCell
    from modules.multithread.CellGroup import CellGroup, GroupStatus
    from modules.multithread.MultiThreadCell import CellStatus
    from modules.multithread.StatusProbe import StatusProbe
    CLS = {"bubble": BubbleSortCell, "insertion": InsertionSortCell}
    res = {"kind": a.kind, "n": a.n, "exps": a.exps, "conditions": {}}
    if os.path.exists(a.out):
        res = json.load(open(a.out))
    for F in [int(x) for x in a.frozen.split(",")]:
        key = str(F)
        rows = res["conditions"].get(key, [])
        for e in range(len(rows), a.exps):
            rng = random.Random(1000 * F + e)
            values = list(range(a.n)); rng.shuffle(values)
            frozen_idx = [rng.randint(0, a.n - 1) for _ in range(F)]     # as official: may repeat
            row = {"seed": e, "frozen_idx": frozen_idx}
            if not a.null_only:
                random.seed(1000 * F + e)
                lock = threading.Lock(); probe = StatusProbe(); cells = []
                lb, rb = (0, 1), (a.n - 1, 1)
                for i in range(a.n):
                    cells.append(CLS[a.kind](i + 1, values[i], lock, (i, 1), cells, lb, rb, probe, disable_visualization=True))
                g = CellGroup(cells, cells, 0, lb, rb, GroupStatus.ACTIVE, lock, 10 ** 9, 10 ** 9)
                for c in cells:
                    c.group = g
                for i in frozen_idx:
                    cells[i].set_cell_to_freeze()
                lock.acquire()
                started = [c for c in cells if c.status != CellStatus.FREEZE]
                for c in started:
                    c.start()
                g.start(); lock.release()
                t0 = time.time(); timed_out = False
                while True:
                    lock.acquire()
                    idle = all(not (c.status == CellStatus.SLEEP or (c.status == CellStatus.ACTIVE and c.should_move())) for c in cells)
                    lock.release()
                    if idle:
                        break
                    if time.time() - t0 > a.timeout:
                        timed_out = True; break
                    time.sleep(0.01)
                lock.acquire()
                for c in cells:
                    c.status = CellStatus.INACTIVE
                g.status = GroupStatus.MERGED; lock.release()
                for c in started:
                    c.join(timeout=5)
                g.join(timeout=5)
                steps = probe.sorting_steps
                inv = [inversions(values)]
                for s in steps:
                    inv.append(inversions(s))
                d = [inv[i + 1] - inv[i] for i in range(len(inv) - 1)]
                row.update({"swaps": len(steps), "timed_out": timed_out, "seconds": round(time.time() - t0, 1),
                            "dg": float(dg["get_max_delay_gratification"](steps)),
                            "dg_fixed": dg_both(dg, steps)[1], "ends_on_rise": dg_both(dg, steps)[2],
                            "episodes": dg_both(dg, steps)[3],
                            "steps_not_minus1_inversion": int(sum(1 for x in d if x != -1)),
                            "final_inversions": inv[-1],
                            "final_sorted": all(steps[-1][i] <= steps[-1][i + 1] for i in range(a.n - 1)) if steps else False})
            ns = null_sort(values, sorted(set(frozen_idx)), a.kind, random.Random(70_000 + 1000 * F + e))
            row["null_swaps"] = len(ns)
            row["null_dg"] = float(dg["get_max_delay_gratification"](ns))
            nb = dg_both(dg, ns)
            row["null_dg_fixed"], row["null_ends_on_rise"], row["null_episodes"] = nb[1], nb[2], nb[3]
            row["null_final_sorted"] = all(ns[-1][i] <= ns[-1][i + 1] for i in range(a.n - 1)) if ns else True
            rows.append(row)
            res["conditions"][key] = rows
            json.dump(res, open(a.out, "w"), indent=0)
            print(a.kind, F, e, {k: row.get(k) for k in ("swaps", "dg", "null_dg", "steps_not_minus1_inversion", "seconds")}, flush=True)


if __name__ == "__main__":
    main()
