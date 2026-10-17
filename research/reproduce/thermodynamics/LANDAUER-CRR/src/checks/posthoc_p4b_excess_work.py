"""POST HOC (written after the P4b FAIL was recorded; not part of the frozen study).
Diagnostic: for the flip drive of P4b, compare the excess work W_ex = W - dF_eq (the quantity
Sivak-Crooks linear response prices) with the heat Q that P4b's declaration used instead."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import landauer_crr as L
E = L.E
C, _ = L.path_lengths([E, -E])
rows = []
for tau in [200, 500, 1000]:
    n = L.steps_for(tau)
    ps = float(L.p_eq(E))
    W, pend = L.drive(L.constant_speed_schedule([E, -E], n), tau, ps)
    dF = float(L.F_eq(-E) - L.F_eq(E))
    Wex = W - dF
    Q = W - (pend * (-E) - ps * E)
    rows.append({"tau": tau, "Wex_tau": Wex * tau, "Wex_rel_err": Wex * tau / C**2 - 1,
                 "Q_tau": Q * tau, "Q_rel_err": Q * tau / C**2 - 1, "Wex_minus_Q_tau": (Wex - Q) * tau})
out = {"label": "POST HOC diagnostic, not a frozen prediction", "C2": C**2, "rows": rows}
json.dump(out, open(os.path.join(os.path.dirname(__file__), "..", "outputs", "posthoc_p4b_excess_work.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
