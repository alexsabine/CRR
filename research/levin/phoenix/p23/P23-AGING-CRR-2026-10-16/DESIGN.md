# P23-AGING-CRR (OD-49): how CRR applies to repair timing and content in the ageing NCA

The owner's question: does CRR's account of *time* help decide **when** to repair an ageing tissue and **from what
part of its past**? P23-AGING found that the published repair (reset damaged cells to the primordial state when an
organ's score falls to 0.6) works, and that a lost organ's own trace helps only within about 10 steps of the loss.
This study derives the CRR operations from `CORE/MATHEMATICS.md` for this system, sets each against its strongest
ordinary rival, and tests them on the authors' code (bhartl/muse 9404ec3, unchanged).

## 1. Mapping, term by term

| CRR (CORE) | this system | choice fixed here, and why |
|---|---|---|
| statistical carrier (I) | per organ, the product of each organ cell's cell-type distribution p_i = softmax(type channels) | the model expresses type by argmax of three channels; the softmax is its natural categorical distribution. A carrier on raw states would be dominated by the injected white noise; CORE IV warns that white noise fed into ds gives unbounded variation |
| Fisher–Rao arc, coherence (I) | Δs_t = sqrt(Σ_i d_FR(p_i,t−1, p_i,t)^2), d_FR = 2 arccos Σ_k sqrt(p_k q_k); coherence = Σ Δs since the last cut | the exact Fisher–Rao distance for categoricals; for a product the squared distances add |
| cut = first passage of coherence to a (II) | a cut occurs when the organ's coherence since the last cut first reaches a = π | π is the Fisher–Rao distance between two pure cell types (vertices of the categorical sphere): a cut fires when one whole cell's worth of type change has accumulated. Fixed from the geometry, not tuned on outcomes |
| content of a completed occasion Φ_n (V) | mean raw organ state (all 4 channels of every organ cell) over the steps of the occasion | flat content coordinates, where CORE V's recursion is exact |
| regeneration m_(n+1) = q m_n + (1−q) Φ_n, explicit prior m_0 (V) | per organ seed, m_0 = the primordial (genome-coded) organ state | past-only (Heaviside gate): only completed occasions enter |
| "no universal value of q" (V) | q calibrated on development seeds, then frozen | |
| reset/impulse must be specified independently (V) | the repair writes the seed into the organ's wrongly expressed cells (the paper's method-B write) and clears their RNN memory | the paper's own write operation, so only content and timing change |

**What this predicts, and what the ordinary rival predicts.**
- **Content.** The paper's primordial reset is the q → 1 limit of the CRR recursion (the seed never leaves m_0).
  Restoring the last occasion is q = 0. The CRR claim is that an intermediate q is better than both: it averages
  out noise and still carries the organism's own realised (mature, hidden-channel) state.
  - Ordinary rival A: restore a **healthy checkpoint**, the organ's state at the last step its score was ≥ 0.9
    (backup and rollback).
  - Ordinary rival B: write the **canonical target** (organ-typed, hidden channel 0; the authors' own alternative).
  - Ordinary rival C: an **exponential moving average sampled on a clock** with the same q (CORE V's recursion is
    mathematically an EMA). Only the CRR cut sampling separates C from CRR.
- **Timing.** CRR regenerates at every cut, so repair is driven by accumulated change, not by a damage level.
  - Ordinary rival D: the paper's **damage threshold** (score ≤ 0.6, at most once per 25 steps).
  - Ordinary rival E: **periodic repair** on a clock with the same mean interval as the CRR cuts (matched number of
    repair occasions).
  - Ordinary rival F: **immediate repair** of any wrong organ cell at every step, an upper reference with maximal
    cost.

  If cut timing beats clock timing at matched cost, the native name is event-triggered (Lebesgue) sampling and
  control (Åström & Bernhardsson 2002). CRR's contribution would be the specific trigger (Fisher–Rao arc of one
  cell flip), not the idea of event triggering.

## 2. Arms

All arms repair the three organs (left eye, right eye, mouth) after development (step 150), at noise 0.15 (0.125 as
sensitivity), competency 1.0, 1,000 steps. Each organ has its own tracker.

| arm | when | what is written into wrong organ cells |
|---|---|---|
| NONE | never | — |
| C_PRIM (paper method B) | score ≤ 0.6, horizon 25 | primordial state |
| C_TARGET | same | canonical organ state [−3, −3, 3, 0] |
| C_CKPT | same | last healthy checkpoint (score ≥ 0.9) |
| C_CRR | same | CRR seed (cut-sampled, q) |
| C_EMACLOCK | same | EMA seed sampled every Δ steps, same q |
| S_CRR | every CRR cut | primordial state |
| S_CLOCK | every Δ steps | primordial state |
| S_IMMEDIATE | every step | primordial state |
| S_CRRFULL | every CRR cut | CRR seed |

Δ is the mean CRR inter-cut interval after step 150, measured on development runs. q is chosen on development seeds
from {0, 0.5, 0.8, 0.9, 0.95, 0.99}.

**Must-pass controls.**
- C_CRR with q = 1 reproduces C_PRIM exactly.
- The re-implemented C_PRIM reproduces the authors' own `recovery.set_initial_state` method-B run (P23-AGING
  B_RESET) exactly on the same seeds.

**Endpoints.**
- Primary: mean fitness over steps 150–1000 (as in P23-AGING).
- Cost: total number of cell writes.
- Reported: organs intact at the end and the share of time all organs are intact.

## 3. Calibration on development seeds 0–9 (before the freeze)

- **Must-pass.** C_PRIM reproduces the authors' method-B run (P23-AGING `B_RESET`) cell for cell on all ten seeds.
  C_CRR with q = 1 equals C_PRIM. NONE equals P23-AGING NONE.
- **CRR cuts without repair.** After step 150 there are 14–16 cuts per eye and 26 for the mouth, so the CRR timescale
  is 32–67 steps.
- **q.** Late fitness rises with q:

  | q | 0 | 0.5 | 0.8 | 0.9 | 0.95 | 0.99 | 1 |
  |---|---|---|---|---|---|---|---|
  | C_CRR | 191.2 | 191.9 | 192.9 | 194.6 | 196.7 | 204.8 | 205.9 (= C_PRIM) |

  The best interior value, **q = 0.99**, is frozen. The calibration already favours the q = 1 boundary, which is the
  paper's own primordial reset.
- **Matched clock.** S_CRR has 40.5, 47.0 and 82.2 cuts after step 150 (left eye, right eye, mouth), so
  **Δ = 21, 18, 10 steps** per organ.
- **Rival added after the first calibration.** S_ANY repairs as soon as any organ cell is wrong, at most once per H
  steps; it is the early damage-triggered rival to CRR's early, activity-triggered repair. H was chosen from
  {5, 10, 15, 20, 30} to match S_CRR's number of repair events (157.6): **H = 15** (147.1 events).
- **Content variants with the canonical target added** (S_CRR_TARGET, S_CLOCK_TARGET), because C_TARGET was the best
  content in calibration.

Development results (late fitness): NONE 191.6; C_PRIM 205.9; C_TARGET 210.4; C_CKPT 205.3; C_CRR(0.99) 204.8;
C_EMACLOCK(0.99) 204.6; S_CRR 217.9; S_CLOCK 218.0; S_ANY(15) 217.9; S_IMMEDIATE 217.8; S_CRRFULL(0.99) 215.9;
S_CRR_TARGET 220.6; S_CLOCK_TARGET 222.0.
