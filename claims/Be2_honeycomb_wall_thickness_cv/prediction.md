# Be2 — Pre-registered prediction (Session 8)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical target: CV = 1/(2π) = 0.15915.

## Sampling protocol (locked)

1. WebSearch for honeycomb wall-thickness SD measurements.
2. Inclusion: A. mellifera worker comb, drone comb separately; measurements of wall thickness in established comb at multiple positions.
3. Statistic: CV = SD(wall thickness)/mean across cells in a single comb (then pooled across combs).
4. Up to 5 cohorts.

## Pre-registered conditions

Pre-reg: median(CV) ∈ [0.111, 0.207] = 1/(2π) ± 30%. Falsifier: outside [0.08, 0.30].

## Tier promotion

Met ⇒ T1 → T3. Partially met ⇒ T1 → T2. Failed ⇒ stays T1
(honest negative).

## Independence

All cohorts/measurements pre-date CRR; cohort-selection rule
locked at this commit; no values used to derive the canonical
target.

## Honest exposure

Honest exposure: Hepburn et al. report wall thicknesses around 73 μm with SD around 10 μm → CV ~ 0.14, in the band. But wall-thickness CV is regulated by surface tension and may be Class B (CV < 0.08).
