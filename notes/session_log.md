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
  The brief's indicative list (M1–M12, P1–P5, B1–B4, Ph1–Ph5)
  expanded to surface claims the brief left implicit (e.g., the
  Fisher-information identification M13, the MaxEnt regeneration
  kernel M14, the Z_n hierarchy M15, the Bonnet-Myers Ω bound M16,
  the martingale and Kan-extension formulations M17/M20, the
  TUR unification M21, the EEG and 132-system aggregate claims
  B5/B6, the consciousness and clinical-typology claims Ph6/Ph7).
  Recorded in `notes/decomposition.md`.
- **Created 42 claim subdirectories** under `claims/`, each with a
  canonical `claim.md` and a `tier.md` initialised to T0.
- **Factored the canonical engine** from `CRR_Church_eff.html`
  (the JS `CRRAgent` class at lines 159–190) into
  `crr-engine/index.py`. Added 24 pytest cases covering: canonical Ω
  values, the topological 2:1 ratio, CV = Ω/2, the rupture condition
  C·Ω = 1, the beauty-peak location C* − Ω, agent operational
  semantics, coherence and regeneration integrals, the Fourier-limit
  kernel, and the φ recurrence φ² = φ + 1. **All 24 tests pass.**
- **Initialised** `notes/classification_table.md` as the central
  artefact, with all 42 claims at T0.
- **Wrote** `CAMPAIGN.md` as the root-level brief.
- **Updated** `README.md` with a campaign dashboard section.

### Surprises / findings

**Apparent inconsistency in the canonical brief.** The brief asserts
both "C·Ω = 1" (rupture) and "exp(C/Ω) → e at C·Ω = 1." These
conditions are mutually consistent only if Ω = 1, not for the
canonical substrates Z₂ (Ω = 1/π) or SO(2) (Ω = 1/(2π)). Under
canonical Ω, exp(C/Ω) at the rupture is e^{π²} ≈ 19,333 (Z₂) or
e^{4π²} ≈ 1.4 × 10¹⁷ (SO(2)), not e. Recorded in
`notes/relabellings.md` and asserted explicitly in two pytest cases
(`test_exp_kernel_at_rupture_for_unit_omega` and
`test_brief_exp_e_inconsistent_with_canonical_omega`). This is a
finding for the framework's author to resolve at review; the campaign
does not modify the canonical formulation per `CAMPAIGN.md` non-goals.

**Engine clamps exp(C/Ω) at 10.** `CRR_Church_eff.html` line 171
clamps `C/Ω` at 10 to avoid numerical blow-up. This means the
operational engine never realises the analytic exp at canonical
ruptures; it runs with a clamped surrogate. Recorded; no tier impact
yet but flagged for Session 3 when M-claim consistency tests will
need to choose between the analytic and engine-clamped semantics.

**M5 is likely a relabelling.** "Cramér-Rao saturation =
Heisenberg-Gabor saturation" is the standard conjugate-variable
correspondence in statistical signal processing. Per the discipline,
M5 may reach T1 as a derivation but is capped at T1 unless a
CRR-specific consequence is exhibited. Recorded.

**M14 (MaxEnt regeneration) is a borderline relabelling.** It is a
correct application of the canonical MaxEnt theorem; what makes it
non-trivial is the M13 identification of C with Fisher information.
M13+M14 together carry domain-specific content; M14 alone does not.

### Promotions / downgrades

None. Session 1 only initialises the table at T0.

### Queued for Session 2

- For each of M1–M21, produce a `derivation.md`. Mathematical claims
  with elementary derivations (M2, M7, M12 via calculus, M17 by
  definition) should be straightforward. Heavier lifts: M3/M4 (must
  pin down conjugate variables and Fisher-information identification
  before the saturation goes through), M8 (KAM-stability minimum
  depth — needs the actual KAM theorem statement applied to the
  recurrence), M9 (singular-continuous spectrum — Bombieri-Taylor /
  Sütő type arguments), M10 (numerical fixed-point existence and
  stability for the fine-structure equation), M16 (Bonnet-Myers
  injectivity-radius application), M19 (Kac's lemma applied to the
  coherent-region indicator), M20 (Kan-extension formalisation).
- Each derivation either machine-checked or step-by-step with each
  step numerically verified in a notebook executable from
  `crr-engine/`.
- Where a derivation reveals further relabellings, append to
  `notes/relabellings.md` and cap the tier accordingly.
- Resolve (or escalate to author) the exp(C/Ω) → e inconsistency
  before invoking it in any M3/M4/M21 derivation.

### Stop-for-review

Session 1 stops here per the brief. No promotions made. Awaiting
review to unblock Session 2.
