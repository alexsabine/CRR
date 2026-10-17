# SEC-OBS1-H-2026-10-08 — result

Scored 2026-10-08 06:27Z by the frozen scorer `studies/SEC-OBS1-H-2026-10-08/score_secobs1h.py` (unchanged since freeze commit 92c73fa) on 100 held-out synthetic histories. The seeds (831489–831588, draw seed 1598158214) were derived from the freeze commit's hash (`draw_log.json`).

Register: R4 (declared synthetic), engineering, specificity S0 for H1 and H2, N0. A provisional held-out pass in this tested class is not a finding. Verdict words below are the scorer's, as printed in `score.txt`.

Files:
* `heldout_episodes.jsonl` (sha256 99a65e60…2dcb), `score.json` (sha256 cd5f044e…f618), `score.txt`, `run.log` (episodes took 15 min 57 s on 3 workers).
* `rerun_check.jsonl`: 4 episodes re-run bit-identical, timings excluded.
* `describe_supplementary.json`: post-run descriptive tables. No verdict depends on them.

## Admissibility

All 100 episodes passed all three screens. The run was powered (≥ 80 required), and the branch construction was identical in every episode.

## Verdicts

| hypothesis | verdict | the numbers |
|---|---|---|
| **H1.** SEC-PG (light anchor κ_SEC/16, GPM from step 100) against the strongest inexpensive comparator | **PASS** | strongest comparator: transferred constant κ = 100 (mean J 0.4415). SEC-PG 0.4313; paired difference −0.0102 [−0.0136, −0.0068]. Guards hold: task-B loss 0.517 against SEC v2's 0.574; task-A loss 0.346 against 0.335 (+0.011 ≤ 0.05) |
| **H2.** The SEC-OBS hypothesis as posed: does an observation-aware diagnostic predict when the stronger intervention is worth it? | **NO** | H2a holds: mean AUC(N+O) 0.790 ≥ 0.70. H2b fails: N+O − N = −0.005 [−0.010, +0.001]; observation-aware features add nothing. H2c fails: intervening on the classifier's say-so is **worse** than always intervening, +0.0058 [+0.0039, +0.0080] in J, because it withholds the projection in 19 % of the cases where it helps by more than 0.02 (12.6 % of all history-condition pairs). The native classifier fails H2c the same way, so not even YES-NATIVE-ONLY |
| **H3.** Do the CRR path quantities (Fisher–Rao coherence, chord, apparent surplus) add predictive information beyond native diagnostics? | **FAIL** | primary target ΔJ: R²(N+C) − R²(N) = +0.0004 [−0.019, +0.018]. Secondary: AUC −0.005 [−0.013, +0.002]; true task-A rise R² −0.0002 [−0.004, +0.004]. Against N+O: −0.002, −0.004, −0.002 |
| **H4.** Observation-aware abstention for monitor-driven tuning | **PASS** | gain on the four corrupting conditions −0.113 [−0.128, −0.100]; change on the informative ones exactly 0 (never fired); detection balanced accuracy 0.944 (flags 84 % of projection, 71 % of missingness, all concept-drift and blind episodes, none of the informative ones). Against the constant alone: +0.0006 [−0.0001, +0.0013], i.e. no gain |

## Means of all arms (true J; lower is better)

| arm | J | arm | J |
|---|---|---|---|
| SEC-PG | **0.4313** | GPM alone | 0.4576 |
| transferred constant κ = 100 | 0.4415 | SEC + GPM from step 0 | 0.4812 |
| SEC v2 | 0.4547 | frozen trunk, new head | 0.5473 |
| pilot then full SEC weight | 0.4558 | none | 0.7767 |
| replay of 1,000 clean samples (extra information) | **0.3746** | frozen | 0.8832 |

Replay with a 1,000-sample clean buffer beats SEC-PG by 0.057. It uses stored old-task data, which the equal-information comparison excludes.

**By maturity** (SEC-PG / constant / SEC v2):

| task-A steps | n | SEC-PG | constant | SEC v2 |
|---|---|---|---|---|
| 300 | 55 | 0.4786 | 0.4810 | 0.5004 |
| 3,000 | 45 | 0.3734 | 0.3932 | 0.3988 |

The schedule's gain over the constant is concentrated in the mature regime.

## Descriptive (registered as descriptive only)

* **C1.** κ_SEC/κ* has a median of 5.7 at 300 task-A steps and 1.6 at 3,000. SEC's regret against the per-history best constant is 0.022 and 0.008. SEC v2 over-regularises young models, as in T4.
* **World 6** (full observation, intervention worth it, n = 65): the N+O classifier says intervene in 82 %.
* **World 8** (full observation, SEC's weight sufficient, n = 35): it says intervene in 23 %. These false interventions cost little, because the projection rarely hurts.
* **Worlds 9 and 5:** the true task-A damage at step 100 is predicted with R² 0.51 when the monitor is blind (N features) and 0.83 with a 64-sample clean reference.
* **Candidate 3** (direction-calibrated SEC): the η-corrected form gives J 0.449–0.463 by condition, against 0.456 for its baseline (pilot, then SEC's weight). Mixed: worse than its baseline in five conditions (+0.005 to +0.007, intervals excluding 0), slightly better under projection (−0.005) and missingness (−0.007). Never better than the constant (0.4415) or SEC-PG.
* **Recovery:** refitting the task-A head on 64 clean samples lowers the unprotected learner's task-A loss from 1.189 to 0.797, against the anchor's 0.317. About 45 % of its forgetting is in the readout.
* **Costs (seconds):**
  * per task-B run: SEC 0.42, SEC-PG 0.45 (of which projection 0.024), the constant 0.43;
  * once per task: GPM bases 0.005, SEC calibration 0.021;
  * the tuned sweep 3.27;
  * diagnostics 0.072 per condition per check.

## Reading

* **The engineering lead survived fresh histories.** A light anchor plus GPM projection switched on after a short plastic pilot beats SEC v2 by 0.023 nats and the strongest inexpensive comparator by 0.010. It does so at about 7 % more task-B compute and a GPM memory of about 14 % of the parameter count here.
  * The schedule uses no observation and no CRR quantity: its parts are EWC-style anchoring and GPM.
  * Its gain over the constant is small at young maturity and at high task overlap.
  * It has not been tested outside this synthetic generator; see the LLM pilot, `studies/SEC-OBS1-2026-10-08/llm_pilot/`.
* **The SEC-OBS hypothesis as posed is not supported.** A diagnostic can rank histories, but here the stronger intervention is right so often that acting on the ranking loses to always intervening. The observation-aware features add nothing to native ones.
* **The CRR path quantities add nothing beyond native diagnostics in this class.**
* **Observation-awareness has one demonstrated use: as a safety check on monitor-driven tuning.** ι catches the observation conditions under which a tuned sweep under-protects. The sweep's median chosen κ is 10 under projection, 30 under missingness, 0 under concept drift and 3 when blind, against 100 with full observation. It does not beat the cheapest monitor-free rule, the transferred constant.
* **A recorded discrepancy.** The frozen preregistration quotes a development AUC of about 0.75 for the native diagnostic. That was an interim figure from 71 of the 120 development episodes; the final development value is 0.695. The held-out value is 0.794, with the predictor fitted on all 120 development episodes. The discrepancy does not affect any verdict.

## Corrections after verification (2026-10-08)

A separate-context verifier re-ran the frozen scorer and reproduced `score.json` exactly. It confirmed all four verdicts and every number in the verdict table. It also corrected four statements in the reading, which are fixed above:

* H2's miss rate is 19 % of the cases where the projection helps. The 12.6 % figure is a share of all history-condition pairs.
* Candidate 3 is mixed, not "within noise".
* The sweep's chosen κ under each condition is now stated, instead of "almost no protection".
* "Cheapest strong" is replaced by "strongest inexpensive", the scorer's selection rule.
