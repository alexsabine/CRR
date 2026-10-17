# RW1 — is Hugging Face Trainer's resume already an "empty cut"? (Ashes Real_World)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at commit `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`Real_World/RW1.md`, `Real_World/DECLARATION_RW1.md`, `Real_World/checks/{rw1.py,rw1_run.py,rw1.txt,rw1_timing.txt}`.
The code imports `crr.instrument.core.kl_step` from Ashes `src/crr/` (in `_shared/ashes/src/crr/`). RW1 lives in
Ashes; the separate Embers repository only audits it and is not needed.

**Status: a declared note, not evidence** (R8, rung R4). `DECLARATION_RW1.md` was "pushed in e0a47b5, before any
script" (`src/Real_World/RW1.md:8`). It is not a hashed preregistration and has no ledger row.

## Question

Training stops right after a checkpoint; a new process resumes with `trainer.train(resume_from_checkpoint=...)`. Is the
continuation bit-for-bit identical to a run that never stopped (an "empty cut": the pause adds nothing), and which
pieces of the checkpoint make it so?

## What CRR suggested / established comparator

CRR's AI-safety work asks that a pause be lossless (nothing happens to the learner during the cut). The comparator is
the **existing stack's own checkpoint resume** (Transformers 5.17.0 `Trainer`, accelerate 1.15.0, torch 2.14.0 CPU),
which restores model, optimiser, scheduler, RNG state and data position.

## Result (as recorded)

`expected/rw1.txt`, last line: "summary: GPT-2 full grid: THE EXISTING STACK'S RESUME IS AN EMPTY CUT ON THIS SETTING;
Qwen2.5-0.5B-Instruct pilot: G0 holds; S1 holds". Table from `src/Real_World/RW1.md:26-36`:

| arm | GPT-2 | Qwen pilot |
|---|---|---|
| G0 two uninterrupted runs in separate processes | identical | identical |
| S1 the default resume | **identical, content 0** | **identical, content 0** |
| T default resume after real pauses of 5 s and 30 s | identical, content 0 | not run |
| S2 `ignore_data_skip=True` | not identical, content 0.0938111 | not run |
| S3 `rng_state.pth` deleted | not identical, content 0.0218955 | not run |
| S4 `optimizer.pt` deleted | not identical, content 0.41686 | not run |
| S5 `scheduler.pt` deleted | not identical, content 0.41686 | not run |

("content" = √(2·KL) on a probe.) Reading: a widely used system already meets the requirement on this setting; nothing
here bears on CRR's truth (`RW1.md:76-77`).

## Data, models, effort

* Synthetic token ids: 512 sequences × 64 ids in [0, 5000) (`rw1.txt` header). No dataset download.
* Models pinned by revision (`rw1_run.py:22-23`): `openai-community/gpt2@607a30d783dfa663caf39e06633721c8d4cfcd7e`
  (MIT, per its model card; check the card before use) and `Qwen/Qwen2.5-0.5B-Instruct@7ae557604adf67be50417f59c2c2f167def9a775` (Apache-2.0
  on its model card). `rw1.py` downloads them with `snapshot_download`, then sets `HF_HUB_OFFLINE=1` for every arm.
  Weights are not redistributed here.
* **Moderate.** CPU, one thread per run. GPT-2 arms ≈ 211–248 s each, full run 487.6 s; Qwen S1 111.9 s, full 209.0 s
  (`expected/rw1_timing.txt`); about 1 h in total. Disk: GPT-2 checkpoint ≈ 1.5 GB per run, Qwen optimiser 3.95 GB +
  weights 1.98 GB (`RW1.md:59-64`); plan for 8–10 GB free.
* Environment: Ashes `uv.lock` with the `realsys` group (torch 2.14.0+cpu, transformers 5.17.0, accelerate 1.15.0,
  numpy 2.5.3; `rw1.txt` line 2 records the uv.lock sha256 `34ad60bc…`, which equals `_shared/ashes/uv.lock`).

## Commands

```bash
bash run.sh
```

Original (from the Ashes root): `uv run --group realsys python Real_World/checks/rw1.py > Real_World/checks/rw1.txt`.
`run.sh` stages `src/Real_World/` beside `_shared/ashes/{pyproject.toml,uv.lock,src/crr}` and runs exactly that.

## Expected outputs and how to compare

`expected/rw1.txt` is byte-compared upstream ("A full rerun was byte-identical", `RW1.md:6`); `rw1_timing.txt` is
machine-dependent and not compared. Bitwise identity is claimed only for CPU, single thread (`RW1.md:74`).

## Verified re-run on 2026-10-17

**Not run here** (≈1 h CPU, ≈2.5 GB of model downloads and ≈10 GB of checkpoints). The environment lock was checked:
`_shared/ashes/uv.lock` has the sha256 recorded in `rw1.txt`.
