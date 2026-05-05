# B18 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target CV = 0.15915. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: published live-cell mitochondrial fission imaging studies.
2. Inclusion: mammalian / yeast cells, wild-type, no fission/fusion-perturbation drugs.
3. Statistic: CV = SD(inter-fission-interval per mitochondrion) / mean.
4. Median CV across cohorts.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.1114, 0.2069] = target ± 30%.
**C2.** ≥60% of qualifying cohorts have CV in [0.1, 0.3] (broader band).
**C3.** No cohort below 1/(4π) ≈ 0.080 (sub-SO(2) regulation excluded for Z₂ targets) OR no cohort above 1/(2π) ≈ 0.16 (super-Z₂ noise excluded for SO(2) targets).

## Falsifier

median(CV) > 1.0 ⇒ Z₂ fails (purely Poisson regime).

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Mitochondrial fission rates are heterogeneous; specific cohort CVs around 0.16 would be non-trivial.
