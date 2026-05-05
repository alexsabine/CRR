# Be8 — Pre-registered prediction (Session 8)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical target: CV = 1/(2π) = 0.15915.

## Sampling protocol (locked)

1. WebSearch for 'honeybee colony swarming frequency inter-swarm interval' studies (Caron, Seeley).
2. CV = SD(inter-swarm interval)/mean across N colonies or N years at one apiary.

## Pre-registered conditions

Pre-reg: median(CV) ∈ [0.10, 0.30] (broader Z₂ band). Falsifier: outside [0.05, 0.50].

## Tier promotion

Met ⇒ T1 → T3. Partially met ⇒ T1 → T2. Failed ⇒ stays T1
(honest negative).

## Independence

All cohorts/measurements pre-date CRR; cohort-selection rule
locked at this commit; no values used to derive the canonical
target.

## Honest exposure

Honest exposure: swarming is highly seasonal — CV across years at one site may be inflated by external triggers.
