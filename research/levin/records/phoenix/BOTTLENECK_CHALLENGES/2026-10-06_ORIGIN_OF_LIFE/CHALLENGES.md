# Origin of life — bottleneck challenges, comparison and grading (2026-10-06)

Frozen sources: `sweeps/origin_of_life_2026.json` (24 papers, 19 from 2026, each with the authors' own unresolved-bottleneck sentence quoted verbatim; 6 fetch failures and a list of excluded items recorded). Frozen core: `CORE/MATHEMATICS.md` through `crr_instrument.py`. Computations: `ool_challenges.py`, output `ool_challenges_output.json`. Grades: NO CONTACT / REPHRASE / REDUCES / CANDIDATE, with WRONG where the core's object gives the wrong answer. No rung; nothing enters the ledger.

## Part A — Computed challenges

### O1 — Assembly theory (Siebert, Chowdhury, Slocombe & Walker, arXiv:2606.15499 v1; Rutter … Cronin, PNAS 2026; critiques Flamm, Merkle & Stadler arXiv:2505.22826; Masierak arXiv:2604.16302; Bieniawski arXiv:2608.19228)

**Bottlenecks named.** "It is an open question whether or not the threshold will be universal across all substrates" (Siebert et al.); the index is NP-complete to compute (Masierak) and "a single cyclization can either decrease, increase, or leave the assembly index unchanged" (Flamm et al.).
**CRR reading.** The assembly index is a minimal construction path, the core's chord in construction space; an actual synthesis history is an arc; the surplus is the detour; copy number is repeated regeneration.
**Run.** Binary-string assembly, exact index by search (indices 3, 5, 5, 3 for the four targets), 300 runs each of a random-joining chemistry and a crude templated (copying) chemistry.

| target | chemistry | copies when made | arc per copy | surplus per copy |
|---|---|---|---|---|
| 0110 (index 3) | random / templated | 1.4 / 24.6 | 16.2 / 4.2 | 13.2 / 1.2 |
| 01101001 (index 5) | random / templated | 1.1 / 15.1 | 29.8 / 7.4 | 24.8 / 2.4 |
| 00001111 (index 5) | random / templated | 1.7 / 26.0 | 25.4 / 5.7 | 20.4 / 0.7 |
| 01010101 (index 3) | random / templated | 1.4 / 27.3 | 24.7 / 4.5 | 21.7 / 1.5 |

**Outcome: REPHRASE.** Selection appears as copy number rising while surplus per copy falls toward zero; the two are the same signal, and assembly theory already carries it as copy number. The core supplies no universal threshold (its own R5 says there is none for the regeneration weight), so it cannot answer the universality question, and it says nothing about the cyclisation pathology or the complexity results. One honest contact: the critiques' point that the index depends on the chosen operations is the core's "the carrier must be declared" caveat in another field.

### O2 — RAF emergence (Golnik, Gatter, Hordijk, Stadler & Vassena, arXiv:2605.25523 v1 and arXiv:2609.23602 v1; Kempes, Avila & Mathis, Phil Trans B 2025; Mrnjavac … Martin, Sci Adv 2026)

**Bottlenecks named.** "The identification of RAFs through stoichiometric autocatalysis remains delicate"; the characterisation of autocatalytic cores in RAF language "remains an open research project"; the space of molecules that could catalyse the same reactions "is likely to be effectively innumerable" (Kempes); "Empirical studies addressing early metabolic evolution are lacking" (Mrnjavac).
**Run.** Binary polymer model to length 5 (62 molecules, ligation only), Hordijk–Steel RAF algorithm, 20 random catalysis assignments per catalysis probability.

| catalysis probability p | 0.0005 | 0.001 | 0.002 | 0.004 | 0.008 | 0.016 |
|---|---|---|---|---|---|---|
| P(RAF exists) | 0.15 | 0.30 | 0.45 | 0.75 | 0.95 | 1.00 |

**Outcome: NO CONTACT.** Emergence is a percolation-type threshold in parameter space, as RAF theory predicts; it is not a first passage of accumulated statistical change and the half-circumference criterion has no meaning here. The core's "regeneration from the settled past" is the RAF closure condition, named by that literature twenty years earlier. None of the four stated bottlenecks (structural correspondences, catalytic-space enumeration, empirical grounding) is touched by any core object.

### O3 — Error threshold and replicator ecology (Kovács, Barabás, Meszéna, Szathmáry & Szilágyi, PLoS Comput Biol 2026; Carr, Biosystems 2026; Solé & De Domenico arXiv:2504.08492)

**Bottlenecks named.** "how the parabolic nature of replication dynamics can increase the amount of sustainable genetic information" (Kovács et al.); "How meaningful, heritable structure first emerged … remains a central open question" (Carr, who finds a fidelity threshold near 0.7 for compositional heredity).
**Run.** Eigen quasispecies, length 50, master fitness 10: threshold μ = 0.046; master fraction 0.24 below it, 0.02 just below, zero above.
**Outcome: NO CONTACT.** The survival condition involves fitness, length and error rate only. The one CRR-adjacent reading, heredity as "regeneration with fidelity 1 − μ", is a rephrase; Carr's fidelity threshold for compositional heredity is a finding about a specific kernel that the core, which fixes no kernel, could not have produced.

### O4 — M7, forms as productions of history, against the 2026 hysteresis and pre-replication papers (Iván, Szilágyi & Szathmáry, PNAS 2026; Pigozzi & Levin, arXiv:2607.28250 v2; Solé & De Domenico 2025; Kaçar … Koonin & Lynch arXiv:2605.05464 v3)

**Bottlenecks named.** Autocatalytic networks lacked "stable, selectable variation rather than mere short-term adjustment" (Iván et al., who supply it through bistable attractors plus stochastic partitioning, i.e. hysteresis); "Whether organized causal structure can arise before replication and influence its emergence remains unclear" (Pigozzi & Levin, who find the first 25 % of a GARD history predicts the rest); which transitions were lawful and which "a path-dependent contingent event" (Solé & De Domenico); the lack of population-genetic reasoning (Kaçar et al.).
**Run.** Two mutually inhibiting autocatalysts, each bistable (fixed points 0 and about 2.6, threshold about 0.38); random sub-threshold feed histories in the first 4.5 time units; chemistry relaxes; observed state read at t = 12; a common feed at t = 15 forces the choice of form; form read at t = 60. With and without a slow hidden variable that integrates the feed history. In-sample logistic accuracy for predicting the form (400 runs each):

| predictor | no hidden variable | with slow hidden variable |
|---|---|---|
| history only (net feed, first pulse) | 0.65 | 0.85 |
| observed terminal state (A, B) | 0.70 | 0.86 |
| observed state + history (net feed, path length) | 0.71 | 0.92 |
| full state including the hidden variable | — | 0.97 |

**Outcome: REDUCES, and it is informative about M7.** Without hidden state, history chooses the basin and then adds nothing once the state is known; the form is "a production of history" exactly as any attractor reached by a path is. With a slow hidden variable, history predicts beyond the *observed* state but not beyond the *full* state. That is what Iván et al. demonstrate in a real chemical model (bistability plus hysteresis as the origin of heritable variation) and what Pigozzi and Levin measure in GARD (early history predicts later replication because it set organisation the composition does not show). M7's defensible content is therefore: **the forms that persist are attractors selected by history, and the part of history that still matters later is carried by slow state.** That is multistability plus hidden variables, the standard account, and the 2026 papers already say it with data. Anything stronger in M7 (forms as productions of history *rather than* attractors of law) is not reached by this test or by theirs.

## Part B — Graded by reading

| Paper (sweep id) | Bottleneck (short) | Grade | Reason |
|---|---|---|---|
| OOL-10 Segal, "Dissipation-Driven Selection of Evolving Replicators", arXiv:2603.15230 | derived only for unlimited fuel, well-mixed histories | REDUCES | compares whole histories by integrated entropy production (England's bound); the core's R6 is the thermodynamic-length form of the same object and inherits the same idealisation; the bottleneck run's C1 showed R6 is unusable on raw stochastic trajectories |
| OOL-11 Endres, "The unreasonable likelihood of being", arXiv:2507.18545 v2 | protocell within the habitable window; efficiency factor unknown | REPHRASE | persistence time and information-rate bounds; the core's first passage is the same kind of object with no additional constraint |
| OOL-12 Tutolo, PNAS 2026 (vent pH gradients) | the assumed proton gradient may not have existed | NO CONTACT | geochemistry |
| OOL-13 Azar, Theory Biosci 2026 (DKS lineage) | the transition "lacks a precise temporal threshold" | consistent, REPHRASE | the core's reading (becoming before life; life as a change of regeneration kernel, not a new category) agrees that there is no sharp event; but agreement with a continuum view is not a prediction |
| OOL-14 Carr 2026 (semantic information under compositional heredity) | fidelity threshold ~0.7 | NO CONTACT | a kernel-specific result the core cannot produce |
| OOL-15 Kovács et al. 2026 (sub-exponential replicators) | diversity limits vs sustainable information | NO CONTACT | replicator ecology |
| OOL-16 Peng … Baum, J Mol Evol 2026 | source of genetic diversity and long polymers | NO CONTACT | multilevel selection with persistence after N generations; "persistence" is the core's regeneration in words only |
| OOL-18 Kaçar … Koonin & Lynch 2026 | no population-genetic reasoning in origin scenarios | NO CONTACT | the core has no population, drift or selection coefficient |
| OOL-19 Pigozzi & Levin 2026 (causal organisation before replication in GARD) | can causal structure precede and predict replication | REPHRASE, with one convergence | "the first 25 % of history predicts the remaining 75 %" is a history-predicts-form result of the O4 type; their measure (causal emergence) is not a core quantity; convergence on the *question* (history before heredity), not on the object |
| OOL-20 Deng, Lancet & Yaniv, Life 2026 (composome to replicase) | no pathway from compositional to sequence heredity | REPHRASE | the core describes it as a change of regeneration kernel (composition to sequence); the pathway itself is chemistry the core does not supply |
| OOL-21 Iván, Szilágyi & Szathmáry, PNAS 2026 (bistability, hysteresis, heritable variation) | stable selectable variation in autocatalytic networks | REDUCES (and O4 reproduces its logic) | hysteresis in compartmentalised bistable chemistry is the formal content of "settled history conditions what follows"; they have the chemistry and the division mechanism, the core has the sentence |
| OOL-22 Koonin, arXiv:2608.22348 (multilevel selection, reproducers first) | energy source; takeover requires random distribution at division | NO CONTACT | population models |
| OOL-23 Barge et al., PNAS 2026 (biosignatures, convergence) | "it is unknown to what extent life on other planets would converge on the same solutions" | the M7 question in the field's words; NO CONTACT as mathematics | the lawful/contingent split is exactly P23's; the core supplies no discriminator |
| OOL-24 Kipping, arXiv:2605.02969 (agnostic searches) | "we don't know what we don't know" | NO CONTACT | Bayesian survey design |
| OOL-17 Solé & De Domenico 2025 (bifurcations) | which transitions were lawful vs contingent | REPHRASE | transitions as bifurcations and percolation; the core's cut is not a bifurcation |
| OOL-03 Mrnjavac … Martin 2026; OOL-04 Kempes et al. 2025 | empirical grounding of metabolic closure; encapsulation thresholds | NO CONTACT | |
| OOL-06, 07, 08, 09 (assembly theory measurement, complexity, critiques) | instrument limits; NP-hardness; cyclisation pathology; approximators | NO CONTACT beyond O1 | |

## Part C — Comparison with the standing theories, in CRR's terms

| Theory | Its unit of "origin" | Its history structure | CRR against it (from Parts A–B) |
|---|---|---|---|
| Autocatalytic sets (RAF) | closure of a reaction set over a food source | structural, no dynamics; emergence as threshold | CRR's regeneration *is* closure, said later and less precisely; the cut is not the RAF threshold. REDUCES |
| Assembly theory | objects with high minimal-construction depth made many times | the index is a geodesic; copy number is repetition | CRR's chord and regeneration; surplus is redundant with copy number. REPHRASE |
| Dynamic kinetic stability | persistence through replication; no sharp threshold | continuum | CRR agrees on the continuum (becoming before life) and adds no criterion. REPHRASE |
| Dissipative adaptation / thermodynamics of replication | histories weighted by integrated dissipation | whole-trajectory comparison | CRR's R6 is the slow-driving relative; unusable on raw stochastic histories. REDUCES |
| RNA world / error threshold | first accurate template copying | fidelity threshold | no CRR object enters. NO CONTACT |
| Compositional inheritance (GARD, lipid world) | composomes re-formed on division | attractors in composition space; hysteresis (Iván et al.) | the formal content of CRR's "settled history conditions what follows", with chemistry attached. REDUCES |
| Chemical ecosystem selection / natural induction | persistence and organisation before genes | multilevel persistence; learning-like consolidation | the nearest kin of M7; Pigozzi & Levin's "history before heredity" is the question CRR asks, answered with a non-CRR measure. REPHRASE |
| Historical contingency vs lawfulness (astrobiology framing) | which features are universal | the lawful/contingent split | M7's question in the field's words; CRR supplies no discriminator (O4: history-dependence reduces to attractor choice plus hidden state). NO CONTACT as mathematics, same question as metaphysics |

## Tally (by paper)

| Outcome | Count |
|---|---|
| NO CONTACT | 14 |
| REPHRASE | 6 |
| REDUCES | 4 |
| CANDIDATE | 0 |
| WRONG | 0 (no core object was applicable enough to be wrong) |

## Convergence worth highlighting (R10, fetched)

- **Iván, Szilágyi & Szathmáry (PNAS, 21 Sep 2026):** heritable, selectable variation in compartmentalised autocatalytic networks arises from bistable attractors plus stochastic partitioning, with explicit memory of past states and environmentally triggered switching. This is the chemistry of "settled history conditions what follows" (M4) and of "forms as productions of history" (M7) in the only sense O4 found defensible. Same mechanism, independent, with data.
- **Pigozzi & Levin (arXiv:2607.28250 v2, 2 Oct 2026):** organised causal structure precedes compositional self-replication in GARD and the early quarter of a history predicts the rest. Same question as M7 (history before heredity), different measure.
- **Azar (Theory Biosci, 2026):** no precise temporal threshold marks the emergence of life. Same direction as CRR's "becoming before life".
- **Solé & De Domenico (2025):** the choice among alternatives at a transition "is a path-dependent contingent event". Same direction as M7's contingency clause.
- **Segal (arXiv:2603.15230, 2026):** whole histories compared by integrated dissipation. Same object class as R6.
