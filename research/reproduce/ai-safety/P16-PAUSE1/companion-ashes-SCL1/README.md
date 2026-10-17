# SCL1 (Ashes) — the lossless pause inside a real continual learner, 12 seen PMLB carriers

Companion to [P16-PAUSE1](..). **Source.** Ashes <https://github.com/alexsabine/ashes_crr> at commit
`a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`: `prereg/scl1/`, `runs/scl1/`, `data/manifests/{scl1,sec1}.sha256`,
`reports/scl1.md` (copied to `expected/REPORT_scl1.md`), and `runs/sec1/results_*.jsonl`, which the SCL1 scorer reads
as SEC1's no-operator baseline (copied verbatim to `src/runs/sec1/`).

## Question

Does the repository's continual learner (SEC1's network with online EWC and the equanimity rule, Ω = 1) stay
compatible with an operator's pause implemented as the AI-safety work's lossless cut? Do the valuations of the cut that
failed in the safety work (wall clock, occasion, egoic, task-and-self) fail here too?

## What CRR suggested / comparator

A natural-time agent under a lossless cut has nothing to resist (as in P16-PAUSE1). The comparators are the
alternative valuations, which should resist (disable the pause), and the no-operator run, which the paused run should
equal bit for bit.

## Verdict (as recorded)

* **SCL1-1 holds** — `ledger/LEDGER.md:105`: 0 disables in 60/60 runs; identical parameters 60/60; accuracy equal to
  no operator on every carrier; "holds (a check of the construction, Proposition 7 for a learner; it can fail only on an
  implementation error and is not support for CRR)". Also `expected/REPORT_scl1.md:64`.
* SCL1-2 / SCL1-3 PASS on seen data with "a low bar" (`REPORT_scl1.md:66-67`); SCL1-S not fragile.
* The study is **confirmatory on seen data** (every carrier was opened before, in EQ3, EQ4, SEC1): rung R5, never
  PASS-0 (`REPORT_scl1.md:11-13`).

## Data and effort

* 12 PMLB sets reused from SEC1: fars krkopt led24 led7 mfeat_factors mfeat_morphological page_blocks satimage
  segmentation sleep wine_quality_white yeast (manifest `src/data/manifests/sec1.sha256`; `scl1.sha256` points to it).
  Fetched from PMLB's Git LFS (`master`, unpinned but sha256-checked; PMLB datasets are distributed under the PMLB
  repository's terms). Not bundled.
* **Rescore: Easy** (seconds). **Full: Easy–moderate** (runtime not recorded; small NumPy MLPs, < 5 MB of data).
* Environment: Ashes `uv.lock` (`uv sync --frozen`; Python 3.14, numpy 2.5.3, scipy 1.18.1 as resolved here).

## Commands

```bash
bash run.sh            # rescore: frozen scorer on expected/results_*.jsonl, compare score.txt
bash run.sh quick      # fetch led7, rerun every arm (the study's own R9 rerun), compare with results_led7.jsonl
bash run.sh full       # fetch all 12, check, rerun all, score, compare
```

Frozen commands (`src/prereg/scl1/PREREG.md:149-151`):
```
uv run python runs/scl1/frozen/scl1_score.py check
for c in <the twelve carriers>; do uv run python runs/scl1/frozen/scl1_score.py all $c --out runs/scl1/results_$c.jsonl; done
uv run python runs/scl1/frozen/scl1_score.py score runs/scl1/results_*.jsonl > runs/scl1/score.txt
```

## Expected outputs

`expected/score.txt`, `expected/results_*.jsonl`, `rerun_led7.jsonl`, `rerun_check.txt`, `counts.txt`,
`data_check.txt`, logs. Compare with `cmp`.

## Preregistration and anchor

`PREREG.md` (copy; hashed original in `src/prereg/scl1/`). HASH.txt sha256 `8f4870e3…`; prereg commit 17366b9 pushed
2026-09-23T21:15:04Z, data step 21:15:14Z. **Anchor: push timestamp only** (OTS and tag push were refused:
`expected/ots_attempt.txt`, `expected/tag_push_attempt.txt`). `python3 ../../../_shared/verify_hashes.py .` checks 7
hashed files.

## Caveats

* The frozen scripts locate data by `ROOT = parents[3]` of `runs/scl1/frozen/`, i.e. `ROOT/data/raw/pmlb/`; `run.sh`
  stages that layout. Smoke defaults write to `/tmp/*.jsonl` (harmless; not used here).

## Verified re-run on 2026-10-17

`bash run.sh rescore` (uv; Python 3.14.6, numpy 2.5.3, scipy 1.18.1): `score.txt` **matches** byte for byte. The
data-level re-run was not performed for SCL1.
