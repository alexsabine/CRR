# SEC4 (Ashes) — clipped SEC on a third unseen family (SEC4-1 PASS-1)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/sec4/`, `runs/sec4/`, `data/manifests/sec4.sha256`, `reports/sec4.md` (→ `expected/REPORT_sec4.md`).

## Question

After SEC3's failure, SEC was made robust with a stability clip (chosen on 16 SEEN carriers, `DEV_DECLARATION.md`
pushed before any guard ran). Is the clipped SEC within a resolvable step of the tuned EWC λ on a third unseen family
(OpenML suites 14/218/379/457)?

## What CRR suggested / comparator

SEC is not a CRR rule ("It is not a CRR rule", `REPORT_sec4.md:20`). Comparator: EWC with a tuned λ (17-configuration
sweep), a 3-point mini-sweep, a reused λ. **Prior art: KNOWN** (`REPORT_sec4.md:106`): the stability clip is AR1
(Maltoni & Lomonaco, arXiv 1806.08568); path-fitted curvature is Synaptic Intelligence; tuning-free principled weights
are VCL and Laplace Redux.

## Verdict (as recorded)

`expected/REPORT_sec4.md:24` "SEC4-1 … 6 of 6 (need 5) | **PASS-1**"; ledger `ledger/LEDGER.md:186`: JapaneseVowels
+2.5626 (step 1.00), anneal +5.5056 (5.63), artificial-characters +0.5594 (1.96), cardiotocography +1.0377 (1.00),
gas-drift +2.1822 (2.59), synthetic_control +3.5000 (3.59); SEC4-S not fragile (0/18); SEC4-2 no divergence.

**Post hoc caveat, recorded** (`ledger/LEDGER.md:211`, SEC4-1-G): under SEC6's later instrument rule, a learner
**frozen after task 1** meets SEC4-1's criterion on 5 of 6 carriers, so SEC4-1 "would be printed UNINFORMATIVE and capped
at PASS-0". SEC4-1 stands as scored. Its replication (SEC5) **failed**.

## Data and effort

* OpenML ids 46906 1459 1466 23380 1476 375 46980 1491 377 (≈ 21.5 MB; cjs, MIC and one-hundred-plants-margin are
  excluded by the registered loader, so 6 are scored). Manifest `src/data/manifests/sec4.sha256`. Not bundled.
* **Rescore: Easy.** **Full: Easy–moderate** — recorded wall 00:08:29 → 00:11:58 (`expected/run_started.txt`,
  `run_finished.txt`), Σ cpu 0.12 h.
* Environment: Ashes `uv.lock` (`uv sync --frozen` in the staged tree; Python 3.14). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1.

## Commands

```bash
bash run.sh            # rescore; compare score.txt
bash run.sh quick      # fetch 377 (synthetic_control), rerun every arm (the study's R9 rerun); compare results_377.jsonl
bash run.sh full
```
Frozen commands (`src/prereg/sec4/PREREG.md:150-154`):
```
uv run python data/fetch_openml.py --manifest sec4 46906 1459 1466 23380 1476 375 46980 1491 377
uv run python runs/sec4/frozen/sec4_score.py check > runs/sec4/data_check.txt
for i in 46906 1459 1466 23380 1476 375 46980 1491 377; do uv run python runs/sec4/frozen/sec4_score.py all $i --out runs/sec4/results_$i.jsonl; done
uv run python runs/sec4/frozen/sec4_score.py all 377 --out runs/sec4/rerun_377.jsonl --times runs/sec4/rerun_times_377.jsonl && cmp runs/sec4/rerun_377.jsonl runs/sec4/results_377.jsonl   # R9
uv run python runs/sec4/frozen/sec4_score.py score runs/sec4/results_*.jsonl > runs/sec4/score.txt
```
`run.sh` stages `src/` (prereg, frozen code, manifest) beside `_shared/ashes/` in `./work`, fetches into a separate manifest name (`<s>_refetch.sha256`) and compares it with the committed one, so nothing committed is overwritten. The frozen scripts read data from `ROOT/data/raw/openml/` with `ROOT = parents[3]` of `runs/<s>/frozen/`; that layout is reproduced. Rescore copies `expected/results_*.jsonl` and `times_*.jsonl` (the scorer reports CPU shares from the latter).

**Caveat (`--times`).** Always pass `--times` with a `rerun_*` output, as above: otherwise the timing rows are written
to the same file as the results (the default timing path replaces `results_` by `times_` in the output name).

## Preregistration and anchor

`PREREG.md` (copy), `DEV_DECLARATION.md` in `src/prereg/sec4/`. HASH.txt sha256 `cf702c31…`; prereg commit 278d0b4
pushed 2026-09-28T04:13Z; data fetched from 2026-09-29T00:05:59Z. **Anchor: OpenTimestamps complete in Bitcoin block
968935** (`expected/hash_check_datastep.txt`). Signed tag created, push refused (`expected/tag_attempt.txt`).

## Verified re-run on 2026-10-17

* `bash run.sh rescore`: `score.txt` **matches** byte for byte.
* `bash run.sh quick`: OpenML 377 fetched through the network (ARFF and description matched the committed manifest);
  every arm re-run under Python 3.14.6 / numpy 2.5.3; `results_377.jsonl` (271 lines) **matches** byte for byte.
