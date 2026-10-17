#!/usr/bin/env python3
"""Run the OFFICIAL cell_research code (Zhang, Goldstein & Levin; github.com/Zhangtaining/cell_research at commit
1fd2bd59) unchanged, for chimeric-array experiments, and save compact per-swap records.

The official modules are imported from OFFICIAL_DIR; nothing in them is edited. This driver reproduces the set-up of
the official `multithread_sorting_cell_aggregation_analysis.py` (one cell group spanning the array, all cells active,
threads started under the lock, run until sorted) without its tkinter/visualisation imports, and lets the caller pick
the algotype mix, the inert-label control and unique or duplicated values.

Mixes: BS, BI, SI (two algotypes, half each), BSI (thirds), and the inert-label controls BB, SS, II (one algorithm,
two labels: the second half of cells get label 9, so the snapshot type field differs while the rule is identical).

Output (one .npz per experiment): types (steps+1, N) uint8 and values (steps+1, N) int16, recorded at the initial state
and after every swap, exactly where the official probe records snapshots.

Usage: python3 run_official.py OFFICIAL_DIR OUT_DIR --mix BS --n 100 --exps 20 [--dup 10] [--timeout 300] [--seed0 0]
"""
import argparse
import os
import random
import sys
import threading
import time

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("official"); ap.add_argument("out")
    ap.add_argument("--mix", default="BS"); ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--exps", type=int, default=10); ap.add_argument("--dup", type=int, default=0)
    ap.add_argument("--timeout", type=float, default=300); ap.add_argument("--seed0", type=int, default=0)
    a = ap.parse_args()
    sys.path.insert(0, os.path.abspath(a.official))
    from modules.multithread.BubbleSortCell import BubbleSortCell
    from modules.multithread.SelectionSortCell import SelectionSortCell
    from modules.multithread.InsertionSortCell import InsertionSortCell
    from modules.multithread.CellGroup import CellGroup, GroupStatus
    from modules.multithread.MultiThreadCell import CellStatus
    from modules.multithread.StatusProbe import StatusProbe
    CLS = {"B": BubbleSortCell, "S": SelectionSortCell, "I": InsertionSortCell}
    os.makedirs(a.out, exist_ok=True)
    mix = a.mix
    inert = len(set(mix)) == 1
    kinds = list(mix) if not inert else [mix[0]] * max(2, len(mix))
    inert_labels = [0, 9, 8]                     # 'BB' -> labels 0 and 9; 'BBB' -> 0, 9, 8; same rule for all
    for e in range(a.seed0, a.seed0 + a.exps):
        fn = os.path.join(a.out, "%s_%s_exp%04d.npz" % (mix, "dup%d" % a.dup if a.dup else "uniq", e))
        if os.path.exists(fn):
            continue
        rng = random.Random(e)
        if a.dup:
            values = [v for v in range(a.n // a.dup) for _ in range(a.dup)]
        else:
            values = list(range(a.n))
        rng.shuffle(values)
        per = a.n // len(kinds)
        slots = []
        for k_i, k in enumerate(kinds):
            slots += [(k, inert_labels[k_i] if inert else 0)] * per
        slots += [(kinds[-1], inert_labels[len(kinds) - 1] if inert else 0)] * (a.n - len(slots))
        rng.shuffle(slots)
        random.seed(e)                      # the official cells draw from the global random module
        lock = threading.Lock(); probe = StatusProbe(); cells = []
        lb, rb = (0, 1), (a.n - 1, 1)
        for i in range(a.n):
            k, label = slots[i]
            cells.append(CLS[k](i + 1, values[i], lock, (i, 1), cells, lb, rb, probe, disable_visualization=True, label=label))
        group = CellGroup(cells, cells, 0, lb, rb, GroupStatus.ACTIVE, lock, 10 ** 9, 10 ** 9)
        for c in cells:
            c.group = group
        init_types = [c.cell_type_dict[c.cell_type] if c.label == 0 else c.label for c in cells]
        init_vals = [c.value for c in cells]
        lock.acquire()
        for c in cells:
            c.start()
        group.start()
        lock.release()
        t0 = time.time(); ok = True
        while True:
            vals = [c.value for c in cells]
            if all(vals[i] <= vals[i + 1] for i in range(len(vals) - 1)):
                break
            if time.time() - t0 > a.timeout:
                ok = False
                break
            time.sleep(0.0005)
        lock.acquire()
        for c in cells:
            c.status = CellStatus.INACTIVE
        group.status = GroupStatus.MERGED
        lock.release()
        for c in cells:
            c.join(timeout=5)
        group.join(timeout=5)
        snaps = probe.cell_types           # list of [[group, type, value, frozen], ...] after each swap
        types = np.array([init_types] + [[s[1] for s in snap] for snap in snaps], dtype=np.uint8)
        vals = np.array([init_vals] + [[s[2] for s in snap] for snap in snaps], dtype=np.int16)
        np.savez_compressed(fn, types=types, values=vals, ok=ok, seconds=time.time() - t0)
        print("%s exp %d swaps %d sorted %s %.1fs" % (mix, e, len(snaps), ok, time.time() - t0), flush=True)


if __name__ == "__main__":
    main()
