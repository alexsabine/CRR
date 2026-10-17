# P14-EMPTY1 — result as scored (2026-10-07; written after the frozen run, per README_FIRE step 9)

**Status: SCORED; receipt awaiting the reviewer.** The frozen scorer's decision is recorded below from `RUNS/P14-EMPTY1-2026-10-07/outcomes.json` (byte-identical on two runs). It becomes a ledger row only when a reviewer verifies the OpenTimestamps proof and a signed tag and sets the receipt booleans (`receipts/P14-EMPTY1-2026-10-07/receipt.json`), after which `scripts/append_result.py` records the verdict the locked `guard.score` recomputes. Until then no verdict word is claimed here beyond "threshold met as computed".

## Chronology (all UTC, 2026-10-07)
| step | time | evidence |
|---|---|---|
| freeze (`freeze_record.py`) | 19:54:55 | `EPISTEMIC/FREEZE_LEDGER.jsonl` entry `P14-EMPTY1-2026-10-07:FROZEN:1`; FREEZE.json sha256 `910170c0…ee261` |
| OTS stamp of FREEZE.json | 19:54 | `receipts/P14-EMPTY1-2026-10-07/FREEZE.json.ots` (pending Bitcoin attestation; `ots upgrade` later) |
| freeze commit pushed | 19:54:57 | commit `33dc4d81…880e`, GitHub record `anchor_github_commit.json` |
| worlds generated (first exposure) | 19:55:55 | `exposure_log.json`; 2400 npz files, target manifest of 600 |
| scorer run a / run b | 19:56–20:03 | `rerun_a.json` = `rerun_b.json` = `outcomes.json` (byte) |

## Decision as computed by the locked engine (`guard.decision`, PREREG.json thresholds)
| set | n | wins (Δ ≥ 0.01) | fraction | mean Δ | Hoeffding lower bound | threshold met |
|---|---|---|---|---|---|---|
| primary (eval = observed repeats + 5 steps) | 600 | 600 | 1.000 | +0.2796 | +0.1796 | yes |
| sensitivity `eval_stale_only` | 600 | — | — | +0.3297 | — | yes |
| sensitivity `eval_all_steps` | 600 | — | — | +0.1891 | — | yes |
| control `pos_long_stale` (expected PASS) | 600 | — | — | +0.3171 | — | yes |
| control `neg_real_repeats` (expected FAIL) | 600 | — | — | +0.0305 | — | no |
| control `neg_frozen_world` (expected FAIL) | 600 | — | — | −0.0035 | — | no |

Sensitivity flips: 0 of 2 (limit 1); not fragile. Exclusions: none. Controls as registered. Plumbing check: a throwaway receipt with the reviewer fields filled was passed through `guard_strict.py` to confirm that the frozen scorer re-executes and matches the outcome bytes; its output was discarded and is not a verdict. Two incidents on the way (both logged): Python wrote a bytecode cache into the frozen directory, and this RESULT file was first written inside it; both broke `verify_freeze` until removed, and RESULT.md now lives in `RUNS/`.

## What this is, and is not
- **Rung R4 (declared synthetic), engineering layer, novelty N0, specificity S1.** The candidate is the textbook missing-observation Kalman recursion applied after a bit-identical repeat is recognised (`prior_art.md`). The pass, if the reviewer completes it, is a restricted engineering effect for linear-Gaussian plants with an unflagged stale channel: do not update on a repeat, do keep propagating the transition.
- **The ablation carries the content.** FROZEN (repeat recognised, propagation removed) loses by the same amount as HOLD and GATED; in the frozen-world control FROZEN and EMPTY coincide exactly and the candidate cannot win, as registered. The claim is therefore about transition propagation, which is the native filter's, not about the cut.
- **Not established:** anything about A3 as ontology (P-G4), corrigibility, or real sensors; GATED is a weak rival here because a long stale run produces a large innovation that the gate then rejects, so the comparison favours the candidate in exactly the regime the claim names.
- **Reduction reading.** If the oracle (flagged missingness) were a rival the candidate would tie it; the result is best read as "repeat detection + the native missing-observation filter", a useful reduction rather than a CRR-specific effect.

## Constraints gained / restrictions removed
Gained: the P14 claim is now a frozen, scored, bounded comparison with controls; its ceiling (PASS-0, R4, S1) is fixed. Removed: none; the enquiry's interpretation ceiling stands.
