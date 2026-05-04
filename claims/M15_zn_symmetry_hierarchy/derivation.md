# M15 — Derivation: Z_n hierarchy CV = n/(4π)

## Claim

For a Z_n discrete-phase memory manifold under Z₂ rupture, with
fundamental-domain geodesic 2π/n, the canonical CV is

    CV_{Z_n} = n / (4π).

## Resolved framing (post-Session-2 convention update)

Per `notes/rupture_topology.md` H1+H2 and the M22 generalisation,
"Z_n" here refers to a **Z_n discrete-phase memory manifold** —
n equally-spaced phase points on a circle. The Z₂ rupture
(structurally Z₂ by H1) acts on this discrete-phase manifold.

Under this reading:
- The rupture is Z₂ regardless of n.
- The phase manifold is discrete with n points; the geodesic between
  adjacent points is 2π/n.
- The *Session-2 non-monotonicity issue* (Z_n increasing with n vs
  SO(2) at the bottom) dissolves: SO(2) is a *different kind of
  manifold* (continuous-phase), not a limit of the Z_n discrete-
  phase sequence.

## Assumptions

(A1) (H1) Rupture is Z₂.
(A2) (H2) The phase manifold is Z_n: n equally-spaced points on a
unit circle.
(A3) The relevant geodesic is the distance between adjacent rupture
points: φ_{Z_n} = 2π/n.
(A4) Ω_{Z_n} = 1/φ_{Z_n} = n/(2π) (convention C4).
(A5) M1: CV = Ω/2.

## Derivation (under A1–A5)

By A4: Ω_{Z_n} = n/(2π).

By A5: CV_{Z_n} = Ω_{Z_n}/2 = **n/(4π)**.

Sanity checks:
- n = 2 (Z₂ phase): CV = 2/(4π) = 1/(2π) ≈ 0.1592. **Matches the
  canonical Z₂-only CV.** This is consistent because Z_2 = pure-Z₂
  rupture with phase = the rupture itself.
- n = 1 (trivial): CV = 1/(4π) ≈ 0.0796. **Numerically equals the
  SO(2) CV** but for a different reason — n=1 corresponds to a
  single phase point, not to the SO(2) continuous limit.

## Relationship to SO(2) (continuous-phase case)

SO(2) is **not** the n → ∞ limit of Z_n discrete phase. The two
are distinct phase-manifold types:

- **Z_n (discrete-phase):** φ_{Z_n} = 2π/n (distance between adjacent
  discrete points). As n → ∞, φ → 0 and CV → ∞ — divergent.
- **SO(2) (continuous-phase):** φ_{SO(2)} = 2π (closed-geodesic
  length). Fixed, gives CV = 1/(4π).

The Session-2 caveat "Z_n hierarchy is non-monotone with respect to
SO(2)" is resolved: Z_n and SO(2) are different phase-manifold
types, not endpoints of a single hierarchy. The brief's "hierarchy"
language should be reserved for Z₂ ⊂ Z₃ ⊂ Z₄ ⊂ … as a sequence of
*discrete* phase manifolds; SO(2) is a separate continuous case.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M15_zn_hierarchy_at_n2`
asserts the n=2 instance equals canonical Z₂.

For the general n case, the formula CV = n/(4π) follows directly
from CV = Ω/2 (M1, verified) and Ω = 1/φ_{Z_n} (M22-style geodesic
identification, also tested in `test_rupture_topology.py`).

## Caveats

- **Discrete-phase vs continuous-phase distinction is forced.** The
  Z_n manifolds form a discrete-phase family; SO(2) is the
  continuous-phase analogue. They are not connected by a smooth
  limit. Recorded as a clarification in `notes/conventions.md`.
- **Convention for "geodesic" on a discrete manifold.** A Z_n
  discrete manifold has only n points and discrete geodesics; the
  identification φ = 2π/n adopts the embedding of Z_n as the
  vertices of a regular n-gon inscribed in the unit circle.
  Alternative embeddings (e.g., Z_n as the n-th roots of unity in ℂ)
  give the same φ.
- **For n = 2:** the formula reproduces the canonical Z₂-only CV,
  consistent with the rupture-only embedding.

## Status

**T1.** Derivation under the discrete-phase reading; numerical
verification at n = 2. Z_n vs SO(2) non-interpolation is now
resolved as structural, not anomalous.
