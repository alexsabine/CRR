# M1 — Derivation: CV = Ω/2 with no free parameters

## Claim

The coefficient of variation of inter-rupture intervals equals Ω/2,
parameter-free, derived from the Bernoulli(1/2) variance of the n=1
binary rupture event.

## Assumptions

(A1) Coherence accumulates at unit rate L = 1: C(t) = t.
(A2) Rupture occurs the *first* time C·Ω = 1 holds, i.e., at
deterministic threshold T = 1/Ω.
(A3) Each rupture carries an n=1 Bernoulli(1/2) random variable
controlling whether the threshold is crossed at the nominal point or
displaced by one half-quantum on either side, with displacement
amplitude = T·(Ω/2) = 1/2.
(A4) Inter-rupture interval distribution is the rescaled
displacement distribution from A3.

## Derivation (under A1–A4)

By A1, A2: nominal inter-rupture interval = 1/Ω.
By A3: displacement Δ takes values ±1/2 with probability 1/2 each,
which is the standard Bernoulli(1/2) on {−1/2, +1/2}. Its mean is 0
and its variance is

    Var(Δ) = E[Δ²] − E[Δ]² = ((1/2)² + (−1/2)²)/2 − 0 = 1/4.

So std(Δ) = 1/2.

By A4: the inter-rupture interval τ = T + Δ = 1/Ω + Δ has

    E[τ] = 1/Ω,    std(τ) = std(Δ) = 1/2.

Coefficient of variation:

    CV = std(τ) / E[τ] = (1/2) / (1/Ω) = Ω/2.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M1_cv_equals_omega_over_2`
samples Bernoulli(1/2) displacements and verifies the empirical CV
of the rescaled inter-rupture interval converges to Ω/2 as the
sample size grows.

## Caveats

- **A3 is the load-bearing assumption.** The "Bernoulli(1/2)
  displacement of magnitude T·CV" specifies the noise model in a way
  that *makes the answer Ω/2 by construction*. The genuine content of
  the M1 claim is that **this** noise model — n=1 binary rupture —
  is the right one, not some other (Gaussian, exponential, fractional
  Brownian, etc.). The derivation given here is consistent with the
  stated noise model; whether the noise model itself is forced is a
  separate question, addressed (partially) by claim M3 (Cramér-Rao
  saturation pins the noise variance to the inverse Fisher
  information) and by Wijsman's optimal-stopping arguments.
- **Wijsman + Jaynes argument.** The brief invokes a Wijsman /
  Jaynes derivation of the factor 1/2; the more rigorous form of
  this argument identifies the variance of the optimal SPRT stopping
  rule (M18) as 1/(4·rate²) under Bernoulli signal, which gives the
  same factor 1/2 in the std. This is consistent with the derivation
  here but more rigorous; it is sketched in M18's derivation file.
- **Empirical CVs across systems** are reported with significant
  spread (Class A 0.13–0.18, etc.); the claim CV = Ω/2 holds for
  Class A "autonomous" systems only. Class B and Class C cohorts
  systematically deviate. So the M1 prediction is conditional on the
  empirical class label.

## Status

**T1.** Derivation is internally consistent under A3. Numerical
verification confirms convergence to Ω/2. The deeper question (is A3
itself derived?) is partially addressed by M3 and M18. Tier remains
T1 until those upstream claims are settled.
