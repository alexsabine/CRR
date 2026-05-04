# M22 — current tier

**Tier: T1 (conjecture).**

**Justification:** Derivation in `derivation.md` rests on M1
(CV = Ω/2 from Bernoulli rupture, independent of phase manifold)
plus the identification "mean inter-rupture interval = one
closed-geodesic excursion on G." Numerical verification across six
compact Lie groups (Z₂, SO(2), SU(2), SO(3), T², SU(3)) in
`crr-engine/tests/test_rupture_topology.py::test_H3_lie_group_cv_scaling`,
plus two exact-equality structural tests (SU(2)≡SO(2), SO(3)≡Z₂ in
CV).

**Promoted from T0 → T1** in the convention-resolution session
following Session 2, prompted by the user's hypothesis "stretch the
framework to any Lie group or geometric structure where Z₂ is the
discrete cut and the phase / SO(2) structure is the continual
memory-bearing manifold." Hypotheses H1 (rupture is Z₂) and H2 (G is
memory manifold) are formalised in `notes/rupture_topology.md`.

**Promotion gates ahead:**
- **T2** requires `consistency.md` reproducing the CV prediction on
  at least one non-SO(2) Lie-group-symmetric system from public
  data. Sharpest tests: SO(3)-symmetric rigid bodies (CV = 1/(2π))
  and SU(2)-symmetric spin-1/2 systems (CV = 1/(4π)).
- **T3** requires a pre-registered prediction on untouched data —
  e.g., CV measurement on a system whose Lie-group symmetry is
  identified *before* the CV is measured.
- **T4** requires independent confirmation by an unaffiliated group.

**Sharpest falsifiers:** the SU(2) ≡ SO(2) and SO(3) ≡ Z₂ CV-equality
predictions. If a SU(2)-symmetric system's CV differs systematically
from the SO(2) CV by more than Bernoulli sampling noise, M22 falls.
