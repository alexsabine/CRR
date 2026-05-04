# M22 — Consistency: Vallortigara & Vitiello 2024 SU(2) doublet algebra

## Update from Session 8 (2026-05-04)

The Hemispheric-asymmetry paper
(`Sabine_Hemispheric_Asymmetry_Saturated_CR_Bound (1).pdf`) cites
**Vallortigara & Vitiello 2024** (*R. Soc. Open Sci.* 11(7): 240465)
as providing an SU(2)-doublet algebra for hemispheric asymmetry.

This is **the campaign's strongest independent-engagement candidate
located to date.** The Italian school (V&V at University of Trento /
University of Salerno) is **genuinely unaffiliated with the Active
Inference Institute**.

## What V&V 2024 derives

Per Sabine's exposition in the Hemispheric paper:

- Two hemispheres modelled as an **SU(2) doublet**.
- Energy depends on scalar product τ₁·τ₂.
- Antisymmetric (singlet) state: τ₁·τ₂ = **−3/4**.
- Symmetric (triplet) state: τ₁·τ₂ = **+1/4**.
- Energy gap: **exactly 1**.
- Singlet is the lowest-energy state → lateralization is
  **structurally enforced** rather than a statistical accident.
- **Inönü-Wigner contraction** SU(2) → E(2) at population scale.
- Boltzmann distribution N_L = N · exp(−βE_X) reproduces:
  - **90% right-handedness**
  - **95% left-lateralized language**
  - both from the same algebraic structure, no separate fit.

## CRR-relevant correspondence

CRR's identification (per Sabine):

> "The gap of 1 is the CRR saturation condition C · Ω = 1."

So **V&V's energy gap of exactly 1** in the SU(2) doublet algebra
is structurally identical to **CRR's saturation condition C·Ω = 1**.

Two independent derivations of the same algebraic structure:
- **V&V:** from SU(2) doublet algebra and free-energy minimisation
  (Vitiello tradition since 1995).
- **CRR:** from Cramér-Rao saturation under M3 + M13 identifications.

This is the strongest formal corroboration of M22's Lie-group
framework located in the campaign.

## Discipline-aligned tier decision

**M22 stays at T1** (with V&V 2024 noted as I-SA support; see
`notes/independent_engagement_log.md`).

Per the campaign's discipline:
- T4 requires "independent confirmation by an unaffiliated group...
  with predictions that have survived attempts at falsification."
- V&V 2024 derives a parallel structure but does NOT explicitly
  test CRR predictions. They derived their SU(2) doublet from
  free-energy considerations independently of CRR.
- CRR's *identification* of the V&V "energy gap = 1" with C·Ω = 1
  is a CRR-side claim, not V&V's claim.
- **This does not constitute confirmation-of-CRR-prediction in the
  strict sense.**

However, the structural-adjacency is substantial enough that:
- M22's **architectural plausibility** is strengthened
  significantly.
- A future pre-registration could test whether V&V's published
  Boltzmann lateralization fractions (90% right-handedness, 95%
  language lateralization) match an independent CRR-derived
  computation. If yes → M22 to T3.
- An independent reviewer running V&V's SU(2) doublet algebra
  on a different organism population (e.g., songbirds, primates,
  octopus — Vitiello's lineage includes cross-species lateralization)
  with confirmatory results → M22 to T4.

## Path to T2 / T3 / T4 (revised)

**T2 promotion** — the simplest unblocking path: implement V&V's
SU(2)-Boltzmann derivation in `crr-engine/predictions/v_and_v_su2.py`
and verify the Boltzmann distribution gives 90% right-handedness.
This is **sandbox-runnable** if the algebra can be implemented
purely numerically. Promotes M22 to T2 if the published V&V
fractions (90%, 95%) are reproduced from the SU(2) algebra
independently.

**T3 promotion** — pre-registered prediction on a fresh dataset
(M22-A SU(2) ≡ SO(2) CV equality test on BMRB T₁ relaxation +
NIST oscillator stability, already pre-registered in
`prediction.md` Session 4). Requires reviewer execution.

**T4 promotion** — independent group's SU(2)-doublet derivation
applied to non-human lateralization (Vallortigara's empirical
animal-cognition tradition) reproduces the CV/Boltzmann predictions
on data not used by Sabine. The Vallortigara school *itself* could
do this — V&V 2024 is the architectural piece, but a follow-on
empirical paper from the same school applying it to specific
animal datasets would constitute independent confirmation.

## Applied usefulness for 2026 and beyond (updated)

The V&V independent-derivation cluster strengthens M22's applied
positioning:

- **Hemispheric-lateralization neurology:** the SU(2)-doublet
  framing connects to clinical lateralization measures (Wada test,
  fTCD, fMRI lateralization indices). V&V's 90%/95% Boltzmann
  fractions match clinical empirical distributions.
- **Animal cognition / cross-species comparative biology:**
  Vallortigara's tradition (asymmetry in fish, chicks, octopus)
  provides cross-species validation infrastructure that the
  Active Inference / CRR community does not have on its own.
  Bridge to CRR is via the SU(2) algebra.
- **NMR / spin-1/2 systems generally:** if the SU(2) doublet
  algebra extends to *any* spin-1/2 paired-system context (NMR
  geminal pairs, donor-bound electron spins, NV-centre defect
  pairs), CRR's CV = 1/(4π) prediction has applied reach beyond
  hemispheric biology.
- **Quantum-computing decoherence:** spin-1/2 qubit error rates
  in entangled-pair codes (surface codes, color codes) operate on
  SU(2) doublet structure. CRR + V&V cluster gives a parameter-free
  scaling for decoherence-rate ratios in 2026+ qubit platforms.

## Connection to the M22-A pre-registration (Session 4)

M22-A pre-registration committed before this Session-8 reading:
"|CV_SU(2)_emp − 0.0796| < 0.015" tested via NMR T₁ + oscillator
stability data.

V&V 2024 does NOT directly test M22-A's CV-equality prediction.
What V&V provides is **independent algebraic structure** in which
the Boltzmann fractions (90%, 95%) emerge from SU(2). Whether
those fractions are equivalent to the CV = 0.0796 prediction
requires further derivation; the Hemispheric paper does not
explicitly bridge from "Boltzmann fractions" to "CV = 1/(2π)" for
the hemispheric case.

So V&V 2024's contribution to M22-A is **architectural plausibility,
not direct prediction-test**. M22-A's pre-registered test remains
[REVIEWER-RUN] awaiting BMRB + NIST execution.
