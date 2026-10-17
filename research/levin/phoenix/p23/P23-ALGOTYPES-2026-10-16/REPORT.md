# P23-ALGOTYPES report (OD-47, 2026-10-16): CRR checks on self-sorting arrays and algotypes

**Status.** Exploratory audit under enquiry P23, written for the owner's request "run more CRR checks on the work of
Michael Levin and algotypes". It reproduces the results with the authors' own code (cell_research `1fd2bd59`,
unchanged), tests ordinary null models, and adds one CRR-explicit check (commitment M7). Nothing was preregistered or
frozen. **No result here is a Phoenix finding**; each is graded as a reproduction, a reduction or a failure (§8).
CPU only, no API spend. Paper: Zhang, Goldstein & Levin, arXiv:2401.05375 (*Adaptive Behavior*).

**Answer.**
1. **Algotype aggregation is real and reproduces with the official code,** but its peaks are lower than the
   paper's: 0.52–0.65 here against the paper's 0.62–0.72. In unique-value chimeric arrays, the peak of the mean
   aggregation curve exceeds the matched inert-label control by +0.07 (Bubble-Selection), +0.11 (Bubble-Insertion), +0.16 (Selection-Insertion) and +0.19 (all three).
   Welch t is 10.6–27.8 on per-run time averages. The paper's peaks (0.65–0.72) and its negative control
   (0.57–0.65, sd 0.04–0.05) match the **mean of each run's own maximum** (control 0.55–0.60, sd 0.03–0.04). They do
   not match the peak of the mean curve, where the inert control sits at 0.50. A per-run maximum of a noisy curve
   is high even when nothing clusters.
2. **A difference in tempo alone produces the same transient clustering.** Every cell runs the identical rule and
   carries an inert label; half the cells act more often. That peaks at 0.58 (Bubble, 16× rate) and 0.63
   (Selection, 16×), the range of the two-type chimeric peaks (0.57–0.65), and it returns to chance by the end.
3. **There is no setpoint.** With duplicated values, segregation persists to the end, but its final level runs from
   0.44 to 0.78, depending on how many cells share a value and on array length. The paper's "segregation value of
   0.69" is one point on that curve (100 cells, ten per value: 0.69–0.70 here). The persistence has an ordinary
   mechanism. Bubble and insertion cells never swap equal values, so they perform a *stable* sort. Any array they
   sort, mixed or not, ends in the same arrangement, fixed by the initial array (200/200 identical end states for
   BI and the BB control). That arrangement carries no information about type (0.49). Selection cells make long
   jumps, which do reorder equal values, and the jumps leave them on the left of each block of equal values (mean
   relative position 0.31; bubble and insertion cells 0.68–0.69).
4. **"Delayed gratification" is a property of the progress measure, not of the cells.**
   - Every swap the official bubble and insertion cells make lowers the inversion count (the true distance to
     sorted) by exactly 1, with 0 exceptions in 1,613,934 recorded steps, frozen cells included. The cells never
     move away from the goal; only the paper's adjacent-pair "monotonicity error" rises and falls.
   - The official DG function has a defect. When a trajectory ends on a rise in error, it returns the sum of its
     episodes instead of their mean. Only frozen-cell runs that stop unsorted can end that way, so the defect
     inflates DG in exactly the conditions the trend claim rests on.
   - With the defect corrected, DG with the official cells does not rise with frozen cells:
     - Bubble is flat: 0.39 with none, 0.38–0.39 with 1–5 (slope −0.002 per frozen cell [95% CI −0.006, +0.002]).
     - Insertion falls: 1.08 → 0.58 (slope −0.14 [−0.16, −0.12]).
   - A strategy-free null, which swaps random out-of-order pairs, matches the official cells at every frozen-cell
     count. Under the defective statistic, the same null even "shows" DG rising with frozen cells.
5. **CRR check (M7: are forms productions of history?).** Two arrays identical in every value and algotype can
   repair an injury completely differently, depending on how each was formed. With the same 20-cell injury, every
   continuation of every freshly assembled array re-sorted (50/50 seeds, about 85 swaps). No sorted-by-history
   array re-sorted (0/50; bubble-selection livelocks at about 15,000 swaps, selection-insertion deadlocks). The
   official classes give the same result: 0/20 history copies re-sorted within 30 s for each of BS and SI, against
   20/20 fresh copies.
   The whole effect sits in stored state: each selection cell's position pointer. Pointers can only advance, so
   after an injury they overshoot and never come back. Renewing the pointers only inside the injured window
   (LOCAL) repairs exactly as well as building every cell fresh. An ordinary hidden-state (Markov) model accounts
   for all of it; nothing beyond the full current state is needed. This agrees with the 2026-10-06 origin-of-life
   result (O4) and leaves ND-2 (produced versus ingressed forms) NOT DECIDABLE.

## 1. Sources and set-up

- **Paper.** Local PDF, sha256 `f4e78ddc8a83f7c983d088713c916adac01c4c90eebe28d1bc9018ddef0098ca`. Claims checked:
  chimeric aggregation and its negative control; swap counts of mixed arrays; duplicate-value aggregation and the
  "specific parameter value (e.g., a segregation value of 0.69)"; delayed gratification with frozen cells.
  The opposite-direction ("cross-purposes") experiment was **not checked**.
- **Official code.** github.com/Zhangtaining/cell_research at `1fd2bd59`. `run_official.py` imports its classes
  unchanged and reproduces the set-up of `multithread_sorting_cell_aggregation_analysis.py`: one Python thread per
  cell under one lock, one cell group spanning the array, run until sorted. Its plotting and tkinter imports are
  left out. Inert-label controls give half the cells label 9 (and a third, label 8, in BBB), with the rule
  unchanged. Each run is seeded, but thread interleaving is not, so official runs repeat only in distribution.
- **Aggregation statistic.** The official `get_aggregation_value_avg`: the share of positions whose right
  neighbour has the same type, with the last position counted as 0. The curve takes the snapshot at
  `int((len-1)·p)` for p = 0, 0.01, …, 1. The "peak" is the maximum of the mean curve (`analyze_runs.py`).
- **Prior art consulted.** alexbaker0/Self-sorting-cells (`3ebc155`), an independent JavaScript replication. It
  already reports three of the points below:
  - the inversion count never rises (with one sort direction);
  - delayed gratification appears only under the adjacent-pair measure;
  - a tags-only control removes the clustering in its model.

  It did not reproduce the DG–frozen-cell trend and suggests its random-order rounds as the reason. This study
  re-checks all three with the authors' own code. The speed null (§4), the setpoint sweep and tie-block mechanism
  (§5), the DG statistic defect (§6) and the history check (§7) are, as far as I found, not in the paper or that
  replication. Novelty is not claimed: no prior-art review was run beyond these two sources.

## 2. Reproduction with the official code (unique values, 100 cells, 100 runs each)

| mix | swaps (paper) | peak of mean curve [95% CI] at % of run | paper peak at % | excess over inert control at peak | time-avg excess, Welch t | mean of per-run max (sd) |
|---|---|---|---|---|---|---|
| BB inert control | 2511 | 0.502 [0.493, 0.512] | 0.65 / 0.61 / 0.57 (their controls) | — | — | 0.601 (0.029) |
| SS inert control | 1606 | 0.506 [0.497, 0.516] | | — | — | 0.599 (0.034) |
| II inert control | 2511 | 0.493 [0.484, 0.502] | | — | — | 0.551 (0.041) |
| BBB inert control (3 labels) | 2511 | 0.332 [0.325, 0.339] | | — | — | 0.427 (0.027) |
| BS | 1919 (1740.9) | 0.573 [0.562, 0.583] at 27% | 0.72 at 42% | +0.074 | +0.034, t = 10.6 | 0.645 (0.040) |
| BI | 2511 (2476.0) | 0.610 [0.601, 0.619] at 25% | 0.65 at 21% | +0.110 | +0.062, t = 17.5 | 0.657 (0.040) |
| SI | 1678 (1534.8) | 0.650 [0.639, 0.661] at 30% | 0.69 at 19% | +0.160 | +0.082, t = 22.9 | 0.692 (0.047) |
| BSI | 1960 | 0.518 [0.505, 0.529] at 30% | 0.62 at 22% | +0.193 (vs BBB) | +0.096, t = 27.8 | 0.567 (0.047) |

- **The effect is real.** Every chimeric mix exceeds its inert control. The control shows the excess comes from
  the rules interacting, not from the metric.
- **The paper's control is not reproduced as a curve peak.** Its stated values match the mean of per-run maxima
  (sd 0.03–0.04 against the paper's 0.04–0.05), and its BI and SI peaks match per-run maxima too (0.657 vs 0.65;
  0.692 vs 0.69). That is consistent with the paper averaging run-wise maxima. It is not confirmed: the official
  analysis script plots the mean curve. The honest effect size is the excess over control: +0.07 to +0.19 at the
  peak, +0.03 to +0.10 averaged over the run.
- **Swap counts.** Bubble and insertion swap only adjacent out-of-order pairs, so their swap count equals the
  initial inversion count exactly. Its mean for random permutations is n(n−1)/4 = 2,475. The paper's "Bubble-
  Insertion mix took 2476.02 steps, between the pure sorts" is therefore an identity, not an efficiency finding.
  The official runs give 2,511, the inversion mean of these 100 seeded arrays. The paper's BS and SI counts are
  9–10% lower than the official code's. Its version of the selection cell may have differed.

## 3. Fast simulator and scheduling (`sim.py`)

A seeded re-implementation of the three rules was needed for thousands of runs. Scheduling matters for selection
cells:

| mean swaps | SS | BS | SI | BI |
|---|---|---|---|---|
| official threads | 1606 | 1919 | 1678 | 2511 |
| uniform random activation | 1014 | 1774 | 1556 | 2511 |
| random activation, bursts | ≈1196 | | | |
| round-robin in creation order | 1587–1600 | 1891–1917 | 1646–1670 | 2474–2487 |

Round-robin (each cell acts once per cycle, in creation order) reproduces the official counts. It also reproduces
the aggregation peaks: BS 0.571, BI 0.608, SI 0.636 and BSI 0.513, against official 0.573, 0.610, 0.650 and 0.518.
Inert controls give 0.49–0.50 (BBB 0.33). Round-robin is the primary scheduling below. Every key result was also run
under uniform random activation (`results/random_scheduling/`), and the conclusions are the same.

## 4. Speed-only null: does tempo alone make labels cluster?

Inert labels on an identical rule, with the labelled half acting r times per cycle (round-robin, 200 runs each):

| null | r = 2 | 4 | 8 | 16 | 64 |
|---|---|---|---|---|---|
| Bubble, peak of mean curve | 0.507 | 0.530 | 0.561 | 0.584 | 0.597 |
| Selection, peak of mean curve | | 0.588 | | 0.629 | |

- Insertion has no tempo effect (0.492 at r = 16), because only one insertion cell is ever eligible to move.
- The tempo null returns to chance by the end: final 0.487–0.494, including with duplicated values.
- **Aggregation of the chimeric size needs no interaction between algotypes**, only a difference in how fast two
  subpopulations move.
- This does not show that the chimeric effect *is* tempo. The algotypes differ in more than rate; selection cells
  jump. But the ordinary rival is strong enough that a chimeric peak by itself is not evidence of an emergent
  "competency" (see §9).

## 5. Duplicate values: persistent segregation without a setpoint

Final aggregation in the paper's duplicate-value design (round-robin, 200 runs per cell). k is the number of cells
sharing each value:

| mix | n=100, k=2 | 5 | 10 | 20 | 25 | 50 | n=200, k=10 | 20 | 40 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|
| BS | 0.445 | 0.581 | 0.691 | 0.711 | 0.703 | 0.603 | 0.730 | 0.780 | 0.764 | 0.743 |
| SI | 0.435 | 0.595 | 0.703 | 0.707 | 0.695 | 0.558 | 0.739 | 0.776 | 0.737 | 0.718 |
| BI | 0.490 | 0.498 | 0.490 | 0.494 | 0.491 | 0.489 | 0.497 | 0.497 | 0.497 | 0.495 |
| BB control | 0.490 | 0.498 | 0.490 | 0.494 | 0.491 | 0.489 | 0.497 | 0.497 | 0.497 | 0.495 |

BI and BB rows are identical: at the same seed they end in the same arrangement (200/200 at n = 100, k = 10).

- **No setpoint.** Final segregation is not regulated to 0.69. It varies from 0.44 to 0.78 with block size and
  array length, peaking at intermediate k. The paper's 0.69 (BS) and 0.71 (SI) at n = 100, k = 10 are reproduced
  (0.691 and 0.703), along with BI's transient-only behaviour (peak 0.607 at 17%). They are one point on a curve
  set by geometry.
- **Mechanism (`tie_blocks.py`).**
  - Bubble and insertion only swap strictly out-of-order neighbours, so both are *stable* sorts. Whatever the mix
    of the two, or their tempo, the end state is the stable-sort order of the initial array. It is independent of
    type, so final aggregation is at chance: BI and BB end identical, and the tempo null in blocks ends at
    0.499/0.501.
  - A selection cell jumps into the first slot that holds a larger value, carrying the occupant back past any
    equal values in between. That breaks stability, and it leaves selection cells at the left of each block of
    equal values (mean relative position 0.31–0.32) and their partners at the right (0.68–0.69).

  The ordinary rival is "persistent segregation = one non-stable rule mixed with a stable one". It accounts for
  the persistence and predicts exactly zero for BI, which the setpoint reading does not.
- **Official code** at the paper's configuration (n = 100, k = 10): 100 runs per condition (97 for BI):
  - Final aggregation: BS 0.688, SI 0.701, BI 0.492, BB control 0.492.
  - BI and BB end in identical arrangements in 97/97 runs. The official threads are stable sorts too.
  - Tie-block positions: S 0.317/0.309, B 0.683, I 0.691. At n = 200, k = 20: BS 0.777 (100 runs), SI 0.772
    (37 runs).
  - These match the simulator at every point (0.691, 0.703, 0.490, 0.490; 0.780, 0.776).

## 6. Delayed gratification (DG) with frozen cells

The paper reports that cell-view bubble and insertion "deploy Delayed Gratification in a context-sensitive manner".
Its DG rises with the number of frozen cells: bubble 0.24 → 0.37 and insertion 1.10 → 1.19 for 0 → 3 frozen cells.

**Set-up (`dg_official.py`).**
- Official cells, with the set-up of `multithread_cell_sorting_with_frozen_steps.py`: values 0..99 shuffled; F
  cells frozen with `random.randint` (as there, a cell may be drawn twice); frozen threads not started; stop when
  no cell "should move".
- F = 0..5. There are 100 runs at F = 0; at F ≥ 1 there are 50, or 69 (bubble, F = 1) and 67 (insertion,
  F = 3) where a stopped 100-run pass had gone further (§10).
- DG computed by the official functions, extracted unchanged from `analysis/delay_gratification_analysis.py`.

**Checks added.**
- (a) Inversion count after every step.
- (b) A strategy-free null:
  - It swaps a uniformly random adjacent out-of-order pair that a non-frozen cell could initiate, under the same
    frozen rule.
  - It uses the same stopping rule.
  - It has no cells, no direction preference and no possible "context sensitivity".
- (c) The official statistic with one correction (below).

**Results** (official cells; 100 runs at F = 0, 50–69 at F ≥ 1; DG is the mean with a 95% bootstrap interval):

| algorithm, F frozen | paper DG | official statistic: mean (median) | corrected: official cells | corrected: strategy-free null | runs ending on a rise | ended sorted |
|---|---|---|---|---|---|---|
| bubble, 0 | 0.24 | 0.392 (0.394) | 0.392 [0.386, 0.398] | 0.380 [0.374, 0.387] | 0% | 100% |
| bubble, 1 | 0.29 | **6.019** (0.387) | 0.383 [0.376, 0.390] | 0.377 [0.371, 0.383] | 4% | 86% |
| bubble, 2 | 0.32 | 0.385 (0.377) | 0.385 [0.376, 0.394] | 0.380 [0.373, 0.388] | 0% | 46% |
| bubble, 3 | 0.37 | 0.387 (0.385) | 0.387 [0.377, 0.396] | 0.384 [0.375, 0.395] | 0% | 16% |
| bubble, 4 | — | 0.387 (0.385) | 0.387 [0.378, 0.397] | 0.382 [0.372, 0.393] | 0% | 2% |
| bubble, 5 | — | 0.384 (0.380) | 0.384 [0.372, 0.395] | 0.394 [0.383, 0.405] | 0% | 0% |
| insertion, 0 | 1.10 | 1.083 (1.068) | 1.083 [1.052, 1.113] | 1.083 (identical) | 0% | 100% |
| insertion, 1 | 1.13 | 0.891 (0.869) | 0.891 [0.831, 0.950] | 0.877 [0.819, 0.934] | 0% | 2% |
| insertion, 2 | 1.15 | 0.732 (0.729) | 0.732 [0.671, 0.795] | 0.730 [0.670, 0.791] | 0% | 0% |
| insertion, 3 | 1.19 | **1.391** (0.651) | 0.683 [0.634, 0.732] | 0.681 [0.633, 0.731] | 1% | 0% |
| insertion, 4 | — | **1.514** (0.593) | 0.591 [0.543, 0.644] | 0.586 [0.540, 0.637] | 2% | 0% |
| insertion, 5 | — | **2.534** (0.578) | 0.583 [0.537, 0.631] | 0.568 [0.523, 0.619] | 4% | 0% |

- **Inversions.** In every run, every recorded step (1,613,934 steps over 736 runs) lowered the inversion count by
  exactly 1. Frozen cells change *which* out-of-order pairs get swapped and *when* the run stops. They never cause
  a move away from the sorted order.
- **Trend (corrected statistic, F = 0–3, least-squares slope per frozen cell).**
  - Bubble: official cells −0.002 [−0.006, +0.002]; null +0.001 [−0.002, +0.005].
  - Insertion: official cells −0.138 [−0.158, −0.119]; null −0.139 [−0.159, −0.120].
  - The paper's rising trend is not reproduced, for either algorithm. Insertion DG at F = 0 matches the paper
    (1.08 vs 1.10). Insertion with no frozen cells is deterministic (one eligible cell at a time), so its null is
    identical. The bubble level does not match (0.39 vs 0.24).
- **Official cells against the null.** They differ by at most +0.02 (bubble F = 0: +0.012 [+0.003, +0.020];
  insertion F = 1 and 5: +0.014 to +0.015). Differences this small need no context-sensitive strategy.
- **The defect makes a trend out of nothing.** With the official (defective) statistic, insertion DG rises with
  frozen cells (0.73 → 1.39 → 1.51 → 2.53 from F = 2 to 5). So does the strategy-free null: slope +0.56 per frozen
  cell [+0.14, +1.06] over F = 0–5. More frozen cells mean more runs stop unsorted, and some of those end on a
  rise, which the defect turns into a sum. Whether the paper's own numbers carry this defect cannot be checked: the
  official step files are not published. Its modest rising values (0.24 → 0.37) do not look like the outliers
  seen here.

**The defect.**
- `avg_wandering_range` averages (recovery − setback)/setback over rise-then-fall episodes, but its early exit
  `return res` returns the running sum.
- Unit check: the error sequence 10, 11, 8, 9, 6, 7, 4, 5, 2, 3 (four identical episodes, ending on a rise) gives
  8.0. The same sequence ending with a fall to 0 gives 2.0.
- In the official runs, every run that ends on a rise is a frozen-cell run that stopped unsorted. Those runs give
  DG ≈ 100–150 instead of about 0.4.

## 7. CRR-explicit check: same form, different history (M7)

**How CRR shaped the design.**
- M7 reads persistent forms as productions of realised history.
- `CORE/MATHEMATICS.md` §V makes regeneration past-only: the successor seed is a weighted mean of completed
  occasions, and "finite memory changes causal influence, not the claim that the past exists".
- The CRR-explicit question for a self-sorting array is therefore: once a form has settled, does the history that
  produced it still act, beyond the visible configuration? And does renewing memory where the cut fell (a local
  rupture) restore repair?
- The ordinary rival is a Markov model on the full state (configuration plus every cell's internal variables):
  history acts only through stored state.

**Design (`crr_history.py`, 50 seeds × 3 continuations, round-robin, 400,000-tick cap).**
- Sort a chimeric array. Copy it three times with identical values and algotypes:
  - **HISTORY:** every selection cell keeps the pointer that sorting left it.
  - **FRESH:** pointers new, as if the same form had been assembled without that history.
  - **LOCAL:** pointers renewed only inside the injured window.
- Shuffle the same contiguous window of W cells in all three, and let each re-sort.

| mix, W | re-sorted: HISTORY | FRESH | LOCAL | repair swaps HISTORY / FRESH | seeds with any stuck continuation (H / F) |
|---|---|---|---|---|---|
| BS, 2 | 95% | 100% | 100% | 188.5 / 0.5 | 4 / 0 |
| BS, 5 | 47% | 100% | 100% | 2,430 / 4.7 | 32 / 0 |
| BS, 20 | 0% | 100% | 100% | 14,812 / 85.4 | 50 / 0 |
| SI, 2 | 100% | 100% | 100% | 0.5 / 0.5 | 0 / 0 |
| SI, 5 | 44% | 100% | 100% | 3.4 / 4.5 | 28 / 0 |
| SI, 20 | 0% | 100% | 100% | 16.6 / 75.5 | 50 / 0 |
| BS, 20, random activation | 2% | 100% | 100% | 15,897 / 83.8 | 50 / 0 |
| BS, 20, ten per value | 5% | 100% | 100% | 4,336 / 41.3 | 50 / 0 |

Sign tests on repair swaps per seed, HISTORY against FRESH: p ≤ 0.001 for every row except SI at W = 2
(p = 1, no difference).

**Official classes (`official_injury.py`).**
- Set-up: 20 seeds per mix, W = 20, 30 s per repair. The HISTORY copy is built with each selection cell's
  `ideal_position` copied from the cell that did the sorting; FRESH uses the class default.

| mix | re-sorted HISTORY | re-sorted FRESH | swaps HISTORY (30 s) | swaps FRESH |
|---|---|---|---|---|
| BS | 0/20 | 20/20 | 36,042 (livelock) | 80.1 |
| SI | 0/20 | 20/20 | 15.1 (deadlock) | 72.6 |

- The official code reproduces the simulator: a BS livelock, an SI deadlock, and fresh repair in under 0.5 s.

**Mechanism (10 seeds per mix, W = 20).**
- After sorting, each selection cell's pointer equals its own position (497 of 500).
- After the injury, a displaced selection cell's pointer still marks its old destination (88 of 89).
- If a smaller value now sits there, the pointer advances past it. Pointers never move left, so the cell is
  repeatedly pulled into a slot to the right of where it belongs:
  - BS: bubble cells push it back, so the array livelocks.
  - SI: insertion cells cannot act on an unsorted left part, so the array deadlocks.
- At the cap, with HISTORY: BS has 99 overshot pointers and 100 misplaced selection cells; SI has 64 and 64. FRESH
  has none in either mix (`crr_mechanism.py`).

**Reading.**
- A settled form does carry its history beyond the visible configuration, in the strong sense that identical
  visible forms differ in repair (0% against 100%).
- The history acts **only** through stored internal state, and LOCAL renewal removes it completely (LOCAL = FRESH
  in every row, to the swap). That is the ordinary hidden-state reading. Its engineering name is cache
  invalidation: an invariant checked on the old configuration (everything left of the pointer is settled) is
  reused after the configuration changed.
- CRR's contribution was the design (matched visible form, varied history, renewal where the cut fell). It made
  no prediction the Markov model does not also make.
- This matches the 2026-10-06 origin-of-life challenge O4: without hidden state, history chooses the basin and
  then adds nothing once the state is known.
- ND-2 (forms produced versus ingressed from an updating Platonic space) is untouched. Both readings describe this
  toy identically.

## 8. Grades

| check | result | grade |
|---|---|---|
| Chimeric aggregation (official code) | reproduced; excess over inert control real (t 10.6–27.8); peaks 0.04–0.15 below the reported values; paper's control and peaks match per-run maxima | REPRODUCED, with a statistic correction |
| Mixed-array swap counts | identity (inversion count) for B/I; BS and SI counts 9–10% below the official code's | REDUCES (identity) |
| Transient clustering | a tempo difference alone gives the chimeric size of peak | ordinary rival sufficient; not yet shown to be the cause |
| Duplicate-value "setpoint" 0.69 | reproduced at the paper's one configuration; no setpoint (0.44–0.78 with geometry); stable versus non-stable sorting predicts BI = chance exactly | FAILS as a setpoint; REDUCES as segregation |
| Delayed gratification | inversions fall by exactly 1 at every step; no frozen-cell trend once the statistic is corrected; the strategy-free null matches the official cells | REDUCES (measure artefact); the frozen-cell trend FAILS to reproduce |
| M7 history check | strong history dependence carried entirely by stored state; local renewal equals fresh | REDUCES to hidden state; ND-2 unchanged |

**What CRR contributed.** The M7 design (§7) and the adversarial question that drove the three null models. **What
it improved.** Nothing measurable: every effect examined has an ordinary model that reproduces it. **Where it
misled.** Nowhere here. The CRR reading of regeneration (past-only, with memory renewed at the cut) is what the
ordinary model also does.

## 9. Single most informative next experiment

Measure each algotype's *effective tempo* in the chimeric runs: swaps per activation and displacement per swap,
per type. Feed those rates into the inert-label speed null, which runs one rule. If the matched-tempo null
reproduces each mix's aggregation curve (peak, timing and decay) within the bootstrap bands, algotype aggregation
reduces entirely to tempo. If it falls short, the residual is the first quantity in this system that is a
candidate "competency" not explained by speed. This is a frozen two-arm comparison that can be preregistered on
fresh seeds.

## 10. Failures and departures recorded before interpretation

- The first delayed-gratification pass used a null that always ran to full sort and recorded only the official
  statistic. It was stopped part-way when the outliers (DG ≈ 100–150 in frozen-cell bubble runs) were traced to
  the sum-not-mean defect. The second pass records both statistics and gives the null the official stopping rule.
  First-pass rows are kept in `results/dg_v1/`. The insertion F = 0 rows are reused from the first pass because
  all 100 runs end sorted, and the two statistics coincide.
- Four cores ran too many jobs at once, so three samples were cut, each before its analysis:
  - The n = 200 official duplicate-value conditions: SI 37 runs; BI and BB at n = 200 not run.
  - The official BI at n = 100, k = 10: stopped at 97 runs.
  - The delayed-gratification frozen conditions: 50 runs each instead of 100.
- Under uniform random activation the simulator under-counted selection swaps (SS 1014 against 1606). Simulator
  results are therefore reported under round-robin, which matched, with random activation as a robustness copy.
- `crr_history.py` first crashed (a `len(None)` on continued state), and then ran very long because HISTORY
  copies livelock. Both were fixed before the reported runs: n is now read from the saved state, and a tick cap
  with a recorded completion share was added.
