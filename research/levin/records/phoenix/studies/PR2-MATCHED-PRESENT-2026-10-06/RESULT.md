# PR2 — Matched-Present, Different-History Form Production: development results (2026-10-06)

**Stage.** FLAME. Synthetic battery and ablation only; no empirical data opened; no PASS claimable. Files: `DECLARATION.md` (claim, hypotheses, rivals, thresholds), `PR1_CORRECTION.md`, `CAUSAL_DIAGRAM.md`, `PROTOCOL.md`, `PRIOR_ART.md`, `DOMAIN_SEARCH.md`, `pr1_static_check.py`, `battery.py`, `ablation.py`, `outputs/*.json`, `sweeps/*.json` (every quote fetched).

## 1. PR1 corrected

A static Zipf library whose probabilities never change reproduces PR1's α (1.07, 1.09 against the texts' 1.00–1.10) and its falling normalised entropy (0.80 → 0.67 against 0.80 → 0.68). PR1's statistic rejects a fixed *equiprobable* library and nothing else. PR1-A is re-graded **NOT DECIDABLE** on that instrument; the Simon reading was one of several equivalent readings and should not have been named as the reduction. The Pólya "learning library" is, by de Finetti exchangeability (fetched), a mixture of fixed-probability sources: on a single history, "learned access probabilities" and "fixed unknown probabilities" are one hypothesis. Details and two further text statistics (61 of the top 100 types shared by all five books; within-text dispersion 1.57) in `PR1_CORRECTION.md`.

## 2. Synthetic identifiability battery (`battery.py`, `outputs/battery.json`; 12 trials per cell; 1 500 steps per sequence; 16 replicates where replicates exist; effect b = 2; observation noise 0.1; 979 s)

Classification counts per true world (rows) and regime. "Correct" counts a declared abstention as correct where the regime cannot decide (A|C on one sequence; E|F without latent or intervention).

| regime | A static | B Simon | C Pólya | D HMM | E path | F omitted latent | S state-sufficient |
|---|---|---|---|---|---|---|---|
| obs1 (one sequence) | A\|C ND ×12 ✔ | B ×11, A\|C ND ×1 (0.92) | A\|C ND ×12 ✔ | D ×12 ✔ | **S ×12 ✘** | **S ×12 ✘** | S ×12 ✔ |
| obsR (16 replicates) | A ×12 ✔ | B ×12 ✔ | C ×12 ✔ | D ×12 ✔ | **S ×12 ✘** | E\|F ND ×9 ✔, S ×3 (0.75) | S ×12 ✔ |
| int (replicates + randomised-route pairs) | A ×12 ✔ | B ×12 ✔ | C ×12 ✔ | D ×12 ✔ | **E ×12 ✔** | F ×11 ✔, S ×1 (0.92) | S ×12 ✔ |
| lat (replicates + latent measured) | A ×12 ✔ | B ×12 ✔ | C ×12 ✔ | D ×12 ✔ | **S ×12 ✘** | F ×8 ✔, S ×4 (0.67) | S ×12 ✔ |

Mean test statistics at the default setting: order gain T1 = −0.29 (A), −0.31 (B), −0.07 (C), +0.22 (D); innovation ratio T2 = 0.35 (A), 0.95 (B), 0.02 (C); replicate Spearman T3 = 0.60 (A), −0.01 (C); path gain T4 = −0.004 (D), 0.004–0.006 (E), 0.012–0.015 (F), −0.003 (S); route gain T5 = 0.056 (E), −0.002 (F); latent-conditioned residual T6 = 0.000 (F).

**What the gate establishes.**
- Static heterogeneous probabilities no longer fool the instrument: World A is never called reinforcement or production (0 of 48 runs), and on a single sequence the scorer abstains between A and C instead of guessing, which de Finetti says is the only honest answer.
- The library worlds, the hidden-Markov world and the state-sufficient control are classified correctly in every regime that permits it (B: 47 of 48; A, C, D, S: 48 of 48).
- **The true path-dependent world is identified only under intervention** (12 of 12 with randomised routes and a common perturbation, route gain 0.056 against a threshold of 0.01). Observationally it is missed at this effect size in every run (path gain 0.004–0.006; the oracle with the true functional reaches only about 0.02, and the windowed path features recover a third of that). This is the finding the owner's point 6 anticipated, now measured: at realistic effect sizes, observational sequence data do not separate production-through-history from a state-sufficient world, and the intervention does.
- The omitted-latent world F is correctly separated from E under intervention (route gain −0.002: randomising the route kills the association) and when the latent is measured (residual 0.000), with power failures of 1 in 12 and 4 in 12 respectively; observationally it is correctly left as E|F NOT DECIDABLE in 9 of 12 and missed (called S) in 3.

**Sensitivity (6 trials per cell; fraction correct).**

| setting | A obsR | C obsR | D obsR | S obsR | E int | F int | E lat | F lat |
|---|---|---|---|---|---|---|---|---|
| default (n 1500, R 16, obs 0.1, b 2, E1) | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.92 | 0.0 | 0.67 |
| n = 300 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.0 | 0.17 |
| n = 600 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.5 | 0.0 | 0.5 |
| n = 4000 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.83 |
| observation noise 0.3 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.83 | 0.0 | 0.67 |
| observation noise 0.6 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.83 | 0.0 | 0.67 |
| effect b = 1 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.5 | 0.0 | 0.83 |
| effect b = 0.5 | 1.0 | 1.0 | 1.0 | 1.0 | 0.33 | 0.17 | 0.0 | 0.0 |
| effect b = 4 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.67 | 0.33 | 0.5 |
| R = 4 replicates | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.33 | 0.0 | 0.17 |
| R = 8 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.0 | 0.17 | 0.5 |
| E2 (hit-count functional) | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.67 | 0.0 | 1.0 |
| E2, b = 1 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.67 | 0.0 | 0.83 |

(The F columns under n = 4000 read 1.0 because at that length the observational path gain exceeds threshold reliably; the E-int column is 1.0 down to b = 1 and fails at b = 0.5, which sets the intervention's detectable effect size for this design: a route gain of about 0.01 nats per outcome.)

## 3. Failure cases, stated plainly
1. **Observational detection of true path dependence fails** at every effect size tried except b = 4 (one in three), with 16 replicates of 1 500 steps. The instrument's path features (multi-scale windowed arc, boundary-hit and position averages; whole-path length; net displacement) capture about a third of what the true functional carries. A flexible sequence model could do better, but the oracle bound (0.02 nats) says the information simply is not large on this carrier. Consequence: the protocol must be interventional; an observational PR2 would mostly return S or NOT DECIDABLE for a true E world.
2. **F is mistaken for S** when the observational path gain falls below threshold (3 of 12 at obsR; 4 of 12 at lat; most at R ≤ 8 or n ≤ 600). This is a power failure in the F direction: it says "present suffices" when an omitted latent exists. It is the conservative error, and it is still an error.
3. **On a single sequence the scorer calls E and F "S"** (24 of 24). A single history cannot carry the test; the battery says so by failing, and the protocol requires replicates and randomised routes.
4. **B on a single sequence** was once called A|C ND (innovation ratio below 0.7 by chance). Harmless, recorded.
5. **Scorer revisions before the full run** (header of `battery.py`): v1 branched on order gain for all worlds (E and F have nearly exchangeable form sequences given the state, so they fell into the library branch) and E's hidden functional was a saturating cumulative sum (no information after the first steps); v2 fixed both and removed a target leak (the EWMA and count features included the current form; found by ablating features in F); v3 made the randomised-route test primary when intervention is available, because the observational T4 gate otherwise blocked the intervention from ever being consulted. The thresholds were not changed. These are instrument-development incidents, which is what FLAME is for; they are listed so a reader can judge the gate's independence.

## 4. CRR ablation on the matched-present pairs (`ablation.py`, `outputs/ablation.json`)

Per unit: the observed state path to the matched present (x* = 0.5, tolerance 0.05, routes randomised), the common kick (+0.4), twenty future forms; target y = (count of form 2 − count of form 3)/20, the signature the hidden path variable acts on. Each predictor is fitted with one slope and one intercept on 300 training units and scored by held-out R² on 300 fresh units (same kick) and on 300 units with a different kick (0.2). "hidden" is the oracle (the true path variable); "route" is the binary design upper bound; "embed1" is one learned direction of the eleven windowed path features, fitted on the training half only.

| world | S = C − C* | C alone | C* alone | duration (= event count = elapsed time here) | native memory summary | embed1 (learned, 1 direction) | route | oracle hidden | unrestricted ceiling |
|---|---|---|---|---|---|---|---|---|---|
| E1 wear, held-out | 0.546 | 0.546 | −0.019 | 0.451 | **0.562** | **0.723** | 0.479 | 0.765 | 0.721 |
| E1, transfer kick 0.2 | 0.576 | 0.576 | 0.018 | 0.512 | 0.579 | 0.685 | 0.518 | 0.774 | 0.688 |
| E1, within detour route only | 0.387 | 0.389 | −0.014 | −0.092 | **0.482** | 0.487 | — | 0.608 | 0.487 |
| E2 hits, held-out | 0.797 | 0.797 | −0.008 | 0.806 | **0.815** | **0.875** | 0.763 | 0.990 | 0.875 |
| E2, transfer kick 0.2 | 0.819 | 0.819 | 0.007 | 0.836 | 0.835 | 0.901 | 0.780 | 0.994 | 0.901 |
| E2, within detour route only | −0.001 | −0.001 | −0.015 | 0.001 | −0.000 | −0.086 | — | −0.004 | −0.073 |
| F omitted latent | −0.008 | −0.008 | −0.005 | −0.008 | −0.011 | −0.034 | −0.005 | 0.963 | −0.030 |
| S state-sufficient | −0.001 | −0.001 | −0.032 | −0.001 | −0.001 | −0.045 | −0.004 | −0.000 | −0.041 |

Correlation between S and C on every test set: 1.000 (0.9996 within route). Readings:
- **S is C.** At matched endpoints the chord is the same for every unit, so the surplus is the arc minus a constant. S cannot beat C, and it does not, anywhere. This is structural, not a sample-size matter. The CRR-specific claim "S, not C, carries the history" is empty under a matched-endpoint design, which is exactly the design the question requires.
- **S never wins.** In the wear world the native memory summary (an exponentially weighted recent path length, the domain's own variable) is at least as good as S on all three sets, and the learned one-direction embedding is clearly better (0.72 against 0.55). In the hit-count world duration and the native summary edge S, and within the detour route nothing predicts because the hidden variable saturates there (a world property, reported).
- **The controls behave.** In F (omitted latent) randomising the route removes every path predictor's power while the oracle keeps 0.96: history was a proxy. In S nothing predicts anything. The instrument does not manufacture history effects.
- **Level 3 is not reached in any synthetic world, including the one built so that path length is the mechanism.** The honest form of the CRR bridge is therefore: "arc length of the state path is one admissible history summary among several, and at matched endpoints it coincides with the surplus"; which is a definition, not a prediction.

## 5. Levels

| level | definition | reached in the battery? | reached anywhere empirically? |
|---|---|---|---|
| 1 History effect | past trajectory predicts the future after naive current-state matching | yes (E1, E2, F under observation; F's is spurious) | yes, throughout the fetched literature (hysteresis, ageing, cryptic planaria, lag phases, batteries) |
| 2 Native-surplus history effect | survives matching on the native sufficient statistics and latent estimate, under randomised routes | yes in E1, E2 (by construction the native model lacks the slow functional); no in F, S | not established by PR2; in the fetched record the field's own hidden variable, when measured, absorbs the effect (hysteron configuration, Vmem, reporter level), with spin glasses and learning-to-criterion as the open cases |
| 3 CRR-specific path effect | predeclared CRR variable predicts the Level-2 residual, beats capacity-matched rivals, transfers, loses on ablation | **no**, in every world; S equals C by construction at matched endpoints and C loses to the native summary and to a one-direction learned embedding | no |

## 6. The Platonic-forms question, stated precisely

The question is not whether forms are real. It is: *can a system's repertoire of future forms be represented as a fixed latent library plus its current state, or does realised history construct constraints that stay causally relevant after the present has been matched?* The four readings and what this study says about each:

1. **Fixed forms with fixed propensities.** This is World A, and it reproduces PR1 exactly. For text, the shared top-100 overlap across five books says it is the dominant component. Nothing in PR1 or PR2 refutes it as a description of any empirical carrier examined.
2. **Fixed forms with learned access probabilities.** World C. By de Finetti this is observationally identical to (1) on a single history; it separates from (1) only with replicates from a common start (the battery does this correctly at R ≥ 4) or with intervention. It is not ontological production; it is Bayesian updating of a fixed library, and the battery labels it so.
3. **Forms whose accessibility changes with history.** Worlds D and E. D is a finite hidden memory, absorbed by the recent window. E is the live case: a slow path functional the current state does not carry. The battery detects E under intervention (route gain 0.06 at the default effect) and is power-limited observationally (path gain 0.004–0.006 against a threshold of 0.01, even with sixteen replicates of 1 500 steps and the true functional's oracle at 0.02). Whether any empirical carrier is E rather than D-with-a-measured-hidden-variable is the open question; the fetched record contains two candidates (spin glasses; learning to criterion) and many apparent cases that the native hidden variable explains.
4. **Genuinely novel forms or constraints generated through history.** No synthetic world here produces novel forms; World B produces novel *labels* at a constant rate, which a large static library also does for a long time (innovation ratio 0.35 for static Zipf against 0.95 for Simon over 1 500 steps, which the battery uses). Nothing in PR1 or PR2 bears on (4), and the Egg should not say it does.

(2) and (3) are not called ontological production here; the data do not require that interpretation of any carrier, and World E, which is production in the strong sense, is detectable only when the experimenter can randomise history.

## 7. Should the form be defined relationally?

The battery's own vocabulary already answers part of this. A "form" in World E is not an object in a library; it is a stable relation between the current state, a slow functional of the path, and the emission law. Of the six candidate modellings:

| modelling | where it fits | empirical statistic that would single it out |
|---|---|---|
| pre-existing latent attractors | A, D (with fixed emission laws) | replicate consistency high; route gain zero |
| learned attractors | C | replicate consistency low; route gain zero once counts are matched |
| metastable states | Kramers-type carriers (ORIGIN-OF-LIFE run, O4) | history selects the basin; the basin is the sufficient statistic |
| path-created constraints | E | route gain positive after native matching under randomised routes |
| equivalence classes of histories | the sufficient statistic itself: two histories are equivalent iff they induce the same future law | this is the definition of "matched present" and is the formal content of M6 |
| relational invariants | what survives the mapping history → future law | identical to the equivalence-class reading; the invariant is whatever the native model names |

The relational reading is therefore not a rival to the fixed-library reading; it is the general case of which the fixed library is the special case where the equivalence classes are indexed by current state alone. The empirical content is entirely in the route gain after native matching. Interpretation adds nothing the statistic does not already carry, and this document keeps them apart.

## 8. Strongest FLAME candidate (the synthetic gate is survived for the **interventional** regime only; see §2 and §3. No observational PR2 is proposed.)

**Carrier.** Deep continual learning (Dohare et al. 2024, Nature, public code; `DOMAIN_SEARCH.md` rank 1).
- **Routes.** Two task sequences (or two curricula) of equal length ending on the same task, assigned at random per network seed, stopped when the network reaches the same loss and accuracy on that task.
- **Matched present.** Loss, accuracy, calibration on the current task; the native plasticity statistics (dead-unit fraction, weight norm, effective rank of representations); and the weights' distributional statistics; tolerance 0.1 SD per variable, TOST equivalence; pairs failing the match excluded before perturbation.
- **Perturbation.** The same new task (or the same input/weight perturbation) for every network.
- **Outcome.** Learning speed and final accuracy on the new task over a fixed update budget; robustness.
- **Native rival (M6).** Prediction of the outcome from the matched present plus the plasticity statistics (Dohare's own account), plus a parameter-space baseline (distance travelled in weight space = cumulative gradient norm).
- **CRR quantity (declared now).** C = Fisher–Rao arc of the network's predictive distribution over a fixed probe set along training (the Fisher metric on softmax outputs; the core's definition, no new term); C* = Fisher–Rao chord between the initial and matched predictive distributions; S = C − C*. Because the present is matched on predictions, C* is nearly constant and S ≈ C − const; the Level-3 claim must therefore be stated as "C beats parameter-space path length, step count, loss-curve integral and a learned one-direction embedding", and S is reported only as a check that the chord is in fact constant.
- **Headroom.** Dohare's incremental-versus-scratch difference is large; whether it survives matching on the plasticity statistics is unknown and is exactly Level 2.
- **Falsifiers.** Level 2 fails if the route gain after full matching is below 0.01 nats per outcome unit; Level 3 fails if C does not beat the parameter-space path length on held-out and transfer sets, which is the expected outcome given §4.
- **Freeze requirements before any READY_FOR_FIRE.** A synthetic positive control at the carrier's noise (a network with an injected slow path-dependent constraint) that the frozen scorer detects; a negative control (state-sufficient) it does not; the tolerance list, horizon and statistic frozen and anchored; a second person running the frozen scorer; the whole run on seeds never used in development.

## 9. The observation that would force the concession

A sceptical modeller who holds that the present state is sufficient would have to concede if, prospectively, the following were seen on pre-registered units:

> Two populations of units are driven from a common start by routes assigned at random, and brought within a pre-declared tolerance of each other on every variable the best available model names as sufficient, including that model's own estimate of its hidden state. The same perturbation is applied to all. The futures differ, with a held-out predictive gain from the route label that exceeds the declared threshold and a permutation null at the declared level, and the difference is predicted, before the perturbation, by a path variable computed from the units' histories, at an accuracy that no variable computable from the matched present attains, on units and under a perturbation not used to fit it.

Randomisation is what rules out the omitted latent; matching on the model's own hidden-state estimate is what rules out "you did not measure enough of the present"; the prospective path predictor is what turns "history matters" into "this much of history, in this form". If that observation is made and the predictor is Fisher–Rao arc length rather than any cheaper history summary, CRR has a Level-3 result. Nothing in this study, in PR1, or in the Ashes and Embers record is such an observation.
