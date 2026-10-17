# SEC5 (Ashes) — replication of SEC4-1 on a fourth unseen family (FAIL)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/sec5/`, `runs/sec5/`, `data/manifests/sec5.sha256`, `reports/sec5.md` (→ `expected/REPORT_sec5.md`).
Included because it failed.

## Question

Does SEC4-1's PASS-1 (clipped SEC within a step of the tuned EWC λ) replicate on OpenML study 293 (AutoML Benchmark
Training Datasets), with κ swept? A CRR-guided refinement (A6: past importance averaged, not summed) was developed on
22 SEEN carriers first (`DEV_DECLARATION.md` pushed before any run).

## What CRR suggested / comparator

The A6 refinement was the CRR-guided part; it did not earn a test (`REPORT_sec5.md:29`). Comparator: EWC with a tuned λ
(17-configuration sweep), a 3-point sweep, a reused λ.

## Verdict (as recorded)

`expected/REPORT_sec5.md:30` "SEC5-1 … 4 of 8 (need 6) | **FAIL**"; ledger `ledger/LEDGER.md:194`: "FAIL (held-out,
the fourth family; not fragile: 0 of 40 sensitivity cells flip, κ included; SEC4-1's PASS-1 does not replicate, so no
PASS-2; SEC4-1 stands as a single-family PASS-1)". Per carrier: Indian_pines −6.7932 (step 5.21), Kuzushiji-MNIST
+5.2000 (1.33), autoUniv-au6-750 −0.3974 (1.64), microaggregation2 −4.1159 (15.52), pokerhand −28.2400 (1.82),
spoken-arabic-digit −0.0200 (1.00), volcanoes-d4 −88.9089 (1.00), walking-activity (see `score.txt`). Also SEC5-2
**FAIL**, SEC5-T **FAIL**, SEC5-P PASS-0 (6/8), SEC5-K CPU share 0.0563–0.0623 (`REPORT_sec5.md:31-35`).

## Data and effort

* OpenML ids 57 155 1503 1509 1529 1530 1532 1541 1549 41671 41972 41982 (≈ 204 MB; four excluded by the registered
  loader, 8 scored). Manifest `src/data/manifests/sec5.sha256`. Not bundled.
* **Rescore: Easy.** **Full: Moderate** — recorded wall 00:21:57 → 00:44:13 (`expected/run_started.txt`,
  `run_finished.txt`), Σ cpu 0.51 h.
* Environment: Ashes `uv.lock` (`uv sync --frozen` in the staged tree; Python 3.14). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1.

## Commands

```bash
bash run.sh            # rescore; compare score.txt
bash run.sh quick      # fetch 1549, rerun every arm (the study's R9 rerun); compare results_1549.jsonl
bash run.sh full
```
Frozen commands (`src/prereg/sec5/PREREG.md:173-177`):
```
uv run python data/fetch_openml.py --manifest sec5 57 155 1503 1509 1529 1530 1532 1541 1549 41671 41972 41982
uv run python runs/sec5/frozen/sec5_score.py check > runs/sec5/data_check.txt
for i in 57 155 1503 1509 1529 1530 1532 1541 1549 41671 41972 41982; do uv run python runs/sec5/frozen/sec5_score.py all $i --out runs/sec5/results_$i.jsonl; done
uv run python runs/sec5/frozen/sec5_score.py all 1549 --out runs/sec5/rerun_1549.jsonl --times runs/sec5/rerun_times_1549.jsonl && cmp runs/sec5/rerun_1549.jsonl runs/sec5/results_1549.jsonl   # R9
uv run python runs/sec5/frozen/sec5_score.py score runs/sec5/results_*.jsonl > runs/sec5/score.txt
```
`run.sh` stages `src/` beside `_shared/ashes/` in `./work`, fetches into a separate manifest name (`<s>_refetch.sha256`) and compares it with the committed one. Data are read from `ROOT/data/raw/openml/` with `ROOT = parents[3]` of `runs/<s>/frozen/`. Rescore copies `expected/results_*.jsonl` and `times_*.jsonl`. Always pass `--times` with a `rerun_*` output (otherwise timing rows overwrite the results file).

## Preregistration and anchor

`PREREG.md` (copy; `DEV_DECLARATION.md`, `dev/` and `dev_SEC5.txt` in `src/prereg/sec5/`). HASH.txt sha256
`2556b65e…`; prereg commit 576a092 pushed 2026-09-29T03:12Z; data from 2026-09-30T00:04:37Z. **Anchor: OpenTimestamps
complete in Bitcoin blocks 969093 and 969098** (`expected/ots_upgrade.txt`). Signed tag created, push refused.

## Verified re-run on 2026-10-17

`bash run.sh rescore`: `score.txt` **matches** byte for byte. The data-level re-run was not performed for SEC5.
