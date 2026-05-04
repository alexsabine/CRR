# B9 — Derivation of CV = 1/(4π) for healthy resting respiratory cycle

## Setup

Let `T_i` be the i-th breath-to-breath interval (BBI) measured in
healthy adult humans at rest, awake, in a recumbent or seated
position, with no external pacing. Let `T̄ = E[T]`,
`σ_T = √Var T`. The dispersion is

    CV = σ_T / T̄.

## CRR identification

The respiratory cycle is a continuous closed orbit on an SO(2)
phase manifold: at any instant, the system has a well-defined
phase φ ∈ [0, 2π) within the cycle, and after exactly 2π of phase
advance the system returns to the same configuration (start of
inspiration).

The cycle is the closed-geodesic representative of SO(2) =
S¹. Geodesic length φ_G = 2π (Convention C2 in
`notes/conventions.md`). Hence

    Ω_{SO(2)} = 1/φ_G = 1/(2π) ≈ 0.1592

The rupture event is the SO(2)→Z₂ projection (the discrete
"start-of-breath" marker), preserving the canonical CV = Ω/2:

    CV = Ω_{SO(2)} / 2 = 1/(4π) ≈ 0.07958.

## Why SO(2), not Z₂

Cardiac depolarisation can also be modelled as Z₂-rupture-only
(refractory-then-fire). Respiration cannot — the cycle has a
*sustained* rising-then-falling tidal volume profile, not a
relax-then-spike profile. The continuous tidal-volume trajectory
is the SO(2) phase observable. (Cardiac is more ambiguous; B2
addresses cardiac separately.)

## Key assumption

The cohort is at rest, healthy, awake, no external pacing
(no metronome, no music, no speech). Vagal tone is intact (no
cardiopulmonary disease; no sleep stage where central pattern
generator dynamics differ; no psychiatric medication affecting
brainstem respiratory rhythm).

These conditions pick out the **autonomous Class A** regime where
the canonical CV = Ω/2 prediction applies. Outside these
conditions:
- Class B (regulated): CV < 1/(4π). E.g., paced breathing.
- Class C (noise-dominated): CV > 1/(4π). E.g., COPD, sleep apnea.

The pre-registration restricts to Class A by inclusion criteria.

## Falsifier (canonical)

A cohort matching the inclusion criteria with CV > 1/(2π) (above
the Z₂ band) would falsify the SO(2) identification — implying
respiration is not in the autonomous SO(2) regime under standard
healthy-resting conditions.

## Empirical-test status

- T1 evidence: this derivation file. ✓
- T2/T3 evidence: see `prediction.md` and forthcoming `result.md`.
