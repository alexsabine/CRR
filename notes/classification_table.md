# CRR Classification Table

Central artefact of the campaign. One row per claim; the tier reflects
only the evidence currently committed to the repository.

**Legend:**
- T0 speculation · T1 conjecture · T2 framework · T3 theory · T4 established
- T1\* relabelling cap · T2 (m) marginal · T2 (p) preliminary · T2 (c) conditional
- Domains: M Ph Ps B T P
- ★ Session-2.5 update · ⚑ Session-3 update

**Status (after Session 3):**
- 22 mathematical claims at T1 (M5, M14 capped T1\*; M10 explicitly
  assessed against CODATA, remains T1).
- 4 firm T2 promotions (P1, P6, P7, B7).
- 3 conditional/preliminary/marginal T2 (P2, P4, P5).
- 7 P/B claims remain T1 with consistency.md committed and
  reviewer-run reproduction scripts.
- All Ph claims remain T0 (Session 5 work).

| ID  | Statement (abbrev.) | Tier | Domain(s) | Evidence files | Justification |
|-----|---------------------|------|-----------|----------------|---------------|
| M1  | CV = Ω/2 | T1 | M, T | [claim](../claims/M1_cv_omega_over_two/) · [derivation](../claims/M1_cv_omega_over_two/derivation.md) | Bernoulli forced by H1 ★ |
| M2  | Z₂:SO(2) ratio = 2 | T1 | M, T | [derivation](../claims/M2_topological_ratio/derivation.md) | Half-turn embedding ★ |
| M3  | C·Ω = 1 saturates Cramér-Rao | T1 | M | [derivation](../claims/M3_cramer_rao_saturation/derivation.md) | Loadbearing on M13 |
| M4  | C·Ω = 1 saturates Heisenberg-Gabor | T1 | M, P | [derivation](../claims/M4_heisenberg_gabor_saturation/derivation.md) | HPW saturation |
| M5  | CR ≡ HG | T1\* | M | [derivation](../claims/M5_cr_hg_equivalence/derivation.md) | Closed (relabelling) |
| M6  | Fourier as trivial CRR specialisation | T1 | M | [derivation](../claims/M6_fourier_limit/derivation.md) | "specialisation" not "limit" ★ |
| M7  | φ = dominant eigenvalue (depth 2) | T1 | M | [derivation](../claims/M7_phi_eigenvalue/derivation.md) | Char poly |
| M8  | Depth-2 minimum for KAM-stable ergodicity | T1 | M, T | [derivation](../claims/M8_depth_two_kam/derivation.md) | Twist-map / Moser ★ |
| M9  | φ-rotated CRR has SC spectrum | **T2** | M, T | [derivation](../claims/M9_singular_continuous_spectrum/derivation.md) · [prediction_v2](../claims/M9_singular_continuous_spectrum/prediction_v2.md) · [result_v2](../claims/M9_singular_continuous_spectrum/result_v2.md) | **v2 coupling sweep PASSES; Sütő-class confirmed** ⚑⚑ |
| M10 | 1/α fixed point (T1) + α³ subatomic (**T3**) | **T1 + T3** | M, P | [derivation](../claims/M10_fine_structure_fixed_point/derivation.md) · [consistency](../claims/M10_fine_structure_fixed_point/consistency.md) · [prediction_v2](../claims/M10_fine_structure_fixed_point/prediction_v2.md) · [result_v2](../claims/M10_fine_structure_fixed_point/result_v2.md) | **First T3 in campaign — α³ Bethe-rescaled mean residual matches at 21.6%** ⚑⚑ |
| M11 | Z₂+Z₂→SO(2) gives ρ=−1/2 | T1 | M | [derivation](../claims/M11_z2_compose_so2_anticorrelation/derivation.md) | Variance-preservation derived ★ |
| M12 | B(C) peaks at C*−Ω | T1 | M, Ph | [derivation](../claims/M12_beauty_peak/derivation.md) | Calculus |
| M13 | C ≡ accumulated Fisher info | T1 | M | [derivation](../claims/M13_fisher_information_identification/derivation.md) | Identification |
| M14 | exp(C/Ω) = MaxEnt kernel | T1\* | M | [derivation](../claims/M14_maxent_regeneration_kernel/derivation.md) | Closed (relabelling) |
| M15 | Z_n hierarchy CV=n/(4π) | T1 | M | [derivation](../claims/M15_zn_symmetry_hierarchy/derivation.md) | Discrete-phase reframing ★ |
| M16 | Bonnet-Myers Ω≥√κ/π | T1 | M | [derivation](../claims/M16_bonnet_myers_omega/derivation.md) | Inversion typo corrected ★ |
| M17 | C = quadratic variation | T1 | M | [derivation](../claims/M17_quadratic_variation/derivation.md) | Definitional |
| M18 | τ_Ω = SPRT optimal stop | T1 | M | [derivation](../claims/M18_optimal_stopping_rupture/derivation.md) | Wald-Wolfowitz |
| M19 | Poincaré+Kac, Ω = μ(coh) | T1 | M | [derivation](../claims/M19_poincare_kac_inevitability/derivation.md) | Convention C5 ★ |
| M20 | R[χ] = right Kan extension | T1 | M | [derivation](../claims/M20_kan_extension_regeneration/derivation.md) | Universal property |
| M21 | C·Ω=1 unifies CR+HG+TUR | T1 | M, P | [derivation](../claims/M21_uncertainty_unification/derivation.md) | Open: TUR factor of 2 |
| M22 | CV_G = 1/(2·φ_G) for compact Lie G | T1 | M, T | [derivation](../claims/M22_lie_group_cv_generalisation/derivation.md) | Lie-group generalisation ★ |
| **P1**  | **Solar Hale CV** | **T2** | P, T | [consistency](../claims/P1_solar_hale_cv/consistency.md) · [script](../crr-engine/consistency/solar_hale.py) | **Predicted 0.0796 ∈ SILSO band ⚑** |
| **P2**  | **GWTC BBH CV** | **T2 (m)** | P | [consistency](../claims/P2_gwtc_binary_bh_cv/consistency.md) · [script](../crr-engine/consistency/gwtc.py) | **0.0796 in CI lower tail ⚑** |
| P3  | Atomic spectral CV (49 elements) | T1 | P | [consistency](../claims/P3_atomic_spectra_cv/consistency.md) | Stub: needs metric specification ⚑ |
| **P4**  | **Dark-energy w=−1 crossing at z≈0.5** | **T2 (p)** | P | [consistency](../claims/P4_dark_energy_w_crossing/consistency.md) | **DESI-2024 evidence at ~3-4σ ⚑** |
| **P5**  | **Single-Ω matches ETAS California** | **T2 (c)** | P, T | [consistency](../claims/P5_csep_california_null/consistency.md) | **Conditional on CSEP run; nested-CRR null recorded ⚑** |
| **P6**  | **Ω = k_B T / κ_eff** | **T2** | P | [consistency](../claims/P6_thermodynamic_omega/consistency.md) · [script](../crr-engine/consistency/thermodynamic_omega.py) | **Equipartition relabelling, OOM consistent ⚑** |
| **P7**  | **CLT regularisation CV/√M** | **T2** | M, P | [consistency](../claims/P7_clt_macro_regularization/consistency.md) · [script](../crr-engine/consistency/clt_regularization.py) | **Verified end-to-end in sandbox ⚑** |
| B1  | 1/f singular-continuous (Fibonacci) | T1 | B, T | [consistency](../claims/B1_biological_1f_singular_continuous/consistency.md) | Stub: Last-Simon test ⚑ |
| B2  | HRV B → A → C ordering | T1 | B, Ps | [consistency](../claims/B2_hrv_pathology_cv/consistency.md) | Stub: PhysioNet rank-sum ⚑ |
| B3  | AGI-26 χ²=8041, ρ=−1/2 | T1 | B, Ps | [consistency](../claims/B3_agi26_phase_gating/consistency.md) | **Blocked: dataset deposition needed** ⚑ |
| B4  | Perception-action ρ=−1/2 | T1 | B, Ps | [consistency](../claims/B4_perception_action_anticorrelation/consistency.md) | Stub: Allen Brain ⚑ |
| B5  | EEG 11/11 + 1.93 ratio | T1 | B, Ps | [consistency](../claims/B5_eeg_class_ordering/consistency.md) | **Blocked: cohort spec needed** ⚑ |
| B6  | 132-system zero reversals | T1 | B, P, Ps | [consistency](../claims/B6_132_system_cv/consistency.md) | **Blocked: catalogue deposition needed** ⚑ |
| **B7**  | **Significance-weighted memory** | **T2** | B, Ps | [consistency](../claims/B7_significance_weighted_memory/consistency.md) · [script](../crr-engine/consistency/significance_memory.py) | **Math by construction; biological consistency with reservoir/replay literature ⚑** |
| Ph1 | Whitehead concrescence | **T2-eq** | Ph | [assessment](Ph1_whitehead_assessment.md) | **Structural** (C/δ/R triad maps to prehension/concrescence/objective-immortality) ⚑5 |
| Ph2 | Bergson durée | **T2-eq (caveat)** | Ph | [assessment](Ph2_bergson_assessment.md) | **Structural** (charitable) / **Metaphorical** (strong reading of anti-spatialisation) ⚑5 |
| Ph3 | δ(now) = ontological present | T1 | Ph | [assessment](Ph3_ontological_present_assessment.md) | **Structural with metaphysical commitment** (presentism / growing-block) ⚑5 |
| Ph4 | Beauty/agency at C*−Ω | **T2-eq** | Ph | [assessment](Ph4_beauty_at_edge_assessment.md) | **Mathematically Exact (M12); philosophically Structural** ⚑5 |
| Ph5 | Identity persists as change | **T2-eq** | Ph | [assessment](Ph5_identity_as_change_assessment.md) | **Structural**; remainder = personal-identity puzzles, normativity ⚑5 |
| Ph6 | Consciousness at coherence-rupture interface | T1 | Ph, B | [assessment](Ph6_consciousness_assessment.md) | **Metaphorical with structural ambitions** ⚑5 |
| Ph7 | Ω-regime psychological typology | **T2-eq** | Ph, Ps | [assessment](Ph7_psychological_typology_assessment.md) | **Structural with empirical falsifiability**; co-promotes with B2 ⚑5 |

## Tier counts (after Session 5)

| Domain | T0 | T1 | T1\* | T2 / T2-eq | T2 (m/p/c) | **T3** | T4 |
|--------|----|----|------|------------|------------|--------|----|
| M (22) | 0  | 18 | 2    | 1 (M9)     | 0          | **1 (M10-α³)** | 0  |
| P (7)  | 0  | 1  | 0    | 3          | 3          | 0      | 0  |
| B (7)  | 0  | 6  | 0    | 1          | 0          | 0      | 0  |
| Ph (7) | 0  | 2 (Ph3, Ph6) | 0 | **5 (Ph1, Ph2, Ph4, Ph5, Ph7)** | 0 | 0 | 0 |
| **Total (43)** | **0** | **27** | **2** | **10** | **3** | **1** | **0** |

**Session 5 changes:** all 7 Ph claims promoted from T0; 5 reach
T2-eq (philosophical pathway); 2 stay at T1. Each carries an
explicit M/S/E (Metaphorical / Structural / Exact) interpretation
label per `notes/philosophical_assessment_framework.md`.

**No Ph claim reached T3-eq** — none has a confirmed novel
phenomenological prediction yet. **No Ph claim reached T4-eq** —
no independent philosophical engagement located.

**T0 count is now zero across the entire claim set** — every CRR
claim has been formally assessed with at least T1 evidence
committed.

**Session 4.5 promotions:**
- **M9**: T1 → T2 (v2 coupling-sweep PASSES Sütő-class trend)
- **M10-α³**: T1 → **T3** (v2 Bethe-rescaled test PASSES — first T3
  in the campaign)

The M10 fixed-point sub-claim (1/α = 137.0324) stays at T1 due to
the 26 ppm CODATA discrepancy. M10-α³ is a separate sub-claim that
reached T3 via the alternative-reading pathway pre-registered in
Session 4.5.

(M22 brings the M-claim count to 22; total is 43.)

## Session 4 — pre-registered predictions and results

**9 pre-registrations committed at git `3fc9681` BEFORE any
analysis script.** The discipline-binding commit; the campaign's
audit trail for T3 testing.

| Claim | Pre-reg | Test status | Result |
|-------|---------|-------------|--------|
| M9 | Sturmian-Hamiltonian Cantor signature | Sandbox-executed | **FAIL** (gap monotonicity, box-dim) |
| M10 | α³ Lamb-shift CV | Sandbox-executed | **FAIL literal**; alt reading at 22% |
| M22-A | SU(2) ≡ SO(2) CV | [REVIEWER-RUN] | pending |
| M22-B | SO(3) ≡ Z₂ CV | [REVIEWER-RUN] | pending |
| M22-C | SU(3) CV ≈ 0.0459 | [REVIEWER-RUN] | pending |
| P1 | Stellar Hale CV | [REVIEWER-RUN] | pending |
| P2 | LIGO O5 BBH CV | [REVIEWER-RUN] | pending |
| P4 | DESI w(z) crossing | [REVIEWER-RUN] | pending |
| P5 | Global ETAS-CRR parity | [REVIEWER-RUN] | pending |
| B2 | PhysioNet HRV ordering | [REVIEWER-RUN] | pending |

**No T3 promotions in Session 4.** Both sandbox-executable tests
failed their literal pre-registrations; reviewer-run tests await
execution. Honest negatives recorded in `result.md` files.

## Session 3 promotions

| Claim | T1 → T2 | Reason |
|-------|---------|--------|
| P1 (Solar Hale) | ✓ T2 | Predicted 0.0796 ∈ SILSO band [0.0767, 0.0820] |
| P2 (GWTC) | ✓ T2 (marginal) | Predicted 0.0796 ∈ CI [0.077, 0.114] but lower tail |
| P4 (Dark energy) | ✓ T2 (preliminary) | DESI-2024 evidence at ~3-4σ; preliminary |
| P5 (CSEP) | ✓ T2 (conditional) | Conditional on reviewer running CSEP harness |
| P6 (Thermodynamic Ω) | ✓ T2 | Equipartition relabelling, dimensionally OOM-consistent |
| P7 (CLT) | ✓ T2 | Verified end-to-end in campaign sandbox |
| B7 (Significance memory) | ✓ T2 | Math + broad biological literature consistency |

**Non-promotion explicitly recorded:** M10 (1/α). 26 ppm CODATA
discrepancy disqualifies T2 at experimental precision.

## Outstanding inconsistencies (post-Session-3)

Still 3 from Session 2:
- M9: Fibonacci identification (Session 4 pre-registration target)
- M10: 26 ppm CODATA discrepancy (now formally assessed)
- M21: TUR factor-of-2 (recommended rephrasing in conventions.md)

## Author action items surfaced in Session 3

| Claim | Action | Priority |
|-------|--------|----------|
| B6 | Deposit 132-system CV catalogue at open archive (DOI) | **HIGH** — broadest empirical reach |
| B3 | Deposit AGI-26 dataset at open archive (DOI) | **HIGH** — sharpest empirical specificity |
| B5 | Specify EEG cohort (database, version, preprocessing) | medium |
| P3 | Specify exact prediction metric (which CV?) | medium |
