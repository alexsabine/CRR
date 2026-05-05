# B17 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target CV = 0.15915. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: published E. coli run-tumble tracking studies.
2. Inclusion: wild-type E. coli, isotropic medium (no chemoattractant gradient), 3D tracking ≥ 100 cells.
3. Statistic: CV = SD(run-duration)/mean across cells.
4. Median CV across qualifying cohorts.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.1114, 0.2069] = target ± 30%.
**C2.** ≥60% of qualifying cohorts have CV in [0.1, 0.3] (broader band).
**C3.** No cohort below 1/(4π) ≈ 0.080 (sub-SO(2) regulation excluded for Z₂ targets) OR no cohort above 1/(2π) ≈ 0.16 (super-Z₂ noise excluded for SO(2) targets).

## Falsifier

median(CV) outside [0.08, 0.50] ⇒ Z₂ fails for run-tumble.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Run-duration CV historically reported ~0.7-1.0 (Berg-Brown 1972 exponential approximation); 0.16 would be a non-trivial departure from canonical Poisson interpretation.
