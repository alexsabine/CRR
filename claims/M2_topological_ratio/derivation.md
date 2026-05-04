# M2 — Derivation: Z₂:SO(2) CV ratio = 2 (topological)

## Claim

Z₂:SO(2) CV ratio is exactly 2, derived from the topological
embedding of Z₂ as a half-turn inside SO(2).

## Resolved framing (post-Session-2 convention update)

Per `notes/rupture_topology.md` H1+H2, "Z₂" and "SO(2)" in the
canonical brief refer to *different types of object*:

- **Z₂** is the rupture topology (always Z₂, by H1).
- **SO(2)** is a continual memory-bearing manifold.

The 2:1 ratio reported by the brief is the ratio between:

- **Z₂-rupture-only** (no continuous-phase memory): geodesic π
  (half-turn embedding of the Z₂ subgroup inside the parent
  manifold).
- **Z₂-rupture-on-SO(2)-phase**: geodesic 2π (one full circuit of
  the SO(2) phase manifold).

This is a **topological half-turn embedding**, not a comparison
between two substrates.

## Assumptions

(A1) (H1, H2) Rupture is Z₂; SO(2) is the continual phase manifold.
(A2) Ω = 1/φ_geodesic (convention C4 in `notes/conventions.md`).
(A3) The Z₂ subgroup of SO(2) acts by antipodal identification
θ ~ θ + π. The quotient SO(2)/Z₂ is a circle of length π.
(A4) M1: CV = Ω/2 (independent of phase manifold).

## Derivation

By A3: SO(2) has closed-geodesic length 2π. The Z₂ quotient
SO(2)/Z₂ has length π.

By A2:
- φ_Z₂ = π (length of the half-turn embedding of Z₂)
- φ_SO(2) = 2π (length of the closed geodesic of SO(2))

Hence
- Ω_Z₂ = 1/π
- Ω_SO(2) = 1/(2π)

Ratio:

    Ω_Z₂ / Ω_SO(2) = (1/π) / (1/(2π)) = 2.

By A4:
- CV_Z₂ = 1/(2π)
- CV_SO(2) = 1/(4π)

Ratio:

    CV_Z₂ / CV_SO(2) = 2.

The factor of 2 is **|Z₂|** — the order of the Z₂ subgroup acting
on SO(2). This generalises (M22) to any compact connected Lie group
G containing a discrete subgroup H: the rupture-only-vs-phase ratio
is |H|.

## Numerical verification

- `crr-engine/tests/test_engine.py::test_topological_ratio_exactly_two`
  asserts the 2:1 Ω-ratio to machine precision.
- `crr-engine/tests/test_rupture_topology.py::test_M2_resolved_z2_is_half_turn_in_so2`
  asserts the embedding π = 2π / 2 explicitly.
- `crr-engine/tests/test_engine.py::test_cv_ratio_exactly_two` —
  inherited CV ratio.

## Caveats

- Resolved as **topological embedding**, not "two substrates with
  different geodesic conventions." The brief's "Z₂ open arc /
  SO(2) ring" wording is misleading; recommended edit in
  `notes/conventions.md` §"What the canonical brief should say."
- M22 generalises: for any compact connected Lie group G containing
  Z₂ as discrete subgroup, the rupture-only embedding has geodesic
  φ_G / 2.

## Status

**T1.** Derivation is the topological half-turn embedding under
convention C4. Verified numerically to machine precision.
