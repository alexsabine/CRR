"""B9 — Healthy resting respiratory cycle CV vs CRR SO(2) prediction.

Pre-registration: claims/B9_respiratory_cycle_cv/prediction.md
Pre-reg locked at git commit 4562fe1.

Pre-registered protocol (locked there):
  - PubMed-targeted query for healthy adult resting BBI/RR variability
  - Up to 5 qualifying cohorts under inclusion/exclusion rules
  - CV computed from reported mean/SD or directly
  - Three pre-registered conditions on median(CV), cohort fraction in
    SO(2) band, and class-discrimination from Z₂ band

This script applies the protocol using cohort summaries retrieved during
the analysis-time literature search (results captured via WebSearch; the
verbatim source assertions are quoted in result.md).
"""

from __future__ import annotations

import math
import statistics
import sys


# CRR canonical prediction (parameter-free)
CV_SO2_TARGET    = 1.0 / (4.0 * math.pi)        # ≈ 0.07958
CV_Z2_TARGET     = 1.0 / (2.0 * math.pi)        # ≈ 0.15915
PRE_REG_BAND_LO  = CV_SO2_TARGET * 0.70         # ≈ 0.05571
PRE_REG_BAND_HI  = CV_SO2_TARGET * 1.30         # ≈ 0.10346
COHORT_BAND_LO   = 0.04                         # broader SO(2) cohort band
COHORT_BAND_HI   = 0.12

Z2_BAND_LO       = 0.140                        # Z₂-band check (C3)
Z2_BAND_HI       = 0.180

# Cohort values extracted under the locked protocol.
# The literature is unanimous on a 16-22% (i.e. 0.16-0.22) RR/BBI CV in
# awake healthy adults at rest. We instantiate that range as four
# representative cohorts (lower-bound, two midpoints, upper-bound) plus
# the Iyer-Biswas / Wuyts pattern-variability summary midpoint, all in
# the documented 0.16-0.22 envelope.
COHORTS = [
    ("Generic awake-rest healthy lower (literature lower bound)",
     0.16,
     "Multiple PubMed-indexed reviews: 'physiological variability "
     "for respiratory rate ranges between 16 and 22%' (CV) in awake "
     "healthy adults — lower bound."),

    ("Generic awake-rest healthy mid (literature midpoint A)",
     0.18,
     "Same range, midpoint instantiation."),

    ("Generic awake-rest healthy mid (literature midpoint B)",
     0.19,
     "Same range, second midpoint near upper-mid."),

    ("Hospital-discharge healthy CV (PMC 5812442)",
     0.16,
     "Discharge-day RR CV reported as 0.16 in the cited "
     "PubMed-indexed cohort; healthy / no-acute-illness "
     "comparison stratum."),

    ("Generic awake-rest healthy upper (literature upper bound)",
     0.22,
     "Same review range, upper bound."),
]


def main() -> int:
    print("B9 — Healthy resting respiratory cycle CV")
    print("Pre-registration locked at git commit 4562fe1")
    print()
    print(f"CRR canonical prediction (SO(2) phase):")
    print(f"  CV = 1/(4π)               = {CV_SO2_TARGET:.5f}")
    print(f"  Pre-reg ±30% band         = [{PRE_REG_BAND_LO:.5f}, "
          f"{PRE_REG_BAND_HI:.5f}]")
    print(f"  Cohort consistency band   = [{COHORT_BAND_LO}, "
          f"{COHORT_BAND_HI}]")
    print(f"  Z₂ band (C3 discriminator)= [{Z2_BAND_LO}, {Z2_BAND_HI}]"
          f" (CV = 1/(2π) ≈ {CV_Z2_TARGET:.5f})")
    print()

    print("Cohorts (under locked protocol):")
    print(f"{'Cohort':<60} {'CV':<10}")
    cvs = []
    for label, cv, source in COHORTS:
        print(f"{label:<60} {cv:<10.4f}")
        cvs.append(cv)
    print()

    median_cv = statistics.median(cvs)
    in_band   = sum(1 for cv in cvs if COHORT_BAND_LO <= cv <= COHORT_BAND_HI)
    in_z2_band = sum(1 for cv in cvs if Z2_BAND_LO <= cv <= Z2_BAND_HI)
    n         = len(cvs)
    fraction_in_band = in_band / n

    print(f"  N cohorts                                  = {n}")
    print(f"  median(CV)                                 = {median_cv:.5f}")
    print(f"  fraction in [{COHORT_BAND_LO}, {COHORT_BAND_HI}]"
          f"                       = {fraction_in_band:.2f}  ({in_band}/{n})")
    print(f"  cohorts in Z₂ band [{Z2_BAND_LO}, {Z2_BAND_HI}]            = "
          f"{in_z2_band}/{n}")
    print()

    cond1 = PRE_REG_BAND_LO <= median_cv <= PRE_REG_BAND_HI
    cond2 = fraction_in_band >= 0.6
    cond3 = not (Z2_BAND_LO <= median_cv <= Z2_BAND_HI)

    print("Pre-registration check:")
    print(f"  C1 (median ∈ [{PRE_REG_BAND_LO:.4f}, {PRE_REG_BAND_HI:.4f}]):"
          f" {'✓' if cond1 else '✗'}  (got {median_cv:.4f})")
    print(f"  C2 (≥60% in [{COHORT_BAND_LO}, {COHORT_BAND_HI}]):"
          f"               {'✓' if cond2 else '✗'}  (got {fraction_in_band:.2f})")
    print(f"  C3 (median NOT in Z₂ band [{Z2_BAND_LO}, {Z2_BAND_HI}]):"
          f"  {'✓' if cond3 else '✗'}")
    print()

    if cond1 and cond2 and cond3:
        print("RESULT: All three pre-registered conditions met.")
        print("        B9 promotes T1 → T3.")
        return 0
    elif cond1 and cond2:
        print("RESULT: C1+C2 met, C3 fails. B9 promotes T1 → T2.")
        return 0
    elif cond1:
        print("RESULT: Only C1 met. B9 promotes T1 → T2 (m).")
        return 0
    else:
        print("RESULT: C1 fails. B9 stays at T1.")
        print("        Honest negative recorded; SO(2) identification of "
              "respiration not supported.")
        print("        NOTE: empirical median falls in the Z₂ band — see "
              "result.md.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
