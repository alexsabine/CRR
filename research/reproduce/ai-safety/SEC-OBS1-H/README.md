# SEC-OBS1-H — observation-aware protection in a continual learner (held-out run)

**Source.** Phoenix `Phoenix_Egg/studies/SEC-OBS1-H-2026-10-08/` (frozen folder), `RUNS/SEC-OBS1-H-2026-10-08/`,
`receipts/SEC-OBS1-H-2026-10-08/`, at commit `1295af24e82e0502a6bd284cd021149d4891eb5b`.

## Question

A small torch MLP learns task A, then task B, in synthetic latent-variable worlds where the learner's *observation*
of task A can be degraded (projection, aliasing, missingness, drift, concept drift, hidden A). Four registered
hypotheses on 100 fresh held-out histories (`PREREG.md`):

* **H1** — does SEC-PG (a light anchor at κ_SEC/16 plus GPM projection switched on at step 100) beat the strongest
  inexpensive comparator?
* **H2** — does an observation-aware diagnostic predict when the stronger intervention is worth it?
* **H3** — do the CRR path quantities (Fisher–Rao coherence, chord, apparent surplus) add predictive information
  beyond native diagnostics?
* **H4** — can observation-aware abstention protect monitor-driven tuning?

## What CRR suggested

That the learner's path on the Fisher–Rao manifold (coherence, chord, surplus) carries information about forgetting
that standard diagnostics miss, and that the observation channel matters to when protection is needed.

## Established comparators

EWC-style quadratic anchors (a transferred constant κ = 100 was the strongest inexpensive comparator), SEC v2, GPM
(gradient projection memory), native diagnostics (loss rise, gradient conflict, overlap, CKA, effective rank, …).
H1's schedule uses no observation and no CRR quantity: its parts are EWC-style anchoring and GPM
(`expected/RESULT.md:63`).

## Verdict (as recorded)

`expected/score.txt` (Phoenix `RUNS/SEC-OBS1-H-2026-10-08/score.txt`): **H1 PASS, H2 NO, H3 FAIL, H4 PASS**;
100/100 admissible, powered. Numbers from `expected/RESULT.md:20-23`:

| hypothesis | verdict | numbers |
|---|---|---|
| H1 SEC-PG vs strongest inexpensive comparator (constant κ = 100, mean J 0.4415) | PASS | SEC-PG 0.4313; paired difference −0.0102 [−0.0136, −0.0068] |
| H2 observation-aware diagnostic | NO | AUC(N+O) 0.790; N+O − N = −0.005 [−0.010, +0.001]; acting on the classifier is *worse* than always intervening, +0.0058 [+0.0039, +0.0080] |
| H3 CRR path quantities add information | FAIL | R²(N+C) − R²(N) = +0.0004 [−0.019, +0.018] |
| H4 observation-aware abstention | PASS | gain on corrupting conditions −0.113 [−0.128, −0.100]; detection balanced accuracy 0.944; against the constant alone +0.0006 [−0.0001, +0.0013], i.e. no gain |

Recorded discrepancy (`RESULT.md:69`): the prereg quotes a development AUC of ≈0.75 (an interim figure); the final
development value was 0.695. A separate-context verifier reproduced `score.json` exactly (`RESULT.md:71-73`).

## Data and effort

* Synthetic worlds from `secobs_lib.py`. Held-out seeds derived from the freeze commit `92c73fa1…5640`: first seed
  831489, count 100, draw seed 1598158214 (`expected/draw_log.json`). Development data are bundled in the frozen
  folder (`dev_episodes.jsonl`, seeds 10000–10119; used only to fit the H2/H3 predictors). No download.
* **Rescore: Easy** (the scorer: sklearn LogisticRegression/Ridge, bootstrap B = 4000; minutes).
  **Full: Moderate** — recorded `real 15m57s`, `user 46m11s` on 3 workers / 4 cores (`expected/run.log`). CPU only.
* Recorded environment (`environment.lock`): python 3.11.15, torch 2.14.1+cpu, numpy 2.4.6, scikit-learn 1.9.1,
  scipy 1.17.1; OMP/MKL/OpenBLAS threads 1; 3 worker processes. `requirements.txt` (full) and
  `requirements-rescore.txt` pin these.

## Commands

```bash
bash run.sh            # rescore (default): frozen scorer on expected/heldout_episodes.jsonl; compare score.json, score.txt
bash run.sh full       # re-run the 100 episodes with the frozen run_heldout.sh, then score and compare
```

Frozen commands: `bash run_heldout.sh 92c73fa15f41f586da1ed108edc108efde145640` (derives the seeds from the SHA and
writes to `../../RUNS/SEC-OBS1-H-2026-10-08`); re-score only:
`python3 score_secobs1h.py <heldout_episodes.jsonl> dev_episodes.jsonl <out.json> > score.txt`.

## Expected outputs and how to compare

* `expected/score.json`, `expected/score.txt` — byte comparison (`cmp`).
* A full re-run does **not** reproduce `heldout_episodes.jsonl` byte for byte: workers append in completion order
  (`imap_unordered`) and each row carries wall-clock timings. Compare through `score.json`. Whether the bootstrap is
  sensitive to row order was not tested here. The original record re-ran 4 episodes bit-identically with timings
  excluded (`expected/rerun_check.jsonl`).
* `run_episodes.py` skips seeds already present in its output file; `run.sh` starts from an empty `RUNS/<ID>/`.

## Preregistration and anchor

* `PREREG.md`, `PREREG_CLAIM.json` (copies; hashed originals in `src/studies/…/`). FREEZE.json sha256 `e4c71317…9f61`,
  row 5 of `_shared/phoenix/EPISTEMIC/FREEZE_LEDGER.jsonl`. The held-out seeds are a function of the freeze commit, so
  they could not be chosen before the freeze.
* OpenTimestamps: `expected/receipts/FREEZE.json.ots`, with the operator's upgraded-attestation check
  (`ots_info_upgraded_2026-10-08.txt`, `attestation_check_2026-10-08.txt`).
* **Anchor not independently verified** (`receipt.json`: `external_anchor_verified: false`, `reviewer: ""`).

## Caveats

* No pinned dependency file existed upstream; torch, scikit-learn and the bootstrap are version-sensitive, so a
  different stack may change digits (rescore with the pinned versions to get bytes).
* `run_heldout.sh` calls `python3` from `PATH`; `run.sh full` puts the venv first.

## Verified re-run on 2026-10-17

`bash run.sh rescore` (python 3.11.17, numpy 2.4.6, scikit-learn 1.9.1, scipy 1.17.1): about 11 min wall on a shared
machine. `score.json` **matches** and `score.txt` **matches** byte for byte (H1 PASS, H2 NO, H3 FAIL, H4 PASS). The
full episode re-run was **not** performed here.
