#!/usr/bin/env python3
"""C5: self-sorting arrays (after Zhang, Goldstein & Levin 2024, reimplemented from the abstract's description; not their code
or parameters) through CRR: delayed gratification is surplus.

Cell's-view bubble sort: each sweep visits cells in random order; a visited (non-frozen) cell compares with its right neighbour
and swaps if out of order, provided the neighbour is not frozen. Frozen cells neither initiate nor accept swaps, so order must
route around them (elements cannot pass a frozen cell by a direct swap; a frozen cell's value is fixed in place).
Carrier: inversions e(t) (sortedness error) after each cell action. C = sum |de|, C* = |e_T - e_0|, S = C - C*, B = S/2.
Must-fail arm: random swaps with the same number of swap events.
numpy only; seed 0.
"""
import json, pathlib
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)


def inversions(a):
    n = len(a); c = 0
    for i in range(n):
        c += int(np.sum(a[i + 1:] < a[i]))
    return c


def run(n=40, frozen_frac=0.0, sweeps=400, rng=None):
    a = rng.permutation(n).astype(float)
    frozen = np.zeros(n, bool)
    k = int(round(frozen_frac * n))
    if k:
        frozen[rng.choice(n, size=k, replace=False)] = True
    e = [inversions(a)]
    swaps = 0
    for _ in range(sweeps):
        changed = False
        for i in rng.permutation(n - 1):
            if frozen[i] or frozen[i + 1]:
                continue
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]; swaps += 1; changed = True
                e.append(inversions(a))
        if not changed:
            break
    e = np.array(e, float)
    C = float(np.abs(np.diff(e)).sum()); Cstar = float(abs(e[-1] - e[0])); S = C - Cstar
    return {"frozen_frac": frozen_frac, "e0": float(e[0]), "eT": float(e[-1]), "C": C, "Cstar": Cstar, "S": S, "B": S / 2, "swaps": swaps, "sorted": bool(e[-1] == 0)}


def random_null(n=40, swaps=300, rng=None):
    a = rng.permutation(n).astype(float)
    e = [inversions(a)]
    for _ in range(swaps):
        i = rng.integers(0, n - 1)
        a[i], a[i + 1] = a[i + 1], a[i]
        e.append(inversions(a))
    e = np.array(e, float)
    C = float(np.abs(np.diff(e)).sum()); Cstar = float(abs(e[-1] - e[0]))
    return {"C": C, "Cstar": Cstar, "S": C - Cstar, "sorted": bool(e[-1] == 0)}


def main():
    res = {"runs": {}, "null": None}
    for f in (0.0, 0.1, 0.3):
        rows = [run(frozen_frac=f, rng=np.random.default_rng(s)) for s in range(20)]
        res["runs"][f"frozen_{f}"] = {"S_mean": float(np.mean([r["S"] for r in rows])), "S_max": float(np.max([r["S"] for r in rows])),
                                      "B_mean": float(np.mean([r["B"] for r in rows])), "sorted_frac": float(np.mean([r["sorted"] for r in rows])),
                                      "eT_mean": float(np.mean([r["eT"] for r in rows]))}
    res["null"] = random_null(rng=np.random.default_rng(0))
    (OUT / "c5_sorting_surplus.json").write_text(json.dumps(res, indent=1))
    lines = ["C5 — self-sorting arrays through CRR: surplus S = C - C* on the inversion carrier (n=40, 20 seeds)"]
    for k, v in res["runs"].items():
        lines.append(f"{k}: S mean {v['S_mean']:.2f}, S max {v['S_max']:.2f}, B mean {v['B_mean']:.2f}, fully sorted {v['sorted_frac']:.2f}, final inversions {v['eT_mean']:.1f}")
    lines.append(f"must-fail random-swap null: S = {res['null']['S']:.1f}, sorted {res['null']['sorted']}")
    lines.append("Declared predictions: frozen 0 -> S = 0 exactly (bubble sort never increases inversions); frozen > 0 -> S >= 0 with B the temporary error increase; null has S far larger and never sorts.")
    (OUT / "c5_sorting_surplus.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
