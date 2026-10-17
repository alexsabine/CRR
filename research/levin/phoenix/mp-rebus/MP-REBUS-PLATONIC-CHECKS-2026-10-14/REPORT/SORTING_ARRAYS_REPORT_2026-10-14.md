---
title: "The self-sorting arrays through a declared ruler: a replication of Zhang, Goldstein & Levin (2024) on their own code, with the mathematics, the findings, the prior art and the metaphysical positions"
subtitle: "Phoenix programme, study MP-REBUS-PLATONIC-CHECKS-2026-10-14, checks C5–C8"
date: "14 October 2026"
---

**Status line (read first).** Every number in this report is either a declared synthetic check (Phoenix rung R4) or a new replication of a published simulation run on its authors' public code. Nothing here is a Phoenix "finding" (that word is reserved for PASS-2/S3 results); the grade throughout is DESCR, a definition applied and a measurement explained. No ontology is proved by any simulation below, and no result is evidence for the CRR framework. One operator (a Claude Code session acting on the owner's instructions, logged verbatim in `notebook/PROMPT_LOG.md`); no second-person review yet. The owner of the programme is Alex Sabine. The literature sweeps were made by separate contexts of the same model and spot-checked; they are not independent replication.

# 1. Summary

Zhang, Goldstein and Levin (2024) report that distributed implementations of classical sorting algorithms, in which each array element is a "cell" that runs its own copy of the algorithm, show "unexpected competencies": in particular *delayed gratification* (a temporary increase in a sortedness error on the way to a better sort) that grows with the number of defective "frozen" cells, and transient clustering by algorithm type in chimeric arrays. The sorting arrays have since been used as a minimal example of a system that "exploits a Platonic behavioral pattern" (Levin 2026).

We ran the authors' own cells, driver logic and analysis functions, unmodified, from their public repository (1,600 experiments on the bubble sort, plus 800 in a sensitivity arm), after committing the predictions. We also reimplemented the three algorithms and the paper's measures from a reading of the code (C6, 50 replicates per arm) and ran two control batteries the paper did not run.

The results, in order of certainty:

1. **On the global sortedness rulers nothing ever regresses.** On the Kendall inversion count and the Spearman footrule, no swap in bubble or insertion sort, cell-view or classical, with or without frozen cells, ever increases disorder. This is a theorem about adjacent swaps of out-of-order pairs (§4.2), confirmed in all 1,600 of the authors' trajectories. "Delayed gratification" exists only on the adjacent-descent ruler the paper uses, where it is present in every experiment, for the textbook algorithm as much as for the cell-view one, at a level within 10 % of a random-swap null. It is a property of the measure.
2. **The published obstacle trend does not reproduce with the code's frozen cells.** In the committed code a frozen cell never initiates a swap but can be swapped by an active neighbour. Under that rule the authors' score is flat: 0.391 / 0.389 / 0.389 / 0.384 for 0–3 frozen cells (the paper: 0.24 / 0.29 / 0.32 / 0.37).
3. **A rise in the paper's direction appears only with immovable obstacles, and the textbook algorithm shows it too** (cell-view 0.391 → 0.462; classical 0.081 → 0.218). The declared diagnostic locates the cause in the statistic: an immovable cell partitions the array into independent short segments; short segments permit only short runs of error-raising swaps; the score divides by that run length. Nothing happens late in the run and nothing happens near the obstacle.
4. **The dynamics are memoryless**, as the paper itself says: two arrays in the same state with different pasts have the same future (97.5 % of trials on a statistic that history can move), while an injected one-parameter fatigue memory is detected 85 % of the time. Whatever "patience" or "memory" a reader attributes to the cells lives in the array state.
5. **The selection rule with obstacles makes genuine global regressions** (up to 106 inversions) through an ideal-position pointer that overshoots its cell. The adjacent-descent measure cannot distinguish this from harmless bubble churn.
6. **Scheduling does not produce the trend.** Lock hand-off fairness moves the level by 0.08 and never produces a rise with frozen cells; the authors' threaded code on this machine behaves as random visiting.
7. **Three defects in the published code**, one of which makes the analysis function return a sum instead of a mean when a trajectory ends on an error increase.

The paper's cell-view level at zero frozen cells (0.24, against 0.39 from the authors' own code and from two independent reimplementations) remains unexplained by anything in their repository. The classical level (0.08) is reproduced exactly.

**Has this been mooted?** Twice, informally and without the mathematics (a 2025 blog comment and a 2026 Substack essay argue that sortedness is an observer-chosen metric); the inversion-count theorem appears in one unreviewed repository of October 2026; the partition mechanism, the memory test, the scheduling control, the pointer regression and the non-reproduction on the authors' own code appear nowhere (§7). The paper has 11–32 citations, none critical, and no one has run its code to a result.

What CRR contributed is not an ontology and not a prediction. It is the discipline of declaring the ruler (the *carrier*) and the invariant before looking, and the question that discipline forces: *where on the array and when in the run does the measured competency live?* Answering it turned a competency into a quotient. §8 sets out what this implies for the authors' metaphysical reading and for the two criteria any "competency" claim should meet before it is granted to a system rather than to its observer.

# 2. The target: the paper's claims and the authors' framing

**The system.** An array of *n* = 100 cells holding the values 0…99 in a random order. Each cell is a thread running one of three local rules: a *bubble* cell looks left or right at random and swaps with that neighbour if they are out of order; an *insertion* cell swaps left only when the prefix to its left is sorted; a *selection* cell keeps an "ideal position" pointer and jumps there when it is smaller than the occupant. A frozen cell never initiates a swap. The run ends when no active cell "should move".

**The measures.** The paper's sortedness error is the number of adjacent descents, `Des(a) = #{i : a[i] < a[i−1]}`, recorded after every swap. Delayed gratification (DG) is computed from that trace: consecutive same-sign changes are summed into runs; from the first increase onward each increase `d_i > 0` is paired with the following decrease `d_j < 0` and scored `(−d_j − d_i)/d_i`; DG is the mean of those scores. Clustering is the fraction of cells whose neighbours share their algorithm type.

**The claims as reported.** Cell-view bubble DG 0.24 / 0.29 / 0.32 / 0.37 for 0–3 frozen cells; cell-view above traditional by +0.16 for bubble, +0.03 (n.s.) for insertion, −2.77 for selection; cell-view selection making 11× the classical swaps; chimeric arrays clustering to 0.62–0.72 against a 0.57–0.65 control; cross-purpose chimeras ending at 42.5 % sortedness. The authors describe these as competencies that the rules do not state ("they often require a different set of conceptual tools to effectively predict", p. 18), while adding "there is no magic here, of course: everything that happens is, in some way, a consequence of the rules being followed."

**The framing that followed.** In *Ingressing Minds* (Levin 2026, §6, Fig. 14) the arrays are "an example of a Platonic behavioral pattern exploited by this very minimal system": patterns of behaviour are taken to pre-exist in a space of forms that physical systems, even ones with "no memory, no feedback, no stochasticity", can ingress into. The sorting paper itself does not use the word Platonic; the reading is imposed afterwards.

# 3. The CRR objects used, and what CRR does not claim here

CRR (Coherence–Rupture–Regeneration) is, in the Phoenix programme, a heuristic and theoretical framework whose core is a small set of mathematical commitments on a declared *carrier*. Only three of its objects are used in this study.

**The carrier and the two lengths (CORE A1/D2/D3, R3).** A path is measured on a declared carrier with a resolution σ. Its *coherence* `C` is the accumulated arc length in units of σ; its *chord* `C*` is the distance between its endpoints on the same carrier; the *surplus* is

$$S = C - C^{*} \;\ge\; 0 .$$

On a one-dimensional carrier, with `B` the total backward travel of the path, forward travel obeys `P − B = C*σ`, so (CORE R3)

$$C = \frac{C^{*}\sigma + 2B}{\sigma}, \qquad S = \frac{2B}{\sigma}, \qquad S = 0 \iff \text{the path is monotone}.$$

The core states this is "standard path-length arithmetic, not evidence for a new physical law". Applied to a sorting run, the carrier is a sortedness ruler `e(·)` on permutations, the path is the error trace `e_0, e_1, …, e_T` after each swap, and

$$C = \sum_t |e_t - e_{t-1}|, \qquad C^{*} = |e_T - e_0|, \qquad S = C - C^{*} = 2B, \qquad B = \sum_t \max(e_t - e_{t-1}, 0).$$

The paper's "temporary increase in error" is exactly `B` on its chosen ruler, so **delayed gratification is surplus on the adjacent-descent carrier**. That is a definition, not a result. What the definition buys is the obligation to say which carrier, because `S` is carrier-relative by construction.

**Path dependence (commitment M4) as a testable property.** CRR holds that an agent carries its past (its "mass") into its present, so that two systems in the same present state with different pasts can have different futures. For a system to be a CRR subject at all this must be false of nothing: there must be *something* the past adds beyond the state. The sorting worlds give a clean test of whether that is so (§4.6).

**Two clocks.** CRR distinguishes a shared clock from each agent's own clock of becoming. For a cell the own clock is its count of swaps experienced. §4.7 shows this clock is fixed by the initial permutation in the adjacent-swap algorithms.

**What CRR does not claim here.** No CRR prediction was at stake. The framework does not predict whether DG rises with obstacles; it says only that whatever rises must be read on a declared ruler, and that "memory" must be shown to be more than state. The study grades DESCR throughout: a definition applied, a measurement explained. Nothing enters the survival ledger.

# 4. Mathematics

## 4.1 Three rulers on a permutation

For an arrangement `a` of distinct values at positions `0…n−1`, with `pos(x)` the position of value `x`:

- **Inversions** (Kendall distance to the identity): `Inv(a) = #{(i, j) : i < j, a[i] > a[j]}`.
- **Adjacent descents** (the paper's monotonicity error): `Des(a) = #{i ≥ 1 : a[i] < a[i−1]}`.
- **Footrule** (Spearman): `Foot(a) = Σ_i |a[i] − i|` (the authors' `get_spearman_distance`).

`Inv` and `Foot` are global: they see every pair, or every displacement. `Des` is local: it sees only neighbours, and `Des ≤ Inv` always, with `Des = 1` compatible with `Inv = n − 1`.

## 4.2 Theorem: no out-of-order swap raises global disorder

**Lemma 1 (inversions).** Let `v < o` occupy positions `q > p` respectively (so `o` sits left of `v`), and let `k` be the number of values strictly between `v` and `o` in value that lie between positions `p` and `q`. Swapping `v` and `o` changes the inversion count by exactly

$$\Delta\,\mathrm{Inv} = -(2k + 1).$$

*Proof.* The pair `(o, v)` was an inversion and is no longer: −1. Each of the `k` intermediate values `w` with `v < w < o` between them formed an inversion with `o` (since `o > w` and `o` was to its left) and with `v` (since `v < w` and `v` was to its right); after the swap both are in order: −2 each. Values between the positions but outside the value interval, and all values outside the positions, keep their order relative to both `v` and `o`. ∎

For an adjacent swap `k = 0` and `Δ Inv = −1` exactly. Every swap in the bubble and insertion rules, cell-view or classical, movable frozen cells or none, is an adjacent swap of an out-of-order pair. Hence along any such run `Inv` is strictly decreasing at every step and

$$S_{\mathrm{Inv}} = 0 \quad\text{for every trajectory.}$$

**Lemma 2 (footrule).** With `v < o` swapped from positions `q > p` to positions `p, q`, the footrule changes by `g(v) − g(o)` where `g(x) = |p − x| − |q − x|`; `g` is nondecreasing in `x`, so the change is `≤ 0`. ∎ Hence `S_Foot = 0` on the same runs.

**Lemma 3 (descents are not monotone).** An adjacent swap at `(i, i+1)` removes the descent at that pair and can create one at `(i−1, i)` and one at `(i+1, i+2)`; so `Δ Des ∈ {−1, 0, +1}`, and `Des` can rise. A selection jump can disturb four pairs. ∎

**Corollary.** `S_Inv = S_Foot = 0` and `S_Des ≥ 0` on every bubble or insertion run; "delayed gratification" on the authors' ruler is `B_Des = S_Des / 2`, and on the global rulers it is identically zero. The paper's competency is a property of the ruler.

**Where the premise fails.** The selection rule with frozen cells is the exception. Its ideal-position pointer advances by one whenever it meets a frozen occupant, without reference to where the cell itself is; the pointer can therefore overshoot the cell's own position, after which the cell swaps *rightward* with a *larger* occupant. That is a swap of an in-order pair, and Lemma 1 runs in reverse: `Inv` rises. This was found because Lemma 1 was declared as a prediction for all six rules and then failed for one (C6: `S_Inv` up to 106 with 1–3 frozen cells; zero at no frozen cells in 50/50 replicates; a diagnostic on 10 replicates found 123 inversion-raising swaps, only 2 involving a frozen cell directly). The authors' `SelectionSortCell.should_move_to` has the same pointer rule.

## 4.3 The paper's statistic, formally

Let `e_0, …, e_T` be the `Des` trace, de-duplicated of consecutive repeats; let `d_1, …, d_m` be the sums of consecutive same-sign differences (so the `d` alternate in sign); let `i_0` be the index of the first positive `d`. Pair each positive `d_i` with the following negative `d_{i+1}` and define

$$\mathrm{DG} = \frac{1}{N} \sum_{\text{pairs}} \frac{-d_{i+1} - d_i}{d_i} = \frac{1}{N}\sum_{\text{pairs}}\left(\frac{\mathrm{dec}}{\mathrm{inc}} - 1\right),$$

the mean over episodes of (recovery beyond the setback, relative to the setback). This is the authors' `avg_wandering_range`, executed from their file in C7. Two features matter below. First, it is a mean of ratios with the setback in the denominator: a shorter setback with the same recovery raises the score. Second, the function has two exit paths: `return res / n` on normal termination, and `return res` (the un-normalised sum) when the trace ends on an increase (§6.6).

## 4.4 The partition lemma and the denominator effect

**Lemma 4 (partition).** An immovable cell at position `f` that neither initiates nor accepts a swap splits the array into the two sub-arrays `[0, f)` and `(f, n−1]`, on each of which the dynamics run independently and never exchange values. With `k` immovable cells the array is `k+1` independent segments whose final state is each segment sorted internally; `Inv` at termination is the number of inversions between segments, which is fixed by the initial arrangement. ∎ (C7: the final inversion counts of the cell-view and classical immovable arms coincide exactly for every seed: 870.5 / 1259.2 / 1552.1 on average for 1–3 cells.)

**The denominator effect.** On the `Des` ruler a setback of length `L` is a run of `L` consecutive swaps each of which creates a new descent (Lemma 3). In a segment of length `m` such runs are bounded by the segment's own disorder and are shorter on average when `m` is smaller. The recovery that follows a setback is about two swaps regardless (the created descents are removed as the swapped values continue). So partition shortens `inc` while leaving `dec` unchanged, and `DG = mean(dec/inc) − 1` rises. The measured decomposition (C7, cell-view immovable, 0 → 3 cells): mean `inc` 1.85 → 1.65, mean `dec` 1.99 → 1.97, episodes 346 → 142, the last episode carrying 2–5 % of the sum, under 1 % of error-raising swaps within one position of a frozen cell. In the classical algorithm `inc` is pinned at 1 by construction (a left-to-right pass creates at most one descent per swap) and only `dec` can respond (1.08 → 1.22), which is why its rise is steeper relative to its level. With *movable* frozen cells there is no partition (an active neighbour can push the frozen cell aside) and no rise.

## 4.5 Surplus on each ruler under each rule

| rule | `S_Inv` | `S_Foot` | `S_Des` |
|---|---|---|---|
| bubble (cell-view or classical), any movable frozen cells | 0 (Lemma 1) | 0 (Lemma 2) | > 0 in every experiment (C5b, C6, C7) |
| insertion (cell-view or classical) | 0 | 0 | > 0 in ≥ 98 % |
| selection, no frozen cells | 0 | 0 | > 0 |
| selection, frozen cells | **> 0** (pointer overshoot) | **> 0** | > 0 |

## 4.6 State-sufficiency as a test of path dependence

**Design.** Reach a state `x` by a real route of 600 visits, recording each cell's own swap count. From the identical state run 20 continuations that carry those counts and 20 that carry zeros. Under the authors' rules the counts do nothing, so the two futures should be indistinguishable; under a "fatigue" rule in which a cell's chance to act is `1/(1 + 0.05 × own swaps)` they should differ. Two-sample permutation test; 40 trials.

**The first statistic was void.** C6 used remaining swaps to completion. By Lemma 1 that equals `Inv(x)` under any adjacent-swap rule, fatigue or not: the must-fail arm could not fail (2.5 % of trials below 0.05), and the test was recorded VOID, not as support. C6b re-declared the statistic as remaining *visits* (activations, swapping or not), which fatigue can move.

**Result (C6b).** Authors' rules: `p > 0.05` in 97.5 % of trials (median 0.43). Fatigue: `p < 0.05` in 85 % (median 0.002; the carried counts add about 1,800–2,500 visits). Remaining swaps: invariant in both arms (100 %, 97.5 %). The sorting worlds are state-sufficient; CRR's M4 has nothing to grip; the paper's "no memory" is correct about the dynamics.

## 4.7 The per-cell clock is fixed by the initial arrangement

**Lemma 5.** In any run of adjacent swaps of out-of-order pairs that ends sorted, the number of swaps a value `v` takes part in equals its inversion degree in the initial permutation, `deg(v) = #{w : (v, w) inverted initially}`.

*Proof.* Each swap involving `v` resolves exactly one inversion involving `v` (Lemma 1 with `k = 0`), none is created, and at the end none remains. ∎

C6: Spearman correlation between swaps experienced and initial inversion degree is 1.000 with maximum absolute difference 0 for cell-view bubble and insertion; 0.015 for selection (non-adjacent jumps). In the adjacent-swap algorithms a cell's whole history of being swapped is written in the starting line-up. There is nothing for its "patience" to be a strategy about.

# 5. Methods

## 5.1 Provenance and handling of the authors' code

Repository `github.com/Zhangtaining/cell_research`, full history fetched (six commits; first commit 2023-08-26; HEAD 1fd2bd59 of 2024-10-30; no licence file). It was cloned into the session's untrusted scratchpad and **nothing from it was copied into Phoenix**; the C7 runner imports it at run time by path, as Phoenix does for other third-party code. File hashes at HEAD are recorded in the runner's output (`BubbleSortCell.py` 40b58682…, `MultiThreadCell.py` a720f5bd…, `CellGroup.py` 9b7c8b4d…, `StatusProbe.py` 618951a8…, `delay_gratification_analysis.py` 1c741904…, `utils.py` 8115d41c…, the frozen-cell driver 768187bd…). `BubbleSortCell.py` is unchanged since the first commit.

**No saved trajectories exist** at any commit (`git log --all --name-only`: no `.npy`, no `csv/`); the analysis scripts load absolute paths on the first author's machine. Everything here is a new replication.

**Not in the code:** the immovable condition (the analysis loads `*_cannot_move_*` files that no committed code produces; the bubble cell's `should_move_to` accepts a `FREEZE` target, so committed frozen cells are movable) and the conventional baselines with frozen cells (`original_*_with_kfrozen` records; the committed classical script is a ten-element visual toy). Both were supplied by Phoenix and are labelled as such: the immovable arm is a one-line subclass requiring an `ACTIVE` target; the classical arms are textbook left-to-right passes in which a frozen cell never initiates and is swappable by its left neighbour (movable) or not (immovable).

**Runner changes, documented before the full run.** The driver imports tkinter at module top, so its `create_cells_within_one_group`, `activate`, `no_cells_should_move` and kill sequence were re-created line for line (cells with boundaries `(0,1)`–`(n−1,1)`, one `CellGroup` with period and count-down 10⁹, frozen cells chosen by `random.randint` with replacement, frozen threads not started, the 1 s stopping-rule poll, lock held during activation and kill). The analysis functions were extracted by parsing the authors' files and executing only their function definitions (the module bodies load the absent `.npy` files). Three corrections were recorded in the declaration after a one-experiment smoke test and before any result was read: the poll interval set to the authors' 1 s (the first draft used 0.05 s); the `frozen_swap_attempts` counter noted as inert; a bookkeeping `None` at index 0 of the snapshot list fixed after a crash that produced no output.

## 5.2 Settings

The paper's, as the driver encodes them: 100 cells with values 0…99 shuffled; 100 experiments per condition; frozen cells 0, 1, 2, 3; shuffle and frozen placement seeded per experiment (`random.seed(10000·k + e)`); thread scheduling the operating system's. Conditions: cell-view movable (the committed code), cell-view immovable (the variant), classical movable, classical immovable. Per experiment the authors' snapshots after every swap, their swap and compare counts, the error trace on their measure and on `Inv` and `Foot`, their DG, `C`, `C*`, `S` on each ruler, and the mechanism diagnostic of §4.4. A second arm repeated the two cell-view conditions with a 0.05 s poll to measure stopping-rule sensitivity. Compute: 52 min wall-clock for the threaded primary arm, 25 min for the second; the 10 MB trace archive is kept out of git with its hash recorded (`8be954e1…c85361`).

## 5.3 The reimplementation battery (C6) and the controls (C6b, C8)

C6 reimplements the three cell rules and the classical versions from a reading of the code (cells visited in random order; one visit is one `move`), with `n = 100`, 50 replicates per arm, frozen cells 0–3 movable; chimeras (50/50 random assignment of two rules), the negative control (bubble cells carrying two labels), the declared cross-purposes arm and the paper's three pairings; the state-sufficiency test and the per-cell clock check. C6b re-declares the state-sufficiency statistic (§4.6). C8 adds one parameter to the C6 engine, `sticky ∈ {0, 0.5, 0.9, 0.99, 1}`: after a cell swaps, with that probability it is visited again at once (`sticky = 0` is C6 exactly), to model lock hand-off fairness.

## 5.4 Protocol

Each check's predictions were written and committed before its run (`DECLARATION_ADDENDUM_C5B/C6/C6B/C7/C8.md`). Failures are recorded beside the declared text and the declarations are not edited (Phoenix rule R15). Outputs are pinned in git past the `studies/*/outputs` ignore rule. The one post-hoc diagnostic (same-mover run length on the authors' code) is labelled post hoc.

# 6. Results

## 6.1 C5b: the paper's rules and carrier, reimplemented (100 replicates)

| declared | observed | verdict |
|---|---|---|
| `S_Inv = 0` in every replicate, arm and frozen count | max 0.0 everywhere | holds (Lemma 1) |
| `S_Des > 0` in most replicates for both bubbles at 0 frozen | 100 %; mean 1,226 (cell-view), 1,182 (classical); random-swap null 1,334 | holds, more strongly than declared |
| cell-view `B_Des` rises with frozen count | 613 / 604 / 595 / 582 (falls slightly) | fails on this statistic (raw backward travel is not the paper's normalised DG) |
| all cell-view arrays with movable frozen cells sort | 1.00 / 1.00 / 0.99 / 0.95 | nearly (two adjacent frozen cells in the wrong order can never be swapped) |

## 6.2 C6: the full battery (50 replicates per arm)

| arm | `S_Inv` max | `S_Foot` max | `S_Des > 0` | DG (mean ± sd) | swaps | sorted |
|---|---|---|---|---|---|---|
| classical bubble | 0 | 0 | 1.00 | 0.084 ± 0.015 | 2,446 | 1.00 |
| cell-view bubble, 0/1/2/3 frozen | 0 | 0 | 1.00 | 0.379 / 0.375 / 0.376 / 0.376 | 2,493 / 2,493 / 2,466 / 2,360 | 1.00 / 1.00 / 0.68 / 0.22 |
| classical insertion | 0 | 0 | 1.00 | 1.095 ± 0.141 | 2,446 | 1.00 |
| cell-view insertion, 0/1/2/3 | 0 | 0 | 0.98–1.00 | 1.066 / 0.939 / 0.952 / 0.938 | 2,493 / 579 / 288 / 213 | 1.00 / 0 / 0 / 0 |
| classical selection | 0 | 0 | 1.00 | 7.01 ± 3.38 | 95 | 1.00 |
| cell-view selection, 0/1/2/3 | **0 / 30 / 98 / 106** | **0 / 8 / 144 / 56** | 1.00 | 3.23 / 3.08 / 3.03 / 2.86 | 1,011 / 991 / 970 / 955 | 1.00 / 0.04 / 0 / 0 |

Against the eight declared predictions: Lemmas 1–2 hold for 12 of 15 arms and fail for selection with obstacles (the pointer overshoot); `S_Des > 0` holds; the paper's three between-algorithm contrasts reproduce (bubble +0.30 against their +0.16; insertion −0.03 against their +0.03 n.s.; selection −3.8 against their −2.77; selection swaps 10.6× against their 11×); **the frozen-cell trend for bubble does not appear** (flat at 0.38); chimeras all sort and the bubble–selection aggregation peak exceeds the control's by 0.09 (their 0.72 against 0.61); the paper's own cross-purposes pairing ends at 37 % ascending pairs (their 42.5 %); the state-sufficiency test was VOID by construction (§4.6); the per-cell clock identity holds exactly (§4.7). Two declared thresholds were naive (the control's aggregation peak; the declared cross-purposes arm had an absorbing state) and are recorded as such.

## 6.3 C6b: state-sufficiency on remaining visits

Authors' rules 97.5 % of trials with `p > 0.05`; fatigue must-fail 85 % with `p < 0.05`; remaining swaps invariant in both arms. All three declared predictions hold.

## 6.4 C7: the authors' own code (100 experiments per cell)

| condition (matched published condition; baseline) | DG at 0 / 1 / 2 / 3 frozen | slope per frozen cell (*t*) | swaps | sorted |
|---|---|---|---|---|
| cell-view, **movable** (the committed code) | **0.391 / 0.389 / 0.389 / 0.384** (sd 0.03) | −0.002 (−1.4) | 2,511 / 2,475 / 2,395 / 2,339 | 1.00 / 1.00 / 0.53 / 0.18 |
| cell-view, **immovable** (Phoenix's variant; the paper's "cannot move" files) | **0.391 / 0.409 / 0.436 / 0.462** | +0.024 (11.1) | 2,511 / 1,605 / 1,216 / 934 | 1.00 / 0 / 0 / 0 |
| classical, movable (Phoenix's baseline) | 0.081 / 0.090 / 0.095 / 0.107 | +0.008 (7.7) | 2,511 / 2,166 / 2,026 / 1,774 | 1.00 / 0.05 / 0.01 / 0 |
| classical, immovable (Phoenix's baseline) | 0.081 / 0.125 / 0.171 / 0.218 | +0.046 (20.5) | 2,511 / 1,605 / 1,216 / 934 | 1.00 / 0 / 0 / 0 |

`S_Inv = S_Foot = 0` in all 1,600 experiments; `S_Des ≥ 174` in every one. Cell-view minus classical at 0 frozen: +0.31 (the paper +0.16). Paired cell-view minus classical, immovable, same seeds: +0.310 / +0.283 / +0.265 / +0.244.

| condition | mean increase run, 0 → 3 | mean decrease run, 0 → 3 | episodes | last-episode share | error-raising swaps near a frozen cell |
|---|---|---|---|---|---|
| cell-view movable | 1.84 → 1.80 | 1.98 → 1.95 | 347 → 324 | 0.03 | 0 → 0.10 |
| cell-view immovable | **1.85 → 1.65** | 1.99 → 1.97 | 346 → 142 | 0.02–0.05 | 0 → 0.005 |
| classical movable | 1.00 | 1.08 → 1.11 | 610 → 462 | 0.12–0.14 | 0 |
| classical immovable | 1.00 | **1.08 → 1.22** | 610 → 223 | 0.13 | 0 |

Against the six declared predictions: the movable trend **fails** (flat; only the 3-frozen value lies within 0.10 of the paper's); the immovable arm is positive and rises; the classical baselines behave as declared; the ruler theorem holds on the authors' trajectories; the thread-scheduled level is within 0.012 of the random-visit engine; the mechanism expectation (longer recoveries, late, near the obstacle) **fails** and the diagnostic gives the denominator effect of §4.4 instead.

**Stopping-rule sensitivity (second arm, 0.05 s poll).** Trajectories identical to within one swap; the immovable arm unchanged (0.394 / 0.408 / 0.434 / 0.463). The movable arm's *means* explode (0.392 / 1.84 / 3.15 / 3.23, sd 14–20) because 5 of 300 experiments score 125–159; medians 0.390 / 0.391 / 0.382 and the means of the other 295 are unchanged. Cause, confirmed by re-running the affected seeds: the fast poll can stop the run right after an error-raising swap next to a frozen cell (the stopping rule does not see disorder against a frozen neighbour), the trace then ends on an increase, and `avg_wandering_range` takes its early exit, returning the un-normalised sum.

## 6.5 C8: scheduling stickiness

| sticky | DG at 0 / 1 / 2 / 3 frozen | mean same-mover run |
|---|---|---|
| 0 (= C6) | 0.382 / 0.375 / 0.378 / 0.386 | 1.05 |
| 0.5 | 0.348 / 0.337 / 0.348 / 0.346 | 1.24 |
| 0.9 | 0.318 / 0.313 / 0.319 / 0.313 | 1.49 |
| 0.99 | 0.307 / 0.306 / 0.303 / 0.310 | 1.56 |
| 1.0 | 0.305 / 0.304 / 0.310 / 0.305 | 1.56 |

Post hoc on the authors' threaded code (20 fresh experiments): same-mover run 1.053 ± 0.006 at 0 frozen, 1.056 at 3: the same as random visiting; and the threaded run is reproducible given the seed (three repeats byte-identical), so the operating system's lock hand-off on this machine is effectively a fixed round-robin. Stickiness lowers the level to a floor of 0.305 (a sticky bubble cell loses the floor at its first failed random-direction try) and never produces a rise with frozen cells. The visualisation path was checked and excluded (the frozen-cell driver constructs every cell with `disable_visualization=True`).

## 6.6 Defects in the published code

1. **Stopping rule.** `BubbleSortCell.should_move` counts a neighbour as a reason to move only if that neighbour is `ACTIVE`; `should_move_to` lets the cell swap with a `FREEZE` neighbour. `no_cells_should_move` can therefore end a run with active cells still out of order against frozen ones; whether it does depends on the poll timing.
2. **Analysis function.** `avg_wandering_range` returns `res` (the sum) rather than `res / n` (the mean) when the de-duplicated trace ends on an increase. Dormant under the 1 s poll in 400 experiments here; live under any condition that ends a run on an increase.
3. **Counter.** `frozen_swap_attempts` increments only when the moving cell is itself frozen, which cannot happen (frozen threads are not started and `should_move_to` requires `self.status == ACTIVE`); it is always 0.

And one behaviour rather than a defect: the selection cell's pointer overshoot (§4.2), which makes real global regressions with frozen cells and is invisible on the paper's ruler.

# 7. Prior art: has this been mooted?

*(This section is filled from two literature sweeps made on 14 October 2026; each item is marked by whether it was read in full or seen only in a search result. See §7.7 for the sweeps' limits.)*

## 7.0 What the paper itself says (read in full, arXiv 2401.05375)

The paper's "monotonicity error is the number of cells that violate the monotonic order" and its "Sortedness Value is defined as the percentage of cells that strictly follow the designated sort order": the adjacent-descent ruler, as used here. Its Glossary defines both kinds of frozen cell: "A 'movable' Frozen Cell will not move on its own … but other cells are able to move it. An immovable Frozen Cell can neither proactively move itself nor can it be moved by another cell." The committed driver produces only the movable kind; the committed analysis has a separate script for `cannot_move` records that no committed code produces. The reported trend ("0.24 with 0 Frozen Cell, 0.29 with 1 …, 0.32 with 2 …, 0.37 with 3"; insertion 1.1 → 1.19; none for selection) is interpreted as "context-sensitive" delayed gratification. Which kind of frozen cell produced the published table cannot be determined from the paper or the repository; the direction reproduces here only under the immovable kind (§6.4).

Two further facts from the text. The words *inversion*, *Kendall* and *footrule* do not occur in the paper (zero occurrences), so the measure-specificity of the result is not considered. And nothing in the paper notes that an immovable cell partitions the array into independent segments. The two central points of this report are therefore not anticipated by the paper.

One discrepancy of definition is worth the authors' attention: Figure 6D's caption defines the DG index "by using the total consecutive increasing value (x) of Sortedness after the drop as the numerator, and the total consecutive decreasing value (y) of Sortedness before the increase as the denominator", i.e. recovery/setback; the committed `avg_wandering_range` computes `(recovery − setback)/setback`, which is one less. The two cannot both describe the published 0.24 (the code's value on its own trajectories is 0.39; the caption's definition would make it 1.39).

## 7.1 Reception, citations, replications and critiques of the paper

**Citation footprint.** Crossref 11, Semantic Scholar 16, Google Scholar 32 (the cited-by list itself could not be opened). Of the sixteen Semantic Scholar citers, read in context, none replicates, re-analyses or criticises the delayed-gratification result; most are Levin-group self-citations (Cool et al. 2026 on Lenia: "surprising latent competencies in very simple systems – sorting algorithms – that found novel ways to complete their task when tangible barriers were placed in their way"; Zhang & Levin 2026; Pezzulo & Levin 2026, who hedge that "this does not mean that we should automatically label as intelligent any form of computation"; Sacco, Sakthivadivel & Levin 2025; Kofman & Levin 2025; Levin 2026 *Philosophies*) or one-line mentions (Baulin et al. 2026; Gardner & Baulin 2025; Prentner 2025; Hora de Carvalho 2025; Armitage et al., who propose to frame the behaviours "as artistic tendencies"). One meeting report (*Neuropsychoanalysis* 2024) misreads the paper as showing "a 'form' of consciousness". A patent exists (WO2025128882A1, Tufts, priority 12 Dec 2023) defining Sortedness and DG as the paper does. arXiv records no trackbacks; alphaXiv has no comments; PubPeer could not be checked.

**Replications and re-implementations.** No published replication on the authors' code exists. The only public record of anyone running their code is issue #1 on the repository (opened 24 Sep 2025; a comment of 21 Aug 2026 reports that the shipped scripts fail with missing arguments and that the chimeric code is absent; no author reply). Independent toy re-implementations: a teaching notebook series (CoursIA, 2026) that "reproduces robustness and delayed gratification but not the paper's positive kin aggregation", under the paper's own metric only; an agent-generated replication (baocin, 2026) that tests damage tolerance, not DG; several visualisers and pre-implementation shells with no results (tinker-casting, morphosort, animath, morphogenesis-sort, the last written explicitly "to avoid threading artifacts that masquerade as emergent behavior"). One repository, `alexbaker0/Self-sorting-cells` (a from-scratch JavaScript re-implementation, all commits of 6 Oct 2026, no stars, generated with Claude Code), states in its notes that "every swap exchanges an out-of-order pair, so the inversion count never increases" and that "our version does NOT reproduce the delayed-gratification-vs-frozen-cells trend", attributing the gap to its random-order approximation of threads and to the ambiguity of the paper's DG definition. It is the only place either point appears before this report. It is not referenced anywhere in Phoenix; whether it is connected to this programme the owner should state before it is cited as independent.

**Critiques of the measure.** No peer-reviewed or preprint critique of the Sortedness measure exists. The two prior statements are informal. Ashvin Pandurangi, in a comment on Levin's blog (14 July 2025, no reply): "'less sorted' and 'more sorted' depend on what kind of metric we use"; "that metric is entirely coupled with the sorting algorithm itself"; a step "may look 'less sorted' as measured by the Bubble metric" while under the hybrid algorithm's own metric nothing is circumvented; "this step is dubbed the cognitive competency of 'delayed gratification'"; "we have a single plane of causation". Bret Kerr, "Nowhere to Hide" (Substack, 12 Sep 2026, a reading of the paper's numbers, no code run): "Sortedness is an observer-chosen statistic, not the algorithm's value function, and a temporary dip in a metric nobody optimized is not foresight"; the DG score "shows up in all the tested algorithms, traditional and cell-view alike"; "'not explicitly in the algorithm' survives only in the weak sense that no function is named delayed_gratification()". Neither invokes inversions, Kendall's distance or the footrule, and neither discusses the frozen-cell trend.

**The partition and denominator point.** Not found anywhere. The nearest is Levin's own reply to a commenter (23 Feb 2026): with "fully glued" cells "the array can never reach full sortedness" and "we measure partial sortedness"; no inference about the ratio statistic is drawn. The commenter's objection (12 Feb 2026) was that with an immovable element some values "can never end up" on its far side, so the preprint's example implied a changed algorithm.

**The memory and state-sufficiency point.** Not stated by anyone in those terms. Related remarks in Levin's comment threads: that the system is deterministic and fully predictable (Dec 2023; Levin: "there is no magic or indeterminism at the low level"); that the lock serialises the threads so multithreading "only acts as a random selector" and is "a distraction" (29 Dec 2024); that the clustering follows from the left-bias of the selection and insertion rules (three commenters, Dec 2023 and Dec 2024); and Levin's reply (21 Jul 2024) that "which behaviors are explicitly encoded and which implicit and surprising, depends on the perspective of an observer", which concedes the observer-relativity at issue here.

**Framing critiques of the paper specifically.** A Hacker News thread (18 Dec 2024, 79 comments) with "self organization … not intelligence" and "to instantiate an abstract description implies almost nothing", none on the measure; a sceptical podcast episode (Brett Hall, ToKCast, Mar 2026, content not accessed); Nathan Sweet's "Religion With A Pipette" (Oct 2026): "before explaining a 'free lunch,' find out who already paid", with the sorting work mentioned in passing. The Platonic framing's critics (Dodig-Crnkovic 2025, 2026; Devine; Kaufman; Segall) do not engage the sorting data in the portions that could be read. Popular coverage (Forbes, Nov 2025: the elements "spontaneously adapted, problem-solving by implementing unprogrammed novel strategies") is uncritical.

**Levin's subsequent uses.** The blog of 17 Dec 2023 ("What do algorithms want?") defines DG as "the ability to temporarily get further from their goal in order to do better later", anticipates the objection ("can you hear the screech of the goal-posts being moved?"), and concedes that "with 2+ fully frozen cells, it may not be 100 % solvable". The *Ingressing Minds* preprint (2025) and journal article (*Philosophies* 2026) retain the example: "this ability to back-track to deal with a broken piece of data is not explicitly in the algorithm … and is an example of a Platonic behavioral pattern exploited by this very minimal system"; "if we don't even understand what else bubble sort is capable of, how can we think we understand what we have when we build complex AI architectures?". Its Figure 14B shows the *traditional* single-algorithm bubble sort trace, not the cell-view one. The Lex Fridman interview (#486) presents the one-immovable-digit case as the algorithm going "against the thing that it's trying to do". The only published "free lunch" paper (Ertle, Levin & Scheutz, ICDL 2025) is about maze exploration, not sorting, and not with Goldstein.

**Verdict on "has this been mooted".** The observer-relativity of the measure has been mooted twice, informally, without the mathematics (Pandurangi 2025; Kerr 2026). The inversion-count theorem appears in one unreviewed repository of October 2026. The partition and denominator mechanism, the state-sufficiency test, the scheduling control, the selection-pointer regression, the code defects and the non-reproduction on the authors' own code appear nowhere. No one has run the authors' code to a result.

## 7.2 Measures of presortedness: the ruler-dependence is textbook, the application is not

The mathematics of §4.1–4.2 is standard and old. Knuth (*The Art of Computer Programming*, vol. 3, §5.1.1 "Inversions"; the concept "was introduced by G. Cramer in 1750") gives the diagram of adjacent interchanges in which "following any line downward inverts exactly one new pair" and "the total number of inversions will increase or decrease by unity"; §5.2.2 gives bubble sort's exchange count as the inversion number. Diaconis and Graham (1977, *J. Roy. Statist. Soc. B* 39: 262–268) treat the footrule as a metric on permutations and prove `I ≤ D ≤ 2I` against Kendall's `I`. Mannila (1985, *IEEE Trans. Computers* C-34: 318–325) axiomatised measures of presortedness (`Inv`, `Runs`, `Rem`, `Exc`); Estivill-Castro and Wood (1992, *ACM Computing Surveys* 24: 441–476) survey a dozen such measures (`Dis`, `Max`, `Osc`, `Enc`, `SUS`, `SMS`, `Par`, the footrule) and their relations. Mannila's five axioms say nothing about monotonicity under an adjacent exchange of an inverted pair; the property proved here for `Inv` and `Foot` and refuted for `Des` (Lemma 3) is not part of the standard axiomatics, and no textbook or paper was found that states Lemma 3's counterexample explicitly. It is elementary enough that nobody needed to write it down. What appears to be new is not the mathematics but its use: reading a claimed behavioural competency on two rulers at once and showing it exists on only one.

## 7.3 Sorting with immovable elements: no prior analysis found

No literature was found that analyses the effect of an immovable *element* on sorting dynamics or on disorder measures. The nearest bodies of work model something else. Fault-tolerant sorting networks (Yao & Yao 1985, *SIAM J. Comput.* 14: 120–128; Rudolph 1985; Assaf & Upfal 1990; Leighton, Ma, Plaxton & Suel 1997; Piotrów 2004) treat a *passive* faulty comparator that "passes its inputs through without comparing them", and ask how much redundancy restores correctness; a stuck comparator in odd-even transposition sort on a linear array is the exact analogue of an immovable frozen cell, but no paper works out its effect on trajectories. In interacting-particle physics, the asymmetric simple exclusion process with a blockage (Janowsky & Lebowitz 1992, *Phys. Rev. A* 45: 618; 1993) has a fully blocked bond decouple the chain into independent segments, which is the partition lemma in another vocabulary, applied to currents and shocks rather than to sortedness. The partition observation of §4.4, as applied to a disorder measure and a run statistic, appears to be unpublished in this form.

## 7.4 Ratio and normalised-score artefacts: the denominator effect has a literature, the application is new

That a mean of ratios is inflated when denominators are small or variable is classical (Jensen's inequality; Hartley & Ross 1954; Cochran's *Sampling Techniques*, ch. 6; Ruel & Ayres 1999, *Trends Ecol. Evol.* 14: 361–366 for the ecological statement). Spurious correlation of ratios goes back to Pearson (1897, *Proc. R. Soc.* 60: 489–498) and is revisited by Kronmal (1993, *J. R. Statist. Soc. A* 156: 379–392); Curran-Everett (2013, *Adv. Physiol. Educ.* 37: 213–219) and Packard & Boardman (1988) treat normalised data in physiology; Vickers (2001, *BMC Med. Res. Methodol.* 1: 6), Cronbach & Furby (1970) and Törnqvist, Vartia & Vartia (1985, *Am. Statist.* 39: 43–46) treat change scores and relative change. The closest structural analogue to the paper's statistic is Hake's normalised gain in physics education, `g = (post − pre)/(max − pre)`, which divides by a quantity that shrinks under a constraint: Bao (2006, *Am. J. Phys.* 74: 917–922) shows the mean of individual gains and the gain of means differ; Marx & Cummings (2007, *Am. J. Phys.* 75: 87–91) document the "bias towards low pretest scores" and the asymmetric range; Nissen et al. (2018, *Phys. Rev. Phys. Educ. Res.* 14: 010115) show the bias in favour of populations with higher pretest scores. Length-biased sampling and the inspection paradox (Feller vol. II) cover the general fact that episodes truncated by a constraint are not a representative sample of episode lengths. No source states the precise mechanism found here, that a constraint which shortens excursions inflates a per-excursion `(recovery − setback)/setback` statistic; the Hake-gain and mean-of-ratios literatures are the right citations and the application to partition-truncated episodes appears to be new.

## 7.5 Observer-relativity of competency attribution: an old debate the paper does not join

The attribution of purpose to a system from its behaviour alone was framed as observer-relative at the origin of cybernetics: Rosenblueth, Wiener & Bigelow (1943, *Phil. Sci.* 10: 18–24) write that "purposeful behavior is one that may be *interpreted* as directed to the attainment of a goal", and Taylor's objection (1950, *Phil. Sci.* 17: 310–317, with the reply and rejoinder in the same volume) is that a black-box account cannot distinguish purpose from regularity. Dennett's intentional stance (1971, 1987) and "Real patterns" (1991, *J. Phil.* 88: 27–51) give the standard criterion for a pattern being real: that it supports prediction and compression beyond the bit-map. Braitenberg's *Vehicles* (1984) states the "law of uphill analysis and downhill invention": observers over-estimate the internal complexity of mechanisms whose behaviour they read as foresight or optimism. Computational mechanics (Crutchfield & Young 1989; Shalizi & Crutchfield 2001, *J. Stat. Phys.* 104: 817–879) locates structure in the observer's modelling class and defines causal states as classes of histories with identical conditional futures. Coarse-graining dependence of "emergent" structure is the live form of the same point: critiques of causal emergence (Dewhurst 2021; Eberhardt & Lee 2022) and the transformation-invariant alternatives of Barnett & Seth (2023, *Phys. Rev. E* 108: 014304) and Rosas et al. (2024, arXiv 2402.09090) demand that a claimed macroscopic process survive a change of description. Bruineberg et al. (2022, *Behav. Brain Sci.* 45: e183) make the parallel distinction for Markov blankets. Within the basal-cognition literature, Levin's own TAME paper (2022) leaves open "whether these spaces have any objective reality", and general scepticism about the literal use of cognitive vocabulary exists (Figdor 2018; Adams 2018; Fábregas-Tejeda & Sims 2025). No paper was found that states, as a criterion, that a claimed competency must be invariant under change of measurement coordinates before being attributed to the system.

## 7.6 The two-test criterion: components exist, the conjunction appears not to

The history test (§8.3, criterion 2) has a formal precedent: the Markov-property tests of Chen & Hong (2012, *Econometric Theory* 28: 130–178; null hypothesis that the current state "will contain all information about the future behavior of the process that is contained in the current information set"), and, closer still, the causal-state construction of Shalizi & Shalizi (2004, UAI), in which a history is split from a state when a two-sample test (χ² or Kolmogorov–Smirnov) rejects equality of its conditional future distribution with the state's. C6b is that test applied to the sorting worlds with the futures sampled from identical states carrying different pasts. The ruler test (criterion 1) has the transformation-invariance demand of Barnett & Seth and the causal-emergence critics as precedent, and Mannila's second axiom (order-isomorphic inputs get the same measure) as a much weaker cousin. No source combines the two as a criterion for attributing a competency to a system rather than to its description. The conjunction can be presented as Shalizi–Crutchfield causal-state sufficiency joined to coarse-graining invariance, with Braitenberg and Dennett as the motivation.

## 7.7 Limits of the sweeps

Two sweeps by separate contexts of the same model on 14 October 2026, with web search and fetching; items marked above as read were read from fetched text, the rest rest on search results and secondary sources and should be checked against the originals before citation in print. Knuth's page numbers are from secondary citations. The sweeps are not a systematic review; a formal citation search (Semantic Scholar, OpenAlex, Google Scholar "cited by") was attempted for the paper's reception and is reported in §7.1 with its coverage.


# 8. Metaphysical positions

## 8.1 The authors' disposition

Three commitments are visible in the paper and its afterlife. (i) *Competency realism*: behaviours not stated in the rules are the system's own competencies, to be discovered by observation ("unexpected", requiring "a different set of conceptual tools to predict"). (ii) *The cognitive light cone*: any system is an agent at some scale, and the right question is which scale (TAME). (iii) *Platonic ingression* (Levin 2026): patterns of form and behaviour pre-exist in a non-physical space and are exploited by physical systems that reach them, so that a memoryless system can nonetheless show a pattern that is not "in" its rules. The sorting arrays are offered as a minimal demonstration of (iii).

The authors also hold, in the same paper, that "there is no magic here" and that everything follows from the rules. The two commitments sit side by side: the behaviours are consequences of the rules, *and* they are competencies of the system. The question the replication raises is whether both can be held once the measurement frame is made explicit.

## 8.2 What the declared-ruler reading says instead

**The competency is in the ruler, not in the system.** On the global rulers nothing regresses; the setback exists only in neighbour-coordinates. A pattern that appears under one coordinate choice and vanishes under another, with the system untouched, is a property of the coordinates. This is a Kantian point rather than a Platonic one: the form is contributed by the frame of observation, not reached by the system.

**The system has no inside.** State-sufficiency means there is no fact about a cell's past that its present does not already contain. "Patience" and "delayed gratification" are dispositional words: they describe a present shaped by a remembered past and an anticipated future. Nothing here is shaped by a past. CRR's own commitment (an agent carries its mass) finds nothing to carry, and for the same reason no stance-based attribution finds anything either. On this point CRR and the authors' critics agree against the authors, and the paper's own abstract ("no memory") is on the critics' side.

**Obstacles subtract, they do not occasion.** Where the score rises the obstacle has removed degrees of freedom (partition) and the statistic has divided by a smaller number. The disposition that reads an obstacle as an occasion for problem-solving reads a quotient as a quality. Goldstein's "free lunch" is here precisely: an apparent contribution from the system that is a loss read through a normalised measure.

**The one real surprise is a defect.** The selection pointer's overshoot is unexpected behaviour. It is also a bug, and it is a *regression* on the global ruler. The competency disposition would read it as exploration; the invariant reads it as the rule failing its own guarantee. The two readings are decidable, and they were decided by writing the invariant down first.

**Created or discovered, for this case.** The CRR fork that would make a Platonic library decidable (studied in C3 of the same study) is: transfer to a naive instance without a physical channel, and survival of a physical reset. The sorting worlds cannot run that test, so they neither support nor refute ingression. What they do is show that each pattern offered as evidence of it is, one by one, a consequence of rules plus ruler. That shifts the burden: the forms are not discovered in these systems; they are written into the choice of what to count.

## 8.3 Two criteria for attributing a competency to a system

The replication suggests that any claimed competency should pass two tests before it is granted to the system rather than to its observer:

1. **Ruler invariance.** The pattern survives a change of sortedness ruler (or, generally, of the coordinates in which the behaviour is read). Delayed gratification fails: present on `Des`, absent on `Inv` and `Foot`.
2. **Carried history.** The pattern depends on something the system carries that is not in its present state (a two-sample test of futures from identical states with different pasts). Delayed gratification fails: the worlds are state-sufficient.

These are not CRR theses; they are what CRR's carrier discipline and path-dependence commitment amount to when turned into tests. A pattern that passes both would be a candidate for being the system's own, and then (and only then) the question of where it comes from would be open.

## 8.4 What remains undecided

The paper's cell-view level at zero frozen cells (0.24 against 0.39) and the source of its reported rise with *movable* cells. Both would be settled by the authors' saved trajectories or by the step between their snapshots and their table. Until then the published numbers are neither reproduced nor shown to be wrong; what is shown is that the committed code does not produce them, and that where a rise exists in the family of conditions the code can run, it is a measurement artefact.

# 9. Implications and next steps

## 9.1 For the authors (a proposed note; the owner decides whether to send it)

- Request the saved `csv/*.npy` trajectories behind the published table and the code that produced the `cannot_move` and `original_*_with_kfrozen` records.
- Report the three code defects (§6.6) and the selection pointer overshoot, with the runner and declaration so they can reproduce every number here from their own files.
- Propose the ruler-invariance check as a referee-level control: report DG on `Inv` and `Foot` beside `Des`. If it is zero there, say so.
- Propose the partition control: report DG for the textbook algorithm with the same immovable cells. If it rises there too, the rise is not the cells'.
- Report medians beside means for DG, and fix the early-exit path.

## 9.2 For the Phoenix programme

- **Ledger.** Nothing enters the survival ledger; seven graded heuristic rows and decision D112 are recorded (`HEURISTIC/LEDGER.md`, 2026-10-14). The grade for the Platonic claim is NOTHING; for the carrier discipline, DISTINCTION; for the mechanism question, QUESTION (the question was CRR's, the answer was arithmetic).
- **Register.** The two criteria of §8.3 are a candidate addition to `EPISTEMIC/GUARDRAILS.md` as a test any imported "competency" claim must pass before Phoenix treats it as a phenomenon to explain. Owner's decision.
- **The C3 fork is the real test of ingression**, and it needs a system with a carried past. The sorting worlds have none; planaria (T2/T3 in the Platonic-space note: the remodelling clock; the cross-switch experiment), neural cellular automata with persistent hidden state, and the authors' own later systems with memory are where the fork can be run. The next synthetic step is cheap: a sorting world with a one-parameter memory (the fatigue rule already built) in which the C3 transfer and reset tests are run, to show what passing and failing look like before any wet-lab or NCA design.
- **For the website.** This study is a clean example of what the programme offers an outside researcher: not a result about CRR, but a reproducible reading of someone else's result that changed what it means. The epistemic statement should say so in those words.

## 9.3 For the wider conversation

The sorting arrays are a small case of a larger pattern in the basal-cognition literature: competencies attributed from a chosen measurement frame to a system with no inside. The remedy is not a competing metaphysics but a pair of controls, cheap in any simulation: change the ruler; carry the history. Where a pattern survives both, the metaphysical question is live. Where it survives neither, the question has been answered by the controls, and the Platonic reading has nothing left to explain.

# 10. Reproducibility

All files are in `Phoenix_Egg/studies/MP-REBUS-PLATONIC-CHECKS-2026-10-14/` on branch `claude/busy-franklin-yvjak0` of `alexsabine/Phoenix-1-`:

- Declarations (committed before each run): `DECLARATION.md` (C5), `DECLARATION_ADDENDUM_C5B.md`, `_C6.md`, `_C6B.md`, `_C7.md`, `_C8.md`.
- Code: `checks/c5_sorting_surplus.py`, `c5b_sorting_surplus_run2.py`, `c6_sorting_battery.py`, `c6b_state_sufficiency_visits.py`, `c7_authors_code_runner.py`, `c8_scheduling_stickiness.py`.
- Outputs (pinned): `outputs/c5*`, `c6_sorting_battery.{txt,json}`, `c6b_*`, `c7_authors_code_run.json`, `c7_authors_code_run_poll005.json`, `c7_mover_runs_posthoc.json`, `c8_*`, and the run logs.
- Results and incidents: `RESULT.md` §C5–C8.
- Manifest: `AGENTS/manifests/2026-10-14_sorting_arrays_C6_C8.yaml`; release tree verified by `scripts/verify_release.py` against `MANIFEST.sha256`.

To re-run C7: clone `Zhangtaining/cell_research` at 1fd2bd5 into a directory outside the repository and run

```
python3 -I checks/c7_authors_code_runner.py --clone <path> --exps 100 --frozen 0,1,2,3 --poll 1.0
```

Thread scheduling is the operating system's; on this Linux/CPython 3.13 the trajectories were reproducible given the seed, but that is a property of the machine, not of the code.

# Appendix A. Proof details

**A.1 Lemma 1 in full.** Let `a` be the arrangement, `o = a[p]`, `v = a[q]`, `p < q`, `v < o`. Partition the other values into: (α) values at positions outside `[p, q]`: their relative order to both `o` and `v` is unchanged by the swap, since both `o` and `v` stay within `[p, q]`. (β) values `w` at positions in `(p, q)` with `w < v`: before the swap `o` is left of `w` with `o > w` (inverted) and `v` is right of `w` with `v > w` (in order); after it `v` is left of `w` with `v > w` (inverted) and `o` is right of `w` with `o > w` (in order): net 0. (γ) values `w` in `(p, q)` with `w > o`: symmetric, net 0. (δ) values `w` in `(p, q)` with `v < w < o`: before, `(o, w)` inverted and `(w, v)` inverted; after, `(v, w)` in order and `(w, o)` in order: net −2 each. (ε) the pair `(o, v)` itself: −1. Total `−(2k + 1)`. ∎

**A.2 Lemma 2.** Only the two swapped values change position. Before: `|p − o| + |q − v|`; after: `|p − v| + |q − o|`. Difference `= (|p − v| − |q − v|) − (|p − o| − |q − o|) = g(v) − g(o)` with `g(x) = |p − x| − |q − x|`. For `p < q`, `g` is nondecreasing in `x` (it is `−(q − p)` for `x ≤ p`, rises with slope 2 on `[p, q]`, and is `q − p` for `x ≥ q`); with `v < o`, `g(v) ≤ g(o)`. ∎

**A.3 Lemma 5.** Let `I(v)` be the set of values inverted with `v`. Each swap involving `v` is with an adjacent neighbour `w` that is out of order with `v`, hence `w ∈ I(v)`, and after the swap `(v, w)` is in order and, by Lemma 1 with `k = 0`, no other pair's order changes; so `|I(v)|` falls by exactly one. No swap not involving `v` changes `I(v)` (it changes only the swapped pair's order). At termination `I(v) = ∅`. ∎

# Appendix B. The authors' statistic on a worked example

Trace of `Des` after successive swaps: 40, 41, 42, 40, 39, 40, 38. De-duplicated differences: +1, +1, −2, −1, +1, −2. Runs: +2, −3, +1, −2. Pairs: (2, −3) scores (3 − 2)/2 = 0.5; (1, −2) scores (2 − 1)/1 = 1.0. DG = 0.75. Partition that shortens the first setback from 2 to 1 with the same recovery of 3 gives (3 − 1)/1 = 2.0 for that episode: the score rises with nothing in the recovery changed. If the trace instead ended on an increase (… 40, 41), the early exit returns the sum 1.5, not the mean 0.75.
