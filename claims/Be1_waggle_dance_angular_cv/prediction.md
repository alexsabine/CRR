# Be1 — Pre-registered prediction (Session 8)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical target: CV = 1/(4π) = 0.07958.

## Sampling protocol (locked)

1. PubMed/Web search for 'honeybee waggle dance angular precision standard deviation' studies.
2. Inclusion: A. mellifera waggle dance recordings, ≥10 dances per target, fast-returning foragers, horizontal target distance reported.
3. Statistic: angular SD per dance / 180° (the half-period normalisation) as a fractional CV; or SD(angle)/π in radians.
4. Up to 5 cohorts, median taken.

## Pre-registered conditions

Pre-reg: median(CV) ∈ [0.056, 0.104] = 1/(4π) ± 30%. Falsifier: median outside [0.04, 0.16].

## Tier promotion

Met ⇒ T1 → T3. Partially met ⇒ T1 → T2. Failed ⇒ stays T1
(honest negative).

## Independence

All cohorts/measurements pre-date CRR; cohort-selection rule
locked at this commit; no values used to derive the canonical
target.

## Honest exposure

Honest exposure: published waggle-dance SDs ≈ 13–25° translate to fractional CVs of 0.07–0.14 — straddles the SO(2) band; could pass or fail depending on which cohorts qualify.
