# P15 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target CV = 0.15915. Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: Smithsonian GVP database.
2. Inclusion: single-volcano cohorts, VEI ≥ 2 events.
3. Selection: top 3 most-frequently-erupting volcanoes (Etna, Stromboli, Kilauea-class).
4. Statistic: median(CV) across the 3 cohorts.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.1114, 0.2069] = target ± 30%.
**C2.** ≥60% of qualifying cohorts have CV in [0.1, 0.25] (broader band).
**C3.** No cohort below 1/(4π) ≈ 0.080 (sub-SO(2) regulation excluded for Z₂ targets) OR no cohort above 1/(2π) ≈ 0.16 (super-Z₂ noise excluded for SO(2) targets).

## Falsifier

median(CV) > 0.50 ⇒ Z₂ fails (pure Poisson regime).

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Single-volcano recurrence often has CV ~ 1 (Poissonian); specific cohorts (Stromboli persistent activity) may show lower CVs near 0.16.
