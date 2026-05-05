# P12 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target CV = 0.07958. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: Planck 2018 results paper VI.
2. Use ℓ_n positions of first 5 acoustic peaks.
3. Statistic: CV = SD(Δℓ) / mean(Δℓ) where Δℓ_n = ℓ_n − ℓ_{n−1}.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.0597, 0.0995] = target ± 25%.
**C2.** ≥60% of qualifying cohorts have CV in [0.05, 0.11] (broader band).
**C3.** No cohort below 1/(4π) ≈ 0.080 (sub-SO(2) regulation excluded for Z₂ targets) OR no cohort above 1/(2π) ≈ 0.16 (super-Z₂ noise excluded for SO(2) targets).

## Falsifier

CV outside [0.04, 0.20] ⇒ SO(2) fails for CMB peaks.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Δℓ spacings are known to be near-uniform (~330) — CV likely very small (Class B regulated rather than Class A). May fail.
