# Session log

## Session 1 — Decomposition and engine (2026-05-04)

### Completed

- **Read canonical brief** in this conversation; cross-checked against
  the canonical CRR source files in the repo:
  - `CRR canonical proof sketch.md`
  - `canonical_crr_rigorous_proof_sketch.md`
  - `CRR_Complete_Proof_Sketch.md`
  - `CRR_COMPREHENSIVE_SUMMARY.md`
  - `crr_first_principles_proofs.md`
  - `crr_meta_theorem.md`
  - `crr_full_proofs.md`
  - `CRR_Church_eff.html`
- **Enumerated 42 distinct propositional claims** across four
  domains: 21 mathematical (M1–M21), 7 physical/temporal (P1–P7),
  7 biological/psychological (B1–B7), 7 philosophical (Ph1–Ph7).
  Recorded in `notes/decomposition.md`.
- **Created 42 claim subdirectories** under `claims/`, each with a
  canonical `claim.md` and a `tier.md` initialised to T0.
- **Factored the canonical engine** from `CRR_Church_eff.html` into
  `crr-engine/index.py`. Added 24 pytest cases. **All passing.**
- **Initialised** `notes/classification_table.md` (all 42 at T0),
  `CAMPAIGN.md` (root brief), `README.md` dashboard banner.

### Surprises / findings

- **exp(C/Ω) → e at C·Ω = 1 inconsistency:** the two conditions only
  coincide when Ω = 1, not under canonical Z₂ (Ω = 1/π) or SO(2)
  (Ω = 1/(2π)). Recorded in `notes/relabellings.md` and asserted in
  two pytest cases.
- **Engine clamps exp(C/Ω) at 10** to avoid numerical blow-up.
- **M5 likely a relabelling**, **M14 borderline**.

### Promotions / downgrades

None. Session 1 only initialises the table at T0.

---

## Session 2 — Mathematical claims, T0 → T1 (2026-05-04)

### Completed

- **All 21 M-claim derivations written** (`claims/M*/derivation.md`).
  Each derivation states assumptions, performs step-by-step argument,
  cites the corresponding numerical-verification test, and lists
  caveats.
- **`crr-engine/tests/test_derivations.py` added** with 19 numerical
  verification tests, one per derivable M-claim. **All 43 tests pass**
  (24 from Session 1 + 19 new).
- **All 21 M-claim `tier.md` files promoted to T1.** Two are flagged
  T1\* (relabelling cap): M5 (CR↔HG equivalence), M14 (Boltzmann-Gibbs
  MaxEnt).
- **Classification table refreshed** to reflect new tier counts.
- **`notes/relabellings.md` extended** with seven new convention/
  identification findings: M11 composition constraint, M14 MaxEnt,
  M15 Z_n non-monotonicity, M16 Ω-convention inconsistency,
  M19 Ω = μ(A) vs 1/μ(A) ambiguity, M21 TUR factor-of-2 mismatch,
  M10 26 ppm CODATA discrepancy.
- **README.md tier counts updated.**

### Promotions

| ID  | T0 → T1 | Caveat |
|-----|---------|--------|
| M1  | ✓ | Loadbearing on noise model A3 |
| M2  | ✓ | — |
| M3  | ✓ | Loadbearing on M13 + estimator efficiency |
| M4  | ✓ | — |
| M5  | ✓* | **Relabelling cap (CR↔HG canonical)** |
| M6  | ✓ | "Limit" is formal substitution, not topological |
| M7  | ✓ | — |
| M8  | ✓ | 1-D state-variable assumption implicit |
| M9  | ✓ | Identification of CRR regen op with Fibonacci-chain Hamiltonian needs justification |
| M10 | ✓ | 26 ppm vs CODATA; equation derivation deferred |
| M11 | ✓ | Composition constraint ambiguous (variance-preserving assumed) |
| M12 | ✓ | — |
| M13 | ✓ | Identification, not theorem |
| M14 | ✓* | **Relabelling cap (Boltzmann-Gibbs MaxEnt)** |
| M15 | ✓ | Z_n hierarchy not monotone; SO(2) endpoint anomalous |
| M16 | ✓ | Ω-convention inconsistency Ω = 1/φ_geo vs π/√κ |
| M17 | ✓ | Definitional under L = local QV rate |
| M18 | ✓ | — |
| M19 | ✓ | Ω = μ(A) vs Ω = 1/μ(A) ambiguity |
| M20 | ✓ | Continuous-time bridge requires enriched Kan |
| M21 | ✓ | TUR factor-of-2 mismatch under direct identification |

### Downgrades

None.

### Surprises / new findings

1. **M10 fixed-point uniqueness search yielded TWO fixed points,
   not one.** The CRR self-consistency equation has α* ≈ 0.007298
   (1/α = 137.0324, stable) and α* ≈ 0.367989 (1/α = 2.717, unstable —
   note the proximity to 1/e). The brief's "unique stable fixed
   point" is correct after the stability filter, but the two-fixed-
   point structure was not stated in the canonical brief.
2. **M10 CODATA discrepancy is large.** 26 ppm in 1/α is six orders
   of magnitude beyond CODATA experimental uncertainty (~10⁻¹⁰).
   T2 promotion in Session 3 will need to engage with this.
3. **M11 anti-correlation derives from variance-preserving
   composition, not topological halving.** Under the M2-implied
   constraint Var(X+Y) = Var(X)/2, the answer would be ρ = −3/4,
   not −1/2. The canonical −1/2 is correct under
   variance-preservation but the brief does not state this.
4. **Multiple convention-direction issues across M-claims** (M15
   non-monotone, M16 inverse-of-Ω, M19 Ω vs 1/Ω, M21 factor-of-2).
   These together suggest the canonical brief's Ω-conventions are
   inconsistent across sub-claims and should be unified before T2
   work begins.
5. **M14 + M17 are both definitional identifications** (MaxEnt
   choice; quadratic-variation choice). Their tier remains T1
   because the *identification* is a substantive choice even when
   the underlying theorem is canonical; the joint M13 + M14 + M17
   structure is what gives CRR its formal content.

### Queued for Session 3

- **Empirical-consistency reproductions for P1–P7, B1–B7.** The
  conventions/identifications flagged in Session 2 must be resolved
  (or explicit choices documented) before consistency files can be
  written without inheriting downstream ambiguity. Suggested order:
  - **P1 (Solar Hale CV).** SILSO v2.0 fetch; reproduce CV =
    0.0796 prediction vs empirical 0.0767–0.0820.
  - **P2 (GWTC-1/2/3 BBH CV).** LIGO public data; replicate
    CV = 0.099, CI [0.077, 0.114].
  - **P3 (atomic spectral CV).** NIST atomic-spectra database;
    aggregate across 49 elements.
  - **B3 (AGI-26 phase-gating).** AGI-26 dataset (in repo as PDF;
    underlying data location to confirm).
  - **B5 (EEG class ordering).** PhysioNet EEG cohorts.
  - **P5 (CSEP California).** Already has reported null result;
    document the downgrade-by-evidence pathway.
  - **P4 (dark energy).** Pantheon+ / DES Year-3 SN compilation.
- **Author review queued items:** the 11 convention/identification
  issues listed in `notes/classification_table.md` "Session 2
  caveats" table. None block Session 3 progress; consistency
  reproductions can proceed under the most-natural resolution and
  flag any sensitivity.

### Stop-for-review

Session 2 stops here per the campaign discipline. 21 promotions
T0 → T1. Awaiting review to unblock Session 3.
