# SEC6R (Ashes) — the same criterion with an instrument gate (gate CLOSED; PASS-0 UNINFORMATIVE)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/sec6r/`, `runs/sec6r/` (including `partA/`), `data/manifests/sec6r.sha256`, `reports/sec6r.md`
(→ `expected/REPORT_sec6r.md`). The scorer also reads `runs/sec4/score.txt` and `runs/sec5/score.txt` (for the
family record); verbatim copies are in `src/runs/sec4/` and `src/runs/sec5/`.

## Question

SEC6 scored 0 of 12 carriers because its loader dropped STRING targets; SEC6R reruns it with the one change that the
loader reads a STRING target as a class label (`DECLARATION.md` pushed before any SEC6R code). Part B (held-out, 12
OpenML ids from SEC7's metadata-only draw): is the clipped SEC not behind the tuned λ — **and does an instrument gate
(would a learner frozen after task 1 also pass?) stay open?** Part A re-runs SEC6's twelve seen carriers (post hoc).

## What CRR suggested / comparator

SEC (not a CRR rule) against EWC with a tuned λ; published baselines SI, AR1; and the **frozen-after-task-1 learner** as
the instrument check.

## Verdict (as recorded)

`expected/REPORT_sec6r.md:93-94`; ledger `ledger/LEDGER.md:234-235`; Phoenix `EPISTEMIC/LEDGER.csv:6`:

| row | observed | verdict |
|---|---|---|
| SEC6R-G | the frozen learner ("edge") is not behind on 8/9 (closes at 7) | **gate CLOSED** |
| SEC6R-1 | 7/9 (need 7); behind on meta_stream_intervals.arff (−10.4600, step 3.23) and volcanoes-d1 (−80.8208, step 23.90) | **PASS-0, UNINFORMATIVE** |
| SEC6R-B | beats every published baseline? clipped SEC 7/9; AR1-B 8/9, SI-1C 8/9 | **FAIL** |
| SEC6R-T | is the saving SEC's? 5/7 (need 6) | **FAIL** |
| SEC6R-2 | divergence on volcanoes-d1 (2.3223 vs tuned 83.1431) | **FAIL** |

"So SEC4-1 gets no PASS-2" (`REPORT_sec6r.md:89`).

## Data and effort

* Part B OpenML ids 183 279 1534 1538 1542 1552 40985 46608 46684 46709 46745 46761 (≈ 140 MB; some are string-target
  or text datasets: HolisticBias, drug_reviews_druglib_com, mental_health_detection). Manifest
  `src/data/manifests/sec6r.sha256`. Not bundled.
* **Rescore: Easy.** **Full: Moderate** (≈ 140 MB; runtime per carrier in `expected/times_*.jsonl`).
* Environment: Ashes `uv.lock` (`uv sync --frozen` in the staged tree; Python 3.14). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1.
* Part A (`expected/partA/`) is kept as a record; `run.sh` scores Part B only. Part A's commands are
  `src/prereg/sec6r/PREREG.md:90-92` and `expected/run_partA.sh`; its data are SEC6's seen carriers.

## Commands

```bash
bash run.sh            # rescore Part B; compare score.txt
bash run.sh quick      # fetch 1552, rerun every arm with --part B (the study's R9 rerun); compare results_1552.jsonl
bash run.sh full
```
Frozen commands (`src/prereg/sec6r/PREREG.md:94-101`; the original driver is `expected/run_partB.sh`, three carriers
at a time):
```
uv run python data/fetch_openml.py --manifest sec6r 183 279 1534 1538 1542 1552 40985 46608 46684 46709 46745 46761
uv run python runs/sec6r/frozen/sec6r_score.py check --part B > runs/sec6r/data_check.txt
for i in <the twelve>; do uv run python runs/sec6r/frozen/sec6r_score.py all $i --part B --out runs/sec6r/results_$i.jsonl; done
uv run python runs/sec6r/frozen/sec6r_score.py all <one scored id> --part B --out runs/sec6r/rerun_<id>.jsonl && cmp …   # R9
uv run python runs/sec6r/frozen/sec6r_score.py score runs/sec6r/results_*.jsonl > runs/sec6r/score.txt
```
`run.sh` stages `src/` beside `_shared/ashes/` in `./work`, fetches into a separate manifest name (`<s>_refetch.sha256`) and compares it with the committed one. Data are read from `ROOT/data/raw/openml/` with `ROOT = parents[3]` of `runs/<s>/frozen/`. Rescore copies `expected/results_*.jsonl` and `times_*.jsonl`. Always pass `--times` with a `rerun_*` output (otherwise timing rows overwrite the results file).

## Preregistration and anchor

`PREREG.md` (copy; `DECLARATION.md`, `devid_r*.txt`, `feat_*.json` in `src/prereg/sec6r/`). HASH.txt sha256
`dc9c64d7…`; prereg commit 20f7d06 pushed 2026-10-01T01:08:02Z; data from 2026-10-02T00:07:24Z. **Anchor:
OpenTimestamps complete in Bitcoin blocks 969375/969398/969440** (`expected/ots_upgrade.txt`). Signed tag created,
push refused.

## Caveats

* `runs/sec6r/frozen/sec6_score.py` (a frozen sibling) contains `DEV_CACHE = Path("/tmp/claude-0/rrm_cache")`, a
  development cache path outside the repository. It is kept byte-identical (hashed); it is not used by the Part B path.

## Verified re-run on 2026-10-17

`bash run.sh rescore`: `score.txt` **matches** byte for byte (with `runs/sec4/score.txt` and `runs/sec5/score.txt`
present, as the scorer requires). The data-level re-run was not performed for SEC6R.
