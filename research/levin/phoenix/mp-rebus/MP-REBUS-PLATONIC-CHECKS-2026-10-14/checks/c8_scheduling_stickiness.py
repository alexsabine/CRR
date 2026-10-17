"""C8: scheduling stickiness and the authors' DG (see DECLARATION_ADDENDUM_C8.md). Imports the C6 engine by path."""
import importlib.util, json, pathlib, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE.parent / "outputs"
spec = importlib.util.spec_from_file_location("c6", HERE / "c6_sorting_battery.py"); c6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c6)
N, REPS = 100, 50
# mover-run statistic: the engine's Array records swaps? No: record via a wrapper on Array.swap
runs_log = []
orig_swap = c6.Array.swap
def swap_logged(self, p, q):
    runs_log.append((self.a[p], self.a[q])); orig_swap(self, p, q)
c6.Array.swap = swap_logged
def mean_mover_run(log):
    """mean length of maximal runs of consecutive swaps sharing a value with the previous swap"""
    if not log: return 0.0
    runs, cur = [], 1
    for i in range(1, len(log)):
        if set(log[i]) & set(log[i - 1]): cur += 1
        else: runs.append(cur); cur = 1
    runs.append(cur); return float(np.mean(runs))
res = {}
lines = ["C8 scheduling stickiness (cell-view bubble, movable frozen cells, n=100, 50 reps; authors' DG on adjacent descents)",
         "sticky | frozen | DG mean (sd) | S_inv max | S_foot max | S_adj mean | swaps | sorted | mover-run mean"]
for sticky in (0.0, 0.5, 0.9, 0.99, 1.0):
    for k in (0, 1, 2, 3):
        rows = []
        for rep in range(REPS):
            rng = np.random.default_rng(1000 * k + rep)       # C6's seeding for the cell-view bubble arms
            vals = list(rng.permutation(N))
            frozen = [False] * N
            for i in rng.integers(0, N, k): frozen[i] = True
            runs_log.clear()
            A, _ = c6.cellview(vals, ["bubble"] * N, frozen, rng, sticky=sticky)
            rows.append({"DG": c6.avg_wandering_range(A.trace_adj), "S_inv": c6.path_stats(A.trace_inv)["S"], "S_adj": c6.path_stats(A.trace_adj)["S"],
                         "S_foot": c6.path_stats(A.trace_foot)["S"], "swaps": A.swaps, "sorted": A.inv == 0, "mover_run": mean_mover_run(list(runs_log))})
        key = f"sticky{sticky}_frozen{k}"
        res[key] = {x: float(np.mean([r[x] for r in rows])) for x in ("DG", "S_adj", "swaps", "sorted", "mover_run")}
        res[key].update({"DG_sd": float(np.std([r["DG"] for r in rows])), "S_inv_max": float(max(r["S_inv"] for r in rows)), "S_foot_max": float(max(r["S_foot"] for r in rows))})
        r = res[key]
        line = f"{sticky} | {k} | {r['DG']:.3f} ({r['DG_sd']:.3f}) | {r['S_inv_max']:.0f} | {r['S_foot_max']:.0f} | {r['S_adj']:.1f} | {r['swaps']:.0f} | {r['sorted']:.2f} | {r['mover_run']:.2f}"
        lines.append(line); print(line, flush=True)
(OUT / "c8_scheduling_stickiness.json").write_text(json.dumps(res, indent=1))
(OUT / "c8_scheduling_stickiness.txt").write_text("\n".join(lines) + "\n")
