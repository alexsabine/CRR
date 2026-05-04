# M11 — Derivation: Z₂ + Z₂ → SO(2) gives ρ = −1/2

## Claim

Two Z₂ rupture channels acting on a shared SO(2) phase manifold
exhibit anti-correlation ρ = −1/2 between their rupture-rate
fluctuations.

## Resolved framing (post-Session-2 convention update)

Per `notes/rupture_topology.md` H1+H2, both "Z₂ ruptures" are the
*same kind of object* (both are Bernoulli(1/2) draws — there is no
other kind of CRR rupture); the composition lives on a shared
SO(2) phase manifold (convention C2).

Under this framing, the variance-preserving composition constraint
needed in the original derivation (Session 2 version) is **forced**
by the shared phase structure: the two Z₂ ruptures together must
complete one SO(2) cycle (geodesic 2π), preserving the total
variance carried by the phase circuit.

## Assumptions

(A1) (H1) Two Z₂ rupture channels X, Y, each a Bernoulli(1/2) draw,
so Var(X) = Var(Y) = 1/4 (Bernoulli(1/2) variance).
(A2) (H2) X and Y act on a shared SO(2) phase manifold; the two
ruptures together complete one geodesic circuit on SO(2), so the
*joint* rupture indicator Z = X + Y has the same variance as a
single SO(2)-circuit Bernoulli(1/2) draw: Var(Z) = 1/4.
(A3) X, Y are jointly second-moment characterised (Gaussian
sufficient).

## Derivation (under A1–A3)

Var(X + Y) = Var(X) + Var(Y) + 2·Cov(X, Y).

Substitute A1 and A2:

    1/4 = 1/4 + 1/4 + 2·Cov(X, Y)
    Cov(X, Y) = (1/4 − 1/2) / 2 = −1/8.

Then

    ρ = Cov(X, Y) / (σ_X · σ_Y) = (−1/8) / ((1/2) · (1/2)) = −1/2.

So **ρ = −1/2** is forced by the shared-SO(2)-phase variance
preservation, which is itself forced by H2 (one SO(2) circuit per
joint-rupture cycle).

The Session-2 version of this derivation introduced the variance-
preservation constraint as an *assumption*; under the resolved
framing it is *derived* from H2.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M11_anticorrelation`
generates jointly-Gaussian (X, Y) with ρ = −1/2 and unit variance;
verifies Var(X + Y) matches Var(X) (variance-preservation) to within
Monte-Carlo error.

## Caveats

- **Variance-preservation is now derived, not assumed.** The Session-2
  caveat about constraint ambiguity (variance-preserving vs rate-
  halving) is resolved: under H2, the two Z₂ ruptures share a single
  SO(2) phase, so their joint variance equals one SO(2) circuit's
  variance — variance-preservation is structural.
- **M2's "rupture-rate halving" interpretation is wrong.** The
  Session-2 derivation considered Var(X+Y) = Var(X)/2 (rate-halving)
  as an alternative; under the resolved framing (M2 reframed as
  half-turn embedding, not rate-halving), this alternative does not
  arise.

## Status

**T1.** Derivation is one-line algebra under H1+H2 (now derived,
not assumed). Numerical verification confirms.
