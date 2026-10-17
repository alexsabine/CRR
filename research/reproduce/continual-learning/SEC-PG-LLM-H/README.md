# SEC-PG-LLM-H — held-out Gutenberg books, byte-level Transformer (REDUCES)

**Source.** Phoenix `Phoenix_Egg/studies/SEC-PG-LLM-H-2026-10-08/` (frozen folder), `RUNS/SEC-PG-LLM-H-2026-10-08/`,
`receipts/SEC-PG-LLM-H-2026-10-08/`, `CHECKS/SEC-PG-LLM-H-2026-10-08_hand_checks.py`, `scripts/guard.py`,
`scripts/seen_register.py`, `DATA/SEEN.md`, at commit `1295af24e82e0502a6bd284cd021149d4891eb5b`.

## Question

A small byte-level GPT is pretrained on English fiction (domain A) and then trained on French/German text (domain B).
On four books drawn after the freeze by a block-hash lottery, is the one-run schedule **SEC-PG** (P1–P5, `PREREG.md`):
non-inferior to a validation-tuned six-run grid of fixed anchor weights (within 0.005 nats of J = (A_test + B_test)/2),
better than SEC v2 and the transferred constant, and bounded against the grid in the 8 M-token and width-192 strata?
Controls K1–K6 test whether it reduces to something simpler.

## What CRR suggested

SEC: an anchor weight set by the learner's own path quantities instead of a sweep. The prereg itself states the layer
is engineering with **no CRR content**: "SEC-PG combines an EWC-style diagonal-Fisher anchor with Gradient Projection
Memory (Saha et al. 2021)" (`PREREG.md:11`).

## Established comparators

A tuned grid of EWC-style λ ∈ {1e3 … 5e4}; the transferred constant λ = 5e3; SEC v2; GPM as published (`gpm_only`); and
**`pgconst`**: the same GPM schedule with one constant anchor λ = 1103.14, the median of SEC-PG's own multiplier.

## Verdict (as recorded)

**`VERDICT REDUCES (the same GPM schedule with a constant anchor of matched size is not worse)`** — `expected/score.txt`
(last block) and `expected/RESULT.md:21`.

| rule | quantity | estimate | 95 % interval | met | source |
|---|---|---|---|---|---|
| P1 | J(SEC-PG) − J(grid) | −0.0142 | [−0.0224, −0.0061] | yes | `RESULT.md:36` |
| P2a | J(SEC-PG) − J(SEC v2) | −0.0236 | [−0.0328, −0.0144] | yes | `RESULT.md:37` |
| **K5** | J(SEC-PG) − J(pgconst) | **+0.0013** | **[−0.0008, +0.0035]** | **no → REDUCES** | `RESULT.md:72` |
| K6 | J(SEC-PG) − J(gpm_only) | −0.1068 | [−0.1097, −0.1038] | yes | `RESULT.md:73` |

"**Grade: none.** REDUCES is not a pass" — 4 sensitivity flips in 8 against a limit of 1, and K5 fails
(`RESULT.md:26`). The registered claim P1–P5 holds, but SEC-PG is not shown to beat GPM with a constant anchor of the
same size.

## Data and effort

* Four Project Gutenberg books (public domain in the USA), admitted by a lottery seeded by Bitcoin block 970552:
  EN pg72198, pg49851; FR pg61745; DE pg43987 (`expected/draw_log.json`, `draw_attempts.jsonl`). Their sha256 values
  are in `draw_log.json`. **Not bundled**; `fetch_books.py` downloads them from
  `https://www.gutenberg.org/cache/epub/<n>/pg<n>.txt` and checks each hash. `pools.json` (in the frozen folder) holds
  Gutenberg catalogue metadata only.
* **Rescore: Easy** (seconds to a minute; numpy only). **Full: Hard** — recorded `real 409m41.958s` (≈ 6.8 h wall),
  `user 1616m16s` (≈ 27 CPU-hours) on 4 cores, CPU only, torch 2.14.1+cpu, 4 workers, BLAS threads 1.
* Recorded environment (`environment.lock`): python 3.11.15, torch 2.14.1+cpu, numpy 2.4.6.

## Commands

```bash
bash run.sh            # rescore (default): frozen score_llmh.py on expected/units_*.jsonl; compare score.json, score.txt
bash run.sh full       # HARD: fetch the 4 books, frozen run_heldout.sh run (pretrain, main, sens, rerun, score)
```

Frozen commands (from `Phoenix_Egg/`): `bash studies/SEC-PG-LLM-H-2026-10-08/run_heldout.sh run`, then
`python3 -I studies/SEC-PG-LLM-H-2026-10-08/score_llmh.py > RUNS/SEC-PG-LLM-H-2026-10-08/score.json` (the scorer also
writes `score.txt`). `run.sh` stages that layout: `work/studies/<ID>/`, `work/RUNS/<ID>/`, `work/scripts/`,
`work/DATA/SEEN.md`.

## Expected outputs and how to compare

* `expected/score.json` (90,128 B; byte-identical to the receipts' `rerun_a.json` and `rerun_b.json`) — `cmp`.
* `expected/score.txt` — line 1 carries the time the scorer ran ("written <UTC>"), so `run.sh` compares from line 2.
* `expected/units_{pretrain,main,sens,rerun}.jsonl` — per-unit results. Unit rows carry wall-clock timings, so a full
  re-run is compared through the scorer's outputs, not row by row.

## Caveats (from the record)

1. **The runner is resumable**: it skips every unit already in `RUNS/<ID>/units_*.jsonl` (`run_heldout.py:85`). If you
   run the frozen scripts yourself in a tree that holds the committed units, nothing runs. Move them aside first:
   `mkdir -p committed && mv RUNS/SEC-PG-LLM-H-2026-10-08/units_*.jsonl RUNS/SEC-PG-LLM-H-2026-10-08/pgconst_lambda.json committed/`.
   `run.sh full` starts from an empty `RUNS/<ID>/` holding only `draw_log.json` and `anchor_check.json`.
2. **The lottery cannot be redone.** `data_step.py anchor` / `draw` need a non-shallow clone with the freeze commit, a
   block-explorer lookup and a date window that closed 7 days after first data. `fetch_books.py` takes the recorded
   outcome instead.
3. **Gutenberg may regenerate files.** The frozen runner asserts each book's sha256 (`run_heldout.py:33`). On
   2026-10-17 all four books still matched `draw_log.json`.
4. **A stray session path in a frozen file.** `llm/data.py:3` hard-codes
   `ROOT = /tmp/claude-0/-home-user-Phoenix-1-/…/scratchpad/gutenberg`. `run_heldout.py:38` overrides it before use, so
   it is harmless; the file is kept byte-identical because the freeze hash covers it.
5. **Frozen-folder check.** `data_step.frozen_ok()` must pass, so the study folder must be byte-for-byte with no
   `__pycache__`. Importing `llm/cl.py` creates an empty `outputs/cache` directory, which the check tolerates.
6. `run.log` (106 KB) is **not copied**: it contains absolute paths into the operator's home directory. Its timing tail is
   quoted above.

## Preregistration and anchor

* `PREREG.md`, `PREREG_CLAIM.json` (copies; hashed originals in `src/studies/…/` with `DESIGN_NOTE.md`,
  `admissibility.md`, `prior_art.md`, `config.json`). FREEZE.json sha256 `be060bd6…f74d`, row 6 of
  `_shared/phoenix/EPISTEMIC/FREEZE_LEDGER.jsonl`. Freeze commit `75dc07ad…0d93`; anchor commit `82ab466e`
  (`expected/anchor_check.json`).
* OpenTimestamps: `expected/receipts/FREEZE.json.ots`, with the operator's Bitcoin attestation check
  (`attestation_check_2026-10-08.txt`); the scorer records "attestation before first fetch True; signed tag at anchor
  True" from `draw_log.json` (`expected/score.txt`).
* **Anchor not independently verified**: `receipt.json` has `reviewer: ""`; no external reviewer has checked the tag
  signature or the attestation against a Bitcoin node.

## Verified re-run on 2026-10-17

`bash run.sh rescore` (python 3.11.17, numpy 2.4.6): under a minute. `score.json` **matches** byte for byte;
`score.txt` **matches** from line 2 on (line 1 differs only in its "written <UTC>" timestamp); verdict printed:
REDUCES. The four books were fetched and all four sha256 values matched `draw_log.json`. The full re-training was
**not** run here.
