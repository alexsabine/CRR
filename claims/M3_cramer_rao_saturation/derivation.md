# M3 — Derivation: C·Ω = 1 saturates the Cramér-Rao bound

## Claim

The CRR rupture condition C·Ω = 1 is the equality case of the
Cramér-Rao bound under the identification of C with accumulated
Fisher information and Ω with parameter-estimator variance.

## Assumptions

(A1) M13: C is accumulated Fisher information I(θ) along the
trajectory.
(A2) Ω = σ², where σ² is the variance of an unbiased estimator
θ̂ of the underlying parameter.
(A3) The estimator achieves the CR bound (i.e., it is *efficient*).

## Derivation (under A1–A3)

The Cramér-Rao inequality for an unbiased estimator θ̂ of θ
based on Fisher information I(θ) is

    Var(θ̂) ≥ 1 / I(θ).

Equality (saturation) holds iff θ̂ is efficient — i.e., a sufficient
statistic for θ in an exponential family.

Under A1, A2: I(θ) = C (per the M13 identification) and Var(θ̂) = σ²
= Ω. Substituting into the equality case:

    Ω = 1/C    ⇔    C·Ω = 1.

This is exactly the CRR rupture condition. So the equality C·Ω = 1
expresses *Cramér-Rao saturation* under the identifications A1, A2,
A3.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M3_cramer_rao_saturation`
takes a Gaussian location model with known I(θ) = 1/σ², constructs
the sample-mean estimator (which is efficient), and verifies that
Var(θ̂) · I(θ) = 1 to within Monte-Carlo error — i.e., the CR
inequality is saturated, equivalent to C·Ω = 1.

## Caveats

- **Loadbearing on M13.** Without the C ↔ Fisher information
  identification, the algebraic identity C·Ω = 1 is just a
  relabelling of σ² = 1/I — which is itself a relabelling of the CR
  saturation condition.
- **Saturation requires efficiency.** Not every estimator achieves
  CR; only sufficient statistics in exponential families do (Lehmann-
  Scheffé). The CRR claim that ruptures occur *at* C·Ω = 1
  presupposes the underlying inference reaches CR-efficient
  estimation at the rupture instant. This is a strong condition;
  not all real-world inference processes are CR-efficient.
- **The exp(C/Ω) → e identification fails at the CR-saturated
  instant.** As recorded in `notes/relabellings.md`, the brief's
  statement "exp(C/Ω) → e at C·Ω = 1" requires Ω = 1, which is not
  implied by CR saturation. M3 derivation does *not* depend on the
  exp → e identification, which is a separate (and apparently
  inconsistent) assertion.

## Status

**T1.** Derivation is one substitution under M13 + A2 + A3.
Numerical verification confirms saturation in the Gaussian case.
Tier capped pending M13 status and resolution of efficiency
requirement.
