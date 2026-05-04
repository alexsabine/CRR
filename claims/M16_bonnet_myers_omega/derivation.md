# M16 — Derivation: Bonnet-Myers gives Ω = π/√κ

## Claim

On a positively curved statistical manifold with Ricci curvature
≥ (n−1)κ (κ > 0), the canonical Ω is bounded by Ω = π/√κ via the
Bonnet-Myers diameter inequality.

## Assumptions

(A1) The statistical manifold is a complete Riemannian n-manifold
with Ricci curvature satisfying Ric ≥ (n−1)κ everywhere, κ > 0.
(A2) Ω is identified with the diameter of the manifold (or more
precisely, with the geodesic length scale Ω = 1/φ_geodesic, where
φ_geodesic is the maximum geodesic length on the manifold).

Wait — the canonical brief identifies Ω = 1/φ_geodesic, so a *small*
Ω corresponds to a *long* geodesic, and a *large* Ω to a *short*
geodesic. The Bonnet-Myers theorem gives an *upper* bound on
geodesic length (diameter ≤ π/√κ), hence a *lower* bound on Ω. So
the claim should read Ω ≥ √κ/π, not Ω = π/√κ. Verifying:

Bonnet-Myers (1941): under A1, the diameter D of the manifold
satisfies D ≤ π/√κ.

If φ_geodesic = D, then Ω = 1/D ≥ √κ/π.

So the equality form of the claim — Ω = π/√κ — corresponds to
*diameter saturation*, i.e., when the manifold is a *round
sphere* of constant sectional curvature κ. Then D = π/√κ exactly,
and (using the *direct* identification φ_geodesic = D) Ω = π/√κ.

Hmm, but π/√κ would be the diameter, not Ω = 1/diameter. The brief
appears to invert the convention. Reading the brief literally:
Ω = π/√κ. This is *not* consistent with Ω = 1/φ_geodesic when
φ_geodesic = π/√κ (then Ω = √κ/π). This is an apparent inconsistency.

## Derivation (under A1, plus a corrected A2)

Let me proceed under the corrected A2': **Ω is identified with the
geodesic length φ_geodesic** (not its inverse) — only on the
positively-curved manifold case where the geodesic length itself
plays the role of the "characteristic precision scale."

Bonnet-Myers (Myers, 1941): For a complete Riemannian n-manifold
with Ric ≥ (n−1)κ > 0, the diameter satisfies D ≤ π/√κ. Equality
holds iff the manifold is the round sphere S^n(1/√κ).

Taking the saturating case: D = π/√κ. Under A2': Ω = π/√κ.

So *on the round sphere*, Ω = π/√κ exactly.

For lower-curvature manifolds satisfying A1, Ω ≤ π/√κ (the diameter
is shorter, and Ω inherits the bound).

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M16_bonnet_myers_sphere`
constructs the unit 2-sphere (κ = 1, n = 2), verifies the geodesic
diameter equals π = π/√1, and confirms Ω = π under A2'. Counter-
example (planar manifold, κ → 0) returns infinite diameter and
Ω → ∞, confirming the bound is non-trivial.

## Caveats

- **A2 / A2' inconsistency in the canonical brief.** The brief
  defines Ω = 1/φ_geodesic *and* asserts Ω = π/√κ on a positively-
  curved manifold. These are inconsistent unless φ_geodesic varies
  inversely with √κ, which is not a Bonnet-Myers consequence.
  Recorded in `notes/relabellings.md`. Resolution requires the
  framework's author to choose between A2 (Ω = inverse length) and
  A2' (Ω = length).
- **Bonnet-Myers gives a bound, not an equality.** Asserting
  Ω = π/√κ requires the *saturation* (round-sphere) case. For
  general positively-curved manifolds, Ω ≤ π/√κ (under A2'). The
  canonical statement should read "Ω attains π/√κ on round spheres
  and is bounded above by π/√κ otherwise."
- **Rauch comparison theorem** gives a more refined bound when only
  sectional curvatures (not Ricci) are bounded; canonical brief's
  statement implicitly chooses the Ricci form (most general for
  diameter bounds).

## Status

**T1 with major caveat.** The Bonnet-Myers theorem is canonical and
the round-sphere saturation gives the equality form. But the brief's
identification Ω = 1/φ_geodesic is inconsistent with Ω = π/√κ unless
the Ω-convention is corrected. Tier capped at T1 pending convention
resolution.
