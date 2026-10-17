# P18-PROV-FLAME: FLAME declaration draft for the provenance statistic in drawn confounded loop worlds (2026-10-09)

**Status: DRAFT for the owner's review.**
* Not frozen, hashed or anchored.
* No held-out world has been generated, and there is no ledger row.
* Nothing here is a result. The development numbers come from `studies/P18-LOOP1-2026-10-08/` (synthetic, seen) and from the helper scripts in this folder. Those scripts read the development outputs or run development seeds only.

**Role.** Experimentalist and statistician (`AGENTS/roles/`). This draft was written and reviewed in one model context, which is not independent review (P-G1).

**Stage.**
* For this sub-claim, P18 and P17 are at SPARK (`AI_SAFETY/SEED_TO_FLAME_2026-10-07.md`).
* The development harness P18-LOOP1 supplied the two pieces SEED_TO_FLAME asked for: a harness and a provenance ablation.
* This draft proposes FLAME for an **engineering** claim (§1.3).
* It also states why the **CRR-specific reading** of that claim (the value of a provenance record) cannot pass G2's identifiability requirement in this harness (§1.4, §6). That reading stays at SPARK.

---

## 0. Inputs, and what the author has seen

| file | sha256 | used for |
|---|---|---|
| `studies/P18-LOOP1-2026-10-08/loopworld.py` | `9c6bed7953adce57f1d7dd39c3067fdba56c21396e3b8b31f52095cab618f1cc` | the world, detectors, localisers; imported unchanged by `provworld_draft.py` |
| `studies/P18-LOOP1-2026-10-08/loop_contrasts.py` | `4729fe0d93a3d1163b778a5e5be6862c6405cab2a3f3b038ecbecaea5aba8df9` | development contrasts (read only) |
| `studies/P18-LOOP1-2026-10-08/outputs/loop_runs.jsonl` | `f580b15927b9d6d2a6b31469a915dee9f7b2621d7ae5740660255226e4333935` | per-seed development rows; the source of every development number in §5 |
| `studies/P18-LOOP1-2026-10-08/outputs/loop_summary.json` | `ef542186f634ddc1b01538ed597e7906d00af67cbe1d9460dd04a082464550c5` | development thresholds and tables |
| `studies/P18-LOOP1-2026-10-08/README.md` | `6e85fce7366d90d953785ade72f01dc3f854a21deaf01efce5ff3778d3cb1140` | the three FLAME requirements (its "Status and what would be needed for FLAME") |

**Also read:**
* `HEURISTIC/CRR_INFLUENCE_2026-10-08.md` §3.3 and `HEURISTIC/EMPTY_CENTRE.md`;
* `ENQUIRIES/REGISTRY.json` (P17, P18);
* `EPISTEMIC/GATES.md`, `EPISTEMIC/R1_R15_EXACT.md` and `EPISTEMIC/GUARDRAILS.md`;
* `EPISTEMIC/OWNER_DECISIONS_2026-10-09.md` (OD-12, OD-13);
* `studies/SEC-PG-LLM-H-2026-10-08/data_step.py` (the beacon precedent).

**What the author has seen.**
* All development outputs of P18-LOOP1.
* Re-analyses of them by `power_plan.py`, including the dependence of the contrast on the detection window (§5.1). This was seen **before** the window and δ below were chosen; it is disclosed as adaptivity (§2.5).
* `outputs/tiny_check.json`: 6 development units (drawn geometry, drawn G, open loop, on-support confounder) scored against thresholds from only 6 aligned runs. This was a code-path check, and its per-unit outcomes carry no information.

**Compute used for this draft.**
* Under one CPU-minute of simulation in total, all at `nice -n 19` with one thread, on development seeds only. No full-size run.
* Repository commit at writing: `3a0daf6f6feb49d6495c27226de009db3a568563` (branch `claude/ecstatic-hawking-26npxo`).
* Environment: Python 3.11.15, NumPy 2.4.6.

---

## 1. The claim, in native terms

### 1.1 The world (performative prediction; unchanged from P18-LOOP1 except where stated)

**Population, agent and outputs.**
* d = 8 features.
* A logistic classifier θ is refitted every round on the last 5 rounds of (observed inputs, proxy labels).
* The agent publishes two outputs: θ itself, and an "explanation" e, which is the top-2 coefficients of θ.

**Gaming.**
* From an onset τ, applicants shift the gameable feature G (the largest true weight) along the published output they respond to: θ or e.
* This is strategic classification inside a performative loop (Perdomo et al. 2020; Hardt et al. 2016; both to be fetched and versioned for the prior-art dossier, R10).

**Labels and divergence.**
* The proxy label is computed from the observed (gamed) inputs; the target label from the true inputs. The agent never sees the target.
* The divergence round is the first round at which proxy accuracy exceeds target accuracy by at least 0.05. It is set by the world, never by a detector.

**Confounder.** An exogenous change moves the true inputs, so it moves the proxy and the target alike. It is a real shift with no divergence. **This draft changes only its geometry, which is now drawn (§2).**

### 1.2 The candidate statistic, in native terms

prov_t = max over o ∈ {θ_{t−1}/‖θ_{t−1}‖, e_{t−1}/‖e_{t−1}‖} of (x̄_t − x̄_ref) · o

* x̄_t is the mean observed input in round t, and x̄_ref is the mean over rounds 1–10.
* A one-sided CUSUM (k = 0.5) runs on the standardised statistic.
* The threshold is set at the aligned world's 5 % false-alarm rate.

**In native terms**, this is black-box shift detection (Lipton et al. 2018; Rabanser et al. 2019) applied to every output the system publishes. The input-mean drift is projected on each published output direction and the projections are combined by their maximum.

### 1.3 The claims proposed for FLAME

**H-det (P18, primary; engineering; the "shift reading").** In loop worlds with gaming and a label-consistent exogenous change whose geometry is drawn from the distribution in §2.1, prov detects the proxy/target divergence in time more often than score-mean BBSD, by at least δ = 0.02 in detection power.
* "In time" means a first alarm within [div − 5, div + 5].
* The comparison is at a matched 5 % false-alarm rate on the aligned world.
* prov must also beat normalised BBSD, the generic input-drift detector and its own ablations by the same margin (§4.1).

**H-div (P18; the "divergence reading").** H-det, and in addition prov does not alarm on label-consistent exogenous change when there is no divergence: the exo world as a must-not-alarm control (§3.4). Only H-div would bear on P18's question as worded ("detect proxy failure").

**H-loc (P17; secondary).** At divergence + 10 rounds, the provenance localiser names the gamed channel more often than randomised intervention on the published output, by at least δ_loc = 0.05, at matched observation window and decision cost (§3.5).

### 1.4 What CRR contributed, and what it did not

**Contributed: the question and the controls.**
* The question is the Empty Centre's: "which of my own outputs will be in my next inputs, and have I kept the record that lets me tell?" (`HEURISTIC/EMPTY_CENTRE.md` §2–§3).
* The controls: shuffled annotations; a confounder off the published direction; the label-consistent exo world as a must-not-alarm control.

**Not contributed: the mechanism.**
* The statistic is a projection. Its advantage, if any, is a matched-filter effect (§6).
* No CRR quantity enters the scorer: no Fisher–Rao length, no cut, no surplus.

**A structural fact registered in advance.**
* In this harness the published explanation e is a deterministic function of θ (its top-2 coefficients). A monitor that holds θ but keeps no record of what was published can therefore compute prov exactly.
* The provenance-free twin `pf_twin` does this. It equals prov in every unit checked (`outputs/equiv_check.json`, `outputs/tiny_check.json`).
* Consequences:
  * any RESULT is credited to the statistic, not to a provenance record;
  * the provenance-record reading is recorded in advance as **REDUCES (structural) to pf_twin** (§4.1).

### 1.5 Ceiling

* Engineering.
* Evidence rung R6 at most (a provisional held-out pass in a synthetic world class).
* Novelty N0 until a prior-art dossier exists.
* Specificity S2.
* PASS-0 at most from this study. PASS-1 is unavailable to the provenance reading because of the structural reduction. PASS-2 needs replication (G7).
* No statement about real deployed systems.

---

## 2. The drawn confounder family

### 2.1 Declared distribution

The geometry is drawn **per unit**, from a generator separate from the world generator. It therefore cannot depend on β, on G, on τ or on the published outputs.

| component | distribution | note |
|---|---|---|
| channel (support) | k ~ U{1, …, 8}; the support is k of the 8 features, drawn uniformly without replacement | G and the published top-2 channels can be included |
| direction | w ~ N(0, I_k) on the support; v = w/‖w‖ | k = 8 is isotropic on the unit sphere; signs are random |
| magnitude | mag = exp(U(log 0.75, log 3.0)) | log-uniform; geometric mean 1.5, the development magnitude |
| onset, ramp | onset τ_x ~ U{15, …, 39}; linear ramp over 10 rounds (world generator, as in development) | unchanged |
| entry route | x_true ← x_true + mag · ramp(t) · v | label-consistent: moves the proxy and the target alike |

**Why "channel" means the support, not the entry route.** A change to the observed inputs alone would itself open a proxy/target gap. That would be a second cause of divergence, not a confounder. A confounder is a real change, so it enters the true inputs.

The draft implementation is `draw_geometry()` in `provworld_draft.py`.

### 2.2 Where the designed development worlds sit inside the family

**The development geometry** was one-hot on a channel kx ≠ G, with magnitude 1.5. It lay wholly off the published top-2 support unless kx happened to be the second published channel: about 6/7 = 0.857 of worlds.

**Under the declared distribution** (`outputs/geom_stats.json`, 200 000 draws):
* The confounder lies wholly off a given 2-channel support with probability **0.25** (exact; Monte Carlo 0.2487).
* The mean share of its energy on that support is 0.25.
* The mean |component on G| is 0.217.
* The magnitude's 5th–95th percentiles are 0.80–2.80 (median 1.50).

**The designed geometry is a corner of the family.** "One channel, off the top-2" has probability 1/8 × 6/8 ≈ 0.094. The mechanism that produced the development edge (the top-2 projection discards confounders outside its support; §6) therefore operates fully in about a quarter of drawn worlds rather than six-sevenths.

### 2.3 Draw rule (beacon)

The rule follows `studies/SEC-PG-LLM-H-2026-10-08/data_step.py` (a future Bitcoin block hash, checked against two public explorers).

**Draw height.**
* `DRAW_BLOCK_HEIGHT` is fixed in the frozen file as the Bitcoin chain tip at freeze time plus 144 blocks (about 24 h).
* The tip height read, and the UTC time it was read, are written into the frozen file.

**Anchor checks.** A1–A8 as in SEC-PG-LLM-H:
* the frozen folder is unchanged against FREEZE.json;
* the OpenTimestamps proof is for this FREEZE.json;
* its Bitcoin attestation is confirmed by blockstream.info and mempool.space, with matching merkle root;
* the attested time plus 7200 s precedes now;
* the date rule (A5): the UTC date is on or after max(2026-10-10, freeze date + 1 day), because W, δ and the arms were chosen on development data on 2026-10-09 (R3);
* the clone is not shallow, and the single freeze commit holds the stamped FREEZE.json;
* the draw block has at least 6 confirmations, and both explorers give the same hash;
* no draw has started.

One check is new:
* **A9.** The earliest Bitcoin attestation of FREEZE.json is at a height strictly below `DRAW_BLOCK_HEIGHT`. This makes the freeze provably older than the draw block. If A9 fails, the block is void for this freeze and the study is NOT DECIDABLE under this ID.

**Keys.** fc is the freeze commit and bh is the hash of the draw block.
* unit seed: s(tag, i) = 1 000 000 + int(sha256("fc|bh|tag|i")[:15], 16). This is a 60-bit range; a repeated seed among about 16 000 units has probability about 10⁻¹⁰, and the draw still asserts uniqueness.
* geometry generator: `default_rng(int(sha256("fc|bh|geom|tag|i")[:16], 16))`.
* probe-flip generator: `default_rng(int(sha256("fc|bh|flip|tag|i")[:16], 16))`.
* bootstrap generator: `default_rng(int(sha256("fc|bh|boot")[:16], 16))`.

**Arms** (tags; i counts from 0):

| tag | world | units | assignment |
|---|---|---|---|
| `cal` | aligned | 2000 | threshold calibration |
| `far` | aligned | 1000 | false-alarm validation (C2) |
| `conf` | gaming + drawn confounder | draw in index order until **6200 diverged** units; cap 6800 draws | gaming along θ for even i, along e for odd i |
| `exo` | drawn confounder only | 1000 | must-not-alarm (C4) |
| `clean` | gaming, no confounder | 500 | positive control (C1, C9); θ for even i, e for odd |
| `designed` | gaming + development geometry | 1000 | S8 |
| `gch` | gaming + drawn confounder + drawn gameable channel | 1000 | S9 |
| `sf3` | gaming + confounder on the published top-2 support | 500 | C7 |
| (open loop) | the `conf` seeds and geometries for i < 2000, with open-loop gaming | 2000 | C8 (paired with `conf`) |

**Stopping rule.** The stop at 6200 diverged units depends only on whether each world diverges, which no detector influences. If the cap is reached first, the study is NOT DECIDABLE.

The draft functions are `unit_seed`, `geom_rng`, `flip_rng` and `draw_geometry` in `provworld_draft.py`. The tiny check used the dummy strings `DEVELOPMENT-ONLY` and `NOT-A-BLOCK-HASH`, never a block hash.

### 2.4 Why development worlds cannot leak into the held-out family

1. **The seeds are disjoint.** Every development seed is below 10⁶:
   * the development tests (0–199);
   * the calibration seeds (10 000–10 199);
   * their +17 offsets for random directions;
   * this folder's checks (500–511 and 20 000–20 005);
   * the planned pilot ranges (100 000–209 999).

   Every held-out seed is at least 10⁶, from a 60-bit range.
2. **The seeds are unknowable at freeze.** A block hash about 144 blocks ahead can be neither known nor chosen when the freeze is stamped, and A9 proves the order. The freeze commit is fixed before the block exists. `freeze_prereg.py` refuses refreeze, so one block cannot be tried against several freezes.
3. **The generators are separate.** Geometry and probe flips come from hashed generators, not from the world seed, so no held-out geometry is a function of a development seed.
4. **The thresholds are fresh.** Calibration worlds are drawn from the beacon. The development thresholds (from seeds 10 000–10 199) are not reused.
5. **The code is frozen.** `loopworld.py` is imported unchanged and locked by the hash in §0. The frozen runner must pass the equivalence check: with the development geometry and no probe, it reproduces `loopworld.simulate` array for array (`outputs/equiv_check.json`: 4 worlds, identical).
6. **The pilot is isolated.** The pilot (§7) uses development seeds, reports the primary contrast only as a sealed commitment, and can only raise n.

**Residual risks.**
* A miner could withhold a block to steer its hash. There is no plausible incentive here.
* An operator could freeze, see the block and abandon the study. This is mitigated by pushing the freeze commit and the OTS proof before the block, and by OD-11 (abandoned frozen studies are recorded).

### 2.5 What does carry over from development (disclosed)

Every design choice was made by an author who has seen the development outputs:
* the world;
* the detectors;
* CUSUM k = 0.5;
* the 10-round baseline;
* the 5-round early-alarm tolerance;
* the window W = 5;
* δ;
* the arms.

This adaptivity can inflate the expected effect size (§5.2). It cannot make held-out worlds equal to development worlds.

---

## 3. Endpoints and analysis

### 3.1 Unit of analysis

The unit is one drawn world: a seed, its drawn geometry and its gaming target, simulated for 80 rounds.
* Every detector and localiser runs on the same trajectory, so all contrasts are paired within the unit.
* Units are independent: distinct seeds and independent geometry draws. The only shared component is the thresholds, handled in §3.3.
* Only units whose world diverges enter the detection and localisation endpoints. Units that do not diverge are counted and reported.

### 3.2 Fixed false-alarm rate

**Rule.** For each detector, the threshold is the ⌈0.95 × 2000⌉-th smallest per-run maximum of the CUSUM over 80 rounds in the 2000 `cal` runs. This is the development rule with ten times the runs.

**Check.** The rate is validated on the 1000 `far` runs (C2).

**Why 2000 runs.** In development, prov and bbsd alarmed in 0.01 of aligned test runs against a nominal 0.05 (`loop_summary.json`). The 200-run calibration was too coarse.

### 3.3 Primary endpoint (H-det)

**Endpoint.** For unit i and detector k with first alarm a_ik:

T_ik = 1 if div_i − 5 ≤ a_ik ≤ div_i + 5, else 0.

* An alarm more than 5 rounds early is a false alarm relative to the divergence.
* No alarm, or a later one, is a miss.

**Contrast.** Δ = mean over the 6200 diverged `conf` units of (T_i,prov − T_i,bbsd): the difference in detection power at the matched 5 % false-alarm rate.

**Interval.** A two-sided 95 % percentile interval [L, U] from a **two-level paired bootstrap** with B = 4000. Each replicate:
1. resamples the 2000 calibration runs and recomputes both thresholds;
2. recomputes every unit's first alarm from the stored CUSUM paths;
3. resamples the units.

This carries the threshold uncertainty into the interval. α = 0.05, two-sided (OD-13).

**Minimum meaningful difference.** δ = 0.02 in detection power: two more timely detections per 100 diverging loops at the same false-alarm rate. It is nonzero and fixed before any held-out data, as OD-13 requires. The owner should confirm it (§5.4).

**Window.** W = 5 makes the window symmetric with the 5-round early-alarm tolerance already in the development code. The author saw the development dependence on W before choosing it (§5.1), and S1 reports W = 3, 10 and 20.

### 3.4 Must-not-alarm control: the exo world (C4)

* **Arm:** 1000 drawn `exo` worlds: drawn geometry, no gaming, no divergence by construction.
* **Statistic:** the proportion of runs in which prov alarms within 80 rounds at the aligned threshold. bbsd is reported beside it as a paired difference.
* **Registered limit:** Wilson 95 % upper bound ≤ 0.10.
* **Expectation from development:** both detectors fail. In the designed exo world, prov alarmed in 0.535 [0.466, 0.603] of runs and bbsd in 0.53 [0.461, 0.598] (Wilson; `outputs/power_plan.json`).
* **Role:** gating for H-div only (§4.3).

### 3.5 Localisation against the intervention rival, at matched cost (H-loc)

**Unit.** A diverged `conf` unit.

**Localisers.**
* **Provenance** (development rule): at div + 10, name the channel with the largest input-mean shift signed along the published outputs.
* **Intervention** (the native causal rival):
  * For 6 rounds from div + 2, flip the sign of each published coordinate at random. The flips come from the flip generator.
  * The probed trajectory shares the world's random numbers until the flips act.
  * Name the channel whose input-mean level, measured against the 3 rounds before probing, correlates most strongly in absolute value with its flips.

**Endpoint.** Accuracy is the rate of naming G. Δ_loc = acc_prov − acc_intervention, with a paired unit bootstrap 95 % interval (no thresholds are involved). δ_loc = 0.05.

**Matched cost.**
1. Same observation window: both localisers decide with data up to div + 10.
2. Decision cost: the intervention's cost in target accuracy, paired by common random numbers. It is the mean over probe rounds of unprobed minus probed target accuracy. The registered ceiling is a 95 % upper bound ≤ 0.01. Provenance costs nothing by construction.

**Timing caveat.** Both localisers are given div (oracle timing, as in development), so the study scores localisation given that divergence occurred. S13b repeats the comparison with alarm-triggered timing.

### 3.6 Rivals for detection

| detector | what it is | role |
|---|---|---|
| bbsd | the shift in the mean deployed score θ·x (development) | the primary rival |
| BBSD-n (`prov_theta`) | the input-mean drift projected on θ/‖θ‖ only | BBSD on prov's footing; prov's only extra ingredient over it is the second published output |
| inshift | the squared norm of the input-mean shift (development) | the generic input-drift rival |
| pf_twin | max of the projections on θ and top2(θ), computed from θ alone | the provenance-free twin; identical by construction here (C5) |
| prov_shuf | prov with the published outputs' channels permuted | must-fail ablation (shuffled annotations) |
| prov_abl | prov on random directions of the same sparsity | must-fail ablation (development) |

Every secondary contrast uses the same endpoint, window, thresholds, interval method and δ as the primary.

### 3.7 Exclusions and missing data

* There are no exclusions beyond non-diverged units, which are counted.
* A missing or malformed registered quantity or sensitivity cell gives NOT DECIDABLE. It never passes (OD-13).
* A crash of the frozen procedure gives VOID. The generated worlds still count as exposed.

---

## 4. Registered rules

### 4.1 H-det: verdict, evaluated in order (the first matching row decides; every REDUCES route that applies is listed)

| step | condition | verdict |
|---|---|---|
| 0 | the frozen procedure cannot score; a hash mismatch; the equivalence check fails (C10) | VOID |
| 1 | C1, C2 or C6 fails; C5 finds a difference (a code fault); any registered cell is missing | NOT DECIDABLE |
| 2 | U < 0 | FAIL (prov is worse than BBSD) |
| 3 | 0 ≤ U < δ | **REDUCES (to BBSD)** |
| 4 | U ≥ δ and (L ≤ 0 or Δ̂ < δ) | NOT DECIDABLE |
| 5 | (L > 0 and Δ̂ ≥ δ), and the prov − BBSD-n contrast has U < δ | REDUCES (to normalised BBSD) |
| 6 | as above, and the prov − inshift contrast has U < δ | REDUCES (to the input-drift detector) |
| 7 | as above, and the prov − prov_shuf or prov − prov_abl contrast has U < δ (C3) | REDUCES (to a generic sparse projection: the published directions are unnecessary) |
| 8 | a contrast in steps 5–7 is indeterminate (U ≥ δ and (L ≤ 0 or estimate < δ)) | NOT DECIDABLE |
| 9 | Δ̂ ≤ 0 in any gating sensitivity cell (§4.5) | NOT DECIDABLE (estimator-dependent) |
| 10 | otherwise | **RESULT** (shift reading) |

**Always appended when C5 holds (expected): "provenance record: REDUCES (structural) to pf_twin".**

**Error rates.** RESULT requires every contrast to pass. This is an intersection–union test, so the secondary contrasts do not inflate the false-RESULT rate above α.

### 4.2 H-loc

| condition | verdict |
|---|---|
| the frozen procedure cannot score | VOID |
| C9 fails (the intervention rival does not work in clean worlds), or a cell is missing | NOT DECIDABLE |
| U_loc < 0 | FAIL |
| 0 ≤ U_loc < δ_loc, and the intervention's cost upper bound ≤ 0.01 | **REDUCES (to intervention)** |
| 0 ≤ U_loc < δ_loc, and the intervention's cost upper bound > 0.01 | NOT DECIDABLE (accuracy tied at unmatched cost; the cost difference is reported) |
| L_loc > 0 and Δ̂_loc ≥ δ_loc | RESULT |
| otherwise | NOT DECIDABLE |

**P17 negative witness (C8b), recorded whatever the row above says.** In the open-loop worlds no output re-enters the inputs. If provenance still names G at a rate of at least its paired loop-world rate minus 0.10, the following is recorded as **FAIL for the causal reading of P17**: "provenance localisation does not distinguish re-entry from alignment".

### 4.3 H-div

H-div takes H-det's verdict if C4 passes. If C4 fails, H-div is **FAIL (divergence reading)**, whatever H-det's verdict. The registered expectation is FAIL. It is recorded as its own ledger row, not dropped.

### 4.4 Controls

| ID | arm | statistic | registered expectation | if violated |
|---|---|---|---|---|
| C1 positive (instrument) | `clean` | timely rate; divergence rate | proxy and calib ≤ 0.10 (the world hides the Goodhart failure from proxy monitors); prov and bbsd ≥ 0.90; ≥ 95 % of units diverge | NOT DECIDABLE |
| C2 matched false-alarm rate | `far` | alarm rate | prov, bbsd, BBSD-n and inshift each in [0.02, 0.08]; \|FAR_prov − FAR_bbsd\| ≤ 0.03 | NOT DECIDABLE |
| C3 must-fail ablations | `conf` | prov − prov_shuf, prov − prov_abl | L > 0 and estimate ≥ δ (development prov − prov_abl at W = 5: 0.50) | REDUCES (step 7) |
| C4 must-not-alarm | `exo` | prov alarm rate | Wilson upper bound ≤ 0.10. **Expected to fail** (development 0.535) | H-div FAIL |
| C5 provenance-free twin | all | pf_twin vs prov, \|difference\| ≤ 1e−12 in every round of every unit | identical (by construction) | NOT DECIDABLE (code fault); identity holding gives the structural REDUCES line |
| C6 completeness | all | all cells present; 6200 diverged within the cap; no NaN after round 0 | complete | NOT DECIDABLE |
| C7 confounder on the published support (SF3) | `sf3` | prov − bbsd | not significantly positive (L ≤ 0) | recorded; the mechanism statement in §6 is then wrong, and the RESULT wording names a general speed edge |
| C8a open loop, detection (SF5) | open loop, paired with `conf` | (prov − bbsd)_loop − (prov − bbsd)_open | 95 % interval inside (−δ, δ) | if inside: recorded line "the edge is not loop-specific" |
| C8b open loop, localisation (SF5) | open loop | rate of naming G, per localiser | provenance ≥ its loop rate − 0.10 (it cannot tell re-entry from alignment); intervention ≤ 0.25 (chance 0.125) | the provenance line is §4.2's negative witness; intervention > 0.25 gives H-loc NOT DECIDABLE (the rival is not measuring re-entry) |
| C9 intervention works | `clean` | intervention localisation accuracy | ≥ 0.90 (development 0.975–0.98) | H-loc NOT DECIDABLE |
| C10 equivalence | — | `geom=None`, no probe reproduces `loopworld.simulate` | identical arrays | VOID |

### 4.5 Sensitivity table (every cell is computed; a missing cell gives NOT DECIDABLE)

**Roles.** In a "gating" cell, RESULT requires Δ̂ > 0. A "descriptive" cell is reported beside the verdict.

| ID | what changes | role |
|---|---|---|
| S1a / S1b | window W = 3 / W = 10 | gating |
| S1c | window W = 20 ("eventual detection") | descriptive |
| S1d | early-alarm tolerance 3 / 8 rounds | descriptive |
| S2 | the continuous development score, 1 − delay/80 | gating |
| S3a / S3b | false-alarm rate 0.01 / 0.10 | gating |
| S4 | magnitude tertiles | descriptive |
| S5 | support size k ∈ {1–2, 3–5, 6–8} | descriptive |
| S6 | the confounder's energy on the published top-2 support at onset (tertiles), and the slope of the per-unit contrast on the energy off that support | descriptive. Ordinary-model expectation: Δ falls as energy on the support rises |
| S7 | gaming target θ / e | descriptive |
| S8 | the designed (development) geometry on fresh seeds | descriptive. Re-estimates the development contrast on new seeds, separating seed luck from geometry |
| S9 | drawn gameable channel (G uniform over 8) | descriptive. Tests the designed fact that G, the largest true weight, is always in the published top-2 |
| S10a / S10b / S10c | CUSUM k = 0.25 / k = 1.0 / baseline rounds 1–15 | gating |
| S11 | units-only bootstrap (thresholds fixed) | descriptive |
| S13a / S13b | H-loc with probe length m = 2 / with alarm-triggered timing (probe at bbsd alarm + 2, decision at + 10) | descriptive |

The gating cells are S1a, S1b, S2, S3a, S3b and S10a–c: the estimator constants (R5).

### 4.6 Mapping to Phoenix verdict tokens

| this draft | Phoenix token | note |
|---|---|---|
| RESULT | PASS-0 | capped; engineering; synthetic class |
| REDUCES | REDUCES | |
| FAIL | FAIL | |
| NOT DECIDABLE | NOT DECIDABLE | |
| VOID | VOID | |

The machine verdict is computed from unrounded quantities by the frozen scorer (R15).

---

## 5. Power calculation (`power_plan.py`; output `outputs/power_plan.json`)

### 5.1 Development inputs

All rows are from 200 seeds per world with the designed geometry, at W = 5 unless stated. Intervals are 95 % bootstrap.

| quantity | value |
|---|---|
| timely detection, confounded worlds pooled (n = 400) | prov 0.920, bbsd 0.8675 |
| Δ (prov − bbsd), confounded pooled | **+0.0525 [0.030, 0.0775]**; per world +0.050 [0.020, 0.085] and +0.055 [0.020, 0.090] |
| discordance P(T_prov ≠ T_bbsd) | 0.0625 (p₊ 0.0575, p₋ 0.005); per-unit SD 0.245 |
| dependence on the window, confounded pooled | W = 3: +0.185; W = 10: +0.0225 [0.005, 0.040]; W = 20: +0.0075 [−0.005, 0.020] |
| clean worlds pooled | W = 5: +0.005 [0.000, 0.0125]; W = 3: +0.1175 |
| where the confounded edge comes from | 368/400 both detected (mean delay prov 1.25, bbsd 2.53 rounds; 95th percentile 3 vs 6); 7 detected by prov and missed by bbsd; 2 the reverse (prov early); 22 both early |
| continuous score, confounded pooled | +0.0241 [0.011, 0.037] (clean +0.0107) |
| prov − inshift, confounded pooled | +0.1475 [0.110, 0.185] (clean 0.000) |
| prov − prov_abl, confounded pooled | +0.50 |
| exo world alarm rate | prov 0.535 [0.466, 0.603]; bbsd 0.53 [0.461, 0.598]; paired difference +0.005 [−0.020, 0.030] |
| localisation, confounded pooled | prov 0.9725, intervention 0.9775, event log 0.4825; Δ_loc −0.005 [−0.0275, 0.0175]; discordance 0.05; mean intervention cost −0.0002 |

**What these say before any held-out run.**
1. prov reaches threshold about one round sooner than bbsd **everywhere**, clean worlds included. A short window turns that into a large power difference (W = 3).
2. At W = 5 the clean-world difference nearly vanishes. The confounded-world edge is mostly that same speed advantage, showing up because the confounder lengthens bbsd's delay tail. It is joined by 7 bbsd misses.
3. The edge shrinks to +0.0075 by W = 20, so it is about **earlier** detection, not **more** detection.

### 5.2 Winner's curse and geometry

The development edge was observed in **designed** worlds and reported per world because each interval excluded 0. Two corrections give planning values:

* **Selection.** The per-world continuous estimates had z = 2.78 and 2.18. Given that each was reported because z > 1.96, their conditional maximum-likelihood estimates are 0.021 (from 0.0288; ratio 0.73) and −0.018 (from 0.0193; clipped to 0). The mean ratio, 0.36, applied to the pooled W = 5 estimate gives **S2 = 0.0191**.
* **Geometry.** If the edge beyond the clean-world level scales with the probability that the confounder lies wholly off the published support (0.25 drawn, against 0.857 designed), then 0.005 + (0.0525 − 0.005) × 0.25/0.857 gives **S3 = 0.0189**.

| planning scenario | Δ |
|---|---|
| S1 designed, as observed (optimistic) | 0.0525 |
| S2 selection-corrected | 0.0191 |
| S3 geometry-diluted | 0.0189 |
| S4 clean-world tie | 0.005 |
| design alternative, 2δ | 0.04 |

**Both corrections land just below δ = 0.02.** The honest expectation is an edge at, or slightly under, the meaningful difference.

### 5.3 n

**Decision targets** (normal approximation):
1. If the truth is the clean-world tie (Δ = 0.005), P(REDUCES or FAIL) ≥ 0.90.
2. If the truth is twice the meaningful difference (Δ = 0.04), P(RESULT) ≥ 0.90.

These targets do not depend on the winner's-cursed estimates; the development data supply only the variance.

**Assumptions** (conservative): discordance 0.10 (development 0.0625), and an interval inflation of 1.15 for threshold uncertainty under the two-level bootstrap.

| assumptions | n for target 1 | n for target 2 |
|---|---|---|
| discordance 0.0625, inflation 1.0 | 2918 | 400 |
| discordance 0.10, inflation 1.15 | **6175** | 855 |
| discordance 0.15, inflation 1.15 | 9263 | 1289 |

**Registered: n = 6200 diverged units** (cap 6800 draws). At this n the primary standard error is about 0.0046.

**Monte Carlo outcome probabilities** at n = 6200 (discordance 0.10, inflation 1.15, 20 000 replicates, the §4.1 partition):

| true Δ | RESULT | REDUCES | FAIL | NOT DECIDABLE |
|---|---|---|---|---|
| 0.0525 (S1) | 1.00 | 0.00 | 0.00 | 0.00 |
| 0.04 (2δ) | 1.00 | 0.00 | 0.00 | 0.00 |
| 0.0191 (S2) | 0.42 | 0.02 | 0.00 | 0.56 |
| 0.0189 (S3) | 0.40 | 0.02 | 0.00 | 0.57 |
| 0.005 (S4) | 0.00 | 0.93 | 0.00 | 0.07 |

**The main statistical risk.** If the development-informed planning values are right, the most likely verdict is **NOT DECIDABLE** (about 0.56), with a marginal RESULT about 0.41 of the time. This comes from an effect sitting at the meaningful-difference boundary, not from n. Separating an effect of 0.019 from δ = 0.02 would need about 506 000 units. The study is designed to decide cleanly if the truth is either a tie or a clear edge.

**The n-update rule** (the only change the pilot may make). If the pilot's discordance D exceeds 0.10, n rises in proportion, n = ⌈6175 × D/0.10⌉, capped at 20 000. n never decreases. The pilot cannot change δ, W, the rules, the distribution or the arms.

### 5.4 δ, for the owner to fix before freeze

At the registered n (discordance 0.10, inflation 1.15):

| δ | n for both targets | S2/S3 (Δ ≈ 0.019) outcome | S4 (tie) outcome |
|---|---|---|---|
| 0.01 | 55 574 | RESULT 0.99 | NOT DECIDABLE 0.73 (cannot confirm a tie) |
| **0.02 (proposed)** | 6175 | RESULT 0.40–0.42, NOT DECIDABLE 0.56–0.57 | REDUCES 0.93 |
| 0.03 | 2223 | REDUCES 0.68–0.69, NOT DECIDABLE 0.30–0.32 | REDUCES 1.00 |
| 0.05 | 687 | REDUCES 1.00 | REDUCES 1.00 |

**Why 0.02 is proposed.**
* It is four times the clean-world W = 5 difference (0.005).
* In the continuous score, the README already judged a difference of about 0.01 "practically negligible".
* It is the smallest value at which a tie can be confirmed with affordable n.

**The constraint on choosing.** δ must be fixed on these substantive grounds, not on where the planning scenarios fall. The table is shown so that the trade-off is visible, not so that δ can be picked to produce a verdict.

### 5.5 Precision of the other endpoints (at the registered sizes)

* **H-loc:** standard error about 0.0028 and half-width about 0.0056 (development discordance 0.05). If the development Δ_loc of −0.005 holds, REDUCES (to intervention) is expected decisively.
* **C4:** with 1000 exo units, the Wilson interval at the development rate is [0.504, 0.566], far above the limit of 0.10. At a true 0.05 it would be [0.038, 0.065].
* **C2:** with 1000 aligned runs at 0.05, the interval is [0.038, 0.065].
* **S8:** with 1000 designed units, the standard error is about 0.0077.

### 5.6 CPU cost, and the 2 CPU-day budget

**Basis.** 0.55 CPU-s per simulation: the development run took 20 CPU-minutes for 2200 simulations, and one simulation measured 0.48 CPU-s on 2026-10-09. A probed localisation is a second full simulation. A 1.5× margin is applied.

| run | simulations | CPU-hours | with margin | wall on 4 cores |
|---|---|---|---|---|
| development (200 × 200, for scale) | 2 200 | 0.33 | — | — |
| pre-freeze pilot (§7) | 4 200 | 0.64 | 0.96 | about 0.25 h |
| frozen run (all arms in §2.3, S13 probes on the first 1000 diverged units) | 27 500 | 4.20 | 6.30 | about 1.6 h |
| worst case: n raised to the 20 000 ceiling | +27 600 | +4.22 | +6.33 | +1.6 h |

**Totals:** pilot plus frozen run 7.3 CPU-hours with margin; worst case 13.6.

**The study fits in 2 CPU-days (48 CPU-hours), with about 3.5 times headroom even in the worst case.** It is about 12.5 development-sized runs. No paid compute is needed. OD-12's budget is a limit, not a permission.

**Not yet costed:** storage of per-unit statistic paths (about 12 detectors × 80 rounds per unit, roughly 60 MB as float32). These go under `RUNS/`, with hashes in the receipts (OD-14), not in git.

---

## 6. The adversarial question

> **What ordinary model would produce the same result with no CRR ontology at all?**

**Answer: a matched-filter account of black-box shift detection under strategic classification.** No CRR term is needed. Each step is standard.

1. **The statistic is multi-output BBSD.** Input-mean drift is projected on each published output, and the projections are combined by their maximum: Rabanser et al.'s multiple univariate tests with max/Bonferroni aggregation, in mean-shift form. Monitoring drift on a model's most important features is also routine practice; the prior-art dossier must source it (R10).
2. **The published explanation is a sparse matched filter.** Gaming acts on G, the largest true weight, which is (almost) always one of the top-2 coefficients. Projecting on top2(θ) puts more weight on G than projecting on θ, while the noise per unit direction is the same. The signal-to-noise ratio for gaming therefore rises by ‖θ‖/‖top2(θ)‖.
   * This would explain the clean-world speed edge: prov alarms about one round sooner (§5.1). The BBSD-n rival (§3.6) separates this from bbsd's other implementation differences (raw score, intercept drift).
3. **Sparsity also rejects nuisance outside the support.** A confounder outside the top-2 support has no projection on e. It still projects on θ, which BBSD sees as an early alarm or a delay.
   * This would explain the confounded edge and its dependence on the confounder lying off the support: the designed worlds put it there in about 0.857 of cases.
4. **Localisation:**
   * "the largest drift signed along the published outputs" is the same matched filter used to pick a channel;
   * randomised sign flips are an ordinary randomised experiment (A/B test) that identifies which channel responds to the published output.

**What the ordinary account predicts, and this study measures:**
* the edge falls as the confounder's energy on the published support rises (S6);
* it vanishes, or turns negative, when the confounder lies on that support (C7);
* it weakens when the gameable channel is outside the explanation (S9);
* it is the same whether or not the agent's outputs re-enter its inputs (C8a). The statistic never reads the timing or the response of inputs to outputs. It projects the current drift on the current published directions, and in the open-loop world the gamed drift points almost the same way.

**Is there a result the ordinary account would not produce?** Only a loop-specific edge (C8a failing). By construction the statistic cannot produce one.

**Honest conclusion.** The ordinary account reproduces every RESULT this study can return. The study's value is:
* engineering: does the multi-output projection beat score-only BBSD when the confounder is not placed for it?
* bookkeeping: it closes the PENDING grade in `HEURISTIC/CRR_INFLUENCE_2026-10-08.md` §3.3.

It is not evidence for CRR.

**Outside this study.** A statistic that would be provenance-specific is one that tests whether input changes **follow changes** in the published outputs with a lag: a passive natural experiment on the agent's own output history. Its rival would be the randomised intervention already in this harness. That would be a new study (a P18b) with its own declaration.

---

## 7. Must-pass and must-fail surrogates before any freeze

**When and where.**
* Run after the frozen CPU experiment ends (about 13:30Z), on development seeds only:
  * pilot units 100 000–109 999;
  * aligned runs 200 000–209 999.
* The pilot is about 4200 simulations (§5.6).

**Blinding.**
* The pilot computes, but does not print, the signed primary contrast (prov − bbsd in the drawn `conf` family) or the prov − inshift contrast.
* It prints the discordance D and a commitment, sha256("salt|Δ̂ to 4 decimals"), with the salt held outside the repository and revealed after the frozen verdict.
* C8a is printed only as the loop-minus-open-loop difference.

### 7.1 Must-pass

| ID | check | go criterion | status |
|---|---|---|---|
| MP1 | equivalence with the development harness | identical arrays, 4 worlds | **done**: `outputs/equiv_check.json`, ok |
| MP2 | code paths: drawn geometry, open loop, on-support confounder, drawn G, probes with a separate flip generator | runs to completion | **done**: `outputs/tiny_check.json` (not evidence) |
| MP3 | instrument (`clean`, 200 units) | proxy and calib timely ≤ 0.10; prov and bbsd ≥ 0.90; ≥ 95 % diverge | pending |
| MP4 | threshold stability | thresholds from half of 1000 aligned runs give a false-alarm rate in [0.02, 0.08] on the other half and on 500 check runs, for prov, bbsd, BBSD-n and inshift | pending |
| MP5 | intervention works (`clean`) | localisation ≥ 0.90 | pending |
| MP6 | provenance-free twin | identical in every unit | partly done (10 development units: 4 in `equiv`, 6 in `tiny`); pending at pilot size |
| MP7 | divergence in the drawn `conf` family | ≥ 0.90 of units diverge (else the cap and n plan fail) | pending |
| MP8 | runtime | ≤ 0.8 CPU-s per simulation (else re-cost) | 0.48 measured |

### 7.2 Must-fail

| ID | check | go criterion |
|---|---|---|
| MF1 | aligned world | no run diverges |
| MF2 | ablations in the drawn `conf` family | prov_shuf and prov_abl timely rates below prov's by ≥ δ |
| MF3 | confounder on the published support (C7) | prov − bbsd not significantly positive |
| MF4 | open loop (C8b) | intervention names G at ≤ 0.25 (the rival must fail when nothing re-enters) |
| MF5 | exo-only world | no run diverges. The alarm rate is recorded; about 0.5 is expected, so C4 is expected to fail |

### 7.3 Go / no-go

**GO to freeze** if MP3–MP8, MF1, MF2, MF4 and MF5 pass.

**NO-GO if any of these holds.** Each failure is recorded first (R14), then fixed in development and the pilot rerun; there is no freeze until the pilot is clean.
* A must-pass fails.
* MF1, MF2 or MF5 fails.
* MF4 fails: the intervention rival would not be measuring re-entry.

**Wording only.** If MF3 fails (prov beats bbsd even with the confounder on the published support), the mechanism statement in §6 is wrong. Before freeze, rewrite the RESULT wording to name a general speed advantage. The rules do not change.

**The pilot may raise n** (§5.3) **and nothing else.** It is frozen and run whatever the sealed primary estimate is. The decision to freeze cannot depend on it.

**The divergence reading.** If the pilot's exo alarm rate is at least 0.10, as expected, H-div is kept in the frozen claims so that its failure is recorded as a row (recommended), not removed.

---

## 8. What a RESULT would and would not license

### 8.1 A RESULT on H-det would license

The following statement, at PASS-0 at most (engineering, R6, N0, S2), in this synthetic world class:

> "In a performative-prediction loop where applicants game the largest-weight feature along the published outputs, and a label-consistent exogenous shift of drawn geometry is present, taking the maximum of the input-mean drift projected on each output the agent publishes detects the proxy/target divergence within five rounds, at a matched 5 % aligned false-alarm rate, more often than score-mean BBSD, normalised BBSD and a generic input-drift detector, by at least 0.02 in detection power."

It would also license reporting the sensitivity rows beside that statement, and changing the CRR_INFLUENCE grade for the confounded edge from PENDING to "engineering edge held in a drawn family, credited to the statistic".

### 8.2 It would not license

1. Anything about the truth of CRR or the Empty Centre as ontology (P-G4; `CONSTITUTION/WHAT_CRR_IS_NOT.md`).
2. Value for a **provenance record** as such. The structural reduction to pf_twin (C5) means the record adds nothing a monitor holding θ lacks.
3. **"Divergence detection"** if C4 fails, as expected. prov would then be a shift detector that cannot tell label-consistent change from gaming along the published directions.
4. **Re-entry specificity**, if C8a's interval lies inside ±δ, as expected.
5. Localisation beyond intervention. H-loc is expected to REDUCE. Nor does it license provenance localisation as causal attribution (C8b).
6. Claims about real deployed systems, other explanation types, LLM agents, other gaming models or other world classes.
7. Novelty (N0 until the dossier), or the word "finding" (that requires PASS-2/S3: a replication on a later day or by another person or machine, G7).

### 8.3 The other outcomes

* **REDUCES (to BBSD, or to normalised BBSD).** The confounded edge was a property of the designed geometry. The CRR_INFLUENCE grade for detection becomes NOTHING. The DESIGN grade for the harness and controls stands.
* **REDUCES (to input-drift, or to a generic sparse projection).** As above, naming which rival suffices.
* **NOT DECIDABLE.** Any edge sits at the meaningful-difference boundary, or a control or estimator cell failed. Do not rerun under this ID with a larger n. A new δ, W or n is a new study (R3, R12).
* **FAIL.** prov is worse than BBSD under drawn geometry. This is recorded before interpretation.
* **H-div FAIL (expected).** It is recorded as its own row: the statistic does not separate re-entry from a real exogenous shift that projects on its outputs. README point 3 said the same.

---

## 9. Open decisions for the owner, and what remains before READY_FOR_FIRE

### 9.1 Decisions to take before freeze

| ID | decision | proposed |
|---|---|---|
| D1 | δ | 0.02 (§5.4) |
| D2 | W | 5. Development-informed; disclosed |
| D3 | keep H-div, with C4 gating it | yes, so its expected failure becomes a row |
| D4 | include C7 and C8 (SF3 and the open loop) as frozen arms | yes; about 4500 simulations |
| D5 | draw-block offset | +144 blocks |
| D6 | add a world whose published output is not a function of θ, to make the provenance record identifiable | **no**, not in this study. It changes the world and belongs in a P18b |
| D7 | role separation | the scorer and replicator context should not be the author context (P-G1) |

### 9.2 Remaining for G3 READY_FOR_FIRE

**Prior-art dossier** (R10: fetched and versioned on the day; nothing was fetched for this draft):
* BBSD (Lipton et al. 2018; Rabanser et al. 2019);
* performative prediction (Perdomo et al. 2020);
* strategic classification (Hardt et al. 2016);
* CUSUM (Page 1954);
* importance-weighted drift monitoring;
* matched filtering;
* randomised intervention.

**Code and environment:**
* a frozen runner and scorer built from `provworld_draft.py`, writing the stored statistic paths and computing every cell in §4;
* the environment lock.

**Records:**
* the pilot outputs committed and covered by the freeze hash (R4);
* the R13 prompt-log entry and the R14 agent-log entry for this draft, which were **not** written because the instruction was to edit nothing outside this folder;
* an agent manifest (`AGENT_MANIFEST.yaml` here).

---

## 10. Files in this folder

| file | what it is |
|---|---|
| `DECLARATION_DRAFT.md` | this draft |
| `provworld_draft.py` | the draft world, with drawn geometry, extra detectors, the open loop, the on-support confounder, drawn G, and a separate flip generator; modes `equiv`, `tiny` and `geomstats`, each under 60 CPU-s |
| `power_plan.py` | development re-analysis, winner's-curse corrections, the power grid, n and cost (no simulation) |
| `outputs/equiv_check.json` | MP1: identity with `loopworld.simulate` on 4 development worlds |
| `outputs/tiny_check.json` | MP2: code paths on 6 development units. **Not evidence** |
| `outputs/geom_stats.json` | the declared geometry distribution against a 2-channel support |
| `outputs/power_plan.json` | every number in §5 |
| `AGENT_MANIFEST.yaml` | the agent manifest for this draft |

**Run** (each under 60 s):
* `python3 -I provworld_draft.py equiv | tiny | geomstats`
* `python3 -I power_plan.py`

Use `nice -n 19` and `OMP_NUM_THREADS=1` while another experiment holds the CPU.
