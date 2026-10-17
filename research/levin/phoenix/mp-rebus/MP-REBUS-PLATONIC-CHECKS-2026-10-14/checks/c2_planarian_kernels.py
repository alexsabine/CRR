#!/usr/bin/env python3
"""C2: three memory kernels against the planarian record (SEEN summary statistics; R5; retrodictive).

Data (DATA/SEEN.md rows levin-lab/*; Durant et al. 2017; Emmons-Bell et al. 2015):
  DH recut: 100/100 and 102/102 DH over three generations.
  cryptic recut: 23 % DH (N=155); 27 % after two rounds (8/30, read as 0.27*30 rounded).
  SCH-28080 reset: 34 % to stable single-headed (N=102), persisting >= 4 generations.
  head shape: remodels toward wild type by day 30 (no fraction in the text; retention <= 0.5 per cycle assumed, conservative).
2a: exact one-sided 95 % lower bound on per-round retention rho from k/k over three rounds (Clopper-Pearson on rho^3).
2b: Polya drift on the cryptic cohort: exact binomial test of 8/30 against 0.23; n per round for 80 % power at +0.04 and +0.10.
2c: an access-weighted kernel (MP P9) vs age-only: can one (q, a) reproduce DH retention >= bound and head-shape retention <= 0.5?
numpy only.
"""
import json, math, pathlib
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)


def binom_pmf(k, n, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)


def binom_sf(k, n, p):  # P(X >= k)
    return sum(binom_pmf(j, n, p) for j in range(k, n + 1))


def lower_bound_p_all_success(n, alpha=0.05):
    # one-sided 95 % lower bound on p when n/n successes: p_L = alpha^(1/n)
    return alpha ** (1.0 / n)


def check_2a():
    out = {}
    for n in (100, 102):
        p3_L = lower_bound_p_all_success(n)       # bound on rho^3 (three generations)
        rho_L = p3_L ** (1.0 / 3.0)
        out[f"n{n}"] = {"lower_bound_rho3": p3_L, "lower_bound_rho_per_round": rho_L}
    head_shape_retention_upper = 0.5
    out["head_shape_retention_upper_assumed"] = head_shape_retention_upper
    out["one_q_fits_both"] = bool(min(v["lower_bound_rho_per_round"] for k, v in out.items() if k.startswith("n")) <= head_shape_retention_upper)
    return out


def check_2b():
    p0, k, n = 0.23, 8, 30
    p_one_sided = binom_sf(k, n, p0)
    # power for one-sided exact test at alpha 0.05 against p1 = p0 + d, as a function of n
    def power(n, d, alpha=0.05):
        # critical k: smallest k with P(X>=k | p0) <= alpha
        kc = next(kk for kk in range(n + 1) if binom_sf(kk, n, p0) <= alpha)
        return binom_sf(kc, n, p0 + d)
    need = {}
    for d in (0.04, 0.10):
        nn = 30
        while power(nn, d) < 0.80 and nn < 20000:
            nn += 10
        need[f"d{d}"] = nn
    return {"observed": f"{k}/{n}", "p0": p0, "p_one_sided_exact": p_one_sided,
            "rejects_stationarity_at_0.05": bool(p_one_sided < 0.05), "n_per_round_for_80pct_power": need}


def check_2c(rho_bound):
    # kernel weight on the DH-state occasion after r rounds, relative to a competing wild-type attractor seeded at weight 1:
    # age-only: w_r = q^r ; access-weighted (P9-like): w_r = q^r * (1 + a*r) (the state is re-written at each recut).
    # retention per round is modelled as w_r / (w_r + (1-w_r)) collapsed to w_r for a two-attractor readout: retention_r = w_r / (w_r + c),
    # with c = 1 - w_0 ... simplest: require w_r >= rho_bound^r for DH (re-accessed, a>0) and w_1 <= 0.5 for head shape (never re-accessed, accesses=0).
    best = None
    grid_q = np.linspace(0.05, 0.999, 400)
    grid_a = np.linspace(0.0, 50.0, 501)
    feasible = []
    for q in grid_q:
        head_ok = q <= 0.5                      # head shape: accesses = 0 -> w_1 = q
        if not head_ok:
            continue
        for a in grid_a:
            dh_ok = all(q ** r * (1 + a * r) >= rho_bound ** r for r in (1, 2, 3))
            if dh_ok:
                feasible.append((float(q), float(a)))
                break
    age_only_feasible = any(q <= 0.5 and all(q ** r >= rho_bound ** r for r in (1, 2, 3)) for q in grid_q)
    return {"rho_bound_used": rho_bound, "age_only_feasible": bool(age_only_feasible),
            "access_weighted_feasible": bool(len(feasible) > 0),
            "example_feasible_q_a": feasible[0] if feasible else None,
            "n_feasible_q_values": len(feasible)}


def main():
    a = check_2a()
    rho_bound = min(v["lower_bound_rho_per_round"] for k, v in a.items() if k.startswith("n"))
    b = check_2b()
    c = check_2c(rho_bound)
    r = {"check_2a": a, "check_2b": b, "check_2c": c}
    (OUT / "c2_planarian_kernels.json").write_text(json.dumps(r, indent=1))
    lines = [
        "C2 — memory kernels against the planarian record (SEEN; R5; retrodictive)",
        f"2a DH persistence: 95 % lower bound on per-round retention rho = {a['n100']['lower_bound_rho_per_round']:.4f} (n=100), {a['n102']['lower_bound_rho_per_round']:.4f} (n=102); "
        f"head-shape retention assumed <= {a['head_shape_retention_upper_assumed']}; one q fits both: {a['one_q_fits_both']}",
        f"2b Polya drift on the cryptic cohort: observed {b['observed']} vs 0.23, one-sided exact p = {b['p_one_sided_exact']:.3f}; rejects stationarity: {b['rejects_stationarity_at_0.05']}; "
        f"n per round for 80 % power: {b['n_per_round_for_80pct_power']}",
        f"2c access-weighted kernel (MP P9): age-only feasible: {c['age_only_feasible']}; access-weighted feasible: {c['access_weighted_feasible']} "
        f"(example q, a = {c['example_feasible_q_a']}; {c['n_feasible_q_values']} feasible q values)",
        "Grade (declared rule): 2a -> one-q age kernel WRONG as a universal; 2b -> precedence NOT EXCLUDED at the registered n (corrects DATA_ACCESS.md section 2); "
        "2c -> MP's access rule compatible (REDUNDANT-DOMAIN for Levin's bistable model); CRR's kernel would need an access term it lacks.",
    ]
    (OUT / "c2_planarian_kernels.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
