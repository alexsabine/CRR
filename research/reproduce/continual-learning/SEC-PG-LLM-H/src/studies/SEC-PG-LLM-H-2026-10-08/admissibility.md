# SEC-PG-LLM-H: bridge and admissibility (written before the freeze, 2026-10-08)

**Bridge.** None to CRR. The study tests an engineering schedule built from two published parts: a diagonal-Fisher quadratic anchor applied as an adaptive-metric proximal step (EWC family), and GPM update projection (Saha et al. 2021). It runs inside T4's learner and benchmark. The quantities are losses of a byte-level language model on held-out text windows. There is no event detection, no fitted law and no target feature that the rule could encode.

## Is the learner capable, and is the task informative? (G3)

T4 measured this learner on its development texts, in 32 cells (`studies/SEC-PG-LLM-2026-10-08/t4_margins.json`):

* without an anchor, the old-task test loss rises 0.50–1.26 nats above the frozen model's (median 0.94);
* the new-task test loss falls 0.92–2.34 nats below the frozen model's (median 1.58);
* the grid beats no anchor by 0.021–0.156 in J (median 0.069), with an interior optimum in 26 of 32 cells.

The held-out texts are new, so this is re-checked per cell by a registered screen, not assumed. The screens' thresholds (0.10 and 0.5 nats) and K1's 0.01 sit well below T4's smallest margins.

* **Forgetting is real:** A_test(none) − A_test(frozen) ≥ 0.10.
* **The new task is learnable:** B_test(frozen) − B_test(none) ≥ 0.5.
* **Gate:** if fewer than 80 % of the 72 cells pass both, the verdict is NOT DECIDABLE. Every cell is listed either way.

## Can the criterion discriminate?

* **K1, positive control.** The grid must beat no anchor by at least 0.01 in J, with the lower bound above 0. If anchoring did not matter, P1 and P2 would say nothing, and the verdict is NOT DECIDABLE (UNINFORMATIVE).
* **K2, instrument check.** The transferred constant must not itself meet P1 (upper bound of J(const) − J(grid) > 0.005). Otherwise P1 cannot separate a one-run constant from the six-run grid.

  On T4's development cells, const − grid was +0.0062 in J on average (`studies/SEC-PG-LLM-2026-10-08/t4_margins.json`), so the margin is real but not large. An earlier draft used the frozen learner here; it could not fail, because the frozen model is 1.43 nats worse than the grid on task B on average.

  P2 independently requires SEC-PG to beat the constant by 0.005.

## Are the claimed ingredients necessary? (P6, R7 reduction)

* **K3:** SEC-PG must beat its own anchor without projection (the light anchor alone), with the upper bound below 0.
* **K4:** the light anchor alone must not meet the claim.
* **K5:** SEC-PG must beat the same GPM schedule with a constant anchor of matched size: λ is the median, over the study's cells, of SEC-PG's own multiplier 10 s/16, fixed after pretraining and before any task-B run. This is R7's "no constant reduction": without it, a gain could come from projection plus a fixed anchor, not from SEC's per-cell calibration.

  An earlier draft used 5e3/16 = 312.5, which is about a third of SEC-PG's typical multiplier on development data. That comparison would have been too easy to win.
* **K6:** SEC-PG must beat GPM as published, with projection from the first task-B step and no anchor, on the same four maps. This is the closest published method; the delayed switch and the anchor are SEC-PG's additions.

If any of K3–K6 fails while P1–P5 hold, the verdict is REDUCES, naming the simpler rule that accounts for the result. The transferred constant λ = 5e3 is in P2, so a schedule that only ties the cheapest one-run comparator fails the claim outright.

## Is the data held out? (R11, G5)

* The books are drawn after the freeze and after the Bitcoin attestation, by a key that includes the hash of block 970552. That height was fixed in the frozen code about 12 hours ahead of the chain tip, so the hash was unknowable at the freeze and cannot be chosen afterwards.
* Candidates already in `DATA/SEEN.md` at draw time are skipped.
* The pools are built from catalog metadata (`pools.json`). They exclude every Gutenberg book in `DATA/SEEN.md` and every work by those books' authors.
* The register lacked three books that RT1-PR1 opened on 2026-10-06 (Gutenberg 84, 1661 and 98). They were registered on 2026-10-08 before the pools were rebuilt, and their authors are excluded.
* Every fetched file is registered as SEEN at the data step, admitted or not, as LLM-exposed public text.

Limit: the texts are public-domain classics and are probably in the training data of the language model that wrote this protocol. The learner is trained from scratch, so that exposure cannot reach it. `DATA/SEEN.md`'s scope note treats public benchmarks as SEEN for an LLM collaborator; whether Gutenberg fiction counts as such is left to the reviewer, and recorded here.

## Exclusions and incidents (registered)

* **Non-finite results.** A non-finite loss in SEC-PG or a sensitivity run is replaced by 10 nats (a loss for the claim) and listed. In any other arm, the verdict is NOT DECIDABLE with the units listed, because a replacement there would favour the claim. No cell, seed or arm is dropped after the run.
* **Missing units.** If any registered unit is missing at scoring, the verdict is NOT DECIDABLE.
* **Interruptions.** The runner resumes and never re-runs a completed unit. A unit in progress at an interruption restarts from scratch, and the runs are deterministic. A truncated output line is ignored and its unit re-run. A pretraining cache left truncated is rebuilt from scratch.
* **Fetch failures.** Only HTTP 404 or 410 rejects a candidate. Other failures stop the draw without deciding the candidate, and a later re-run resumes from the recorded attempts.
* **Frozen files.** The runner and the scorer both refuse to proceed if any frozen file differs from `FREEZE.json`'s record.
