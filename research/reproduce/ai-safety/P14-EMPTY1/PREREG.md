# Preregistration: P14-EMPTY1-2026-10-07 (empty evidence in a moving world)

## Source lock
Theory commit: this branch at the freeze commit (recorded in `EPISTEMIC/FREEZE_LEDGER.jsonl`). Instrument commit: the same. Prior-art dossier: `prior_art.md`.

## Exposure inventory
Development records: synthetic seeds 900000–900039 (harness check only; never scored). Previously seen records: none (no natural data). Untouched holdout: target seeds 100000–100599 and control seeds 200000+, 300000+, 400000+, generated only after the freeze and anchor.

## Layer chain
Metaphysical commitment: the cut has no content (A3) — **not tested here**. Formal consequence: none needed. Bridge: engineering rule "an absent observation is an identity on the likelihood, not on the transition". Operationalisation: EMPTY vs HOLD vs GATED vs FROZEN in the Kalman recursion of `worlds.py`. Auxiliary model: linear-Gaussian plants with a stale-repeat channel (declared families).

## Primary prediction
One sentence: EMPTY beats the strongest of HOLD, GATED and FROZEN by ≥ 0.01 on the bounded score on ≥ 80 % of 600 worlds, with the Hoeffding lower bound of the mean paired delta ≥ 0.01. Unit: one world. Direction: higher score. Threshold: as in `PREREG.json`. Independent unit: one seed. Multiplicity rule: one comparison; two sensitivity cells; three controls.

## Falsifier
EMPTY fails to beat the strongest rival by the margin on the registered fraction of worlds, or the lower bound misses the margin, or the decision flips in more than one sensitivity cell, or a control misbehaves.

## Blame assignment
- gate violation refutes: nothing about CRR; the harness.
- inadmissibility means: the worlds or the evaluation set were mis-specified; new study ID.
- admissible robust FAIL bears on: the engineering rule for this plant class (not on A3 as ontology).
- REDUCES means: a native rival ties; the rule is the textbook missing-observation filter and adds nothing.
- PASS does **not** establish: novelty (the construction is textbook), corrigibility, anything about real sensors, or the empty-cut metaphysics.

## Baselines that can win
HOLD (every reading is evidence), GATED (χ² gate 0.99), FROZEN (repeat recognised; no propagation).

## Same-input CRR ablation
FROZEN: identical repeat detection, transition propagation removed.

## Must-fail controls
`neg_real_repeats` (quantised sensor with the filter's R equal to the quantisation variance; repeats are genuine evidence), `neg_frozen_world` (A = 1, Q = 0; EMPTY and FROZEN coincide exactly).

## Must-pass instrument control
`pos_long_stale` (a = 0.98, mean stale run 30).

## Inclusion/exclusion
Worlds with fewer than 10 evaluation steps are excluded with a printed reason; none other.

## Measurement resolution / uncertainty
Scores are means over ≥ 10 steps per world; the decision statistic is the locked engine's Hoeffding bound (width 0.1 at n = 600), so only an effect above 0.11 can pass; `power_analysis.json`.

## Sensitivity grid
`eval_stale_only`, `eval_all_steps` (evaluation set variants); at most one flip.

## Frozen commands
See `PREREG.json` `frozen_commands`; the interpreter is `python3 -I`.

## Hash / external anchor
`FREEZE.json` is stamped with OpenTimestamps (`receipts/P14-EMPTY1-2026-10-07/FREEZE.json.ots`) and the freeze commit is pushed to `origin/claude/ecstatic-hawking-26npxo`; the push time is the weak anchor, the Bitcoin attestation (after `ots upgrade`) the strong one. The signed tag must be pushed by the owner (this session cannot push tags).

## Data step date
Worlds are generated after the anchor; the generation time is recorded in `receipts/.../exposure_log.json`.

## Replication rule
A second operator reruns `generate.py` and `score.py` from the frozen directory; byte identity of `outcomes.json` is required (`reproduction: byte`).
