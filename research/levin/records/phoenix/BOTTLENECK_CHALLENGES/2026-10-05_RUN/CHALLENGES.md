# Bottleneck challenges against 2026 papers — run of 2026-10-05/06

Format: `BOTTLENECK_CHALLENGES/CHALLENGE_TEMPLATE.md`, condensed. Frozen paper versions are those in `sweeps/*.json` (43 items, every one fetched, each with the paper's own bottleneck sentence quoted verbatim). Frozen CRR ingredients: `CORE/MATHEMATICS.md` as released, implemented only through `crr_instrument.py` (self-tested against the core's numbers; causality rule enforced). Role: prior-art auditor plus experimentalist (software). Outcomes use the Egg's vocabulary: NO CONTACT / REPHRASE / REDUCES / CANDIDATE; WRONG is added where the core's object, applied as the paper would need, gives the wrong answer. No PASS of any kind; nothing here enters the ledger.

Computed challenges (eight) are written out; the remaining thirty-five are graded by reading in the table at the end. Numbers come from `physics_challenges_output.json` and `bio_cog_challenges_output.json`.

---

## C1 — Fritz & Seifert, arXiv:2603.05170 v2 (PRE 114, 034109): entropy production from region-crossing waiting times in continuous space

**Exact unresolved statement.** "Estimating entropy production in continuous systems that can only be observed with a limited resolution remains an open problem in stochastic thermodynamics."
**What the domain already provides.** Waiting-time estimators needing Markovian events; TUR bounds; coarse-grained affinity estimators.
**Candidate missing object (the Egg's own example).** Path information between coarse crossings: arc `C`, chord `C*`, surplus `S` of the trajectory, fed into R6 as a dissipation bound.
**Derivation and run.** Brownian vortex (harmonic trap, rotational force ε = 1, D = 1; true EP rate 2ε² = 2). Four angular sectors; events = sector crossings (which are exactly the core's R2 first-passage clock). Per segment, Euclidean path length `L` (the Gaussian-mean carrier makes Fisher arc Euclidean) and R6's implied rate Σ L²/T.

| dt | crossings | coarse-grained affinity EP (standard lower bound) | mean surplus per segment | R6-implied rate | ratio to true |
|---|---|---|---|---|---|
| 0.1 | 1014 | 0.39 | 1.24 | 36.7 | 18× |
| 0.01 | 3544 | 0.09 | 1.56 | 324 | 162× |
| 0.001 | 11228 | 0.04 | 1.81 | 3162 | 1581× |

**No-CRR reduction.** Any smoothed carrier reduces to the current-based or TUR estimators the paper compares.
**Outcome: NO CONTACT, and WRONG if R6 is read as an EP bound on raw data.** The path length of a Brownian trajectory diverges as dt → 0, so the "bound" grows without limit while the true EP is fixed. The core states this itself (white-noise paths have infinite Fisher variation; R6 assumes η = 0 or an OU drive). The crossing clock is REPHRASE.

## C2 — Keidar et al., arXiv:2607.16474 v1 (review) and Biswas, Majumdar & Pal, arXiv:2603.25338 v3: resetting beyond renewal; resets coupled to intrinsic dynamics

**Exact unresolved statements.** "…partial resetting, many-body resetting, and environmental memory, break renewal in different ways. For these, existing results remain mostly case-specific, and no comparable unifying framework has yet replaced the role played by renewal theory." / "In most existing studies, however, resetting events are governed by an external timer and remain decoupled from the system's intrinsic dynamics."
**Candidate missing object.** The core's regeneration R5: reset to a past-only weighted mean seed `m_n = q m_{n−1} + (1−q) Φ_n`, with events either on an external Poisson clock or at first passage of accumulated arc (R2).
**Run.** 1-D diffusion from x₀ = 1 to the origin, D = 1, reset rate r = 1. Mean first-passage time:

| protocol | MFPT |
|---|---|
| full reset to x₀, renewal closed form (Evans–Majumdar) | 1.72 |
| full reset, simulated (q = 1) | 1.83 |
| memory seed q = 0.9 / 0.5 / 0.0, external clock | 2.26 / 9.54 / 12.2 |
| memory seed q = 0.9, intrinsic arc clock a = 0.5 / 1 / 2 | 90.9 / 69.3 / 43.8 |

**No-CRR reduction.** Resetting with memory of past positions is an existing model class (the review's "environmental memory"); threshold resetting is Biswas et al.'s own construction.
**Outcome: REPHRASE / REDUCES.** The core supplies a one-parameter family with no closure for `q` (the core says so) and explicitly declines to supply the reset's energy budget, which is the ingredient the review calls missing. The intrinsic arc clock on a Brownian carrier is resolution-dependent (same defect as C1) and pins the walker, so it is not a usable alternative to the external timer.

## C3 — Matsuki, Kobayashi & Kori, arXiv:2606.25892 v2 and Osmers & Kolossa, arXiv:2601.13962 v2: defining phase and cycle boundaries from data, isochron-free and causal

**Exact unresolved statements.** "…reconstructing isochrons from observed trajectories is often challenging for complex models and real-world systems." / "Despite its widespread empirical use, the systematic endpoint distortions of ecHT have lacked a principled, closed-form analysis."
**Candidate missing object.** The R2 cut: first passage of half the Fisher circumference of accumulated arc, causal by construction and isochron-free.
**Run.** Van der Pol μ = 2 with state noise 0.05; ground truth = isochron (asymptotic-phase) events computed by batched forward integration; rivals = polar protophase (the paper's), Hilbert phase (non-causal). Statistic: circular SD of each method's event lag behind the preceding isochron event, in periods.

| method | events | circular SD of lag | interval CV |
|---|---|---|---|
| isochron (truth) | 39 | — | 0.040 |
| polar protophase | 40 | **0.005** | 0.041 |
| Hilbert (non-causal) | 40 | 0.013 | 0.038 |
| CRR arc first passage, deterministic circumference | 40 | 0.178 (steady drift: noise path inflates the arc) | 0.039 |
| CRR arc first passage, circumference calibrated on the first half | 18 (test half) | 0.376 | — |

**Outcome: REDUCES in the deterministic limit; WRONG as a cycle-boundary detector on noisy data.** The arc clock accumulates noise path length, so its boundaries random-walk away from the isochron events; calibration removes the mean drift but not the random walk. The polar protophase, which the paper already uses, is thirty times tighter and equally causal and isochron-free.

## C4 — Domínguez, Chubb & Woods, arXiv:2609.31832 v1 and Miller & Erker, arXiv:2603.04556 v2: ticking clocks

**Exact unresolved statements.** "Determining a clock's precision usually requires comparison with a better time reference, yet no ideal reference is physically attainable." / "…a theoretical description that unifies these perspectives and incorporates feedback into autonomous quantum clocks has been lacking."
**Run.** The core's R4 rotor with OU drive as a tick generator: 222 ticks, precision (mean²/variance of intervals) 5.97, lag-1 interval autocorrelation −0.65 (non-renewal).
**Outcome: REPHRASE.** The core's counting process is a tick sequence described by exactly the renewal or non-renewal statistics the papers use; it has no self-referential precision estimator and no feedback map.

## C5 — Auconi & Ito, arXiv:2605.03757 v1: information-geometric constraints during relaxation

**Exact unresolved statement.** "how they are constrained by detailed balance during relaxation remains unclear."
**Run.** Three-state relaxation with and without detailed balance: temporal Fisher information at t = 0 is 31.9 vs 49.9; total Fisher–Rao arc 1.27 vs 1.42; arc equals ∫√(temporal FI) dt by definition.
**Outcome: REDUNDANT-IG / REDUCES.** The paper's coordinate is the time derivative of the core's coherence. The core supplies neither the detailed-balance constraint nor the high-dimensional tightening the paper names.

## B1 — Raz … Alon, Nature Aging 6:1330 (2026), PMID 42265466: damage accumulation with saturating removal; death as first passage

**Exact unresolved statement.** "It is not clear how these similarities and differences arise from the accumulation of damage that underlies aging."
**Candidate missing object.** The core's history variable `C` (accumulated arc of the damage trajectory) as a predictor of death beyond the current damage state.
**Run.** SR-class model, 40 000 individuals, checkpoint at age 12, death within the next 4 units. State X predicts death: AUC 0.90 (must-pass). Within a narrow X band (n = 659), accumulated arc predicts death: AUC 0.42 (no positive effect).
**Outcome: NO CONTACT.** The model is Markov; the paper's death event is already a first passage of a level by a non-circular variable; the open regime question concerns the drift law, not path geometry.

## B3 — Nguyen, Etzel, Bezdek & Zacks, eLife 14:RP107955 (2026): event boundaries beyond error and uncertainty triggers

**Exact unresolved statement.** "…approximately 16% of the explainable variance remains unaccounted for."
**Candidate missing object.** A third trigger type: a boundary when accumulated change since the last boundary exceeds a threshold, which can fire under slow drift that never produces an error spike.
**Run.** Feature stream with six abrupt jumps and six slow drifts of equal total displacement, observation noise 0.3; EMA event model.

| trigger | events | jumps hit (of 6) | drift-ends hit (of 6) | false alarms |
|---|---|---|---|---|
| error peak (the paper's class) | 10 | 6 | 1 | 3 |
| accumulated **arc** since last boundary (core) | 44 | 6 | 6 | 29 |
| displacement since last boundary (standard CUSUM-type rival) | 14 | 4 | 5 | 4 |

**Outcome: REDUCES, with the core's specific object WRONG for the purpose.** A cumulative-change trigger is a live candidate for the residual variance, and the paper's data are public (OpenNeuro ds005551). But accumulated arc is dominated by noise path length (7.8 units per quiet segment against a 1.2 threshold) and fires continuously; the displacement trigger catches the same boundaries with few false alarms. What survives is the standard rival. The core contributed the question, not the detector.

## B4 — Blattner, bioRxiv 10.64898/2026.04.01.715890 v1: excess-cost functional and endpoint displacement as hidden regenerative state

**Exact unresolved statement.** "These quantitative layers are intended as proof-of-concept calibratability and mechanistic-grounding checks rather than full validation of the complete open-path model."
**Run.** Regression of an outcome on (path cost, displacement) versus (path cost, displacement, excess): identical residual sum of squares, design rank 3 in both cases.
**Outcome: REPHRASE with one transferable constraint.** The paper's objects are the core's surplus and chord, independently arrived at. The core's identifiability result transfers as a caution for their model: excess cost carries no information beyond the pair.

---

## Graded by reading (no computable contact with the frozen core)

| Paper (sweep id) | Bottleneck (short) | Outcome | Reason |
|---|---|---|---|
| 2511.00974 Mohite & Rieger | finite-time optimal control framework missing | REDUCES | R6 is the slow-driving thermodynamic-length bound the paper says is insufficient |
| 2510.21670 Brémont | non-Poisson shot-noise first passage | NO CONTACT | different first-passage object (level crossing of a jump process) |
| 2609.08219 Kobayashi & Dechant | which information parameters acquire, on what timescales | NO CONTACT | their Fisher information is parameter–latent mutual information, not the path metric |
| 2601.12475 Melo et al. | trajectory-level quantum FI | REPHRASE (QUANTUM_CRR SPARK) | conditional-QFI path length under another name; no coherent/incoherent split in the core |
| 2606.06759 Carrasco & Spehner | Bures geodesics for non-faithful states | NO CONTACT | the core needs the geodesic to exist; says nothing about rank deficiency |
| 2607.23573 Maleki | QSL and sensor scaling | NO CONTACT | — |
| 2512.24775 Gebrezabher; 2609.16449 Rajabi et al. | phase reduction beyond weak coupling; amplitude | NO CONTACT | the core has one phase coordinate and no amplitude; the bottleneck is the amplitude |
| 2604.21805; 2608.16732 Stoica | clock ambiguity; preferred time | NO CONTACT (maths); M3 as stance | M3 is the relational stance these papers show insufficient without a clock–world split; the core does not supply the split |
| 2604.00092 Hosseini & Lock | time of arrival | REPHRASE | arrival is a first-passage event; the core is classical and gives no observable or POVM |
| 2603.08845 Baumann & Lock | events across temporal frames | NO CONTACT | — |
| PMID 41928495 Lim et al.; PMC12694990 Weed et al.; 2605.00910 Xu et al. | circadian phase: initial-condition forgetting time; confident wrong convergence; latency | NO CONTACT | convergence time is set by amplitude relaxation and forcing; the core has no formula for it and no latency advantage |
| 2603.08866 Gunawardena & He | robust phase–amplitude coupling | NO CONTACT | — |
| PMID 42671587 Cortés-Poza | slow tissue-memory variable; open mathematical questions | REPHRASE | the slow memory variable is a seed-like state; the core does not answer the open questions |
| PMID 42556770 McMillen & Levin; 2609.29755 Hartl et al. | bioelectric code; regulatory handles | NO CONTACT | — |
| PMID 42627925 Huang et al.; PMID 42289846 Zomorodi et al.; PMID 41997872 Bova et al. | ramps as intrinsic time-since-event codes | REPHRASE | "time since the last cut" is the core's count/interval; no mechanism supplied |
| PMID 42619903 Goker et al. | circadian gating of an ultradian oscillator | NO CONTACT | — |
| PMID 41673193 Baror et al. | continuity vs segmentation, one system or two | NO CONTACT | — |
| niag018 Bellingrath | information length as width of the present, unlinked to chronometry | REDUNDANT-IG | `C` is information length; the link to judgments is the paper's open problem and the core has no bridge |
| PMID 41959097 Hummos et al. | online latent-context discovery | REPHRASE | transient-error change points; see B3 for why the core's arc trigger is not the answer |
| 2606.23279 Taye | internal time θ = ∫ f ds as biological proper time | REPHRASE | literally the clock of becoming; unvalidated, as the paper says of itself |
| PMID 42079282 An, Yang & Wang | forgetting depends on interference timing within a window | REPHRASE | history-dependence (weak M4) consistent; no mechanism |
| 2601.16979 Kalra et al. | curvature along the training path at LLM scale | NO CONTACT | — |
| 2609.35926 Aguilar et al. | trajectory-based forgetting mitigation ignoring Riemannian geometry | REDUCES | RWalk-type path importance; see the CL sweep of 2026-10-05 |
| 2606.01863 Khilar | stability–plasticity as a Stefan problem | NO CONTACT | — |

## Tally

| Outcome | Count |
|---|---|
| NO CONTACT | 24 |
| REPHRASE | 10 |
| REDUCES or REDUNDANT-IG | 8 |
| CANDIDATE | 0 |
| WRONG (core's object applied as the paper would need) | 3 (C1 as EP bound, C3 as boundary detector on noise, B3 arc trigger) |

Counts are by paper where several papers share a challenge. One transferable constraint found (B4 identifiability). One question worth a prospective test found (B3, cumulative-change trigger), but the detector that would answer it is the standard displacement rule, not the core's arc.
