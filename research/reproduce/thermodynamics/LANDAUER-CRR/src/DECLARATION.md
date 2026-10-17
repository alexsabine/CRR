# LANDAUER-CRR (2026-10-17): the owner's Landauer hypothesis for the cut, beside Landauer, Sivak–Crooks and Fields et al.

**Status.** Declared-synthetic checks (R4) on a two-state model. Written, with its script, before the script was first run: this file's commit precedes `outputs/`, and the git timestamps are the record. The protocols in P3 are drawn from a seed fixed here and were never generated before the freeze. No real data are used, so no PASS is possible; nothing here is evidence for CRR or for any ontology. Layer: formal comparison and prior art (P-G4). The owner's instruction is in `notebook/PROMPT_LOG.md`, entry of 2026-10-17.

**Owner's hypothesis (H-owner), as stated.** "Every choice is 1 bit at the Dirac delta": each cut settles one bit, and that bit leaves as heat of at least k_B T ln 2 (Landauer), the past being "consecrated" as information released into the world.

**Prior art, stated before the run.** Szilard (1929, *Z. Phys.* 53: 840–856) priced one bit of measurement at k_B T ln 2. Landauer (1961, *IBM J. Res. Dev.* 5: 183–191) located the cost at logically irreversible erasure; Bennett (2003, *Stud. Hist. Phil. Mod. Phys.* 34: 501–510) reviews why writing to blank memory need not cost it. Bérut et al. (2012, *Nature* 483: 187–189) measured it. Finite-time corrections: Salamon & Berry (1983, *PRL* 51: 1127), Crooks (2007, *PRL* 99: 100602), Sivak & Crooks (2012, *PRL* 108: 190602), Proesmans, Ehrich & Bechhoefer (2020, *PRL* 125: 100602). Fields, Friston, Glazebrook & Levin (2022, *Prog. Biophys. Mol. Biol.* 173: 36–59; arXiv:2112.15242, December 2021), §2.1: the energy "to receive and irreversibly record one bit, is given by Landauer's Principle as ln 2 k_B T", paid on each cycle (β ≥ ln 2). CRR's form dates from April 2025. The per-bit statement is 65 years older than either framework and belongs to neither.

**Ordinary model that would give every result here with no CRR ontology.** Stochastic thermodynamics of a driven two-state system: Landauer's bound plus the Sivak–Crooks friction metric. Every number below is computed by it. CRR enters only through two identities: its coherence C is the Fisher arc length of the control path, and its cut on the binary carrier is a full half-turn (a flip from one certain state to the other).

## Model

One bit, states {0, 1}, energies {0, ε}, bath at temperature T, units k_B T = 1, τ_R = 1. p = probability of state 1. Work W = ∫ p dε; heat to the bath Q = W − ΔU. CRR carrier: the equilibrium family p_eq(ε) = 1/(1 + e^ε), Fisher metric g = p(1 − p); the Fisher arc length from ε = 0 is G(ε) = arctan(sinh(ε/2)), so a path's coherence is Σ|ΔG| (σ = 1) and its chord is |G(end) − G(start)|. From certainty to certainty (ε = +E to −E) is 2G(E), which tends to π, the half-turn of the binary carrier: a CRR cut. From maximum uncertainty to certainty (ε = 0 to E) is G(E), which tends to π/2: a quarter-turn, no cut.

Two rate laws: **uniform relaxation** (Glauber; total rate 1, so the friction metric is exactly g·τ_R and CRR's C is the thermodynamic length) and **Arrhenius** (k₀₁ = ½e^{−ε/2}, k₁₀ = ½e^{ε/2}; τ_R varies with ε, so it is not). E = 8 throughout. Master equation integrated by RK4 with dt ≤ 0.005 τ_R (at least 20 000 steps). Paths move at constant Fisher speed unless stated. Seeds: 20261017 (P3), 20261018 (P4a).

## Checks and predictions (fixed here)

**P1. The floor (Landauer; Fields et al.'s per-bit statement).** Erase a fair bit: ε from 0 to E at constant Fisher speed over τ, then rates off and ε reset to 0. Bound = ln 2 − H(p_end) (nats; H the binary entropy). *Prediction:* W ≥ bound at every τ ∈ {5, 10, 20, 50, 100, 200, 500, 1000} (difference > −10⁻⁹); (W − bound)·τ/τ_R within 5 % of C² for τ ≥ 200, with C = G(8) = 1.5342.
**P1b. "One bit per choice".** Erase a biased bit, p₀ ∈ {0.5, 0.25, 0.1, 0.01}, at τ = 1000. *Prediction:* 0 < W − [H(p₀) − H(p_end)] < 0.01. The cost of settling a choice is the uncertainty it removes; it is ln 2 only when the choice was 50/50.
**P2. Finite-time slope.** Same erasure drive without the reset, τ ∈ {50, 100, 200, 500, 1000}. *Prediction:* W_ex·τ/τ_R within 5 % of C² for τ ≥ 100, with the error falling as τ rises. A drive linear in ε costs more: W_ex·τ → E(½ − p_eq(E)) = 3.997, a ratio of 1.70 ± 0.09 to the constant-Fisher-speed drive at τ = 500.
**P2b. Must-fail (where CRR's C stops being the right length).** The constant-Fisher-speed drive under Arrhenius rates, τ = 500. *Prediction:* W_ex·τ/C² differs from 1 by more than 20 %, while the friction-metric prediction τ_R(ε)-weighted (Sivak–Crooks) is within 5 %.
**P3. Surplus prices the excess (held-out protocols).** 200 protocols from seed 20261017: 2–7 waypoints uniform in [0, E] between ε = 0 and E, constant Fisher speed, τ = 200, uniform relaxation. All share endpoints, so all erase the same information. *Predictions:* max |W_ex·τ/C² − 1| < 5 %; least-squares slope of W_ex·τ on C² through the origin in [0.97, 1.03]; R² > 0.995; the extra cost over the geodesic, (W_ex − W_ex,geo)·τ, against C² − C*² = S(S + 2C*), slope in [0.95, 1.05]. A per-bit count (Fields et al.'s per-cycle accounting, or the floor alone) gives every protocol the same cost and explains none of the variation (R² = 0 by construction). That is a DISTINCTION, not a contradiction: Fields et al. state a floor and do not claim the excess is zero.
**P4a. Must-fail for H-owner, literal form: cuts without heat.** Equilibrium hopping at fixed ε = 1 for 2 × 10⁵ τ_R (Gillespie). Each switch is a cut on the binary carrier. *Prediction:* about 2p(1 − p)·T ≈ 78 650 cuts (±2 %); mean heat to the bath per cut |m| < 0.01, so "each cut releases ≥ ln 2" fails by more than 100 standard errors.
**P4b. Must-fail for H-owner, driven form: a full half-turn of a known bit.** ε from +E to −E at constant Fisher speed (C = 2G(8) = 3.068, 0.977 of π), τ ∈ {50, …, 1000}. *Prediction:* Q·τ within 5 % of C² for τ ≥ 200, and Q(τ = 1000) < 0.02 ≪ ln 2. A completed occasion that removes no uncertainty costs no Landauer bit; its only cost is the path term.

## Grades fixed in advance

- P1, P1b hold → REDUNDANT-DOMAIN (Landauer 1961; Fields et al. 2022 restate it). Fail → error in the model or code, not a CRR result.
- P2, P3 hold → REDUNDANT-IG and REDUNDANT-DOMAIN: CRR's coherence is the thermodynamic length (Salamon & Berry; Crooks), and its surplus prices the Sivak–Crooks excess. Credit to them, not to CRR.
- P2b holds → WRONG for C as a universal cost length: C prices heat only when relaxation is uniform; the friction length is the general object.
- P4a, P4b hold → H-owner **WRONG in its literal form**. The amended reading, credited to Landauer and Sivak–Crooks: a cut settles the uncertainty it removes, which sets the heat floor (zero for a choice already certain, ln 2 at most for a binary one), and the walk's coherence sets the excess, k_B T·C²·τ_R/τ.
- CRR-specific ADDS: none is claimed. The cut rule decides which drive counts as a completed occasion; this study tests whether that occasion carries the Landauer bit, and it is predicted not to.

## Deviations

Any change to the script after the first run is a new study ID, or is logged here as a deviation with its reason before the result is read.
