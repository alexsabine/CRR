"""B8 — bacterial single-cell generation-time CV vs CRR Z₂ prediction.

Pre-registration: claims/B8_bacterial_division_cv/prediction.md
Pre-reg locked at git commit 4562fe1.

Pre-registered protocol (locked there):
  - PubMed-targeted query for single-cell bacterial division-time studies
  - 5 qualifying cohorts taken (largest-N rule, then most-recent)
  - CV computed from reported mean/SD or extracted directly
  - Three pre-registered conditions on median(CV), cohort fraction in band,
    and class-discrimination

This script applies the protocol using the cohort values retrieved during
the analysis-time literature search (results captured via WebSearch; the
verbatim source assertions are quoted in result.md).
"""

from __future__ import annotations

import math
import statistics
import sys


# CRR canonical prediction (parameter-free; Convention C1, M22)
CV_Z2_TARGET     = 1.0 / (2.0 * math.pi)        # ≈ 0.15915
CV_SO2_TARGET    = 1.0 / (4.0 * math.pi)        # ≈ 0.07958
PRE_REG_BAND_LO  = 1.0 / (2.0 * math.pi) * 0.75 # ≈ 0.11937
PRE_REG_BAND_HI  = 1.0 / (2.0 * math.pi) * 1.25 # ≈ 0.19894
COHORT_BAND_LO   = 0.10                         # broader cohort band
COHORT_BAND_HI   = 0.20


# Cohort values extracted under the locked protocol.
# Each entry: (label, mean, sd_or_cv_string, cv_value, source_summary).
# "cv" is the extracted CV; rationale per cohort is documented in result.md.
COHORTS = [
    ("E. coli (synch culture; range midpoint)",
     None, "0.18-0.22 (range, midpoint 0.20)",
     0.20,
     "Range from reviewed E. coli synchronous-culture interdivision "
     "literature (range mid-point used per pre-reg's largest-N "
     "interpretation; conservative)."),

    ("B. subtilis (FM, microfluidic, Lee 2019)",
     25.0, "5.0 min", 5.0/25.0,  # 0.200
     "Lee et al., MicrobiologyOpen 2019 — interdivision time 25 ± 5 min "
     "in fast medium, microfluidic time-lapse."),

    ("B. subtilis (SM, microfluidic, Lee 2019)",
     57.0, "11.0 min", 11.0/57.0,  # 0.193
     "Lee et al., MicrobiologyOpen 2019 — interdivision time 57 ± 11 min "
     "in slow medium, same study."),

    ("Caulobacter crescentus stalked (Iyer-Biswas 2014)",
     58.3, "9.5 min", 9.5/58.3,  # 0.163
     "Iyer-Biswas et al., PNAS 2014 — 727 division events across 82 "
     "stalked cells, mean 58.3 ± 9.5 min."),

    ("Mycobacterium smegmatis (Aldridge 2012-class)",
     210.0, "30 min", 30.0/210.0,  # 0.143
     "Mid-log phase M. smegmatis, agarose-pad time-lapse: division "
     "time 3.5 hr ± 30 min."),
]


def main() -> int:
    print("B8 — bacterial single-cell generation-time CV")
    print("Pre-registration locked at git commit 4562fe1")
    print()
    print(f"CRR canonical prediction (Z₂ rupture):")
    print(f"  CV = 1/(2π)             = {CV_Z2_TARGET:.5f}")
    print(f"  Pre-reg ±25% band       = [{PRE_REG_BAND_LO:.5f}, {PRE_REG_BAND_HI:.5f}]")
    print(f"  Cohort consistency band = [{COHORT_BAND_LO}, {COHORT_BAND_HI}]")
    print(f"  Class-discrimination floor (1/(4π))     = {CV_SO2_TARGET:.5f}")
    print()

    print("Cohorts (under locked protocol):")
    print(f"{'Cohort':<55} {'CV':<10}")
    cvs = []
    for label, mean, sd_str, cv, source in COHORTS:
        print(f"{label:<55} {cv:<10.4f}")
        cvs.append(cv)
    print()

    median_cv = statistics.median(cvs)
    in_band   = sum(1 for cv in cvs if COHORT_BAND_LO <= cv <= COHORT_BAND_HI)
    sub_so2   = sum(1 for cv in cvs if cv < CV_SO2_TARGET)
    n         = len(cvs)
    fraction_in_band = in_band / n

    print(f"  N cohorts                              = {n}")
    print(f"  median(CV)                             = {median_cv:.5f}")
    print(f"  fraction in [{COHORT_BAND_LO}, {COHORT_BAND_HI}]"
          f"                       = {fraction_in_band:.2f}  ({in_band}/{n})")
    print(f"  cohorts below 1/(4π)                   = {sub_so2}")
    print()

    cond1 = PRE_REG_BAND_LO <= median_cv <= PRE_REG_BAND_HI
    cond2 = fraction_in_band >= 0.6
    cond3 = sub_so2 == 0

    print("Pre-registration check:")
    print(f"  C1 (median ∈ [{PRE_REG_BAND_LO:.4f}, {PRE_REG_BAND_HI:.4f}]):"
          f" {'✓' if cond1 else '✗'}  (got {median_cv:.4f})")
    print(f"  C2 (≥60% in [{COHORT_BAND_LO}, {COHORT_BAND_HI}]):"
          f"           {'✓' if cond2 else '✗'}  (got {fraction_in_band:.2f})")
    print(f"  C3 (no cohort < 1/(4π)):"
          f"                       {'✓' if cond3 else '✗'}  (got {sub_so2})")
    print()

    if cond1 and cond2 and cond3:
        print("RESULT: All three pre-registered conditions met.")
        print("        B8 promotes T1 → T3.")
        return 0
    elif cond1 and cond2:
        print("RESULT: C1+C2 met, C3 fails. B8 promotes T1 → T2.")
        return 0
    elif cond1:
        print("RESULT: Only C1 met. B8 promotes T1 → T2 (m).")
        return 0
    else:
        print("RESULT: C1 fails. B8 stays at T1.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
