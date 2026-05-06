"""
P10 — Analysis script.

Pre-registered prediction (notes/session_8_new_predictions_and_applied.md,
committed prior to this analysis):

    CV_sunspot / CV_Hale ∈ [1.7, 2.3]   AND   N_full_Hale ≥ 12.

Falsifier: ratio outside [1.5, 2.5].
Null (i.i.d. sunspot cycles): ratio = √2 ≈ 1.414.

Method:
  1. Load SILSO V2 monthly mean total sunspot number.
  2. Compute 13-month centred running mean (standard SMSSN).
  3. Find sunspot-cycle minima as local minima of the SMSSN with a
     ±36-month exclusion window (suppresses spurious sub-cycle dips).
  4. Define sunspot-cycle period as min-to-min interval in years.
  5. Define Hale-cycle period as the sum of two consecutive sunspot
     cycles, paired starting from cycle 1.
  6. Compute CV (std/mean) of each.
  7. Report ratio CV_sunspot / CV_Hale and bootstrap 95% CI.

Run: python analyse.py
"""
from __future__ import annotations
import csv
import pathlib
import statistics
import math
import random

DATA = pathlib.Path(__file__).parent / "SN_m_tot_V2.0.csv"
SMOOTH_WINDOW = 13          # months — canonical SILSO smoothing
MIN_EXCLUSION = 36          # months — suppress spurious local minima
N_BOOT = 10_000             # bootstrap replicates


def load_silso() -> tuple[list[float], list[float]]:
    """Return (fractional_year, monthly_mean_SSN) lists."""
    t, ssn = [], []
    with DATA.open() as f:
        for row in csv.reader(f, delimiter=";"):
            row = [c.strip() for c in row if c.strip() != ""]
            if not row:
                continue
            t.append(float(row[2]))
            ssn.append(float(row[3]))
    return t, ssn


def running_mean(x: list[float], window: int) -> list[float]:
    """Centred running mean with NaN at the boundaries."""
    half = window // 2
    out: list[float] = [float("nan")] * len(x)
    for i in range(half, len(x) - half):
        out[i] = sum(x[i - half : i + half + 1]) / window
    return out


def find_minima(t: list[float], y: list[float], exclusion: int) -> list[float]:
    """Local minima of y (NaNs treated as +∞), with min spacing `exclusion`."""
    n = len(y)
    minima_idx: list[int] = []
    last = -10**9
    for i in range(1, n - 1):
        yi = y[i]
        if math.isnan(yi):
            continue
        # window check: min over [i-exclusion, i+exclusion]
        lo = max(0, i - exclusion)
        hi = min(n, i + exclusion + 1)
        window = [v for v in y[lo:hi] if not math.isnan(v)]
        if not window:
            continue
        if yi == min(window) and (i - last) >= exclusion:
            minima_idx.append(i)
            last = i
    return [t[i] for i in minima_idx]


def cv(xs: list[float]) -> float:
    return statistics.stdev(xs) / statistics.mean(xs)


def bootstrap_ratio(periods: list[float], n_boot: int) -> tuple[float, float]:
    """Bootstrap 95% CI for the CV-ratio statistic.

    Resampling unit: the per-cycle period (sunspot cycle). Hale periods
    are reconstructed from consecutive pairs in the resampled series.
    """
    rng = random.Random(0xC2B)
    ratios: list[float] = []
    for _ in range(n_boot):
        sample = [periods[rng.randrange(len(periods))] for _ in periods]
        if len(sample) < 4:
            continue
        hale = [sample[i] + sample[i + 1] for i in range(0, len(sample) - 1, 2)]
        if len(hale) < 2:
            continue
        try:
            r = cv(sample) / cv(hale)
        except (statistics.StatisticsError, ZeroDivisionError):
            continue
        ratios.append(r)
    ratios.sort()
    lo = ratios[int(0.025 * len(ratios))]
    hi = ratios[int(0.975 * len(ratios))]
    return lo, hi


def main() -> None:
    t, ssn = load_silso()
    print(f"Loaded {len(ssn)} monthly samples ({t[0]:.3f} → {t[-1]:.3f}).")

    smoothed = running_mean(ssn, SMOOTH_WINDOW)
    minima = find_minima(t, smoothed, MIN_EXCLUSION)
    print(f"Detected {len(minima)} sunspot-cycle minima.")

    periods = [minima[i + 1] - minima[i] for i in range(len(minima) - 1)]
    print(f"Sunspot cycles: N = {len(periods)}.")
    print(f"  mean period = {statistics.mean(periods):.3f} yr,"
          f"  std = {statistics.stdev(periods):.3f} yr,"
          f"  CV = {cv(periods):.4f}")

    hale = [periods[i] + periods[i + 1] for i in range(0, len(periods) - 1, 2)]
    print(f"Hale cycles (paired): N = {len(hale)}.")
    print(f"  mean period = {statistics.mean(hale):.3f} yr,"
          f"  std = {statistics.stdev(hale):.3f} yr,"
          f"  CV = {cv(hale):.4f}")

    ratio = cv(periods) / cv(hale)
    print(f"\nCV-ratio  CV_sunspot / CV_Hale = {ratio:.3f}")
    print(f"  CRR (M22) prediction band [1.7, 2.3]")
    print(f"  i.i.d. null (uncorrelated cycles) ≈ √2 = 1.414")
    print(f"  hard falsifier outside [1.5, 2.5]")

    lo, hi = bootstrap_ratio(periods, N_BOOT)
    print(f"  bootstrap 95% CI [{lo:.3f}, {hi:.3f}]")

    # Verdict
    in_pred = 1.7 <= ratio <= 2.3
    in_band = 1.5 <= ratio <= 2.5
    n_hale = len(hale)
    print()
    if in_pred and n_hale >= 12:
        print("VERDICT: pre-registered band met → P10 promotes to T3.")
    elif in_band:
        print("VERDICT: in non-falsifier band but outside T3 band → P10 stays at T2-marginal.")
    else:
        print("VERDICT: ratio outside falsifier band [1.5, 2.5] → P10 falsified at T1.")


if __name__ == "__main__":
    main()
