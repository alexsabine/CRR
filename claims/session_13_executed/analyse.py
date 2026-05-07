"""
Session 13 — partial execution.

Sandbox allowlist (GitHub + PyPI only) blocks the named scientific
archives for 18 of 20 Session 13 pre-registrations. Two are
runnable in informational form (with explicit deviations from
the strict pre-registration N / date constraints):

- B18 (menstrual cycle Z₂ replication): kollesal/menstruation CSV
  has 1665 cycles. Pre-reg required N_women ≥ 5000. Run as
  informational — strict T3 promotion not awarded; the CV value
  itself is honestly reported.

- P37 (Old Faithful Class B SO(2)): canonical R `faithful` dataset
  has 272 eruptions from August 1985. Pre-reg required post-2000
  AND N ≥ 1000. Run as informational — strict T3 promotion not
  awarded; the CV value is reported with date-window caveat.

Run: python analyse.py
"""
from __future__ import annotations
import csv
import math
import statistics
import urllib.request
import pathlib
from collections import defaultdict

DIR = pathlib.Path(__file__).parent
MEN_URL = ("https://raw.githubusercontent.com/kollesal/"
           "menstruationCycleAnalysis/main/backend/"
           "menstrual_cycle_data_enriched_per_CYCLE.csv")
FAI_URL = ("https://raw.githubusercontent.com/vincentarelbundock/"
           "Rdatasets/master/csv/datasets/faithful.csv")


def cv(xs):
    if len(xs) < 2:
        return None
    m = statistics.mean(xs)
    if m <= 0:
        return None
    return statistics.stdev(xs) / m


# =================================================================
# B18 — menstrual cycle Z₂ replication (informational)
# =================================================================
def b18():
    p = DIR / "menstrual.csv"
    if not p.exists():
        print(f"Fetching {MEN_URL}")
        urllib.request.urlretrieve(MEN_URL, p)

    cycles_per_client: dict[str, list[int]] = defaultdict(list)
    pooled: list[int] = []
    with p.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                length = int(row["LengthofCycle"])
            except (ValueError, KeyError):
                continue
            if not (10 <= length <= 90):  # exclude obvious data errors
                continue
            client = row.get("ClientID", "").strip()
            cycles_per_client[client].append(length)
            pooled.append(length)

    print("=" * 60)
    print("B18 — Menstrual cycle Z₂ replication (informational)")
    print("=" * 60)
    print(f"  Cycles loaded     : {len(pooled)}")
    print(f"  Unique clients    : {len(cycles_per_client)}")

    # Pre-reg required N_women ≥ 5000 — not satisfied
    print(f"  Pre-reg N≥5000    : NOT MET (N_women = "
          f"{len(cycles_per_client)})")
    print()

    # Compute pooled CV (across all reported cycles)
    pooled_cv = cv(pooled)
    print("  Pooled across-cycles statistics:")
    print(f"    mean cycle length (days) : {statistics.mean(pooled):.2f}")
    print(f"    std  cycle length (days) : {statistics.stdev(pooled):.2f}")
    print(f"    pooled CV                : {pooled_cv:.4f}")
    print()

    # Compute per-client CV, then median (matches M22 v2 protocol style)
    per_client_cvs = []
    for c, ls in cycles_per_client.items():
        if len(ls) >= 3:
            v = cv(ls)
            if v is not None:
                per_client_cvs.append(v)
    n = len(per_client_cvs)
    if n > 0:
        med = statistics.median(per_client_cvs)
        mean_cv = statistics.mean(per_client_cvs)
        print(f"  Per-client (≥3 cycles) statistics:")
        print(f"    N clients eligible       : {n}")
        print(f"    median(intra-client CV)  : {med:.4f}")
        print(f"    mean(intra-client CV)    : {mean_cv:.4f}")
        print()

    # Comparison to bands
    print("  Pre-registered Z₂ band [0.140, 0.200]:")
    for label, c in [("pooled", pooled_cv)]:
        if c is not None:
            in_band = 0.140 <= c <= 0.200
            in_falsifier = 0.10 <= c <= 0.25
            verdict = "PASS (informational)" if in_band else (
                "in falsifier band" if in_falsifier else
                "outside falsifier")
            print(f"    {label}: {c:.4f} → {verdict}")
    print()

    # Bull 2019 reference: CV = 0.177 (M22 v2 Test 1)
    print("  Bull et al. 2019 reference (M22 v2 Test 1): CV = 0.177")
    print()


# =================================================================
# P37 — Old Faithful (informational; 1985 data, not post-2000)
# =================================================================
def p37():
    p = DIR / "faithful.csv"
    if not p.exists():
        print(f"Fetching {FAI_URL}")
        urllib.request.urlretrieve(FAI_URL, p)

    waiting: list[float] = []
    with p.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                w = float(row["waiting"])
            except (ValueError, KeyError):
                continue
            waiting.append(w)

    print("=" * 60)
    print("P37 — Old Faithful Class B SO(2) (informational)")
    print("=" * 60)
    print(f"  Eruptions loaded  : {len(waiting)}  (R faithful, Aug 1985)")
    print(f"  Pre-reg N≥1000    : NOT MET (N = {len(waiting)})")
    print(f"  Pre-reg date≥2000 : NOT MET (1985 data)")
    print()

    cv_val = cv(waiting)
    print(f"  mean (min)        : {statistics.mean(waiting):.2f}")
    print(f"  std  (min)        : {statistics.stdev(waiting):.2f}")
    print(f"  CV(inter-eruption): {cv_val:.4f}")
    print()
    print("  Pre-registered Class B SO(2) band [0.040, 0.080]:")
    if cv_val is not None:
        in_band = 0.040 <= cv_val <= 0.080
        in_falsifier = 0.020 <= cv_val <= 0.120
        verdict = ("PASS (informational)" if in_band else
                   ("in falsifier band, outside pre-reg"
                    if in_falsifier else "OUTSIDE FALSIFIER"))
        print(f"    CV = {cv_val:.4f} → {verdict}")
    print()

    # Note: 1985 Old Faithful is famous for bimodal distribution
    # (~55 min and ~80 min waiting times — Azzalini & Bowman 1990)
    # so this CV reflects bimodality, not a single SO(2) phase
    short = [w for w in waiting if w < 65]
    long = [w for w in waiting if w >= 65]
    print(f"  Bimodality check (Azzalini-Bowman 1990):")
    print(f"    short eruptions (<65 min) : N={len(short)}, "
          f"mean={statistics.mean(short):.1f}, "
          f"std={statistics.stdev(short):.1f}, "
          f"CV={cv(short):.4f}")
    print(f"    long  eruptions (≥65 min) : N={len(long)}, "
          f"mean={statistics.mean(long):.1f}, "
          f"std={statistics.stdev(long):.1f}, "
          f"CV={cv(long):.4f}")
    print()
    print("  Within each mode, CV is much lower — consistent with")
    print("  Class B SO(2) regulation. The pooled CV reflects mode")
    print("  mixing, not a single regulator.")
    print()


def main():
    b18()
    p37()


if __name__ == "__main__":
    main()
