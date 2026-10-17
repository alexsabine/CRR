# SEC-PG-LLM-H: design note (2026-10-08, before the freeze)

This note records how the frozen configuration and design were reached. All numbers are printed by committed development scripts on SEEN data (T4's 32 cached anchors). None of them is a held-out result.

## CPU-1: the selection

**Rule.** It was fixed in `studies/SEC-OBS1-2026-10-08/LLM_NEXT_STEPS.md` before CPU-1 ran:

* choose the variant, or the original, with the smallest mean (SEC-PG − grid) at 8 M tokens;
* only among variants whose mean at 1–2 M tokens is ≤ −0.005;
* stop if no variant reaches +0.005 at 8 M.

**Results.** `studies/SEC-PG-LLM-2026-10-08/cpu1/cpu1_selection.json`; mean SEC-PG − grid in test J over 32 cells.

| variant | 1 M | 2 M | 4 M | 8 M | 1–2 M | width 192 | vs SEC v2 | vs const 5e3 |
|---|---|---|---|---|---|---|---|---|
| original (pilot: 3 maps, switch 25 %, threshold 0.97, SEC weight/16) | −0.0121 | −0.0088 | +0.0001 | +0.0194 | −0.0104 | +0.0070 | −0.0050 | −0.0066 |
| sw50 (switch at 50 %) | −0.0140 | −0.0100 | −0.0041 | +0.0130 | −0.0120 | +0.0063 | −0.0085 | −0.0100 |
| thr90 (threshold 0.90) | −0.0095 | −0.0110 | −0.0009 | +0.0169 | −0.0103 | +0.0048 | −0.0058 | −0.0073 |
| thr99 (threshold 0.99) | −0.0121 | −0.0057 | +0.0030 | +0.0227 | −0.0089 | +0.0104 | −0.0027 | −0.0042 |
| **all4 (attention out-projection also protected)** | −0.0169 | −0.0188 | −0.0202 | **+0.0002** | −0.0178 | −0.0141 | −0.0186 | −0.0201 |
| lconst (constant anchor 312.5) | +0.0086 | +0.0152 | +0.0216 | +0.0219 | +0.0119 | +0.0488 | +0.0121 | +0.0106 |

**Decision.** `SELECT all4`.

* all4 is the only variant whose mean over the 8 M cells reaches the rule's limit (+0.0002). It reduces the mature-cell reversal but does not remove it: in the two width-192 × 8 M cells it is still +0.0167 and +0.0023 above the grid (mean +0.0095, against +0.0321 for the original), and above SEC v2 in both.
* It is better than the original in every column of the table, and worse in 3 of 32 cells, all at width 64 (`studies/SEC-PG-LLM-2026-10-08/cpu1/cpu1_tolerance.json`).
* The out-projection's input is rebuilt from the in-projection input by an explicit causal attention. That reconstruction is checked against the module's output in every run; the largest error over the 32 runs is 1.9e-6 (`studies/SEC-PG-LLM-2026-10-08/cpu1/cpu1_tolerance.json`).
* The GPM bases of all4 take 43 % of the parameter count on average.

## Changes made after seeing development numbers

All of these were made before the freeze, and each is logged in `notebook/AGENT_LOG.md` (2026-10-08).

* **P5 made one-sided.**
  * T4's tolerance is two-sided: it counts a cell as a miss when an arm beats the grid by more than 0.02 in J, or differs from it by more than 0.05 on a task. On the 32 development cells, all4 meets it in 5 cells against SEC v2's 12 (`studies/SEC-PG-LLM-2026-10-08/cpu1/cpu1_tolerance.json`).
  * One-sided ("no worse than the grid beyond the tolerance"), the counts are 15 against 12. Of the 10 cells the one-sided form adds, 7 are cells where all4 beats the grid by more than 0.02 in J; in the other 3, only its old-task loss is more than 0.05 below the grid's.
  * The one-sided form keeps P5's purpose, which is that neither task becomes much worse than under the grid. The two-sided count is reported as description only.
  * This change makes the claim easier to meet than the plan's wording, and it was made after the development numbers were seen. Readers should weigh P5 accordingly.
* **Eight seeds instead of six.** The development power check (`studies/SEC-PG-LLM-2026-10-08/cpu1/cpu1_power.json`) used two estimates of the seed-level spread. With the cautious one, the probability that P1–P3 all hold was 0.49 at n = 6 and 0.78 at n = 8; the other gave 1.00 at both. Eight seeds cost about a third more compute (`studies/SEC-PG-LLM-2026-10-08/budget_estimate.json`: about 35 CPU-hours in all).
* **Student-t interval** over seed means, wider than the plan's percentile bootstrap at this n. The bootstrap is kept as description.

## Changes made after the adversarial review

Four reviewers worked in separate contexts, covering code, protocol, statistics and claim language. Each finding was checked by two skeptics. The findings applied were:

* **Anchor check.**
  * The OpenTimestamps proof is now tied to this freeze: its file digest equals FREEZE.json's.
  * Each Bitcoin attestation's Merkle root is checked against two block explorers.
  * Block times allow the protocol's 2-hour tolerance.
  * The frozen files are checked against FREEZE.json, not only HASHES.sha256.
  * Shallow clones are refused.
* **Draw key.** It includes the attested block hash, which nobody could know when the freeze commit was made, so the commit could not have been chosen to steer the draw.
* **R3 date.** It is computed from the freeze date as well as fixed at 2026-10-09 or later.
* **Signed tag.** The tag (R2, G4) is a step for the owner. The draw waits for it until 2026-10-09T12:00Z.
* **Draw safety.** The draw is append-only and resumable, and only HTTP 404 or 410 rejects a candidate.
* **SEEN rows.** They are entered where `scripts/seen_register.py` reads them, labelled LLM-exposed.
* **Runner and scorer.**
  * Both refuse if a frozen file changed.
  * The runner refuses a failed draw.
  * Truncated outputs and caches are handled on resume.
  * The repeat re-runs a width-128 pretraining from scratch.
* **New arms and controls.** Two arms and two controls were added for R7's "no constant reduction": GPM with a constant anchor (K5) and GPM alone (K6). K2 now uses the transferred constant; the frozen-learner gate could not fail. REDUCES and UNINFORMATIVE print the reason they were reached.
* **Scorer output.**
  * The grid choice uses T4's rounding.
  * Non-finite values outside SEC-PG make the verdict NOT DECIDABLE.
  * The rerun comparison is NaN-safe.
  * Stdout is deterministic JSON, as `append_result_v2.py` requires.
  * The verdict words are those of LA-1's set: RESULT, FAIL, REDUCES, NOT DECIDABLE.
* **Claim language.**
  * P3 is stated as a bounded reversal, not "no reversal".
  * Inference is conditional on the drawn books.
  * The labels are U3/N0/S0, and any attribution to SEC's secant is excluded unless K5 holds.
  * The ledger route and PASS-2 are stated as the scripts allow.
  * The PASS-1 preconditions are marked as not a grade.

The full reviewer output is kept at `studies/SEC-PG-LLM-2026-10-08/research/prereg_review.json`.

## Changes made after the second review round

A second round covered code, protocol and statistics, with one skeptic per finding; all 23 findings were confirmed. Applied (record: `studies/SEC-PG-LLM-2026-10-08/research/prereg_review_round2.json`):

* **Blocker.** `git show <rev>:<path>` reads paths from the repository top level, one directory above `Phoenix_Egg/`. The anchor's history check and the draw's committed-version check could never have passed, and both now use `./`-relative paths. The first rehearsal had mocked those steps, so it missed this.
* **Seen register.** Gutenberg 84, 1661 and 98, opened by RT1-PR1 on 2026-10-06, were missing from `DATA/SEEN.md`. They are now registered, their authors excluded, and the pools rebuilt (EN 16,075 → 15,932).
* **K5.** It used λ = 312.5, about a third of SEC-PG's typical multiplier on development data. It now uses a size-matched constant: the median of SEC-PG's own multiplier over the study's cells.
* **K6.** It inherited the delayed switch. It is now GPM as published, projecting from the first step.
* **Tag check.** A lightweight tag on the SSH-signed freeze commit would have passed as signed. The check now requires an annotated tag object, fetched into a private ref and matched to origin's.
* **Draw block.** The draw key now uses the hash of a block at a height fixed in the frozen code (970552), not whichever attestation the proof carries, so the block cannot be chosen.
* **Chronology.** The anchor refuses to run once the draw has started. The scorer takes the tag status and attestation time from `draw_log.json`, which is fixed at draw time, and checks that the anchor check preceded the first fetch.
* **Deadlines.** The tag deadline is the earliest data date + 12 h; a final draw date is set at + 7 days. A missing draw log scores NOT DECIDABLE.
* **Draw.** A partial last line in the attempt log is handled. Candidates already seen at draw time are skipped. `register` checks that every fetched file is registered, and the runner refuses until it is.
* **Receipts.** `make_receipts.py` writes the files LA-1 reads, and `RESULT.md` goes in `RUNS/<id>/`.
* **Wording.** The scorer's docstring, the budget (at least 8.7 hours) and the account of the P5 change were corrected.

## Rehearsal

The whole chain was rehearsed on a scratch copy, with tiny token budgets on SEEN books and a mock freeze, anchor and draw. That copy is not in the repository. All four stages ran, and the scorer handled every path tried:

* the repeat (including the repeated pretraining) was byte-identical;
* re-executing the scorer gave byte-identical stdout;
* changing a frozen file made both the runner and the scorer refuse;
* no bytecode was written into the study folder.

## Integration test (scratch clone with the real layout)

After the second review, the whole procedure was run end to end in a scratch clone of the repository: the same `repo/Phoenix_Egg` layout, real git history and a scratch bare origin, with tiny budgets. The script was kept in the session scratchpad and is not in the repository.

Scratch-only changes, applied before the scratch freeze so that A1 was tested for real:

* the date gate was moved to the test day;
* the draw block was set to an already-mined block;
* P14's attested proof stood in for the scratch freeze's (A2 bypassed);
* the pools held SEEN books only, so no new book was fetched;
* the German size floor was lowered to 150 kB so that Faust I (191 kB) passes S4.

Results:

* **Anchor.** A1 and A3–A7 passed, including the Merkle checks against both explorers and the history check fixed after the second review; A2 was bypassed, as above.
* **Tag.** A lightweight tag and an unsigned annotated tag were rejected; an SSH-signed annotated tag was accepted.
* **Order of steps.** The draw refused until the anchor record was committed. A dummy candidate returning 404 was rejected (S1), and the anchor refused to run again after the draw had started.
* **Register and run.** `register` confirmed every fetched file. The run completed all four stages, with the size-matched constant derived from the pretraining outputs.
* **Scoring and receipts.** The scorer printed its verdict (NOT DECIDABLE at these toy budgets, because no cell is admissible). `make_receipts.py` produced two re-executions byte-identical to `score.json`. The frozen folder was unchanged at the end.
* **Ledger path.** `scripts/append_result_v2.py` (LA-1), run inside the scratch clone, accepted the receipts and recorded the scorer's verdict word.

An earlier run of the same test, with the 200 kB floor, showed the draw correctly refusing (`ok` false) when the German quota could not be filled.
