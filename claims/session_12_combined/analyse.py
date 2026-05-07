"""
Session 12 — Combined analysis for P27, P28, P29.

Pre-registration commit: f7492b7
(notes/session_12_pre_registrations.md)

Datasets:
- datasets/finance-vix daily 1990-2026 (VIX close)
- datasets/s-and-p-500 monthly 1871-2026 (Shiller real price)
- NBER 12 post-WWII recession peak dates (embedded; public domain)

Run: python analyse.py
"""
from __future__ import annotations
import csv
import math
import statistics
from datetime import date, datetime
import urllib.request
import pathlib
import sys

DIR = pathlib.Path(__file__).parent
VIX_URL = "https://raw.githubusercontent.com/datasets/finance-vix/main/data/vix-daily.csv"
SPX_URL = "https://raw.githubusercontent.com/datasets/s-and-p-500/main/data/data.csv"

# --- NBER post-WWII recession peak dates (public-domain facts) ---
# Source: https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions
NBER_PEAKS = [
    (1948, 11), (1953, 7), (1957, 8), (1960, 4),
    (1969, 12), (1973, 11), (1980, 1), (1981, 7),
    (1990, 7), (2001, 3), (2007, 12), (2020, 2),
]


def fetch(url: str, name: str) -> pathlib.Path:
    p = DIR / name
    if not p.exists():
        print(f"Fetching {url}")
        urllib.request.urlretrieve(url, p)
    return p


def cv(xs):
    if len(xs) < 2:
        return None
    m = statistics.mean(xs)
    if m <= 0:
        return None
    return statistics.stdev(xs) / m


# =================================================================
# P27 — VIX spike inter-arrival CV
# =================================================================
def run_P27():
    p = fetch(VIX_URL, "vix-daily.csv")
    spikes = []  # ordinal day numbers where VIX close >= 30
    with p.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                close = float(row["CLOSE"])
                d = datetime.strptime(row["DATE"], "%m/%d/%Y").date()
            except (ValueError, KeyError):
                continue
            if close >= 30.0:
                spikes.append(d.toordinal())
    spikes.sort()
    if not spikes:
        print("P27: no spikes found")
        return
    # Inter-spike intervals in days
    intervals = [spikes[i + 1] - spikes[i] for i in range(len(spikes) - 1)]
    # Filter zero-day intervals (consecutive days both above 30) — these are
    # within-event continuations, not separate spikes. Define a "spike" as
    # the *first* day of a contiguous run.
    # Re-derive: collapse consecutive days into single events.
    events = [spikes[0]]
    for s in spikes[1:]:
        if s - events[-1] >= 5:  # require 5+ day gap to count as new event
            events.append(s)
    intervals = [events[i + 1] - events[i] for i in range(len(events) - 1)]
    n_spikes = len(events)
    n_int = len(intervals)
    cv_val = cv(intervals)
    print("=" * 60)
    print(f"P27 — VIX spikes (close >= 30, 5-day collapse rule)")
    print("=" * 60)
    print(f"  N spike days raw         : {len(spikes)}")
    print(f"  N events after 5-day gap : {n_spikes}")
    print(f"  N intervals              : {n_int}")
    if cv_val is None:
        print("  CV: undefined")
        return
    print(f"  mean interval (days)     : {statistics.mean(intervals):.1f}")
    print(f"  std interval  (days)     : {statistics.stdev(intervals):.1f}")
    print(f"  CV(inter-spike interval) : {cv_val:.4f}")
    print()
    print(f"  Pre-registered band [0.85, 1.15]: "
          f"{'PASS' if 0.85 <= cv_val <= 1.15 else 'FAIL'}")
    print(f"  Falsifier band [0.70, 1.30]    : "
          f"{'inside' if 0.70 <= cv_val <= 1.30 else 'OUTSIDE → falsified'}")
    print(f"  N >= 30 condition              : "
          f"{'PASS' if n_spikes >= 30 else 'FAIL'}")
    print()


# =================================================================
# P28 — NBER recession peak-to-peak interval CV
# =================================================================
def run_P28():
    months = [(y - 1900) * 12 + m for y, m in NBER_PEAKS]
    intervals = [months[i + 1] - months[i] for i in range(len(months) - 1)]
    n = len(intervals)
    cv_val = cv(intervals)
    print("=" * 60)
    print(f"P28 — NBER US recession peak-to-peak intervals (post-WWII)")
    print("=" * 60)
    print(f"  Peaks (year-month): {NBER_PEAKS}")
    print(f"  Intervals (months): {intervals}")
    print(f"  N intervals       : {n}")
    print(f"  mean (months)     : {statistics.mean(intervals):.1f}")
    print(f"  std  (months)     : {statistics.stdev(intervals):.1f}")
    print(f"  CV                : {cv_val:.4f}")
    print()
    print("  Substrate identification against three pre-registered bands:")
    bands = [
        ("No-regulator", 0.85, 1.15),
        ("Z₂",           0.140, 0.180),
        ("SO(2)",        0.070, 0.090),
    ]
    for name, lo, hi in bands:
        match = lo <= cv_val <= hi
        print(f"    {name:14s} [{lo:.3f}, {hi:.3f}]: "
              f"{'MATCH' if match else 'no match'}")
    overall_in = any(lo <= cv_val <= hi for _, lo, hi in bands)
    print(f"  Falsifier (outside [0.06, 1.30]): "
          f"{'falsified' if not (0.06 <= cv_val <= 1.30) else 'inside'}")
    print()


# =================================================================
# P29 — S&P 500 monthly drawdown event inter-arrival CV
# =================================================================
def run_P29():
    p = fetch(SPX_URL, "spx.csv")
    rows = []
    with p.open(newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                d = datetime.strptime(row["Date"], "%Y-%m-%d").date()
                rp = float(row["Real Price"])
            except (ValueError, KeyError):
                continue
            if rp > 0:
                rows.append((d, rp))
    rows.sort(key=lambda x: x[0])
    drawdown_dates = []
    for i in range(1, len(rows)):
        prev = rows[i - 1][1]
        cur = rows[i][1]
        if cur <= 0 or prev <= 0:
            continue
        log_ret = math.log(cur / prev)
        if log_ret < -0.05:
            drawdown_dates.append(rows[i][0])
    intervals = [(drawdown_dates[i + 1] - drawdown_dates[i]).days
                 for i in range(len(drawdown_dates) - 1)]
    # Filter: drop within-month duplicate interval=0 cases (none expected
    # since monthly data, but defensive)
    intervals = [x for x in intervals if x > 0]
    n_int = len(intervals)
    cv_val = cv(intervals)
    print("=" * 60)
    print(f"P29 — SPX monthly real-return drawdown < -5% inter-arrival")
    print("=" * 60)
    print(f"  Months in series   : {len(rows)} ({rows[0][0]} → {rows[-1][0]})")
    print(f"  Drawdown events    : {len(drawdown_dates)}")
    print(f"  Intervals          : {n_int}")
    if cv_val is None:
        print("  CV: undefined")
        return
    print(f"  mean (days)        : {statistics.mean(intervals):.1f}")
    print(f"  std  (days)        : {statistics.stdev(intervals):.1f}")
    print(f"  CV                 : {cv_val:.4f}")
    print()
    print(f"  Pre-registered band [0.85, 1.15]: "
          f"{'PASS' if 0.85 <= cv_val <= 1.15 else 'FAIL'}")
    print(f"  Falsifier band [0.70, 1.30]    : "
          f"{'inside' if 0.70 <= cv_val <= 1.30 else 'OUTSIDE → falsified'}")
    print(f"  N >= 30 condition              : "
          f"{'PASS' if len(drawdown_dates) >= 30 else 'FAIL'}")
    # Substrate identification (informational)
    print()
    print("  Substrate identification (informational, not pre-registered for P29):")
    bands = [
        ("No-regulator", 0.85, 1.15),
        ("Z₂",           0.140, 0.180),
        ("SO(2)",        0.070, 0.090),
    ]
    for name, lo, hi in bands:
        match = lo <= cv_val <= hi
        print(f"    {name:14s} [{lo:.3f}, {hi:.3f}]: "
              f"{'MATCH' if match else 'no match'}")
    print()


def main():
    run_P27()
    run_P28()
    run_P29()


if __name__ == "__main__":
    main()
