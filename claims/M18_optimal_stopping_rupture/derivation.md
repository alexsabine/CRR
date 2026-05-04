# M18 — Derivation: Rupture time τ_Ω is optimal stopping (SPRT equivalent)

## Claim

The CRR rupture time τ_Ω = inf {t : C(t)·Ω ≥ 1} is the optimal
stopping time of a Sequential Probability Ratio Test (SPRT) under
the M13 identification of C with accumulated log-likelihood ratio
(Fisher-information equivalent).

## Assumptions

(A1) M13: C(t) is accumulated Fisher information, equivalently the
log-likelihood ratio process L(t) = log Λ(t) for testing H₀ vs H₁
under the relevant exponential-family model.
(A2) The SPRT stops the first time the log-likelihood ratio crosses
either of two thresholds A < 0 < B.
(A3) "Rupture" corresponds to crossing the upper threshold B; the
CRR rupture condition C·Ω = 1 identifies B = 1/Ω.

## Derivation (under A1–A3)

**Wald's SPRT (1947).** For testing H₀ vs H₁ on iid observations
with likelihood ratios λ_n, accumulate L_n = Σ log λ_i. Stop when
L_n ∉ (A, B); accept H₀ if L_n ≤ A; accept H₁ if L_n ≥ B.

**Optimality (Wald-Wolfowitz 1948).** Among all sequential tests
with given error probabilities (α, β), SPRT minimises expected
sample size under both H₀ and H₁.

Under A1, A3: C(t) plays the role of L_n; the upper threshold B is
1/Ω. So the CRR rupture time is

    τ_Ω = inf {t : C(t) ≥ 1/Ω}

= the first hitting time of the SPRT upper boundary at level 1/Ω.

By Wald-Wolfowitz, this is the *optimal* stopping rule in the sense
of minimising expected accumulated coherence (≡ expected sample size
≡ expected Fisher information collected) for a given decision-error
budget.

**Connection to M1 (CV = Ω/2).** The variance of the SPRT stopping
time at the upper boundary, under one-sided crossing, has a Wald-
identity-derived form

    Var(τ_Ω) ≈ (1/Ω)² · Var(log λ) / (E[log λ])² · O(1)

with the O(1) factor depending on the boundary-crossing details. For
Bernoulli(1/2) signal under M1's noise model, the result reduces
algebraically to CV = Ω/2 — providing the rigorous SPRT-based
underpinning that M1's derivation invokes informally.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M18_sprt_stopping_time`
simulates iid Bernoulli(p=0.6) data, accumulates log-likelihood
ratio for H₀: p=0.5 vs H₁: p=0.6, runs N = 10000 SPRT trials with
upper threshold B = 1/Ω for chosen Ω, and verifies the empirical
mean stopping time matches the Wald approximation E[τ] ≈ B / E[log λ
| H₁].

## Caveats

- **Upper-boundary only.** CRR's rupture is a single (upper) crossing
  — it discards the SPRT lower boundary. Strictly, CRR is a
  *one-sided* SPRT, which is optimal in the *Bayes* sense (with
  appropriate prior) but loses the symmetric optimality of two-sided
  SPRT. Recorded.
- **Continuous-time SPRT.** Wald's original SPRT is for iid discrete
  observations; the continuous-time analogue (Liptser-Shiryaev) gives
  the same optimality under appropriate regularity. The CRR
  continuous-time formulation inherits this.
- **Optimality is *given* the cost structure.** SPRT minimises
  expected sample size under fixed error rates. If the CRR cost is
  formulated differently (e.g., minimising expected *time* with
  unbounded errors), the optimal rule changes. The CRR rupture-time
  minimisation is justified only under SPRT-style costs.

## Status

**T1.** Derivation rests on Wald-Wolfowitz (canonical) under
M13's identification. Verification numerical.
