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

### M2. Z₂ rupture is a half-turn (index-2 subgroup) embedding inside SO(2)
**[RESOLVED — reworded per `notes/conventions.md` recommendation]**
Not "Z₂ vs SO(2) substrates" (a false parallel). SO(2) = ℝ/2πℤ carries
a natural Z₂ action by antipodal identification θ ~ θ+π; the Z₂
rupture-only geodesic (π) is exactly the SO(2) closed-geodesic (2π)
divided by the order of this subgroup (2). The ratio is the *order of
the Z₂ subgroup*, forced in any consistent normalisation — not two
independently-measured lengths compared post hoc. Generalises to any
compact G containing Z₂ as a discrete subgroup: rupture-only geodesic
= φ_G / 2 (M22).

**Source:** canonical brief; `CRR_COMPREHENSIVE_SUMMARY.md`; derivation in `notes/rupture_topology.md` H2.

### M3. C·Ω = 1 saturates the Cramér-Rao bound (in geometric units; see C3)
At rupture, the CRR equality is the equality case of the Cramér-Rao
inequality with C identified as accumulated Fisher information. Holds
in Ω_geo units. Do not additionally invoke "exp(C/Ω)→e at C·Ω=1" —
that identity holds only in the separate Ω_int (Z₂-intrinsic) units
(`notes/conventions.md` C3); conflating the two units is the source
of the apparent inconsistency flagged below ("Notes on apparent
inconsistency in the canonical brief").

**Source:** `canonical_crr_rigorous_proof_sketch.md`; `crr_full_proofs.md` Part I.

### M4. C·Ω = 1 saturates the Heisenberg-Gabor uncertainty (algebraic form only)
Equivalent statement in time-frequency: the rupture point is the centre
of a minimum-uncertainty Gabor wavelet. Per `Alexander/boundary_is_a_rate`
§4, this kinship holds only as an algebraic form (same dimensionless
saturated-uncertainty structure), not a literal identification of C, Ω
with the conjugate physical variables Δt, ΔE — state it that way rather
than as a stronger physical identity.

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

### M15. Z_n hierarchy: CV = n/(4π) for Z_n discrete-phase symmetry classes
Generalisation of M2 to arbitrary cyclic *discrete*-phase symmetry
(n equally-spaced points on a circle, geodesic 2π/n between adjacent
points). **[RESOLVED, corrected per `notes/conventions.md` C2]** SO(2)
is *not* the n=1 or n→∞ endpoint of this sequence — it is a
structurally distinct continuous-phase manifold (φ_SO(2) = 2π, fixed,
not a limit of φ_{Z_n} = 2π/n). CV = n/(4π) is monotonically
*increasing* in n and diverges as n→∞, while SO(2)'s CV = 1/(4π) is
smaller than every Z_n≥2 value — the two families do not interpolate.
See `claims/M15_zn_symmetry_hierarchy/derivation.md`.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md`; corrected in `claims/M15_zn_symmetry_hierarchy/derivation.md`.

### M16. Bonnet-Myers gives Ω ≥ √κ/π on positively-curved statistical manifolds
**[RESOLVED — inversion typo corrected per `notes/conventions.md` C4]**
Bonnet-Myers bounds the diameter, not Ω, directly: D ≤ π/√κ. Under
Ω = 1/D (C4: Ω is *inverse* geodesic length), this gives Ω ≥ √κ/π, with
equality (Ω = √κ/π) on the saturating round sphere — not Ω = π/√κ as
originally stated, which inverts the bound.

**Source:** `crr_full_proofs.md` Part I.3; correction in `notes/conventions.md` C4.

### M17. C is quadratic variation [μ,μ]_t in the martingale formulation
Coherence is the quadratic-variation process of the underlying
information-flow martingale.

**Source:** `crr_full_proofs.md` Part II.2; `crr_martingale_derivation.pdf`.

### M18. Rupture time τ_Ω is an optimal stopping time (SPRT equivalent)
The first crossing of C·Ω = 1 is the optimal stopping rule for a
sequential probability ratio test.

**Source:** `crr_full_proofs.md` Part II.6.

### M19. Poincaré recurrence + Kac's lemma make rupture inevitable for ergodic systems
**[RESOLVED — convention corrected per `notes/conventions.md` C5]**
Kac's lemma gives E[return time to A] = 1/μ(A). Identifying this with
the mean inter-rupture interval 1/Ω gives **Ω = μ(A_coherent)**, not
Ω = 1/μ(A_coherent) as originally stated — the brief's inverse reading
was a sign error in the identification, now corrected.

**Source:** `crr_full_proofs.md` Parts III.2–III.3; correction in `notes/conventions.md` C5.

### M20. Regeneration is a right Kan extension in the categorical formulation
R[χ] is the right Kan extension of the coherence-history functor along
the rupture inclusion.

**Source:** `crr_first_principles_proofs.md` §1.2; `CRR_Bounded_Kan_Extension_QED_v2.pdf`.

### M21. C·Ω = 1 does NOT simultaneously saturate Cramér-Rao, Heisenberg-Gabor, and the thermodynamic uncertainty relation
**[OPEN — genuine, unresolved mismatch, not dissolved by the H1/H2/H3
rupture-topology reframing.]** The three-way unification claim fails
for TUR specifically: the thermodynamic uncertainty relation reads
Var(J)/⟨J⟩² ≥ 2/Σ, i.e. Σ·Var(J)/⟨J⟩² ≥ 2. Direct identification
C ↔ Σ, Ω ↔ Var(J)/⟨J⟩² gives C·Ω ≥ 2 at TUR saturation, not the
canonical C·Ω = 1. `crr-engine/tests/test_derivations.py::test_M21_tur_factor_two`
demonstrates the mismatch numerically. Either (a) restrict the
saturation claim to Cramér-Rao alone (drop TUR from M21), or (b)
state TUR saturation as C·Ω = 2 explicitly and stop describing it as
the same C·Ω = 1 condition. This decision is left to the framework's
author; until made, M21 should not be cited as a confirmed three-way
identity.

**Source:** `CRR_COMPREHENSIVE_SUMMARY.md` Part IV; mismatch documented in `notes/conventions.md` (M21 row) and `notes/relabellings.md`.

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

**[RESOLVED per `notes/conventions.md` C3.]** The brief states "At
C·Ω = 1, exp(C/Ω) → e." Under the canonical Z₂ Ω = 1/π, the rupture
condition C·Ω = 1 forces C/Ω = π², so exp(C/Ω) = e^{π²} ≈ 19333.7,
not e. The two conditions C·Ω = 1 and C/Ω = 1 coincide only at Ω = 1.

Resolution: the brief was conflating two distinct quantities both
called Ω — Ω_geo = 1/φ_G (the geometric quantity used throughout the
Ω table, M2, M22) and Ω_int = 1 (a separate Z₂-intrinsic normalisation
in which C is measured directly in Bernoulli-draw units). "exp(C/Ω)→e
at C·Ω=1" is correct *only* in Ω_int units; the rupture-as-geometric-
event reading (M3, the Ω table, M22) is correct in Ω_geo units. Any
formula using Ω must now specify which. This has been applied to
`CAMPAIGN.md` PART I and to M3/M4 above; tier assignments for M3/M4
should cite the disambiguated (Ω_geo) reading. M21 remains open for a
different reason (the TUR factor-of-2 mismatch, not this conflation).
