# P13 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target CV = 0.07958. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: Pantheon+ public release (Scolnic+ 2022).
2. Inclusion: standardised SNe Ia peak magnitudes after stretch (x1) and colour (c) corrections.
3. Statistic: CV = σ_{intrinsic} / |M̄| in absolute magnitude units (or equivalent fractional dispersion).

## Pre-registered conditions

**C1.** median(CV) ∈ [0.0557, 0.1035] = target ± 30%.
**C2.** ≥60% of qualifying cohorts have CV in [0.05, 0.12] (broader band).
**C3.** No cohort below 1/(4π) ≈ 0.080 (sub-SO(2) regulation excluded for Z₂ targets) OR no cohort above 1/(2π) ≈ 0.16 (super-Z₂ noise excluded for SO(2) targets).

## Falsifier

Fractional dispersion outside [0.04, 0.15] ⇒ SO(2) fails.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Pantheon+ intrinsic scatter is ~0.10 mag in M (5% in flux); may be Class B regulated rather than SO(2)-Class A.
