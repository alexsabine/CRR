# P23-AGING report (OD-48, 2026-10-16): stale versus lost memory in Levin's team's ageing model

**Status.** Frozen test. The protocol (`PREREG.md`) was frozen at commit 14cbb5c and its decision script at
cc138ae, both before any test seed ran. Development used seeds 0–9; the test used seeds 1000–1049 (and 2000–2019 for
the noise sweep). Two exploratory follow-ups were run after the test and are labelled as such. The model is the
authors' code, unchanged. CPU only, no API spend. One builder; the same model in another context would not be an
independent replication.

**Question (from OD-48).**
1. Search Levin's team's work on cancer and ageing.
2. Run checks on their code, carrying over the question from P23-ALGOTYPES: does *stale* stored memory block repair,
   as it did in the sorting cells, or is the problem *lost* memory, as the team's ageing papers propose?

## Answer

1. **Search.** Of the team's ageing and cancer papers, only one has runnable code: the ageing model of Pio-Lopez,
   Hartl & Levin (2025, *Adv. Sci.* e09872). The paper itself links no code ("available on request"). The code sits
   in co-author Ben Hartl's public repository `bhartl/muse` (commit 9404ec3), with a pretrained agent and the
   notebooks behind the figures (§1).
2. **The cells' memory carries nothing over time.** Each cell has a small recurrent network with 4 internal values.
   That network recomputes its state from the current inputs at every step (4 internal iterations). After every
   cell's memory is wiped to zero:
   - one step later the memory differs from the unwiped run by 0.003 on average (1% of its typical size, 0.28), at
     most 0.037;
   - no cell type ever changes as a result (20/20 lifetimes, two noise levels).

   So the stale-memory failure seen in the sorting cells cannot arise in this model. The authors' repair code always
   cleared this memory. Keeping it instead gives equivalent results in 5/5 frozen comparisons, with paired
   differences of at most 0.05 fitness units out of 256.
3. **No lasting "memory of lost structures".** Take an organism whose left eye was lost at step 300 and one whose
   left eye never formed, with identical noise.
   - **Convergence.** They converge to the same state in 48/50 lifetimes (median 38.5 steps; 28/30 at step 600,
     median 11 steps). Neither ever regrows the eye by itself (0/50, 0/30).
   - **Single injection.** Given the paper's regenerative injection at the moment of loss, the just-lost eye regrows
     more often (12/50 vs 0/50 survive 50 steps, p = 0.0005). With any delay of 10 steps or more, the advantage
     disappears (0/50 vs 0/50 at every delay from 10 to 200).
   - **Repeated repair.** The paper's repeated targeted repair (method B), started 50 or 200 steps after the loss,
     keeps an eye that never existed going exactly as well as one that was lost (eye present 40% vs 40% of the time;
     identical at 200).

   Regeneration here is driven by the injected primordial state and the cells' fixed program. A trace of the lost
   organ helps only for a few steps after the loss. The paper's "memory of lost structures" (high information
   storage at the former eye site) is therefore not information about the lost eye in this agent.
4. **Ageing needs noise.** At noise 0 and 0.025, nothing declines after step 150 and no organ is lost (20/20
   lifetimes each). Without noise the pattern settles once, from 246 to 226 by step 100, and then stays fixed for
   good. Decline grows steadily with noise (Spearman ρ = 0.93):

   | noise | 0.05 | 0.1 | 0.15 | 0.2 |
   |---|---|---|---|---|
   | fitness lost, steps 150–1000 | 1.2 | 8.4 | 35.8 | 39.7 |
   | organs lost by step 1000 (of 3) | 0 | 0.5 | 2.25 | 3 |

   So the abstract's "even without noise" holds only for the one-time settling after development, not for
   progressive ageing. The paper's own §4.2.2 says the noise of 0.125 used "leads to accumulated damage".
5. **The paper's repair result reproduces.** Targeted repair (method B) beats no repair by 15.3 fitness units
   [95% CI 13.5, 17.1]. Whole-organ repair (method A) gains 3.7, within the ±5 predicted from the paper's "not
   sustainable". At the paper's noise of 0.125, method B needs about 9 interventions per lifetime (the paper reports
   5–15). The organ-plus-socket variant does best (213 vs 212). Clearing memory alone, with no injection, does
   nothing.

## 1. Search (complete as of 2026-10-16)

Sources: PubMed author searches (Pio-Lopez L; Levin M with cancer, ageing or senescence, 2023–2026), the Levin Lab
ageing and preprint pages, and web searches for code.

| work | code |
|---|---|
| Pio-Lopez, Hartl & Levin 2025, *Aging as a Loss of Goal-Directedness*, Adv. Sci. (doi 10.1002/advs.202509872) | not linked in the paper; public at github.com/bhartl/muse `examples/aging-as-loss-of-goal-directedness` (**run here**) |
| Pio-Lopez & Levin 2024, *Aging as a loss of morphostatic information*, Ageing Res. Rev. (doi 10.1016/j.arr.2024.102310) | review, none |
| Pio-Lopez & Levin 2025, *Atavistic Genetic Expression Dissociation (AGED) during aging*, Aging Cell (doi 10.1111/acel.70305) | meta-analysis; no code found |
| Pio-Lopez & Levin 2023, *Morphoceuticals*, Drug Discov. Today (doi 10.1016/j.drudis.2023.103585) | review, none |
| Gumuskaya et al. 2025, *Anthrobots life cycle* (epigenetic age reduction), Adv. Sci. (doi 10.1002/advs.202409330) | wet lab |
| Kapsetaki et al. 2025, *Bioelectrics of immortality and mortality in Hydra*, Bioelectricity (doi 10.1089/bioe.2025.0002); Sediqi & Levin 2025, senescing keratinocytes, iScience | wet lab |
| Pio-Lopez & Levin 2025, *MultiXVERSE* (GABA–cancer link), BMC Bioinformatics (doi 10.1186/s12859-025-06158-5) | network-embedding tool; not an ageing or memory model |
| Pio-Lopez, Hartl & Levin 2026, *BraiNCA*, arXiv:2604.01932 | github.com/LPioL/BraiNCA; morphogenesis and motor control, not ageing (not run) |
| Pigozzi, Cirrito & Levin 2025, *AI-guided resetting of memories in gene regulatory network models*, bioRxiv | **not checked**: bioRxiv rate-limited the request; the most relevant open item for memory resetting |
| 2026 preprints: Pio-Lopez, Jawanda & Levin, *Theories of Aging*; Pio-Lopez & Levin, *Multi-Scale Longevity*; Lyons, Pio-Lopez & Levin, *From Cancer to AI Alignment*; Grodstein, Mathews & Levin, cancer membrane voltage (bioRxiv) | theory, or not retrieved (403/429) |

## 2. The model and set-up

- **The model.**
  - A 16×16 grid of cells. Each cell has 4 state channels: 3 cell-type channels and 1 hidden channel visible to
    neighbours.
  - Each cell senses its neighbours, averages their embeddings, and passes the result through a recurrent
    gene-regulatory-style network (RGRN, 4 hidden units, 4 internal iterations per step). The output is the
    update to its own state.
  - The network was evolved (CMA-ES) to grow a smiley face within 35 steps.
  - Fitness is the number of correctly typed cells, at most 256.
- **Runs.** Fresh world per lifetime, seeded, so arms are paired and identical up to their first difference.
  Settings are those of the published notebooks: noise 0.15, competency 1.0, 1,000 steps, repair threshold 0.6,
  development 150, horizon 25. The paper's stated noise, 0.125, was run as a sensitivity check.
- **Environment.** The pinned training stack uses `numpy.product`, which numpy 2 removed, so a Python 3.11
  environment with numpy 1.26 was built; no code was edited. The configuration files were read before running.
  They contain no executable content beyond class locations and one `Box(...)` expression.

**Development (seeds 0–9).**
- Method B beat no repair by +14.2 (9 of 10 seeds).
- Keeping memory equalled clearing it.
- Memory-only repair did nothing.
- At noise 0 there was no decline.
- Wiping all memory at step 300 changed no cell type.
- Lost and never-formed eyes converged.

These predictions were frozen.

## 3. Frozen results (seeds 1000–1049)

**Q1: stale memory in repair.** The frozen rule calls a contrast equivalent if the 95% CI lies within ±2.

| contrast (clear minus keep memory) | mean diff | 95% CI | verdict |
|---|---|---|---|
| method A, noise 0.15 | +0.019 | [+0.010, +0.032] | equivalent |
| method B, noise 0.15 | +0.047 | [−0.118, +0.278] | equivalent |
| method B + sockets, noise 0.15 | −0.036 | [−0.140, +0.047] | equivalent |
| method A, noise 0.125 | +0.007 | [+0.004, +0.011] | equivalent |
| method B, noise 0.125 | +0.007 | [−0.038, +0.045] | equivalent |

**Q2: memory duration (20 lifetimes per noise level).**
- **Memory, after wiping all RNN memory at step 300.** One step later it differs from the unwiped run by 0.003 on
  average and 0.037 at most; two steps later, by at most 0.010. The typical size is |m| = 0.28 on average and 0.33
  at most.
- **Cell types.** After the wipe, the share of cells with a different type is 0.0002 at step 301 and 0 at steps 310,
  400 and 1000. The full state returns to within 0.01 in every lifetime (median 78 steps at noise 0.15, 47 at 0.125).
- **Hidden-channel wipe.** Zeroing every cell's hidden channel leaves longer-lived differences, a median 224–303
  steps to converge, but changes at most 0.3% of cell types.
- **One frozen prediction failed.** I predicted the *largest* memory difference one step after the wipe would be
  under 10% of typical size. It was 13% (0.037 against 0.28). The average difference was 1%. The prediction missed
  on its maximum criterion, and the miss is recorded as such.

**Q3: memory of the lost structure.** The left eye is overwritten with a face-typed state at T (LOST), or held there
from step 0 to T (NEVER). Its memory is cleared, it is released at T, and the noise is identical in both.
- **(a) Convergence.** The full states converge below 0.01 and stay there in 48/50 lifetimes (T = 300, median 38.5
  steps, range 9–296) and in 28/30 (T = 600, median 11). Both clear the frozen 90% bar.
- **(b) Spontaneous regrowth.** 0/50 and 0/30 in both arms.
- **(c) Paper's injection at T.**
  - At T = 300, LOST regrows (eye score ≥ 0.6 fifty steps later) in 12/50 lifetimes against 0/50 for NEVER (exact
    McNemar p = 0.0005). The mean eye score over the next 100 steps is 0.31 vs 0.09 (Wilcoxon p = 1.6e-8).
  - At T = 600, the advantage is not detectable: 2/30 vs 0/30 (p = 0.5), mean eye score 0.15 vs 0.09 (p = 0.64).

  As fixed in advance, (c) reads as a short-lived effect of the surrounding tissue. The exploratory delay test (§4)
  measures how short.

**Q4: noise.** See the Answer, point 4. Noise 0 is deterministic: all 20 seeds give the same lifetime, 226 from
step 100 to step 1000. At noise 0.025 the 20 lifetimes stay at 226.4 throughout.

**Q5: the paper's repair.**
- Method B vs no repair: +15.3 [13.5, 17.1], different (predicted).
- Method A vs no repair: +3.7 [2.8, 4.6], within ±5 (predicted).
- Memory-only repair vs no repair: +0.02, equivalent (predicted).

## 4. Exploratory (after the test; not frozen)

**Delay between loss and injection** (`analyze_delay.py`; T = 300, 50 lifetimes per cell):

| delay (steps) | regrown 50 steps after injection, LOST / NEVER | cell types identical at injection |
|---|---|---|
| 0 (frozen run) | 12 / 0 | 10% of lifetimes |
| 10 | 0 / 0 | 92% |
| 25 | 0 / 0 | 92% |
| 50 | 0 / 0 | 92% |
| 100 | 0 / 0 | 92% |
| 200 | 0 / 0 | 94% |

**Repeated targeted repair** (method B for the left eye, starting T + delay):

| delay | eye present, share of time, LOST / NEVER | late fitness, LOST / NEVER |
|---|---|---|
| 0 | 0.60 / 0.41 | 197.1 / 195.4 |
| 50 | 0.40 / 0.40 | 194.6 / 195.0 |
| 200 | 0.41 / 0.41 (identical) | 194.1 / 194.1 |

The "memory" that helps regrowth lasts under 10 steps after the loss. After that, repair builds an eye from the
injected primordial state equally well whether or not one ever existed.

## 5. Reading

- **What the hidden memory is in this model.** A per-cell recurrent state that is rebuilt from the current inputs
  every step. It is a fast filter, not a store. The only persistent "memory" is the tissue's current pattern itself,
  plus the hidden channel, which relaxes over a few hundred steps. Even the pattern does not keep the history of a
  lost organ for more than a few dozen steps.
- **Stale versus lost memory.**
  - In P23-ALGOTYPES, a persistent internal pointer went stale after damage and blocked repair.
  - Here the internal state cannot go stale, and the tissue cannot keep a lost organ's memory either. What declines
    is the pattern under noise: damage accumulates faster than the evolved controller corrects it once development
    has finished.
  - The reading closest to the code is therefore "noise damage outruns a controller tuned only for development".
    Calling it "loss of goal-directedness" is fair as a description, but it is not an alternative to damage: without
    noise there is no ageing.
- **Relevance to cancer and ageing biology.** This agent has no persistent cell memory (nothing like epigenetic
  marks), so it cannot test whether stale cell memory contributes to ageing. That needs a model whose cells keep a
  slow internal state (see §7). Its rejuvenation result, injecting a primordial state into the cells that are
  wrong, is closer to "re-seed from a template" than to "reactivate a memory".
- **CRR (M7).**
  - Same present, different past: here history leaves no lasting trace (convergence in ≤ 300 steps, usually under
    40). The form is a product of the genome-coded rule plus recent noise, not of its realised history.
  - This is the ordinary, contracting-dynamics (Markov) reading, and it agrees with P23-ALGOTYPES and OOL challenge
    O4: history acts only through stored state, and here almost no state persists.
  - CRR contributed the design (matched present, varied history, renewal at the cut). It made no prediction the
    ordinary model does not make.

## 6. Grades

| claim (paper) | result | grade |
|---|---|---|
| C1 ageing "even without noise" | no decline and no organ loss at noise ≤ 0.025; one-time settling only | **FAILS** for progressive ageing; holds for the post-development settling |
| C4 "memory of lost structures … reactivated for restoration" | lost and never-formed tissue converge (median 38.5 steps); injection advantage lasts < 10 steps; delayed repair is equal for both | **FAILS** as information about the lost organ beyond a few steps |
| C5 targeted regenerative information rejuvenates | method B +15.3; sockets best; 9 interventions at noise 0.125 | **REPRODUCED** |
| Stale cell memory blocks repair (carried over from P23-ALGOTYPES) | memory rebuilt each step; keep = clear (5/5 equivalent) | **does not apply** (no persistent cell memory in this model) |

Native terms: recurrent filter with a short effective memory; contraction and synchronisation by common noise;
stochastic damage accumulation against a homeostatic controller.

## 7. Single most informative next experiment

Give each cell a slow internal variable: a leaky memory with time constant τ, a minimal stand-in for an epigenetic
mark. Evolve or fine-tune this agent to the same smiley target, then rerun the frozen Q1 and Q3 arms across τ. The
question is whether a crossover appears:
- at small τ, as here, nothing is stale and nothing is remembered;
- at large τ, memory might either preserve organs ("memory of lost structures" becomes real) or go stale and block
  repair (the sorting-cell failure).

The τ at which keeping versus clearing memory starts to matter is the quantity that would connect this model to
epigenetic ageing and partial reprogramming.

## 8. Departures and failures (recorded before interpretation)

- One frozen Q2 prediction failed on its maximum criterion (13% against < 10%); see §3.
- `aging_checks.py` was extended after the test with exploratory options (`--delay`; arms LOST_B and NEVER_B). With
  `--delay 0` it reproduces the frozen LOST_INJ run exactly (checked on 2 seeds). The frozen hash in `FREEZE.sha256`
  is of the pre-extension file (commit 14cbb5c).
- The driver uses a fresh world per lifetime. The published notebooks reuse one world across episodes, whose log
  then has unequal episode lengths (1,001 and 1,000 entries). A fresh world keeps episodes independent and paired.
  This was a development-stage choice, made before the freeze.
- The paper's figures use noise 0.15 in the notebooks but state 0.125 in the text. Both were run.
- The history test removes the eye acutely (overwrite at T) rather than by natural ageing. The paper's AIS
  observation concerns gradual loss; the convergence result does not depend on how the eye was lost, but the
  difference is noted.
- Not checked: the AIS/TE computation itself (the paper names no software); the noise, competency and connectivity
  ageing schedules beyond the noise sweep; the Pigozzi et al. GRN memory-reset model.
