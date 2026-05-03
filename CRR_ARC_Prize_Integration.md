# CRR for the ARC Prize

A direct application of the Coherence–Rupture–Reformation (CRR) framework
(documented in `index.html`) to the Abstraction and Reasoning Corpus
(ARC-AGI). This document does two things: (1) restates the CRR mathematics
in a form that can be checked against the source, and (2) shows how each
quantity in that mathematics maps onto a concrete operational decision in
an ARC solver — budget allocation, hypothesis switching, two-shot answer
selection, and stopping.

---

## 1. CRR mathematics, as used here

The canonical CRR system (`index.html`, lines ~2511–2564) is three
equations and one parameter:

```
C(x,t) = ∫₀ᵗ L(x,τ) dτ                           (coherence: cumulative adaptive work)
δ(t − t₀)              with t₀ defined by C·Ω = 1 (rupture: Cramér–Rao saturation)
R[χ](x,t) = ∫_{−∞}^t φ(x,τ) · exp(C(x,τ)/Ω) · Θ(t−τ) dτ   (regeneration: memory-weighted reconstruction)
```

with the adaptive-work rate
```
L = Ω · ε² · κ           (κ = 0.20 in the reference implementation)
```

`Ω` is the only free parameter and is fixed by the symmetry class of the
state-space manifold via Čencov's uniqueness theorem:
```
Z₂  (bistable, Bernoulli manifold, geodesic π):    Ω_Z₂  = 1/π   ≈ 0.3183,  C* = π
SO(2) (rotational, S¹, circumference 2π):          Ω_SO₂ = 1/2π ≈ 0.1592,  C* = 2π
```

The framework also gives:

- **Beauty (criticality) function**: `B(C) = exp(C/Ω) · (C* − C)`, peaking
  at `C = C* − Ω`. This is the "edge of criticality" — one capacity-unit
  before rupture — where the system is maximally responsive and where, in
  the framework's language, "agency lives."
- **Precision**: `π = (1/Ω) · exp(C/Ω)` — a fixed topological piece times a
  growing dynamical piece.
- **Two-channel allocation**: edges of a Markov blanket carry Z₂
  (likelihood) precision; nodes carry SO(2) (prior) precision. The
  free-energy-optimal precision ratio is `π_prior / π_likelihood = √2`
  ("invest √2 times more confidence in priors than in sensory data").
- **CV identity**: `CV = Ω/2 = σ_rupture · Ω` with `σ_rupture = 1/2` from
  the maximum-entropy Bernoulli rupture event. Yields `CV_Z₂ ≈ 0.159`,
  `CV_SO₂ ≈ 0.080`.

The phase machine is deterministic:

```
phase = COHERENCE
loop:
    L ← Ω · ε² · κ
    C ← C + L
    if C · Ω ≥ 1:
        emit δ(now); phase = RUPTURE
        regenerate using R[·]; reset C to 0; phase = COHERENCE
```

The mathematics is internally closed — once the symmetry class is named, Ω
is determined, C* is determined, the rupture time is determined, the
regeneration kernel is determined, and the only thing the world supplies
is the error stream `ε(t)`.

---

## 2. Why ARC is a CRR problem

An ARC-AGI-2 task is a tiny stream of evidence — typically three
demonstration input/output grid pairs (sometimes more) — followed by a
query (usually one test input, occasionally two). The solver must induce
a transformation, then apply it. **Two attempts per test input** are
scored exact-match (no partial credit; output dimensions must also be
correct). A task counts as solved only if *every* test input is solved.

The competition envelope (ARC Prize 2025/2026, Kaggle):
**4× NVIDIA L4 GPUs (24 GB each), 12-hour wall clock, 240 hidden tasks
(120 semi-private + 120 private), no internet**. That gives a hard
average of **≈3 minutes per task**. The grand prize ($700K) requires
&gt;85% on the private set; the 2025 top score was NVARC at 24.03%
(Qwen-4B + test-time training + heavy synthetic data); the human mean is
~66%. So a CRR-grounded solver does not need to beat 85% to be useful —
it needs to compose well with TTT/synthesis pipelines and use its
~3 minutes per task without thrashing.

Reading the task through CRR:

| ARC concept                                      | CRR object                                                      |
| ------------------------------------------------ | --------------------------------------------------------------- |
| A candidate hypothesis class (e.g. "recolour")   | A **regime**                                                    |
| Within a class, parameter search                 | Motion **inside** the regime's manifold                         |
| Mismatch on a training pair                      | Prediction **error ε**                                          |
| Cumulative work spent fitting the class          | **Coherence C** in that regime                                  |
| "We've exhausted this class, switch"             | **Rupture** at `C·Ω = 1`                                        |
| Seeding next class from past attempts            | **Regeneration** weighted by `exp(C/Ω)`                         |
| Per-pixel exact match on a demo                  | **Z₂ channel** (sensory / likelihood)                           |
| Rule consistency across all demos                | **SO(2) channel** (prior / transition)                          |
| Choosing which two answers to submit             | The two natural CRR phases — pre-rupture leader and post-rupture survivor |

The mapping is not metaphorical. Each item is what the CRR equations
already say to do:

- The error-driven work rate `L = Ω·ε²·κ` is a budget that *grows
  fast when the current class is bad*. Bad regimes self-terminate quickly;
  good regimes hover near `B(C) = max` without rupturing.
- The rupture condition `C·Ω = 1` is a hard, principled abort signal that
  prevents the solver from thrashing on a hypothesis class that is not
  going to fit. Per ARC's compute budget (Kaggle: ~12 hours total), this
  gives a non-arbitrary answer to "when do I give up on this approach?"
- The regeneration kernel `exp(C/Ω)` says: when forced to reform, weight
  the *next* generation of hypotheses by how much work the *previous*
  generation did. High-effort dead-ends are informative; low-effort
  glance-offs are not. This is a directly usable proposal distribution
  for hypothesis search.
- ARC allows two predictions per test input. CRR provides the natural
  pair: the highest-coherence regime that *fits the demos* (top-1) and
  the post-rupture survivor produced by `R[·]` from the next-best class
  (top-2). These are two structurally different bets, not two near-copies.

---

## 3. The CRR-ARC algorithm

Inputs: a task `T = (demos = [(in_i, out_i)], tests = [in_j])`.
Outputs: for each test input, two predicted output grids.

```
procedure SOLVE(T):
    # The solver maintains two coupled CRR processes — one for the
    # likelihood channel (Z₂, per-pixel match) and one for the prior
    # channel (SO(2), rule consistency across demos). Their precision
    # ratio is fixed at √2 (prior > likelihood).

    pool ← initial hypothesis classes
            (geometric, recolour, object-move, symmetry-complete,
             tiling, gravity, count, fill, …)

    leaders ← empty                # (regime, score) records that survived
    for h in pool:
        run CRR_REGIME(h, demos)   # see below — fills C_h, ε_h, ruptured?
        if h fits all demos exactly:
            leaders.add((h, B(C_h)))   # B is the criticality / beauty score

    if leaders is non-empty:
        h₁ ← argmax_{h ∈ leaders} B(C_h)
        h₂ ← REGENERATE(pool, ruptured)   # memory-weighted second bet
    else:
        # No clean fit — use the two best partial regimes
        h₁, h₂ ← top two by combined Z₂/SO(2) precision

    for each test input x:
        emit (h₁(x), h₂(x))


procedure CRR_REGIME(h, demos):
    C, phase ← 0, COHERENCE
    Ω ← Ω_Z₂ if h is "binary/discrete" else Ω_SO₂   # symmetry class of h
    while phase == COHERENCE:
        params ← refine(h.params, demos)            # one search step
        ε_pix  ← mean per-pixel mismatch on demos   # Z₂ residual
        ε_rule ← inconsistency across demos         # SO(2) residual
        ε      ← combine(ε_pix, ε_rule, ratio = √2) # √2 in favour of rule
        L      ← Ω · ε² · κ
        C      ← C + L
        if ε == 0 over all demos:
            return (h, C, fitted = True)
        if C · Ω ≥ 1:
            phase ← RUPTURE
            return (h, C, fitted = False, ruptured = True)


procedure REGENERATE(pool, ruptured):
    # The regeneration integral R[χ] = ∫ φ(τ) exp(C(τ)/Ω) Θ(t-τ) dτ
    # becomes a weighted sample over the ruptured regimes:
    weights[h] ← exp(C_h / Ω_h)         for h in ruptured
    parent ← sample from ruptured ~ weights
    child  ← compose(parent, neighbour-class)   # e.g. "recolour ∘ flip"
    run CRR_REGIME(child, demos)
    return child
```

### Why each piece is in the algorithm

- **`L = Ω · ε² · κ`** — quadratic in error. Two doublings of error
  quadruple the work. Bad regimes terminate quickly; near-misses linger
  long enough to be parameter-refined.
- **Symmetry-typed Ω** — discrete/binary primitives (e.g. "is the output
  the input flipped?") sit on a Bernoulli manifold and use `Ω_Z₂ = 1/π`,
  giving them a budget of `C* = π ≈ 3.14` work units. Continuous
  primitives ("rotate by some angle / colour-permute over a 10-cycle")
  use `Ω_SO₂ = 1/(2π)`, giving `C* = 2π ≈ 6.28`. The framework
  prescribes exactly twice the budget for continuous search — which
  matches how much harder it is to settle a continuous parameter than a
  discrete one. This is not a tunable; it is the topology of the search.
- **Rupture at `C·Ω = 1`** — non-arbitrary stopping rule per regime.
  Without this, search either thrashes (no time-out) or uses an
  ad-hoc time-out that has to be tuned per task class. CRR's time-out is
  set by Čencov.
- **Beauty `B(C) = exp(C/Ω) · (C* − C)`** — used to score candidates that
  *do* fit. It rewards regimes that have done substantial work (the
  exponential `exp(C/Ω)` term) but have not pushed all the way to
  rupture (the `(C* − C)` term). A regime that fits the demos at the
  first guess (`C ≈ 0`) is suspicious; a regime that fits only after
  exhausting its capacity (`C ≈ C*`) is brittle. Beauty peaks at
  `C* − Ω`: one capacity-unit before saturation. That is the "edge of
  criticality" the framework predicts and it is exactly the right
  preference for hypothesis selection — *committed but not cornered*.
- **`exp(C/Ω)` regeneration weights** — when no regime fits, the next
  generation of hypotheses should be biased toward the descendants of
  the regimes that worked hardest, not the ones that gave up first.
  This is exactly what the regeneration kernel does and it gives the
  search a memory across rupture events, replacing random-restart
  enumeration with a principled posterior over hypothesis classes.
- **`π_prior / π_likelihood = √2`** — when combining the per-pixel match
  residual (Z₂) with the cross-demo consistency residual (SO(2)),
  weight rule-consistency by `√2` more than per-pixel agreement. This
  is a soft regularizer against overfitting the easiest demo pair.
- **Two predictions = two CRR phases** — ARC's two-attempt rule is a
  perfect fit. Top-1 is the pre-rupture leader; top-2 is the
  post-rupture survivor produced by regeneration. They are guaranteed
  to come from structurally different hypothesis classes (regeneration
  always crosses a rupture boundary), giving a real second bet rather
  than an `argmax` plus its near-twin.

---

## 4. Concrete operating defaults

These constants are taken from `index.html` directly (no tuning):

```
Ω_Z₂     = 1/π        ≈ 0.31831      # binary / discrete hypothesis classes
Ω_SO₂    = 1/(2π)     ≈ 0.15915      # continuous / parametric classes
C*_Z₂    = π          ≈ 3.14159      # Z₂ rupture threshold
C*_SO₂   = 2π         ≈ 6.28319      # SO(2) rupture threshold
κ        = 0.20                       # adaptive-work scaling (index.html line 3456)
π_p/π_s  = √2         ≈ 1.41421      # prior/likelihood weight ratio
B-peak   = C* − Ω                     # commit-time criterion
```

The only externally provided quantity is the error stream `ε`, defined
per regime as the combined residual

```
ε  =  √( ε_pixel²  +  2 · ε_rule² ) / √3        # √2-weighted RMS, normalised
```

(the factor 2 in the second term is `(√2)² = 2`, the precision ratio
squared; the divisor `√3` re-normalises so `ε ∈ [0, 1]`).

---

## 5. Compute-budget mapping

The Kaggle envelope is **4× L4 GPUs, 12 h, 240 tasks ≈ 3 min/task**. The
CRR budget divides naturally:

- A regime can use **at most `C*/L_min`** internal iterations before it
  is forced to rupture. With `L_min ≈ Ω · ε_floor² · κ` and a
  reasonable `ε_floor ≈ 0.05`, this gives ~hundreds of refinement
  iterations per regime — enough for serious parameter search, capped
  before runaway.
- The four GPUs run regimes (and per-task TTT, see §6) in parallel; the
  regeneration step produces one new regime per rupture, so total
  regimes per task is bounded by `|pool| + (ruptures so far)`. With
  ~10 base classes and ~5 expected ruptures, the typical task explores
  ~15 regimes in &lt;3 min on a single L4.
- Tasks that are solved by a low-Ω regime (a discrete fit) finish early
  and donate their unused budget to harder tasks via a global scheduler
  — this is just the same `exp(C/Ω)` weighting applied at the *task*
  level: tasks that did high-coherence work earn more time on later
  attempts.

## 6. Composing CRR with the dominant Kaggle approaches

CRR is a search-control law, not a hypothesis generator. The 2025
Kaggle leaders (NVARC at 24%, ARChitects 2025 at 16.5%) are dominated
by **test-time training (TTT)** with heavy D4 + colour-permutation
augmentation on a small base LM (Qwen-4B class). Off-Kaggle, the strong
methods are **LLM-guided program synthesis** (Greenblatt's k=2,048
Python-program search, SOAR's evolutionary fine-tuning loop) and
recursive tiny networks (TRM, 7M params). CRR composes with all three:

- **CRR + TTT**: the TTT inner loop becomes the per-regime parameter
  refinement. The rupture condition `C·Ω = 1` decides when the LM has
  stopped improving on this task and the budget should be reallocated
  to a different augmentation regime, a different base prompt, or a
  symbolic fallback. This is exactly the kind of stop-and-switch
  decision that current TTT pipelines tune by hand.
- **CRR + program synthesis**: each candidate program is an SO(2)
  regime (continuous parameter search inside it) or a Z₂ regime
  (discrete commit/reject). The `exp(C/Ω)` regeneration kernel becomes
  a principled posterior over which programs to mutate next — a direct
  drop-in for the random-restart step in evolutionary synthesis.
- **CRR + tiny recursive networks (TRM-style)**: the recursive
  refinement is a single SO(2) regime; rupture says "you've stopped
  converging — try a different latent initialisation" rather than
  using a hand-set step count.

The framework's unique deliverables across all three are: (a) a
non-arbitrary stop rule (`C·Ω = 1`); (b) a non-arbitrary commit rule
(`B(C)` peaks at `C* − Ω`); (c) two structurally distinct answers from
the same search (pre-rupture leader + post-rupture survivor) — exactly
matching ARC's two-attempt allowance.

---

## 7. What this does *not* claim

- CRR does not supply a DSL. The hypothesis-class pool — geometric
  primitives, object detection, recolouring, tiling, counting,
  containment, gravity, etc. — has to be built in the usual ARC way.
  What CRR supplies is the *search dynamics* over that pool: when to
  stop, when to switch, how to weight, how to choose two answers.
- CRR does not replace test-time training or LLM-guided synthesis. It
  composes with both: a TTT loop or an LLM proposal step is just
  another way to refine `params` inside a regime, and the rupture
  condition decides when to stop calling it.
- The framework's predictions about `Ω = 1/π` vs `1/(2π)` are
  empirically motivated for physical / biological systems with named
  symmetries. For ARC, the assignment of a hypothesis class to a
  symmetry class is a modelling choice. The defensible default is:
  discrete-output classes → Z₂; classes with a continuous parameter
  (angle, scale, colour-permutation cycle) → SO(2). This matches the
  framework's own examples (heartbeat / breath = Z₂; circadian / gait =
  SO(2)).

---

## 8. Reference implementation

A runnable scaffold is in `crr_arc_solver.py`. It implements:

- the CRR phase machine per regime (coherence → rupture → regeneration),
- the `L = Ω·ε²·κ` work rule and `C·Ω = 1` rupture test,
- the beauty function `B(C)` for ranking fitted regimes,
- the `exp(C/Ω)`-weighted regeneration step for the second-best bet,
- the √2-weighted Z₂/SO(2) residual,
- a small starter pool of hypothesis classes (identity, flips, rotations,
  transposition, recolour, constant-output) sufficient to demonstrate the
  algorithm on real ARC-AGI tasks.

It is a scaffold, not a competitive solver: the value is in the search
dynamics, not in the size of the DSL. Adding more hypothesis classes is
the obvious next step and slots in without changes to the CRR loop.
