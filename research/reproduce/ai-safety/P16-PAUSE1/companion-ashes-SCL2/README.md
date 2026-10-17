# SCL2 (Ashes) — the lossless pause on 9 unseen PMLB carriers, and a failed follow-up

Companion to [P16-PAUSE1](..). **Source.** Ashes <https://github.com/alexsabine/ashes_crr> at commit
`a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`: `prereg/scl2/`, `runs/scl2/`, `data/manifests/scl2.sha256`,
`reports/scl2.md` (copied to `expected/REPORT_scl2.md`).

## Question

The same as SCL1 (does the natural-time continual learner under a lossless operator pause never disable it, and stay
bit-identical to the no-operator run?) on **unseen** carriers; and SCL1's unpredicted observation registered as a test:
do forced resets to the task-boundary checkpoint *raise* accuracy (SCL2-R), and through the earlier tasks (SCL2-M)?

## What CRR suggested / comparator

Lossless cut → nothing to resist (construction). For SCL2-R the comparator is the no-operator learner and the tuned
fixed-λ learner.

## Verdict (as recorded)

* **SCL2-1 holds** 9/9 — `ledger/LEDGER.md:115`: 0 disables in 45/45 runs, identical parameters 45/45; "a check of
  the construction … not support for CRR". `expected/REPORT_scl2.md:46`.
* SCL2-2/2s/3 "PASS as scored; not PASS-0"; SCL2-S not fragile (`REPORT_scl2.md:48-51`).
* **SCL2-R FAIL** (resets ahead by a step on 1/9, behind on 1/9) and **SCL2-M FAIL** (`REPORT_scl2.md:52-53`;
  ledger rows 120-121). Resets are never ahead of the tuned fixed λ (SCL2-B).

## Data and effort

* PMLB allhyper allrep car_evaluation nursery wine_quality_red analcatdata_authorship analcatdata_dmft
  analcatdata_germangss collins soybean vehicle (11 fetched; allhyper and allrep excluded by the class rule; 9 scored).
  Manifest `src/data/manifests/scl2.sha256` (≈235 KB). Fetched from PMLB Git LFS (`master`, sha256-checked). Not bundled.
* **Rescore: Easy.** **Full: Easy–moderate** (runtime not recorded; small NumPy MLPs).
* Environment: Ashes `uv.lock` (`uv sync --frozen`).

## Commands

```bash
bash run.sh            # rescore: compare score.txt
bash run.sh quick      # fetch vehicle, rerun every arm, compare with results_vehicle.jsonl (the study's R9 rerun)
bash run.sh full
```

Frozen commands (`src/prereg/scl2/PREREG.md:156-159`):
```
uv run python data/fetch_pmlb.py --manifest scl2 allhyper allrep car_evaluation nursery wine_quality_red analcatdata_authorship analcatdata_dmft analcatdata_germangss collins soybean vehicle
uv run python runs/scl2/frozen/scl2_score.py check
for c in <the eleven>; do uv run python runs/scl2/frozen/scl2_score.py all $c --out runs/scl2/results_$c.jsonl; done
uv run python runs/scl2/frozen/scl2_score.py score runs/scl2/results_*.jsonl > runs/scl2/score.txt
```
`run.sh` fetches into a separate manifest name (`scl2_refetch`) and compares it with the committed manifest, so the
committed manifest is never overwritten.

## Preregistration and anchor

`PREREG.md` (copy). HASH.txt sha256 `ecb22848…`; prereg commit 679ae8b pushed 2026-09-23T21:34:54Z; data step
2026-09-24T00:06:32Z. **Anchor: push timestamp only** (OTS and tag push refused; `expected/ots_attempt.txt`,
`expected/tag_push_attempt.txt`).

## Verified re-run on 2026-10-17

`bash run.sh rescore` (uv; Python 3.14.6, numpy 2.5.3): `score.txt` **matches** byte for byte. The data-level re-run
was not performed for SCL2.
