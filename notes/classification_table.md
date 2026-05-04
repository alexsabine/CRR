# CRR Classification Table

Central artefact of the campaign. One row per claim; the tier reflects
only the evidence currently committed to the repository.

**Legend:**
- Tiers: T0 speculation · T1 conjecture (derivation present) ·
  T2 framework (independent consistency) · T3 theory (pre-registered
  novel prediction confirmed) · T4 established (independent replication).
- Domains: M mathematical · Ph philosophical/phenomenological ·
  Ps psychological · B biological · T temporal/dynamical · P physical.
- "T1*" indicates relabelling cap: T1 reachable as derivation, but no
  further promotion possible on the basis of the underlying canonical
  result alone.

**Status:** Session 2 complete. All 21 mathematical claims promoted to
T1 with derivation files; 5 of those carry caveats (M5, M9, M14, M15, M16,
M19, M21). Empirical (P, B) and philosophical (Ph) claims remain at T0
pending Sessions 3–5.

| ID  | Canonical statement (abbreviated) | Tier | Domain(s) | Evidence files | Justification |
|-----|-----------------------------------|------|-----------|----------------|---------------|
| M1  | CV = Ω/2, no free parameters | T1 | M, T | [claim](../claims/M1_cv_omega_over_two/claim.md) · [derivation](../claims/M1_cv_omega_over_two/derivation.md) · [tier](../claims/M1_cv_omega_over_two/tier.md) | Bernoulli(1/2) noise model; verified |
| M2  | Z₂:SO(2) CV ratio = 2 (topological) | T1 | M, T | [claim](../claims/M2_topological_ratio/claim.md) · [derivation](../claims/M2_topological_ratio/derivation.md) · [tier](../claims/M2_topological_ratio/tier.md) | Algebraic; machine-precision verification |
| M3  | C·Ω = 1 saturates Cramér-Rao | T1 | M | [claim](../claims/M3_cramer_rao_saturation/claim.md) · [derivation](../claims/M3_cramer_rao_saturation/derivation.md) · [tier](../claims/M3_cramer_rao_saturation/tier.md) | Loadbearing on M13; Gaussian-location verification |
| M4  | C·Ω = 1 saturates Heisenberg-Gabor | T1 | M, P | [claim](../claims/M4_heisenberg_gabor_saturation/claim.md) · [derivation](../claims/M4_heisenberg_gabor_saturation/derivation.md) · [tier](../claims/M4_heisenberg_gabor_saturation/tier.md) | HPW saturation; Gaussian wavelet verification |
| M5  | CR ≡ HG (same theorem) | T1* | M | [claim](../claims/M5_cr_hg_equivalence/claim.md) · [derivation](../claims/M5_cr_hg_equivalence/derivation.md) · [tier](../claims/M5_cr_hg_equivalence/tier.md) | Relabelling — capped at T1 |
| M6  | Fourier is the trivial CRR limit | T1 | M | [claim](../claims/M6_fourier_limit/claim.md) · [derivation](../claims/M6_fourier_limit/derivation.md) · [tier](../claims/M6_fourier_limit/tier.md) | Substitution; verified |
| M7  | φ = dominant eigenvalue, depth-two regen op | T1 | M | [claim](../claims/M7_phi_eigenvalue/claim.md) · [derivation](../claims/M7_phi_eigenvalue/derivation.md) · [tier](../claims/M7_phi_eigenvalue/tier.md) | Char poly; machine-precision verification |
| M8  | Depth-2 = minimum for KAM-stable ergodicity | T1 | M, T | [claim](../claims/M8_depth_two_kam/claim.md) · [derivation](../claims/M8_depth_two_kam/derivation.md) · [tier](../claims/M8_depth_two_kam/tier.md) | Twist-map / Moser; caveat on 1-D state assumption |
| M9  | φ-rotated CRR has singular-continuous spectrum | T1 | M, T | [claim](../claims/M9_singular_continuous_spectrum/claim.md) · [derivation](../claims/M9_singular_continuous_spectrum/derivation.md) · [tier](../claims/M9_singular_continuous_spectrum/tier.md) | Sütő-Bellissard-Damanik; identification caveat |
| M10 | Fine-structure equation: unique fixed point at 137.032 | T1 | M, P | [claim](../claims/M10_fine_structure_fixed_point/claim.md) · [derivation](../claims/M10_fine_structure_fixed_point/derivation.md) · [tier](../claims/M10_fine_structure_fixed_point/tier.md) | Numerical: 137.0324; 26 ppm vs CODATA |
| M11 | Z₂+Z₂→SO(2) gives ρ = −1/2 | T1 | M | [claim](../claims/M11_z2_compose_so2_anticorrelation/claim.md) · [derivation](../claims/M11_z2_compose_so2_anticorrelation/derivation.md) · [tier](../claims/M11_z2_compose_so2_anticorrelation/tier.md) | Variance-preserving composition; Monte-Carlo verification |
| M12 | B(C) = exp(C/Ω)(C* − C) peaks at C* − Ω | T1 | M, Ph | [claim](../claims/M12_beauty_peak/claim.md) · [derivation](../claims/M12_beauty_peak/derivation.md) · [tier](../claims/M12_beauty_peak/tier.md) | Calculus; analytic + numerical verification |
| M13 | C ≡ accumulated Fisher information | T1 | M | [claim](../claims/M13_fisher_information_identification/claim.md) · [derivation](../claims/M13_fisher_information_identification/derivation.md) · [tier](../claims/M13_fisher_information_identification/tier.md) | Identification via Fisher-Rao speed²; verification |
| M14 | exp(C/Ω) = unique MaxEnt regen kernel | T1* | M | [claim](../claims/M14_maxent_regeneration_kernel/claim.md) · [derivation](../claims/M14_maxent_regeneration_kernel/derivation.md) · [tier](../claims/M14_maxent_regeneration_kernel/tier.md) | Boltzmann-Gibbs MaxEnt — relabelling cap |
| M15 | Z_n hierarchy: CV = n/(4π) | T1 | M | [claim](../claims/M15_zn_symmetry_hierarchy/claim.md) · [derivation](../claims/M15_zn_symmetry_hierarchy/derivation.md) · [tier](../claims/M15_zn_symmetry_hierarchy/tier.md) | Verifies n=2; SO(2) endpoint not monotone — flagged |
| M16 | Bonnet-Myers: Ω = π/√κ | T1 | M | [claim](../claims/M16_bonnet_myers_omega/claim.md) · [derivation](../claims/M16_bonnet_myers_omega/derivation.md) · [tier](../claims/M16_bonnet_myers_omega/tier.md) | Convention inconsistency Ω = 1/φ_geo vs Ω = π/√κ |
| M17 | C = quadratic variation [μ,μ]_t | T1 | M | [claim](../claims/M17_quadratic_variation/claim.md) · [derivation](../claims/M17_quadratic_variation/derivation.md) · [tier](../claims/M17_quadratic_variation/tier.md) | Definitional; Brownian motion verification |
| M18 | τ_Ω = optimal stopping time (SPRT) | T1 | M | [claim](../claims/M18_optimal_stopping_rupture/claim.md) · [derivation](../claims/M18_optimal_stopping_rupture/derivation.md) · [tier](../claims/M18_optimal_stopping_rupture/tier.md) | Wald-Wolfowitz; SPRT mean-stop verification |
| M19 | Poincaré + Kac: rupture inevitable; Ω = 1/μ(coh) | T1 | M | [claim](../claims/M19_poincare_kac_inevitability/claim.md) · [derivation](../claims/M19_poincare_kac_inevitability/derivation.md) · [tier](../claims/M19_poincare_kac_inevitability/tier.md) | Kac's lemma; convention Ω = μ(A) vs 1/μ(A) flagged |
| M20 | R[χ] = right Kan extension | T1 | M | [claim](../claims/M20_kan_extension_regeneration/claim.md) · [derivation](../claims/M20_kan_extension_regeneration/derivation.md) · [tier](../claims/M20_kan_extension_regeneration/tier.md) | Universal property; finite discrete verification |
| M21 | C·Ω = 1 unifies CR + HG + TUR | T1 | M, P | [claim](../claims/M21_uncertainty_unification/claim.md) · [derivation](../claims/M21_uncertainty_unification/derivation.md) · [tier](../claims/M21_uncertainty_unification/tier.md) | TUR factor-of-2 mismatch; convention rescaling needed |
| P1  | Solar Hale CV matches SO(2) within 3.6% | T0 | P, T | [claim](../claims/P1_solar_hale_cv/claim.md) | Not yet assessed (Session 3) |
| P2  | GWTC BBH CV consistent with SO(2), not Z₂ | T0 | P | [claim](../claims/P2_gwtc_binary_bh_cv/claim.md) | Not yet assessed (Session 3) |
| P3  | Atomic spectral CV across 49 elements | T0 | P | [claim](../claims/P3_atomic_spectra_cv/claim.md) | Not yet assessed (Session 3) |
| P4  | Dark-energy w=−1 crossing at peak ρ_DE, z≈0.5 | T0 | P | [claim](../claims/P4_dark_energy_w_crossing/claim.md) | Not yet assessed (Session 3) |
| P5  | Single-Ω matches ETAS on California (CSEP null) | T0 | P, T | [claim](../claims/P5_csep_california_null/claim.md) | Not yet assessed (Session 3) |
| P6  | Ω = k_B T / κ_eff in physical systems | T0 | P | [claim](../claims/P6_thermodynamic_omega/claim.md) | Not yet assessed (Session 3) |
| P7  | CLT regularisation: macro-scale determinism | T0 | M, P | [claim](../claims/P7_clt_macro_regularization/claim.md) | Not yet assessed (Session 3) |
| B1  | Biological 1/f signals: singular-continuous (Fibonacci) | T0 | B, T | [claim](../claims/B1_biological_1f_singular_continuous/claim.md) | Not yet assessed (Session 3) |
| B2  | HRV pathology cohorts: B → A → C ordering | T0 | B, Ps | [claim](../claims/B2_hrv_pathology_cv/claim.md) | Not yet assessed (Session 3) |
| B3  | AGI-26 phase-gating: χ²=8041, conservation 1.003 | T0 | B, Ps | [claim](../claims/B3_agi26_phase_gating/claim.md) | Not yet assessed (Session 3) |
| B4  | Perception-action ρ = −1/2 | T0 | B, Ps | [claim](../claims/B4_perception_action_anticorrelation/claim.md) | Not yet assessed (Session 3) |
| B5  | EEG: 11/11 class orderings, CV ratio 1.93 | T0 | B, Ps | [claim](../claims/B5_eeg_class_ordering/claim.md) | Not yet assessed (Session 3) |
| B6  | 132-system CV cross-domain, 0 reversals | T0 | B, P, Ps | [claim](../claims/B6_132_system_cv/claim.md) | Not yet assessed (Session 3) |
| B7  | Memory significance-weighted, not recency-weighted | T0 | B, Ps | [claim](../claims/B7_significance_weighted_memory/claim.md) | Not yet assessed (Session 3) |
| Ph1 | Whitehead concrescence formalised by C/δ/R | T0 | Ph | [claim](../claims/Ph1_whitehead_concrescence/claim.md) | Not yet assessed (Session 5) |
| Ph2 | Bergson durée formalised by R[χ] | T0 | Ph | [claim](../claims/Ph2_bergson_duree/claim.md) | Not yet assessed (Session 5) |
| Ph3 | δ(now) = ontological present | T0 | Ph | [claim](../claims/Ph3_ontological_present/claim.md) | Not yet assessed (Session 5) |
| Ph4 | Beauty/agency at C* − Ω (the edge) | T0 | Ph | [claim](../claims/Ph4_beauty_at_edge/claim.md) | Not yet assessed (Session 5) |
| Ph5 | Identity persists as change | T0 | Ph | [claim](../claims/Ph5_identity_as_change/claim.md) | Not yet assessed (Session 5) |
| Ph6 | Consciousness at coherence-rupture interface | T0 | Ph, B | [claim](../claims/Ph6_consciousness_at_interface/claim.md) | Not yet assessed (Session 5) |
| Ph7 | Ω-regime psychological typology | T0 | Ph, Ps | [claim](../claims/Ph7_psychological_phase_typology/claim.md) | Not yet assessed (Session 5) |

## Tier counts (after Session 2)

| Domain | T0 | T1 | T1* (relabelling) | T2 | T3 | T4 | Down |
|--------|----|----|-------------------|----|----|----|------|
| M (21) | 0  | 19 | 2 (M5, M14)       | 0  | 0  | 0  | 0    |
| P (7)  | 7  | 0  | 0                 | 0  | 0  | 0  | 0    |
| B (7)  | 7  | 0  | 0                 | 0  | 0  | 0  | 0    |
| Ph (7) | 7  | 0  | 0                 | 0  | 0  | 0  | 0    |
| **Total (42)** | **21** | **19** | **2** | 0 | 0 | 0 | 0 |

## Session 2 caveats / convention issues queued for author review

| Claim | Issue | Recorded in |
|-------|-------|-------------|
| M5 | Confirmed relabelling of CR↔HG translation correspondence | relabellings.md §M5 |
| M6 | "Limit" is formal substitution, not topological limit | M6/derivation.md |
| M8 | Minimum-depth claim needs 1-D state assumption made explicit | M8/derivation.md |
| M9 | Identification of CRR regen op with Fibonacci Hamiltonian needs justification | M9/derivation.md |
| M10 | Equation derivation deferred; 26 ppm CODATA discrepancy unaddressed | M10/derivation.md |
| M11 | Composition constraint (variance-preserving vs rate-halving) ambiguous | M11/derivation.md |
| M14 | Confirmed relabelling of Boltzmann-Gibbs MaxEnt | relabellings.md §M14 |
| M15 | Z_n formula not monotone; SO(2) endpoint anomalous | M15/derivation.md |
| M16 | Convention inconsistency: Ω = 1/φ_geo vs Ω = π/√κ | M16/derivation.md |
| M19 | Convention Ω = μ(A) vs Ω = 1/μ(A) ambiguous | M19/derivation.md |
| M21 | TUR identification has factor-of-2 mismatch | M21/derivation.md |
| (S1 finding) | exp(C/Ω) → e at C·Ω = 1 holds only at Ω = 1 | relabellings.md (S1) |
