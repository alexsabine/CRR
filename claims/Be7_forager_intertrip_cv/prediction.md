# Be7 — Pre-registered prediction (Session 8)

**Pre-registered before any data lookup or analysis.**

## Statement

CRR canonical target: CV = 1/(2π) = 0.15915.

## Sampling protocol (locked)

1. WebSearch for 'honeybee forager trip duration' or 'forager inter-trip interval' tracking studies.
2. Inclusion: RFID/harmonic-radar tracked individual foragers, stable feeder or natural foraging in stable habitat; ≥ 50 trips per individual or ≥ 5 individuals.
3. CV = SD(trip interval)/mean.

## Pre-registered conditions

Pre-reg: median(CV) ∈ [0.10, 0.22] (broader Z₂ band). Falsifier: outside [0.05, 0.50].

## Tier promotion

Met ⇒ T1 → T3. Partially met ⇒ T1 → T2. Failed ⇒ stays T1
(honest negative).

## Independence

All cohorts/measurements pre-date CRR; cohort-selection rule
locked at this commit; no values used to derive the canonical
target.

## Honest exposure

Honest exposure: forager trip durations vary widely (5 min to 1 hr+); CV across trips for one bee may be 0.3–0.8 (closer to Class C). Honest negative possible.
