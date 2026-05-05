# B15 — Pre-registered prediction (Session 7)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical: target: Class C noise-dominated (CV >> 1/(2π)). Cohort search protocol locked below.

## Sampling protocol (locked)

1. Source: published in-vivo extracellular cortical spike-train studies in awake behaving animals.
2. Inclusion: pyramidal neurons in V1/V2/MT/PFC, spontaneous or stimulus-driven firing.
3. Statistic: CV_ISI = SD/mean of inter-spike intervals.
4. Median CV across cohorts.

## Pre-registered conditions

**C1.** median(CV) ∈ [0.5, 1.5] — demonstrates Class C noise-dominated regime.
**C2.** All qualifying cohorts > 1/(2π) ≈ 0.16.
**C3.** Median above 1/(2π) by ≥ 30% margin.

## Falsifier

median(CV_ISI) < 1/(2π) ≈ 0.16 ⇒ in-vivo cortical firing is NOT Class C noise-dominated; canonical regime fails.

## Tier promotion

C1+C2+C3 ⇒ T1 → T3. C1+C2 only ⇒ T2. C1 only ⇒ T2 (m). C1 fail ⇒
stays T1.

## Independence

Data sources pre-date CRR; the cohort selection rule is locked
before lookup; no cohort here was used to derive the canonical
target value.

## Honest exposure

Cortical ISI CV is widely documented at ~0.7-1.2 (the Softky-Koch puzzle); strongly expected to be Class C.
