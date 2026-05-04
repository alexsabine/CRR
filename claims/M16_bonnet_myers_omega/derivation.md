# M16 — Derivation: Bonnet-Myers gives Ω ≥ √κ/π (saturating round sphere)

## Claim (corrected statement)

On a positively-curved compact statistical manifold with Ricci
curvature ≥ (n−1)κ (κ > 0), the canonical Ω is bounded below by
√κ/π via the Bonnet-Myers diameter inequality:

    Ω ≥ √κ/π,    saturating on the round sphere of curvature κ.

## Resolved framing (post-Session-2 convention update)

The brief states "Ω = π/√κ." This is an inversion of the correct
formula. Under convention C4 (`notes/conventions.md`: Ω = 1/φ_geodesic),
Bonnet-Myers gives an *upper* bound on geodesic length and hence a
*lower* bound on Ω.

The Session-2 derivation flagged this as a major caveat. It is now
resolved as a typo in the brief; the corrected form is
**Ω ≥ √κ/π**, with equality on the round sphere.

## Assumptions

(A1) The statistical manifold is a complete Riemannian n-manifold
with Ricci curvature satisfying Ric ≥ (n−1)κ everywhere, κ > 0.
(A2) Convention C4: Ω = 1/φ_geodesic, where φ_geodesic is the
diameter (or closed-geodesic length) of the manifold.

## Derivation (under A1, A2)

**Bonnet-Myers theorem (Myers, 1941).** For (M, g) a complete
Riemannian n-manifold with Ric ≥ (n−1)κ, κ > 0, the diameter D
satisfies

    D ≤ π/√κ,

with equality iff M is the round sphere S^n(1/√κ).

By A2: Ω = 1/D, so

    Ω = 1/D ≥ √κ/π,

with equality iff M is the round sphere S^n(1/√κ).

**Saturating case (round sphere of curvature κ):** D = π/√κ exactly,
so Ω = √κ/π exactly. For example:
- Unit 2-sphere (κ = 1): D = π, Ω = 1/π. (Matches the canonical
  Z₂-rupture Ω = 1/π — the unit 2-sphere is the natural geometric
  realisation of the half-turn embedding.)
- 2-sphere of radius r (κ = 1/r²): D = πr, Ω = 1/(πr).

## Numerical verification

- `crr-engine/tests/test_derivations.py::test_M16_bonnet_myers_sphere`
  verifies the unit-2-sphere diameter equals π = π/√1.
- `crr-engine/tests/test_rupture_topology.py::test_M16_resolved_omega_inversion`
  verifies the corrected formula Ω = √κ/π for κ = 4 and shows it
  is the multiplicative inverse of the brief's stated π/√κ.

## Caveats

- **Brief contains a typo.** The recommended edit is "Ω ≥ √κ/π,
  saturating on the round sphere" (per `notes/conventions.md`
  §"What the canonical brief should say"). I do not modify the
  canonical text per `CAMPAIGN.md` non-goals; the correction lives
  in this derivation file.
- **For non-saturating manifolds (Ric > (n−1)κ strictly), the bound
  is strict.** Generic positively-curved manifolds give Ω > √κ/π
  (i.e., shorter diameter than the round-sphere bound).
- **Rauch comparison theorem** gives a tighter bound when sectional
  curvatures (not just Ricci) are bounded; the canonical statement
  uses the Ricci form for full generality.
- **Connection to M22:** the round sphere of curvature κ has
  φ_diameter = π/√κ. Under M22's Lie-group framework, the round
  sphere is not a Lie group itself (S^n is a Lie group only for
  n = 0, 1, 3 — corresponding to ℤ/2ℤ, U(1), SU(2)). The M16
  identification therefore applies to a broader class of
  manifolds than M22 (which specifies compact Lie groups).

## Status

**T1.** Inversion typo in the brief is identified and corrected;
the Bonnet-Myers application gives **Ω ≥ √κ/π**, saturating on
round spheres. Numerical verification of the corrected formula in
`test_M16_resolved_omega_inversion`.
