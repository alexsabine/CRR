# B16 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target: Class B regulated (CV << 1/(4π)). Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: published gait stride-time studies in healthy adults walking at preferred speed.
2. Inclusion: healthy adult cohorts, treadmill or overground at preferred speed, ≥ 100 strides per subject.
3. Statistic: CV = SD(stride-time)/mean.
4. Median CV across cohorts.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.005, 0.05] — demonstrates Class B regulated regime.
**C2.** All qualifying cohorts < 1/(4π) ≈ 0.080.
**C3.** Median below 1/(4π) by ≥ 30% margin.

## Falsifier

median(CV) > 1/(4π) ≈ 0.08 ⇒ healthy gait is NOT Class B regulated; canonical regime classification fails.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Gait stride-time CV is widely documented at ~0.015-0.030 in healthy young adults; strongly expected to be Class B.
