# Framework summary (one page)

CRR (Coherence–Rupture–Regeneration) is a temporal-process framework
in which every oscillatory system is described by three operators:

- **Coherence accumulates:**  C(x, t) = ∫ L(x, τ) dτ
- **Rupture is instantaneous:**  δ(now) when C·Ω = 1
- **Regeneration is exponentially weighted:**  R = ∫ φ(x, τ)·exp(C/Ω)·Θ dτ

The single parameter Ω is the system's boundary permeability. CRR
makes a quantitative, parameter-free prediction for the coefficient
of variation of cycle times:

- **Geometric M22 form:**  CV_G = 1 / (2 · φ_G), where φ_G is the
  bi-invariant closed-geodesic length of the Lie-group phase
  manifold G.
- **Special cases (paper):**  CV(Z₂) = 1/(2π) ≈ 0.1592;
  CV(SO(2)) = 1/(4π) ≈ 0.0796.
- **Topological ratio:**  CV(Z₂) / CV(SO(2)) = 2 exactly.

## Three-class diagnostic taxonomy

| Class | Physical reading | Prediction | Paper data |
|-------|------------------|-----------|------------|
| A — autonomous stochastic oscillator | Ω at intrinsic value | CV ∈ [0.6×, 1.3×] of 1/(2·φ_G) | 40/45 = 89% match |
| B — deterministic / actively regulated | Ω suppressed below intrinsic | CV ≪ 1/(2·φ_G) | 34/40 = 85% suppressed |
| C — noise-dominated / volitional | Ω inflated above intrinsic | CV ≫ 1/(2·φ_G) | 40/47 = 85% elevated |

Paper aggregate: 114/132 = 86% three-class correct, **zero
directional reversals**, ~10.6 σ vs log-uniform null.

## What this package adds

1. **Machine-readable form** of the 132-system table from Appendix A
   (`data/cv_predictions_132.csv`, `…json`), with each row carrying
   physical_justification, class_justification, and reference fields
   so the rubric is reproducible.
2. **Z₂-on-SO(2) compositional predictions** (14 rows) — the
   structural consequence of "all ruptures are Z₂" + "SO(2) is the
   continual substrate" being applied compositionally:
   ρ = −1/2 anti-correlation between two channels, nested CV (sub-
   rupture jitter vs full cycle), k-channel ρ = −1/(k−1).
3. **Lie-group CV predictions beyond M22** (14 rows) — adds
   SO(4), U(2), SU(4), Sp(2), G₂, Spin(7), T³, T⁴, golden-ratio
   PHI, plus concrete candidate empirical systems for each.
4. **6-step rubric as runnable Python** (`src/crr_cv_predictions/
   rubric.py`) — apply the protocol to a new system and emit a
   prediction row.
5. **Integrity tests** that pin the paper's headline numbers
   (53/34/45, 114/132, 0 reversals) so any future edit that breaks
   them fails CI.

## What this package does *not* do

- Re-derive M1 (CV = Ω/2). That derivation lives in
  `claims/M1_cv_omega_over_two/derivation.md`.
- Re-derive M11 (ρ = −1/2). See `claims/M11_z2_compose_so2_anti
  correlation/derivation.md`.
- Re-derive M22. See `claims/M22_lie_group_cv_generalisation/
  derivation.md`.
- Reproduce the paper's Monte Carlo null-model significance.
  That lives in `crr-engine/consistency/significance_memory.py`.

This package is the *predictions catalogue*, not the derivation
engine.
