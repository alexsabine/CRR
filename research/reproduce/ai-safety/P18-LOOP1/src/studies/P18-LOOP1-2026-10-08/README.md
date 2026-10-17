# P18-LOOP1 / P17: a feedback-provenance harness in a performative loop (development; synthetic; 2026-10-08)

**Status.** Development only: synthetic worlds, no preregistration, no ledger rows. It is the first harness for P18's one declaration-grade sub-claim and for P17's loop-world localisation design (`AI_SAFETY/SEED_TO_FLAME_2026-10-07.md`). **Owner instruction:** `notebook/PROMPT_LOG.md`, 2026-10-08 about 17:28Z, item 5 ("advance the P17/P18 feedback-provenance harness where feasible").

**Files.**
* `loopworld.py`: the world, the detectors, the localisers and the summary.
* `outputs/loop_runs.jsonl`: one row per world and seed.
* `outputs/loop_summary.json`: the tables below.
* `outputs/loop_log.txt`: stdout.

Run with `python3 -I loopworld.py 200 200` (about 20 CPU-minutes).

## The world (performative prediction in its simplest strategic form)

**Population and agent.**
* d = 8 features.
* The agent refits a logistic classifier every round on its last 5 rounds of data. It publishes two outputs:
  * the classifier, θ;
  * an "explanation", e: the classifier's top-2 coefficients.

**Gaming.**
* From an onset round τ (drawn from 20–35), applicants shift the one gameable feature along the published output they respond to: θ in the *game_theta* worlds, e in the *game_expl* worlds.
* The gameable feature is the one with the largest true weight.
* The shift ramps up over 8 rounds and scales with an individual propensity c ~ U(0, 1).

**Labels.**
* The **proxy** label is measured from the observed (gamed) features.
* The **target** label comes from the true features. The agent never sees it: it is the independent endpoint.
* The **divergence round** is the first round at which proxy accuracy exceeds target accuracy by at least 0.05. It is set by the world, not by any detector.

**Exogenous change.** In the *exo* worlds, a real, label-consistent shift of another feature starts at a random round. It moves the proxy and the target alike, so it creates no divergence.

## The worlds

| world | gaming | exogenous change | role |
|---|---|---|---|
| aligned | none | none | calibration: sets every detector's threshold at a 5 % false-alarm rate (200 calibration seeds) |
| game_theta | along θ | none | must-pass: a divergence exists and the proxy hides it |
| game_expl | along e | none | the outputs that re-enter are not the model's score direction |
| exo | none | yes | must-not-alarm for divergence: a real shift with no proxy/target gap |
| game_theta+exo, game_expl+exo | yes | yes, larger than the gaming shift in another channel | confounded: the plausible but wrong trace (P17's negative witness) |

## Detectors

Each detector runs a one-sided CUSUM on a per-round statistic, standardised on rounds 1–10, with its threshold set on the aligned world.

| detector | statistic | what it represents |
|---|---|---|
| proxy | fall in proxy accuracy | the monitor Goodhart defeats |
| calib | rise in ECE against proxy labels | calibration monitoring |
| inshift | squared norm of the input-mean shift | a generic input-drift detector (no provenance) |
| bbsd | shift in the mean deployed score θ·x | black-box shift detection on the model's own output (Lipton et al. 2018; Rabanser et al. 2019) |
| **prov** | input-mean shift projected on every output the agent has published (θ and e) | the Empty Centre's operational rule, "which of my outputs re-entered my inputs" (`HEURISTIC/EMPTY_CENTRE.md` §3) |
| prov_abl | the same projection on random directions of the same sparsity | provenance removed (the ablation SEED_TO_FLAME asks for) |

## Localisation (P17)

At divergence + 10 rounds, each localiser names the gamed channel.

| localiser | how it chooses |
|---|---|
| event log | the largest input-mean shift |
| provenance | the largest shift signed along the published outputs |
| intervention | the native causal rival: for 6 rounds, the published output's sign is flipped at random per channel, and each channel's input-mean level is correlated with the flips. Its decision cost in target accuracy is reported. |
| shuffled | provenance with the outputs' channels permuted (shuffled annotations) |
| none | a uniform guess |

## Results (200 seeds per world; development; `outputs/loop_summary.json`, `outputs/loop_contrasts.json`)

**Detection score** (1 − delay/80; 0 for a miss or for an alarm more than 5 rounds before divergence). In the aligned and exo worlds the cell shows the alarm rate.

| world | proxy | calib | inshift | bbsd | **prov** | prov_abl |
|---|---|---|---|---|---|---|
| aligned (alarm rate) | 0.05 | 0.065 | 0.025 | 0.01 | 0.01 | 0.075 |
| game_theta | 0.000 (199/200 missed) | 0.005 | **0.991** | 0.971 | 0.982 | 0.814 |
| game_expl | 0.000 (199/200 missed) | 0.005 | **0.990** | 0.969 | 0.979 | 0.849 |
| exo (alarm rate; no divergence) | 0.025 | 0.04 | 1.00 | 0.53 | 0.535 | 0.99 |
| game_theta+exo | 0.000 | 0.009 | 0.746 (50 early) | 0.888 | **0.917** | 0.796 |
| game_expl+exo | 0.000 | 0.005 | 0.789 (41 early) | 0.900 | **0.919** | 0.812 |

**Paired contrasts over seeds** (mean, 95 % bootstrap interval).

| world | prov − bbsd | prov − inshift | prov − prov_abl |
|---|---|---|---|
| game_theta | +0.011 [0.010, 0.013] | −0.008 [−0.010, −0.007] | +0.169 [0.139, 0.201] |
| game_expl | +0.010 [0.009, 0.011] | −0.011 [−0.012, −0.009] | +0.130 [0.106, 0.157] |
| game_theta+exo | +0.029 [0.009, 0.050] | +0.172 [0.119, 0.229] | +0.121 [0.078, 0.166] |
| game_expl+exo | +0.019 [0.003, 0.037] | +0.130 [0.083, 0.179] | +0.107 [0.062, 0.153] |

**Localisation accuracy** (the gamed channel among 8). The intervention's target-accuracy cost was below 0.004 in every world.

| world | event log | **provenance** | intervention | shuffled | none |
|---|---|---|---|---|---|
| game_theta | 1.00 | 1.00 | 0.975 | 0.46 | 0.095 |
| game_expl | 1.00 | 1.00 | 0.98 | 0.475 | 0.095 |
| game_theta+exo | 0.32 | **0.96** | 0.975 | 0.385 | 0.095 |
| game_expl+exo | 0.645 | **0.985** | 0.98 | 0.40 | 0.095 |

## What this shows

1. **The instrument works.** The proxy and calibration monitors miss the divergence in 199 of 200 runs: the world hides a Goodhart failure from the proxy, as designed. The aligned world holds every threshold at or below 7.5 %.
2. **In clean worlds, provenance adds nothing over a generic input-drift detector.** The generic detector is better by 0.008–0.011. Provenance beats BBSD by about 0.01, which is detectable but practically negligible.
3. **Provenance cannot tell re-entry from exogenous change that projects on its outputs.** In the exo world it alarms in 53.5 % of runs, the same as BBSD (53 %), although there is no divergence.
4. **Its edge appears only when a large exogenous change sits in another channel.**
   * Detection: +0.02–0.03 over BBSD, with intervals excluding 0, and +0.13–0.17 over the generic detector.
   * Localisation: it names the gamed channel 0.96–0.985 of the time, where the event log is misled to 0.32–0.645.
   * **But the native causal rival does as well.** Six rounds of randomised sign flips of the published output localise at 0.975–0.98, at negligible decision cost in this world.
5. **The ablation shows that the published outputs carry the signal.** Random directions of the same sparsity lose 0.11–0.17 in detection, and permuted annotations localise at 0.39–0.48.

## Usefulness, separately from CRR

* **The harness is useful in its own right.** It is a small, fast performative-prediction world with an independent target endpoint, a Goodhart divergence the proxy cannot see, a confounded variant, and a causal-intervention rival.
* It can host the registry's other P18 sub-claims, for example sycophancy-style proxy optimisation, as separate worlds.

## CRR's contribution, separately

* **What it shaped.** The Empty Centre's rule ("keep the record of which of your outputs re-entered your inputs") defined the candidate statistic and the shuffled-annotation control.
* **The native route.**
  * Operationally, the statistic is the input-mean shift projected on the agent's published outputs: model-output (black-box) shift detection, extended to every published output.
  * Its localisation is matched by randomised intervention on the published output, an A/B-style test that needs no CRR.
* **Grade.**
  * **DESIGN** for the harness and the controls, since the framing produced the confounded worlds and the ablation.
  * **NOTHING** for detection beyond BBSD in clean worlds.
  * **PENDING** for the confounded-world edge: an engineering effect of about 0.02–0.03, development only, and plausibly an artefact of how strongly the exogenous change was placed in a channel off the published direction.
* The Empty Centre's further claim, that provenance supports "reliable intervention" (P17), is not supported beyond what intervention itself provides.

## Status and what would be needed for FLAME

* **P18's sub-claim.** A harness and a provenance ablation now exist; SEED_TO_FLAME named both as the missing pieces.
* **G2's identifiability requirement against "a shift detector that happens to use input features" is only half met.**
  * Provenance separates from the generic detector and from its ablation.
  * Against BBSD it separates only in confounded worlds, and by about 0.02–0.03.
* **A FLAME declaration would need:**
  * a registered bound on prov − bbsd in a confounded-world family whose confounder geometry is drawn, not designed;
  * the exo world as a must-not-alarm control, with a registered limit (both detectors fail it today);
  * the intervention arm as the strongest rival for localisation.
* **This note does not declare FLAME.** It is recorded as development evidence toward it.
