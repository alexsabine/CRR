# P23-AGING-CRR report (OD-49, 2026-10-16): does CRR's account of time say when, and from what, to repair?

**Status.** Frozen test: protocol at commit 7fd6b14, before any test seed. Calibration used development seeds 0–9;
the test used seeds 1000–1049 at noise 0.15, plus a sensitivity run at noise 0.125. The subject is the ageing NCA of
Pio-Lopez, Hartl & Levin (2025), run on the authors' code unchanged. CPU only, no API spend. One builder.

**Question.** The owner asked how CRR applies to the repair finding of P23-AGING (resetting damaged cells to the
primordial state restores the face), and in particular to its *timing*. CRR says two things about time:
- **when:** a cut happens when accumulated change, the Fisher–Rao coherence, first reaches a fixed size;
- **from what:** regeneration draws on the past, weighting recent occasions by q^age.

`DESIGN.md` §1 derives each operation for this system and sets each against its strongest ordinary rival.

## Answer

**CRR earns no credit under the frozen criteria.**

1. **Timing.** Repairing at CRR cuts is no better than repairing on a plain clock at the same rate: +0.26
   [−0.31, +0.93], equivalent; 0.125 sensitivity, −0.24, equivalent. It is slightly worse, and costs 76 more cell
   writes, than an ordinary early trigger: repair as soon as any organ cell is wrong, at most once per 15 steps
   (−0.84 [−1.37, −0.26]; 0.125 sensitivity, −1.45).
2. **Content.** CRR's past-weighted seed does worse than the paper's primordial reset: −1.59 [−2.19, −1.08], worse
   in 49 of 50 lifetimes, verdict undetermined because |mean| < 2. Calibration showed the same: fitness rises with
   q all the way to q = 1, and q = 1 *is* the paper's primordial reset. Weighting recent occasions mixes the
   organ's drifting, noise-damaged states into the seed. Sampling the seed at CRR cuts or on a clock makes no
   difference (+0.04, equivalent).
3. **What the CRR-guided search did find.** Two ordinary improvements over the paper:
   - **Repairing early and often** beats the paper's damage threshold by +10.8 [+10.0, +11.6] (50 of 50
     lifetimes). It matches repairing every step at a tenth of the cell writes (446.9 against 4,436.8). Any early,
     frequent trigger gets this gain; CRR's own trigger does not add to it.
   - **Writing the canonical mature organ state** instead of the primordial one adds +3.0 [+2.2, +4.0] with a third
     of the writes. Combined with frequent repair it reaches 224.8–226.5 with every organ intact 99–100% of the
     time. That is the level the evolved controller holds with no noise at all (226), so frequent target repair
     cancels the organ damage completely.
4. **Correspondence (no credit).** The paper's own method is the q = 1 member of CRR's regeneration family, with the
   primordial state as the prior. "Restore the most recent state" is q = 0. CRR places the two familiar repairs on
   one axis. On that axis the data favour the end that ignores the recent past.

## 1. How CRR was applied (summary of DESIGN.md §1)

- **Carrier.** Each organ cell's cell-type distribution (softmax of its three type channels). The coherence step is
  the Fisher–Rao arc of the product distribution.
- **Cut.** Coherence since the last cut first reaches a = π, the Fisher–Rao distance between two pure cell types:
  one whole cell's worth of type change. It is fixed from the geometry, not tuned on outcomes.
- **Regeneration.** m ← q·m + (1 − q)·Φ, where Φ is the mean organ state over the completed occasion and m₀ is the
  primordial organ state (CORE §V, past-only). q was calibrated (frozen at 0.99).
- **Write.** The paper's method-B impulse: write the content into the wrongly expressed organ cells and clear their
  RNN memory.
- **Must-pass, all exact on the 10 development seeds.** The re-implemented paper repair reproduces the authors' run
  cell for cell; CRR with q = 1 reproduces it too; the no-repair arm reproduces P23-AGING.

## 2. Frozen test (seeds 1000–1049, noise 0.15)

| arm | when | content | late fitness | cell writes | all organs intact (share of time) |
|---|---|---|---|---|---|
| NONE | — | — | 196.3 | 0 | 0.21 |
| C_PRIM (paper method B) | damage ≤ 0.6 | primordial | 211.6 | 130 | 0.85 |
| C_CKPT | damage ≤ 0.6 | healthy checkpoint | 209.8 | 172 | 0.81 |
| C_CRR | damage ≤ 0.6 | CRR seed (q 0.99) | 210.0 | 169 | 0.76 |
| C_EMACLOCK | damage ≤ 0.6 | EMA seed on a clock | 210.0 | 184 | 0.76 |
| C_TARGET | damage ≤ 0.6 | canonical organ state | 214.6 | 43 | 1.00 |
| S_CRR | every CRR cut | primordial | 222.4 | 447 | 0.94 |
| S_CLOCK | clock, matched rate | primordial | 222.1 | 445 | 0.88 |
| S_ANY | any wrong cell, every ≤ 15 steps | primordial | **223.2** | 370 | 0.91 |
| S_IMMEDIATE | every step | primordial | 222.1 | 4,437 | 0.99 |
| S_CRRFULL | every CRR cut | CRR seed | 220.6 | 511 | 0.91 |
| S_CRR_TARGET | every CRR cut | canonical | 224.8 | 57 | 0.99 |
| S_CLOCK_TARGET | clock | canonical | **226.5** | 50 | 1.00 |

| id | contrast | mean diff [95% CI] | wins / losses | verdict | prediction |
|---|---|---|---|---|---|
| P1 | S_CRR − S_CLOCK | +0.26 [−0.31, +0.93] | 11 / 39 | equivalent | equivalent ✓ |
| P2 | S_CRR − S_ANY | −0.84 [−1.37, −0.26] | 7 / 43 | equivalent | not better ✓ |
| P3 | C_CRR − C_PRIM | −1.59 [−2.19, −1.08] | 1 / 49 | undetermined (worse) | not better ✓ |
| P4 | C_CRR − C_EMACLOCK | +0.04 [−0.55, +0.66] | 26 / 24 | equivalent | equivalent ✓ |
| P5 | S_CRR − C_PRIM | +10.78 [+10.03, +11.58] | 50 / 0 | different | different ✓ |

Secondary (no verdict):
- C_TARGET − C_PRIM: +3.02 [+2.18, +3.96], 50/0.
- S_CRR_TARGET − S_CRR: +2.40.
- S_CRR_TARGET − S_CLOCK_TARGET: −1.73.
- S_CRRFULL − S_CRR: −1.81.
- C_CKPT − C_PRIM: −1.80.
- S_CRR − S_IMMEDIATE: +0.30, at 3,990 fewer writes.

**Sensitivity, noise 0.125.** The matched clock interval was fixed by the frozen rule at 34, 26 and 14 steps.

| contrast | mean diff | verdict |
|---|---|---|
| S_CRR − S_CLOCK | −0.24 | equivalent |
| S_CRR − S_ANY | −1.45 | equivalent |
| C_CRR − C_PRIM | −0.31 | equivalent |
| S_CRR − C_PRIM | +8.65 | different |

Every prediction in the frozen table came true. Under the frozen criteria, CRR earns no credit.

## 3. Reading

- **Why the CRR cut adds nothing over a clock.** Native theory: event-triggered (Lebesgue) sampling beats periodic
  (Riemann) sampling at the same average rate, even for steady random disturbances, *when the event is defined on
  the error being controlled* (Åström & Bernhardsson 2002). The early damage trigger is such an event: a wrong cell is
  the error. It does slightly better than the clock (223.2 against 222.1) with fewer writes. The CRR cut is defined
  on accumulated cell-type *activity*. Under steady noise that activity grows almost steadily, and much of it is
  harmless fluctuation in cells that stay correct. So the cut behaves like a clock, and it is no better than one.
- **Why the early damage trigger is slightly better.** It reacts to the thing that matters, a wrong cell, rather than
  to type activity, which also counts harmless fluctuation. It wastes fewer writes.
- **Why recent-weighted content hurts.** The organ's recent past is noisier and already drifting. In this system,
  the most useful information about what an organ should be is in its oldest record (the genome-coded primordial
  state) or in the canonical target, not in its recent history. This is the same lesson as P23-AGING from the other
  side: the tissue keeps no useful memory, so regenerating from the realised recent past cannot help.
- **What CRR contributed.** Posing timing and content as one design question, and placing the paper's repair and
  checkpoint rollback on a single q axis, led to the two practical improvements: repair early and often, and write
  the canonical organ state. Neither improvement is a CRR operation, and the CRR operations themselves (Fisher–Rao
  cut, past-weighted seed) were matched or beaten by ordinary rivals.

## 4. Grades

| CRR element | result | grade |
|---|---|---|
| Cut timing (Fisher–Rao arc first passage) | = matched clock; slightly below an early damage trigger | **NOTHING** (native event-triggered control triggers on the error; the CRR cut triggers on activity and behaves like a clock under steady noise) |
| Past-weighted regeneration (q) | best at q = 1, the paper's primordial reset; recent weighting hurts | **NOTHING**; mildly **MISLED** (recency weighting reduced fitness by 1.6) |
| Design lens (timing × content as one question; q axis) | surfaced "repair early and often" (+10.8) and "write the canonical target" (+3.0) | **DISTINCTION** as heuristic, not as mechanism |

## 5. Departures and failures (recorded before interpretation)

- Two rivals and two content variants were added after the first calibration and before the freeze (DESIGN.md §3):
  S_ANY, and the *_TARGET variants. They were added because the first calibration suggested that early repair, not
  the CRR cut, carried the gain, and that the canonical target beat the primordial state. The freeze includes them.
- The calibrated q (0.99) is the best *interior* value. The boundary q = 1, the paper's own method, was better still
  in calibration. This was recorded before the test.
- The 0.125 sensitivity used clock intervals fixed by the frozen rule from its own S_CRR run (34, 26, 14).
- A first draft of §3 said event-triggering theory predicts no gain under steady noise. That was wrong: Åström &
  Bernhardsson show an advantage for error-based events even under steady noise. It was corrected before commit, and
  the corrected reading fits the data better (the error-based trigger beat the clock; the activity-based CRR cut did
  not).
- Not tested: bursty damage (for example sudden organ ablations), where event-triggered timing should beat a clock
  and CRR's cut might show its value. That is the natural next experiment (§6).

## 6. Single most informative next experiment

Make the damage **bursty** instead of steady. Remove organ cells at random times (an injury process), add to the
steady noise, then rerun the frozen timing contrasts:
- CRR cut against a matched clock;
- CRR cut against the early damage trigger.

Under bursty disturbances, cell-type activity could rise *before* organ cells turn wrong, for example as a damaged
neighbourhood destabilises. That is the one place an activity-based cut might anticipate damage that an
error-based trigger only sees afterwards. If CRR's Fisher–Rao cut beats both the clock and the early damage trigger
there, CRR's timing would earn real credit. If the damage trigger still wins, the CRR cut has no role in repair
scheduling for this system.
