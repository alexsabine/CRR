# SOTA1 (Ashes) — online Split-CIFAR-100: the CRR learner against ER, ER-ACE, DER++ and X-DER (FAIL)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/sota1/` (including the frozen scorer `sota1_score.py`), `runs/sota1/frozen/` (runner, vendored Mammoth, env lock),
`runs/sota1/{units,score.txt,results.json,…}`, `data/manifests/sota1.sha256`, `reports/sota1.md`
(→ `expected/REPORT_sota1.md`). Only the hashed copy of Mammoth (`runs/sota1/frozen/mammoth/`) is included, not the
duplicate under `studies/sota1/vendor/`.

## Question

In online Split-CIFAR-100 (10 tasks × 10 classes, reduced ResNet-18, buffer M = 2000, one epoch, batch 10, lr 0.1), is
the CRR safe continual learner (CRR-SCL, added to Mammoth as `models/crr_scl.py`) **ahead** of the best of ER, ER-ACE,
DER++ and X-DER? (SOTA1-1a/1b.) Is equanimity as a weight (Ω = 1) at least as good as MKD's published constant
(SOTA1-2)? Which CRR components help (SOTA1-3)?

## What CRR suggested / established comparators

A learner assembled from CRR's commitments (asymmetric incoming loss, cosine head, past-logit mask and fill, logit and
label replay, a slow model on the model's own clock, a lossless pause). Comparators: Mammoth's reference ER, ER-ACE,
DER++, X-DER (plus SGD, A-GEM, iCaRL, LwF, EWC-online for context).

## Verdict (as recorded)

`expected/REPORT_sota1.md:86-97`; ledger `ledger/LEDGER.md:152-154`:

| row | observed | verdict |
|---|---|---|
| SOTA1-1a / 1b | against ER-ACE: d = −3.30, step 1.07; per seed −2.11 / −4.51 / −3.00 / −4.60 / −2.28 | **FAIL / FAIL** |
| SOTA1-2 | against the constant λ = 5.5: d = −2.94 | **FAIL** (BEHIND, not REDUCES) |
| SOTA1-3 | 1 of 7 components passes: label replay +5.18 (PASS-0) — DER++'s β term, a published mechanism | 6 FAIL |
| SOTA1-S | 0 of 6 cells flip | not fragile |
| SOTA1-C1 | 6/6 units bitwise identical under a lossless pause | holds (construction) |

Final class-incremental accuracy, mean over seeds (`expected/score.txt:5-12`): ER-ACE 21.90, X-DER 20.44, ER 19.32,
**CRR 18.60**, DER++ 10.87, SGD 5.57. "CRR-SCL does not beat the state of the art" (`REPORT_sota1.md:18`).

## Data and effort

* CIFAR-100 (python version, Krizhevsky 2009) fetched by `_shared/ashes/data/fetch_cifar100.py` from
  `https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz`, md5 `eb9058c3…2d85` (torchvision's constant). Converted to
  `data/raw/cifar100/cifar100.npz`. **Not redistributed** (the repository records no licence statement for it).
* **Rescore: Easy** (seconds, Python standard library only). **Full: Hard** — budget 30.3 unit-hours (tiers A + C + S + B
  = 12.64 + 10.97 + 3.24 + 3.45; `src/prereg/sota1/budget.txt`), 2 units × 2 threads on a 4-CPU host; the recorded queue
  ran 2026-09-26 00:07Z → 17:13Z with two container losses, 104 of 110 unit records (`expected/run_log.txt`). CPU only.
* Full-run environment: the frozen lock `src/runs/sota1/frozen/env/{pyproject.toml,uv.lock}` — Python 3.12, torch
  2.14.0+cpu, torchvision 0.29.0+cpu, numpy 2.5.3. `run.sh full` builds it with `uv sync --frozen`.

## Commands

```bash
bash run.sh                 # rescore: frozen prereg/sota1/sota1_score.py on expected/units/*.json; compare score.txt, results.json
bash run.sh full [tier ...] # HARD: env, CIFAR-100 fetch, frozen sota1_run.py run [tiers], score, compare
```

Original commands (`sota1_score.py:3`, `sota1_run.py` docstring):
```
python data/fetch_cifar100.py
(cd studies/sota1/env && uv sync)        # the runner hard-codes ROOT/studies/sota1/env/.venv/bin/python
python runs/sota1/frozen/sota1_run.py run [tier ...]
python prereg/sota1/sota1_score.py > runs/sota1/score.txt          # also writes runs/sota1/results.json
```

## Caveats (from the record)

* **The runner runs missing units only.** If you run it in a tree holding the committed `runs/sota1/units/`, nothing
  runs. Move them aside first: `mv runs/sota1/units committed_units && mkdir runs/sota1/units`. `run.sh` starts from an
  empty `units/` (the committed ones stay in `expected/units/`). The scorer also accepts `SOTA1_UNITS=<dir>`.
* **Six units fail by construction**: lwf and ewc_on × 3 seeds failed on an argparse error ("NOT DECIDABLE",
  `run_log.txt` tail); a re-run reproduces those failures.
* `sota1_run.py` hard-codes the interpreter at `ROOT/studies/sota1/env/.venv/bin/python`; `run.sh full` builds the
  environment there inside the work tree.
* `HASH.txt` lists three vendored-Mammoth files (`requirements.txt`, `requirements-optional.txt`,
  `datasets/imagenet_r_utils/label_to_class_name.pkl`) that Mammoth's own `.gitignore` kept out of the Ashes repository;
  they are absent here too and are not on the SOTA1 code path. `verify_hashes.py` reports them as KNOWN.
* **Not copied:** `runs/sota1/run_stdout.txt` and eleven `runs/sota1/units/*.log` failure logs (container losses,
  argparse failures, a start-up race) — they contain absolute paths into the operator's home directory. The scorer reads only the
  `units/*.json` records.

## Third-party code

`src/runs/sota1/frozen/mammoth/` is a trimmed copy of aimagelab/mammoth at `e75a491c…` (MIT, © 2020 Buzzega, Boschini,
Porrello, Abati, Calderara; `mammoth/LICENSE`, `gem_license`, `NOTICE.md` kept). Upstream files are byte-identical;
three files were added for SOTA1 and 283 removed (`src/runs/sota1/frozen/MODIFICATIONS.md`).

## Preregistration and anchor

`PREREG.md` (copy; `budget.txt`, `gate_sota1.txt`, `timing/` and the frozen scorer in `src/prereg/sota1/`). HASH.txt
sha256 `4986bbee…`; prereg commit de95c63 (2026-09-25T11:51:16Z); data step 2026-09-26T00:07:26Z. **Anchor: OpenTimestamps
complete in Bitcoin blocks 968549/968554/968555/968581**, merkle roots matched against a public explorer
(`expected/ots_upgrade.txt`). All 197 hashed files unchanged after the run (`expected/hash_check.txt`).

## Verified re-run on 2026-10-17

`bash run.sh` (rescore, Python 3 standard library): under a second. `score.txt` and `results.json` **match** byte for
byte. The full training run was **not** performed here.
