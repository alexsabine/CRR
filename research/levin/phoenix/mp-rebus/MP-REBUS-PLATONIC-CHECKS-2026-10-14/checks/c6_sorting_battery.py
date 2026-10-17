#!/usr/bin/env python3
"""C6: the full sorting battery, reimplemented from a reading of the authors' public code (not copied, not executed):
cell-view bubble / insertion / selection with movable frozen cells; classical versions; chimeras; cross-purposes;
three rulers (inversions, adjacent descents = the authors' monotonicity error, footrule); the authors' delayed-gratification
statistic (avg_wandering_range) on their measure; aggregation (the paper's description); state-sufficiency; per-cell clocks.
numpy only; seed per replicate.
"""
import json, math, pathlib, random
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)
N, REPS = 100, 50


# ---------- rulers, updated incrementally ----------
class Array:
    def __init__(self, vals):
        self.a = list(vals)
        self.n = len(self.a)
        self.inv = sum(1 for i in range(self.n) for j in range(i + 1, self.n) if self.a[i] > self.a[j])
        self.adj = sum(1 for i in range(1, self.n) if self.a[i] < self.a[i - 1])
        self.foot = sum(abs(self.a[i] - i) for i in range(self.n))
        self.trace_inv, self.trace_adj, self.trace_foot = [self.inv], [self.adj], [self.foot]
        self.swaps = 0

    def swap(self, p, q):
        """swap positions p < q (any distance); update rulers; record."""
        if p > q:
            p, q = q, p
        a = self.a
        v, o = a[q], a[p]  # v will move left to p, o right to q
        # inversions: pairs with intermediates plus the pair itself
        d = 0
        for k in range(p + 1, q):
            x = a[k]
            d += (1 if v > x else 0) - (1 if o > x else 0) + (1 if x > o else 0) - (1 if x > v else 0)
        d += (-1 if o > v else (1 if v > o else 0))
        self.inv += d
        # adjacent descents: recompute around p and q
        def adj_local():
            s = 0
            for i in {p, p + 1, q, q + 1}:
                if 1 <= i < self.n:
                    s += 1 if a[i] < a[i - 1] else 0
            return s
        before = adj_local()
        a[p], a[q] = v, o
        after = adj_local()
        self.adj += after - before
        self.foot += (abs(v - p) - abs(v - q)) + (abs(o - q) - abs(o - p))
        self.swaps += 1
        self.trace_inv.append(self.inv); self.trace_adj.append(self.adj); self.trace_foot.append(self.foot)


def path_stats(e):
    e = np.asarray(e, float)
    C = float(np.abs(np.diff(e)).sum()); Cs = float(abs(e[-1] - e[0]))
    return {"C": C, "Cstar": Cs, "S": C - Cs}


def avg_wandering_range(trace):
    """the authors' DG statistic on an error trace (reimplemented from analysis/delay_gratification_analysis.py)."""
    arr = []
    for x in trace:
        if not arr or arr[-1] != x:
            arr.append(x)
    temp = [arr[i] - arr[i - 1] for i in range(1, len(arr))]
    if not temp:
        return 0.0
    runs, x = [], temp[0]
    for i in range(1, len(temp)):
        if temp[i - 1] * temp[i] > 0:
            x += temp[i]
        else:
            runs.append(x); x = temp[i]
    runs.append(x)
    i = next((k for k, d in enumerate(runs) if d > 0), len(runs))
    if i >= len(runs) - 1:
        return 0.0
    tot, cnt = 0.0, 0
    while i < len(runs):
        j = i + 1
        if j >= len(runs) or runs[j] > 0:
            break
        tot += (-(runs[j] + runs[i])) / runs[i]; cnt += 1
        i += 2
    return tot / cnt if cnt else 0.0


# ---------- cell-view engine ----------
def cellview(vals, algos, frozen, rng, reverse=None, fatigue=0.0, counters=None, max_moves=2_000_000, sticky=0.0):
    """algos: list of 'bubble'|'insertion'|'selection' per cell; frozen: bool list; reverse: per-cell bool (descending).
    Cells are visited in random order; each visit is one 'move' of that cell. Returns Array and per-cell swap counts."""
    n = len(vals)
    A = Array(vals)
    a = A.a
    pos = {v: i for i, v in enumerate(a)}            # value -> position (values unique)
    algo_of = {a[i]: algos[i] for i in range(n)}
    frz_of = {a[i]: frozen[i] for i in range(n)}
    rev_of = {a[i]: (reverse[i] if reverse else False) for i in range(n)}
    ideal = {v: (n - 1 if rev_of[v] else 0) for v in a}
    cnt = dict(counters) if counters else {v: 0 for v in a}

    def do_swap(p, q):
        vp, vq = a[p], a[q]
        A.swap(p, q)
        pos[a[p]] = p; pos[a[q]] = q
        cnt[vp] += 1; cnt[vq] += 1

    def lt(x, y, rev):  # "x should be left of y"
        return x > y if rev else x < y

    moves = 0
    idle = 0
    last_actor = None  # C8: scheduling stickiness; sticky=0.0 reproduces C6 exactly (one extra rng draw only when sticky > 0)
    while moves < max_moves and idle < 2 * n:
        if sticky > 0 and last_actor is not None and rng.random() < sticky:
            v = last_actor
        else:
            v = a[rng.integers(0, n)]
        moves += 1
        if frz_of[v]:
            idle += 1; continue
        if fatigue and rng.random() > 1.0 / (1.0 + fatigue * cnt[v]):
            idle += 1; continue
        p = pos[v]; rev = rev_of[v]; kind = algo_of[v]
        acted = False
        if kind == "bubble":
            if rng.random() < 0.5:
                if p + 1 < n and lt(a[p + 1], v, rev):
                    do_swap(p, p + 1); acted = True
            else:
                if p - 1 >= 0 and lt(v, a[p - 1], rev):
                    do_swap(p - 1, p); acted = True
        elif kind == "insertion":
            ok = True; prev = None
            for i in range(0, p):
                if frz_of[a[i]]:
                    prev = None; continue
                if prev is not None and lt(a[i], prev, rev):
                    ok = False; break
                prev = a[i]
            if ok and p - 1 >= 0 and lt(v, a[p - 1], rev):
                do_swap(p - 1, p); acted = True
        elif kind == "selection":
            ip = ideal[v]
            step = -1 if rev else 1
            if ip != p and 0 <= ip < n:
                occ = a[ip]
                if frz_of[occ]:
                    ideal[v] = ip + step
                    if lt(v, occ, rev):
                        do_swap(min(p, ip), max(p, ip)); acted = True
                elif not lt(v, occ, rev):
                    ideal[v] = ip + step
                else:
                    do_swap(min(p, ip), max(p, ip)); acted = True
        last_actor = v if acted else None
        if acted:
            idle = 0
        else:
            idle += 1
        if idle >= 2 * n:
            # confirm nothing can move: full scan
            can = False
            for u in a:
                if frz_of[u]:
                    continue
                pp = pos[u]; rv = rev_of[u]; kd = algo_of[u]
                if kd == "bubble" and ((pp + 1 < n and lt(a[pp + 1], u, rv)) or (pp - 1 >= 0 and lt(u, a[pp - 1], rv))):
                    can = True; break
                if kd == "insertion" and pp - 1 >= 0 and lt(u, a[pp - 1], rv):
                    can = True; break
                if kd == "selection" and ideal[u] != pp and 0 <= ideal[u] < n:
                    can = True; break
            if can:
                idle = 0
            else:
                break
    A.moves = moves  # added for C6b (visits to completion); no effect on C6's outputs
    return A, cnt


def classical(vals, kind):
    A = Array(vals); a = A.a; n = len(a)
    if kind == "bubble":
        for _ in range(n):
            ch = False
            for i in range(n - 1):
                if a[i] > a[i + 1]:
                    A.swap(i, i + 1); ch = True
            if not ch:
                break
    elif kind == "insertion":
        for i in range(1, n):
            j = i
            while j > 0 and a[j] < a[j - 1]:
                A.swap(j - 1, j); j -= 1
    elif kind == "selection":
        for i in range(n - 1):
            m = min(range(i, n), key=lambda k: a[k])
            if m != i:
                A.swap(i, m)
    return A


def inversion_degree(vals):
    n = len(vals)
    return {vals[i]: sum(1 for j in range(n) if (j < i and vals[j] > vals[i]) or (j > i and vals[j] < vals[i])) for i in range(n)}


def spearman(x, y):
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])


def aggregation(labels):
    return float(np.mean([labels[i] == labels[i - 1] == labels[i + 1] for i in range(1, len(labels) - 1)]))


def perm_test(x, y, rng, n_perm=2000):
    x, y = np.asarray(x, float), np.asarray(y, float)
    obs = abs(x.mean() - y.mean()); pool = np.concatenate([x, y]); k = len(x); c = 0
    for _ in range(n_perm):
        rng.shuffle(pool)
        if abs(pool[:k].mean() - pool[k:].mean()) >= obs:
            c += 1
    return (c + 1) / (n_perm + 1)


def main():
    res = {"arms": {}, "chimeras": {}, "state_sufficiency": {}, "cell_clocks": {}}
    # ---- arms: classical and cell-view x algorithm x frozen ----
    for kind in ("bubble", "insertion", "selection"):
        rows = []
        for r in range(REPS):
            rng = np.random.default_rng(r)
            vals = list(rng.permutation(N))
            A = classical(vals, kind)
            rows.append({"S_inv": path_stats(A.trace_inv)["S"], "S_adj": path_stats(A.trace_adj)["S"], "S_foot": path_stats(A.trace_foot)["S"],
                         "DG": avg_wandering_range(A.trace_adj), "swaps": A.swaps, "sorted": A.inv == 0})
        res["arms"][f"classical_{kind}"] = summarise(rows)
        for k in (0, 1, 2, 3):
            rows = []
            for r in range(REPS):
                rng = np.random.default_rng(1000 + r)
                vals = list(rng.permutation(N))
                frozen = [False] * N
                for _ in range(k):
                    frozen[int(rng.integers(0, N))] = True
                A, _ = cellview(vals, [kind] * N, frozen, rng)
                rows.append({"S_inv": path_stats(A.trace_inv)["S"], "S_adj": path_stats(A.trace_adj)["S"], "S_foot": path_stats(A.trace_foot)["S"],
                             "DG": avg_wandering_range(A.trace_adj), "swaps": A.swaps, "sorted": A.inv == 0})
            res["arms"][f"cellview_{kind}_frozen{k}"] = summarise(rows)
    # ---- chimeras and cross-purposes ----
    # rev_label: which label (0 or 1) runs in the descending direction; None = all ascending.
    # The three paper pairings (bubble-down + selection-up; bubble-up + insertion-down; selection-down + insertion-up) were added
    # after the 30-cell smoke test and before the full run (R14): the declared arm "bubble up + selection down" is kept as declared.
    for name, pair, rev_label in (("bubble_selection", ("bubble", "selection"), None), ("bubble_insertion", ("bubble", "insertion"), None),
                                  ("selection_insertion", ("selection", "insertion"), None), ("control_bubble_bubble", ("bubble", "bubble"), None),
                                  ("cross_bubble_up_selection_down", ("bubble", "selection"), 1),
                                  ("paper_cross_bubble_down_selection_up", ("bubble", "selection"), 0),
                                  ("paper_cross_bubble_up_insertion_down", ("bubble", "insertion"), 1),
                                  ("paper_cross_selection_down_insertion_up", ("selection", "insertion"), 0)):
        peaks, finals, sorted_frac, ascend = [], [], [], []
        for r in range(REPS):
            rng = np.random.default_rng(5000 + r)
            vals = list(rng.permutation(N))
            lab = [0 if rng.random() < 0.5 else 1 for _ in range(N)]
            algos = [pair[l] for l in lab]
            reverse = [(l == rev_label) for l in lab] if rev_label is not None else None
            # track aggregation over the run by sampling snapshots: rerun with a recording wrapper
            A, cnt = cellview(vals, algos, [False] * N, rng, reverse=reverse)
            # aggregation of algotype labels is tied to values; compute along the recorded trace is expensive, so sample positions at the end and at start
            lab_of = {vals[i]: lab[i] for i in range(N)}
            start_lab = [lab_of[v] for v in vals]; end_lab = [lab_of[v] for v in A.a]
            peaks.append(max(aggregation(start_lab), aggregation(end_lab)))
            finals.append(aggregation(end_lab))
            sorted_frac.append(A.inv == 0)
            ascend.append(float(np.mean([A.a[i] < A.a[i + 1] for i in range(N - 1)])))
        res["chimeras"][name] = {"aggregation_start_or_end_max_mean": float(np.mean(peaks)), "aggregation_end_mean": float(np.mean(finals)),
                                 "sorted_frac": float(np.mean(sorted_frac)), "ascending_pair_frac_mean": float(np.mean(ascend))}
    # transient aggregation needs a mid-run snapshot: rerun bubble_selection and control recording aggregation every 50 swaps
    for name, pair in (("bubble_selection", ("bubble", "selection")), ("control_bubble_bubble", ("bubble", "bubble"))):
        peak_over_run = []
        for r in range(REPS):
            rng = np.random.default_rng(7000 + r)
            vals = list(rng.permutation(N))
            lab = [0 if rng.random() < 0.5 else 1 for _ in range(N)]
            algos = [pair[l] for l in lab]
            lab_of = {vals[i]: lab[i] for i in range(N)}
            A = TrackedRun(vals, algos, rng, lab_of)
            peak_over_run.append(A.peak)
        res["chimeras"][name]["aggregation_peak_over_run_mean"] = float(np.mean(peak_over_run))
    # ---- state-sufficiency ----
    for label, fat in (("authors_rules", 0.0), ("mustfail_fatigue", 0.05)):
        ps = []
        for t in range(40):
            rng = np.random.default_rng(9000 + t)
            vals = list(rng.permutation(N))
            # route A: run 600 moves to reach a state with real per-cell counts
            A, cnt = cellview(vals, ["bubble"] * N, [False] * N, rng, fatigue=fat, max_moves=600)
            state = list(A.a)
            rem_A, rem_B = [], []
            for s in range(20):
                r1 = np.random.default_rng(100000 + 100 * t + s); r2 = np.random.default_rng(200000 + 100 * t + s)
                B1, _ = cellview(state, ["bubble"] * N, [False] * N, r1, fatigue=fat, counters=cnt)
                B2, _ = cellview(state, ["bubble"] * N, [False] * N, r2, fatigue=fat, counters={v: 0 for v in state})
                rem_A.append(B1.swaps); rem_B.append(B2.swaps)
            ps.append(perm_test(rem_A, rem_B, np.random.default_rng(300000 + t)))
        ps = np.array(ps)
        res["state_sufficiency"][label] = {"frac_p_gt_0.05": float(np.mean(ps > 0.05)), "frac_p_lt_0.05": float(np.mean(ps < 0.05)), "median_p": float(np.median(ps))}
    # ---- per-cell clocks ----
    for kind in ("bubble", "insertion", "selection"):
        rhos, maxdiff = [], []
        for r in range(20):
            rng = np.random.default_rng(11000 + r)
            vals = list(rng.permutation(N))
            A, cnt = cellview(vals, [kind] * N, [False] * N, rng)
            deg = inversion_degree(vals)
            x = [cnt[v] for v in vals]; y = [deg[v] for v in vals]
            rhos.append(spearman(x, y)); maxdiff.append(max(abs(xi - yi) for xi, yi in zip(x, y)))
        res["cell_clocks"][f"cellview_{kind}"] = {"spearman_swaps_vs_inversion_degree_mean": float(np.mean(rhos)), "max_abs_diff_mean": float(np.mean(maxdiff)),
                                                    "per_cell_swaps_CV_mean": None}
    (OUT / "c6_sorting_battery.json").write_text(json.dumps(res, indent=1))
    lines = ["C6 — sorting battery (n=100, 50 replicates per arm; authors' rules reimplemented; authors' DG statistic on their measure)",
             "arm | S_inv max | S_foot max | frac S_adj>0 | S_adj mean | DG mean | swaps mean | sorted"]
    for k, v in res["arms"].items():
        lines.append(f"{k} | {v['S_inv_max']:.0f} | {v['S_foot_max']:.0f} | {v['frac_S_adj_pos']:.2f} | {v['S_adj_mean']:.1f} | {v['DG_mean']:.3f} | {v['swaps_mean']:.0f} | {v['sorted_frac']:.2f}")
    lines.append("chimeras: " + json.dumps(res["chimeras"]))
    lines.append("state-sufficiency: " + json.dumps(res["state_sufficiency"]))
    lines.append("cell clocks: " + json.dumps(res["cell_clocks"]))
    (OUT / "c6_sorting_battery.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


class TrackedRun:
    """cell-view run that samples the aggregation of algotype labels every 50 swaps (bubble/selection chimeras)."""
    def __init__(self, vals, algos, rng, lab_of):
        n = len(vals); self.peak = 0.0
        A = Array(vals); a = A.a
        pos = {v: i for i, v in enumerate(a)}; algo_of = {a[i]: algos[i] for i in range(n)}
        ideal = {v: 0 for v in a}
        last = -1; idle = 0; moves = 0
        def lt(x, y): return x < y
        def do_swap(p, q):
            A.swap(p, q); pos[a[p]] = p; pos[a[q]] = q
        while moves < 2_000_000 and idle < 2 * n:
            v = a[rng.integers(0, n)]; moves += 1; p = pos[v]; acted = False
            if algo_of[v] == "bubble":
                if rng.random() < 0.5:
                    if p + 1 < n and a[p + 1] < v: do_swap(p, p + 1); acted = True
                else:
                    if p - 1 >= 0 and v < a[p - 1]: do_swap(p - 1, p); acted = True
            else:
                ip = ideal[v]
                if ip != p and 0 <= ip < n:
                    occ = a[ip]
                    if not (v < occ): ideal[v] = ip + 1
                    else: do_swap(min(p, ip), max(p, ip)); acted = True
            if acted:
                idle = 0
                if A.swaps // 50 != last:
                    last = A.swaps // 50
                    self.peak = max(self.peak, aggregation([lab_of[x] for x in a]))
            else:
                idle += 1
                if idle >= 2 * n:
                    can = any((algo_of[u] == "bubble" and ((pos[u] + 1 < n and a[pos[u] + 1] < u) or (pos[u] - 1 >= 0 and u < a[pos[u] - 1]))) or
                              (algo_of[u] == "selection" and ideal[u] != pos[u] and ideal[u] < n) for u in a)
                    if can: idle = 0
                    else: break
        self.peak = max(self.peak, aggregation([lab_of[x] for x in a]))


def summarise(rows):
    return {"S_inv_max": float(max(r["S_inv"] for r in rows)), "S_foot_max": float(max(r["S_foot"] for r in rows)),
            "frac_S_adj_pos": float(np.mean([r["S_adj"] > 0 for r in rows])), "S_adj_mean": float(np.mean([r["S_adj"] for r in rows])),
            "DG_mean": float(np.mean([r["DG"] for r in rows])), "DG_sd": float(np.std([r["DG"] for r in rows])),
            "swaps_mean": float(np.mean([r["swaps"] for r in rows])), "sorted_frac": float(np.mean([r["sorted"] for r in rows]))}


if __name__ == "__main__":
    main()
