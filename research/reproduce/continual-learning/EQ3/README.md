# EQ3 (Ashes) — replication of EQ2 on six unseen PMLB carriers (FAIL)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/eq3/`, `runs/eq3/`, `data/manifests/eq3.sha256`, `reports/eq3.md` (→ `expected/REPORT_eq3.md`).
Included because it failed.

## Question

Does EQ2-1b's provisional pass replicate: is the equanimity rule (Ω = 1) not behind the tuned EWC λ by a step on every
one of six fresh PMLB carriers, with no single λ transferring?

## What CRR suggested / comparator

As [EQ2](../EQ2): Ω = 1 normalised penalty step against online EWC with a tuned λ and the other baselines.

## Verdict (as recorded)

**FAIL** — `ledger/LEDGER.md:46`: Ω=1 − tuned −3.7400 / +0.9790 / +0.6886 / +4.0625 / +3.9000 / +3.7000 (steps
3.3508 / 8.9180 / 4.3633 / 3.2031 / 4.5371 / 4.8719); 5/6 not behind; "**FAIL** (fars behind by 3.7400 > step; … fars,
whose class 0 is empty after the pre-registered subsample and whose EWC family is at chance; scored as committed, no
exemption)". `expected/REPORT_eq3.md:35`. Consequence for EQ2: `LEDGER.md:61` (EQ2-1c).

## Data and effort

* PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes,
  5000-row subsample) (≈ 1.3 MB; `src/data/manifests/eq3.sha256`). Fetched from PMLB (Git LFS on `master`, which is unpinned; every file is checked against the LFS oid and the committed sha256 manifest, so drift makes the run fail rather than silently change). Not bundled.
* **Rescore: Easy.** **Full: Easy–moderate** (runtime not recorded).
* Environment: Ashes `uv.lock` (`uv sync --frozen`; Python 3.14). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1. `gate.py` imports `crr.instrument.core` and `crr.surrogates.battery` from Ashes `src/crr/` (in `_shared/ashes/src/crr/`), and results record the sha256 of `ROOT/uv.lock`, so the lockfile must sit at the work root byte-identical (`run.sh` stages it).

## Commands

```bash
bash run.sh            # rescore; compare score.txt
bash run.sh quick      # fetch led7, run the registered single-unit rerun (ewc, eq, Ω = 1, seed 0); compare with rerun_led7_a.json
bash run.sh full
```
No command block in `PREREG.md`; usage from the scorer's docstring (`… all <dataset>`, `… score <results…>`,
`… run <dataset> <method> <mode> <value> <seed>`), inferred as for EQ2:
```
uv run python data/fetch_pmlb.py --manifest eq3 mfeat_factors mfeat_morphological led7 led24 krkopt fars
uv run python runs/eq3/frozen/eq3_score.py all <dataset> --out runs/eq3/results_<dataset>.jsonl
uv run python runs/eq3/frozen/eq3_score.py score runs/eq3/results_*.jsonl > runs/eq3/score.txt
```

## Expected outputs

`expected/score.txt`, `results_*.jsonl`, `rerun_<carrier>_{a,b}.json` (one single-unit byte rerun per carrier),
`exclusions.txt`, logs.

## Preregistration and anchor

`PREREG.md` (copy). HASH.txt sha256 `5b3bec36…`; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched
2026-09-22T01:23Z. **Anchor: push-timestamp only** (weak).

## Verified re-run on 2026-10-17

* `bash run.sh rescore`: `score.txt` **matches** byte for byte.
* `bash run.sh quick`: led7 fetched from PMLB (sha256 matched); `run led7 ewc eq 1.0 0` **matches**
  `rerun_led7_a.json` byte for byte.
