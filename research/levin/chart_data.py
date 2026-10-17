#!/usr/bin/env python3
"""Regenerates the numbers drawn in the three charts on levin.html.

Written for the web page (not part of the original record). It calls the verbatim record scripts and reads
their values; it computes nothing new:
  (a) sorting surplus vs away-moves: calls cell_view_sort() from ashes/ontology/checks/turing_safety_ingression.py
      with exactly the arguments row_sorting_surplus() uses (array rng seed 3, 40 cells, p in {0, 0.1, 0.3}).
  (b) form selection (F1a, F1b) and (c) the precedence entropy curve (F4): executes phoenix/forms/forms_checks.py
      unchanged and reads its variables (acc_early, forms, Hp, Hi). The per-occasion entropy series is not in the
      committed output, which holds only the two endpoints; the endpoints are checked against it below.
Run from this folder:  python chart_data.py > out/chart_data.json
"""
import contextlib, io, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "ashes", "src"))
sys.path.insert(0, os.path.join(HERE, "ashes", "ontology", "checks"))
import numpy as np
from turing_safety_ingression import cell_view_sort

# (a) sorting
vals = np.random.default_rng(3).permutation(40)
sort_rows = []
for p in (0.0, 0.1, 0.3):
    swaps, away, inv0 = cell_view_sort(vals, p, seed=int(p * 10))
    sort_rows.append({"p_defect": p, "swaps_C": swaps, "inversions_Cstar": inv0, "surplus_S": swaps - inv0,
                      "away_moves": away, "two_x_away": 2 * away})

# (b), (c) forms
path = os.path.join(HERE, "phoenix", "forms", "forms_checks.py")
g = {"__name__": "__forms__"}
with contextlib.redirect_stdout(io.StringIO()):
    try:
        exec(compile(open(path).read(), path, "exec"), g)
    except SystemExit:
        pass
Hp, Hi = [float(x) for x in g["Hp"]], [float(x) for x in g["Hi"]]
committed = json.load(open(os.path.join(HERE, "expected", "forms_output.json")))
f4 = [c for c in committed["checks"] if c["id"] == "F4-precedence-signature"][0]["values"]
out = {
    "sorting": sort_rows,
    "form_selection": {"accuracy_from_early_path": float(g["acc_early"]), "P_form_plus_law": float(g["forms"].mean()),
                       "n_histories": int(len(g["forms"]))},
    "precedence": {"H_bits_production": [round(x, 6) for x in Hp], "H_bits_ingression": [round(x, 6) for x in Hi],
                   "endpoints_match_committed_output": [Hp[0], Hp[-1]] == f4["H_bits_production_n0_n59"]
                                                        and [Hi[0], Hi[-1]] == f4["H_bits_ingression_n0_n59"]},
}
print(json.dumps(out, indent=1))
