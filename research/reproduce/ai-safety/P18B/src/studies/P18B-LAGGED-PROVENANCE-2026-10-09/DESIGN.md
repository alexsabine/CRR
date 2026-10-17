# P18B-LAGGED-PROVENANCE: design draft for a lagged-response test that needs the agent's own publication record (2026-10-09)

**Status: DESIGN DRAFT for the owner's review. Not a freeze.**
* Nothing is frozen, hashed or anchored. No held-out world exists. There is no ledger row.
* Nothing here is a result. Every number comes from a helper script in this folder, run on development seeds or on a stylised surrogate that does not use the world (§0, §6.1).
* This is the "P18b" that `HEURISTIC/LEDGER.md` row D99 names as the candidate successor to P18-PROV-FLAME.

**Role.** Experimentalist and statistician (`AGENTS/roles/`). The draft was written and checked in one model context. That is not independent review (P-G1).

**Stage.** The provenance-record reading of P17/P18 is at SPARK. This draft says what a FLAME declaration would need, and it gives a forecast of how that declaration would likely fare. It does not declare FLAME.

**The draft in five lines.**
1. **The world change.** The published explanation is no longer a function of θ. A publisher with its own random stream decides when to publish (batched release) and which explanation to publish (a random 2 of the top-K channels, or the deterministic top-2 with probability λ). Only the record of what was published, and when, carries that randomness.
2. **What the record supplies.** It supplies η, the part of what was live that neither θ nor the earlier record predicts. A record-free twin can compute only E[published | θ], and η is independent of everything it holds. The access check in §8 confirms that the draft's twin never reads the record.
3. **A design constraint the surrogate found** (§2.3). Random publication makes re-entry intermittent, and a monitor without the record can see that intermittency. A lag statistic with a model-based standard error alarmed just as often when given a phantom record (0.95). So the world must also contain exogenous intermittency, and the record-specific test must be an exact randomisation test that uses the logged propensities. Such a test carries at most about one bit per publication event.
4. **The primary endpoint** is re-entry attribution: "did my published explanation re-enter my inputs?". It is scored as balanced accuracy at a matched 5 % false-attribution rate, with δ = 0.05. The rivals are the record-free twin, the lag-free projection, the record-shuffled (phantom) ablation and randomised intervention. Detection power at a matched 5 % false-alarm rate is secondary, with δ = 0.02. Both directions are registered.
5. **The forecast** (stylised surrogate, not the world). The record-specific test is valid under every nuisance, but it loses to the record-free jump twin on attribution: balanced accuracy 0.745 against 0.8875. It is far too slow for timely detection (0.03). The most likely verdicts are FAIL for the primary claim and FAIL for detection. The pilot (1.5 CPU-hours) would replace this forecast with numbers from the world.

---

## 0. Inputs, what the author has seen, and compute

| file | sha256 | used for |
|---|---|---|
| `studies/P18-LOOP1-2026-10-08/loopworld.py` | `9c6bed79…f1cc` | the world, fits, CUSUM; imported unchanged by `pubworld_draft.py` |
| `studies/P18-LOOP1-2026-10-08/README.md` | `6e85fce7…1140` | the harness, its localisers and the intervention rival |
| `studies/P18-LOOP1-2026-10-08/loop_contrasts.py` | `4729fe0d…a8df9` | read only |
| `studies/P18-PROV-FLAME-2026-10-09/provworld_draft.py` | `c319289e…2eb12894` | `draw_geometry`, the declared smooth-confounder distribution; imported unchanged |
| `studies/P18-PROV-FLAME-2026-10-09/DECLARATION_DRAFT.md` | `f90d9c08…15a6` | §1.4 (the structural reduction to pf_twin), §2.3 (beacon), §6 (the provenance-specific test) |
| `studies/P18-PROV-FLAME-2026-10-09/outputs/power_plan.json` | `33101d7e…cc7b` | development detection rates in the LOOP1 world (§6.1) |
| `HEURISTIC/EMPTY_CENTRE.md` | `797a4bcd…1a7e` | the question (§2–§3) |
| `HEURISTIC/LEDGER.md` | `3b8cb1c8…2420` | row D99 |
| `EPISTEMIC/GATES.md` | `de80a343…85b4` | G2 identifiability |
| `EPISTEMIC/OWNER_DECISIONS_2026-10-09.md` | `61d8dc68…1629` | OD-12, OD-13 |

Full hashes are in `AGENT_MANIFEST.yaml`. The repository was at commit `b8d2101337bc4be107d096c0d56a5f2c27bb0def` on branch `claude/ecstatic-hawking-26npxo`. Environment: Python 3.11.15, NumPy 2.4.6.

**What the author has seen before writing the design:**
* every P18-LOOP1 and P18-PROV-FLAME development output;
* this folder's checks: `equiv`, `access`, `tiny` and `timing`;
* two stylised surrogates, `outputs/surrogate_check_v1.json` and `outputs/surrogate_check.json`.

**Adaptivity, disclosed.**
* v1 of the helper registered a lag statistic with the standard error max(HC3, model-based floor). Its surrogate showed three things:
  * that form is neither record-specific nor powerful;
  * the model-based form is powerful but not record-specific;
  * the randomisation form is record-specific but slow (§2.3).
* After seeing that, the author:
  * added the exogenous telegraph confounder;
  * made the exact randomisation test the registered record-specific statistic;
  * made attribution, not detection, the primary endpoint.
* The telegraph's distribution (§4.1) was fixed in the v2 code **before** the v2 surrogate was run. It was **not** changed after seeing that the v2 surrogate favours the record-free twin (§10, D2).
* The range of the publication probability q was proposed before any world data existed. §2.4 gives the equal-information reasoning for it.

**Compute used for this draft.** About 1.5 CPU-minutes in all. Every run was at `nice -n 19` with one thread, on development seeds or the surrogate, while a frozen experiment held the four cores. The runs were:
* `equiv`: 5.5 s wall;
* `access`: 5.0 s;
* `tiny`: 9.8 CPU-s;
* `timing`: 1.6 s;
* surrogate v1: 29.7 CPU-s;
* surrogate v2: 26.6 CPU-s;
* the power plan: under 1 s.

No full-size run was made.

---

## 1. The claim in native terms

### 1.1 The question

**The Empty Centre's question:** "which of my own outputs will be in my next inputs, and have I kept the record that lets me tell?" (`HEURISTIC/EMPTY_CENTRE.md` §2).

**P18-PROV-FLAME's diagnosis (§1.4, §6).** In the P18-LOOP1 harness, the published explanation e = top2(θ) is a deterministic function of θ. A monitor with no record (pf_twin) therefore reproduces the provenance statistic exactly, and the record-specific reading reduces structurally.

**The only provenance-specific test** that draft names is lagged response: do input changes **follow** changes in the published outputs? Row D99 records the same conclusion and names this study as the successor.

### 1.2 Native framing (prior art to be fetched; nothing was fetched for this draft)

The claim lives entirely inside existing literatures. Every reference below is cited from memory, is unverified, and must be fetched and versioned before any prior-art or novelty statement (R10).

* **Performative prediction and strategic classification.** The deployed model changes the distribution it is evaluated on: Perdomo, Zrnic, Mendler-Dünner and Hardt 2020; Hardt, Megiddo, Papadimitriou and Wootters 2016. Miller, Milli and Hardt 2020 read strategic classification as causal modelling.
* **Estimating the response of data to deployment by perturbing what is deployed:** the performative-gradient work of Izzo, Ying and Zou 2021; performative power, Hardt, Jagadeesan and Mendler-Dünner 2022.
* **Identification from logged predictions.** Mendler-Dünner, Ding and Wang 2022 ("anticipating performativity by predicting from predictions") is, from memory, the closest known statement of this study's logic. The causal effect of a prediction on outcomes is identifiable from data that include the predictions only if the predictions carry randomness not determined by the features, and only if the predictions are logged.
* **Lagged response with known timing:**
  * Granger 1969;
  * intervention analysis in time series, Box and Tiao 1975;
  * event studies.
* **Exact tests given a known assignment mechanism:**
  * Fisher's randomisation inference;
  * conditional randomisation tests in observational studies (Rosenbaum);
  * the assignment-mechanism framing of Imbens and Rubin.
* **Logged propensities for counterfactual evaluation:** Bottou et al. 2013.
* **Black-box shift detection (the BBSD rivals):** Lipton, Wang and Smola 2018; Rabanser, Günnemann and Lipton 2019.
* **Auto-induced distributional shift:** Krueger, Maharaj and Leike 2020.
* **Motivation only, for randomness in published explanations:** the instability of LIME- and SHAP-type explanations (Alvarez-Melis and Jaakkola 2018; Slack et al. 2020).

**In native terms, the claim is this.** The publisher's randomness is an assignment mechanism with known propensities. The record is the assignment log. The lagged-response test is a randomisation test of "applicants respond to the published explanation", using the logged assignments.

### 1.3 The world change that makes the record necessary

The world is P18-LOOP1 unchanged: d = 8, N = 400 applicants per round, 80 rounds, and a logistic classifier θ refitted on the last 5 rounds of proxy-labelled inputs. Divergence is defined as before and the agent never sees the target. **One thing is new: the publisher** (`publish()` in `pubworld_draft.py`). It runs after each refit, with its own generator.

| step | rule |
|---|---|
| timing | publish with probability q; otherwise the previous explanation stays live (delayed, batched release). Round 0 always publishes |
| content | with probability λ, the deterministic top-2 explanation. Otherwise 2 channels drawn uniformly from the top-K channels by \|θ\|, carrying θ's coefficients |
| family | K ~ U{3, 4, 5}, λ ~ U(0, 0.75), q ~ U(0.25, 1), drawn per unit |
| random stream | each round consumes exactly 2 uniforms and one permutation, whatever is decided, so a phantom record and a probed trajectory keep common random numbers |

**What applicants see.** Applicants on route e respond in round s + 1 to a_s, the normalised live explanation after round s. The gaming rule is P18-LOOP1's: a shift of the gameable channel G along the published direction, ramping in over 8 rounds.

**What the record supplies that θ alone does not.** Write A(θ) and V(θ) for the mean and variance of the normalised published explanation at a publication round. Both are computable from θ and the policy.
* **Record holder.** Its one-step prediction of what is live is q·A(θ_s) + (1 − q)·a_{s−1}. The innovation η_s = a_s − (q·A(θ_s) + (1 − q)·a_{s−1}) has conditional variance v_s = q·V + q(1 − q)(A − a_{s−1})². Both need a_{s−1} (the record) and the realised a_s (the record).
* **Record-free twin.** It holds θ, the inputs and the policy, and it can compute â_t = E[a_t | θ_0..t]. Its reconstruction carries no innovation at all. Whatever it computes is a function of (θ, inputs, policy).

**By construction, a pf_twin cannot reproduce a record statistic.** The publisher's stream is a separate generator that the world never reads, except through applicants on route e.
* In any world where nobody responds to the explanation (routes θ, open and none), the joint law of (θ, inputs) does not depend on the publisher's stream. Every record-free statistic is then invariant to that stream, while η, and every statistic built on it, is not.
* On route e, (θ, inputs) depend on the stream only through the applicants' response, which is the effect under test.
* A twin that reconstructed the record from the inputs' own response would be using the outcome to build the treatment. That is excluded by definition: the twin's reconstruction uses θ and the policy only.

**Checks that this holds in the draft's world** (`outputs/access_check.json`, `outputs/equiv_check.json`; §8 MP1–MP3):
1. **The twin cannot see the record.** The twin's input object `twin_view()` has the keys Xobs, theta, score, proxy, ece and pub, and no record field.
2. **Swapping the record changes only record statistics.** On a fixed trajectory, swapping the stored record for a phantom leaves every record-free statistic byte-identical (proxy, calib, inshift, bbsd, mobbsd, djump, pf_twin, twin_jump), and it changes lag_ri and proj_rec. This held in 4 of 4 development units (routes e, θ, open and none).
3. **Swapping the publisher's stream leaves the world unchanged where nobody responds to the explanation.** The world trajectory is byte-identical on routes θ, open and none, and different on route e, as it should be.
4. **The deterministic publisher (pub = None) is the negative control in which the record adds nothing.** It reproduces `loopworld.simulate` array for array in 5 of 5 worlds. In those worlds η ≡ 0 exactly, every lag statistic is undefined, mobbsd equals proj_rec to 1e−12, pf_twin equals lag_full exactly, and the randomisation p-value is 1.

### 1.4 Why random publication alone is not enough

The surrogates (§2.3) show a mechanism that any design of this kind must face.
* **Random publication makes re-entry intermittent.** When G drops out of the published explanation, gaming on G stops. When G returns, gaming resumes.
* **A monitor without the record sees the jumps.** One that also knows the policy knows that only the explanation varies at random. It can therefore attribute re-entry from the jumpiness alone.
* **The record adds information only through alignment:** the jumps follow the logged publications. Alignment matters only if something else also makes the inputs jump.

So the world adds an **exogenous telegraph confounder**. It is a label-consistent on/off shift of the true inputs on drawn channels, with its own timing. Jumpiness then does not imply re-entry, and the record's alignment information has something to do. How much the record helps should scale with how common and how large that exogenous intermittency is. The design reports this as a registered descriptive dose–response (S-tele and the telegraph strata, §5.4).

### 1.5 Worlds

| world | route | publisher | nuisance | role |
|---|---|---|---|---|
| **main** | e | drawn | drawn (smooth and telegraph, each with probability 1/2) | the record-necessary family; primary and secondary endpoints |
| theta | θ (deterministic output) | drawn, paired with main | paired with main | N2: re-entry, but not through the recorded output; the "no" class for attribution |
| open | fixed top2(β) | drawn, paired with main | paired with main | N3: no re-entry (alignment only); the "no" class for attribution; P17's negative witness |
| det | e / θ / open | deterministic top-2 | drawn | N1: the record adds nothing (structural) |
| nogame | none | drawn | drawn | N4: must-not-alarm and must-not-attribute |
| pos | e / θ / open | K = 3, λ = 0, q = 1 (maximal variation) | none | positive control |
| cal, far | none | drawn | drawn | thresholds and false-alarm validation |

### 1.6 The claims

**H-A (primary; the record is necessary for attribution).** In the main family, a monitor that logs what it published and when, and tests input changes against the unpredictable part of its publications by exact randomisation (passive_ri), attributes re-entry through the explanation with higher balanced accuracy than three comparators, each by at least δ_A = 0.05:
* the record-free twin (twin_jump);
* the lag-free projection on the published output (proj_attr);
* the same test on a phantom record (phantom_ri).

All comparisons are at matched 5 % false-attribution rates.

**H-I (co-registered, tested only if H-A gives RESULT; fixed sequence).** passive_ri is non-inferior to randomised intervention on the published outputs (intervention_ri), within 0.05 in balanced accuracy, at zero intervention cost.

**H-D (secondary; detection).** In the main family, the record-specific lag statistic lag_ri detects the proxy/target divergence in time ([div − 5, div + 5]) at a matched 5 % aligned false-alarm rate. It must do so more often than each of bbsd, mobbsd, proj_rec, djump and pf_twin, and than its phantom, by at least δ_D = 0.02.

**Registered in the other direction.** In N1, N2, N3 and N4 the record must not help:
* the record statistic is equivalent to its phantom (TOST within ±δ);
* it does not beat the record-free twin (upper bound below δ);
* it does not attribute or alarm in no-re-entry worlds beyond the registered limits (§3.4, §5.3).

### 1.7 What CRR contributed, and what it did not

* **Contributed.** The question, and the insistence on the record as first-class state (`EMPTY_CENTRE.md` §3).
* **Not contributed.** The mechanism, the estimator, the identification condition or any predicted outcome. Every one of those comes from §1.2 (§7).
* **No CRR quantity enters any scorer.**

### 1.8 Ceiling

* Engineering. Evidence rung R6 at most (a provisional held-out pass in a synthetic world class).
* N0 until a prior-art dossier exists. S2.
* PASS-0 at most from this study; PASS-2 needs replication (G7).
* Nothing about deployed systems, or about how common random publication is in practice.

---

## 2. Statistics

### 2.1 The record quantities

* a_s, η_s and v_s are as in §1.3.
* The response is y_s = x̄_{s+1} − x̄_s, the change in the mean observed input across the round in which applicants first see a_s.
* σ is the pooled standard deviation of first differences over rounds 1–10.

### 2.2 The record-specific test: exact conditional randomisation (`ri_pvalue`)

**Statistic** at decision round d, over the window s ∈ [d − 10, d − 1]:

T = max_j Σ_s η_{s,j} c_{s,j} / √(Σ_s v_{s,j} c²_{s,j}), where c is y centred within the window.

**Reference distribution.** B = 999 redraws of the publisher's choices and timing inside the window, from the logged policy. θ along the observed path, and the record before the window, are held fixed. The p-value is (1 + #{T_b ≥ T})/(B + 1).

**Validity.** If nobody responds to the explanation, the response series does not depend on the publisher's draws inside the window. Given the response series, the observed (η, v) sequence is then one draw from the redraw distribution, so the test is exact whatever the response does: ramps, jumps, gaming along θ, alignment.
* Surrogate check: yes-rates 0.03–0.035 in no-re-entry conditions.
* Phantom record: 0.05 under re-entry.
* Lead control: 0.0375–0.0475 (`outputs/surrogate_check.json`, attribution).

**Resolution limit.** The evidence is capped at about one bit per publication event when the choice is binary-like (G in or out). A perfectly aligned window of E events cannot reach a p-value much below 2^(−E × entropy). This is standard for randomisation inference, and it is why the same statistic, scanned for detection (lag_ri: the first two moments of this test over 6-round windows, with an aligned-calibrated threshold), is slow.

### 2.3 Why the model-based lag statistic is not record-specific (the design constraint)

**The forms compared:**
* *model-based* lag_mb: the regression t with standard error σ/√Sxx;
* the v1 hybrid, max(HC3, floor);
* *randomisation* lag_ri.

All three are scanned for detection with a threshold set at 95 % on the no-nuisance null of the surrogate.

| form | null, smooth ramp | null, telegraph | route θ (no explanation re-entry) | **phantom record under re-entry** | timely detection, route e | source |
|---|---|---|---|---|---|---|
| lag_ri (randomisation) | 0.0725 | 0.0625 | 0.0625 | **0.045** | 0.03 | v2 |
| lag_mb (model-based) | 0.065 | 0.275 | 0.19 | **0.9475** | 0.7025 | v2 |
| max(HC3, floor) (v1 form) | 0.05 | 0.0925 | 0.065 | **0.15** | 0.175 | v2 |
| v1 runs (no telegraph): lag_ri / lag_mb / hybrid | 0.0575 / 0.0575 / 0.06 | — | — | 0.0625 / 0.9575 / 0.175 | 0.0325 / 0.7375 / 0.2162 | v1 |

**Reading.**
* The only lag statistic with timely power (lag_mb) alarms in 95 % of re-entry runs when it is fed a phantom record. It also alarms in 27.5 % of telegraph runs with no gaming. It is a jump detector, and the realised record is not what gives it power.
* The record-specific form (lag_ri) is valid everywhere and nearly powerless for timely detection.
* No form in this table is both. That is the reason for the changes listed in §0.

lag_mb is kept as a descriptive row, with its phantom, so that the frozen run shows this in the world.

### 2.4 Rivals, with equal information and cost

| monitor | θ history | inputs | policy | record (what, when) | own probe log | changes the world? | intervention cost | endpoints |
|---|---|---|---|---|---|---|---|---|
| **passive_ri / lag_ri** (record) | yes | yes | yes | yes | — | no | 0 | A, D |
| lag_mb (record; descriptive) | yes | yes | yes | yes | — | no | 0 | D |
| **proj_attr / proj_rec** (lag-free projection on the published output) | yes | yes | — | live output only | — | no | 0 | A, D |
| **twin_jump** (record-free twin, attribution): max over the policy's pool channels of Σ(y − ȳ)²/σ² in the window | yes | yes | yes | **no** | — | no | 0 | A |
| **pf_twin** (record-free twin, detection): the lag_mb regression on Δâ | yes | yes | yes | **no** | — | no | 0 | D |
| **mobbsd** (record-free multi-output BBSD): drift projected on θ and on â | yes | yes | yes | **no** | — | no | 0 | D |
| **bbsd**: shift in the mean deployed score | scores | yes | no | no | — | no | 0 | D |
| djump (record-free jump detector): \|second difference\| | — | yes | no | no | — | no | 0 | D |
| **intervention_ri** (the causal rival) | yes | yes | yes | **no publication history** | its own 6 rounds of flips | yes: 6 rounds of overridden, sign-flipped publication | target-accuracy loss (common random numbers); 6 rounds of deliberately misleading publication | A (D descriptive) |
| phantom_ri / lag_ri_ph (record-shuffled ablation) | yes | yes | yes | a phantom record from the policy | — | no | 0 | A, D |

**Equal information.**
* **Same data cut-off.** For attribution, every localiser decides at d = div + 10 with data up to d. The passive window is rounds d − 10 to d − 1. The intervention probes rounds div + 2 to div + 7.
* **Same expected variation.** The q range was proposed so that the expected number of publication events in the passive window, 10 × E[q] = 6.25, matches the intervention's 6 probe rounds.
* **Same inference.** Both use the same exact randomisation inference: redraws of the publisher for the passive monitor, and redraws of the flips for intervention. Neither gets a model-based standard error.
* **Detection.** All detectors see the same trajectory, and each threshold is its 95th percentile peak over the aligned calibration runs.
* **What "needs no record" means for intervention.** It needs no publication history. It does need the log of its own flips, which it generates at decision time.

**Equal compute.** Every passive statistic costs at most 0.05 CPU-s per unit (`outputs/timing.json`: statistics 0.043 s, attribution with B = 999 0.009 s). Intervention needs a perturbed world: in the harness, a second simulation (0.466 s). Storing the record costs 80 × 8 floats and 80 flags per unit.

**Rivals with no attribution rule.** BBSD and multi-output BBSD do not say which output re-entered, so they are detection rivals only.

---

## 3. Endpoints

### 3.1 Unit

**The unit** is one drawn world: a seed, a publisher draw, a nuisance draw and a route, simulated for 80 rounds. All statistics and localisers run on the same trajectory, so contrasts are paired within the unit. Intervention runs on a probed copy that shares the unit's common random numbers until the flips act.

**Who enters which endpoint.**
* Only diverged units with div + 10 < 80 enter attribution.
* Only diverged units enter detection.
* Other units are counted and reported.

### 3.2 Primary endpoint: re-entry attribution (H-A, H-I)

**Question and timing.** At d = div + 10, each localiser answers "did my published explanation re-enter my inputs?". Timing is oracle, as in P18-LOOP1 and P18-PROV-FLAME. S-alarm uses alarm-triggered timing.

**Truth.** Yes for route e. No for routes θ and open.

**Decision rules (each at a matched 5 % false-yes rate):**
* passive_ri and intervention_ri: p < 0.05. The test is exact, so the false-yes rate under no re-entry is at most 0.05 by construction.
* twin_jump and proj_attr: the score exceeds its 95th percentile over the `calA` runs, which have no gaming, drawn nuisance and drawn publisher, at decision rounds drawn uniformly from 31–69.

**Unit of the endpoint: balanced accuracy.** BA = ½[P(yes | route e) + P(no | route θ or open)], a proportion where chance is 0.5. It is computed over the attribution mix: route e : θ : open = 2 : 1 : 1 diverged units, with θ and open index-paired to route e.

**Contrasts:**
* A2 (primary): passive_ri − twin_jump.
* A3: passive_ri − proj_attr.
* A4: passive_ri − phantom_ri.
* A1 (H-I): passive_ri − intervention_ri.

**Interval.** A two-sided 95 % percentile interval from a stratified paired bootstrap, B = 4000. Units are resampled within the route-e and non-e strata. For twin_jump and proj_attr, the `calA` runs are resampled too and their thresholds recomputed, which is the two-level bootstrap of P18-PROV-FLAME §3.3. α = 0.05 (OD-13).

**Minimum meaningful difference: δ_A = 0.05 in balanced accuracy.** That is 5 more correct answers per 100 units at equal class weight. It is the same δ as P18-PROV-FLAME's localisation endpoint, fixed before any world data and nonzero. The owner should confirm it (§10, D1).

### 3.3 Secondary endpoint: detection power at a matched false-alarm rate (H-D)

**Endpoint.** T_ik = 1 if the first alarm a_ik of detector k satisfies div_i − 5 ≤ a_ik ≤ div_i + 5. An alarm more than 5 rounds early counts as a false alarm; none, or a later one, is a miss.

**Matched false-alarm rate.** Each threshold is the ⌈0.95 × 2000⌉-th smallest per-run peak over the 2000 `cal` runs: the CUSUM peak for CUSUM detectors, the scan peak for lag statistics. The rate is validated on 1000 `far` runs.

**Contrasts.** Δ_k = mean(T_lag_ri − T_k) over diverged main units, for each rival k.

**Interval.** The two-level paired bootstrap of P18-PROV-FLAME §3.3 (resample `cal`, recompute thresholds, recompute alarms from stored paths, resample units), B = 4000.

**Minimum meaningful difference: δ_D = 0.02,** two more timely detections per 100 diverging loops. It is the same as P18-PROV-FLAME, for comparability.

### 3.4 The other direction

**Attribution.** Each check is a control with a registered limit, not a hypothesis that can yield RESULT (§5.3):
* passive_ri's false-yes rate on routes θ and open, and in nogame at random decision rounds: each Wilson 95 % upper bound ≤ 0.10;
* phantom_ri's and lead_ri's balanced accuracy in the main mix: 90 % interval inside 0.5 ± 0.05;
* in the det mix, passive_ri − twin_jump has an upper bound below δ_A (passive_ri's p-value is 1 by construction there, so its balanced accuracy is 0.5).

**Detection:**
* in theta, open and nogame, lag_ri − lag_ri_ph has a 90 % interval inside ±δ_D;
* lag_ri − pf_twin has an upper bound below δ_D;
* lag_ri's alarm rate in nogame has a Wilson upper bound ≤ 0.10 (C4).

**How much these checks prove.** In N1–N3 most of them hold by construction (exchangeability of the real and phantom records when nobody responds to the explanation). They are instrument checks. A failure means a code fault or a leak, not evidence about the record.

### 3.5 The intervention's cost

**Measure.** The mean over probe rounds of unprobed minus probed target accuracy, paired by common random numbers, reported with a 95 % interval.

**Effect on H-I's wording.** If its upper bound is ≤ 0.001, H-I's wording must add: "the intervention it matches costs under 0.001 in target accuracy in this world, so the saving is negligible here".

**The other cost: six rounds of misleading publication.** It is not captured by accuracy, and it is stated in words.

---

## 4. Drawn world geometry and the beacon rule

### 4.1 Declared distributions (all drawn per unit from generators separate from the world generator)

| component | distribution | generator |
|---|---|---|
| publisher | K ~ U{3, 4, 5}; λ ~ U(0, 0.75); q ~ U(0.25, 1) | `pubpar` |
| publisher stream | 2 uniforms and 1 permutation per round | `pub` |
| smooth confounder | present with probability 1/2; P18-PROV-FLAME §2.1 exactly (support k ~ U{1..8}, isotropic direction on the support, magnitude log-uniform on [0.75, 3.0]); onset τ_x ~ U{15..39} and a 10-round ramp from the world generator | `nuis` |
| telegraph | present with probability 1/2; support k ~ U{1..8} uniformly without replacement (G and the pool can be included); direction N(0, I_k) normalised; magnitude log-uniform on [0.2, 1.0]; switching probability per round ~ U(0.1, 0.5); starts off; the whole path is drawn at unit start | `nuis` |
| route | main: e. theta and open: index-paired copies of main | — |
| phantom record | the policy rerun with an independent stream on the observed θ path | `phantom` |
| flips | intervention probes | `flip` |
| randomisation redraws | B = 999 per decision | `ri` |

**Why the telegraph magnitude range is [0.2, 1.0].** At full ramp, the mean gaming shift on G is 1.8 × a_G, about 1.3. Near divergence, the ramp is about 1/4–1/2, so the shift is about 0.3–0.7. The telegraph range spans exogenous jumps from below to above the re-entry jumps that the attribution window sees. It was fixed before the v2 surrogate ran (§0).

### 4.2 Draw rule (beacon; as P18-PROV-FLAME §2.3)

**Draw height.** `DRAW_BLOCK_HEIGHT` is fixed in the frozen file as the Bitcoin chain tip at freeze plus 144 blocks. The tip height read, and the UTC time it was read, are written into the file.

**Anchor checks.** A1–A9 as in P18-PROV-FLAME §2.3:
* the frozen folder is unchanged;
* an OpenTimestamps proof for FREEZE.json, confirmed by two explorers;
* the attestation plus 7200 s precedes now;
* the date rule A5: on or after max(2026-10-10, freeze date + 1), because the design was chosen on development data on 2026-10-09 (R3);
* the clone is not shallow, with a single freeze commit;
* the draw block has 6 or more confirmations, with the same hash from both explorers;
* no draw has started;
* A9: the earliest attestation of FREEZE.json is at a height strictly below `DRAW_BLOCK_HEIGHT`. Otherwise the study is NOT DECIDABLE under this ID.

**Keys.** fc is the freeze commit and bh the draw block's hash. The domain tag `p18b` is fixed.
* unit seed: s(tag, i) = 1 000 000 + int(sha256("fc|bh|p18b|tag|i")[:15], 16). The draw asserts that seeds are unique.
* generators: `default_rng(int(sha256("fc|bh|p18b|<purpose>|tag|i")[:16], 16))`, where the purpose is one of `pubpar`, `pub`, `nuis`, `phantom`, `flip` or `ri`. The bootstrap generator uses purpose `boot` with i = 0.

These are `unit_seed` and `gen` in `pubworld_draft.py`. The development checks used the dummy strings `DEVELOPMENT-ONLY` and `NOT-A-BLOCK-HASH`, never a block hash.

### 4.3 Arms (planning sizes; §6.2 gives the n-rules)

| tag | world | units | role |
|---|---|---|---|
| `cal` | no gaming, drawn nuisance, drawn publisher | 2000 | detection thresholds |
| `calA` | as `cal`, decision round ~ U{31..69} | the `cal` runs | attribution thresholds for twin_jump, proj_attr and passive_mb |
| `far` | as `cal` | 1000 | C2 |
| `main` | route e, drawn | draw in index order until n_main diverged (planning 6000; cap 15 000; draw cap ⌈n_main / (pilot divergence rate − 0.05)⌉) | H-D; source of the route-e attribution units |
| `theta`, `open` | index-paired with main i < 2000 | 2000 each | N2, N3; the non-e attribution class |
| attribution mix | first n_A/2 diverged main units; first n_A/4 diverged theta and open units each; all with probes | planning n_A = 2000 | H-A, H-I |
| `det` | deterministic publisher; route e 1000, theta 500, open 500 | 2000 | N1 |
| `nogame` | drawn nuisance, no gaming | 2000 | N4; C4 |
| `pos` | maximal publication variation, no nuisance; route e 500, theta 250, open 250; probes | 1000 | C1, C9 |
| sensitivity arms | §5.4 | 1000 each | descriptive |

**Stopping.** The stopping rule depends only on whether a world diverges, which no statistic influences. If the draw cap is reached first, the study is NOT DECIDABLE.

### 4.4 Why development worlds cannot leak into the held-out family

1. **The seeds are disjoint.** Every development seed used or planned is below 10⁶:
   * P18-LOOP1: 0–199 and 10 000–10 199, plus their +17 offsets;
   * P18-PROV-FLAME: 500–511, 20 000–20 005, and its planned pilot at 100 000–209 999;
   * this folder's checks: 300 000–300 003, 310 000–310 005, 320 000–320 006 and 330 000;
   * this study's planned pilot: 340 000–399 999.

   The surrogate uses generator seeds 424 242, 424 243 and 7, and simulates no world. Every held-out seed is at least 10⁶, from a 60-bit hash range with the `p18b` domain tag.
2. **The seeds are unknowable at freeze.** The block hash is about 144 blocks ahead, and A9 proves the order. `freeze_prereg.py` refuses refreeze, so one block cannot be tried against several freezes.
3. **The generators are separate.** Publisher parameters, the publisher stream, nuisance, phantom, flips and redraws each come from their own hashed generator. None is a function of a development seed.
4. **The thresholds are fresh.** `cal` is drawn from the beacon, and no development threshold is reused.
5. **The code is frozen and checked.** The frozen runner must pass MP1, equivalence with `loopworld.simulate`, again at run time (C10).
6. **The pilot is isolated.** It uses development seeds and seals the primary contrasts. It can only raise n (§6.4).

**Not leakage, but adaptivity** (§0): every design choice was made by an author who had seen development and surrogate outputs. That can bias the design toward or against the record. It cannot make held-out worlds equal to development worlds.

**Residual risks.** These are as in P18-PROV-FLAME: a miner withholding a block (no plausible incentive here), and an operator abandoning the study after seeing the block (mitigated by pushing the freeze and its proof before the block, and by OD-11).

---

## 5. Registered rules

### 5.1 H-A (primary). Evaluated in order; the first matching row decides

| step | condition | verdict |
|---|---|---|
| 0 | the frozen procedure cannot score; a hash mismatch; C10 (equivalence) fails | VOID |
| 1 | C1, C2, C5, C6 or C9 fails; a registered cell is missing | NOT DECIDABLE |
| 2 | a control in the other direction fails (C3a, C3b or C3c: the record "helps where it cannot", or the randomisation test is not exact as built) | NOT DECIDABLE (instrument) |
| 3 | A2: U < 0 | **FAIL** (the record-based monitor attributes worse than a record-free monitor that knows the policy) |
| 4 | A2: 0 ≤ U < δ_A | **REDUCES** (to the record-free twin) |
| 5 | A2: U ≥ δ_A and (L ≤ 0 or Δ̂ < δ_A) | NOT DECIDABLE |
| 6 | A2 passes (L > 0, Δ̂ ≥ δ_A); A3: U < 0 → FAIL (worse than the lag-free projection); 0 ≤ U < δ_A → REDUCES (to the lag-free projection); indeterminate → NOT DECIDABLE | as stated |
| 7 | A4 (ablation): U < δ_A → REDUCES (the realised record is unnecessary); indeterminate → NOT DECIDABLE | as stated |
| 8 | Δ̂ ≤ 0 for A2 in any gating sensitivity cell (§5.4) | NOT DECIDABLE (estimator-dependent) |
| 9 | otherwise | **RESULT** |

**Multiplicity.** RESULT requires A2, A3 and A4 to pass. This is an intersection–union test, so the secondary contrasts do not inflate the false-RESULT rate.

### 5.2 H-I (tested only after an H-A RESULT; fixed sequence, so the family-wise α stays 0.05)

| condition | verdict |
|---|---|
| C9 fails (intervention does not work in `pos`) | NOT DECIDABLE |
| L_A1 > −δ_A | **RESULT** (non-inferior to intervention, at zero intervention cost; the cost wording of §3.5 applies) |
| U_A1 < −δ_A | **FAIL** (inferior to intervention) |
| otherwise | NOT DECIDABLE |

If H-A is not RESULT, the A1 estimate and interval are still reported, labelled as outside the confirmatory sequence.

### 5.3 H-D (secondary; its own ledger row; α = 0.05)

| step | condition | verdict |
|---|---|---|
| 0 | as H-A step 0 | VOID |
| 1 | C1, C2, C5 or C6 fails; a missing cell | NOT DECIDABLE |
| 2 | C3d, C3e or C4d fails (the other direction, §3.4) | NOT DECIDABLE (instrument) |
| 3 | lag_ri − pf_twin: U < 0 → FAIL; 0 ≤ U < δ_D → REDUCES (to pf_twin); indeterminate → NOT DECIDABLE | as stated |
| 4 | the same rule against bbsd, mobbsd, proj_rec and djump, in that order: any U < 0 → FAIL (worse than that rival); any 0 ≤ U < δ_D → REDUCES (to it) | as stated |
| 5 | lag_ri − lag_ri_ph: U < δ_D → REDUCES (the realised record is unnecessary) | as stated |
| 6 | Δ̂ ≤ 0 in a gating cell | NOT DECIDABLE |
| 7 | otherwise | RESULT |

**Descriptive row, always reported:** lag_mb against the same rivals and against lag_mb_ph. The registered expectation is that lag_mb − lag_mb_ph has U < δ_D: lag_mb REDUCES to its phantom (§2.3).

### 5.4 Controls

| ID | arm | statistic | registered expectation | if violated |
|---|---|---|---|---|
| C1 positive (instrument) | `pos` | proxy and calib timely rate; divergence rate; passive_ri sensitivity and false-yes rate | proxy and calib ≤ 0.10; ≥ 95 % diverge; passive_ri sensitivity ≥ 0.80 and false-yes ≤ 0.10 | NOT DECIDABLE |
| C2 matched false-alarm rate | `far` | alarm rate per detector | each in [0.02, 0.08] | NOT DECIDABLE |
| C3a record-shuffled ablation | main mix | phantom_ri BA | 90 % interval inside 0.5 ± 0.05 | NOT DECIDABLE (H-A) |
| C3b lead (placebo in time: a publication cannot move inputs observed before it) | main mix | lead_ri BA | 90 % interval inside 0.5 ± 0.05 | NOT DECIDABLE (H-A) |
| C3c exactness under no re-entry | theta, open, nogame | passive_ri yes-rate | each Wilson upper bound ≤ 0.10 | NOT DECIDABLE (H-A) |
| C3d detection phantom equivalence | theta, open, nogame | lag_ri − lag_ri_ph | 90 % interval inside ±δ_D | NOT DECIDABLE (H-D) |
| C3e record does not help where it cannot | det mix; theta; open | passive_ri − twin_jump (det); lag_ri − pf_twin (theta, open) | U < δ (expected by construction) | NOT DECIDABLE (instrument) |
| C4d must-not-alarm | nogame | lag_ri alarm rate within 80 rounds | Wilson upper bound ≤ 0.10. Surrogate 0.065; P18-LOOP1's prov failed the analogue at 0.535 | NOT DECIDABLE (H-D) |
| C4l must-not-alarm, level rivals | nogame | bbsd, mobbsd, proj_rec, djump alarm rates | recorded; expected to fail as in P18-LOOP1 | recorded |
| C5 no access | every unit in theta, open and nogame; the first 200 main units | record-free statistics recomputed with the stored record swapped for a phantom | byte-identical; the world trajectory under a publisher-stream swap is byte-identical off route e (first 200 non-e units, rerun) | NOT DECIDABLE (code fault) |
| C6 completeness | all | cells present; n reached within the caps; no NaN after round 0 in the CUSUM statistics (djump, a second difference, from round 2: clarification of 2026-10-09, §6.4 operator note) | complete | NOT DECIDABLE |
| C8 open loop (P17's negative witness) | open | passive_ri and intervention_ri yes-rates | each ≤ 0.10. Unlike P18-PROV-FLAME's C8b, the lag test is expected to tell re-entry from alignment | recorded; H-A NOT DECIDABLE through C3c |
| C9 intervention works | `pos` | intervention_ri sensitivity (p_e < 0.05 on route e) and false-yes rate | ≥ 0.80 and ≤ 0.10 | H-I NOT DECIDABLE |
| C10 equivalence | — | deterministic publisher, no telegraph, no probe reproduces `loopworld.simulate` | identical arrays | VOID |

### 5.5 Sensitivity table (every cell is computed; a missing cell gives NOT DECIDABLE)

| ID | what changes | role |
|---|---|---|
| S1a / S1b | attribution window 6 / 15 rounds | gating (H-A) |
| S2a / S2b | B = 499 / 1999 | gating (H-A) |
| S3a / S3b | decision time div + 6 / div + 15 | gating (H-A) |
| S4a / S4b | twin_jump and proj_attr calibrated at false-yes 0.01 / 0.10 | gating (H-A) |
| S5 | channel statistic: sum over channels instead of max | gating (H-A) |
| S6a / S6b | detection window W = 3 / 10; S6c W = 20 ("eventual detection") | gating / gating / descriptive (H-D) |
| S7a / S7b | false-alarm rate 0.01 / 0.10 | gating (H-D) |
| S8a / S8b | scan window R = 4 / 10 | gating (H-D) |
| S9 | CUSUM k = 0.25 / 1.0 for level rivals | gating (H-D) |
| S10 | **the four nuisance strata** (none, smooth only, telegraph only, both) | descriptive. Ordinary expectation: A2 is most favourable to the record in the telegraph strata |
| S11 | telegraph magnitude tertiles, and whether the telegraph touches G | descriptive (dose–response) |
| S12 | q, λ and K tertiles (publication-variation energy) | descriptive. Ordinary expectation: passive_ri's sensitivity rises with q and with the entropy of the choice |
| S-tele | arm: telegraph always present and always on G, magnitude drawn | descriptive. The regime where the record should matter most |
| S-designed | arm: development smooth geometry | descriptive |
| S-noise | arm: publication-noise mechanism (continuous perturbation of the published coefficients) | descriptive; implemented 2026-10-09 (`pubworld_draft.py`, kind `noise`; parameters in the §6.4 operator note) |
| S-stale | arm: explanation from a stale model version, top2(θ_{t−L}) with L ~ U{0..5} | descriptive; implemented 2026-10-09 (`pubworld_draft.py`, kind `stale`; parameters in the §6.4 operator note). Expected to carry almost no record information because θ is nearly static |
| S-alarm | attribution at bbsd alarm + 10 (probes at alarm + 2) | descriptive |
| S-probe-det | an always-on probe detector (probe rate 0.25), power and cost | descriptive |
| S-mb | lag_mb and passive_mb with their phantoms | descriptive (§2.3) |
| S-full | lag_full (raw record changes, no twin centring) | descriptive. Exposed to reverse causation (θ responds to the confounder, and the pool follows θ) |
| S-chan | channel naming (G) accuracy for every localiser | descriptive |
| S-boot | bootstrap over units only (thresholds fixed) | descriptive |

**Which cells gate.** The gating cells are the estimator constants (R5). The nuisance and mechanism cells are descriptive, because they change the estimand rather than the estimator.

### 5.6 Mapping to Phoenix verdict tokens

* RESULT maps to PASS-0: capped, engineering, synthetic class.
* REDUCES, FAIL, NOT DECIDABLE and VOID map to themselves.
* The frozen scorer computes the verdicts from unrounded quantities (R15).
* Each of H-A, H-I and H-D gets its own ledger row.

---

## 6. Power and cost (`power_plan_p18b.py`; output `outputs/power_plan.json`)

### 6.1 No development data from the world: what the forecast rests on

**No P18B world run exists.** The planning inputs are of two kinds.
1. **The stylised surrogate** (`outputs/surrogate_check.json`). It has no refits, a fixed θ near 2β, and no applicant heterogeneity. The stylised divergence round is τ + 2, the development median for game_expl: `div − τ` quantiles (0, 10, 50, 90, 100 %) [1, 1, 2, 3, 5] in 200 diverged game_expl runs (`outputs/power_plan.json`, `development_div_minus_tau`).
2. **P18-LOOP1's level detectors in the designed confounded world**: prov 0.920 and bbsd 0.8675 timely at W = 5 (P18-PROV-FLAME `power_plan.json`).

**Surrogate forecasts** (400 runs per condition; route e against route θ, each with drawn nuisance):

| localiser | yes, route e | yes, route θ | yes, no gaming | BA (e against θ) |
|---|---|---|---|---|
| passive_ri | 0.525 | 0.035 | 0.03 | **0.745** |
| twin_jump (record-free) | 0.89 | 0.115 (0.1854 with telegraph, 0.041 without) | 0.05 | **0.8875** |
| phantom_ri | 0.05 | 0.0225 | 0.0325 | 0.5138 |
| lead_ri | 0.0375 | 0.0475 | 0.0475 | 0.495 |

**Detection.** lag_ri is timely in 0.03 of route-e runs (0.795 never alarm). The level detectors were about 0.87–0.92 in P18-LOOP1.

**What these forecast.**
* H-A: A2 ≈ −0.14, giving FAIL.
* H-D: lag_ri − bbsd far below zero, giving FAIL.
* The other-direction controls (C3a, C3b, C3c, C3d) pass.

**The forecast's weaknesses.**
* It is not the world. Refits, applicant heterogeneity and the real divergence timing all differ.
* The nuisance distribution decides how often jumpiness misleads the twin.

### 6.2 n

**Attribution** (balanced accuracy; n/2 units per class).
* Var(Δ̂) = (D_e + D_n)/(2n) × 1.15², where D_e and D_n are the paired discordances in the route-e and non-e units.
* Decision targets:
  * at a true difference of 0, P(REDUCES or FAIL) ≥ 0.90;
  * at 2δ_A, P(RESULT) ≥ 0.90;
  * for H-I, at 0, P(non-inferior) ≥ 0.90.
* All three need SE ≤ δ_A/3.24.
* **Rule:** n_A = max over A1–A4 of ⌈(D_e + D_n)/2 × 1.3225 × (3.2415/0.05)²⌉, with the D's taken from the pilot and rounded up to 0.05. Floor 2000, cap 6000.

| D_e \ D_n | 0.05 | 0.15 | 0.25 |
|---|---|---|---|
| 0.30 | 973 | 1251 | 1529 |
| 0.45 | 1390 | 1668 | 1946 |
| 0.60 | 1807 | 2085 | 2363 |

The planning discordances are D_e = 0.45 and D_n = 0.15. The surrogate's lower bounds, which assume nested decisions, are 0.365 and 0.08. They give 1668, so **n_A = 2000** (floor), SE = 0.0141.

**Detection.** n_main = max over the gating contrasts of ⌈D × 1.3225 × (3.2415/0.02)²⌉. Floor 6000, cap 15 000.

| D | 0.05 | 0.10 | 0.15 | 0.20 | 0.30 | 0.40 | 0.50 |
|---|---|---|---|---|---|---|---|
| n (tie target) | 1738 | 3475 | 5212 | 6949 | 10 423 | 13 897 | 17 371 |

**The other direction (TOST).** The detection equivalences need 716 / 1432 / 2147 / 3579 units at D = 0.02 / 0.04 / 0.06 / 0.10. The registered 2000 units per arm cover D up to about 0.055. If the pilot's D is larger, those arms rise in proportion, capped at 4000. The attribution equivalences need about 206 units.

**The n-update rule.** This is the only thing the pilot may change. n is raised by the rules above and never lowered. δ, the windows, the rules, the distributions and the arms are fixed.

### 6.3 Outcome probabilities at the planned n (Monte Carlo, 20 000 replicates, normal approximation)

**H-A, A2 (superiority), n_A = 2000:**

| true Δ | RESULT | REDUCES | FAIL | NOT DECIDABLE |
|---|---|---|---|---|
| −0.1425 (surrogate forecast) | 0.00 | 0.00 | **1.00** | 0.00 |
| −0.05 | 0.00 | 0.055 | 0.945 | 0.00 |
| 0 | 0.00 | 0.921 | 0.024 | 0.055 |
| +0.05 (= δ_A) | 0.498 | 0.024 | 0.00 | 0.478 |
| +0.10 (2δ_A) | 1.00 | 0.00 | 0.00 | 0.00 |

**H-I, A1 (non-inferiority):**

| true Δ | non-inferior | inferior | NOT DECIDABLE |
|---|---|---|---|
| −0.2 | 0 | 1.00 | 0 |
| −0.1 | 0 | 0.945 | 0.055 |
| −0.05 | 0.024 | 0.024 | 0.952 |
| 0 | 0.947 | 0 | 0.053 |

**H-D at n_main = 6000.** At D = 0.15 or 0.30 and a true Δ of −0.5, P(FAIL) = 1.00. At Δ = 0 and D = 0.15, P(REDUCES) = 0.913.

**The main statistical risk is not n. It is that the forecast is right:** the most likely verdicts are FAIL (H-A) and FAIL (H-D). If the pilot shows A2 near zero instead, REDUCES is likely. A RESULT needs a true A2 of about 0.1. The surrogate puts that out of reach unless exogenous intermittency is much commoner than the declared distribution makes it (S10, S11, S-tele).

### 6.4 The pre-freeze pilot (development seeds 340 000–399 999)

**Arms** (`outputs/power_plan.json`, `cost.pilot`; 6000 simulations):
* cal 1000;
* far 500;
* main 1500, with probes on the first 400 diverged;
* theta and open 400 each, paired, with probes on 200 diverged each;
* det 300;
* nogame 500;
* pos 300 units with probes (600 simulations).

**What it delivers:**
* the discordances D_e, D_n and D for every gating contrast, which set n;
* the divergence rate, which sets the draw cap;
* MP4–MP6 and MF1–MF6 (§8);
* the runtime;
* the `div − τ` distribution in the P18B world.

**Blinding.**
* The pilot prints D's and a commitment, sha256("salt|signs and estimates of A1–A4 and the H-D contrasts to 4 decimals"). The salt is held outside the repository and revealed after the frozen verdict.
* The control rates (C1, C3, C4, C9) are printed, because go/no-go needs them. They reveal something about the primary, and this is disclosed.

**Cost.** 1.0 CPU-hour, 1.5 with margin; about 0.4 hours wall on 4 cores.

**Pilot-operator note (2026-10-09, written before the full pilot ran; implementation choices, not changes to δ, windows, rules, distributions or arms).**
* **det split.** The pilot's det arm (300) is split route e 150, θ 75, open 75, the §4.3 2 : 1 : 1 mix scaled. `power_plan.json` labels it "route e" only; C3e (det mix) cannot be computed without non-e det units. The total is unchanged. Owner to confirm.
* **S-noise and S-stale parameters** (§5.5, D9, MP10; descriptive arms; not run in the pilot). Both keep the declared timing (q ~ U(0.25, 1); round 0 always publishes) and replace only the content rule.
  * S-noise: content is the deterministic top-2 support of θ_t with coefficients θ_j · exp(s · z_j), z ~ N(0, I₂) per round, s ~ U(0.1, 1.0) per unit.
  * S-stale: content is top2(θ_{max(0, t−L)}), L ~ U{0..5} drawn each round.
  * These ranges were proposed by the pilot's builder before any pilot data existed and are recorded here before the full pilot ran. Owner to confirm.
* **C6.** djump is a second difference, undefined at round 1; C6 checks it from round 2 (wording clarified in §5.4).
* **MP7.** §8.1 says "else the draw cap is re-costed"; §8.3 says any MP failure is NO-GO. The pilot's go/no-go follows §8.3 and reports the re-costed draw cap alongside.
* **MP9** is checked as defined in §8.1 (arms, probes, attribution); C6 is reported as its own control.
* **TOST arm sizes (§6.2).** The registered rule is applied as written: arm size = min(4000, max(2000, n_tost(D))). A version that divides n_tost by the share of the arm entering the contrast (θ and open: diverged units) is reported as an owner option.
* **MF1.** The pilot has no aligned arm; MF1 is evaluated on every no-gaming unit (cal, far, nogame). MF1 and the divergence half of MF5 cannot fail by construction (no gaming means x_obs = x_true).
* **Blinding.** Only the D's rounded up to 0.05, which the n-rules use, are public; raw D's are sealed. The residual leakage through the public control rates (MP4, MF2, MF3) is stated in the public JSON.
* **Commitments.** A rerun archives earlier sealed files rather than overwriting them, so every earlier commitment stays verifiable.
* The pilot's record is `PILOT.md`.

### 6.5 CPU cost against the 2 CPU-day budget (OD-12)

**Basis** (`outputs/timing.json`, measured under load at nice 19):

| step | CPU-s |
|---|---|
| simulation | 0.485 |
| all statistics, with the phantom | 0.043 |
| attribution, B = 999 | 0.009 |
| probed simulation | 0.466 |
| intervention randomisation | 0.003 |

The plan uses 0.6 CPU-s per simulation, all statistics included, with a 1.5× margin.

| run | simulations | CPU-hours | with margin | wall on 4 cores |
|---|---|---|---|---|
| pilot | 6 000 | 1.00 | 1.50 | 0.38 h |
| frozen run (all arms in §4.3 and §5.5) | 28 500 | 4.75 | 7.12 | 1.78 h |
| worst case extra (n_main 15 000, n_A 6000) | +19 250 | +3.21 | +4.81 | +1.2 h |
| scoring (two-level bootstrap, B = 4000) | — | about 0.5 (estimated, not measured) | — | — |

**Totals.** Pilot, frozen run and scoring come to 9.1 CPU-hours with margin. The worst case is 13.9.

**Budget.** **This fits in 2 CPU-days (48 CPU-hours) with 3.4 times headroom in the worst case.** No paid compute is needed. OD-12's budget is a limit, not a permission.

**Not yet costed.** Storage of the per-unit statistic paths, about 10 statistics × 80 rounds per unit, roughly 60 MB as float32. These go under `RUNS/`, with hashes in the receipts (OD-14).

---

## 7. The adversarial question

> **What ordinary model would produce the same result with no CRR ontology at all?**

**Answer: causal inference with a known assignment mechanism.** The publisher's randomness assigns "treatments" (what is published, and when) with known propensities. The record is the assignment log. The lagged-response test is a Fisher randomisation test, an event study with known treatment timing, run on that log. No CRR term is needed at any step.

1. **Identification needs positivity and logging.** The record can help only if the published output varies given θ, and only if what was published is logged. This is the textbook condition for estimating a treatment effect from observational data. It is also, from memory, the identification condition in Mendler-Dünner, Ding and Wang 2022 for the effect of logged predictions. The negative controls N1–N3 are this condition switched off.
2. **The resolution limit is standard.** About one bit per binary assignment is the ordinary resolution of randomisation inference, and it is why passive_ri is slow.
3. **The twin's advantage is ordinary detection theory.** Intermittent re-entry has a signature that needs no log. The log adds alignment, which is worth something only against rival sources of the same signature (the telegraph). Every row of S10, S11 and S-tele is predicted by this account.
4. **The intervention comparison is an ordinary experimental-design trade-off.** Incidental, logged variation costs nothing but is weak and irregular. Designed variation is strong and regular, and it costs an intervention.
5. **The detection result is ordinary.** A model-based standard error is invalid when the response has unmodelled jumps. That is why lag_mb alarms with a phantom record.

**Is there any outcome the ordinary account would not produce? No.** Every registered outcome, in both directions, is entailed by that account together with the declared distributions. The negative-direction controls hold by exchangeability. The size of the record's advantage is set by the nuisance distribution, which is a modelling choice, not a CRR prediction.

**What CRR adds beyond the question: nothing in the mechanism, the estimator, the identification condition or the predicted outcomes.** What it did add:
* **the question**, posed as "which of *my own* outputs are in my next inputs". This treats the agent's own outputs as treatments to be logged;
* **the design rule** "keep the record as first-class state" (`EMPTY_CENTRE.md` §3). Impression and exposure logging, and propensity logging for off-policy evaluation, already do this for recommendations and advertisements. Whether explanation publication is commonly logged in practice is an empirical claim this draft has not checked.

**Honest conclusion.** The study can show only whether, in a synthetic world built so that the record is necessary, a record-holding monitor turns that necessity into better attribution or detection than strong record-free monitors and intervention. A RESULT would be an engineering statement about this world class. A FAIL would say that, here, the record's information is real but too thin (about one bit per publication) to beat a record-free monitor that watches for jumps. Neither outcome is evidence for or against CRR (P-G4).

---

## 8. Must-pass and must-fail surrogates before any freeze

### 8.1 Must-pass

| ID | check | go criterion | status |
|---|---|---|---|
| MP1 | equivalence with the development harness | identical arrays (aligned, game_theta, game_expl, exo, game_expl+exo) | **done**: `outputs/equiv_check.json`, ok |
| MP2 | **the draft's world gives pf_twin no access to the record** | `twin_view` has no record field; a record swap on a fixed trajectory leaves every record-free statistic byte-identical and changes the record statistics; a publisher-stream swap leaves the world byte-identical off route e | **done**: `outputs/access_check.json`, ok (4 development units, routes e, θ, open and none) |
| MP3 | N1 identities | η ≡ 0; lag statistics undefined; mobbsd ≡ proj_rec; pf_twin ≡ lag_full; passive_ri p = 1 | **done**: `outputs/equiv_check.json` |
| MP4 | the randomisation test is exact in the world | passive_ri yes-rate in nogame, theta and open; phantom_ri and lead_ri yes-rates in main: each Wilson upper bound ≤ 0.10 | pending (pilot). Surrogate: 0.0225–0.05 |
| MP5 | positive control (`pos`) | C1 thresholds; passive_ri sensitivity ≥ 0.80 | pending |
| MP6 | intervention works (`pos`) | C9 thresholds | pending |
| MP7 | divergence in main | ≥ 0.80 of units diverge (else the draw cap is re-costed) | pending |
| MP8 | runtime | ≤ 0.9 CPU-s per simulation with statistics | 0.54 measured |
| MP9 | code paths | all arms, probes and attribution run | **done**: `outputs/tiny_check.json` (not evidence) |
| MP10 | S-noise and S-stale implemented and tested | runs to completion; equivalence unaffected | implemented; `outputs/mp10_check.json` ok; recomputed in the pilot (`PILOT.md`) |

### 8.2 Must-fail

| ID | check | go criterion |
|---|---|---|
| MF1 | aligned world | no run diverges |
| MF2 | phantom record (record-shuffled ablation) | phantom_ri BA within 0.5 ± 0.05; lag_ri_ph alarm rate ≤ 0.10 in main |
| MF3 | lead (placebo in time) | lead_ri BA within 0.5 ± 0.05 |
| MF4 | open loop | passive_ri and intervention_ri yes-rates ≤ 0.10 |
| MF5 | nogame | no run diverges; lag_ri alarm rate ≤ 0.10 |
| MF6 | lag_mb with a phantom record under re-entry | phantom alarm rate ≥ 0.50 (the §2.3 non-specificity holds in the world). **Wording only**: if it fails, the S-mb wording changes, not the rules |

### 8.3 Go / no-go

**GO to freeze** if MP1–MP10 and MF1–MF5 pass.

**NO-GO** if any of them fails. The failure is recorded first (R14), then fixed in development, and the pilot is rerun.

**The freeze decision must not depend on the sealed primary estimate or on the forecast.** A design that is frozen only when its forecast favours the claim selects for passes. The forecast in §6.1 is disclosed so that a FAIL, if it comes, is read as the expected outcome it is, not as a surprise.

**The pilot may raise n and nothing else.**

---

## 9. What a RESULT would and would not license

### 9.1 An H-A RESULT would license, at PASS-0 at most (engineering, R6, N0, S2), in this synthetic world class

> "In a performative-prediction loop where applicants game along a published explanation whose content and timing are randomised by the publisher, and where label-consistent exogenous changes of drawn geometry (smooth and intermittent) are present, a monitor that logs what it published and when, and tests input changes against the unpredictable part of its publications by exact randomisation, answers 'did my published explanation re-enter my inputs?' with balanced accuracy at least 0.05 higher than a record-free monitor that knows the publication policy, than a lag-free projection on the published output, and than the same test on a phantom record, at matched 5 % false-attribution rates."

An H-I RESULT would add: "and within 0.05 of a six-round randomised intervention on the published outputs, without intervening". The §3.5 cost wording applies.

An H-D RESULT, unexpected, would license the matching detection statement at W = 5.

### 9.2 It would not license

1. Anything about the truth of CRR or the Empty Centre as ontology (P-G4; `CONSTITUTION/WHAT_CRR_IS_NOT.md`).
2. That a provenance record helps when published outputs are deterministic functions of the model. The opposite is built in (N1).
3. That random or batched publication of explanations is common in deployed systems, or that it is logged.
4. Any claim beyond binary-like publication choices (S-noise and S-stale are descriptive), beyond this gaming model, or beyond these nuisance distributions.
5. Detection, unless H-D also gives RESULT. In particular, nothing about lag_mb, which is not record-specific.
6. P17's broader claims about causal failure and reliable intervention.
7. Novelty (N0 until the dossier), or the word "finding", which needs PASS-2/S3 and replication on a later day or by another person or machine (G7).

### 9.3 The other outcomes

* **H-A FAIL (forecast).** In this family, the record's alignment information, at about one bit per publication, does not beat a record-free monitor that watches publishable channels for jumps.
  * The Empty Centre's design rule then has no engineering value here beyond the question. The CRR_INFLUENCE grade for the "keep the record" rule in a performative loop becomes NOTHING in this world class.
  * The S10, S11 and S-tele rows say whether there is any regime (common, large exogenous intermittency on G) in which the ordering reverses. Those rows are descriptive and cannot be promoted after the fact.
* **H-A REDUCES (to the twin, or to the lag-free projection).** The same reading, with the named rival sufficing.
* **H-A NOT DECIDABLE.** An edge at the boundary, or a failed control. Do not rerun under this ID: a new δ, nuisance distribution or n is a new study (R3, R12).
* **H-D FAIL (forecast).** The record-specific lag statistic is too slow for timely detection. The only fast lag statistic (lag_mb) does not need the realised record.
* **H-I** is not tested unless H-A gives RESULT.

---

## 10. Open decisions for the owner, and what remains before READY_FOR_FIRE

### 10.1 Decisions to take before the pilot or the freeze

| ID | decision | proposed |
|---|---|---|
| D1 | δ_A and δ_D | 0.05 and 0.02 (continuity with P18-PROV-FLAME) |
| D2 | the nuisance distribution (telegraph and smooth presence each 1/2; telegraph magnitude [0.2, 1.0], switching [0.1, 0.5]) | keep as declared. **Do not tune it after the surrogate's forecast.** A change must be argued on grounds independent of the forecast, disclosed, and it makes a new design version (P-G5) |
| D3 | whether to proceed given the forecast | run the pilot (1.5 CPU-hours) to replace the stylised forecast with world numbers. Then freeze if the controls pass, whatever the sealed primary says. The alternative is to keep this as a design record, as D99 did for P18-FLAME. That is the owner's call, but it should not be made conditional on the forecast's direction |
| D4 | primary endpoint | attribution (H-A), with detection secondary (H-D). Reason: §2.3. The only record-specific statistic is too slow for timely detection |
| D5 | the confirmatory sequence | H-A, then H-I (fixed sequence); H-D as its own secondary row |
| D6 | oracle timing for attribution | yes, as in P18-LOOP1 and P18-PROV-FLAME; S-alarm reports alarm-timed attribution |
| D7 | draw-block offset | +144 blocks |
| D8 | role separation | the scorer and replicator contexts should not be this author's context (P-G1) |
| D9 | implement S-noise and S-stale before the pilot | yes (MP10) |

### 10.2 Remaining for G3 READY_FOR_FIRE

**A prior-art dossier** (R10; nothing was fetched for this draft): every item in §1.2, with special attention to identification from logged predictions (Mendler-Dünner, Ding and Wang 2022) and to performative power.

**Code:**
* a frozen runner and scorer built from `pubworld_draft.py`, computing every cell of §5, with stored statistic paths;
* S-noise and S-stale;
* the environment lock.

**Records:**
* the pilot outputs, committed and covered by the freeze hash (R4);
* the R13 prompt-log entry and the R14 agent-log entry for this draft. These were **not** written, because the instruction was to edit nothing outside this folder;
* `scripts/run_final_checks.py`, which was not run because the CPU was reserved.

---

## 11. Files in this folder

| file | what it is |
|---|---|
| `DESIGN.md` | this draft |
| `pubworld_draft.py` | the draft world, v2: publisher, nuisance, routes, probes, every statistic and localiser, and the exact randomisation tests. Modes `equiv`, `access`, `surrogate`, `tiny` and `timing`, each under 60 CPU-s |
| `power_plan_p18b.py` | n-rules, verdict-partition Monte Carlo, TOST n, and cost (no simulation) |
| `outputs/equiv_check.json` | MP1, MP3 |
| `outputs/access_check.json` | MP2: pf_twin has no access to the record |
| `outputs/surrogate_check.json` | v2 stylised surrogate (§2.3, §6.1). **Not evidence about the world** |
| `outputs/surrogate_check_v1.json` | v1 surrogate, kept for disclosure (§0, §2.3); its `never_alarmed` field is wrong, as noted inside it |
| `outputs/tiny_check.json` | MP9: code paths on 19 development simulations (6 calibration runs, 7 units, 6 probed copies). **Not evidence** |
| `outputs/timing.json` | CPU seconds per step |
| `outputs/power_plan.json` | every number in §6 |
| `AGENT_MANIFEST.yaml` | the agent manifest for this draft |

**Run** from this folder:
* `nice -n 19 env OMP_NUM_THREADS=1 python3 -I pubworld_draft.py equiv|access|surrogate|tiny|timing`
* `python3 -I power_plan_p18b.py`

Each run is under 60 CPU-s.
