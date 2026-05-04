# M15 — Derivation: Z_n hierarchy CV = n/(4π)

## Claim

For a Z_n cyclic-symmetry substrate (n ≥ 2), CV = n/(4π).

## Assumptions

(A1) The Z_n substrate has geodesic length 2π/n (the arc spanning
one fundamental domain of the n-fold cyclic symmetry on the unit
circle).
(A2) Ω = 1 / φ_geodesic ⇒ Ω_{Z_n} = n/(2π).
(A3) CV = Ω/2 (M1).

Wait. Under (A1) Ω = 1/(2π/n) = n/(2π), and CV = Ω/2 = n/(4π). For
n = 2 this gives CV = 2/(4π) = 1/(2π) ✓ (matches Z₂). But the
canonical SO(2) value is CV = 1/(4π), which corresponds to n = 1 —
not to the n → ∞ limit. The natural reading is that SO(2) is the
*continuous limit* not in the Z_n discrete sequence; the n = 1 case
of the formula gives the same number as SO(2) by coincidence
(or by a consistency built into the canonical convention).

## Derivation (under A1–A3)

Step 1 (geodesic length). A Z_n substrate partitions the unit circle
into n equal arcs; each fundamental domain has length 2π/n. Adopt
this as φ_geodesic^{Z_n}.

Step 2 (Ω). Ω_{Z_n} = 1 / φ_geodesic = n/(2π).

Step 3 (CV). CV_{Z_n} = Ω_{Z_n}/2 = n/(4π).

Sanity checks at the canonical endpoints:
- n = 2 (Z₂): CV = 2/(4π) = 1/(2π) ≈ 0.1592 ✓.
- n → ∞: CV → ∞, which would mean increasingly noisy. The brief
  reports SO(2) (continuous rotation) at CV = 1/(4π) ≈ 0.0796 — an
  *extremum*, not a limit of Z_n. So the SO(2) value lies *outside*
  the Z_n discrete sequence; geometrically, "all-the-way-continuous"
  has a different geodesic identification (full circle 2π, not a
  vanishing fundamental domain).

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M15_zn_hierarchy_at_n2`
asserts the n=2 instance equals canonical Z₂ to machine precision.

## Caveats

- **The relationship between Z_n and SO(2) in this formula is not
  monotone.** Z_2 sits at CV = 1/(2π); Z_3 at 3/(4π); Z_4 at 1/π;
  …; SO(2) at 1/(4π). The Z_n sequence increases with n; SO(2) is
  smaller than every Z_n (n ≥ 2). Whether this is intended or
  evidence of a missing ingredient (e.g., n in denominator instead of
  numerator) needs author confirmation.
- The geodesic-length identification φ_geodesic = 2π/n for Z_n is
  the most natural choice but is one of several geometric
  conventions; alternatives (e.g., φ_geodesic = 2π for the full
  circle traversed n times) would invert the formula.
- Recorded as a candidate **inconsistency to escalate** in
  `notes/relabellings.md`: the Z_n formula CV = n/(4π) does not
  smoothly connect to the SO(2) value, contrary to the language of
  "hierarchy."

## Status

**T1 with caveat.** The derivation under A1–A3 is algebraic and
internally consistent at n = 2. The behaviour at large n and the
SO(2) endpoint is not a smooth limit of the formula; this is flagged
for the framework's author. Tier capped at T1 pending resolution.
