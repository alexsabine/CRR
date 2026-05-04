# M10 — current tier

This claim has two sub-tiers tracked separately:

## M10 fixed-point claim (1/α = 137.0324): T1

**Tier: T1 (consistency assessed; CODATA-precision falsification
recorded).**

**Justification:** Predicted 1/α = 137.0324 vs CODATA 137.036
differs by 26 ppm — six orders of magnitude beyond CODATA
experimental uncertainty (~10⁻¹⁰). The fixed-point existence and
stability are confirmed (Session-2 derivation, Session-3
consistency); the precise numerical value disagrees at experimental
precision. Stays at T1. See `consistency.md`.

## M10-α³ extension (subatomic CV scales as α³): **T3**

**Tier: T3 — first T3 promotion in the campaign.**

**Justification:** Pre-registered v2 Bethe-rescaled test
(prediction_v2.md, locked at git `102fedc`) shows that the
Bethe-rescaled residual

    B(system) = (ν_L × n³) / (Z⁴ × Ry × log(1/(Zα)²))

across hydrogenic 2S systems (H, D, He⁺) clusters at
⟨B⟩ = 2.59 × 10⁻⁷ with intra-system spread of just 3.6%, agreeing
with the leading-Bethe-coefficient prediction (8/3π) × α³ ≈
3.30 × 10⁻⁷ within 21.6%. All three pre-registered conditions
cleared:
1. Intra-system spread < 0.20: 3.6% ✓
2. |⟨B⟩ − target|/target < 0.30: 21.6% ✓
3. ⟨B⟩ > 0: ✓

See `result_v2.md` for the full output.

The Session-4 v1 negative (literal "CV ≈ α³" formulation, off by
5 orders of magnitude) is preserved in the audit trail; v2 does
not retroactively rescue v1. The lesson is that pre-registration
discipline rewards asking the right statistical question, not just
committing-then-running.

**Promotion gates ahead:**
- **T4** requires independent confirmation by an unaffiliated
  group, e.g.: a fourth hydrogenic system (Li²⁺ 2S Lamb shift)
  measured independently confirms B(Li²⁺) within the same 3.6%
  cluster, or muonic-hydrogen / antiprotonic-helium spectroscopy
  testing the same B-statistic. Queued for Session 6.
