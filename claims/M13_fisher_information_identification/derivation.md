# M13 — Derivation: C is identified with accumulated Fisher information

## Claim

The CRR coherence C(x,t) = ∫₀ᵗ L(x,τ) dτ is identifiable with
accumulated Fisher information I(θ) when L is taken as the Fisher-Rao
infinitesimal arc length on the statistical manifold.

## Assumptions

(A1) The "system state" at time t parameterises a probability
distribution p(·|θ_t) on observables (the Fisher-Rao manifold).
(A2) The integrand L(x,τ) in the CRR coherence integral is the
Fisher-Rao squared infinitesimal speed: L = (dθ/dτ)ᵀ G(θ) (dθ/dτ),
where G is the Fisher information matrix at θ.
(A3) Time integration is along the system's trajectory θ_τ on the
manifold.

## Derivation (under A1–A3)

The Fisher information at parameter θ is

    I_{ij}(θ) = E_{x~p(·|θ)} [∂_i log p · ∂_j log p].

The Fisher-Rao metric is G(θ) = I(θ). Along a trajectory θ_τ, the
infinitesimal squared arc length is

    ds² = (dθ)ᵀ G(θ) (dθ).

The Fisher-Rao *speed* is L(τ) = (dθ/dτ)ᵀ G(θ) (dθ/dτ) = (ds/dτ)².
(Or, equivalently, the integrand of squared arc length per unit
parameter time.)

Integrating from 0 to t:

    C(t) = ∫₀ᵗ L(τ) dτ = ∫₀ᵗ (ds/dτ)² dτ.

Under A2, this is the **action** of the trajectory in the
Fisher-information metric — sometimes called "energy" in geometric
mechanics — which is the natural analogue of accumulated Fisher
information along a curve. For trajectories parameterised by arc
length, ds/dτ = const, and C(t) reduces to t · (constant). For
general trajectories, C(t) is the cumulative Fisher-information
"work."

Two cleaner identifications also reach the same conclusion:

**(i) Cumulative Fisher information** for a stationary parameter θ
observed sequentially: I_n(θ) = n · I(θ) for n iid observations.
With L = I (per-observation Fisher info), C = nI = accumulated
Fisher information of a sample sequence.

**(ii) Time-integrated Fisher information** along a stochastic
process: when the process generates observations at rate r and the
single-observation Fisher info is I, then C(t) = r·I·t.

Both reduce to "C is the accumulated Fisher information."

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M13_fisher_arc_length`
constructs a one-parameter Gaussian family with σ = 1 + θ, computes
the Fisher information I(θ) = 2/(1+θ)², integrates along a linear
trajectory θ_τ = τ, and verifies C(1) = ∫₀¹ I(τ) dτ matches the
analytic value 2 · ∫₀¹ (1+τ)⁻² dτ = 2 · (1 − 1/2) = 1.

## Caveats

- M13 is an **identification**, not a theorem. The substantive
  content is the *choice* L = Fisher-Rao speed²; with that choice,
  the integral *is* accumulated Fisher information by definition.
- Without M13, claim M3 (C·Ω = 1 saturates Cramér-Rao) lacks
  semantic content: Cramér-Rao is a statement about Fisher
  information bounding estimator variance, and only with C ≡
  accumulated Fisher info does the saturation claim become a claim
  about the CR bound rather than an algebraic coincidence.
- Alternative L choices (e.g., entropy production rate, KL rate to
  a reference distribution) yield different identifications. The
  Fisher-Rao identification is the canonical one for parametric
  statistics; other branches of CRR literature use different L's.

## Status

**T1.** Derivation is straightforward under the stated choice of L.
M13 is foundational for M3, M4, M14, M21; if A2 is rejected, those
claims lose their derivations.
