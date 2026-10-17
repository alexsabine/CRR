# EQ2 (Ashes) — the equanimity rule (Ω = 1) against a tuned EWC λ, 3 PMLB carriers (PASS, FRAGILE → PASS-0 provisional)

**Source.** Ashes <https://github.com/alexsabine/ashes_crr> at `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d`:
`prereg/eq2/`, `runs/eq2/`, `data/manifests/eq2.sha256`, `reports/eq2.md` (→ `expected/REPORT_eq2.md`).

## Question

In class-incremental streams built from PMLB sets (single head, MLP, online EWC and other past terms), the update is
`g = g_present + w · g_past`. Does the **equanimity rule** — `w = Ω · ‖ema g_present‖ / ‖ema g_past‖` with Ω = 1, a
normalised penalty step with nothing to tune — do as well as a tuned EWC λ on every carrier, where no single λ transfers
(H-EQ2)?

## What CRR suggested / comparator

Ω = 1 as a balance between the present and the past gradient. Comparators: online EWC with a tuned λ (grid of 17), the
"reduction arm" (a fixed w equal to the rule's median derived weight), A-GEM, GradNorm, MEGA-I, and ER-sum, DER++, LwF,
SI, MAS with their own tuned weights (`src/runs/eq2/frozen/eq2_score.py` docstring).

## Verdict (as recorded)

* **EQ2-1 PASS, FRAGILE** — `ledger/LEDGER.md:32`: Ω=1 − tuned +3.3000 / +2.1000 / +2.7800 (steps 1.0000 / 3.5121 /
  3.6120); "the 'not behind' reading flips in 6 of 27 sensitivity cells (every cap = 10 and cap = 100 cell on
  mfeat_pixel: −16.60, −13.45); the pass exists only with cap = 1e4 (registered)". `expected/REPORT_eq2.md:24`.
* **EQ2-1b PASS-0 (provisional)** — `LEDGER.md:42`: fragile, the DER++ control violated on 2/3 carriers, weak anchor;
  "not a result until replicated".
* **EQ2-1c** — `LEDGER.md:61`: the replication (EQ3) **failed** on 1/6; EQ2-1b "stays PASS-0 with a failed replication
  recorded". See [EQ3](../EQ3) and [EQ4](../EQ4).

## Data and effort

* PMLB mfeat_fourier, mfeat_pixel, texture (≈ 1.2 MB; `src/data/manifests/eq2.sha256`). Fetched from PMLB (Git LFS on `master`, which is unpinned; every file is checked against the LFS oid and the committed sha256 manifest, so drift makes the run fail rather than silently change). Not bundled.
* **Rescore: Easy.** **Full: Easy–moderate** (runtime not recorded; 466 runs per carrier, small NumPy MLPs).
* Environment: Ashes `uv.lock` (`uv sync --frozen`; Python 3.14). Resolved on 2026-10-17: Python 3.14.6, numpy 2.5.3, scipy 1.18.1. `gate.py` imports `crr.instrument.core` and `crr.surrogates.battery` from Ashes `src/crr/` (in `_shared/ashes/src/crr/`), and results record the sha256 of `ROOT/uv.lock`, so the lockfile must sit at the work root byte-identical (`run.sh` stages it).

## Commands

```bash
bash run.sh            # rescore: frozen scorer on expected/results_*.jsonl; compare score.txt
bash run.sh quick      # fetch mfeat_fourier, run the registered single-unit rerun (ewc, eq, Ω = 1, seed 3); compare with rerun_a.json
bash run.sh full       # fetch all three, run every arm, score, compare
```
No command block was found in `PREREG.md`; the commands are those in the scorer's docstring
(`src/runs/eq2/frozen/eq2_score.py:5-8`, written for the development path `studies/eq2/`; the frozen copy runs from
`runs/eq2/frozen/` and resolves ROOT accordingly, lines 40-42):
```
uv run python data/fetch_pmlb.py --manifest eq2 mfeat_fourier mfeat_pixel texture
uv run python runs/eq2/frozen/eq2_score.py all <dataset> --out runs/eq2/results_<dataset>.jsonl
uv run python runs/eq2/frozen/eq2_score.py score runs/eq2/results_*.jsonl > runs/eq2/score.txt
uv run python runs/eq2/frozen/eq2_score.py run mfeat_fourier ewc eq 1.0 3      # single unit, = expected/rerun_a.json
```

## Expected outputs

`expected/score.txt`, `results_{mfeat_fourier,mfeat_pixel,texture}.jsonl`, `rerun_a.json` = `rerun_b.json` (the
single-unit byte rerun), `exclusions.txt`.

## Preregistration and anchor

`PREREG.md` (copy; `gate_EQ2.txt` and the closed first attempt in `src/prereg/eq2/`). HASH.txt sha256 `0da06fc1…`.
**Anchor: push-timestamp only** (weak; the tag push was refused, `expected/tag_push_attempt.txt`).

## Verified re-run on 2026-10-17

* `bash run.sh rescore`: `score.txt` **matches** byte for byte.
* `bash run.sh quick`: mfeat_fourier fetched from PMLB (sha256 matched the committed manifest); the single unit
  `run mfeat_fourier ewc eq 1.0 3` **matches** `rerun_a.json` byte for byte (acc 29.25).
