# P14-EMPTY1 — a repeated observation as empty evidence, against the Kalman missing-observation filter

**Source.** Phoenix `Phoenix_Egg/studies/P14-EMPTY1-2026-10-07/` (frozen folder), `RUNS/P14-EMPTY1-2026-10-07/`,
`receipts/P14-EMPTY1-2026-10-07/`, `scripts/guard.py` (locked decision engine), at commit
`1295af24e82e0502a6bd284cd021149d4891eb5b`.

## Question

A sensor channel sometimes re-emits its last value without a flag (a stale, bit-identical repeat). For a
linear-Gaussian plant, does treating the repeat as **empty evidence** — no measurement update, but keep propagating
the transition — beat (i) treating it as a fresh observation (HOLD), (ii) a standard χ² innovation gate (GATED), and
(iii) recognising the repeat but freezing the state (FROZEN, the CRR ablation)?

## What CRR suggested

The "empty cut" has no content: do not invent an observation where there is none, but time still passes.

## Established comparator

This is the textbook missing-observation Kalman recursion (Anderson & Moore 1979 §3.4; Bar-Shalom, Li & Kirubarajan
2001 §5.2; Harvey 1989; Shumway & Stoffer 2017 §6.4), applied after the repeat is detected (`prior_art.md`; novelty
N0, specificity S1). The ablation FROZEN loses by as much as HOLD and GATED, so the content is the native filter's
transition propagation, not the cut (`expected/RESULT.md:28`).

## Verdict (as recorded)

**"Status: SCORED; receipt awaiting the reviewer … no verdict word is claimed here beyond 'threshold met as
computed'"** (`expected/RESULT.md:3`; Phoenix `RUNS/P14-EMPTY1-2026-10-07/RESULT.md:3`). The decision table, computed
by the locked engine `guard.decision` with the thresholds in `PREREG.json` (`RESULT.md:15-22`):

| set | n | wins (Δ ≥ 0.01) | mean Δ | Hoeffding lower bound | threshold met |
|---|---|---|---|---|---|
| primary (observed repeats + 5 steps) | 600 | 600 (1.000) | +0.2796 | +0.1796 | yes (`RESULT.md:17`) |
| sensitivity `eval_stale_only` | 600 | — | +0.3297 | — | yes |
| sensitivity `eval_all_steps` | 600 | — | +0.1891 | — | yes |
| control `pos_long_stale` (expected PASS) | 600 | — | +0.3171 | — | yes |
| control `neg_real_repeats` (expected FAIL) | 600 | — | +0.0305 | — | no |
| control `neg_frozen_world` (expected FAIL) | 600 | — | −0.0035 | — | no |

Sensitivity flips 0 of 2; controls as registered. The ceiling, if a reviewer completes the receipt, is PASS-0 (R4,
declared synthetic). The record's own reading (`RESULT.md:30`): "repeat detection + the native missing-observation
filter, a useful reduction rather than a CRR-specific effect". GATED is a weak rival in exactly the regime the claim
names (a long stale run makes a large innovation that the gate then rejects; `RESULT.md:29`).

## Data and effort

* Synthetic: 2400 worlds (targets W0001–W0600 in families F1a/F1b/F2a/F2b; controls P, N, Z × 600), seeds
  100000+, 200000+, 300000+, 400000+ (`generate.py`). Generated locally; no download.
* CPU, numpy only. Recorded: two scorer runs in about 3–4 min each. **Easy.**
* Recorded environment: python 3.11.15, numpy 2.4.6, `python3 -I`.

## Commands

```bash
bash run.sh      # stage ./work, venv, generate, score, compare, then recompute the decision table (decide.py)
```

Frozen commands (`PREREG.json` "frozen_commands"), run unchanged by `run.sh` in the required layout:

```bash
cd work/studies/P14-EMPTY1-2026-10-07 && python3 -I generate.py > ../../receipts/P14-EMPTY1-2026-10-07/data_manifest.json
cd work && python3 -I studies/P14-EMPTY1-2026-10-07/score.py studies/P14-EMPTY1-2026-10-07 > RUNS/P14-EMPTY1-2026-10-07/outcomes.json
```

`decide.py` (written for this folder) calls `guard.verify_freeze` and `guard.decision` exactly as `guard.score` does.
It skips `guard.score`'s receipt checks (`scripts/guard_strict.py` additionally needs `git verify-tag` and an
OpenTimestamps verification): those need the reviewer's signed receipt, which does not exist yet.

## Expected outputs

* `expected/outcomes.json` (514,751 B; sha256 `897bf6f7…cb91`). The original `rerun_a.json` and `rerun_b.json` are
  byte-identical to it and are not duplicated here.
* `expected/receipts/data_manifest_full.json` — the generator's stdout (all 2400 worlds). `data_manifest.json` is the
  600-target subset with `raw/`-relative paths that the receipt checker reads, derived from it afterwards.
* Compare with `cmp`; the decision lines should equal the table above.

## Preregistration and anchor

* `PREREG.md` and `PREREG.json` (copies here; hashed originals in `src/studies/…/`), plus `power_analysis.json`,
  `controls.json`, `admissibility.md`, `prior_art.md`. FREEZE.json sha256 `910170c0…ee261`, row 1 of
  `_shared/phoenix/EPISTEMIC/FREEZE_LEDGER.jsonl`. Frozen 19:54:55Z, freeze commit `33dc4d81` pushed 19:54:57Z, worlds
  first generated 19:55:55Z (2026-10-07; `RESULT.md:8-11`).
* OpenTimestamps proof `expected/receipts/FREEZE.json.ots` (pending Bitcoin attestation when recorded).
* **Anchor not independently verified** (`receipt.json`: `external_anchor_verified: false`, `signed_tag_verified:
  false`, `reviewer: ""`). The freeze commit is not reachable from a shallow clone.

## Caveats

* Python must not write `__pycache__` into the frozen folder: that broke `verify_freeze` once in the original run
  (`RESULT.md:24`). `run.sh` runs on a staged copy with `python -I -B`.
* Not copied: `anchor_github_commit.json` (80 KB GitHub API dump), `ots_verify_output.txt` (local node path),
  `rerun_a.json`/`rerun_b.json` (duplicates of `outcomes.json`).

## Verified re-run on 2026-10-17

`bash run.sh` (python 3.11.17, numpy 2.4.6): scorer 4 min 44 s wall. `outcomes.json` **matches** byte for byte; the
generator's manifest **matches** `data_manifest_full.json` byte for byte; `decide.py` reproduces every row of the
table above (600/600, mean +0.2796, lower bound +0.1796; controls as registered; 0 flips).
