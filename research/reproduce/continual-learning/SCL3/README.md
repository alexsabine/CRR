# SCL3 (Ashes) — one self-calibrated EWC weight (SEC) against a tuned 17-point λ sweep, 10 unseen OpenML sets

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at commit `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/scl3/`, `runs/scl3/`, `data/manifests/scl3.sha256`, `reports/scl3.md` (→ `expected/REPORT_scl3.md`).

## Question

Can a single run with SEC — the Laplace (EWC) penalty weight calibrated from the learner's own Fisher, with no sweep —
stay within a resolvable step of the best λ from a 17-configuration sweep (class-incremental MLP on tabular streams)?
SCL3-1: on miscalibrated carriers, does calibration close half the raw-Laplace gap? SCL3-2: no harm elsewhere?
SCL3-3: not behind the tuned λ on ≥ ⌈0.75 N⌉ carriers? SCL3-4: does calibration collapse the tuned λ's spread?

## What CRR suggested / established comparator

"**SEC is not a CRR rule.** It is the textbook Laplace weight with a units calibration" (`REPORT_scl3.md:22-23`).
CRR's own rule (the equanimity rule, Ω = 1) was the comparison arm: not behind the tuned λ on 7/10. The comparator is
EWC with a validation-tuned λ (17-point sweep). Later prior-art review of the SEC method: **KNOWN**
(`../SEC4/expected/REPORT_sec4.md:106`).

## Verdict (as recorded)

`expected/REPORT_scl3.md:54-57` and `ledger/LEDGER.md:131-134`:

| row | observed | verdict |
|---|---|---|
| SCL3-1 | 5/6; not on cnae-9 (gap 18.4375, gain −3.5417) | **PASS-0** |
| SCL3-2 | 4/4 not behind | **PASS-0** |
| SCL3-3 | 9/10; cnae-9 behind (−21.9792, step 1.73). Raw Laplace 4/10, the rule Ω = 1 7/10 | **PASS-0** |
| SCL3-4 | raw span 18866.67×, calibrated 500.00× | **PASS-0** |

"PASS-1 not reached: SCL3-S FRAGILE" (6 of 80 sensitivity cells flip; `LEDGER.md:133`). Compute: SEC is 1 of 17
configurations; the "~94 % compute saving" quoted elsewhere is 1 − ≈0.06 from the SEC3/SEC4/SEC5/SEC6R compute rows,
not an SCL3 row. Phoenix caveat: a learner frozen after task 1 meets the same criterion on 24/30 carriers
(Phoenix `AI_SAFETY/README.md:28`, `CONTINUAL_LEARNING.md:12`).

## Data and effort

* OpenML-CC18 ids 1468 188 1475 4538 1478 300 40966 1501 40982 1497 (≈ 98 MB ARFF), fetched from
  `https://www.openml.org/api/v1/json/data/<id>` by `_shared/ashes/data/fetch_openml.py`, md5-checked against the
  description, sha256 against `src/data/manifests/scl3.sha256`. OpenML lists the licence of all ten as "Public"
  (`src/prereg/scl3/descriptions/*.json`). Not bundled.
* **Rescore: Easy** (seconds). **Full: Easy–moderate** (runtime not recorded; the same learner's logged CPU totals for
  SEC3/4/5 are 0.29/0.12/0.51 CPU-h).
* Environment: Ashes `uv.lock` (`uv sync --frozen` in the staged tree; Python 3.14 from `.python-version`). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1. The scorers are NumPy-only learners.

## Commands

```bash
bash run.sh            # rescore: frozen scorer on expected/results_*.jsonl; compare score.txt
bash run.sh quick      # fetch 1497 (wall-robot-navigation), rerun every arm = the study's R9 rerun; compare results_1497.jsonl
bash run.sh full       # fetch all ten, check, rerun all, score, compare each results file and score.txt
```

Frozen commands (`src/prereg/scl3/PREREG.md:197-201`):
```
uv run python data/fetch_openml.py --manifest scl3 1468 188 1475 4538 1478 300 40966 1501 40982 1497
uv run python runs/scl3/frozen/scl3_score.py check > runs/scl3/data_check.txt
for i in <the ten ids>; do uv run python runs/scl3/frozen/scl3_score.py all $i --out runs/scl3/results_$i.jsonl; done
uv run python runs/scl3/frozen/scl3_score.py all 1497 --out runs/scl3/rerun_1497.jsonl && cmp runs/scl3/rerun_1497.jsonl runs/scl3/results_1497.jsonl   # R9
uv run python runs/scl3/frozen/scl3_score.py score runs/scl3/results_*.jsonl > runs/scl3/score.txt
```
`run.sh` fetches into `data/manifests/scl3_refetch.sha256` and compares it with the committed manifest, so the committed
manifest is not overwritten.

## Expected outputs

`expected/score.txt`, `results_*.jsonl`, `rerun_1497.jsonl`, `rerun_check.txt`, `counts.txt`, `data_check.txt`,
`hash_check*.txt`, `ots_upgrade.txt`, per-carrier logs. Compare with `cmp`.

## Preregistration and anchor

`PREREG.md` (copy; hashed original in `src/prereg/scl3/`). HASH.txt sha256 `d9d8e853…`; prereg commit 05318d4
(2026-09-24); data fetched 2026-09-25T00:07:06Z. **Anchor: OpenTimestamps complete, Bitcoin blocks 968341/968343,
merkle roots checked** (`expected/ots_upgrade.txt`; `src/prereg/scl3/HASH.txt.ots`). Signed tag created, push refused.

## Caveats

* Layout: `ROOT = parents[3]` of `runs/scl3/frozen/`; data are read from `ROOT/data/raw/openml/`. `HASH.txt` uses
  `../../runs/scl3/frozen/…` relative paths. `run.sh` stages exactly that layout.
* `HASH.txt` lists itself, so its own line cannot match (recorded upstream in `expected/hash_check.txt`);
  `verify_hashes.py` reports it as KNOWN.
* Smoke defaults write to `/tmp/*.jsonl` (harmless; not used).

## Verified re-run on 2026-10-17

* `bash run.sh rescore`: `score.txt` **matches** byte for byte (uv; Python 3.14.6, numpy 2.5.3).
* `bash run.sh quick`: OpenML 1497 fetched through the network; its ARFF matched the committed manifest;
  every arm re-run; `results_1497.jsonl` **matches** byte for byte.
