# CRR Prediction Validation Audit: Are the Predictions Actually Predictive?

**Auditor:** Claude (Anthropic), at request of Alexander Sabine
**Date:** 2026-02-05
**Scope:** All MD and Python files containing CRR predictions and empirical validations

---

## Executive Summary

This document provides a rigorous, independent assessment of whether the CRR (Coherence-Rupture-Regeneration) framework's claimed predictions are genuinely predictive, or whether they suffer from common methodological pitfalls: post-hoc fitting disguised as prediction, unfalsifiable claims, excessive degrees of freedom, or confirmation bias.

**Overall verdict:** The CRR repository contains a mix of genuinely interesting structural insights, some legitimately prospective predictions, and several claims that do not meet the standard of "prediction" in the scientific sense. The analysis below breaks this down domain by domain.

---

## Methodology of This Audit

For each claimed prediction, I assess:

1. **Temporal ordering**: Was the prediction actually made before the data was examined?
2. **Specificity**: Is the prediction precise enough to be falsified?
3. **Degrees of freedom**: How many free parameters are available to fit the data?
4. **Comparison to null models**: Does CRR outperform simpler alternatives?
5. **Independence of evidence**: Is the "validation" data truly independent?
6. **Confirmation bias risk**: Were disconfirming results honestly reported?

I use a 5-tier rating:

| Rating | Meaning |
|--------|---------|
| **GENUINELY PREDICTIVE** | A priori, specific, falsifiable, confirmed |
| **PARTIALLY PREDICTIVE** | Some predictive content, but with caveats |
| **DESCRIPTIVE (NOT PREDICTIVE)** | Fits existing data well, but not a genuine prediction |
| **UNFALSIFIABLE** | Too vague or flexible to be tested |
| **OVERCLAIMED** | The strength of the claim exceeds the evidence |

---

## Domain 1: Muscle Hypertrophy (crr_muscle_predictions.py, crr_muscle_validation.py)

### Claims Made

- 10/10 predictions confirmed
- R-squared = 0.9985
- Predictions made "BEFORE seeing data"

### Audit Findings

**The "predictions" are well-known exercise science facts, not novel CRR predictions:**

| CRR "Prediction" | Status in Exercise Science |
|---|---|
| P1: Diminishing returns | Textbook knowledge since the 1960s |
| P2: Genetic ceiling (FFMI ~25) | Established by Kouri et al. 1995 |
| P3: Novice gains faster than advanced | Universal coaching knowledge |
| P4: Minimum threshold intensity | Known since DeLorme 1945 |
| P5: Individual variation (3-4x) | Published by Hubal et al. 2005 |
| P6: MPS peaks at 24h, baseline by 48-96h | MacDougall et al. 1995 (the cited source) |
| P7: Muscle memory / faster regain | Gundersen 2016, Staron et al. 1991 |
| P8: Advanced need more recovery | Standard periodization theory |
| P9: Exponential approach to plateau | Any saturating growth model predicts this |
| P10: 2-3x/week optimal | Schoenfeld meta-analysis 2016 |

**The R-squared = 0.9985:** This is from fitting a 3-parameter model (`R_max`, `Omega`, `k`) to 12 data points using `scipy.optimize.curve_fit`. Any 3-parameter saturating function would achieve similar R-squared on monotonically increasing data approaching a plateau. For comparison, the simple 2-parameter exponential already achieves R-squared > 0.99 (as shown in the code itself).

**Critical issue with the data:** The `lean_mass_gain` array in the code is described as "synthesized from multiple sources" -- it is not raw empirical data but a hand-constructed consensus trajectory. Fitting a model to hand-constructed data and reporting R-squared is circular.

**Rating: DESCRIPTIVE (NOT PREDICTIVE)**

The CRR framework provides a *language* for describing muscle hypertrophy (coherence = training adaptation, rupture = training session, regeneration = MPS response). This is a valid interpretive mapping, but calling already-known phenomena "predictions confirmed" is overclaiming. No novel prediction was made that wasn't already established in exercise science.

---

## Domain 2: Wound Healing (crr_wound_analysis.py)

### Claims Made

- R-squared = 0.9989
- CRR "explains" the 80% maximum recovery ceiling
- Phase transitions align with clinical observations

### Audit Findings

**Model comparison is informative but the conclusion is wrong:**

The code fits four models: Exponential, Gompertz, CRR Simple, and CRR Full. The CRR Full model has **7 free parameters** (`S_max`, `Omega`, `k_inflam`, `k_prolif`, `k_remodel`, `t_inflam`, `t_prolif`) fit to **16 data points**. With 7 parameters and 16 data points, achieving high R-squared is expected regardless of the model's theoretical justification.

The Gompertz model (3 parameters) achieves comparable R-squared. The code's own analysis shows the CRR models don't dramatically outperform classical alternatives -- they achieve marginally better fit with substantially more parameters.

**The "80% ceiling explanation"** -- CRR claims this is because "regeneration can only access post-wound history, not developmental coherence." This is a restatement in CRR language of the established biological fact that adult wound healing involves fibrotic repair rather than true regeneration. The explanation doesn't generate any new testable predictions beyond what is already known from wound biology (e.g., fetal wounds heal scarlessly, which was known before CRR).

**The data itself:** The tensile strength values are described as "consensus from multiple studies" -- again, hand-constructed rather than raw experimental data.

**Rating: DESCRIPTIVE (NOT PREDICTIVE)**

The CRR model fits wound healing data, but so do simpler models with fewer parameters. The mechanistic interpretation (coherence lost at wound → can't regenerate developmental structure) is a restatement of known biology in CRR vocabulary.

---

## Domain 3: Cardiac RR Intervals (crr_cardiac_validation.py)

### Claims Made

- Prospective prediction made BEFORE data search
- 24-hour CV matches Z2 prediction to 3.8%
- Timescale-dependent symmetry discovered

### Audit Findings

**This is the strongest example of genuine predictive methodology in the repo.**

The protocol is clear: (1) classify system symmetry on physical grounds, (2) derive CV prediction, (3) search literature. The initial prediction (SO(2), CV ~ 0.080) was partially wrong -- the short-term CV is 0.058, the long-term is 0.165. The document honestly acknowledges the partial failure.

**However, several concerns:**

1. **Post-hoc symmetry switching:** The initial prediction (SO(2)) didn't match well. The 24-hour CV matches Z2 instead. The document then retroactively explains this as "timescale-dependent symmetry," which is an interesting insight but wasn't predicted a priori. The "3.8% error" claim cherry-picks the comparison that works (24-hour vs Z2) while downplaying the comparison that doesn't (5-minute vs SO(2), 28% error).

2. **Two predictions for one system:** CRR offers two possible CV values (0.080 and 0.159). With two candidates, the chance of one being "close" to an arbitrary empirical value doubles. The 24-hour CV of 0.165 being within 3.8% of 0.159 is notable, but the framework had a 50% chance of being "close" simply by offering two options.

3. **The CV prediction itself:** CV = Omega/2 is the core quantitative prediction. But where does CV = Omega/2 come from? It's derived from the CRR framework's own assumptions. Whether this relationship is a deep truth about nature or a mathematical artifact of the framework's construction is an open question.

**Rating: PARTIALLY PREDICTIVE**

The methodology is genuinely prospective, which is commendable. But the post-hoc symmetry switching and cherry-picking of the better match weaken the claim. A stronger test would pre-commit to a single prediction per system.

---

## Domain 4: Saltatory Growth (Saltatory_Guide.py)

### Claims Made

- 11/11 structural predictions confirmed
- Sleep cycle CV matches to 0.5% error

### Audit Findings

**The 11 "structural predictions" are mostly restatements of known biology:**

| Prediction | Pre-existing knowledge? |
|---|---|
| P1: Growth is punctuated | Lampl et al. 1992 (this IS the finding) |
| P2: Bursts complete within 24h | Lampl et al. 1992 |
| P3: Variable intervals | Lampl et al. 1992 |
| P4: Amplitude 0.5-2.5 cm | Lampl et al. 1992 |
| P5: Sleep-growth coupling | Lampl & Johnson 2011 |
| P6: Same pattern at multiple scales | Standard auxological observation |
| P7: Pubertal spurt pattern | Tanner stages, known since 1960s |
| P8: Multi-site coupling 1-8 days | Lampl & Johnson 2011 |
| P9: Individual variation | Universal biological observation |
| P10: Stasis not deficit | Lampl 1993 |
| P11: Chondrocyte phases map to CRR | This is the CRR mapping itself |

**The critical problem:** CRR is being "validated" against the very data that inspired its application to growth. The Lampl findings are the empirical basis, not independent validation. Saying CRR "predicts" Lampl's findings is like saying general relativity "predicts" the anomalous precession of Mercury -- it was designed to account for it.

**The sleep cycle CV claim (0.5% error):** The Saltatory_Guide.py claims sleep cycle CV = 0.224, matching the Dual-Z2 prediction of 0.225. However:

- The "empirical" CV of 0.224 is stated without a specific literature citation in the code
- The symmetry classification (Dual-Z2 for sleep) is assigned post-hoc -- there's no a priori reason why sleep must be Dual-Z2 rather than Z2 or SO(2)
- With three symmetry classes to choose from, the chance of one being close to any empirical value increases

**The category error defense:** The Saltatory_Guide.py spends significant effort explaining why the CV prediction doesn't apply to macro-saltation intervals (2-63 day range). This is intellectually honest and well-argued. However, it also means the quantitative CV prediction is effectively unfalsifiable for this domain: if the macro-level CV matches, it confirms CRR; if it doesn't, that's a "category error." The prediction only applies at a level (daily chondrocyte cycles) where direct measurement is extremely difficult.

**Rating: DESCRIPTIVE (NOT PREDICTIVE) for the 11 structural predictions**
**Rating: PARTIALLY PREDICTIVE for the sleep cycle CV, but with post-hoc symmetry assignment**

---

## Domain 5: Bone Remodeling, Coral Bleaching, Dwarf Novae (crr_empirical_validation_test.md)

### Claims Made

- Three novel systems selected a priori
- Kac's Lemma derivation of system-specific Omega
- Phase asymmetry predictions match empirical data

### Audit Findings

**The Kac's Lemma derivation is circular:**

The document derives Omega from Kac's Lemma: Omega = 1/mu(A), where mu(A) is the fraction of the cycle spent in the "coherent region." But mu(A) is computed FROM the empirical phase durations:

- Bone: mu(A) = 150/180 (formation phase / total cycle) → Omega = 1.2 → predicts asymmetry 3-5x
- Dwarf nova: mu(A) = 40/50 (quiescence / total cycle) → Omega = 1.25 → predicts asymmetry 4-6x

**This is circular.** The "prediction" of asymmetry is derived from the empirical asymmetry itself. You cannot use the observed phase durations to compute Omega and then claim Omega "predicts" the phase durations. The Kac's Lemma approach amounts to:

1. Observe that phase A takes fraction f of the cycle
2. Compute Omega = 1/f
3. "Predict" that phase A takes fraction 1/Omega = f of the cycle
4. Celebrate the "match"

**For coral bleaching,** the analysis is slightly better because it predicts the *order of magnitude* of asymmetry (10-100x) and the empirical value (50-500x) overlaps. But the range is so wide that it's hard to falsify.

**The qualitative CRR structure (accumulation → threshold → phase transition)** does genuinely describe these systems. But threshold-triggered dynamics are not unique to CRR -- they are described by any accumulate-and-fire model, dating back to Lapicque (1907).

**Rating: OVERCLAIMED for quantitative predictions (circular Kac's Lemma)**
**Rating: DESCRIPTIVE for qualitative structural mapping**

---

## Domain 6: 16 Nats Hypothesis (crr_16_nats_hypothesis.md)

### Claims Made

- 16 systems converge on ~16 nats information threshold
- Mean 15.6 nats, prediction 16 nats, within 95% CI
- "Well-supported" with p < 0.01

### Audit Findings

**The document itself acknowledges the key problem (credit for this honesty):**

> "NOTE: This document searches for deliberate 'curve fitted' and 'hard-coded' ways to derive 16 nats. It is a deductive check, not an inductive emergent finding."

This is critical. The analysis STARTS with 16 nats and then finds ways to reach it in each system. The calculations involve:

1. **Choosing what to multiply**: e.g., working memory = 4 chunks x 6 bits/chunk = 24 bits. But why 6 bits/chunk rather than 4 or 8? The choice of operands is flexible.

2. **Choosing integration windows**: e.g., neural integration = 15 spikes x 1.5 bits/spike = 22.5 bits. But the number of spikes in an "integration window" ranges from 5 to 50 in the literature. Choosing 15 gives you the answer you want.

3. **Choosing the number of dimensions/pathways**: e.g., absolute judgment = 2.8 bits x 8 dimensions = 22.4 bits. Why 8 dimensions? Because it gives ~16 nats.

4. **Very wide ranges reported as "matches"**: Protein folding: 8-24 bits (range includes prediction). This range is so wide it would include almost any prediction between 6 and 17 nats.

5. **The T cell calculation is emblematic**: TCR repertoire log2(10^7) = 23 bits... but this is the repertoire size, not the information at activation threshold. The actual threshold (8000 TCRs) gives log2(8000) = 13 bits = 9 nats, which DOESN'T match. So 10 bits of "antigen discrimination" are added to reach 23 bits. This additional term is chosen to make the total work.

**Statistical concern:** The claimed p < 0.01 assumes each system provides an independent measurement of the same quantity. But the "measurements" are not independent -- they are constructed calculations where the analyst has freedom to choose operands, integration windows, and which quantities to multiply.

**Rating: UNFALSIFIABLE / OVERCLAIMED**

The convergence is not from independent measurements but from constructive calculations with sufficient degrees of freedom to reach any target near 16 nats. The document's own disclaimer about this being a "deductive check, not inductive" is accurate and honest.

---

## Domain 7: Martingale Verification (crr_martingale_verification.py)

### Claims Made

- Theorem 6.2 (Wald's Identity): E[C_tau] = Omega -- VERIFIED
- Theorem 7.2 (Conservation): E[B_tau] = B_0 -- VERIFIED
- Proposition 7.3 (Variance): Var(B_tau) = Var(B_0) + Omega -- VERIFIED
- Theorem 9.1 (Regeneration weighting) -- VERIFIED

### Audit Findings

**These are mathematical theorems, not empirical predictions.** The verification code confirms that the simulation correctly implements the mathematical framework. This is internal consistency checking, not empirical validation.

Specifically:
- Wald's Identity for stopping times is a well-known result in probability theory
- Optional Stopping Theorem is a standard result
- The variance increase is a direct consequence of the setup

**The simulations verify that the code is correct, not that the theory describes reality.** This is analogous to verifying that a physics simulation correctly solves Newton's equations -- it tells you the code works, not that Newton's laws apply to any particular real-world system.

**Rating: NOT APPLICABLE (mathematical verification, not empirical prediction)**

---

## Domain 8: CRR-FEP Simulation (crr_simulation.py)

### Audit Findings

This file implements the theoretical framework as a simulation. It does not make or test empirical predictions. The Q-factor correlation analysis uses **invented data** (the substrate adaptivity values are not from published measurements but assigned by the author). The multi-armed bandit simulation demonstrates how CRR-modulated exploration works in a toy model, not against real data.

**Rating: NOT APPLICABLE (simulation/demonstration, not empirical test)**

---

## Cross-Cutting Issues

### Issue 1: The Omega Problem

CRR's quantitative power depends on the Omega parameter. But across domains, Omega is handled inconsistently:

- **Sometimes fixed a priori**: Omega = 1/pi (Z2) or 1/(2*pi) (SO(2)) -- but the symmetry class is chosen post-hoc
- **Sometimes fitted**: curve_fit recovers Omega from data (e.g., muscle: Omega = 2.0, wound: Omega = 3.0)
- **Sometimes derived from data**: Kac's Lemma using empirical phase fractions (circular)

When Omega is a free parameter fit to data, CRR is just a parameterized curve-fitting model. When it's fixed a priori, the symmetry class assignment is the degree of freedom.

### Issue 2: CRR vs. Simpler Models

The fundamental CRR structure (accumulate → threshold → reset) is isomorphic to:

- Integrate-and-fire models (neuroscience, since 1907)
- Cumulative damage models (engineering reliability)
- Renewal theory (probability)
- Excitable systems (nonlinear dynamics)

The claim to novelty rests on: (a) the exp(C/Omega) memory weighting in regeneration, and (b) the specific Omega values tied to symmetry classes. However, (a) is a standard MaxEnt/Boltzmann weighting, and (b) remains unproven.

### Issue 3: Confirmation Bias in Validation

The repository reports validations across ~7 domains with high success rates (10/10, 11/11, R-squared > 0.99). There is no mention of domains where CRR was tried and failed, or predictions that were disconfirmed. The cardiac validation is the one exception, where partial failure is honestly reported. This pattern raises concern about selection bias -- are we seeing the highlight reel?

### Issue 4: The "Before Seeing Data" Claim

Several files claim predictions were made "BEFORE seeing data." This is difficult to verify in a repository without timestamped commits showing the prediction files existed before the validation files. The muscle predictions file (`crr_muscle_predictions.py`) is dated "December 2024" in its header, but the repository doesn't provide git history evidence of this ordering.

---

## Summary Assessment

| Domain | Claim | Rating | Key Issue |
|--------|-------|--------|-----------|
| Muscle hypertrophy | 10/10 confirmed | DESCRIPTIVE | Predictions are pre-existing exercise science |
| Wound healing | R-sq=0.9989 | DESCRIPTIVE | 7-param model on 16 points; Gompertz comparable |
| Cardiac RR | Prospective, 3.8% error | PARTIALLY PREDICTIVE | Post-hoc symmetry switching |
| Saltatory growth | 11/11 confirmed | DESCRIPTIVE | Predictions are the source data |
| Bone/coral/nova | Asymmetry matches | OVERCLAIMED | Circular Kac's Lemma derivation |
| 16 nats | 15/16 match | UNFALSIFIABLE | Constructed calculations with free operands |
| Martingale | Theorems verified | N/A | Math verification, not empirical |
| CRR-FEP simulation | Framework demo | N/A | No empirical test |

---

## What IS Genuinely Valuable in CRR

Despite the above criticisms, CRR offers several genuine contributions:

1. **A unifying vocabulary**: The C-delta-R structure provides a consistent language for discussing threshold-triggered dynamics across domains. This has pedagogical and conceptual value even if the predictions are post-hoc.

2. **The Omega-as-system-character idea**: The notion that a single parameter captures whether a system is rigid (frequent micro-ruptures) or fluid (rare transformative ruptures) is a useful organizing principle.

3. **The memory weighting insight**: exp(C/Omega) weighting in regeneration is a principled (MaxEnt) way to formalize how systems weight their history. This is theoretically well-motivated.

4. **The cardiac validation methodology**: The prospective protocol (classify → predict → search → compare) is the right way to test CRR. More of this is needed.

5. **Intellectual honesty in several places**: The Saltatory_Guide's "category error" discussion, the 16 nats "deductive check" disclaimer, and the cardiac validation's admission of partial failure are commendable.

---

## Recommendations for Strengthening CRR's Predictive Claims

1. **Pre-register predictions**: Before applying CRR to a new domain, publish the specific quantitative prediction (including which symmetry class and why) in a timestamped, publicly accessible format.

2. **Single prediction per system**: Commit to ONE CV or Omega value per system before seeing data. Don't offer Z2 and SO(2) as options and claim the one that matches.

3. **Use raw data**: Stop fitting models to "consensus" or "synthesized" data. Use specific datasets with proper error bars.

4. **Report failures**: Document domains where CRR predictions failed. The absence of negative results is a red flag.

5. **Benchmark against null models**: Always compare CRR models against the simplest alternative (exponential, logistic, Gompertz) with matching parameter counts. Use AIC/BIC for model comparison.

6. **Derive Omega independently**: The Kac's Lemma approach must derive Omega from system properties OTHER than the phase durations it aims to predict. Otherwise it's circular.

7. **The killer test**: Find a system where CRR predicts something that NO other framework predicts, test it prospectively, and publish the result regardless of outcome.

---

## Conclusion

CRR is a **mathematically coherent descriptive framework** that provides a useful vocabulary for understanding threshold-triggered dynamics with memory. Its theoretical foundations (integrate-and-fire, MaxEnt, first-passage time theory) are solid and well-established.

However, the empirical "validation" claims in the repository are substantially overclaimed. Most "predictions" are restatements of known phenomena, the quantitative fits use flexible multi-parameter models on hand-constructed data, and the one genuinely novel prediction pathway (Omega/symmetry → CV) suffers from post-hoc symmetry assignment.

**CRR's status is best described as: a promising descriptive framework seeking its first genuine prospective predictive success.** The cardiac RR interval validation comes closest, but needs to be replicated with pre-committed single predictions across many more systems.

The framework would benefit enormously from a single, clean, pre-registered prediction that succeeds -- or from an honest published failure that sharpens the theory. Both outcomes would be more valuable than additional post-hoc "confirmations."
