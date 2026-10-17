#!/usr/bin/env python3
"""Fast, seeded re-implementation of the official cell-view sorting rules (cell_research commit 1fd2bd59), for null
models that need thousands of runs. Validated against runs of the official code (validate.py) before use.

Rules, translated line by line from the official classes (no frozen cells here):
  Bubble     pick left or right with probability 1/2; swap right if value > right neighbour, left if value < left.
  Insertion  only if every cell to its left is in non-decreasing order: swap left if value < left neighbour.
  Selection  keeps an ideal position (initially the left boundary); if ideal != current position: if the occupant of
             the ideal position is smaller or equal, advance ideal by one and do nothing; else swap into the ideal
             position (the occupant goes to the selection cell's old position).
Scheduling: the official code runs one Python thread per cell under one lock. burst=1 (default): each tick activates one
cell drawn at random, with probability proportional to its rate (1 unless a speed null is requested). burst=-1:
round-robin over cells in creation order, a cell of rate r taking r interleaved turns per cycle; this is the scheduling
that reproduces the official swap counts (validated in REPORT.md), so it is the primary scheduling of the study.
Snapshots are recorded at the initial state and after every swap, as the official probe does.

Library use: run(values, kinds, labels, seed, rates=None, reset_selection_at=None, record=True) -> dict
"""
import numpy as np

B, S, I = 0, 1, 2
TYPE_ID = {"B": 0, "S": 1, "I": 2}


def run(values, kinds, labels=None, seed=0, rates=None, max_ticks=10 ** 8, record=True,
        reset_selection_at=None, reset_mode="left", start_state=None, label_rates=None, burst=1):
    """values, kinds: lists (kind in 'B','S','I'). labels: recorded type per cell (defaults to the kind id).
    reset_selection_at: swap count at which every selection cell's ideal position is reset (CRR state-vs-history
    check); reset_mode 'left' (initial value) or 'current' (own current position).
    start_state: optional (values, kinds, labels, ideal) to continue from a saved state."""
    rng = np.random.default_rng(seed)
    n = len(values) if start_state is None else len(start_state[0])
    if start_state is not None:
        val, kind, lab, ideal = [list(x) for x in start_state]
    else:
        val = list(values); kind = [TYPE_ID[k] for k in kinds]
        lab = list(labels) if labels is not None else list(kind)
        ideal = [0] * n                      # selection cells' ideal position (index into the array)
    # ideal is stored per CELL; cells are tracked by position, so carry an id array
    cid = list(range(n))
    ideal_by_cell = {cid[i]: ideal[i] for i in range(n)}
    w = np.array([1.0 if rates is None else rates[kind[i]] for i in range(n)])
    if label_rates:
        lr = dict((int(a), float(b)) for a, b in (x.split(":") for x in label_rates.split(",")))
        w = np.array([lr.get(lab[i], 1.0) for i in range(n)])    # speed null: rate depends on the inert label only
    cell_kind = {cid[i]: kind[i] for i in range(n)}
    cell_rate = {cid[i]: w[i] for i in range(n)}
    order_ids = np.array(cid)
    probs = w / w.sum()
    snaps_t, snaps_v = ([list(lab)], [list(val)]) if record else (None, None)
    swaps = 0; ticks = 0
    pos_of = {cid[i]: i for i in range(n)}
    sorted_now = lambda: all(val[i] <= val[i + 1] for i in range(n - 1))
    check_every = n
    batch = rng.choice(order_ids, size=100000, p=probs)
    bi = 0
    # round-robin schedule: each cell id appears round(weight) times per cycle, interleaved (rate 1 everywhere gives
    # plain creation-order round-robin, which reproduces the official swap counts; see REPORT)
    reps = [max(1, int(round(x))) for x in w]
    sched = [c for r_ in range(max(reps)) for c in range(n) if r_ < reps[c]]
    while ticks < max_ticks:
        if ticks % check_every == 0 and sorted_now():
            break
        if burst == -1:
            cur = sched[ticks % len(sched)]              # round-robin over cells in creation order (cell id)
        elif burst > 1 and ticks % burst != 0:
            pass                                     # burst scheduling: the same cell keeps the turn
        else:
            if bi == len(batch):
                batch = rng.choice(order_ids, size=100000, p=probs); bi = 0
            cur = int(batch[bi]); bi += 1
        c = cur; ticks += 1
        p = pos_of[c]; k = cell_kind[c]
        tgt = None
        if k == B:
            if rng.random() < 0.5:
                if p + 1 < n and val[p] > val[p + 1]:
                    tgt = p + 1
            else:
                if p - 1 >= 0 and val[p] < val[p - 1]:
                    tgt = p - 1
        elif k == I:
            if p > 0 and val[p] < val[p - 1]:
                ok = True
                for j in range(1, p):
                    if val[j] < val[j - 1]:
                        ok = False; break
                if ok:
                    tgt = p - 1
        else:  # selection
            ip = ideal_by_cell[c]
            if ip != p and 0 <= ip < n:
                if val[p] >= val[ip]:
                    ideal_by_cell[c] = ip + 1
                else:
                    tgt = ip
        if tgt is not None:
            other = cid[tgt]
            val[p], val[tgt] = val[tgt], val[p]
            lab[p], lab[tgt] = lab[tgt], lab[p]
            cid[p], cid[tgt] = cid[tgt], cid[p]
            pos_of[c], pos_of[other] = tgt, p
            swaps += 1
            if record:
                snaps_t.append(list(lab)); snaps_v.append(list(val))
            if reset_selection_at is not None and swaps == reset_selection_at:
                for cc, kk in cell_kind.items():
                    if kk == S:
                        ideal_by_cell[cc] = 0 if reset_mode == "left" else pos_of[cc]
    out = {"swaps": swaps, "ticks": ticks, "sorted": sorted_now(), "final_labels": list(lab), "final_values": list(val)}
    if record:
        out["types"] = np.array(snaps_t, dtype=np.uint8); out["values"] = np.array(snaps_v, dtype=np.int16)
    out["state"] = (list(val), [cell_kind[x] for x in cid], list(lab), [ideal_by_cell[x] for x in cid])
    return out


def setup(n, mix, dup, seed):
    """Same construction as run_official.py: values (unique or `dup` copies each) and algotype slots shuffled
    independently; inert-label mixes ('BB', 'SS', 'II') get label 9 on the second half."""
    import random
    rng = random.Random(seed)
    values = [v for v in range(n // dup) for _ in range(dup)] if dup else list(range(n))
    rng.shuffle(values)
    inert = len(set(mix)) == 1
    kinds_list = list(mix) if not inert else [mix[0]] * max(2, len(mix))
    inert_labels = [TYPE_ID[mix[0]], 9, 8]          # 'BB' -> two labels, 'BBB' -> three labels, same rule
    per = n // len(kinds_list)
    slots = []
    for k_i, k in enumerate(kinds_list):
        slots += [(k, inert_labels[k_i] if inert else TYPE_ID[k])] * per
    last = len(kinds_list) - 1
    slots += [(kinds_list[-1], inert_labels[last] if inert else TYPE_ID[kinds_list[-1]])] * (n - len(slots))
    rng.shuffle(slots)
    return values, [s[0] for s in slots], [s[1] for s in slots]
