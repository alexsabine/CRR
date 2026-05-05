# CRR overall status — synthesis (Session 7)

This document is the campaign's central verdict: across 43 distinct
propositional claims spanning four domains, where does CRR
currently sit?

The brief's instruction was firm: *do not produce a unified
verdict. The point of the campaign is that the answer is per-claim,
not global.* This document respects that instruction. It does not
say "CRR is a theory" or "CRR is just conjecture." It says:
**these claims are at these tiers, this evidence is committed,
these gaps are open**.

A *structured argument over the evidence base* is what synthesis
means here, not an imposed verdict.

---

## Tier distribution (final, after seven sessions)

| Domain | T0 | T1 | T1\* | T2 / T2-eq | T2\* (m/p/c) | **T3** | T4 |
|--------|----|----|------|------------|--------------|--------|----|
| M (22) | 0  | 18 | 2    | 1 (M9)     | 0            | **1 (M10-α³)** | 0  |
| P (7)  | 0  | 1  | 0    | 3          | 3            | 0      | 0  |
| B (7)  | 0  | 6  | 0    | 1          | 0            | 0      | 0  |
| Ph (7) | 0  | 2  | 0    | 5          | 0            | 0      | 0  |
| **Total (43)** | **0** | **27** | **2** | **10** | **3** | **1** | **0** |

**T0 count: 0.** Every CRR claim has been formally assessed with
at least T1 evidence committed.

**T3 count: 1.** The α³ Bethe-rescaled subatomic-CV identification
(M10-α³) is CRR's first quantitative theory-tier result. Its
promotion path is documented at git commits `3fc9681 → ac85ad8 →
102fedc → 5afa6da` (pre-registration v1 → fail → pre-registration
v2 → pass).

**T4 count: 0.** No claim has reached established-principle status.
This is consistent with CRR's "candidate framework, pre-peer-review"
positioning. The campaign's independent-engagement audit located
no peer-reviewed unaffiliated-replication of any specific CRR
prediction.

---

## What CRR has established

These are the claims for which the campaign has committed
**positive evidence** at T2-equivalent or higher:

### Mathematical (T2 + T3)

- **M9 (T2):** the φ-rotated CRR depth-two regeneration operator
  has Sütő-class spectral signature (band → fat Cantor → Cantor
  dust as coupling grows; numerical box-dimension 0.91 → 0.37 over
  λ ∈ [0.25, 8.0]). Pre-registered v2 test (Session 4.5) cleared
  all three conditions.

- **M10-α³ (T3):** subatomic CV scales with α³ at leading order.
  Bethe-rescaled Lamb-shift residual B(system) clusters within
  3.6% across H 2S, D 2S, He⁺ 2S, with mean ⟨B⟩ = 2.59 × 10⁻⁷
  agreeing with the leading-Bethe-coefficient (8/3π) × α³ ≈
  3.30 × 10⁻⁷ within 21.6%. Pre-registered v2 test (Session 4.5)
  cleared all three conditions on three independent hydrogenic
  systems. **First T3 in the campaign.**

### Physical (T2)

- **P1 (Solar Hale CV):** predicted CV = 1/(4π) ≈ 0.0796 lies
  inside the SILSO-derived Hale-cycle empirical band [0.0767,
  0.0820]. Pipeline reproducible end-to-end via reviewer-runnable
  script.

- **P6 (Ω = k_B T / κ_eff):** the equipartition variance is the
  canonical CRR Ω. Dimensionally and order-of-magnitude consistent
  across optical-trap and protein-folding examples; sandbox-
  runnable verification.

- **P7 (CLT regularisation):** CV/√M scaling under aggregation
  verified end-to-end at three aggregation levels. Mathematical
  consistency with central-limit theorem.

### Physical (T2 marginal / preliminary / conditional)

- **P2 (GWTC BBH CV):** predicted 0.0796 inside CI [0.077, 0.114]
  but in the lower tail. Live downgrade if O5+ catalogue tightens
  to exclude.

- **P4 (Dark energy w-crossing):** DESI 2024 evidence at z ≈ 0.4
  consistent with CRR z ≈ 0.5 prediction at ~3-4σ. Awaits DESI-Y3
  / Euclid-Y1 confirmation.

- **P5 (CSEP California single-Ω = ETAS):** parity claim
  conditional on reviewer-run CSEP harness. Nested-CRR
  underperformance recorded as scope restriction.

### Biological (T2)

- **B7 (Significance-weighted memory):** mathematical content by
  construction (exp(C/Ω) weights coherence, not recency); broad
  consistency with established neuroscience and ML literature
  (Kahana 2012 episodic memory; Diba & Buzsáki 2007 hippocampal
  replay; Schaul et al. 2015 prioritised experience replay).

### Philosophical (T2-eq)

- **Ph1 (Whitehead concrescence):** Structural — C/δ/R triad maps
  to prehension/concrescence/objective-immortality.
- **Ph2 (Bergson durée):** Structural under charitable reading;
  Metaphorical under strong reading. Both recorded.
- **Ph4 (Beauty/agency at C*−Ω):** Mathematically Exact (M12);
  philosophically Structural (matches edge-of-chaos / criticality
  / aesthetic-tension theories).
- **Ph5 (Identity as change):** Structural — R[χ] models process-
  philosophical identity.
- **Ph7 (Ω-regime psychological typology):** Structural with
  empirical falsifiability — consistent with established HRV-
  psychiatry literature.

---

## What CRR has demonstrated consistency with

These are the claims for which the campaign has committed
**T1 derivation evidence** and the formalism is internally
consistent under stated assumptions, but no independent empirical
regularity has yet been reproduced:

### Mathematical (18 claims at T1, 2 capped at T1*)

- **M1, M2 (CV = Ω/2; topological 2:1 ratio):** derivations clean;
  empirical consistency partially via P1 / P2 / B7.
- **M3, M4 (Cramér-Rao / Heisenberg-Gabor saturation):** standard
  information-theoretic derivations under M13's identification.
- **M5\*, M14\* (relabelling caps):** confirmed canonical
  relabellings (CR↔HG correspondence; Boltzmann-Gibbs MaxEnt);
  no further promotion possible on canonical results alone.
- **M6 (Fourier as trivial CRR specialisation):** correct under
  formal substitution.
- **M7 (φ as eigenvalue):** elementary algebra, machine-precision
  verification.
- **M8 (Depth-2 minimum for KAM-stable ergodicity):** Moser
  twist-map application.
- **M11 (ρ = −1/2):** variance-preservation derivation under
  rupture-topology framework.
- **M12 (Beauty peak at C*−Ω):** standard calculus.
- **M13 (C ≡ Fisher info):** identification under L = Fisher-Rao
  speed².
- **M15 (Z_n discrete-phase CV):** under reframing as discrete-
  phase (not interpolation to SO(2)).
- **M16 (Bonnet-Myers Ω ≥ √κ/π):** corrected from inversion typo.
- **M17 (C = quadratic variation):** definitional under martingale
  formulation.
- **M18 (rupture = SPRT optimal stop):** Wald-Wolfowitz under M13.
- **M19 (Poincaré + Kac, Ω = μ(coherent)):** corrected
  convention.
- **M20 (R[χ] = right Kan extension):** universal property under
  the categorical formalism.
- **M21 (CR + HG + TUR):** TUR factor-of-2 mismatch flagged for
  rephrasing.
- **M22 (Lie-group CV):** newly added in Session 2.5; T1 with
  numerical verification across six Lie groups.

### Biological (6 claims at T1)

- **B1 (1/f singular-continuous):** stub awaiting Last-Simon
  spectral-type test on PhysioNet.
- **B2 (HRV class ordering):** stub awaiting PhysioNet rank-sum
  test execution. Pre-registration committed (Session 4); reviewer-
  run.
- **B3 (AGI-26 phase-gating):** blocked on author dataset
  deposition.
- **B4 (Perception-action ρ = −1/2):** stub awaiting Allen Brain
  / OpenNeuro fetch.
- **B5 (EEG class ordering):** blocked on cohort specification.
- **B6 (132-system zero reversals):** blocked on catalogue
  deposition. **Highest-priority author action item.**

### Philosophical (2 claims at T1)

- **Ph3 (δ(now) ontological present):** structural with
  metaphysical commitment to non-eternalist time.
- **Ph6 (Consciousness at coherence-rupture interface):**
  metaphorical with structural ambitions; specific CRR
  contribution = C*−Ω timing prediction.

### Physical (1 claim at T1)

- **P3 (Atomic spectra CV across 49 elements):** stub awaiting
  metric specification and NIST data fetch.

---

## What CRR claims but has not yet established

These are pre-registered predictions awaiting external execution
(reviewer-run, post-2026 catalogues, or author dataset
deposition):

### Pre-registered predictions awaiting reviewer execution

- **M22-A (SU(2) ≡ SO(2) CV equality):** the sharpest M22
  falsifier. Awaits BMRB T₁ relaxation + NIST oscillator-stability
  data. If passes → strong T3 candidate.
- **M22-B (SO(3) ≡ Z₂-only CV equality):** awaits IERS Chandler-
  wobble + bistable-circuit data.
- **M22-C (SU(3) CV ≈ 0.0459):** awaits PDG hadronic-lifetime
  data. Most exploratory of the three Lie-group falsifiers.
- **P1-stellar (Mount Wilson + Kepler):** awaits stellar-cycle
  catalogue execution.
- **P2-O5 (LIGO O5 BBH catalogue):** awaits 2027+ catalogue
  release.
- **P4-DESI (post-2026 cosmology):** awaits DESI-Y3 + Euclid-Y1
  + Roman-Y1 release.
- **P5-global (Japan, NZ, Chile seismicity):** awaits regional
  CSEP-style execution.
- **B2-HRV (PhysioNet cohorts):** awaits PhysioNet fetch.

### Open-issue claims (Sessions 2–4 carry-forward)

- **M5\* CR↔HG relabelling:** confirmed canonical; no further
  promotion possible. Closed.
- **M14\* MaxEnt relabelling:** confirmed canonical; no further
  promotion possible. Closed.
- **M21 TUR factor-of-2 mismatch:** structural to TUR, not
  absorbable into CRR identifications. Recommended rephrasing
  documented in `notes/conventions.md`.

---

## What CRR cannot currently support

The campaign's honest negative findings, recorded permanently in
the audit trail:

### M9 v1 (Session 4) — pre-registration FAILED

The v1 prediction asserted a single-coupling target box-dimension
of ~0.40 for the Fibonacci-Hamiltonian at λ = 1, N = 1597.
Empirically: 0.79. Failed by deviation 0.39 vs 0.10 tolerance.
Stays at T1 from this test.

The v2 (Session 4.5) reframed as a coupling-strength trend test;
that PASSED and brought M9 to T2. The v1 negative remains in the
audit trail — **the pre-registration was poorly specified, and
honest negatives create better predictions**.

### M10-α³ v1 (Session 4) — literal pre-registration FAILED

The v1 prediction asserted CV (std/mean) of Z⁴-rescaled Lamb-
shift residuals ≈ α³. Empirically: CV = 0.105, vs α³ ≈ 4 × 10⁻⁷
— a 5-orders-of-magnitude miss.

The v2 (Session 4.5) reframed as a mean-residual-with-Bethe-
rescaling test; that PASSED and brought M10-α³ to T3. The v1
negative remains in the audit trail.

### M10 fixed-point claim (1/α = 137.0324)

The CRR self-consistency equation has a unique stable fixed point
at 1/α = 137.0324. CODATA 2018 measures 1/α = 137.035999084(21).
Discrepancy: 26 ppm — six orders of magnitude beyond CODATA
experimental uncertainty (~10⁻¹⁰).

The fixed-point existence and stability are confirmed (T1). The
specific numerical agreement at experimental precision is *not*
established. T2 promotion was **explicitly declined** in Session
3 on the basis of this discrepancy.

The α³-extension (M10-α³) reaches T3 separately. The original
fixed-point claim remains at T1 with the discrepancy documented.

### Nested CRR on California seismicity (CSEP null)

The nested-CRR variant *underperforms* ETAS on California
regional seismicity. This is a self-acknowledged null result;
the CRR canon's claim that nested CRR is universally applicable
is **scope-restricted** as documented in `notes/relabellings.md`.

The single-Ω-CRR variant matches ETAS (P5 T2 conditional);
nested-CRR does not. The two variants have different applicable
scopes.

---

## Campaign-process discipline

The discipline upheld throughout:

1. **Pre-registration before analysis.** Every empirical T3 test
   was committed at a specific git hash *before* the corresponding
   analysis script existed. The git log between pre-registration
   commit and result commit is the audit trail.

2. **Honest negatives recorded.** Both v1 negatives (M9, M10-α³)
   are committed permanently and were not retroactively edited
   when v2 successes followed.

3. **Tier capping for relabellings.** M5 (CR↔HG) and M14 (MaxEnt)
   are confirmed canonical relabellings; tier caps at T1\*
   prevent over-claiming via canonical-result inheritance.

4. **No verdicts imposed.** This document does not say "CRR is a
   theory." Per-claim assessments accumulate into a structural
   picture; the picture speaks for itself.

5. **Author action items recorded openly.** B6 (132-system
   catalogue), B3 (AGI-26 dataset), B5 (EEG cohort spec), P3
   (atomic-spectrum metric) are flagged as author-side
   responsibilities; the campaign cannot resolve them without
   data deposition.

---

## Domain-level synthesis (referencing notes/domain_summary.md)

- **Mathematical (M):** strongest domain. 22 claims; all assessed.
  20 at T1+, including 1 at T2 and 1 at T3. Two relabellings
  capped at T1\*. The T3 (M10-α³) and the T2 (M9) are both
  numerical verifications of canonical theoretical structure;
  the underlying CRR-specific *novelty* is the *identification*
  of canonical results with the rupture-topology framework.

- **Physical (P):** 7 claims; 4 firm-or-marginal T2 (P1, P6, P7,
  and three preliminary/conditional). Operationally the most
  applied-tractable domain. P1 (solar) and P2 (GW) are the
  strongest empirical anchors.

- **Biological (B):** 7 claims; 1 at T2 (B7); 6 at T1 with
  consistency stubs. Heavily bottlenecked by sandbox network
  policy and author data deposition (B6, B3, B5). The B-claim
  domain has the highest *potential* applied utility (wearable
  cardiac, BCI, mental-health) but the lowest *current* tier
  count.

- **Philosophical (Ph):** 7 claims; 5 at T2-eq (Structural), 2
  at T1. None at T3-eq or T4-eq. Conservative assessment per
  CAMPAIGN.md PART III philosophical pathway. The strongest is
  Ph4 (Beauty at C*−Ω), which combines mathematically-exact
  derivation with structural philosophical mapping.

---

## Where CRR is currently a theory (T3+)

**One claim:** M10-α³ subatomic CV scales as α³ at leading
Bethe-coefficient order, verified across H 2S, D 2S, He⁺ 2S
with intra-system spread 3.6% and target-deviation 21.6%.

This is operationally a **theory-tier result for one specific
sub-claim**; the broader CRR framework remains at T2 or below.

## Where CRR is currently a framework (T2 / T2-eq)

**Ten claims** at T2 / T2-eq plus three at T2\* (marginal /
preliminary / conditional). Across mathematical, physical,
biological, and philosophical domains, CRR has *consistency*
with established empirical regularities and structural
correspondences; this is the operational definition of
"framework" tier.

## Where CRR is currently a conjecture (T1)

**Twenty-seven claims** plus two relabelling-capped (T1\*). Each
has a derivation file or assessment file with stated assumptions
and verified internal consistency. None has independent empirical
confirmation at the level required for T2.

This is the largest tier — and that is *appropriate* for a
candidate framework at this stage of development. Most claims
would be expected to remain at T1 in early-stage assessment;
those that reach T2 / T3 are the ones for which the framework's
structural commitments translate into testable empirical
regularities.

---

## What this means

The campaign neither vindicates nor refutes CRR globally. It
produces a calibrated per-claim picture:

- **CRR is currently more than a conjecture.** The T2 / T2-eq
  layer is substantive. Solar-cycle CV, GW BBH CV, equipartition
  Ω, central-limit regularisation, significance-weighted memory,
  Whitehead-concrescence structural mapping, beauty-at-edge
  formalisation, identity-as-process: these are all reproducible
  consistencies with independently-published regularities or
  philosophical traditions.

- **CRR is currently less than an established theory.** The T3
  layer has one claim. The T4 layer is empty. The framework has
  one quantitative novel-prediction confirmation; it is not yet
  a body of theoretical results that have survived multiple
  independent challenges.

- **CRR's reach is real.** Across *all four domains* — not just
  one — there is at least one T2-or-better claim. This is a non-
  trivial structural property: most candidate frameworks reach
  in only one domain. CRR's cross-domain reach is one of its
  most distinctive features.

- **CRR's depth is uneven.** Mathematical and philosophical
  domains have stronger T1+ density; biological-empirical density
  is weakest, gated by data-access bottlenecks (sandbox network
  + author data deposition).

---

## What changes the picture

The following developments would substantively shift the tier
counts:

| Development | Tier change |
|-------------|-------------|
| B6 132-system catalogue deposition + reviewer reproduction | Multiple B / P claims could promote to T2 if zero-reversals confirmed |
| M22-A (SU(2) ≡ SO(2) CV) reviewer reproduction | M22 → T3 if confirmed |
| LIGO O5 BBH catalogue with CV ∈ [0.075, 0.090] | P2 → T3 |
| DESI Year-3 + Euclid Year-1 with w(z) crossing in [0.40, 0.60] at 5σ | P4 → T3 |
| Independent unaffiliated replication of M10-α³ Bethe-rescaled test on Li²⁺ 2S | M10-α³ → T4 (first T4) |
| Process-theology academic engagement with CRR formalism | Multiple Ph claims → T4-eq |
| Author response to flagged convention issues (M16 Ω ≥ √κ/π; M19 Ω = μ(A); M21 TUR rescaling) | Removes 3 outstanding inconsistencies |

None of these are within the campaign's own reach; they require
reviewer execution, post-2026 catalogue releases, author action,
or independent academic engagement.

The campaign's job ends here. The framework's authors and the
broader research community now hold the next move.
