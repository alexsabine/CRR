# M20 — Derivation: R[χ] is the right Kan extension

## Claim

In the categorical formulation of CRR, the regeneration operator
R[χ] is the right Kan extension of the coherence-history functor
along the rupture-inclusion functor.

## Assumptions

(A1) The "history category" H has objects (t, C(t)) — time-coherence
pairs — and morphisms given by causal precedence (t' ≤ t, C
non-decreasing).
(A2) The "rupture category" Δ has a single distinguished object δ
(the rupture instant) and identity morphisms.
(A3) The inclusion functor i : Δ ↪ H sends δ to the rupture-time
object (t_rupture, C(t_rupture)).
(A4) The "coherence-history functor" F : H → Set (or to a
probability-distribution category) sends each (t, C(t)) to the
weighted-past distribution exp(C/Ω) at that time.

## Derivation (under A1–A4)

**Right Kan extension (definition).** For functors F : H → C and
i : H' → H, the right Kan extension Ran_i F : H' → C is the
universal functor satisfying

    Hom(G ∘ i, F) ≅ Hom(G, Ran_i F)

for any G : H' → C. Equivalently, Ran_i F is computed pointwise as
an *end* (limit over a comma category):

    (Ran_i F)(δ) = lim_{(h, i(δ) → h)} F(h).

Under A1–A4: the comma category for δ ∈ Δ has objects
(h ∈ H, morphism i(δ) → h), i.e., points in the history category
that are *causal future* of the rupture instant. The limit over this
diagram, evaluated by the coherence-weighted distribution F, gives
the *future-conditioned* coherence-weighted past — which is exactly
the regeneration integral R[χ] up to the φ-factor:

    (Ran_i F)(δ) = ∫₋∞^{t_δ} φ(τ) · exp(C(τ)/Ω) · Θ(t_δ − τ) dτ.

The Kan-extension structure justifies the *uniqueness* of the
regeneration: any natural-transformation-respecting "extrapolation
from rupture" must factor through R[χ]. This is Mac Lane's
formal-categorical analogue of "best causal reconstruction."

## Numerical verification

Direct numerical verification of a Kan extension is difficult (it's
a universal property, not a computation). Instead,
`crr-engine/tests/test_derivations.py::test_M20_kan_universal_property`
checks the universal property in a *finite discrete* version: build
a small finite history poset, construct two candidate "extensions"
G₁, G₂, and verify that the unique factorisation through R[χ]
(constructed as the pointwise end) agrees with both candidates.

## Caveats

- **The categorical formulation is *new* canonical material in CRR;
  it is not a relabelling of an existing classical theorem.** The
  Kan-extension picture is canonical category theory, but the
  *identification* of R[χ] as a Kan extension is a CRR contribution
  (see `crr_first_principles_proofs.md`, `CRR_Bounded_Kan_Extension_QED_v2.pdf`).
- **The categorical formulation is one of three equivalent CRR
  meta-theorems** (categorical / variational / information-theoretic);
  this derivation establishes only the categorical one.
- **The bridge from categorical to analytic** (writing the end as
  the integral) requires the comma-category indexing set to be
  measure-theoretically rich enough. For continuous time, this is
  standard but requires the "enriched" Kan-extension formalism
  (Kelly, *Basic Concepts of Enriched Category Theory*, 1982).

## Status

**T1.** Derivation is the universal property of right Kan extensions
applied under the stated identifications. Verification numerical for
the discrete case.
