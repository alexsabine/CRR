# SEC-PG-LLM-H-2026-10-08: RESULT

Written 2026-10-09, after the score.

**The plan behind this document.** It follows `CHECKS/SEC-PG-LLM-H-2026-10-08_RESULT_REPORTING_PLAN.md` (6f0d809; time corrected in 5193e44; addenda 3a0daf6 and b74605f). The claim that the plan was "fixed before the score" rests on two things:
- the plan's own stated times;
- commit ancestry: the plan is unchanged since b74605f, which is an ancestor of the commits that record the run's 08:22Z and 09:26Z interruptions.

There is no external timestamp on the plan. §11 lists the departures from it.

**Sources.** Numbers are copied from:
- `score.json` (sha256 34b1a2c1…), which is byte-identical to both receipt re-executions and to the verifier's re-execution;
- `hand_checks.json`, the `units_*.jsonl` files and `run.log`;
- `pgconst_lambda.json`, `anchor_check.json`, `draw_log.json`, `draw_attempts.jsonl`, `tag_verification.json` and `interruptions.jsonl`;
- the frozen `PREREG.md`.

Values are rounded for display only. Every verdict comparison uses the scorer's unrounded values.

## 1. Verdict

**`REDUCES (the same GPM schedule with a constant anchor of matched size is not worse)`**: the frozen scorer's verdict line, quoted exactly.

- **The registered claim P1–P5 holds on the held-out books.**
- **Control K5 fails.** SEC-PG was not shown to be better than `pgconst`. pgconst is the same GPM schedule with one constant anchor, whose λ is the median of SEC-PG's own multiplier α·s·κ over the 72 cells (λ = 1103.14, `pgconst_lambda.json`; the scorer re-derives the same value). The difference is SEC-PG − pgconst = +0.0013 nats, 95 % interval [−0.0008, +0.0035].
- **K5 is a superiority test.** Its failure means superiority was not shown. It does not show equivalence: the interval still allows SEC-PG to be better by up to 0.0008.
- **Grade: none.** REDUCES is not a pass. The scorer-computable PASS-1 preconditions are not all met: the verdict is not RESULT, there are 4 flips in 8 against a limit of 1, and K5 fails.
- **Ledger route:** `scripts/append_nonnumeric.py`, with two different reviewers (§10).
- **What this means:** under PREREG.md:211, no claim that SEC's secant contributes is licensed, because K5 does not hold.

## 2. The registered claim (P1–P5)

J = (A_test + B_test)/2, in nats; lower is better. The unit is the seed (n = 8). The interval is 95 % Student-t with t(0.975, 7) = 2.365.

| rule | quantity | estimate | 95 % interval | condition | met |
|---|---|---|---|---|---|
| P1 | J(SEC-PG) − J(grid) | −0.0142 | [−0.0224, −0.0061] | upper ≤ +0.005 | yes |
| P2a | J(SEC-PG) − J(SEC v2) | −0.0236 | [−0.0328, −0.0144] | mean ≤ −0.005, upper < 0 | yes |
| P2b | J(SEC-PG) − J(transferred constant λ = 5e3) | −0.0226 | [−0.0313, −0.0139] | mean ≤ −0.005, upper < 0 | yes |
| P3a | 8 M stratum: J(SEC-PG) − J(grid) | −0.0051 | [−0.0148, +0.0046] | upper ≤ +0.01 | yes |
| P3b | width-192 stratum: J(SEC-PG) − J(grid) | −0.0174 | [−0.0297, −0.0051] | upper ≤ +0.01 | yes |
| P4 | mean B_test, SEC-PG 2.1422 vs SEC v2 2.1534; mean A_test, SEC-PG − grid −0.0254 | | | B ≤ SEC v2 and A − grid ≤ 0.05 | yes |
| P5 | cells within T4's tolerance (one-sided): SEC-PG 33, SEC v2 24 | | | SEC-PG ≥ SEC v2 | yes |

**Per-seed values**, in drawn seed order 651629, 666445, 120855, 458320, 876683, 479962, 734239, 743387:

| quantity | per-seed values |
|---|---|
| P1 | −0.0136, −0.0107, −0.0093, −0.0021, −0.0202, −0.0193, −0.0329, −0.0057 |
| P2a | −0.0232, −0.0180, −0.0135, −0.0105, −0.0308, −0.0343, −0.0416, −0.0166 |
| P2b | −0.0186, −0.0229, −0.0142, −0.0089, −0.0280, −0.0311, −0.0411, −0.0162 |
| P3a | −0.0079, +0.0129, +0.0051, −0.0061, −0.0110, −0.0036, −0.0267, −0.0035 |
| P3b | −0.0119, −0.0073, −0.0040, −0.0100, −0.0351, −0.0211, −0.0437, −0.0060 |

Bootstrap intervals are given for description only in `score.json`.

**P5, two-sided form** (description only; PREREG.md:117-121):
- SEC-PG has 10 cells within tolerance, SEC v2 has 24. Under T4's declared two-sided tolerance, P5 would not be met.
- 23 cells count for SEC-PG only under the one-sided form. In all 23, SEC-PG beats the grid by more than the tolerance: in J for 15 of them, only in A for 7, and only in B for 1.
- SEC v2's count is 24 under both forms.
- The one-sided form was fixed before the freeze, after the development counts had been seen. That history is recorded in PREREG.md.

**Width-192 × 8 M cells alone** (description only; PREREG.md:212): SEC-PG − grid = +0.0023 [−0.0144, +0.0190]. No statement about these cells is licensed.

## 3. Controls

| id | kind | registered condition | quantity | estimate [95 % interval] | holds |
|---|---|---|---|---|---|
| K1 | positive | mean ≥ 0.01 and lower > 0 | J(none) − J(grid) | +0.0774 [+0.0712, +0.0835] | yes |
| K2 | instrument | upper > +0.005 (the transferred constant does not meet P1) | J(const) − J(grid) | +0.0084 [+0.0060, +0.0108] | yes |
| K3 | ablation | upper < 0 | J(SEC-PG) − J(light) | −0.0493 [−0.0542, −0.0444] | yes |
| K4 | must-fail | the light anchor alone does not meet P1–P5 | light meets P1–P5? | no | yes |
| **K5** | **constant reduction (R7)** | **upper < 0** | **J(SEC-PG) − J(pgconst)** | **+0.0013 [−0.0008, +0.0035]** | **no → REDUCES** |
| K6 | reduction to published GPM | upper < 0 | J(SEC-PG) − J(gpm_only) | −0.1068 [−0.1097, −0.1038] | yes |

K5 per-seed values: +0.0019, −0.0014, −0.0013, +0.0058, +0.0020, +0.0016, −0.0014, +0.0034. The scorer's check of every rival unit passed (score_llmh.py:69).

## 4. Admissibility and non-finite values

- 72 of 72 cells are admissible, against the 80 % the verdict needs, so there are none to list. Every cell is analysed either way (PREREG.md:123).
- There were no non-finite values and no missing registered units.
- The frozen folder was unchanged at scoring (`frozen_unchanged: true`).

## 5. Sensitivity

Each row moves one constant of SEC-PG and recomputes P1–P5. A flip is a change in whether the claim holds. The main claim holds, so flips are counted (PREREG.md:156).

| cell | change | SEC-PG − grid | P1 | P2 | P3 | P4 | P5 | claim holds | flip |
|---|---|---|---|---|---|---|---|---|---|
| kappa_lo | anchor multiplier 1/32 | +0.0082 | no | no | no | yes | no | no | **yes** |
| kappa_hi | anchor multiplier 1/8 | −0.0286 | yes | yes | yes | no | yes | no | **yes** |
| switch_lo | GPM from 12.5 % of task B | −0.0004 | no | yes | no | no | no | no | **yes** |
| switch_hi | GPM from 50 % | −0.0197 | yes | yes | yes | yes | yes | yes | no |
| thr_lo | energy threshold 0.95 | −0.0148 | yes | yes | yes | yes | yes | yes | no |
| thr_hi | energy threshold 0.99 | −0.0136 | yes | yes | yes | no | no | no | **yes** |
| basis_lo | 16 basis sequences | −0.0148 | yes | yes | yes | yes | yes | yes | no |
| basis_hi | 64 basis sequences | −0.0139 | yes | yes | yes | yes | yes | yes | no |

**4 flips in 8**, against the PASS-1 precondition of at most 1.
- The claim is fragile to the anchor multiplier in both directions, to an earlier switch point, and to a higher energy threshold.
- In kappa_hi and thr_hi it fails only through P4's task-B guard (and, in thr_hi, P5); P1–P3 hold in both.

## 6. Hand checks for Daniel Friedman's audit asks

These come from the operator's script (`CHECKS/SEC-PG-LLM-H-2026-10-08_hand_checks.py`, 8b6915f) run on his asks, written to `hand_checks.json` with `all_ok: true`. Daniel did not perform them.

- **Repeat pair (#6).** `units_rerun.jsonl` holds exactly the two prescribed units, once each: (seed 651629, width 128, 2 M, `pretrain+pg`) and (seed 651629, width 64, 1 M, `sec`). The scorer reports both identical to their main units in every field except timings. The width-128 unit repeats its pretraining from scratch (`run_heldout.py:17`, `:54-58`).
- **Sensitivity uniqueness (#10).** Each of the 8 cells appears exactly once for each of the 72 (seed, width, tokens) cells: 576 rows, none missing or duplicated. Main (936) and pretraining (72) likewise have nothing missing, duplicated or unexpected.
- **Timers (#27).** `seconds` covers different work across arms, so no SEC-vs-SEC-PG cost comparison is drawn from it. `pg`, `light`, `pgconst` and `gpm_only` include four evaluations (`sec_pg.py:73`); `none`, `sec` and `grid_*` exclude them (`llm/cl.py:125`). Mean `seconds` per run, as recorded and not comparable across arms: pg 89.6, pgconst 89.5, gpm_only 92.3, light 85.5, sec 83.9, grid 84.4–85.5, none 79.3.
- **Chord length (#25).** `path_length` is a checkpoint chord length at stride 100 (`llm/cl.py:72`), not optimizer-step travel. The scorer uses it only in the repeat-pair identity check (`score_llmh.py:44`, `:116`), not in any claim or control.
- **Full precision (#26).** This is from the scorer source, not `hand_checks.json`. The verdict uses unrounded means. The only rounding is T4's preregistered grid-selection rule (`score_llmh.py:76`: five decimals, ties to the smaller λ). Stored losses are full-precision floats.
- **Concurrent load and interruptions.** This is from `interruptions.jsonl` and ledger D103–D104, not `hand_checks.json`.
  - Other processes ran on the same machine during the run: tests, lint, dry pilots, design-draft surrogate checks and workflow tool calls.
  - The container restarted twice. The operator infers that it is reclaimed when the session is idle.
  - The run was resumed each time by the frozen runner's skip-completed rule, after 222 and then 230 completed main units. Units in flight at each restart were re-run from scratch.
  - This is a deficiency for timings and wall-clock only. Losses are expected to be deterministic per unit; the registered repeat pair, the only direct test, is identical.

## 7. Provenance and chronology

These come from the run's own records. No committer date is used as a time.

- **Freeze:** commit `75dc07a`; FREEZE.json sha256 `be060bd6…`.
- **Bitcoin attestation:** OpenTimestamps on the freeze, block 970483, 2026-10-08T11:16:00Z (`anchor_check.json`). Block time + 7,200 s is 2026-10-08T13:16:00Z, and both that time and the anchor check precede the first fetch (`score_llmh.py:122`).
- **Signed tag** `prereg-SEC-PG-LLM-H-2026-10-08`, tag object `e15e2fe`, made by the owner and peeling to `75dc07a`.
  - Its SSH ed25519 signature was verified locally with a tamper control, using the key embedded in the signature.
  - The binding of that key to the owner rests on GitHub's verification alone (`tag_verification.json`, `key_owner_binding`).
  - The tag was on origin at the anchor check (`tag_ok_at_anchor: true`).
- **Anchor check:** 2026-10-09T04:37:29Z, with A1–A7 true. It replaced the earlier check of 01:10Z (060ccb0, `tag_ok_for_draw` false), as `data_step.py:135` prescribes.
- **Draw:** block 970552. First fetch 2026-10-09T04:38:49Z (`draw_log.json`, `draw_attempts.jsonl`).
- **Scorer-computable preconditions:** `bitcoin_attestation_before_first_fetch` and `signed_tag_on_origin_at_anchor` are both true.
- **Interim ledger script:** in `append_result_v2.py`, the `freeze_commit_push_utc` field is a committer date and carries no chronological weight (reporting plan §6).
- **Outside this record:** verifying the tag signature and the attestation against a Bitcoin node is for the reviewers.

## 8. Exposure, compute, memory, and the SEC lineage

- **Exposure.**
  - Five books were drawn: EN 72198 and 49851, FR 61745, DE 43987, and 56066, which was fetched and rejected at S4. None was in `DATA/SEEN.md` at draw time.
  - The frozen runner refuses unregistered books (`run_heldout.py:29-31`). The push of the five rows before the run (`9d75690`) is recorded in the operator's self-declared ledger row D92.
  - The books are public-domain classics and almost certainly in the training data of the language model that wrote the protocol (PREREG.md:225). Whether that makes them LLM-exposed public data under `DATA/SEEN.md`'s scope note is for the reviewers; this document does not judge it.
- **Compute against the preregistered budget (#15).**
  - Summed unit wall times, one thread each: pretraining 6.48 CPU-hours, main 20.85, sensitivity 14.03, rerun 0.07. **Total 41.43 CPU-hours**, about 18 % over the estimate of about 35 in PREREG.md:199.
  - Work lost to the two interruptions is not in that sum.
  - The run was launched at about 04:39Z (ledger D92) and scored at 2026-10-09T16:15:35Z (`run.log:1624`). That is about 11.6 h elapsed including both outages, against PREREG.md:199's "at least 8.7 h".
  - For the last segment, `time` reports real 409m42s and user+sys 27.00 h, against 27.10 h of summed unit wall time (`run.log:1621-1623`).
  - Descriptive only; the concurrent-load caveat of §6 applies.
- **Memory** (PREREG.md:14; description only). The GPM bases held on average 0.448 of the parameter count (`descriptive.basis_frac`).
- **SEC-family qualification (#14), a dated paragraph (2026-10-09).**
  - The Ashes prior-art sweep declared SEC's method KNOWN, except for the one-scalar secant rescaling, which it did not find published (`GENEALOGY/UPSTREAM/ashes_sec4.md:106`, `:107-113`; `GENEALOGY/HISTORICAL_CLARIFICATIONS_2026-10-09.md` C3).
  - In a declared post hoc analysis on seen records, a learner frozen after task 1 was not behind the tuned λ on 24 of the 30 held-out carriers of SCL3, SEC3, SEC4 and SEC5 (`ashes_sec4.md:117,128`; C3).
  - Embers is not independent of Ashes (`GENEALOGY/UPSTREAM/embers_audit.md`; `GENEALOGY/INHERITED_RECORD_ADDENDA_2026-10-07.md:19`; `HISTORICAL_CLARIFICATIONS` C4).
  - Against the transferred constant: SEC-PG beats λ = 5e3 by 0.0226 (P2b), and K2 shows that P1 separates that constant from the grid. The 5e3 arm has no GPM.
  - K5 shows that SEC-PG was not shown to be better than the same GPM schedule with one constant anchor, λ = 1103, the median of SEC's own multiplier over these cells.
- **Endpoint 5 (#4).** This is an engineering study with no CRR content (PREREG.md:11, :17). The operator reads it as not a bridge for endpoint 5 (`CONSTITUTION/PROGRAMME_EXIT_CONDITIONS.md:27`). This REDUCES therefore neither adds to nor resets the count of consecutive FAIL/VOID/REDUCES bridges. A reviewer may disagree.

## 9. Reading

### 9.1 The words fixed by the reporting plan §3 (REDUCES branch)

"Failing control: K5. SEC-PG reduces to a size-matched constant." The route is `append_nonnumeric.py`, with two reviewers.

### 9.2 Additions (not fixed by the plan; listed as departure (c) in §11)

- **Controls that hold.**
  - K3: SEC-PG lowers J by 0.049 nats relative to the light anchor (−0.0493 [−0.0542, −0.0444]).
  - K6: SEC-PG beats GPM as published by 0.107 nats.
  - K4: the light anchor alone does not meet the claim.
- **What the controls do and do not isolate.**
  - Read together, K3 and K6 (which hold) and K5 (which fails) are consistent with SEC-PG's advantage over the grid not depending on the secant's per-cell variation.
  - They do not isolate the switch point or the anchor's overall size:
    - gpm_only differs from SEC-PG in both anchor and switch;
    - switch_hi also meets the claim;
    - the anchor's size was itself set from SEC's multiplier (its median over this study's cells), and J moves strongly with it (kappa_lo +0.0082, kappa_hi −0.0286 against the grid).
  - pgconst was not a registered claimant and was not compared with the grid under any registered rule, so no claim is made for it.
  - Mean J over cells, for description: pgconst 2.3390, SEC-PG 2.3404, grid 2.3546, transferred constant 2.3630, SEC v2 2.3639.
  - This is a reading, not a tested result.
- **Not licensed** (PREREG.md:207-213):
  - any claim that SEC's secant contributes;
  - any cost claim;
  - larger models, other tokenisations, other task pairs, longer task sequences, or real continual-learning benchmarks;
  - the absence of a reversal smaller than 0.01 nats in the 8 M or width-192 strata, or any statement about the width-192 × 8 M cells alone;
  - anything about CRR.

  Intervals cover seed variation only. Every inference is conditional on the one draw of four books (PREREG.md:104).
- **Note for `HEURISTIC/LEDGER.md` (not evidence about CRR).**
  - SEC came from the CRR programme upstream. Its secant rescaling s = clip(c/ρ_F) is the ratio of the loss's chord curvature along the end of pretraining to the Fisher's claim along the same direction (`CRR-LLM-CALIBRATION/SEC_V2_RULE.md:4`).
  - It is the one element of SEC that the Ashes prior-art sweep did not find published.
  - On these held-out books, its per-cell variation was not shown to add anything beyond one constant of matched size.
  - That is consistent in direction with three earlier records, but none of them tests the same question:
    - the upstream KNOWN verdict, which did not cover the secant;
    - the 24/30 frozen-learner control, which concerns the family's success criterion;
    - SEC-OBS1-H's H3 FAIL, which concerns CRR path quantities as predictors (`RUNS/SEC-OBS1-H-2026-10-08/RESULT.md:22`).

## 10. Ledger route and hand-off

- **Terminal row.** REDUCES goes through `scripts/append_nonnumeric.py`.
  - Its input needs the study id; the verdict, which must be exactly `REDUCES` (`append_nonnumeric.py:16`), with the scorer's parenthetical placed in `reason`; `reviewer`; a different `second_reviewer`; the freeze sha256; and the bound evidence.
  - The operator does not append it. The terminal row closing `SEC-PG-LLM-H-2026-10-08:FROZEN:6` waits for two named reviewers.
- **Receipts** are in `receipts/SEC-PG-LLM-H-2026-10-08/`: `receipt.json`, `exposure_log.json`, `data_manifest.json`, and `rerun_a.json` and `rerun_b.json`, both byte-identical to `score.json`. The receipt is self-declared by the operator and is not independent verification.
- **For the reviewers:**
  - verify the tag signature (`git tag -v` with the owner's key);
  - verify the attestation against a Bitcoin node;
  - judge exposure under the scope note;
  - re-execute the scorer (`python3 -I studies/SEC-PG-LLM-H-2026-10-08/score_llmh.py`; it also rewrites `score.txt`, whose first line is a time) and compare its stdout with `score.json`;
  - check this document against `score.json`.
- **No pass to promote.** An independent re-run under PREREG.md:221 would still test the REDUCES verdict.

## 11. Departures from the reporting plan

Plan line 3 requires every departure to be listed here.

- **(a) Per-seed values.** They are given for P1, P2a, P2b, P3a, P3b and K5. For the other quantities the per-seed values are only in `score.json`.
- **(b) Control conditions.** The first version omitted each control's condition; §3 now states them.
- **(c) Additions in §9.2.** These go beyond the plan's §3 words for REDUCES: the controls-that-hold summary, the paragraph on what the controls do and do not isolate, and the note for the heuristic ledger.
- **(d) #14.** The SEC-family paragraph is written as a dated list rather than "one dated paragraph". It now carries the `embers_audit.md` citation.
- **(e) #15.** The first version omitted the start and end times; §8 now gives them.
- **(f) "Dry pilots".** These were dropped from the concurrent-load list in the first version and are restored in §6.
- **(g) First fetch.** The first version cited it from `draw_log.json` only; §7 now also cites `draw_attempts.jsonl`.
- **(h) The two interruptions.** The plan did not foresee them. They are reported as a timing-only deficiency (§6, §8).

## 12. Separate-context verification

A separate context checked the first version of this document on 2026-10-09. It is the same underlying model, so this is not independent review.

**What it confirmed:**
- every number in the first version against `score.json`;
- the verdict line, the grade and the route;
- the CPU-hours, recomputed from the unit files;
- the provenance records;
- 23 cited file:line references;
- one re-execution of the scorer, byte-identical to `score.json`. The scorer's own rewrite of `score.txt` was restored to the original bytes.

**Its findings and how each was handled:**
- **Two major findings**, both fixed:
  - an overclaim about "what carries the gain" (§9.2 rewritten);
  - the absence of a departures section and a §9 heading that overstated the plan's coverage (§9 split and §11 added).
- **Thirteen minor findings**, all fixed:
  - equivalence language for K5;
  - "agrees with" changed to "consistent in direction";
  - the C3/C4 citation;
  - the statement about path_length's use;
  - a cross-reference;
  - the admissibility wording;
  - per-seed values and conditions;
  - start and end times;
  - the attribution in the §6 heading;
  - inference stated as fact;
  - the incomplete "not licensed" list;
  - memory;
  - the K3 wording.
- **Seven notes**, all taken up: the P5 decomposition, the chronology evidence, D92 being self-declared, the provenance details, the `reason` field, the PASS-2 sentence and the pgconst λ check.
