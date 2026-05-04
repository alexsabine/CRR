# M1 — current tier

**Tier: T1 (conjecture).**

**Justification:** T1. Derivation under Bernoulli(1/2) noise model; numerical verification via test_M1_cv_equals_omega_over_2. Caveat: A3 (the noise model) is the load-bearing assumption — see derivation.md.

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
