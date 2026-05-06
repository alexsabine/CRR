# I6 — Pre-registered prediction (verbatim from Session 10 doc)

## Statement

Across Fortune 500 / FT Global 500 firms with ≥3 disclosed major
incidents 2010-2025 in the VERIS Community Database (VCDB), the
median across firms of intra-firm CV(inter-incident interval)
satisfies

    median CV(inter-incident Δt) ∈ [0.140, 0.180]
    AND   N_firms ≥ 30.

## Substrate

Z₂ autonomous; CV = 1/(2π) ≈ 0.1592.

## Falsifier

median CV outside [0.120, 0.200] with N ≥ 30.

## Dataset

VERIS Community Database (`https://github.com/vz-risk/VCDB`),
canonical CSV at `data/csv/vcdb.csv.zip`.

## Pre-registered protocol deviations (committed before analysis)

The protocol applied in `analyse.py` deviates from the strict
pre-registration in two ways, recorded transparently:

1. **Fortune 500 proxy.** VCDB does not tag Fortune 500. We use
   `victim.orgsize.Large = 1` as a broader proxy.
2. **Magnitude filter omitted.** VCDB record-count fields are
   sparse; we test on all large-victim incidents 2010-2025
   without restricting to ≥10⁵ records.

These widen the eligible set, making the test *less* conservative.
The N ≥ 30 binding remains.

## T3 promotion criterion

median CV ∈ [0.140, 0.180] with N ≥ 30 (under either strict or
proxy filter).
