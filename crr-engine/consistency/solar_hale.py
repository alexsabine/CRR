"""P1 — Solar Hale-cycle CV reproduction from SILSO v2.0.

Predicted: CV_SO(2) = 1/(4π) ≈ 0.0796.
Reported empirical (canonical brief, citing SILSO Hale-cycle analyses):
  CV ∈ [0.0767, 0.0820].

This script downloads the SILSO v2.0 monthly mean total sunspot
number, identifies Hale-cycle peaks (22-year magnetic cycle), and
computes the empirical CV of Hale-cycle durations.

Consistency check: the predicted 0.0796 must lie within the empirical
[0.0767, 0.0820] band, and our re-derived empirical CV from raw
SILSO data must reproduce that band.

[REVIEWER-RUN] Network access to www.sidc.be is required. The campaign
sandbox blocks this host; the script is committed for unaffiliated
reviewer execution.

Why this matters in 2026+: solar-cycle phase prediction is a live
operational problem for satellite-orbit decay forecasts, GPS-error
bounds, polar-flight radiation dosimetry, and ESA / NASA
space-weather services. A parameter-free CV prediction for the Hale
cycle, if confirmed, gives a falsifiable benchmark against which
empirical solar-cycle models (NOAA SWPC, ESA's S2P) can be cross-
checked.
"""

from __future__ import annotations

import io
import math
import sys
import urllib.request

import numpy as np

PI = math.pi
SILSO_URL = "https://www.sidc.be/SILSO/DATA/SN_m_tot_V2.0.txt"


def fetch_silso() -> np.ndarray:
    """Download SILSO v2.0 monthly total sunspot number.

    Format (per SILSO documentation):
        col 1: year (int)
        col 2: month (int)
        col 3: decimal year
        col 4: monthly mean SN
        col 5: stddev
        col 6: number of obs
        col 7: provisional flag
    """
    with urllib.request.urlopen(SILSO_URL, timeout=30) as resp:
        data = resp.read().decode("ascii")
    rows = []
    for line in data.splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        try:
            decimal_year = float(parts[2])
            sn = float(parts[3])
        except ValueError:
            continue
        if sn < 0:  # SILSO uses -1 for missing
            continue
        rows.append((decimal_year, sn))
    return np.array(rows)


def find_solar_minima(decimal_year: np.ndarray, sn: np.ndarray, smooth_months: int = 13) -> np.ndarray:
    """Locate solar minima as smoothed-SN local minima within ±5 yr windows.

    The canonical Schwabe ~11-yr cycle is anchored on minima per
    Clette & Lefèvre (2016). Returns minima decimal-years.
    """
    kernel = np.ones(smooth_months) / smooth_months
    smoothed = np.convolve(sn, kernel, mode="same")
    minima = []
    half_window = 5 * 12  # 5 years in months
    for i in range(half_window, len(smoothed) - half_window):
        window = smoothed[i - half_window : i + half_window + 1]
        if smoothed[i] == window.min():
            minima.append(decimal_year[i])
    return np.array(minima)


def hale_cycle_durations(minima_years: np.ndarray) -> np.ndarray:
    """Hale = pair of Schwabe cycles. Durations between every other minimum."""
    if len(minima_years) < 3:
        return np.array([])
    return minima_years[2::2] - minima_years[:-2:2]


def main() -> int:
    print("Fetching SILSO v2.0 monthly total sunspot number ...", flush=True)
    raw = fetch_silso()
    decimal_year, sn = raw[:, 0], raw[:, 1]
    print(f"  loaded {len(decimal_year)} months: {decimal_year[0]:.3f} – {decimal_year[-1]:.3f}")

    minima = find_solar_minima(decimal_year, sn)
    print(f"  identified {len(minima)} solar minima")

    durations = hale_cycle_durations(minima)
    print(f"  {len(durations)} Hale-cycle durations: mean = {durations.mean():.2f} yr, "
          f"std = {durations.std(ddof=1):.2f} yr")
    cv_empirical = durations.std(ddof=1) / durations.mean()
    cv_predicted = 1.0 / (4.0 * PI)
    print(f"\n  Empirical CV  = {cv_empirical:.5f}")
    print(f"  Predicted CV  = {cv_predicted:.5f}  (= 1 / (4π))")
    print(f"  Brief-reported empirical band: [0.0767, 0.0820]")

    in_band = 0.0767 <= cv_empirical <= 0.0820
    pred_in_band = 0.0767 <= cv_predicted <= 0.0820
    print(f"  Empirical CV in band:  {in_band}")
    print(f"  Predicted CV in band:  {pred_in_band}")

    return 0 if (in_band and pred_in_band) else 1


if __name__ == "__main__":
    sys.exit(main())
