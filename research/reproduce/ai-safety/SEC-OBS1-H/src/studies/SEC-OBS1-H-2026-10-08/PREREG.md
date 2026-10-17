# Preregistration: SEC-OBS1-H-2026-10-08 (held-out test of the SEC-OBS1 development selections; claim-specific scorer)

Protocol file: `PREREG_CLAIM.json`. Scorer: `score_secobs1h.py` (frozen with this file). Runner: `run_episodes.py` and `secobs_lib.py`, byte-identical to the development copies in `studies/SEC-OBS1-2026-10-08/dev/` (sha256 recorded in `HASHES.sha256` at freeze). Development data: `dev_episodes.jsonl` (120 development episodes, seeds 10000–10119, draw seed 101), frozen here. It is used to fit the H2/H3 predictors and is never rescored as held-out.

**Register.** R4 (declared synthetic: every world comes from the same generator as development, with fresh history seeds). Layer: engineering. Specificity: H1 S0 (the selected schedule combines native components; no CRR restriction); H2 S0 (a diagnostic; its observation-aware features are ordinary mathematics); H3 tests whether a CRR-derived quantity (Fisher–Rao path coherence and apparent surplus) adds anything to standard diagnostics. Novelty N0 throughout: the design was selected on development data from the same generator. A pass here is a provisional held-out pass in this tested class. It is not a finding, and it says nothing about transformers or real streams.

**Parents.** SEC-OBS1 development (`studies/SEC-OBS1-2026-10-08/`); the SEC lineage (SEC v2, `CRR-LLM-CALIBRATION/SEC_V2_RULE.md`); T4 (maturity over-regularisation, C1). Failed parent named under R12: the T2/T3 direction line (`CRR-LLM-CALIBRATION/T2-DIRECTION-2026-10-07/`, STOP). Candidate 3 (direction-calibrated SEC) is its successor. It failed in development and is reported here descriptively only.

## What is held out

100 fresh histories. Seeds `first = 200000 + (int(sha[:8], 16) mod 700000)` and `draw_seed = int(sha[8:16], 16)`, where `sha` is the full hash of the commit that adds this frozen folder (`run_heldout.sh` computes both and writes `draw_log.json`). The development seeds are 10000–10119, which cannot collide. Each episode draws overlap uniformly from 0..8 and task-A maturity from {300, 3000} steps, exactly as in development. Nothing about these seeds or their outcomes has been seen.

## Admissibility (C2: genuine learning before scored evaluation)

Per episode, all of:

* task A learned: clean accuracy at the end of A ≥ 0.70 (chance 0.25);
* task B genuinely learned by the unprotected learner: accuracy ≥ 0.75, B loss at least 0.5 nats below the frozen learner's, and at least 0.05 below a frozen-trunk head;
* forgetting at stake: the unprotected learner's task-A loss at least 0.10 above the anchor's.

Episodes failing any screen are excluded and counted. If fewer than 80 of 100 are admissible, the study is reported **INCONCLUSIVE (underpowered)** and no hypothesis is scored as passing. Development: 120 of 120 admissible.

## Hypotheses and decision rules

Primary metric: true `J = ½(L_A + L_B)` on clean territory test sets (4,000 samples per task) that no method sees. Intervals: percentile bootstrap over admissible held-out episodes, B = 4000, `default_rng(0)`.

**H1 — primary, engineering (the design that survived development).** *SEC-PG* is the `D2:gpm@k` arm: SEC's weight divided by 16 (`κ = 10·s/16`) for all 400 task-B steps, plus GPM update projection of the trunk weights onto the complement of the stored task-A input subspaces (energy threshold 0.97), switched on at step 100.

* Comparators (inexpensive: one task-B run each, no stored samples): SEC v2; the transferred constant `κ = 100` (the development's best constant, fixed now); GPM alone; SEC + GPM from step 0; frozen trunk with a new head.
* The strongest comparator is the one with the lowest held-out mean J. This is chosen on held-out data, the conservative direction.
* **PASS** requires all of:
  * mean paired difference J(SEC-PG) − J(strongest) ≤ −0.005 with the 95 % upper bound < 0;
  * guard on genuine learning: mean task-B loss of SEC-PG below SEC v2's;
  * guard on retention: mean task-A loss of SEC-PG no more than 0.05 above SEC v2's.

  Otherwise **FAIL**.
* Development expectation (120 episodes; the selection was made on these same episodes, so this is in-sample): SEC-PG 0.4249, SEC v2 0.4477, constant κ = 100 0.4367, GPM alone 0.4504, SEC + GPM 0.4707, frozen trunk with a new head 0.5411. SEC-PG minus the constant: −0.0119 (better in 80 % of episodes). SEC-PG's task-A loss is 0.350 against SEC v2's 0.339; its task-B loss is 0.500 against 0.557. Source: `dev_summary.json`.

**H2 — the SEC-OBS hypothesis as posed (primary engineering question).** At step 100 of a plastic pilot (D2), does a cheap diagnostic predict when the stronger intervention is worth its cost?

* Target: y = 1 if J(SEC-PG) < J(pilot then full SEC weight from step 100) − 0.02.
* Classifiers: logistic regression (C = 1) fitted on all admissible development episodes, pooled over the eight observation conditions. Native features N (15 standard diagnostics) against observation-aware features N+O (N plus anchor re-evaluation, observability ι, direction visibility η and two derived ratios).
* Evaluated on held-out episodes in each of the eight observation conditions.
* H2a: mean AUC(N+O) ≥ 0.70.
* H2b: mean AUC(N+O) − mean AUC(N) ≥ 0.02 with the 95 % lower bound > 0.
* H2c (decision value): intervening iff p̂ ≥ 0.5 beats always intervening by ≥ 0.002 in mean J, with the 95 % upper bound < 0.
* Verdicts:
  * **YES-OBSERVATION-AWARE** if H2a, H2b and H2c all hold;
  * **YES-NATIVE-ONLY** if the native classifier meets the H2a and H2c thresholds;
  * **NO** otherwise.
* Development expectation: native AUC ≈ 0.75, N+O no better, always intervening close to the oracle. The expected verdict is NO, or YES-NATIVE-ONLY at most.

**H3 — secondary scientific question.** Do CRR-derived coherence and apparent surplus (Fisher–Rao length of the old-task output distributions over the pilot's checkpoints on observed probes, the chord, their difference and their ratio) add predictive information beyond the native features?

* Ridge (α = 10) for continuous targets and logistic regression for the binary one, fitted on development and evaluated on held-out, averaged over conditions.
* Primary H3 target: ΔJ = J(SEC-PG) − J(pilot then full SEC weight).
* **PASS** if R²(N+C) − R²(N) ≥ 0.02 with the 95 % lower bound > 0. Reported also: N+O+C against N+O; the y target (AUC); the true task-A rise at step 100 (R²).
* Note: the apparent surplus is the coherence minus the chord, so for a linear model it adds nothing to that pair (`FOUNDATIONS/MATHEMATICAL_OBJECT.md` line 15). Development expectation: no gain (N+C at or below N).

**H4 — observation-aware abstention for monitor-driven tuning.** The tuned sweep picks κ from {0, 3, 10, 30, 100, 300, 1000, 3000} by observed validation J. Its task-A validation passes through the condition's channel; task B is observed cleanly. The aware sweep uses the transferred constant κ = 100 whenever the anchor's observability ι < 0.5 on that condition's probes, and the sweep's choice otherwise.

* **PASS** if all of:
  * mean J gain over the four by-construction corrupting conditions (proj, missing, concept, hideA) ≥ 0.02 with the upper bound of the difference < 0;
  * mean change over the four informative conditions (full, alias, drift, hideA+ref) has its upper bound < 0.005;
  * ι < 0.5 separates the two groups with balanced accuracy ≥ 0.90.
* Also reported: the aware sweep against the constant alone.
* Development expectation: PASS on abstention, with no gain over the constant.

**Descriptive only (not hypotheses).**

* Candidate 3 (SEC's secant re-measured along the actual task-B displacement; a: with the stored Fisher; b: with the observed-probe Fisher, the η-corrected form) by condition.
* C1: SEC's over-regularisation by maturity (median κ_SEC/κ*).
* Worlds 6 and 8: sensitivity and false interventions under full observation.
* Worlds 9 against 5: blind observation against blind observation plus a 64-sample clean reference.
* Recovery by refitting the task-A head on the 64-sample buffer.
* Costs and stored floats.

## The nine worlds of Part D, as realised here

All conditions within an episode share one underlying history and identical training. Only what the monitors and the sweep's task-A validation can see differs.

| Part D world | realisation |
|---|---|
| 1 fully informative | condition `full` |
| 2 known lossy projection | `proj` (random 12-dimensional subspace of the 24-dimensional input) |
| 3 class overlap / aliasing | `alias` (classes 0 and 1 merged in the observed label) |
| 4 stochastic missingness | `missing` (each feature zeroed with probability 0.4) |
| 5 partial observability with historical reference | `hideA+ref` (the stream hides A's subspace; a 64-sample clean buffer stored at the end of A is used instead) |
| 6 genuine forgetting without observation loss | `full`, episodes where the stronger intervention is worth it (y = 1) |
| 7 drift without forgetting | `drift` (covariate shift of the probe stream) and `concept` (label permutation on half the stream) |
| 8 negative control, ordinary SEC sufficient | `full`, episodes with y = 0 |
| 9 erased information, unrecoverable without another source | `hideA` (projection removing A's input subspace; no buffer) |

## Equal information and compute

* **Common to every arm:** the stored anchor, SEC's Fisher and secant, the GPM bases (computed at the end of A from clean A inputs, as GPM does), the recorded clean end-of-A loss, and current task-B data.
* **Monitors and the sweep:** they see task A only through the condition's channel.
* **Replay arms:** they use stored clean samples. They are reported as extra-information references, not as equal-information comparators.
* **Ground truth:** no method reads the territory test sets.

**Budget.** CPU only, 3 worker processes; about 30 s per episode in development, so about 17 minutes for 100 episodes. Wall-clock is recorded.

## What would change the reading

| outcome | reading |
|---|---|
| H1 FAIL | the schedule's development gain did not survive fresh histories |
| H1 PASS with H2 NO | there is an engineering lead (a schedule) but no diagnostic value; the SEC-OBS hypothesis as posed is not supported here |
| H3 FAIL | CRR path quantities add nothing beyond native diagnostics in this class |
| H4 PASS with no gain over the constant | observation-aware abstention protects monitor-driven tuning but does not beat the cheapest monitor-free rule |
