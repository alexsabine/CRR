# Be9 — Pre-registered prediction (Session 8)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical target: CV_exp = 1 (M23: Z₂-without-SO(2)).

## Sampling protocol (locked)

1. WebSearch for 'csd complementary sex determiner allele frequency Apis mellifera population' studies.
2. Compute CV = SD(allele frequency)/mean(allele frequency) within a wild population.

## Pre-registered conditions

Pre-reg: median(CV) ∈ [0.7, 1.4] (Class C / M23). Falsifier: CV < 0.3 (would mean frequencies are tightly regulated, contradicting NFDS).

## Tier promotion

Met ⇒ T1 → T3. Partially met ⇒ T1 → T2. Failed ⇒ stays T1
(honest negative).

## Independence

All cohorts/measurements pre-date CRR; cohort-selection rule
locked at this commit; no values used to derive the canonical
target.

## Honest exposure

Honest exposure: NFDS literature suggests broad frequency distributions; CV ≈ 1 is plausible but depends on sampling.
