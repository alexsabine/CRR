# SEC-PG-LLM-H-2026-10-08: preregistration

**Question.** On text it has never seen, does SEC-PG do what the development record says it does with T4's byte-level Transformer learner? SEC-PG is a one-run continual-learning schedule. The registered claim (P1–P5, below) states three things:

* SEC-PG is non-inferior to T4's validation-tuned six-run grid of fixed anchor weights, within 0.005 nats of J pooled over cells;
* it is better than the one-run comparators, SEC v2 and T4's transferred constant;
* its disadvantage against the grid is bounded by 0.01 nats within the 8 M-token stratum and within the width-192 stratum. That is where the development pilot reversed.

**Register.**

* **Layer:** engineering. No CRR content: SEC-PG combines an EWC-style diagonal-Fisher anchor with Gradient Projection Memory (Saha et al. 2021).
* **Specificity:** S0.
* **Novelty:** N0, since the configuration was selected on development data (`DESIGN_NOTE.md`) and every component is published (`prior_art.md`).
* **Usefulness:** U3, an engineering candidate. A RESULT supports at most U4 for J in the tested scope. Run time and memory are reported descriptively and are not claimed: a SEC-PG run costs more than one anchored run, and its GPM bases are a sizeable fraction of the parameter count.
* **Rung:** the frozen scorer prints a verdict word, not a grade. A RESULT can support at most a provisional held-out pass (PASS-0, rung R6) for the claim in the tested class. PASS-1 (rung R7) also needs the conditions listed below and the reviewers' receipts.
* **Robustness** is reported separately: sensitivity, controls, anchoring, rerun, exposure.
* Nothing here bears on CRR.

**Parents.**

* SEC-OBS1-H H1 PASS: the schedule beat the transferred constant on 100 fresh synthetic histories (`RUNS/SEC-OBS1-H-2026-10-08/RESULT.md`).
* The development pilot on T4's 32 cached anchors (`studies/SEC-OBS1-2026-10-08/llm_pilot/`).
* CPU-1 (`studies/SEC-PG-LLM-2026-10-08/cpu1/`), which selected the configuration frozen here under a rule fixed before it ran.
* T4 (`CRR-LLM-CALIBRATION/T4-MATURITY-2026-10-07/`), whose learner, grid, comparators and tolerance are used.

If CPU-1 had printed STOP, this study would not have been frozen (`LLM_NEXT_STEPS.md`, R12). It printed `SELECT all4`.

## Held-out data

T4's texts are in `DATA/SEEN.md`, so this study draws new books. There are three pools, built from Project Gutenberg's catalog metadata only (`pools.json`, written by `build_pools.py`). The catalog's sha256 and fetch time are recorded in `pools.json`; no book text was read.

| pool | rule | size |
|---|---|---|
| EN (domain A, the old task) | Text, language exactly `en`, LoCC PR or PS, "fiction" in subjects | 15,932 |
| FR (half of domain B, the new task) | Text, language exactly `fr`, LoCC PQ, "fiction" in subjects | 1,322 |
| DE (half of domain B) | Text, language exactly `de`, LoCC PT, "fiction" in subjects | 739 |

Every Gutenberg book in `DATA/SEEN.md` is excluded, and so is every work by an author of one (Austen, Melville, Hugo, Goethe, Darwin, Joyce, Dante, Mary Shelley, Conan Doyle, Dickens).

Three of those books (Gutenberg 84, 1661 and 98) were opened by RT1-PR1 on 2026-10-06 but had never been entered in `DATA/SEEN.md`. The second pre-freeze review found them, and they were registered on 2026-10-08, before the pools were rebuilt.

**Draw** (`data_step.py`, whose docstring is the exact rule):

* For pool P and ebook n, the key is sha256(`<freeze commit>|<hash of Bitcoin block 970552>|P|n`).
  * The block height is fixed in the frozen `data_step.py`, about 12 hours ahead of the chain tip at the freeze (tip 970480 at 10:49Z).
  * Its hash could not be known at the freeze and cannot be chosen afterwards.
  * The draw needs at least 6 confirmations of that block, with both explorers agreeing on its hash.
* A candidate already in `DATA/SEEN.md` at draw time is skipped and recorded as "S0 already seen".
* Candidates are fetched in increasing key order until the quota is admitted: EN 2, FR 1, DE 1. There are at most 12 tries per pool; otherwise the verdict is NOT DECIDABLE.
* HTTP 404 or 410 is a rejection.
* Any other HTTP error or network failure is retried (4 attempts). If it persists, the draw stops without deciding that candidate and resumes later. Every attempt is logged as it happens, and recorded attempts are never re-decided.

**Screens**, in order:

* S1: HTTP 200.
* S2: at most 0.1 % replacement characters after UTF-8 decoding.
* S3: the `*** START OF` and `*** END OF` markers are present, in that order.
* S4: stripped size, using T4's `_strip`, is within 300 kB–2.5 MB (EN) or 200 kB–2.5 MB (FR, DE).
* S5: the most frequent lower-case word is in a declared list: EN {the, and, of, to, a, i}; FR {de, la, le, et, les, à, il}; DE {der, die, und, sie, ich, er, das, zu}.

Every fetched file, admitted or rejected, is entered in `DATA/SEEN.md` as LLM-exposed public text. The rows go above the verbatim-import section, where `scripts/seen_register.py` reads them (`data_step.py register`).

**Domains.**

* Domain A is the two EN books concatenated.
* Domain B is the FR book followed by the DE book, as T4 paired a French and a German text.
* T4's split applies unchanged: 20,000-byte chunks; chunk i goes to validation if i mod 10 = 8, to test if i mod 10 = 9, and to development otherwise.

**Seeds.** Eight: 100000 + int(sha256(`<freeze commit>|<hash of block 970552>|seed|i`)[:8], 16) mod 800000, for i = 0…7. They are disjoint from every seed used before (0–12).

## Learner, cells and arms

**Learner.** T4's learner, byte-identical copies in `llm/` (`cl.py`, `model.py`, `data.py`). Only `data.ROOT`, `data.DOMAINS` and the cache path are redirected (`run_heldout.py`). Importing `llm/cl.py` creates an empty `outputs/cache` directory in this folder, as it does in T4's; nothing is written there.

* A pre-LN decoder-only Transformer over bytes: width 64 with 2 layers, or width 128 or 192 with 4 layers; 4 heads; context 128.
* Pretraining on domain A for 1, 2 or 8 M tokens, one run per cell from initialisation: AdamW lr 1e-3, warm-up 100, batch 16.
* At the end of pretraining: the micro-batch diagonal Fisher and SEC's secant `s`. Their estimator constants (window 0.2, 64 micro-batches of 2) are inherited from T4 and shared by SEC v2.
* Task B: 1 M tokens of domain B, AdamW lr 3e-4, with T4's adaptive-metric proximal anchor step.

**Cells.** 8 seeds × 3 widths × 3 maturities = 72.

**Arms per cell** (13 runs):

| arm | definition |
|---|---|
| frozen | the pretrained model |
| none | task B without an anchor |
| grid | T4's six fixed weights λ ∈ {1e3, 2e3, 5e3, 1e4, 2e4, 5e4}, choosing the run with the lowest validation (A_val + B_val)/2, rounded to 5 decimals with ties to the smaller λ (T4's rule) |
| const | the grid's λ = 5e3 run (T4's transferred constant) |
| SEC v2 | λ = α s F, α = 10 |
| **SEC-PG** | `config.json`: anchor SEC's weight × 1/16 (λ = 10 s F/16) throughout task B; GPM update projection from 25 % of task B on all four linear maps of every block (attention in- and out-projections, MLP up- and down-projections), with energy threshold 0.97 and bases from 32 task-A sequences at the anchor; projection is applied to the AdamW update before the proximal step (`sec_pg.py`) |
| light | SEC-PG without GPM |
| pgconst | SEC-PG's GPM schedule with a constant anchor whose λ is the median, over this study's 72 cells, of SEC-PG's own multiplier 10 s/16. It is computed from the pretraining outputs before any task-B run and recorded in `pgconst_lambda.json`. This is the constant SEC-PG's weight reduces to (R7); the scorer re-derives it and checks every unit |
| gpm_only | GPM as published: update projection on the same four maps from the first task-B step, with no anchor |

The configuration is CPU-1's `all4` (`DESIGN_NOTE.md`).

## Metric, unit, statistics

* **Metric:** test J = (A_test + B_test)/2 on T4's fixed evaluation windows (64 windows each from the test slices).
* **Unit:** the seed. The cells of a seed share data order, task-B stream and evaluation windows, and the 1/2/8 M cells are checkpoints of one trajectory.
* **Estimate:** for a difference between arms, each seed's value is its mean over its cells (all nine, or one stratum's three). The estimate is the mean over the eight seeds.
* **Interval:** 95 % Student-t, mean ± t(0.975, 7) × sd/√8 with t = 2.365. A percentile bootstrap over seeds is reported as description only.
* **Book draw:** all cells use one draw of four books. The interval covers seed variation, not variation between books in the pools, so every inference is conditional on the drawn books.
* **Non-finite values:** in SEC-PG or a sensitivity run, a non-finite value is replaced by 10 nats (a loss for the claim) and listed. In any other arm it makes the verdict NOT DECIDABLE.

## The registered claim (all must hold; otherwise FAIL)

| rule | condition |
|---|---|
| P1 | upper bound of mean J(SEC-PG) − J(grid) ≤ +0.005 |
| P2 | mean J(SEC-PG) − J(SEC v2) ≤ −0.005 with upper bound < 0, **and** mean J(SEC-PG) − J(const) ≤ −0.005 with upper bound < 0 |
| P3 | upper bound of mean J(SEC-PG) − J(grid) ≤ +0.01 within the 8 M stratum (averaged over widths), **and** within the width-192 stratum (averaged over maturities) |
| P4 | mean B_test(SEC-PG) ≤ mean B_test(SEC v2), **and** mean A_test(SEC-PG) − mean A_test(grid) ≤ 0.05 (means over cells) |
| P5 | cells no worse than the grid beyond T4's tolerance (J − J_grid ≤ 0.02, A − A_grid ≤ 0.05, B − B_grid ≤ 0.05): SEC-PG at least as many as SEC v2 |

**P5 is one-sided.** T4's declared tolerance is two-sided: it also counts as misses the cells where an arm beats the grid by more than the tolerance.

* On development data the selected configuration met the two-sided form in 5 cells against SEC v2's 12.
* One-sided, the counts are 15 against 12.
* Of the 10 cells the one-sided form adds, 7 are cells where the configuration beats the grid by more than 0.02 in J. In the other 3, only its old-task loss is more than 0.05 below the grid's (`studies/SEC-PG-LLM-2026-10-08/cpu1/cpu1_tolerance.json`). P5 was changed to one-sided before the freeze, and that change was made after those development numbers were seen (`DESIGN_NOTE.md`; `notebook/AGENT_LOG.md`). The two-sided count is reported as description only.

**Admissibility.** A cell is admissible if A_test(none) − A_test(frozen) ≥ 0.10 (forgetting is real) and B_test(frozen) − B_test(none) ≥ 0.5 (task B is learnable). If fewer than 80 % of the 72 cells are admissible, the verdict is NOT DECIDABLE. Every cell is analysed; inadmissible cells are listed.

**Controls:**

| id | kind | condition | if it fails |
|---|---|---|---|
| K1 | positive | mean J(none) − J(grid) ≥ 0.01 with lower bound > 0 (anchoring matters) | NOT DECIDABLE (UNINFORMATIVE …) |
| K2 | instrument | the transferred constant does not meet P1: upper bound of J(const) − J(grid) > 0.005 | P1 cannot separate a one-run constant from the grid; listed as a failed precondition |
| K3 | ablation | upper bound of J(SEC-PG) − J(light) < 0 | REDUCES |
| K4 | must-fail | the light anchor alone does not meet P1–P5 | REDUCES |
| K5 | constant reduction (R7) | upper bound of J(SEC-PG) − J(pgconst) < 0 (the size-matched constant) | REDUCES |
| K6 | reduction to published GPM | upper bound of J(SEC-PG) − J(gpm_only) < 0 | REDUCES |

**Verdict.** `score_llmh.py` computes it, using the words that `scripts/append_result_v2.py` accepts:

1. **NOT DECIDABLE (…)** if any of these holds:
   * the frozen folder changed;
   * the draw failed;
   * a registered unit is missing;
   * an arm other than SEC-PG is non-finite;
   * fewer than 80 % of cells are admissible;
   * K1 fails. The verdict then reads "UNINFORMATIVE" and says whether the claim held.
2. Else **FAIL (…)**, naming the rules not met.
3. Else **REDUCES (…)**, naming the failing controls among K3–K6.
4. Else **RESULT**: the registered claim holds and no reduction was found.

**Sensitivity table** (`config.json`). The four constants of SEC-PG that the selected configuration uses are each moved to two other values, one at a time:

* anchor multiplier 1/32 and 1/8 (it absorbs α, since λ = α s κ F);
* switch point 12.5 % and 50 % of task B;
* GPM energy threshold 0.95 and 0.99;
* basis sample 16 and 64 sequences.

The runner checks that every override changes a parameter the configuration uses. For each of the eight, the claim P1–P5 is recomputed with the perturbed SEC-PG in its place, and a *flip* is a change in whether the claim holds. If the main claim fails, flips are not counted toward anything; variants that meet P1–P5 are listed as exploratory, not as a rescue.

Not swept, with reasons:

* the number of protected maps, a structural choice compared in CPU-1;
* the inherited Fisher and secant estimator constants, which T4 fixed. They are shared with the SEC v2 comparator, and their scale is covered by the anchor multiplier.

**Scorer-computable PASS-1 preconditions.** These are printed and stored, and they are *not a grade*:

* verdict RESULT;
* at most one flip in eight;
* K2–K6 hold;
* at least 80 % of cells admissible;
* a Bitcoin attestation verified for this freeze, with block time + 7,200 s before the first fetch, and the anchor check itself before the first fetch, as recorded in `draw_log.json` at draw time;
* a signed annotated tag on origin at the anchor check, as recorded in `draw_log.json`;
* both rerun units identical to their main units in every field except timings. One rerun unit repeats a width-128 pretraining from scratch.

Outside the scorer, and needed for any grade:

* the reviewers' receipts;
* verification of the tag's signature and of the attestation against a Bitcoin node;
* the reviewers' judgement on Gutenberg text under `DATA/SEEN.md`'s scope note (1).

## Order of operations

1. Freeze with `scripts/freeze_claim_specific.py`. Commit and push to the working branch and `main`.
2. Copy `FREEZE.json` to `receipts/SEC-PG-LLM-H-2026-10-08/` and `ots stamp` it. Record the pushed freeze commit (`anchor_github_commit.json`). Commit and push.
3. The owner signs and pushes the tag `prereg-SEC-PG-LLM-H-2026-10-08` on the freeze commit. This session cannot push tags; R2 and G4 require the tag before data.
4. On or after max(2026-10-09, the freeze date + 1 day) UTC (R3), run `data_step.py anchor` until it reports ok. That needs:
   * a Bitcoin attestation on the stamp;
   * block 970552 with at least 6 confirmations.

   Then commit and push `anchor_check.json` and the upgraded `.ots`. Once the draw has started, anchor refuses to run again.
5. `data_step.py draw`:
   * it refuses unless step 4 is committed and on origin;
   * it waits for the tag until the earliest data date + 12 h (2026-10-09T12:00Z), then proceeds without it, and the study is capped at a weak-anchor PASS-0 under LA-1;
   * it refuses after the earliest data date + 7 days, and the study is then NOT DECIDABLE.
6. `data_step.py register`, then commit and push `draw_attempts.jsonl`, `draw_log.json` and the `DATA/SEEN.md` rows (not the books). The runner refuses until every fetched file is registered.
7. `run_heldout.py 4 all` (pretrain, main, sens, rerun). It resumes after an interruption without re-running completed units.
8. `score_llmh.py > RUNS/<id>/score.json` (it also writes `score.txt`).
9. `make_receipts.py` writes the receipts LA-1 reads into `receipts/<id>/`: the exposure log, the data manifest, two further executions of the scorer that must equal `score.json` byte for byte, and the receipt. Commit and push.
10. `RESULT.md` is written only after the score, in `RUNS/<id>/`, never in this folder.

**Budget.** CPU only, 4 worker processes with 1 thread each: about 35 CPU-hours, so at least 8.7 hours wall-clock (`studies/SEC-PG-LLM-2026-10-08/budget_estimate.json`, from T4's and CPU-1's measured timings).

**Power.** This is development-based and optimistic, because the configuration was selected on the same anchors (a winner's curse). With the development means as true effects, the probability that P1–P3 all hold at n = 8 is 0.78 to 1.00, depending on how the seed-level spread is estimated (`studies/SEC-PG-LLM-2026-10-08/cpu1/cpu1_power.json`). A FAIL here means "not shown on these books at this power" as much as "refuted".

## What a RESULT would and would not license

**Would license:** a provisional held-out pass for SEC-PG (all4) on small byte-level Transformers (widths 64–192, 1–8 M pretraining tokens), for one drawn English-fiction → French/German-fiction task pair, conditional on that draw.

**Would not license:**

* larger models, other tokenisations, other task pairs, longer task sequences, or real continual-learning benchmarks;
* any cost claim;
* any claim that SEC's secant contributes, unless K5 holds;
* the absence of a reversal smaller than 0.01 nats in the 8 M or width-192 strata, or a statement about the width-192 × 8 M cells alone (those are reported descriptively);
* anything about CRR.

**Ledger route.** The scorer is claim-specific.

* NOT DECIDABLE and REDUCES go through `scripts/append_nonnumeric.py`; REDUCES needs two reviewers.
* RESULT and FAIL wait for a reviewer to apply LA-1. Its interim script is `scripts/append_result_v2.py`: it re-executes this scorer, requires its stdout to equal `score.json` byte for byte, and caps the row at a weak-anchor PASS-0 unless the Bitcoin attestation precedes exposure and the tag is verified.
* The entry's `signed_tag` may be `verified` only if `draw_log.json` shows `tag_ok_at_anchor` true (the tag was on origin before the first fetch) and the reviewer has verified the signature. Otherwise it is `none`.

**PASS-2.** This needs a second person or machine re-running this frozen protocol (CPU, `environment.lock`) on a later day, or a fresh preregistration on a new draw of books. A GPU study at other widths would be a separate extension, not a replication.

## Known limits, stated before the run

* **Exposure.** The texts are public-domain classics and almost certainly in the training data of the language model that wrote this protocol. The learner is trained from scratch, and the books are drawn after the freeze by a key that includes a then-unknown block hash. None was opened in any CRR work. Under `DATA/SEEN.md`'s scope note, a reviewer may still judge them LLM-exposed public data; that question is left to them.
* **Independence.** One operator wrote the configuration, the scorer and this protocol. The separate-context reviews were not independent replication.
* **Sample.** Eight seeds and one book draw.
