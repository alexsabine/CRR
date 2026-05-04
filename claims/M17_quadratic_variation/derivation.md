# M17 — Derivation: C is quadratic variation [μ,μ]_t

## Claim

In the martingale formulation of CRR, the coherence C(t) is the
quadratic variation [μ, μ]_t of an underlying information-flow
martingale μ_t.

## Assumptions

(A1) The underlying process μ_t is a continuous square-integrable
martingale (e.g., a Brownian motion or a stochastic integral against
one) on a filtered probability space.
(A2) The "rate" L(τ) in C(t) = ∫₀ᵗ L(τ) dτ is identified with the
predictable density of [μ, μ] with respect to dτ:

    [μ, μ]_t = ∫₀ᵗ L(τ) dτ.

## Derivation (under A1, A2)

**Standard fact (continuous martingale theory).** For any continuous
square-integrable martingale μ_t, the quadratic variation [μ, μ]_t
exists and is the unique continuous, increasing, predictable process
A_t such that μ_t² − A_t is a martingale (Doob-Meyer decomposition,
continuous case).

Under A2: A_t = ∫₀ᵗ L(τ) dτ = C(t).

So C(t) = [μ, μ]_t by *definition* of L. The CRR identification is
the choice "L is the local quadratic-variation rate of μ."

For Brownian motion B_t, [B, B]_t = t, so L = 1 ⇒ C(t) = t (constant
unit-rate accumulation). For a stochastic integral ∫₀ᵗ σ(s) dB_s,
L(τ) = σ(τ)² — the canonical Itō isometry result.

So C is *exactly* the quadratic variation of the underlying
martingale; the integrand L is the local volatility squared.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M17_quadratic_variation_brownian`
simulates a discrete Brownian-motion path with N steps of variance
1/N, computes the realised quadratic variation as Σ (ΔB_n)², and
verifies it converges to t = 1 (and to ∫₀ᵗ L dτ for non-constant
σ(τ)) as N → ∞.

## Caveats

- **This is a definition, not a theorem.** The identification A2 is
  a *choice* of what L means in the martingale formulation; with
  that choice, C = [μ, μ] is tautological. The substantive content
  is the *commitment* to the martingale formulation in the first
  place — which is one of several equivalent CRR formulations
  (alongside the information-geometric and ergodic formulations
  documented in `crr_first_principles_proofs.md`).
- **Recorded in `notes/relabellings.md`** as a definitional
  identification under the martingale picture.
- **Connection to M3 (Cramér-Rao).** Under M3 + M13, C is also
  Fisher information; under M17, C is also quadratic variation. The
  joint identification "Fisher information = quadratic variation" is
  a separate consistency claim, true for parametric exponential
  families (Bickel-Doksum reference) but not in full generality.

## Status

**T1 (definitional).** Derivation is one-step under A2. Tier capped
at T1.
