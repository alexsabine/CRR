# SEC3 (Ashes) — replication of SCL3 on a second unseen family (FAIL)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/sec3/`, `runs/sec3/`, `data/manifests/sec3.sha256`, `reports/sec3.md` (→ `expected/REPORT_sec3.md`).
Included because it failed: it is part of the honest record.

## Question

Does SCL3's result — one SEC run within a step of the tuned EWC λ — replicate on OpenML study 271 (AutoML Benchmark):
covertype, dionis, fabert, helena, jannis, volkert (shuttle excluded by the class floor)?

## What CRR suggested / comparator

As SCL3: SEC is "the textbook Laplace weight with a units calibration", not a CRR rule; comparator EWC with a tuned λ
(17-configuration sweep), a 3-point mini-sweep and a reused λ.

## Verdict (as recorded)

`expected/REPORT_sec3.md:17-26`; ledger `ledger/LEDGER.md:176-178`:

| row | observed | verdict |
|---|---|---|
| **SEC3-3** (replication of SCL3-3) | 4 of 6 (need 5): covertype −3.3634 (step 4.81), dionis −4.5554 (3.44), fabert −3.8362 (1.00), helena −0.3800 (2.97), jannis −2.9400 (15.33), volkert +0.7200 (1.00) | **FAIL** — "SCL3-3's PASS-0 does not replicate on the second family" |
| SEC3-S | 2 of 18 cells flip | FRAGILE |
| SEC3-T | 2 of 3 | **FAIL** |
| SEC3-P | within a step of a 3-point mini-sweep on 5 of 6 | **PASS-0** |
| SEC3-2 | no harm where raw Laplace is fine: 4 of 5 (fabert harmed) | **FAIL** |
| SEC3-4 | spread: raw 23.50×, calibrated 30.00× | **FAIL** |
| SEC3-0/1 | only dionis miscalibrated | NOT DECIDABLE |
| SEC3-K | 1 of 17 configurations; CPU share 0.0575–0.0617 of the full sweep | report |

## Data and effort

* OpenML ids 1596 41167 41164 41169 41168 40685 41166 (≈ 328 MB ARFF; `src/data/manifests/sec3.sha256`), fetched from
  OpenML, md5- and sha256-checked. Not bundled; each dataset's licence is in its OpenML description.
* **Rescore: Easy** (seconds). **Full: Moderate** — recorded wall 00:20:45 → 00:32:02 (`expected/run_start.txt`,
  `run_end.txt`), Σ cpu 0.29 h; ≈ 328 MB download.
* Environment: Ashes `uv.lock` (`uv sync --frozen` in the staged tree; Python 3.14). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1.

## Commands

```bash
bash run.sh            # rescore; compare score.txt
bash run.sh quick      # fetch 41168 (jannis), rerun every arm (the study's R9 rerun); compare results_41168.jsonl
bash run.sh full
```
Frozen commands (`src/prereg/sec3/PREREG.md:176-180`):
```
uv run python data/fetch_openml.py --manifest sec3 1596 41167 41164 41169 41168 40685 41166
uv run python runs/sec3/frozen/sec3_score.py check > runs/sec3/data_check.txt
for i in 1596 41167 41164 41169 41168 40685 41166; do uv run python runs/sec3/frozen/sec3_score.py all $i --out runs/sec3/results_$i.jsonl; done
uv run python runs/sec3/frozen/sec3_score.py all 41168 --out runs/sec3/rerun_41168.jsonl --times runs/sec3/rerun_times_41168.jsonl && cmp runs/sec3/rerun_41168.jsonl runs/sec3/results_41168.jsonl   # R9
uv run python runs/sec3/frozen/sec3_score.py score runs/sec3/results_*.jsonl > runs/sec3/score.txt
```
`run.sh` stages `src/` (prereg, frozen code, manifest) beside `_shared/ashes/` in `./work`, fetches into a separate manifest name (`<s>_refetch.sha256`) and compares it with the committed one, so nothing committed is overwritten. The frozen scripts read data from `ROOT/data/raw/openml/` with `ROOT = parents[3]` of `runs/<s>/frozen/`; that layout is reproduced. Rescore copies `expected/results_*.jsonl` and `times_*.jsonl` (the scorer reports CPU shares from the latter).

**Caveat (`--times`).** Without `--times`, the timing rows go to the `--out` path with `results_` replaced by `times_`;
for a `rerun_*` file that is the same file, so the results get overwritten by timing rows. Pass `--times` explicitly,
as the prereg's R9 command does (`run.sh` does).

## Preregistration and anchor

`PREREG.md` (copy). HASH.txt sha256 `0c5ab70b…`; prereg commit 916d3d4 pushed 2026-09-27T23:42:45Z; data fetched from
2026-09-28T00:00:13Z. **Anchor: OpenTimestamps stamped 2026-09-27T23:42Z, "awaiting Bitcoin confirmation at the data
step"** (`LEDGER.md:176`; `expected/ots_attempt.txt`); no upgrade recorded. Signed tag created, push refused.

## Verified re-run on 2026-10-17

`bash run.sh rescore`: `score.txt` **matches** byte for byte (after adding the committed `times_*.jsonl`, which the
scorer reads for its compute row). The data-level re-run was not performed for SEC3.
