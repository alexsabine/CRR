# CRR Claim Decomposition

This document enumerates every distinct propositional claim CRR makes,
derived from the canonical formulation in `CAMPAIGN.md` PART I, refined
against the canonical source files in this repository:

- `CRR canonical proof sketch.md`
- `canonical_crr_rigorous_proof_sketch.md`
- `CRR_Complete_Proof_Sketch.md`
- `CRR_COMPREHENSIVE_SUMMARY.md`
- `crr_first_principles_proofs.md`
- `crr_meta_theorem.md`
- `crr_full_proofs.md`
- `CRR_Church_eff.html` (canonical engine)

A claim is a definite propositional content amenable to evidence-based
classification. Rhetorical framing (e.g., "the mathematics of becoming")
is excluded by the discipline of `CAMPAIGN.md` PART III.

## Counting summary

| Domain               | Count | IDs |
|----------------------|-------|-----|
| Mathematical (M)     | 21    | M1–M21 |
| Physical / temporal (P) | 7  | P1–P7 |
| Biological / psychological (B) | 7 | B1–B7 |
| Philosophical (Ph)   | 7     | Ph1–Ph7 |
| **Total**            | **42** |     |

Each claim is initialised at tier T0 (speculation) per the campaign
discipline; promotions happen only when corresponding evidence files
are committed.

---

## Mathematical claims (M)

### M1. CV = Ω/2 with no free parameters
The coefficient of variation of inter-rupture intervals equals Ω/2,
derived from Bernoulli(1/2) variance of the n=1 rupture event combined
with the Wijsman / Jaynes argument. No fitted parameter.

**Source:** canonical brief; `CRR_CV_Derivation.pdf`; `CRR_Complete_Proof_Sketch.md` §19.

### M2. Z₂:SO(2) CV ratio is exactly 2 from arc-to-ring topology
Geodesic length doubles from open arc (π) to closed ring (2π); Ω halves;
CV halves. Ratio is topological, not parametric.

**Source:** canonical brief; `CRR_COMPREHENSIVE_SUMMARY.md`.

### M3. C·Ω = 1 saturates the Cramér-Rao bound
At rupture, the CRR equality is the equality case of the Cramér-Rao
inequality with C identified as accumulated Fisher information.

**Source:** `canonical_crr_rigorous_proof_sketch.md`; `crr_full_proofs.md` Part I.

### M4. C·Ω = 1 saturates the Heisenberg-Gabor uncertainty
Equivalent statement in time-frequency: the rupture point is the centre
of a minimum-uncertainty Gabor wavelet.

**Source:** canonical brief; `CRR_Complete_Proof_Sketch.md`.

### M5. Cramér-Rao saturation and Heisenberg-Gabor saturation are the same theorem
Under the conjugate-variable identification (time ↔ frequency, parameter
↔ estimator), the two equalities are a single theorem in two
parameterisations. **Likely a relabelling** — see `relabellings.md`.

**Source:** `crr_meta_theorem.md`.

### M6. Fourier transform is the trivial CRR limit
Setting C(τ) = τ, Ω = i/k, and removing Θ recovers exp(−ikτ). CRR
generalises Fourier on three independent axes.

**Source:** canonical brief.

### M7. φ is the dominant eigenvalue of the depth-two regeneration operator
For the symmetric depth-two recurrence r_{n+1} = r_n + r_{n−1}, the
golden ratio φ ≈ 1.6180 is the dominant root of x² = x + 1.

**Source:** canonical brief; elementary algebra.

### M8. Depth two is the minimum depth supporting KAM-stable ergodicity
Depth-one memory is Markov (no stable quasi-periodicity); depth-two with
φ-rotation is the smallest substrate on which KAM tori survive.

**Source:** canonical brief; `crr_full_proofs.md` Part III.

### M9. φ-rotated CRR on bounded depth-two substrate has singular-continuous spectrum
The spectrum is in the Fibonacci-chain class — neither pure point nor
absolutely continuous.

**Source:** canonical brief.

### M10. The fine-structure self-consistency equation has a unique stable fixed point at 1/α = 137.032
The equation α = exp(2π²α / (1 + (π−1)α)) / (16π²) admits a unique
stable fixed point. Empirical 1/α = 137.036.

**Source:** canonical brief; `crr_137(attempt).pdf`.

### M11. Z₂ + Z₂ → SO(2) composition gives ρ = −1/2
Anti-correlation between two Z₂ channels composing to one SO(2) channel
is ρ = −1/2, derived (not fitted).

**Source:** canonical brief.

### M12. Beauty B(C) = exp(C/Ω)·(C* − C) peaks at C* − Ω
Setting dB/dC = 0 gives the location of the maximum analytically.

**Source:** canonical brief.

### M13. C is identified with accumulated Fisher information I(θ)
Foundational identification underwriting M3, M14. Without this, M3 has
no semantic content.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md`.

### M14. exp(C/Ω) is the unique MaxEnt regeneration kernel under mean-coherence constraint
The exponential family with natural parameter η = 1/Ω and sufficient
statistic C is the maximum-entropy distribution given a constraint on
mean coherence.

**Source:** `CRR_Complete_Proof_Sketch.md` §13; `crr_full_proofs.md` Part I.5.

### M15. Z_n hierarchy: CV = n/(4π) for Z_n symmetry classes
Generalisation of M2 to arbitrary cyclic symmetry. Z_2 and SO(2) are the
n=1 and n→∞ endpoints.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md`.

### M16. Bonnet-Myers gives Ω = π/√κ on positively-curved statistical manifolds
The injectivity radius bound on a positively curved manifold sets a
geometric upper limit on Ω.

**Source:** `crr_full_proofs.md` Part I.3.

### M17. C is quadratic variation [μ,μ]_t in the martingale formulation
Coherence is the quadratic-variation process of the underlying
information-flow martingale.

**Source:** `crr_full_proofs.md` Part II.2; `crr_martingale_derivation.pdf`.

### M18. Rupture time τ_Ω is an optimal stopping time (SPRT equivalent)
The first crossing of C·Ω = 1 is the optimal stopping rule for a
sequential probability ratio test.

**Source:** `crr_full_proofs.md` Part II.6.

### M19. Poincaré recurrence + Kac's lemma make rupture inevitable for ergodic systems
Kac's lemma E[return time to A] = 1/μ(A) identifies Ω with the inverse
measure of the coherent region.

**Source:** `crr_full_proofs.md` Parts III.2–III.3.

### M20. Regeneration is a right Kan extension in the categorical formulation
R[χ] is the right Kan extension of the coherence-history functor along
the rupture inclusion.

**Source:** `crr_first_principles_proofs.md` §1.2; `CRR_Bounded_Kan_Extension_QED_v2.pdf`.

### M21. C·Ω = 1 simultaneously saturates Cramér-Rao, Heisenberg-Gabor, and the thermodynamic uncertainty relation
Three-way unification claim. M3 + M4 + a third saturation across
information, time-frequency, and dissipation.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Part IV.

---

## Physical / temporal claims (P)

### P1. Solar Hale cycle CV matches SO(2) prediction within 3.6%
SILSO Hale-cycle CV is reported in [0.0767, 0.0820], straddling the
SO(2) prediction CV = 1/(4π) ≈ 0.0796.

### P2. GWTC binary-black-hole population CV is consistent with SO(2), inconsistent with Z₂
Radiated-fraction CV from GWTC-1/2/3: 0.099, CI [0.077, 0.114].

### P3. Atomic spectral CV across 49 elements is consistent with the fine-structure derivation
Cross-element comparison of spectral CV values.

### P4. Dark-energy w = −1 crossing coincides with peak ρ_DE at z ≈ 0.5
Cosmological prediction tying dark-energy equation-of-state crossing to
the energy-density maximum.

### P5. Single-Ω CRR matches ETAS baseline on California seismicity (CSEP)
Null result: nested CRR underperforms; single-Ω CRR matches ETAS. This
result downgrades any unrestricted "nested CRR is universal" claim.

### P6. Ω = k_B T / κ_eff in physical thermodynamic systems
Identification of Ω with the ratio of thermal energy to effective
stiffness.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Definition 3.

### P7. Central-limit regularisation: CV^(n+1) ≈ CV^(n) / √M^(n) explains macro-scale determinism
Multi-scale CRR produces √M reduction at each level, recovering
classical determinism as a limit.

**Source:** `CRR_Complete_Proof_Sketch.md` §20.

---

## Biological / psychological claims (B)

### B1. Biological 1/f signals exhibit singular-continuous spectra in the Fibonacci-chain class
Empirical realisation of M9 in living systems.

### B2. HRV cohort CVs separate by pathology along Class B → A → C
Heart-rate-variability CVs map onto regulated / autonomous / noise-driven
classes by clinical category.

### B3. AGI-26 phase-gating signature: χ² = 8,041; conservation ratio 1.003; ρ = −1/2
Specific predicted statistical signature in the AGI-26 dataset.

**Source:** `AGI_Conference_2026 (Sabine, 2026).pdf`.

### B4. Anti-correlation ρ = −1/2 between perception and action channels
Empirical realisation of M11 in sensorimotor data.

### B5. EEG validation: 11/11 class orderings correct; CV ratio 1.93
Reported empirical match against the 2:1 prediction.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Part V.

### B6. 132-system CV cross-domain prediction with zero directional reversals
Aggregate falsifier-survival claim across 30+ domains.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Part V.

### B7. Memory is significance-weighted, not recency-weighted
The exp(C/Ω) kernel weights past states by their coherence, not their
recency, predicting that high-coherence remote events dominate
regeneration.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Part VI.

---

## Philosophical / phenomenological claims (Ph)

### Ph1. CRR formalises Whitehead's concrescence and satisfaction
Mapping: prehensive accumulation ↔ C; concrescence ↔ δ(now); objective
immortality ↔ R[χ].

### Ph2. CRR formalises Bergson's durée
The regeneration integral is offered as a mathematical reconstruction of
Bergsonian duration.

### Ph3. δ(now) marks the ontological present at which past is metabolised into future
Metaphysical claim about the temporal orientation of the rupture.

### Ph4. Beauty (B(C) maximum) lives at C* − Ω: agency lives at the edge
Aesthetic-ethical claim placing the optimal point of agency near, not at,
the rupture threshold.

### Ph5. Identity persists as change
Ontological claim about persistence under continuous regeneration.

### Ph6. Conscious experience arises at the coherence-rupture interface
Phenomenological claim about the location of consciousness in the CRR
cycle.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Part IX.

### Ph7. Psychological phase typology by Ω regime
Depression ↔ rigid low Ω; anxiety ↔ unstable Ω; trauma ↔ rupture without
regeneration. Specific clinical-category mapping.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Part IX.

---

## Notes on what is NOT a separate claim

The following appear in the canonical sources but are folded into other
claims rather than counted independently:

- *Three-class diagnostics (Class A/B/C)* — operationalises M1 and is
  the testable form of B2/B5; not a separate claim.
- *CRR-FEP correspondence table* — a structural mapping, not a claim
  with truth conditions; informs how M and Ph claims interact.
- *√2 as optimal precision-allocation ratio* — restates a known result
  (Kelly criterion / portfolio theory) under CRR labels; classified as
  a relabelling (see `relabellings.md`).
- *CV_Z₂ × C*_SO(2) = 1* — algebraic identity following from M1 and M2;
  not an independent claim.
- *132-system "no directional reversals"* — counted as B6, not as 132
  separate claims.
- *24-domain meta-theorem* — counted as a single methodological claim;
  the underlying derivations are M3, M4, M14, M17, M18, M19, M20.

## Notes on apparent inconsistency in the canonical brief

The brief states "At C·Ω = 1, exp(C/Ω) → e." Under the canonical
Z₂ Ω = 1/π, the rupture condition C·Ω = 1 forces C/Ω = π², so
exp(C/Ω) = e^{π²} ≈ 19333.7, not e. The two conditions C·Ω = 1 and
C/Ω = 1 coincide only at Ω = 1. Recorded for resolution in
`relabellings.md`; tier assignments for M3/M4/M21 must address this.
