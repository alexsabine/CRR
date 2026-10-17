# EQ4 (Ashes) — the bounded equanimity rule EQ-B on six unseen PMLB carriers (FAIL)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/eq4/`, `runs/eq4/`, `data/manifests/eq4.sha256`, `reports/eq4.md` (→ `expected/REPORT_eq4.md`).
Included because it failed.

## Question

EQ-B bounds the rule: the present gradient is clipped at κ × the running median of its recent lengths before the
normalised step (`src/runs/eq4/frozen/eq4_score.py:1-31`). On clean streams, is EQ-B at Ω = 1 not behind the tuned EWC
λ on every carrier (EQ4-1)? Does the registered rule (EQ3-1's criterion) hold on fresh carriers (EQ4-1r)? Under
poisoned gradients, is it the rule or the clip that helps (EQ4-3, EQ4-4)?

## What CRR suggested / comparator

Ω = 1 with a bound. Comparators: online EWC with a tuned λ, a fixed weight with the same clip (`fixedclip`, the R7
baseline under poison), the reduction arm, ER-sum.

## Verdict (as recorded)

* **EQ4-1 FAIL (4/6)** — `expected/REPORT_eq4.md:50`; `ledger/LEDGER.md:74`: EQ-B − tuned −3.1832 / +4.0841 / −2.2727 /
  −0.4995 / −6.7304 / −6.7857 (page_blocks / satimage / segmentation / sleep / wine_quality_white / yeast); behind on
  segmentation (2.2727 > step 1.8625) and yeast (6.7857 > 6.0415).
* **EQ4-1r FAIL** — `LEDGER.md:75`: "EQ3-1's 5/6 does not replicate as 6/6".
* Under poison, "the clip is what helps, not the rule" (EQ4-3 FAIL); the ER-sum control is violated on sleep and
  satimage; 16 of 96 sensitivity cells flip (FRAGILE) (`REPORT_eq4.md:1-12`).

## Data and effort

* PMLB satimage, segmentation, yeast, wine_quality_white, sleep, page_blocks (≈ 1.3 MB; `src/data/manifests/eq4.sha256`).
  Fetched from PMLB (Git LFS on `master`, which is unpinned; every file is checked against the LFS oid and the committed sha256 manifest, so drift makes the run fail rather than silently change). Not bundled. satimage's records were also opened later in another study (T1x); verdicts are unchanged without it
  (`expected/score_without_satimage.txt`).
* **Rescore: Easy.** **Full: Easy–moderate** (runtime not recorded).
* Environment: Ashes `uv.lock` (`uv sync --frozen`; Python 3.14). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1. `gate.py` imports `crr.instrument.core` and `crr.surrogates.battery` from Ashes `src/crr/` (in `_shared/ashes/src/crr/`), and results record the sha256 of `ROOT/uv.lock`, so the lockfile must sit at the work root byte-identical (`run.sh` stages it).

## Commands

```bash
bash run.sh            # rescore; compare score.txt
bash run.sh quick      # fetch page_blocks, run the registered single-unit rerun (ewc, eqb, Ω = 1, seed 0); compare with rerun_page_blocks_a.json
bash run.sh full
```
Frozen commands (`src/prereg/eq4/PREREG.md:157-160`):
```
uv run python data/fetch_pmlb.py --manifest eq4 satimage segmentation yeast wine_quality_white sleep page_blocks
for c in satimage segmentation yeast wine_quality_white sleep page_blocks; do uv run python runs/eq4/frozen/eq4_score.py all $c > runs/eq4/log_$c.txt 2>&1; done
uv run python runs/eq4/frozen/eq4_score.py score runs/eq4/results_*.jsonl > runs/eq4/score.txt
uv run python runs/eq4/frozen/exclusions.py > runs/eq4/exclusions.txt
```

## Expected outputs

`expected/score.txt`, `score_without_satimage.txt`, `results_*.jsonl`, `rerun_<carrier>_{a,b}.json`,
`exclusions.txt`, logs.

## Preregistration and anchor

`PREREG.md` (copy). HASH.txt sha256 `e634280e…`; prereg commit a55be4d (2026-09-22T05:39:00Z); data fetched
2026-09-23T04:45:13Z. **Anchor: push-timestamp only** (weak).

## Verified re-run on 2026-10-17

* `bash run.sh rescore`: `score.txt` **matches** byte for byte.
* `bash run.sh quick`: page_blocks fetched from PMLB (sha256 matched); `run page_blocks ewc eqb 1.0 0` **matches**
  `rerun_page_blocks_a.json` byte for byte.
