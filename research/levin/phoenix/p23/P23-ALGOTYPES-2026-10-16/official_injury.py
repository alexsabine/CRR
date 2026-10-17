#!/usr/bin/env python3
"""Same form, different history, with the OFFICIAL cell classes (cell_research 1fd2bd59, unchanged).

1. Sort a chimeric array with the official threaded cells (as run_official.py).
2. Injure the sorted array: shuffle a contiguous window of W cells (seeded).
3. Re-sort two copies built from fresh official cell objects with the injured configuration:
   HISTORY: each selection cell's ideal_position is copied from the cell that sorted the array (moved with it);
   FRESH:   ideal_position left at the class default (the left boundary).
   Bubble and insertion cells carry no internal memory in the official classes, so both copies differ only there.
4. Record whether each copy re-sorts within the timeout, and its swaps.

Usage: python3 official_injury.py OFFICIAL_DIR OUT_JSON --mix BS --n 100 --exps 20 --window 20 --timeout 30
"""
import argparse
import json
import os
import random
import sys
import threading
import time


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("official"); ap.add_argument("out"); ap.add_argument("--mix", default="BS")
    ap.add_argument("--n", type=int, default=100); ap.add_argument("--exps", type=int, default=20)
    ap.add_argument("--window", type=int, default=20); ap.add_argument("--timeout", type=float, default=30)
    a = ap.parse_args()
    sys.path.insert(0, os.path.abspath(a.official))
    from modules.multithread.BubbleSortCell import BubbleSortCell
    from modules.multithread.SelectionSortCell import SelectionSortCell
    from modules.multithread.InsertionSortCell import InsertionSortCell
    from modules.multithread.CellGroup import CellGroup, GroupStatus
    from modules.multithread.MultiThreadCell import CellStatus
    from modules.multithread.StatusProbe import StatusProbe
    CLS = {"B": BubbleSortCell, "S": SelectionSortCell, "I": InsertionSortCell}
    lb, rb = (0, 1), (a.n - 1, 1)

    def build(spec, ideals=None):
        lock = threading.Lock(); probe = StatusProbe(); cells = []
        for i, (k, v) in enumerate(spec):
            c = CLS[k](i + 1, v, lock, (i, 1), cells, lb, rb, probe, disable_visualization=True)
            if ideals is not None and k == "S" and ideals[i] is not None:
                c.ideal_position = ideals[i]
            cells.append(c)
        g = CellGroup(cells, cells, 0, lb, rb, GroupStatus.ACTIVE, lock, 10 ** 9, 10 ** 9)
        for c in cells:
            c.group = g
        return cells, g, lock, probe

    def run(cells, g, lock, probe, timeout):
        lock.acquire()
        for c in cells:
            c.start()
        g.start(); lock.release()
        t0 = time.time(); ok = False
        while time.time() - t0 < timeout:
            vals = [c.value for c in cells]
            if all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1)):
                ok = True; break
            time.sleep(0.0005)
        lock.acquire()
        for c in cells:
            c.status = CellStatus.INACTIVE
        g.status = GroupStatus.MERGED; lock.release()
        for c in cells:
            c.join(timeout=5)
        g.join(timeout=5)
        return ok, probe.swap_count, time.time() - t0

    rows = []
    for e in range(a.exps):
        rng = random.Random(e)
        values = list(range(a.n)); rng.shuffle(values)
        kinds = [k for k in a.mix for _ in range(a.n // len(a.mix))]
        kinds += [a.mix[-1]] * (a.n - len(kinds)); rng.shuffle(kinds)
        random.seed(e)
        cells, g, lock, probe = build(list(zip(kinds, values)))
        ok0, sw0, _ = run(cells, g, lock, probe, 120)
        order = list(cells)                          # array order after sorting
        spec = [(c.cell_type[0], c.value) for c in order]
        ideals = [c.ideal_position if c.cell_type == "Selection" else None for c in order]
        r2 = random.Random(30_000 + e)
        start = r2.randrange(0, a.n - a.window)
        perm = list(range(start, start + a.window)); r2.shuffle(perm)
        idx = list(range(a.n)); idx[start:start + a.window] = perm
        spec_i = [spec[i] for i in idx]; ideals_i = [ideals[i] for i in idx]
        res = {"seed": e, "first_sort_ok": ok0, "first_sort_swaps": sw0, "window_start": start}
        for name, ide in (("history", ideals_i), ("fresh", None)):
            random.seed(50_000 + e)
            c2, g2, l2, p2 = build(spec_i, ide)
            ok, sw, sec = run(c2, g2, l2, p2, a.timeout)
            res[name] = {"resorted": ok, "swaps": sw, "seconds": round(sec, 2)}
        rows.append(res)
        print(e, res["history"], res["fresh"], flush=True)
    summ = {"mix": a.mix, "n": a.n, "exps": a.exps, "window": a.window, "timeout_s": a.timeout,
            "history_resorted": sum(r["history"]["resorted"] for r in rows),
            "fresh_resorted": sum(r["fresh"]["resorted"] for r in rows),
            "history_swaps_mean": sum(r["history"]["swaps"] for r in rows) / len(rows),
            "fresh_swaps_mean": sum(r["fresh"]["swaps"] for r in rows) / len(rows)}
    json.dump({"summary": summ, "rows": rows}, open(a.out, "w"), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
