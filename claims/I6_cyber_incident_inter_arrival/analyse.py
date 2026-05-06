"""
I6 — Analysis script.

Tests the pre-registered Z₂ prediction
(notes/session_10_industrial_predictions.md, commit aa6ee72):

    median CV(inter-incident interval) ∈ [0.140, 0.180]
    AND   N_firms ≥ 30.

Falsifier band: outside [0.120, 0.200].

PROTOCOL DEVIATIONS (recorded honestly per CAMPAIGN.md PART III):

1. Pre-reg specifies "Fortune 500 / FT Global 500 firms." VCDB
   does not tag Fortune 500 directly. We use
   `victim.orgsize.Large = 1` as a proxy. This is a *broader*
   filter than Fortune 500 (any large enterprise). Documented as
   a v1 deviation; a stricter v2 with explicit Fortune 500
   matching would require an independent victim-name → SIC →
   Fortune 500 mapping table.

2. Pre-reg specifies "≥10⁵ records or operational-disruption
   flag" for "major" incidents. VCDB record-count fields are
   sparse (most rows have unknown record count). We do *not*
   apply the magnitude filter in v1 — we use *all* large-victim
   incidents 2010-2025. This is a *wider* set than strict
   "major." Documented as a v1 deviation.

3. Many VCDB incidents have year-only timestamps (month and day
   are missing). We compute inter-incident intervals in *years*
   from `timeline.incident.year`. Same-year incidents have
   0-year intervals, which inflates the CV. Honest note in
   result.md.

4. The pre-registered N ≥ 30 binding remains. The proxy filter
   gives N = 110 large-victim firms with ≥3 incidents 2010-2025
   (110 ≥ 30 ✓).

Per discipline, the v1 result is binding. Honest documentation
of deviations does not retroactively re-write the pre-registration.

Run: python analyse.py
"""
from __future__ import annotations
import csv
import pathlib
import statistics
from collections import defaultdict

csv.field_size_limit(10**8)

CSV_PATH = pathlib.Path(__file__).parent / "vcdb.csv"


def main() -> None:
    if not CSV_PATH.exists():
        print(f"ERROR: {CSV_PATH} not found. Run fetch.py first.")
        return

    by_victim: dict[str, list[float]] = defaultdict(list)
    n_total = 0
    n_large = 0
    n_with_year = 0

    with CSV_PATH.open(newline="") as f:
        r = csv.reader(f)
        hdr = next(r)
        idx = {k: i for i, k in enumerate(hdr)}
        yr_i = idx["timeline.incident.year"]
        mo_i = idx["timeline.incident.month"]
        dy_i = idx["timeline.incident.day"]
        vid_i = idx["victim.victim_id"]
        lrg_i = idx["victim.orgsize.Large"]
        for row in r:
            n_total += 1
            if row[lrg_i].strip().lower() not in ("1", "true"):
                continue
            n_large += 1
            try:
                y = int(row[yr_i])
            except (ValueError, IndexError):
                continue
            if not (2010 <= y <= 2025):
                continue
            n_with_year += 1
            v = row[vid_i].strip()
            if not v or v.upper() == "NA":
                continue
            try:
                m = int(row[mo_i])
            except (ValueError, IndexError):
                m = 7  # mid-year default
            try:
                d = int(row[dy_i])
            except (ValueError, IndexError):
                d = 15
            t_years = y + (m - 1) / 12.0 + (d - 1) / 365.25
            by_victim[v].append(t_years)

    print(f"Total VCDB rows           : {n_total:>6,}")
    print(f"Large-victim rows         : {n_large:>6,}")
    print(f"Large + year ∈ [2010,2025]: {n_with_year:>6,}")
    print(f"Unique large victims      : {len(by_victim):>6,}")

    # Per-victim stats with ≥3 incidents
    eligible = {v: sorted(ts) for v, ts in by_victim.items() if len(ts) >= 3}
    print(f"Victims with ≥3 incidents : {len(eligible):>6,}")
    print()

    # Top-10 by incident count (transparency on data-quality outliers)
    print("Top 10 victims by incident count:")
    for v, ts in sorted(eligible.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"  N={len(ts):>4d}  {v[:65]}")
    print()

    def victim_cv(times: list[float]) -> float | None:
        intervals = [times[i + 1] - times[i] for i in range(len(times) - 1)]
        if len(intervals) < 2 or statistics.mean(intervals) <= 0:
            return None
        try:
            return statistics.stdev(intervals) / statistics.mean(intervals)
        except statistics.StatisticsError:
            return None

    cvs_all: list[float] = []
    cvs_capped: list[float] = []  # cap at ≤50 incidents to exclude data-quality outliers
    for v, ts in eligible.items():
        cv = victim_cv(ts)
        if cv is None:
            continue
        cvs_all.append(cv)
        if 3 <= len(ts) <= 50:
            cvs_capped.append(cv)

    def report(label: str, cvs: list[float]) -> None:
        n = len(cvs)
        if n == 0:
            print(f"{label}: empty")
            return
        cvs_sorted = sorted(cvs)
        med = (cvs_sorted[n // 2] if n % 2 else
               0.5 * (cvs_sorted[n // 2 - 1] + cvs_sorted[n // 2]))
        mean = statistics.mean(cvs)
        q1 = cvs_sorted[n // 4]
        q3 = cvs_sorted[3 * n // 4]
        print(f"{label}:")
        print(f"  N = {n}")
        print(f"  median CV = {med:.4f}")
        print(f"  mean   CV = {mean:.4f}")
        print(f"  IQR       = [{q1:.4f}, {q3:.4f}]")
        print(f"  min, max  = [{cvs_sorted[0]:.4f}, {cvs_sorted[-1]:.4f}]")

    report("All eligible large victims (≥3 incidents)", cvs_all)
    print()
    report("Filtered large victims (3 ≤ incidents ≤ 50)", cvs_capped)
    print()

    # Verdict against pre-registered band
    print("=" * 60)
    print("Pre-registered Z₂ prediction: median CV ∈ [0.140, 0.180]")
    print("Falsifier band: outside [0.120, 0.200]")
    print("=" * 60)
    for label, cvs in [("All", cvs_all), ("Filtered (≤50)", cvs_capped)]:
        if not cvs:
            continue
        cvs_sorted = sorted(cvs)
        n = len(cvs_sorted)
        med = (cvs_sorted[n // 2] if n % 2 else
               0.5 * (cvs_sorted[n // 2 - 1] + cvs_sorted[n // 2]))
        in_pred = 0.140 <= med <= 0.180
        in_band = 0.120 <= med <= 0.200
        if in_pred and n >= 30:
            verdict = "PASS — promotes to T3"
        elif in_band:
            verdict = "in-band, outside T3 — stays T2-marginal"
        else:
            verdict = "outside falsifier band — FAIL at T1"
        print(f"  {label}: median = {med:.4f}, N = {n} → {verdict}")


if __name__ == "__main__":
    main()
