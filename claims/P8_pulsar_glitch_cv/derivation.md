# P8 — Derivation of CV = 1/(2π) for pulsar glitch inter-arrival

## Setup

Let `T_i` = time between successive glitches at a single pulsar. Let
`T̄ = E[T]`, `σ_T = √Var T`. Dispersion: CV = σ_T / T̄.

## CRR identification

A glitch is a single avalanche-class rupture: the superfluid
vortex pinning lattice releases stored angular momentum at the
threshold C·Ω = 1. The release is Bernoulli(1/2) at threshold
(pinned vs unpinned regimes; C1).

Z₂ open arc on Bernoulli statistical manifold: φ_{Z₂} = π;
Ω_{Z₂} = 1/π; CV = 1/(2π) ≈ 0.15915.

## Key assumption

Steady-state glitching epoch — no anomalous "macro-quake" outliers
(those are flagged in primary catalogues). Single pulsar, single
neutron-star regime. Cohort selection per pre-reg.

## Falsifier

CV substantially below 1/(4π) ≈ 0.080 → sub-rupture regulation
(unphysical for avalanche systems); CV > 1/(π) → Poissonian
super-rupture limit, contradicts Z₂ identification.

## Status

T1 by this derivation. T2/T3 evidence in `prediction.md` and
forthcoming `result.md`.
