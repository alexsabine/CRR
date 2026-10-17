#!/usr/bin/env python3
"""C7: run Zhang, Goldstein & Levin's original cell-view bubble sort (threaded) from their public repository, imported at run
time by path (never copied into Phoenix), under the paper's settings; score with their own analysis functions (extracted by
parsing their files; the module bodies load absent .npy files on the first author's machine); add inversion, adjacent-descent
and footrule rulers with CRR surplus on each; conventional baselines (Phoenix's classical bubble with frozen cells) and the
immovable variant (documented subclass) are labelled as not theirs.

usage: python3 -I c7_authors_code_runner.py --clone <path to cell_research clone> [--exps 100] [--frozen 0,1,2,3] [--smoke]
"""
import argparse, ast, hashlib, json, os, pathlib, random, sys, threading, time
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "outputs"
OUT.mkdir(exist_ok=True)


def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def extract_functions(path, names):
    """execute only the named top-level function definitions of a file (the module body is not run)."""
    tree = ast.parse(pathlib.Path(path).read_text())
    mod = ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[])
    ns = {"np": np, "copy": __import__("copy")}
    exec(compile(mod, str(path), "exec"), ns)
    return {k: ns[k] for k in names}


# ---------- rulers ----------
def inversions(a):
    n = len(a); c = 0
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            if ai > a[j]:
                c += 1
    return c


def path_stats(e):
    e = np.asarray(e, float)
    C = float(np.abs(np.diff(e)).sum()); Cs = float(abs(e[-1] - e[0]))
    return {"C": C, "Cstar": Cs, "S": C - Cs}


def episode_diagnostics(mono_trace, frozen_pos_trace, steps_cell_types):
    """decompose the authors' DG: runs of +1 / -1 after dedup; which +1 swaps occur within one cell of a frozen position."""
    arr = []
    idx = []
    for k, x in enumerate(mono_trace):
        if not arr or arr[-1] != x:
            arr.append(x); idx.append(k)
    diffs = [arr[i] - arr[i - 1] for i in range(1, len(arr))]
    runs, run_idx = [], []
    if diffs:
        x = diffs[0]; start = 0
        for i in range(1, len(diffs)):
            if diffs[i - 1] * diffs[i] > 0:
                x += diffs[i]
            else:
                runs.append(x); run_idx.append(start); x = diffs[i]; start = i
        runs.append(x); run_idx.append(start)
    first = next((k for k, d in enumerate(runs) if d > 0), len(runs))
    episodes = []
    i = first
    while i < len(runs) - 1:
        j = i + 1
        if runs[j] > 0:
            break
        episodes.append({"inc": float(runs[i]), "dec": float(-runs[j]), "change": float((-runs[j] - runs[i]) / runs[i])})
        i += 2
    # +1 swaps near frozen cells: a swap at snapshot k is "near frozen" if any frozen position is within 1 of a changed position
    near, tot = 0, 0
    if steps_cell_types is not None and len(steps_cell_types) == len(mono_trace):
        prev_vals = None
        for k in range(1, len(mono_trace)):
            if mono_trace[k] - mono_trace[k - 1] == 1:
                tot += 1
                vals_k = [c[2] for c in steps_cell_types[k]]; vals_p = [c[2] for c in steps_cell_types[k - 1]]
                changed = [p for p in range(len(vals_k)) if vals_k[p] != vals_p[p]]
                frozen = [p for p, c in enumerate(steps_cell_types[k]) if c[3] == 1]
                if any(abs(p - f) <= 1 for p in changed for f in frozen):
                    near += 1
    return {"n_episodes": len(episodes), "mean_inc": float(np.mean([e["inc"] for e in episodes])) if episodes else 0.0,
            "mean_dec": float(np.mean([e["dec"] for e in episodes])) if episodes else 0.0,
            "last_episode_share": float(episodes[-1]["change"] / sum(e["change"] for e in episodes)) if episodes and sum(e["change"] for e in episodes) != 0 else 0.0,
            "frac_plus1_swaps_near_frozen": (near / tot) if tot else 0.0, "n_plus1_swaps": tot}


# ---------- conventional baselines (Phoenix's; not the authors') ----------
def classical_bubble_frozen(vals, frozen, movable):
    """left-to-right passes; a frozen cell never initiates; movable: an active left neighbour may swap it; immovable: never swapped."""
    a = list(vals); frz = list(frozen); n = len(a)
    snaps = [list(a)]
    for _ in range(n):
        changed = False
        for i in range(n - 1):
            if frz[i]:
                continue
            if frz[i + 1] and not movable:
                continue
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]; frz[i], frz[i + 1] = frz[i + 1], frz[i]; changed = True
                snaps.append(list(a))
        if not changed:
            break
    return snaps


# ---------- the authors' threaded run ----------
def run_authors_bubble(clone, vals, frozen_idx, immovable, poll=1.0):
    sys.path.insert(0, str(clone))
    from modules.multithread.StatusProbe import StatusProbe
    from modules.multithread.BubbleSortCell import BubbleSortCell
    from modules.multithread.CellGroup import CellGroup, GroupStatus
    from modules.multithread.MultiThreadCell import CellStatus

    class ImmovableBubbleSortCell(BubbleSortCell):
        """documented variant: a frozen target cannot be swapped (the committed code allows ACTIVE or FREEZE targets)."""
        def should_move_to(self, target_position, check_right):
            if not (self.status == CellStatus.ACTIVE and self.within_boundary(target_position)
                    and self.cells[int(target_position[0])].status == CellStatus.ACTIVE):
                return False
            return self.value > self.cells[int(target_position[0])].value if check_right else self.value < self.cells[int(target_position[0])].value

    Cls = ImmovableBubbleSortCell if immovable else BubbleSortCell
    lock = threading.Lock(); probe = StatusProbe()
    n = len(vals); left, right = (0, 1), (n - 1, 1); cells = []
    for i in range(n):
        cells.append(Cls(i + 1, vals[i], lock, (i, 1), cells, left, right, probe, disable_visualization=True))
    group = CellGroup(cells, cells, 0, left, right, GroupStatus.ACTIVE, lock, 1000000000, 1000000000)
    for c in cells:
        c.group = group
    for i in frozen_idx:
        cells[i].set_cell_to_freeze()
    # the driver's no_cells_should_move
    def no_cells_should_move():
        for c in cells:
            if c.status == CellStatus.SLEEP:
                return False
            if c.status == CellStatus.ACTIVE and c.should_move():
                return False
        return True
    lock.acquire()
    for c in cells:
        if c.status != CellStatus.FREEZE:
            c.daemon = True; c.start()
    group.daemon = True; group.start()
    lock.release()
    t0 = time.time()
    while not no_cells_should_move():
        time.sleep(poll)
        if time.time() - t0 > 600:
            break
    lock.acquire()
    for c in cells:
        c.status = CellStatus.INACTIVE
    group.status = GroupStatus.MERGED
    lock.release()
    for c in cells:
        if c.is_alive():
            c.join(timeout=2)
    group.join(timeout=2)
    final = [c.value for c in cells]
    return {"steps": [vals] + [list(s) for s in probe.sorting_steps], "cell_types": [[[0, 0, v, 1 if i in frozen_idx else 0] for i, v in enumerate(vals)]] + probe.cell_types,  # index 0: the initial state in the authors' snapshot format
            "swap_count": probe.swap_count, "compare_and_swap_count": probe.compare_and_swap_count,
            "frozen_attempts": probe.frozen_swap_attempts, "final": final, "seconds": time.time() - t0}


def score(snaps, cell_types, fn):
    mono = [fn["get_monotonicity"](s) for s in snaps]
    inv = [inversions(s) for s in snaps]
    foot = [fn["get_spearman_distance"](s) for s in snaps]
    dg = fn["get_max_delay_gratification"](snaps)
    diag = episode_diagnostics(mono, None, cell_types)
    return {"DG": float(dg), "S_adj": path_stats(mono)["S"], "S_inv": path_stats(inv)["S"], "S_foot": path_stats(foot)["S"],
            "final_adj": int(mono[-1]), "final_inv": int(inv[-1]), "n_swaps": len(snaps) - 1, **diag}, mono, inv, foot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clone", required=True); ap.add_argument("--exps", type=int, default=100)
    ap.add_argument("--frozen", default="0,1,2,3"); ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--conditions", default="cv_movable,cv_immovable,cl_movable,cl_immovable")
    ap.add_argument("--poll", type=float, default=1.0, help="stopping-rule poll interval in seconds; the authors' driver uses 1 s")
    ap.add_argument("--tag", default=None)
    args = ap.parse_args()
    clone = pathlib.Path(args.clone)
    files = ["modules/multithread/BubbleSortCell.py", "modules/multithread/MultiThreadCell.py", "modules/multithread/CellGroup.py",
             "modules/multithread/StatusProbe.py", "analysis/delay_gratification_analysis.py", "analysis/utils.py", "multithread_cell_sorting_with_frozen_steps.py"]
    prov = {"clone": str(clone), "commit": os.popen(f"git -C {clone} rev-parse HEAD").read().strip(), "sha256": {f: sha256(clone / f) for f in files},
            "python": sys.version.split()[0], "numpy": np.__version__}
    fn = extract_functions(clone / "analysis/delay_gratification_analysis.py", ["get_monotonicity", "dedup", "get_discrepency_arr", "get_first_pos", "avg_wandering_range", "max_wandering_range", "get_max_delay_gratification"])
    fn.update(extract_functions(clone / "analysis/utils.py", ["get_spearman_distance"]))
    frozen_counts = [int(x) for x in args.frozen.split(",")]
    conds = args.conditions.split(",")
    exps = 1 if args.smoke else args.exps
    results = {"provenance": prov, "settings": {"n": 100, "exps": exps, "frozen_counts": frozen_counts, "poll_seconds": args.poll}, "conditions": {}}
    traces = {}
    for cond in conds:
        for k in frozen_counts:
            rows = []
            for e in range(exps):
                random.seed(10_000 * k + e)
                vals = list(range(100)); random.shuffle(vals)
                frozen_idx = [random.randint(0, 99) for _ in range(k)]  # the driver's choice, with replacement
                if cond.startswith("cv"):
                    r = run_authors_bubble(clone, vals, frozen_idx, immovable=(cond == "cv_immovable"), poll=args.poll)
                    snaps, ct = r["steps"], r["cell_types"]
                    extra = {"probe_swaps": r["swap_count"], "probe_compare_and_swap": r["compare_and_swap_count"], "frozen_attempts": r["frozen_attempts"], "seconds": r["seconds"]}
                else:
                    frozen = [False] * 100
                    for i in frozen_idx:
                        frozen[i] = True
                    snaps = classical_bubble_frozen(vals, frozen, movable=(cond == "cl_movable")); ct = None; extra = {}
                sc, mono, inv, foot = score(snaps, ct, fn)
                sc.update(extra); sc["sorted"] = bool(inv[-1] == 0)
                rows.append(sc)
                traces[f"{cond}_f{k}_e{e}"] = np.array([mono, inv, foot], dtype=np.int32)
                if args.smoke:
                    print(cond, k, json.dumps(sc))
            keys = [x for x in rows[0] if isinstance(rows[0][x], (int, float, bool))]
            results["conditions"][f"{cond}_frozen{k}"] = {x: {"mean": float(np.mean([r[x] for r in rows])), "sd": float(np.std([r[x] for r in rows])),
                                                            "min": float(np.min([r[x] for r in rows])), "max": float(np.max([r[x] for r in rows]))} for x in keys}
            results["conditions"][f"{cond}_frozen{k}"]["per_experiment_DG"] = [r["DG"] for r in rows]
            print(f"{cond} frozen={k}: DG mean {np.mean([r['DG'] for r in rows]):.3f} sd {np.std([r['DG'] for r in rows]):.3f} | S_inv max {max(r['S_inv'] for r in rows):.0f} | S_foot max {max(r['S_foot'] for r in rows):.0f} | S_adj mean {np.mean([r['S_adj'] for r in rows]):.1f} | swaps {np.mean([r['n_swaps'] for r in rows]):.0f} | sorted {np.mean([r['sorted'] for r in rows]):.2f} | episodes {np.mean([r['n_episodes'] for r in rows]):.1f} inc {np.mean([r['mean_inc'] for r in rows]):.2f} dec {np.mean([r['mean_dec'] for r in rows]):.2f} last-share {np.mean([r['last_episode_share'] for r in rows]):.2f} near-frozen {np.mean([r['frac_plus1_swaps_near_frozen'] for r in rows]):.2f}", flush=True)
    tag = args.tag or ("smoke" if args.smoke else "run")
    (OUT / f"c7_authors_code_{tag}.json").write_text(json.dumps(results, indent=1))
    np.savez_compressed(OUT / f"c7_authors_code_{tag}_traces.npz", **traces)


if __name__ == "__main__":
    main()
