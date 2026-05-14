# Derivation chain (Ω → φ_G → CV)

This is the chain that justifies every `cv_pred` in this package's
data files. Each link is a single claim with a derivation note in
`claims/`.

## The chain

```
                     A1: rupture is Z₂ by construction (C1, H1)
                     │
                     ▼
                     ┌──────────────────────────────────┐
                     │  M3 (Cramér–Rao saturation)      │
                     │  Var(θ) · I(θ) ≥ 1               │
                     │  rupture event = saturation      │
                     └─────────────┬────────────────────┘
                                   │
                                   ▼
                     ┌──────────────────────────────────┐
                     │  M1: CV = Ω / 2                  │
                     │  (from Bernoulli(1/2) variance)  │
                     │  claims/M1_cv_omega_over_two/    │
                     └─────────────┬────────────────────┘
                                   │
                     A2: phase manifold is compact connected Lie group G (C2, H2)
                                   │
                                   ▼
                     ┌──────────────────────────────────┐
                     │  M22: Ω_G = 1 / φ_G              │
                     │  CV_G = 1 / (2 · φ_G)            │
                     │  claims/M22_lie_group_cv_         │
                     │  generalisation/derivation.md    │
                     └─────────────┬────────────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                ▼                  ▼                  ▼
   ┌────────────────────┐  ┌──────────────┐  ┌──────────────────────┐
   │ M2: topological    │  │ M11: ρ=-1/2 │  │ M15: discrete-phase  │
   │ ratio CV(Z₂)/      │  │ for two Z₂ │  │ Z_n  CV = n/(4π)     │
   │ CV(SO(2)) = 2     │  │ on shared  │  │ (paper extrapolation │
   │ exact             │  │ SO(2)     │  │  CV = 1/(nπ) is a    │
   └───────────────────┘  └────────────┘  │  separate convention)│
                                          └─────────────────────┘
```

## What each ingredient does

| Step | Output | Source |
|------|--------|--------|
| A1 (C1) | Rupture is Z₂. Bernoulli(1/2) variance = 1/4. | `notes/conventions.md` C1; `notes/rupture_topology.md` H1 |
| M3 | C·Ω = 1 at rupture (Cramér–Rao saturation). | `claims/M3_cramer_rao_saturation/` |
| M1 | CV = Ω/2 from Bernoulli variance and constant-speed geodesic. | `claims/M1_cv_omega_over_two/derivation.md` |
| A2 (C2) | Phase manifold is compact connected Lie group G. | `notes/conventions.md` C2 |
| M22 | Ω_G = 1/φ_G; CV_G = 1/(2·φ_G). | `claims/M22_lie_group_cv_generalisation/derivation.md` |
| M2 | CV(Z₂)/CV(SO(2)) = 2 (half-turn embedding π / 2π). | `claims/M2_topological_ratio/` |
| M11 | ρ = −1/2 between two Z₂ rupture channels on a shared SO(2). | `claims/M11_z2_compose_so2_anticorrelation/derivation.md` |
| M15 | Discrete-phase Z_n CV = n/(4π) under the M15 reading; paper uses CV = 1/(nπ). | `claims/M15_zn_symmetry_hierarchy/derivation.md` |

## Open theoretical questions (paper's own honest assessment)

The paper's Section 1.5 and Section 8 list four open derivations.
This package records them in code so a future contributor knows
what to fix without reading the paper:

1. **Constant-speed geodesic traversal.** M1's CV = Ω/2 assumes
   coherence accumulates at constant rate along a Fisher–Rao
   geodesic. Without this, drift-diffusion to a threshold gives
   CV = Ω, not Ω/2. The factor of 1/2 is consistent with the
   conjugacy structure of CR / HG / Gabor but not yet derived from
   first principles.
2. **Circular Landauer ∆F = kT·π/2 per barrier.** The Z_n
   extrapolation CV = 1/(nπ) requires this universal barrier cost.
   Not derived from manifold geometry alone.
3. **Z_n discrepancy.** This package's `cv_zn_paper(n)` = 1/(nπ)
   (paper) and `cv_zn_discrete_phase(n)` = n/(4π) (M15) disagree
   for n ≥ 3. Both are recorded; reconciliation is deferred.
4. **A4 (mean interval = one closed geodesic).** M22 needs the
   identification E[τ_rupture] = φ_G; this is consistent with M19
   (Kac's lemma) but the rupture-set measure equals 1/φ_G is only
   sketched, not fully developed.

These are noted in the paper too (Section 1.5 "Derivation status",
Section 8 "Weaknesses").
