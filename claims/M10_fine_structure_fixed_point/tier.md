# M10 — current tier

**Tier: T1 (conjecture).**

**Justification:** T1. Numerical verification confirms unique stable fixed point at 1/α = 137.0324 (test_M10_fine_structure_fixed_point and test_M10_unique_stable_fixed_point). Caveat: 26 ppm discrepancy with CODATA 1/α = 137.0360 is six orders of magnitude beyond CODATA precision. Equation derivation from CRR first principles deferred to Session 3+.

**Promoted from T0** in Session 2 by `derivation.md` in this directory
and the corresponding pytest case(s) in
`crr-engine/tests/test_derivations.py`.

**Promotion gates ahead:**
- **T2** requires `consistency.md` reproducing an independent empirical
  regularity (Session 3).
- **T3** requires `prediction.md` (committed before data fetch) and
  `result.md` confirming on untouched data (Session 4).
- **T4** requires `independent.md` citing replication by an
  unaffiliated group (Session 6 audit).
