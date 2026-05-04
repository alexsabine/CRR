# M2 — Derivation: Z₂:SO(2) CV ratio = 2 (topological)

## Claim

Z₂:SO(2) CV ratio is exactly 2, derived from the arc-to-ring topology
of the substrate.

## Assumptions

(A1) The canonical Ω of a substrate equals the inverse of its geodesic
length: Ω = 1 / φ_geodesic.
(A2) The Z₂ substrate is a *closed open arc* with geodesic length π
(diameter of the unit circle).
(A3) The SO(2) substrate is the *circle* with geodesic length 2π.
(A4) CV = Ω/2 holds (claim M1, derived separately).

## Derivation

By A1, A2: Ω_{Z₂} = 1/π.
By A1, A3: Ω_{SO(2)} = 1/(2π).
Hence Ω_{Z₂} / Ω_{SO(2)} = (1/π) / (1/(2π)) = 2.

By A4: CV = Ω/2, so the CV ratio inherits the Ω ratio:
CV_{Z₂} / CV_{SO(2)} = Ω_{Z₂} / Ω_{SO(2)} = 2.

The factor 2 is the ratio of geodesic lengths 2π : π, which is the
topological double cover of the circle by its "diameter" interval.

## Numerical verification

`crr-engine/tests/test_engine.py::test_topological_ratio_exactly_two`
asserts `omega_canonical("Z2") / omega_canonical("SO2") == 2.0` to
machine precision (1e-12). `test_cv_ratio_exactly_two` verifies the
inherited ratio.

## Caveats

- A1 (Ω = 1/φ_geodesic) is a *definition* in the canonical brief; M2
  inherits whatever justification A1 has. If the geodesic-length
  identification is challenged, M2 falls with it.
- A4 (CV = Ω/2, claim M1) is a *separate* claim with its own
  derivation; M2 is derivative on M1's status.
- The "open arc" of length π for Z₂ is one geometric realisation of
  the two-point-set carrier of Z₂ (interval connecting fixed points
  on the circle); other realisations would give different lengths.
  The choice is canonical but not forced.

## Status

**T1.** Derivation is two algebraic steps under stated assumptions;
numerical verification is exact to machine precision.
