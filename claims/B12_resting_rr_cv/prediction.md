# B12 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target CV = 0.15915. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: published healthy-adult resting HRV cohorts.
2. Inclusion: healthy adults, supine/seated rest, awake, 5-min standardised recording (Task Force 1996 protocol).
3. Statistic: CV = SDNN/meanNN (SDNN being the standard deviation of normal-to-normal RR intervals).
4. Median CV across qualifying cohorts.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.1114, 0.2069] = target ± 30%.
**C2.** ≥60% of qualifying cohorts have CV in [0.05, 0.2] (broader band).
**C3.** No cohort below 1/(4π) ≈ 0.080 (sub-SO(2) regulation excluded for Z₂ targets) OR no cohort above 1/(2π) ≈ 0.16 (super-Z₂ noise excluded for SO(2) targets).

## Falsifier

median(CV) outside [0.03, 0.25] ⇒ both Z₂ and SO(2) fail; cardiac is in regulated regime.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Resting HRV SDNN/meanNN typically reported as ~0.05-0.10 (Class A SO(2)) for healthy young adults. Older / sicker cohorts shift higher.
