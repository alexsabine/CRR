# B8 — Derivation of CV = 1/(2π) for bacterial division

## Setup

Let `T_i` be the generation time of the i-th individual cell tracked
under exponential-phase steady-state growth (constant medium,
constant temperature, no stress). Let `T̄ = E[T]` and
`σ_T = (Var T)^(1/2)`. The dimensionless dispersion is

    CV = σ_T / T̄.

## CRR identification

Cell division is a single Z₂ event: at any instant either the cell
has not yet divided (state 0) or it has just divided (state 1).
The transition is the Dirac-delta rupture `δ(now) at C·Ω = 1`.

Under the canonical convention C1 (rupture is Z₂ by construction),
the rupture event has Bernoulli(1/2) variance, and the inter-rupture
interval inherits this variance via the `T = 1/Ω` rate identification
(C5; Kac's lemma).

The geodesic length of the Z₂ open arc on the Bernoulli statistical
manifold is φ_{Z₂} = π (Fisher–Rao geodesic from p=0 to p=1 on the
Bernoulli simplex; cf. M2 derivation). Therefore

    Ω_{Z₂} = 1/φ_{Z₂} = 1/π
    CV     = Ω/2 = 1/(2π) ≈ 0.15915.

## Key assumption

The cohort is in the Z₂-rupture regime — i.e., division is the
dominant rupture event and no upstream regulation is artificially
sharpening (Class B) or broadening (Class C) the distribution.
This is empirically realised under steady-state exponential growth
in well-controlled microfluidic experiments where each tracked
cell experiences an effectively identical environment.

## Falsifier (canonical)

A directional reversal — i.e., a cohort showing CV < CV_SO(2) =
1/(4π) ≈ 0.080 (which would indicate sub-Z₂ regulation contradicting
the rupture-as-Z₂ thesis) — would falsify the framework's regime
classification, not just B8.

A simple non-match (CV in [0.10, 0.20] but not at 1/(2π) within
tolerance) would weaken B8 specifically without falsifying the
broader framework.

## Empirical-test status

- T1 evidence: this derivation file. ✓
- T2 evidence: cohort consistency from published bacterial single-
  cell experiments — see `prediction.md` (pre-reg) and `result.md`.
