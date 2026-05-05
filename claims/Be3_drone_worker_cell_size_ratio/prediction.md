# Be3 — Pre-registered prediction (Session 8)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical target: ratio = 1.3333333333333333.

## Sampling protocol (locked)

1. WebSearch for honeybee 'worker cell diameter' and 'drone cell diameter' canonical values.
2. Compute ratio drone/worker.
3. Statistic: |ratio − 4/3| / (4/3).

## Pre-registered conditions

Pre-reg: |ratio − 4/3| / (4/3) < 0.05 (within 5%). Falsifier: deviation > 10%.

## Tier promotion

Met ⇒ T1 → T3. Partially met ⇒ T1 → T2. Failed ⇒ stays T1
(honest negative).

## Independence

All cohorts/measurements pre-date CRR; cohort-selection rule
locked at this commit; no values used to derive the canonical
target.

## Honest exposure

Honest exposure: 6.9/5.2 = 1.327 vs 4/3 = 1.333 — deviation 0.45% if I use these canonical numbers. The pre-reg is whether the canonical literature confirms 4/3.
