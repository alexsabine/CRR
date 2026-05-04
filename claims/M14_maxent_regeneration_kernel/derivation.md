# M14 — Derivation: exp(C/Ω) is the unique MaxEnt regeneration kernel

## Claim

The exponential kernel exp(C/Ω) in the regeneration integral is the
unique maximum-entropy distribution over coherence states under a
constraint on mean coherence, with natural parameter η = 1/Ω and
sufficient statistic C.

## Assumptions

(A1) The "distribution over coherence states" is a probability density
ρ(C) on a coherence axis C ∈ ℝ (or [0, ∞) with a measure that makes
the integral finite).
(A2) The constraint is a fixed expected coherence: E_ρ[C] = ⟨C⟩.
(A3) The objective is to maximise the differential entropy
H[ρ] = −∫ ρ log ρ subject to A2 and normalisation.

## Derivation (under A1–A3)

Lagrangian:

    L[ρ] = −∫ ρ log ρ dC − λ_0 (∫ ρ dC − 1) − λ_1 (∫ C ρ dC − ⟨C⟩).

Functional derivative δL/δρ = 0 gives

    −log ρ − 1 − λ_0 − λ_1 C = 0
    ρ(C) ∝ exp(−λ_1 C).

Identifying −λ_1 = 1/Ω (natural parameter η = 1/Ω; minus sign
absorbed by sign convention or by direction of the C-axis):

    ρ(C) = Z⁻¹ exp(C/Ω),    Z = ∫ exp(C/Ω) dμ(C).

This is the canonical exponential family with natural parameter
η = 1/Ω and sufficient statistic T(C) = C. By Boltzmann-Gibbs
uniqueness, this is the *unique* MaxEnt distribution under A2.

In the regeneration integral

    R[χ](x,t) = ∫₋∞ᵗ φ(x,τ) · exp(C(x,τ)/Ω) · Θ(t − τ) dτ,

the kernel exp(C/Ω) is precisely this MaxEnt density (up to
normalisation, which is absorbed into φ or into a separate Z), and
ρ acts as a *coherence-weighted prior* over past states.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M14_maxent_kernel`
verifies that on a discrete coherence grid with constrained mean,
the gradient-ascent solution to the entropy-maximisation problem
returns exp(C/Ω) (up to normalisation) for a chosen Ω.

## Caveats

- **This is a relabelling of Boltzmann-Gibbs.** The derivation
  reproduces the standard MaxEnt result; under M13 (C ≡ Fisher info)
  the *content* of the relabelling is non-trivial (CRR identifies
  the regeneration kernel as the MaxEnt under a specific choice of
  sufficient statistic), but M14 in isolation adds no information
  beyond the canonical Boltzmann-Gibbs theorem. **Tier capped at
  T1** per discipline; recorded in `notes/relabellings.md`.
- The convention of the sign of η (whether ρ ∝ exp(+C/Ω) or
  exp(−C/Ω)) depends on whether C is interpreted as "energy"
  (negative log-probability) or "negative energy"; CRR's choice
  exp(+C/Ω) corresponds to C as a *log-likelihood-like* quantity
  whose growth weights the past more heavily.
- Direct measure (dμ) on the coherence axis matters: with dμ = dC
  on [0, ∞), Z is finite only if Ω < 0 or if C is bounded above.
  In CRR, the bounding mechanism is the rupture C·Ω = 1 itself,
  which truncates the integration at C = 1/Ω.

## Status

**T1 (relabelling).** Standard MaxEnt argument; capped at T1 per
campaign discipline because the underlying theorem is canonical.
Domain-specific content arrives only via M13 + M14 together.
