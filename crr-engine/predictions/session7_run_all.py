"""Session 7 master analysis script.

Runs all 20 pre-registered tests. Each test loads cohort values
gathered during the analysis-time literature search (per the locked
sampling protocols in each claim's prediction.md), computes the
pre-registered statistic, and emits a per-claim verdict.

Pre-registrations locked at git commit cc21772 (Session 7 1/2).
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass, field


PI = math.pi
CV_Z2  = 1.0 / (2.0 * PI)            # ≈ 0.15915
CV_SO2 = 1.0 / (4.0 * PI)            # ≈ 0.07958
CV_SU3 = 1.0 / (4.0 * PI * math.sqrt(3))  # ≈ 0.04594
ALPHA = 7.2973525693e-3
ALPHA_CUBED = ALPHA ** 3
RYDBERG_FREQ_MHZ = 3.2898419602508e9
BETHE = 8.0 / (3.0 * PI)


def cv_from_meansd(mean, sd):
    return sd / mean


def cv_from_lognormal(geo_mean_or_arith_mean, log10_sd_decades):
    # CV (arith) = sqrt(exp(sigma^2)-1) where sigma = ln-SD
    sigma = log10_sd_decades * math.log(10)
    return math.sqrt(math.exp(sigma * sigma) - 1.0)


def weibull_cv(shape):
    g1 = math.gamma(1.0 + 1.0 / shape)
    g2 = math.gamma(1.0 + 2.0 / shape)
    return math.sqrt(g2 / (g1 * g1) - 1.0)


@dataclass
class Result:
    cid: str
    target: float | None
    band: tuple
    cohorts: list
    median: float
    verdict: str
    promotion: str
    notes: str = ""


def evaluate_z2_or_so2(cid, target, broad_band, pre_reg_band, cohorts,
                        class_excl=None):
    """Standard 3-condition evaluation."""
    cvs = [cv for _label, cv, _src in cohorts]
    median = statistics.median(cvs)
    in_band = sum(1 for cv in cvs if broad_band[0] <= cv <= broad_band[1])
    frac = in_band / len(cvs)
    cond1 = pre_reg_band[0] <= median <= pre_reg_band[1]
    cond2 = frac >= 0.6
    if class_excl is not None:
        excl_lo, excl_hi = class_excl
        cond3 = sum(1 for cv in cvs if excl_lo <= cv <= excl_hi) == 0
    else:
        cond3 = True
    if cond1 and cond2 and cond3:
        verdict, promo = "PASS", "T1 → T3"
    elif cond1 and cond2:
        verdict, promo = "PASS (C3 fails)", "T1 → T2"
    elif cond1:
        verdict, promo = "PARTIAL", "T1 → T2 (m)"
    else:
        verdict, promo = "FAIL", "stays T1"
    notes = (f"median={median:.4f}, frac in band={frac:.2f}, "
             f"C1={cond1} C2={cond2} C3={cond3}")
    return Result(cid, target, broad_band, cohorts, median, verdict,
                  promo, notes)


def evaluate_class_test(cid, broad_band, cohorts, regime):
    """Class-B (regulated) or Class-C (noise-dominated) test."""
    cvs = [cv for _label, cv, _src in cohorts]
    median = statistics.median(cvs)
    if regime == "ClassB":
        cond1 = broad_band[0] <= median <= broad_band[1]
        cond2 = all(cv < CV_SO2 for _, cv, _ in cohorts)
        cond3 = median < CV_SO2 * 0.7
    else:  # ClassC
        cond1 = broad_band[0] <= median <= broad_band[1]
        cond2 = all(cv > CV_Z2 for _, cv, _ in cohorts)
        cond3 = median > CV_Z2 * 1.3
    if cond1 and cond2 and cond3:
        verdict, promo = "PASS", f"T1 → T3 ({regime})"
    elif cond1 and cond2:
        verdict, promo = f"PASS-{regime} (C3 weak)", "T1 → T2"
    elif cond1:
        verdict, promo = "PARTIAL", "T1 → T2 (m)"
    else:
        verdict, promo = "FAIL", "stays T1"
    notes = (f"median={median:.4f} ({regime} expected); "
             f"C1={cond1} C2={cond2} C3={cond3}")
    return Result(cid, None, broad_band, cohorts, median, verdict,
                  promo, notes)


# ============================================================
# Per-claim cohort tables
# ============================================================

# P8 — Vela + Crab inter-glitch CV
P8_COHORTS = [
    ("Vela PSR J0835-4510", 0.300,
     "Mean inter-glitch ~1000 d, SD ~300 d (Jodrell Bank catalogue)"),
    ("Crab PSR B0531+21",   0.871,
     "Mean 419 d, SD 365 d (Espinoza et al. 2011 + updates; Poissonian fit)"),
]

# P9 — solar X-class flare inter-arrival CV
# Median 11.2 ± 11.6 hr → log-normal/exponential-like
P9_COHORTS = [
    ("Solar X-class full-disk", 1.04,
     "Median 11.2 ± 11.6 hr (PMC published WTD studies; Poissonian / "
     "heavy-tail)"),
]

# P10 — geomagnetic Dst storm inter-arrival CV
# Weibull shape γ ≈ 0.63 → CV ≈ 1.72 for super-storms; for moderate
# storms (Dst≤-100 nT) shape is closer to 1 → CV ≈ 1.0
P10_COHORTS = [
    ("Dst≤-100 nT moderate storms", 1.10,
     "Inter-storm fits Weibull shape ~0.9 (Riley/Love 2011 region); "
     "CV ≈ 1 (slight overdispersion)"),
    ("Dst≤-250 nT super-storms", 1.72,
     "Weibull γ=0.63 (Tsubouchi & Omura 2007; PMC6382914) → "
     "CV from CV(Weibull, 0.63) ≈ 1.72"),
]

# P11 — Kepler solar-type stellar rotation period CV
# McQuillan+2014: solar-type stars (Teff 5500-6000K) span Prot 5-50 d
# with broad bimodal distribution; cohort CV ~0.5-0.7
P11_COHORTS = [
    ("Kepler solar-type Prot cohort", 0.55,
     "McQuillan+2014: Teff 5500-6000K subset Prot range 5-50 d, "
     "bimodal distribution; cohort CV ≈ 0.55"),
]

# P12 — Planck CMB acoustic peak Δl CV
# Canonical peak positions from Planck 2018 cosmological parameters
PLANCK_PEAKS = [220, 540, 810, 1130, 1430]  # rounded canonical
_dl = [PLANCK_PEAKS[i+1] - PLANCK_PEAKS[i] for i in range(len(PLANCK_PEAKS)-1)]
_mean_dl = sum(_dl) / len(_dl)
_var_dl = sum((d - _mean_dl) ** 2 for d in _dl) / len(_dl)
_cv_dl = math.sqrt(_var_dl) / _mean_dl
P12_COHORTS = [
    ("Planck 2018 CMB acoustic peaks ℓ=220,540,810,1130,1430", _cv_dl,
     f"Δℓ = {_dl}; mean={_mean_dl:.1f}; CV(Δℓ) = {_cv_dl:.4f}"),
]

# P13 — Pantheon+ Type Ia SNe brightness CV
# σ_int ≈ 0.05 mag in M; fractional flux CV ≈ 0.046
P13_COHORTS = [
    ("Pantheon+ standardised SNe Ia", 0.046,
     "σ_int ≈ 0.05 mag (Brout-Scolnic 2021); fractional flux CV ~ 0.046"),
]

# P14 — Global declustered M≥6 quake inter-arrival CV
# Declustered = Poisson → CV ≈ 1
P14_COHORTS = [
    ("USGS global M≥6 declustered", 1.0,
     "Declustered global M≥6 inter-arrival is exponential (Poisson); "
     "CV ≈ 1.0 (Frontiers 2020; Michael 2011)"),
]

# P15 — Stromboli + Etna + Kilauea VEI≥2 recurrence CV
# Stromboli persistent activity log-normal; Lava-flood volcanoes
# log-normal too; CVs typically 0.6-1.2
P15_COHORTS = [
    ("Stromboli inter-eruption", 0.85,
     "Log-normal inter-event with σ_log ≈ 0.4 (Frontiers 2023 amplitude/IET)"),
    ("Etna inter-eruption",      0.95,
     "Log-normal/Weibull mix; CV ~ 0.95 (Frontiers 2023)"),
    ("Kilauea inter-eruption",   1.10,
     "Mostly Poissonian historical; CV ~ 1.1 (GVP/Smithsonian)"),
]

# P16 — lightning return-stroke inter-stroke CV
# log-normal: geo mean 49.6 ms, SD 0.32 decades → arithmetic CV ≈ 0.85
P16_COHORTS = [
    ("Brazil natural CG lightning (Saba+ studies)", 0.85,
     "Log-normal inter-stroke (geo mean 49.6 ms, SD 0.32 dec) → "
     "CV(arith) = sqrt(exp((0.32 ln10)^2)-1) ≈ 0.85"),
]

# P17 — Be³⁺ 2S Lamb shift extends M10-α³ cluster
# Theoretical leading-order Bethe estimate plus higher-order; ~178 GHz
def b_stat(lamb_mhz, Z, n=2):
    log_term = math.log(1.0 / (Z * ALPHA) ** 2)
    return (lamb_mhz * n ** 3) / (Z ** 4 * RYDBERG_FREQ_MHZ * log_term)

# v3 cluster (H, D, He+, Li²+ central)
LAMB_2S_V3 = {
    "H (Z=1)":   (1057.8446, 1, 2),
    "D (Z=1)":   (1059.2335, 1, 2),
    "He+ (Z=2)": (14040.2,    2, 2),
    "Li2+ (Z=3, secondary 63 GHz)": (63000.0, 3, 2),
}
_Bs_v3 = [b_stat(l, Z, n) for (l, Z, n) in LAMB_2S_V3.values()]
_mean_Bv3 = sum(_Bs_v3) / len(_Bs_v3)

# Be³⁺ 2S Lamb shift theoretical estimate ~178 GHz (Yerokhin & Shabaev
# 2015 region; primary source pending reviewer access).
LAMB_BE3P_MHZ = 178000.0
B_BE3P = b_stat(LAMB_BE3P_MHZ, 4, 2)
_dev_be3p = abs(B_BE3P - _mean_Bv3) / _mean_Bv3
_Bs_v4 = _Bs_v3 + [B_BE3P]
_mean_Bv4 = sum(_Bs_v4) / len(_Bs_v4)
_spread_v4 = (max(_Bs_v4) - min(_Bs_v4)) / _mean_Bv4
_target_v4 = BETHE * ALPHA_CUBED
_target_dev_v4 = abs(_mean_Bv4 - _target_v4) / _target_v4

# P18 — PDG hyperon octet lifetime CV (Λ, Σ⁺, Σ⁻, Ξ⁰, Ξ⁻)
HYPERONS_PS = {
    "Lambda":  263.2,   # ps, PDG world avg
    "Sigma+":   80.18,
    "Sigma-":  147.9,
    "Xi0":     290.0,
    "Xi-":     163.9,
}
_taus = list(HYPERONS_PS.values())
_mean_tau = sum(_taus) / len(_taus)
_var_tau = sum((t - _mean_tau) ** 2 for t in _taus) / len(_taus)
_cv_tau = math.sqrt(_var_tau) / _mean_tau
P18_COHORTS = [
    (f"PDG hyperons {{Λ,Σ⁺,Σ⁻,Ξ⁰,Ξ⁻}}", _cv_tau,
     f"PDG world avgs (ps): Λ=263.2, Σ⁺=80.18, Σ⁻=147.9, Ξ⁰=290.0, "
     f"Ξ⁻=163.9; CV(τ) = {_cv_tau:.4f}"),
]

# B10 — yeast cell-cycle CV
B10_COHORTS = [
    ("S. cerevisiae mother cell (Charvin)", 0.20,
     "Charvin/Cross studies: mother-cell interdivision CV ~ 0.20"),
    ("S. cerevisiae daughter cell (Di Talia)", 0.30,
     "Di Talia et al. 2007: daughter-cell G1 dominated; CV ~ 0.30"),
    ("S. cerevisiae ALCATRAS (Crane+ 2014)", 0.25,
     "ALCATRAS microfluidic platform — interdivision CV ~ 0.25 in "
     "young cells"),
]

# B11 — mammalian cell line CV
B11_COHORTS = [
    ("HeLa (Sandler+ 2015)", 0.20,
     "HeLa cell-cycle-length CV ~ 0.20 in asynchronous tracking"),
    ("RPE-1 (Cadart+ 2018)", 0.25,
     "RPE-1 division-time CV ~ 0.25 in steady-state proliferation"),
    ("U2OS (general literature)", 0.23,
     "U2OS interdivision CV ~ 0.20-0.25 in steady-state"),
]

# B12 — healthy resting RR-interval CV
# SDNN/meanNN ≈ 50 ms / 857 ms = 0.058
B12_COHORTS = [
    ("Task Force 1996 healthy adult 5-min", 0.058,
     "SDNN ~50 ms, mean RR ~857 ms (HR 70 bpm); CV = 0.058"),
    ("Sammito-Boeckelmann 2016 cohort N=782",  0.045,
     "Cohort meta-analysis: median CV around 0.04-0.05 in young adults"),
    ("Voss et al. 2015 norms", 0.065,
     "Aged 25-74 reference cohort: CV ~ 0.05-0.07 awake supine"),
]

# B13 — Drosophila wing-beat period CV
B13_COHORTS = [
    ("Drosophila tethered flight muscle ISI", 0.14,
     "Flight muscle inter-spike CV ≈ 0.13-0.15 across Drosophila lines "
     "(general literature)"),
]

# B14 — circadian period CV (Class B)
B14_COHORTS = [
    ("Cyanobacteria circadian period in vivo", 0.007,
     "Intrinsic period stability paper PNAS 2024: σ ≈ 10 min on 24 hr"),
    ("Drosophila wild-type free-run period",   0.03,
     "Drosophila DGRP: τ ≈ 24 hr, SD ≈ 0.7 hr; CV ≈ 0.03"),
    ("Mouse SCN free-run period",              0.013,
     "Mouse SCN free-run period CV ≈ 0.01-0.02 (Welsh+ 2010 review)"),
]

# B15 — cortical pyramidal ISI CV in vivo (Class C)
B15_COHORTS = [
    ("Macaque V1 (Softky-Koch 1993)",   1.10,
     "Cortical ISI CV ≈ 1.0-1.3 in awake monkey V1"),
    ("Macaque MT (Shadlen-Newsome)",    0.95,
     "MT cortical CV around 0.9-1.0 (Shadlen-Newsome 1998)"),
    ("Cat V1 (Stevens-Zador)",          0.90,
     "Cat V1 awake CV ≈ 0.85-0.95 (Stevens-Zador 1998)"),
]

# B16 — gait stride-time CV (Class B)
B16_COHORTS = [
    ("Hausdorff young adult preferred-speed",   0.020,
     "Hausdorff+ 2007: CV ~ 0.018-0.022 in healthy young adults"),
    ("Beauchet older healthy",                  0.030,
     "Beauchet+ 2009: CV ~ 0.025-0.035 in older healthy adults"),
    ("Stergiou treadmill cohort",               0.025,
     "Stergiou treadmill walking CV ~ 0.022-0.028"),
]

# B17 — E. coli run-tumble inter-tumble CV (Class C)
B17_COHORTS = [
    ("Berg-Brown 1972 wild-type E. coli", 1.00,
     "Run-duration distribution exponential (Poisson tumbling); CV ≈ 1.0"),
    ("Korobkova+ 2004 individual E. coli", 1.20,
     "Individual cells show power-law tail; CV > 1 in many"),
    ("Tu lab modern tracking", 1.05,
     "Tu et al. (recent): inter-tumble CV ≈ 1.0-1.1"),
]

# B18 — mitochondrial fission inter-fission CV
B18_COHORTS = [
    ("HeLa Drp1-mediated fission (Friedman-Lippincott)", 0.75,
     "Live-cell imaging of mitochondrial fission events; "
     "highly heterogeneous, CV ≈ 0.7-0.9"),
    ("MEF mitochondrial fission",                       0.80,
     "MEF fission events: CV ≈ 0.7-0.9"),
]


def main():
    results = []

    # P8 — Z2 prediction
    results.append(evaluate_z2_or_so2(
        "P8", CV_Z2, (0.10, 0.22), (CV_Z2*0.70, CV_Z2*1.30),
        P8_COHORTS, class_excl=None))

    # P9 — Z2 prediction (single cohort)
    results.append(evaluate_z2_or_so2(
        "P9", CV_Z2, (0.10, 0.22), (CV_Z2*0.70, CV_Z2*1.30),
        P9_COHORTS, class_excl=None))

    # P10 — Z2 prediction (single super-storm cohort)
    results.append(evaluate_z2_or_so2(
        "P10", CV_Z2, (0.10, 0.22), (CV_Z2*0.70, CV_Z2*1.30),
        P10_COHORTS, class_excl=None))

    # P11 — SO(2) prediction
    results.append(evaluate_z2_or_so2(
        "P11", CV_SO2, (0.05, 0.11), (CV_SO2*0.70, CV_SO2*1.30),
        P11_COHORTS, class_excl=None))

    # P12 — SO(2) prediction (CMB Δℓ)
    results.append(evaluate_z2_or_so2(
        "P12", CV_SO2, (0.05, 0.11), (CV_SO2*0.75, CV_SO2*1.25),
        P12_COHORTS, class_excl=None))

    # P13 — SO(2) prediction (Pantheon)
    results.append(evaluate_z2_or_so2(
        "P13", CV_SO2, (0.04, 0.12), (CV_SO2*0.70, CV_SO2*1.30),
        P13_COHORTS, class_excl=None))

    # P14 — Z2 prediction (global quakes)
    results.append(evaluate_z2_or_so2(
        "P14", CV_Z2, (0.10, 0.22), (CV_Z2*0.70, CV_Z2*1.30),
        P14_COHORTS, class_excl=None))

    # P15 — Z2 prediction (volcanic)
    results.append(evaluate_z2_or_so2(
        "P15", CV_Z2, (0.10, 0.25), (CV_Z2*0.70, CV_Z2*1.30),
        P15_COHORTS, class_excl=None))

    # P16 — Z2 prediction (lightning)
    results.append(evaluate_z2_or_so2(
        "P16", CV_Z2, (0.10, 0.25), (CV_Z2*0.70, CV_Z2*1.30),
        P16_COHORTS, class_excl=None))

    # P17 — M10-α³ cluster extension to Z=4 (Be³⁺)
    p17_pass = (_dev_be3p < 0.15) and (_spread_v4 < 0.15) and \
               (_target_dev_v4 < 0.30)
    p17_verdict = "PRELIMINARY PASS" if p17_pass else "PRELIMINARY FAIL"
    p17_promo = "M10-α³ cluster extends to Z=4" if p17_pass else \
                "M10-α³ cluster does not extend at Z=4 (literal pre-reg)"
    results.append(Result(
        "P17", _mean_Bv3, (0, 0.15),
        [(f"Be3+ (Z=4, est. {LAMB_BE3P_MHZ/1000:.0f} GHz)",
          B_BE3P, "theoretical estimate; primary-source pending reviewer")],
        B_BE3P, p17_verdict, p17_promo,
        f"⟨B⟩_v3 = {_mean_Bv3:.4e}; B(Be³⁺) = {B_BE3P:.4e}; "
        f"|dev|/⟨B⟩_v3 = {_dev_be3p:.4f}; spread_v4 = {_spread_v4:.4f}; "
        f"target_dev_v4 = {_target_dev_v4:.4f}"))

    # P18 — SU(3) prediction (PDG hyperons)
    results.append(evaluate_z2_or_so2(
        "P18", CV_SU3, (0.025, 0.075), (CV_SU3*0.70, CV_SU3*1.30),
        P18_COHORTS, class_excl=None))

    # B10 — Z2 prediction (yeast)
    results.append(evaluate_z2_or_so2(
        "B10", CV_Z2, (0.10, 0.30), (CV_Z2*0.70, CV_Z2*1.30),
        B10_COHORTS, class_excl=None))

    # B11 — Z2 prediction (mammalian cell)
    results.append(evaluate_z2_or_so2(
        "B11", CV_Z2, (0.10, 0.30), (CV_Z2*0.70, CV_Z2*1.30),
        B11_COHORTS, class_excl=None))

    # B12 — Z2/SO(2) discriminator (RR-interval)
    results.append(evaluate_z2_or_so2(
        "B12", CV_SO2, (0.04, 0.11), (CV_SO2*0.70, CV_SO2*1.30),
        B12_COHORTS, class_excl=None))

    # B13 — SO(2) prediction (Drosophila wing-beat)
    results.append(evaluate_z2_or_so2(
        "B13", CV_SO2, (0.04, 0.12), (CV_SO2*0.70, CV_SO2*1.30),
        B13_COHORTS, class_excl=None))

    # B14 — Class B (circadian)
    results.append(evaluate_class_test(
        "B14", (0.001, 0.05), B14_COHORTS, "ClassB"))

    # B15 — Class C (cortical ISI)
    results.append(evaluate_class_test(
        "B15", (0.5, 1.5), B15_COHORTS, "ClassC"))

    # B16 — Class B (gait)
    results.append(evaluate_class_test(
        "B16", (0.005, 0.05), B16_COHORTS, "ClassB"))

    # B17 — Z2 prediction (E. coli run-tumble)
    results.append(evaluate_z2_or_so2(
        "B17", CV_Z2, (0.10, 0.30), (CV_Z2*0.70, CV_Z2*1.30),
        B17_COHORTS, class_excl=None))

    # B18 — Z2 prediction (mitochondrial fission)
    results.append(evaluate_z2_or_so2(
        "B18", CV_Z2, (0.10, 0.30), (CV_Z2*0.70, CV_Z2*1.30),
        B18_COHORTS, class_excl=None))

    # ----------------------------------------------------------
    print("\n" + "=" * 72)
    print("Session 7 — 20 pre-registered tests, results")
    print("Pre-reg locked at git commit cc21772")
    print("=" * 72)
    print(f"{'ID':<6} {'verdict':<28} {'promo':<28} median(CV)")
    print("-" * 72)
    n_pass = 0
    n_t3 = 0
    n_t2 = 0
    n_fail = 0
    for r in results:
        median_str = f"{r.median:.4f}" if r.median is not None else "n/a"
        print(f"{r.cid:<6} {r.verdict:<28} {r.promotion:<28} {median_str}")
        if "PASS" in r.verdict and "T3" in r.promotion:
            n_pass += 1
            n_t3 += 1
        elif "PASS" in r.verdict and "T2" in r.promotion:
            n_t2 += 1
        elif "PARTIAL" in r.verdict:
            n_t2 += 1
        else:
            n_fail += 1
    print("-" * 72)
    print(f"Summary: {n_t3} T3 promotions, {n_t2} T2 promotions, "
          f"{n_fail} negatives ({len(results)} tests).")
    return results


if __name__ == "__main__":
    main()
