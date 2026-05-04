# M6 — Derivation: Fourier transform is the trivial CRR limit

## Claim

Setting C(τ) = τ, Ω = i/k, and removing the Heaviside Θ in the
regeneration kernel recovers the Fourier kernel exp(−ikτ).

## Assumptions

(A1) The CRR regeneration kernel is K(τ) = exp(C(τ)/Ω), modulating
φ(x,τ) inside the integral R[χ] = ∫ φ · K · Θ dτ.
(A2) "Trivial limit" admits substitution of complex-valued Ω
(formally extending the real precision parameter to C).
(A3) Removing Θ replaces ∫₋∞ᵗ with ∫_ℝ.

## Derivation

Substitute A1's kernel under A2's substitution C(τ) = τ, Ω = i/k:

  K(τ) = exp(τ / (i/k)) = exp(kτ / i) = exp(−ikτ).

(The third equality uses 1/i = −i.)

Substitute into the regeneration integral with A3:

  R[χ] → ∫_ℝ φ(τ) · exp(−ikτ) dτ = F[φ](k).

The right-hand side is the Fourier transform of φ at frequency k.

So the Fourier transform is recovered as the special case
(C linear, Ω imaginary, no causal cut). CRR generalises Fourier on
three independent axes:
- non-linear C(τ),
- real Ω (precision, not frequency),
- causal cut Θ(t−τ) (one-sided integration).

## Numerical verification

`crr-engine/tests/test_engine.py::test_fourier_limit_kernel_modulus`
verifies |exp(−ikτ)| = 1 across (k,τ) pairs;
`test_fourier_limit_kernel_phase_at_tau_zero` verifies the kernel
evaluates to 1 at τ = 0.

## Caveats

- A2 (complex Ω) breaks the canonical "Ω = σ²" identification, which
  requires Ω real and positive. So this is not a *limit* in the
  topological sense; it is a *formal substitution*. The claim that
  Fourier is a "trivial limit" should be read as "Fourier is a
  trivial formal specialisation," not "Fourier is the limit of CRR
  as some real parameter goes to a boundary."
- The standard inverse Fourier transform requires both halves of the
  real line; A3 (no Θ) is essential. With Θ present, the
  corresponding object is a Laplace transform, not a Fourier
  transform. So the relationship CRR ⊃ Fourier is via a *non-causal*
  CRR variant, not the canonical causal CRR.

## Status

**T1.** Derivation is one substitution; verification is exact.
The "trivial limit" framing should arguably be "trivial formal
specialisation" — recorded in `notes/relabellings.md` as a phrasing
issue. Tier capped at T1 absent independent novel content.
