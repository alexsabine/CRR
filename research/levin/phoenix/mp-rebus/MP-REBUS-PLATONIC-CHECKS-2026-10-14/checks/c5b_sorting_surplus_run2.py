#!/usr/bin/env python3
"""C5b: self-sorting arrays with the paper's rules (after Zhang, Goldstein & Levin 2024/25 as reported by the sweep; not their code)
and two carriers: inversions, and the adjacent-pair sortedness measure the paper uses.

Cell-view bubble: each sweep visits cells in random order; a visited non-frozen cell compares with its right neighbour and swaps if
out of order (and with its left neighbour likewise). Movable frozen cells never initiate but can be moved by a neighbour.
Classical bubble: left-to-right passes. Carriers: e_inv(t) = inversions; e_adj(t) = number of adjacent pairs out of order
(100 - Sortedness in the paper's units, up to the pair/cell convention). C = sum|de|, C* = |e_T - e_0|, S = C - C*, B = S/2.
numpy only; seed 0.
"""
import json, pathlib
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)
N, REPS = 100, 100


def inversions(a):
    c = 0
    for i in range(len(a)):
        c += int(np.sum(a[i + 1:] < a[i]))
    return c


def adj_err(a):
    return int(np.sum(a[:-1] > a[1:]))


def path_stats(e):
    e = np.array(e, float)
    C = float(np.abs(np.diff(e)).sum()); Cstar = float(abs(e[-1] - e[0])); S = C - Cstar
    return {"C": C, "Cstar": Cstar, "S": S, "B": S / 2}


def cellview_bubble(a, frozen, rng, max_sweeps=2000):
    e_inv, e_adj = [inversions(a)], [adj_err(a)]
    for _ in range(max_sweeps):
        changed = False
        for i in rng.permutation(N):
            if frozen[i]:
                continue
            if i + 1 < N and a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]; changed = True
                e_inv.append(inversions(a)); e_adj.append(adj_err(a))
            elif i - 1 >= 0 and a[i - 1] > a[i]:
                a[i - 1], a[i] = a[i], a[i - 1]; changed = True
                e_inv.append(inversions(a)); e_adj.append(adj_err(a))
        if not changed:
            break
    return e_inv, e_adj, bool(e_inv[-1] == 0)


def classical_bubble(a):
    e_inv, e_adj = [inversions(a)], [adj_err(a)]
    for _ in range(N):
        changed = False
        for i in range(N - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]; changed = True
                e_inv.append(inversions(a)); e_adj.append(adj_err(a))
        if not changed:
            break
    return e_inv, e_adj, bool(e_inv[-1] == 0)


def random_null(rng, swaps=2000):
    a = rng.permutation(N).astype(float)
    e_inv, e_adj = [inversions(a)], [adj_err(a)]
    for _ in range(swaps):
        i = rng.integers(0, N - 1)
        a[i], a[i + 1] = a[i + 1], a[i]
        e_inv.append(inversions(a)); e_adj.append(adj_err(a))
    return {"inv": path_stats(e_inv), "adj": path_stats(e_adj), "sorted": bool(e_inv[-1] == 0)}


def main():
    res = {"cellview": {}, "classical": None, "null": None}
    for k in (0, 1, 2, 3):
        rows = []
        for r in range(REPS):
            rng = np.random.default_rng(r)
            a = rng.permutation(N).astype(float)
            frozen = np.zeros(N, bool)
            if k:
                frozen[rng.choice(N, size=k, replace=False)] = True
            e_inv, e_adj, ok = cellview_bubble(a, frozen, rng)
            rows.append({"inv": path_stats(e_inv), "adj": path_stats(e_adj), "sorted": ok})
        res["cellview"][f"frozen_{k}"] = {
            "S_inv_max": float(max(x["inv"]["S"] for x in rows)),
            "S_adj_mean": float(np.mean([x["adj"]["S"] for x in rows])),
            "B_adj_mean": float(np.mean([x["adj"]["B"] for x in rows])),
            "frac_S_adj_positive": float(np.mean([x["adj"]["S"] > 0 for x in rows])),
            "sorted_frac": float(np.mean([x["sorted"] for x in rows])),
        }
    rows = []
    for r in range(REPS):
        rng = np.random.default_rng(r)
        a = rng.permutation(N).astype(float)
        e_inv, e_adj, ok = classical_bubble(a)
        rows.append({"inv": path_stats(e_inv), "adj": path_stats(e_adj), "sorted": ok})
    res["classical"] = {
        "S_inv_max": float(max(x["inv"]["S"] for x in rows)),
        "S_adj_mean": float(np.mean([x["adj"]["S"] for x in rows])),
        "B_adj_mean": float(np.mean([x["adj"]["B"] for x in rows])),
        "frac_S_adj_positive": float(np.mean([x["adj"]["S"] > 0 for x in rows])),
        "sorted_frac": float(np.mean([x["sorted"] for x in rows])),
    }
    res["null"] = random_null(np.random.default_rng(0))
    (OUT / "c5b_sorting_surplus_run2.json").write_text(json.dumps(res, indent=1))
    lines = ["C5b — self-sorting arrays, the paper's rules and carrier (n=100, 100 replicates, seed 0)",
             "arm | S on inversion carrier (max) | S on adjacent-pair carrier (mean) | B adj (mean) | frac S_adj > 0 | fully sorted"]
    for k, v in res["cellview"].items():
        lines.append(f"cell-view {k} | {v['S_inv_max']:.1f} | {v['S_adj_mean']:.2f} | {v['B_adj_mean']:.2f} | {v['frac_S_adj_positive']:.2f} | {v['sorted_frac']:.2f}")
    v = res["classical"]
    lines.append(f"classical | {v['S_inv_max']:.1f} | {v['S_adj_mean']:.2f} | {v['B_adj_mean']:.2f} | {v['frac_S_adj_positive']:.2f} | {v['sorted_frac']:.2f}")
    n = res["null"]
    lines.append(f"random-swap null | S_inv {n['inv']['S']:.0f} | S_adj {n['adj']['S']:.0f} | sorted {n['sorted']}")
    lines.append("Declared predictions: S_inv = 0 everywhere; S_adj > 0 in most replicates for both bubbles at 0 frozen; B_adj rises with frozen count (cell-view); all cell-view arrays sort; null S far larger, never sorts.")
    (OUT / "c5b_sorting_surplus_run2.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
