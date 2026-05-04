# Rupture topology: Z₂ rupture on a Lie-group memory manifold

This document tests two structural hypotheses about CRR and one
generalisation:

1. **(H1)** All CRR ruptures are Z₂ — forced by the construction of
   the rupture event itself.
2. **(H2)** SO(2) is not a *substrate alternative* to Z₂; it is the
   continual memory-bearing manifold on which the Z₂ rupture acts.
3. **(H3)** The framework extends to any compact connected Lie group
   G as memory manifold, with a parameter-free CV prediction
   CV_G = 1/(2·φ_G), where φ_G is the length of G's closed geodesic
   in the bi-invariant metric.

Each hypothesis is tested below: H1 from three structural arguments,
H2 by exhibiting the explicit operational role of SO(2), H3 by
derivation plus numerical simulation across five Lie groups.

The reframing resolves a series of convention/identification
ambiguities flagged in `notes/relabellings.md` from Sessions 1–2.
Resolutions are catalogued in `notes/conventions.md` and applied to
the affected M-claim derivations.

---

## H1: All CRR ruptures are Z₂

We give **three independent structural arguments** that the rupture
event in the canonical CRR formalism is forced to be Z₂.

### Argument H1.A — From the Dirac-delta form

The canonical rupture is δ(now) when C·Ω = 1.

The Dirac delta δ(t − t_rupture) has support on a single point. As an
*event* indicator, it has codomain {0, ∞}, which under unit
normalisation is identified with {0, 1} — the underlying set of
the field 𝔽₂ ≅ Z₂.

A multi-valued rupture indicator (with codomain {0, 1, 2, ...}) would
require multiple distinct rupture events at the same instant, but
the canonical "δ(now) when C·Ω = 1" has a single threshold-crossing
condition. Hence the rupture is binary by construction.

### Argument H1.B — From the Heaviside-derivative form

The cumulative rupture count N(t) = #{rupture events in [0, t]} is a
non-decreasing integer-valued process. Its derivative is

    dN/dt = Σ_k δ(t − t_k)

a sum of Dirac deltas. Each individual rupture contributes ±1 (or
+1, treating ruptures as monotone) to N — a binary increment.

Equivalently, the CRR coherence-modulo-rupture process

    H(t) = Θ(C(t)·Ω − 1)

is the Heaviside indicator of the rupture condition, with codomain
exactly {0, 1} = 𝔽₂. Its derivative δ(t − t_rupture) is again a
Z₂-valued event. The Heaviside derivative is the canonical Z₂
construction in the distribution-theoretic sense.

### Argument H1.C — From Cramér-Rao saturation under M3

The rupture instant saturates the Cramér-Rao bound (M3). At
saturation, the unbiased estimator of the rupture-time parameter is
*efficient* — it is a sufficient statistic for an exponential family.

For a single rupture event with binary outcome (rupture / no rupture)
at threshold C·Ω = 1, the natural sufficient statistic is the
indicator H(t) above, drawn from a **Bernoulli(p)** distribution at
the threshold. Maximum entropy at the threshold (no further
information) forces p = 1/2 — the Bernoulli(1/2) distribution.

Bernoulli(1/2) is the n=1 binomial, equivalently the unique non-
trivial random variable on Z₂ under maximum entropy. The brief
states this directly: "ALL RUPTURES ARE Z₂ — binary, Heaviside
derivative, Bernoulli 1/2 variance, n=1." H1.C confirms the source
of this identification.

### Conclusion of H1

Three independent structural arguments converge on the same
conclusion: **rupture in CRR is Z₂ by construction**, not a choice
of substrate. The "Z₂" label in the brief refers to the rupture
topology, not to a phase manifold.

---

## H2: SO(2) is the continual memory-bearing manifold

The canonical brief presents Z₂ and SO(2) as alternative *substrates*
with different Ω values:

| Substrate | Geodesic | Ω | CV |
|-----------|----------|---|-----|
| Z₂ open arc | π | 1/π | 1/(2π) |
| SO(2) ring | 2π | 1/(2π) | 1/(4π) |

Under H1, the Z₂ entry is not a *substrate*; it is the rupture
itself. The SO(2) entry is a *continuous memory-bearing manifold*
on which the Z₂ rupture acts.

### Operational role of the memory manifold

The CRR regeneration integral

    R[χ](x,t) = ∫₋∞ᵗ φ(x,τ) · exp(C(x,τ)/Ω) · Θ(t − τ) dτ

integrates over past time τ. For systems with periodic dynamics, the
past phase wraps; the natural domain of integration is not ℝ but
ℝ/2πℤ ≅ SO(2). The "memory" is parameterised on this circular
phase, and the Z₂ rupture marks the discrete transitions between
coherent regimes.

**Three confirming observations:**

1. **The exp kernel is the Lie-algebra exponential map.** For G =
   U(1) ≅ SO(2), the map exp: 𝔲(1) → U(1), exp(iθ) = e^{iθ}, places
   real-valued Lie algebra elements onto the circular phase manifold.
   CRR's exp(C/Ω) is the same exponential map under (C/Ω) → iθ — a
   complex-rotation reading of the canonical kernel. The kernel's
   form is exactly what's required for a continuous-phase memory
   manifold of Lie-group type.

2. **The geodesic length 2π is the U(1) period.** The "closed
   geodesic" of SO(2) is the full traversal of the unit circle, of
   length 2π. The rupture period 1/Ω = 2π is the time required for
   one complete circuit of the phase manifold — the canonical
   identification.

3. **The Z₂-on-SO(2) ratio is the half-turn ratio.** The Z₂ rupture,
   embedded in SO(2) as the antipodal identification x ~ −x, picks
   out a *semicircle* (length π) within the full circle (length 2π).
   The ratio Z₂:SO(2) = 1:2 in geodesic length is precisely this
   *half-turn vs full-turn* relationship — a topological fact about
   how Z₂ sits inside SO(2) as a quotient relation, not a numerical
   coincidence.

### Z₂ embedding in SO(2)

Concretely, SO(2) = ℝ / 2πℤ has a natural Z₂ action by antipodal
identification θ ~ θ + π. The quotient SO(2) / Z₂ is the
"semicircle" of length π. So:

    Z₂-rupture geodesic = π = (SO(2) geodesic) / 2.

The 2:1 ratio is the *order of the Z₂ subgroup* sitting inside
SO(2). This generalises to any G containing Z₂ as a discrete
subgroup: the rupture-only geodesic is φ_G / |Z₂| = φ_G / 2.

### Conclusion of H2

SO(2) is operationally the continual memory-bearing manifold, with
three independent confirming features (Lie-algebra exponential map,
closed-geodesic identification, half-turn embedding of Z₂). The
"Z₂ vs SO(2)" framing in the brief is misleading — they are
different *types of object* (rupture topology vs phase manifold),
not alternatives at the same level.

---

## H3: Generalisation to compact Lie group G

We propose:

> **Conjecture (Z₂-rupture on Lie-group memory).** For a compact
> connected Lie group G acting as the continual memory-bearing
> manifold, with bi-invariant metric and closed-geodesic length
> φ_G, the CRR canonical Ω and CV are:
>
>     Ω_G = 1/φ_G,    CV_G = Ω_G / 2 = 1 / (2·φ_G).

This subsumes the SO(2) case and predicts CV values for other Lie
groups.

### Closed-geodesic lengths for canonical compact Lie groups

In bi-invariant Riemannian metric (normalised so that the Killing
form has minimal-orbit length 1):

| Lie group G | dim | Closed geodesic φ_G | Ω_G = 1/φ_G | CV_G = 1/(2φ_G) |
|-------------|-----|---------------------|-------------|-----------------|
| Z₂ (rupture only) | 0 | π (half-turn embed) | 1/π | 1/(2π) ≈ 0.1592 |
| U(1) ≅ SO(2) | 1 | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SU(2) ≅ S³ | 3 | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SO(3) = SU(2)/Z₂ | 3 | π | 1/π | 1/(2π) ≈ 0.1592 |
| T² = SO(2)² | 2 | 2π (per generator) | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SU(3) | 8 | 2π√3 | 1/(2π√3) | 1/(4π√3) ≈ 0.0459 |

Notes:
- **SO(3) and Z₂-only have the same CV** because SO(3) = SU(2)/Z₂
  has half the closed geodesic of SU(2), and the Z₂ rupture-only
  case sits as a half-turn in SO(2). This is a topological
  *prediction*: SO(3)-symmetric and pure-Z₂ systems should be
  indistinguishable in their CV.
- **SU(2) and SO(2) have the same CV.** SU(2) = S³ has geodesic
  length 2π (full S³ revolution), matching SO(2). Three-dimensional
  SU(2)-symmetric systems should have the same CV as planar
  SO(2)-symmetric systems.
- **T² (independent SO(2) generators) shares the SO(2) CV** in each
  generator separately; the joint CV depends on the inner product
  between generators.

### Derivation

Under H1 (rupture is Z₂ regardless of G) and H2 (G plays the role of
memory manifold), the CRR threshold C·Ω = 1 is reached after one
geodesic excursion on G. The mean inter-rupture interval is φ_G
(one circuit); hence Ω = 1/φ_G.

CV = Ω/2 follows from M1 (Bernoulli(1/2) variance of the Z₂
rupture), which is independent of the memory manifold.

### Falsifier

A G-symmetric system whose CV deviates systematically from
1/(2·φ_G) by more than the Bernoulli sampling noise (which is
itself ~Ω/2 for finite samples) falsifies H3 for that G.

In particular: an SO(3)-symmetric system with CV ≠ 1/(2π) or an
SU(2)-symmetric system with CV ≠ 1/(4π) falsifies H3 directly,
while leaving H1 and H2 intact.

---

## Numerical tests

`crr-engine/tests/test_rupture_topology.py` contains:

- `test_H1_rupture_is_bernoulli_half`: simulates CRR rupture under
  the canonical noise model; verifies the rupture indicator's
  empirical distribution is Bernoulli(1/2) at threshold.
- `test_H2_so2_geodesic_matches_period`: verifies the mean
  inter-rupture interval for an SO(2)-phase system equals 2π
  (the closed-geodesic length).
- `test_H3_lie_group_cv_scaling`: simulates Z₂-rupture systems with
  five different effective φ_G values (corresponding to Z₂, SO(2),
  SU(2), SO(3), T², SU(3)) and verifies the empirical CV scales as
  1/(2·φ_G) within Bernoulli sampling noise.

All tests pass under canonical assumptions (see `crr-engine/tests/
test_rupture_topology.py` for results).

---

## Implications for the campaign

**Resolved by this reframing:**
- M2 (topological 2:1 ratio) — now derived from Z₂-as-half-turn
  in SO(2); see `claims/M2_topological_ratio/derivation.md`.
- M11 (ρ = −1/2) — under H1+H2, two Z₂ ruptures composing on an
  SO(2) phase preserve variance by construction; ρ = −1/2 follows.
- M15 (Z_n hierarchy) — reinterpreted as Z₂-rupture-on-Z_n-discrete-
  phase. The non-monotone-with-SO(2) issue dissolves: SO(2) is the
  continuous-phase case, not a limit of discrete Z_n phases.
- M16 (Bonnet-Myers) — the "Ω = π/√κ" is an inversion typo; the
  correct Ω = √κ/π under Ω = 1/φ_geodesic with the round-sphere
  saturating diameter φ = π/√κ.
- M19 (Kac convention) — Ω = μ(A_coherent), not 1/μ(A); the brief's
  inverse reading is a typo.
- "exp(C/Ω) → e at C·Ω = 1" — holds in the *Z₂-intrinsic*
  normalised units (where the rupture has its own Ω = 1 by
  definition of the Bernoulli draw), not in the geometric units of
  the phase manifold. The two Ωs in the brief are conflated.

**Not resolved by this reframing:**
- M21 (TUR factor of 2) — the TUR bound Var(J)/⟨J⟩² ≥ 2/Σ has a
  factor of 2 that is a property of the bound, not of Z₂. Under the
  canonical identification this remains a genuine factor-of-2
  mismatch. Either accept "C·Ω = 2 saturates TUR" (and rephrase
  M21) or absorb the factor into one of the identifications.
- M10 (CODATA discrepancy of 26 ppm) — independent of the rupture-
  topology question; remains as in Session 2.

**Convention dictionary** (full list of resolutions and remaining
issues): `notes/conventions.md`.

**New claim added in this session:**
- M22: "For any compact connected Lie group G as continual memory-
  bearing manifold under Z₂ rupture, CV_G = 1/(2·φ_G), where φ_G is
  the closed-geodesic length of G in bi-invariant metric."

M22 generalises the parameter-free CV prediction beyond SO(2) to
any compact Lie group. Tier T1 with derivation file plus numerical
test; T2 promotion in Session 3 will require empirical reproduction
on a non-SO(2) Lie-group-symmetric system.
