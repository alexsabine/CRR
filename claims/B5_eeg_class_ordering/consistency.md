# B5 — Consistency: hemispheric language-lateralization (Mazoyer 2014) + EEG claims

## Update from Session 8 (2026-05-04)

The hemispheric-asymmetry paper
(`Sabine_Hemispheric_Asymmetry_Saturated_CR_Bound (1).pdf`)
provides two empirical anchors that bear on B5:

1. **Hemispheric language-lateralization CV test (NEW; pre-registered
   prediction with explicit empirical comparison).**
2. **109+ EEG datapoints** confirming the CV ratio Z₂/SO(2) = 2
   (mentioned in the Hemispheric paper, Section 6 prediction table:
   "CV ratio Z₂/SO(2) = exactly 2 — Confirmed (109+ EEG)").

## I. Hemispheric language-lateralization (Mazoyer 2014)

### Prediction

CRR predicts CV = 1/(2π) ≈ **15.92%** for the typical-Gaussian
component of healthy hemispheric-language-lateralization-index
(HFLI) distributions. This is a Z₂-rupture prediction (binary
hemispheric switching).

### Empirical regularity

**Source:** Mazoyer, B. et al. (2014). *PLoS ONE* 9(6): e101165.
"Gaussian mixture modeling of hemispheric lateralization." n = 144
right-handers, 3-Gaussian mixture model (their Table 3, AICc =
1245.9).

| Component | Mean | SD | Fraction | CV |
|-----------|------|-----|----------|-----|
| G1 (typical-strong) | 65.3 | 8.0 | 67% | **12.25%** |
| G2 (typical-moderate) | 43.9 | 5.3 | 20% | **12.07%** |
| G3 (ambilateral) | 4.4 | 17.7 | 12% | — |

### Consistency check

**Predicted CV:** 15.92% (Z₂-rupture, parameter-free).
**Empirical CV:** 12.2% (mean of G1, G2).
**Deviation:** 23% below prediction.

**Structural sub-confirmation:** G1 (mean=65.3, SD=8.0) and G2
(mean=43.9, SD=5.3) — different means and different SDs — produce
**near-identical CV (12.25% vs 12.07%)**. The CV is a *topological
invariant* across the two components, even though the absolute
value disagrees with the CRR prediction by 23%.

This is the same pattern as the campaign's M10-α³ v1 negative:
the structural shape is right, the absolute value is off.

### Honest disclosure (Sabine's own assessment)

From the Hemispheric paper Section 6.2:

> "The framework has not been confirmed. But a framework whose
> prediction lands within 24% on the first attempt, with no fitted
> parameters, and which correctly predicts that two structurally
> different Gaussian components should have the same CV — that
> framework is worth refining rather than discarding."

Three diagnostic candidates Sabine offers:
1. **Class B regulation** — callosal inhibition compresses
   effective Ω from 1/π to ~0.244 (77% of canonical). Predicts
   split-brain patients should show CV closer to 15.9%.
2. **σ(C*) refinement** — equipartition assumption σ(C*) = 1/2
   replaced by σ(C*) ≈ 0.385 fits data exactly. Tests in other
   Z₂ systems would corroborate or refute.
3. **Geodesic-extent overshoot** — π → π+0.7 gives CV ≈ 13.0%.
   Predicts a consistent overshoot across lateralization tasks.

### Tier decision

**B5 stays at T1.** Per discipline:
- T2 requires "reproducing at least one independent empirical
  regularity not used to construct the claim." Mazoyer 2014 is
  independent and pre-CRR; the prediction is parameter-free.
- The empirical CV (12.2%) lies **outside** the canonical Class A
  band [0.06, 0.10] of B2's pre-registration (Session 4) and is
  **23% below** the canonical Z₂ prediction.
- Per the discipline, **the literal prediction is not confirmed**.
- **Structural sub-prediction (CV-invariance across G1, G2) IS
  confirmed.** This is a partial consistency.

The Hemispheric paper's interpretation that callosal regulation
explains the 23% gap is plausible *but is a post-hoc adjustment*,
not a pre-registered prediction. Per discipline, post-hoc fitting
does not retroactively confirm the original prediction.

**Tier upgrade pathway:** if a fresh pre-registration commits to
the Class B regulated reading (CV ∈ [0.10, 0.13] for callosally-
intact populations) and is confirmed on a *new* dataset, B5 could
promote. The campaign cannot do this in the sandbox.

## II. 109+ EEG datapoints (claimed)

The Hemispheric paper Section 6 prediction table cites:

> "CV ratio Z₂/SO(2) = exactly 2 — Confirmed (109+ EEG)"

This claim is **not detailed further** in the Hemispheric paper.
The 109+ EEG datapoints are referenced as confirming the 2:1 ratio
between Z₂ (bistable) and SO(2) (rotational) substrate CVs.

**Status:** **Pending dataset deposition.** The campaign cannot
verify this claim without:
- The specific EEG dataset(s) referenced.
- The processing pipeline (which features classified as Z₂ vs
  SO(2)).
- The per-feature CV computations.

This is **the same author-action item** as the original B5 claim
("11/11 class orderings; CV ratio 1.93"). The 109+ EEG anchor
appears to be the source of the original B5 claim (or an extension
of it), but the underlying data is not committed.

## III. Path to T2 / T3 for B5

The B5 claim has three avenues to T2 promotion:

1. **Author deposits the 109+ EEG cohort** with reproduction
   pipeline. Reviewer reproduces 1.93 ratio. → T2.
2. **Independent reviewer reproduces the Mazoyer 2014 CV test
   on a different cohort** (UK Biobank, ENIGMA, Human Connectome
   Project). If 12.2% replicates → T2-as-Class-B-confirmation; if
   15.9% → T2-as-canonical-CRR.
3. **Pre-registered split-brain test** (per Sabine's diagnostic
   candidate i): CRR predicts split-brain CV ≈ 15.9% (no callosal
   regulation), normal CV ≈ 12.2% (regulated). Demonstrating this
   contrast would be sharp evidence for the callosal-regulation
   reading.

## Applied usefulness for 2026 and beyond (updated)

The hemispheric-CV reading has direct applied implications:

- **Callosal-integrity diagnostics:** if Ω reflects callosal
  regulation, CV measurement on lateralization tasks could serve
  as a non-invasive callosal-integrity proxy. Useful for surgical
  planning (Wada test alternative), epilepsy presurgical
  evaluation, multiple-sclerosis disease tracking.
- **Hemispheric-asymmetry-based psychiatric biomarkers:** Sabine's
  Section 5 connects high-Ω pathology (mania, psychosis, dissociation)
  and low-Ω pathology (anxiety, trauma, addiction) to the
  hemispheric-Ω regime. Wearable EEG-derived class label could
  integrate.
- **Brain-computer-interface decoders:** SU(2) / Z₂ phase structure
  predicts decoder priors for hemispheric BCI signals (Neuralink,
  Synchron, BrainGate). The phase-gating insight from the AGI 2026
  paper (B3) directly applies.
- **Anaesthesia-depth monitoring:** Class A vs B vs C transitions
  during induction / emergence are clinically tractable. CRR-derived
  CV labels supplement BIS / SedLine / CONOX.
- **Disorder-of-consciousness assessment:** CRR-derived CV in
  hemispheric phase-locking measurements could supplement Coma
  Recovery Scale-Revised in differential diagnosis (vegetative
  vs minimally conscious vs locked-in).

The empirical anchor (12.2% with structural CV-invariance) is
substantial enough that B5 has stronger applied potential than
its T1 status would suggest, *contingent on* the 23% deviation
diagnostics being resolvable.
