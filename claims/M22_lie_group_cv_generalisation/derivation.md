# M22 — Derivation: CV_G = 1/(2·φ_G) for any compact connected Lie group G

## Claim

For a compact connected Lie group G acting as the continual memory-
bearing manifold under Z₂ rupture, with bi-invariant Riemannian
metric and closed-geodesic length φ_G,

    CV_G = 1 / (2 · φ_G).

## Assumptions

(A1) **H1: All ruptures are Z₂.** The rupture event is structurally
Bernoulli(1/2), forced by the Dirac-delta / Heaviside-derivative /
Cramér-Rao saturation arguments in `notes/rupture_topology.md`.

(A2) **H2: G is the continual memory-bearing manifold.** The
regeneration kernel exp(C/Ω) places coherence trajectories on G via
the Lie-group exponential map; the integration domain of the
regeneration integral is canonically G (or a homogeneous space
acted on by G).

(A3) The bi-invariant Riemannian metric on G is well-defined
(automatic for any compact G; chosen so that the smallest closed
geodesic through the identity has length φ_G).

(A4) Mean inter-rupture interval = one closed-geodesic excursion
on G, i.e., E[τ_rupture] = φ_G.

## Derivation (under A1–A4)

By A4: E[τ_rupture] = φ_G.

By M1 (which is independent of the phase manifold; CV = Ω/2 follows
from the Bernoulli(1/2) variance of the Z₂ rupture under A1):

    std(τ_rupture) = (Ω_G / 2) · E[τ_rupture]
                   = (1 / (2 · φ_G)) · φ_G
                   = 1/2.

CV_G = std / mean = (1/2) / φ_G = **1 / (2 · φ_G)**. ∎

Equivalently: Ω_G = 1/φ_G (canonical inverse-geodesic identification,
convention C4 in `notes/conventions.md`), and CV_G = Ω_G/2 from M1.

## Predicted CV values

In bi-invariant metric, for canonical compact Lie groups:

| G | dim | φ_G | Ω_G | CV_G |
|---|-----|-----|-----|------|
| Z₂ (rupture only) | 0 | π | 1/π | 1/(2π) ≈ 0.1592 |
| U(1) ≅ SO(2) | 1 | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SU(2) ≅ S³ | 3 | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SO(3) = SU(2)/Z₂ | 3 | π | 1/π | 1/(2π) ≈ 0.1592 |
| T² (per generator) | 2 | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SU(3) | 8 | 2π√3 | 1/(2π√3) | 1/(4π√3) ≈ 0.0459 |

**Topological predictions (testable consequences):**

- **SU(2) and SO(2) systems are CV-indistinguishable.** Both have
  φ_G = 2π. A SU(2)-symmetric system (e.g., a spin-1/2 particle
  driven through coherence-rupture cycles) should exhibit the same
  CV ≈ 0.080 as a SO(2)-symmetric system (e.g., a planar oscillator).
- **SO(3) and Z₂-only systems are CV-indistinguishable.** Both have
  φ_G = π. A SO(3)-symmetric system (rigid rotor) should exhibit
  CV ≈ 0.159, the same as a binary on/off bistable.
- **The covering relation SU(2) → SO(3) doubles the CV.** This is a
  direct topological consequence of the Z₂ centre of SU(2): SU(2) =
  SO(3) × Z₂ (as bundle), so SO(3) geodesics are *half* as long as
  SU(2) geodesics, doubling Ω and CV.

## Numerical verification

`crr-engine/tests/test_rupture_topology.py` parametrises the test
`test_H3_lie_group_cv_scaling` over the six groups in the table
above, simulates Z₂-rupture systems with the corresponding φ_G
values, computes empirical CVs, and verifies all match the
predicted CV_G to within Bernoulli sampling noise (5% tolerance,
50,000 ruptures per group).

Two structural identities are also verified analytically:

- `test_H3_so3_and_z2_only_have_same_cv` — exact equality.
- `test_H3_su2_and_so2_have_same_cv` — exact equality.
- `test_H3_cv_is_half_omega_universal` — CV_G = Ω_G/2 holds for
  every G in the table (M1 generalised).

## Caveats

- **Bi-invariant metric assumption (A3).** For non-abelian compact
  Lie groups, the bi-invariant metric is unique up to scalar
  multiplication; the choice of scalar fixes the unit of φ_G. The
  canonical normalisation (Killing form on the Lie algebra,
  smallest-orbit length 1) is implicit in the table. Other
  normalisations rescale Ω_G but preserve the CV ratios across
  groups.
- **Compact connected only.** Non-compact Lie groups (e.g., ℝ as
  translation group) have infinite geodesic length and the CV_G
  formula gives 0 — i.e., perfect determinism. This is the correct
  limit for non-periodic systems but the M22 claim formally applies
  only to compact G.
- **Disconnected G (e.g., O(3) = SO(3) × Z₂).** The closed-geodesic
  length of the connected component (SO(3)) sets φ_G; the
  disconnected components contribute discrete-rupture multiplicity
  but not continuous-phase length. Treatment is analogous to the
  Z_n discrete-phase case (M15).
- **A4 (mean interval = one closed geodesic) is the substantive
  identification.** It says: one rupture cycle corresponds to one
  closed-geodesic excursion on G. For SO(2), this is one full
  revolution; for SU(2), one S³ great-circle traversal. The
  identification is consistent with M19 (Kac's lemma applied to the
  coherent region's measure on G) but requires the rupture-set
  measure to equal 1 / φ_G — provable for ergodic Lie-group flows
  by Haar-measure invariance, sketched but not fully developed here.

## Status

**T1.** Derivation rests on M1 (CV = Ω/2 from Bernoulli) and the
A4 identification (mean interval = closed-geodesic length).
Numerical verification is six-Lie-group parametric test plus two
exact-equality structural tests (SU(2)=SO(2), SO(3)=Z₂ in CV).

**T2 promotion in Session 3+** requires reproduction of the CV
prediction on a real Lie-group-symmetric system distinct from
SO(2). Suggested empirical tests (ranked by accessibility):

1. **SO(3)-symmetric: rigid-body precession data.** Predict
   CV = 1/(2π) ≈ 0.159, same as Z₂-bistable systems.
2. **SU(2)-symmetric: spin-1/2 NMR T₁ relaxation.** Predict
   CV = 1/(4π) ≈ 0.080, same as SO(2)-rotational systems.
3. **T²-symmetric: double-pendulum CV.** Predict CV = 1/(4π) per
   generator.
4. **SU(3)-symmetric: chromodynamic confinement timescale CVs.**
   Predict CV = 1/(4π√3) ≈ 0.046; experimentally challenging.

The SU(2) ≡ SO(2) and SO(3) ≡ Z₂ CV-equality predictions are the
sharpest falsifiers — independent of the underlying symmetry's
*details*, only the Lie-group covering structure should matter.
