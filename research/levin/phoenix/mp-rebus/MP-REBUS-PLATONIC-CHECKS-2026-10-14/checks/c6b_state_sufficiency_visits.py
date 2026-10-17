"""C6b: state-sufficiency on remaining visits (see DECLARATION_ADDENDUM_C6B.md). Imports the C6 engine by path."""
import importlib.util, json, pathlib, sys, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE.parent / "outputs"
spec = importlib.util.spec_from_file_location("c6", HERE / "c6_sorting_battery.py"); c6 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c6)
N = 100
res = {}
for label, fat in (("authors_rules", 0.0), ("mustfail_fatigue", 0.05)):
    pv, psw = [], []
    for t in range(40):
        rng = np.random.default_rng(9000 + t)
        vals = list(rng.permutation(N))
        A, cnt = c6.cellview(vals, ["bubble"] * N, [False] * N, rng, fatigue=fat, max_moves=600)
        state = list(A.a)
        vA, vB, sA, sB = [], [], [], []
        for s in range(20):
            r1 = np.random.default_rng(100000 + 100 * t + s); r2 = np.random.default_rng(200000 + 100 * t + s)
            B1, _ = c6.cellview(state, ["bubble"] * N, [False] * N, r1, fatigue=fat, counters=cnt)
            B2, _ = c6.cellview(state, ["bubble"] * N, [False] * N, r2, fatigue=fat, counters={v: 0 for v in state})
            vA.append(B1.moves); vB.append(B2.moves); sA.append(B1.swaps); sB.append(B2.swaps)
        pv.append(c6.perm_test(vA, vB, np.random.default_rng(300000 + t)))
        psw.append(c6.perm_test(sA, sB, np.random.default_rng(400000 + t)))
        print(label, t, "visits p", round(pv[-1], 4), "mean carried", np.mean(vA), "zeroed", np.mean(vB), "| swaps p", round(psw[-1], 4), flush=True)
    pv, psw = np.array(pv), np.array(psw)
    res[label] = {"visits": {"frac_p_gt_0.05": float(np.mean(pv > 0.05)), "frac_p_lt_0.05": float(np.mean(pv < 0.05)), "median_p": float(np.median(pv))},
                  "swaps": {"frac_p_gt_0.05": float(np.mean(psw > 0.05)), "frac_p_lt_0.05": float(np.mean(psw < 0.05)), "median_p": float(np.median(psw))}}
(OUT / "c6b_state_sufficiency_visits.json").write_text(json.dumps(res, indent=1))
(OUT / "c6b_state_sufficiency_visits.txt").write_text("C6b state-sufficiency, statistic = remaining visits (remaining swaps as invariant control)\n" + json.dumps(res, indent=1) + "\n")
print(json.dumps(res, indent=1))
