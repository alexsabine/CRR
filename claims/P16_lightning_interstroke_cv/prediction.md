# P16 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target CV = 0.15915. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: published lightning return-stroke literature.
2. Inclusion: cloud-to-ground multi-stroke flashes (natural lightning, not triggered).
3. Statistic: CV = SD(inter-stroke interval)/mean across all flashes in the cohort.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.1114, 0.2069] = target ± 30%.
**C2.** ≥60% of qualifying cohorts have CV in [0.1, 0.25] (broader band).
**C3.** No cohort below 1/(4π) ≈ 0.080 (sub-SO(2) regulation excluded for Z₂ targets) OR no cohort above 1/(2π) ≈ 0.16 (super-Z₂ noise excluded for SO(2) targets).

## Falsifier

CV outside [0.08, 0.40] ⇒ Z₂ fails.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Inter-stroke intervals in CG lightning are known to span 10–300 ms with broad distribution; specific cohort CVs around 0.16 would be non-trivial.
