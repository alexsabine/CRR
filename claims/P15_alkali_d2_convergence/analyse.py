"""
P15 — Analysis script.

Tests the pre-registered prediction (committed at git commit
14c1c84 prior to this script existing): alkali D2 f-convergence
including Francium per F_Structure.pdf §11.2.

Inputs: lifetime τ and wavelength λ of the ns₁/₂ → np₃/₂ D2
transition for {Li, Na, K, Rb, Cs, Fr}, sourced from canonical
published references (Steck D-line reviews, Simsarian 1998 for Fr).
Values are committed in the prediction.md table; this script
re-states them inline so the script is self-contained for review.

Statistic:  CV = A/(2π·ν₀), f_meas = α³/(4π·CV),
α = 1/137.035999084.

Run: python analyse.py
"""
from __future__ import annotations
import math

# ---- Physical constants ----
ALPHA = 1.0 / 137.035999084          # CODATA 2018 fine-structure constant
C_M_S = 299_792_458.0                # speed of light, m/s
A3 = ALPHA ** 3                      # ≈ 3.882e-7
PRED_F = 2.0                         # alkali f from F_Structure Table 3

# ---- Data table (verbatim from prediction.md, committed before this script) ----
# Columns: tau in ns, lambda in nm, source citation
ALKALIS = {
    # element : (tau_ns, lambda_nm, ref)
    "Li": (27.102, 670.776, "McAlexander 1996 + Steck Li D"),
    "Na": (16.299, 588.995, "Steck Sodium D Line Data"),
    "K":  (26.34,  766.701, "Steck Potassium D Line Data"),
    "Rb": (26.24,  780.241, "Steck Rubidium 87 D Line Data"),
    "Cs": (30.473, 852.347, "Steck Cesium D Line Data"),
    "Fr": (21.02,  718.184, "Simsarian PRL 80, 4346 (1998); Grossman 2000"),
}

CONVERGENT_CORE = ("K", "Rb", "Cs", "Fr")
LIGHT_DEVIANTS = ("Li", "Na")


def cv_and_f(tau_ns: float, lambda_nm: float) -> tuple[float, float]:
    """Compute CV = A/(2π·ν₀) and f_meas = α³/(4π·CV)."""
    A = 1.0 / (tau_ns * 1e-9)
    nu = C_M_S / (lambda_nm * 1e-9)
    cv = A / (2 * math.pi * nu)
    f = A3 / (4 * math.pi * cv)
    return cv, f


def main() -> None:
    print("P15 alkali D2-line f-convergence test")
    print(f"α³ = {A3:.4e}, predicted f = {PRED_F:.2f}\n")
    print(f"{'Elem':4} {'τ(ns)':>8} {'λ(nm)':>10} {'CV':>13} {'f_meas':>8} {'err%':>7}")
    print("-" * 60)

    results: dict[str, dict[str, float]] = {}
    for elem, (tau, lam, _ref) in ALKALIS.items():
        cv, f = cv_and_f(tau, lam)
        err = abs(f - PRED_F) / PRED_F * 100.0
        results[elem] = {"tau": tau, "lambda": lam, "cv": cv, "f": f, "err_pct": err}
        print(f"{elem:4} {tau:>8.3f} {lam:>10.3f} {cv:>13.4e} {f:>8.4f} {err:>6.2f}%")

    # ---- Convergent-core analysis (T3 primary criterion) ----
    core_f = [results[e]["f"] for e in CONVERGENT_CORE]
    core_f_sorted = sorted(core_f)
    n = len(core_f_sorted)
    median = (core_f_sorted[n // 2] if n % 2 == 1
              else 0.5 * (core_f_sorted[n // 2 - 1] + core_f_sorted[n // 2]))
    max_abs_err = max(abs(f - PRED_F) / PRED_F for f in core_f)

    print("\n--- Primary (T3) criterion: convergent core {K, Rb, Cs, Fr} ---")
    print(f"  median(f) = {median:.4f}   (band [1.85, 2.15])")
    print(f"  max element error = {max_abs_err*100:.2f}%   (threshold 20%)")
    print(f"  N = {len(core_f)}   (threshold 4)")

    primary_pass = (1.85 <= median <= 2.15
                    and max_abs_err <= 0.20
                    and len(core_f) >= 4)

    # ---- Secondary criterion: Francium-specific F_Structure §11.2 ----
    fr_cv = results["Fr"]["cv"]
    pred_fr_cv = A3 / (8 * math.pi)
    fr_rel_err = abs(fr_cv - pred_fr_cv) / pred_fr_cv

    print("\n--- Secondary criterion: Francium-specific F_Structure §11.2 ---")
    print(f"  predicted CV(Fr D2) = α³/(8π) = {pred_fr_cv:.4e}")
    print(f"  empirical CV(Fr D2) = {fr_cv:.4e}")
    print(f"  relative error = {fr_rel_err*100:.2f}%   (threshold 20%)")

    secondary_pass = fr_rel_err <= 0.20

    # ---- Tertiary criterion: light-s deviant cluster Li, Na ----
    print("\n--- Tertiary criterion: light-s deviants {Li, Na} ---")
    for elem in LIGHT_DEVIANTS:
        f = results[elem]["f"]
        outside_core_band = not (1.85 <= f <= 2.15)
        within_outer_bounds = 1.0 <= f <= 3.0
        print(f"  {elem}: f = {f:.4f}, outside [1.85, 2.15]? {outside_core_band}, "
              f"within [1.0, 3.0]? {within_outer_bounds}")

    tertiary_pass = all(
        (not (1.85 <= results[e]["f"] <= 2.15)) and (1.0 <= results[e]["f"] <= 3.0)
        for e in LIGHT_DEVIANTS
    )

    # ---- Falsifier check ----
    falsifier_max_err = max(abs(results[e]["f"] - PRED_F) / PRED_F for e in CONVERGENT_CORE)
    falsifier_band = 1.70 <= median <= 2.30
    falsifier_triggered = (falsifier_max_err > 0.30) or (not falsifier_band)

    # ---- Verdict ----
    print("\n" + "=" * 60)
    print(f"  Primary   (T3 promotion):  {'PASS' if primary_pass else 'FAIL'}")
    print(f"  Secondary (Fr §11.2):      {'PASS' if secondary_pass else 'FAIL'}")
    print(f"  Tertiary  (Li/Na bounded): {'PASS' if tertiary_pass else 'FAIL'}")
    print(f"  Falsifier triggered:       {'YES (P15 rejected)' if falsifier_triggered else 'NO'}")
    print("=" * 60)

    if primary_pass and secondary_pass:
        print("VERDICT: P15 promotes to T3.")
    elif primary_pass:
        print("VERDICT: P15 promotes to T2 (primary met; secondary marginal).")
    elif falsifier_triggered:
        print("VERDICT: P15 falsified at T1.")
    else:
        print("VERDICT: P15 stays at T1 (primary missed; falsifier not triggered).")


if __name__ == "__main__":
    main()
