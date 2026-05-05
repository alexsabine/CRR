# B3 — Consistency reframing after AGI 2026 paper read (Session 8)

**Significant reframing.** Until Session 8, the campaign treated B3
("AGI-26 phase-gating: χ² = 8,041; conservation 1.003; ρ = −1/2")
as a claim about an *empirical neuroscience dataset* awaiting
deposition. With the AGI 2026 paper now in the repository
(`AGI_Conference_2026 (Sabine, 2026) (1).pdf`), the underlying
content is clarified: B3 is a **POMDP simulation result**, not an
empirical-data analysis.

## What the AGI 2026 paper actually contains

**Source:** Sabine, A. (2026). *Phase-Gating Across Precision
Channels: Topological Constraints on Multi-Channel Belief Update
Dynamics.* AGI 2026 conference submission.

**Setup:** Active-inference POMDP with two precision channels —
Z₂ (sensory) at threshold π and SO(2) (prior) at threshold 2π.
Dirichlet learning. Multiple agents.

**Results:**

| Statistic | Value | Status |
|-----------|-------|--------|
| Phase-gating χ² | **8,041** (df=9, n=10,345 ruptures, 60 runs × 1,200 trials) | **Discriminating CRR result** |
| Conservation ratio | **1.003** (CV 0.024) | **Structurally guaranteed** (NOT discriminating) |
| ρ tested values | 0, −0.3 (conservation OK), −0.7 (breaks) | Sensitivity analysis |

**Sabine's own honest disclosure (AGI 2026, Section 4.3):**

> "Total precision-gain equality is therefore a structural
> consequence of equal evidence delivery, not a prediction that
> discriminates CRR from alternatives."

i.e., **the conservation = 1.003 finding is not a CRR-specific
empirical signature.** It is a structural feature of any
two-channel system with equal evidence delivery.

**The phase-gating result IS discriminating** (Sabine, AGI 2026
Section 4.3):

> "The phase relationship depends on the specific threshold ratio
> and does not emerge from continuous updating or from arbitrary
> thresholds."

The χ² = 8041 quantifies the non-uniformity of Z₂ phases at SO(2)
ruptures in a system with the canonical CRR thresholds π and 2π.

## Reframing of B3's status

### What B3 IS (after Session 8 reading)

A claim that **CRR's threshold architecture (π and 2π) produces
non-trivial phase-gating dynamics in a POMDP simulation that would
not emerge from arbitrary thresholds or continuous updating.**

This is a structural-mathematical claim verified by simulation,
not an empirical-data finding.

### What B3 IS NOT

- An empirical neuroscience-dataset analysis. The "AGI-26 dataset"
  is the simulation output, not behavioural / neural recording.
- A discriminating empirical confirmation of CRR (the conservation
  ratio of 1.003 is structurally guaranteed, not a discriminating
  test).
- A demonstration of ρ = −1/2 in real perception-action data.
  The AGI paper tests ρ ∈ {0, −0.3, −0.7} as sensitivity analysis;
  ρ = −1/2 (M11's prediction) is not directly tested in this
  paper.

## Discipline-aligned tier decision

**B3 stays at T1** — with the consistency reframing now explicit.

Reasoning:
1. B3 was a T1 claim before; the AGI paper provides the underlying
   simulation derivation but doesn't change empirical status.
2. T2 promotion would require **empirical** reproduction of
   phase-gating in real neuroscience data. The AGI paper *cites*
   compatibility with Jang et al. (ACh-DA timing) but does not
   quantitatively test it.
3. The χ² = 8,041 statistic remains as the original brief stated,
   but its interpretation is now more precisely "a discriminating
   structural property of the CRR threshold architecture in a
   POMDP simulation."

## Reproduction script

The AGI 2026 paper's simulation should be reproducible. The
campaign's `crr-engine/consistency/agi26_phase_gating.py` skeleton
should be updated to:

1. Implement the two-channel POMDP with Z₂ threshold π and SO(2)
   threshold 2π.
2. Run 60 simulations × 1,200 trials.
3. Track Z₂ phase at each SO(2) rupture (~10,000 ruptures expected).
4. Compute χ² of the resulting phase distribution against uniform.
5. Verify conservation ratio in [0.99, 1.01].

Comparison values (per AGI 2026):
- χ² ≈ 8,041 ± expected statistical noise
- Conservation ratio 1.003
- Z₂ mean inter-rupture interval 3.0 trials (CV 0.26)
- SO(2) mean inter-rupture interval 10.4 trials (CV 0.50)

This is sandbox-runnable in principle. Reframed as a structural-
verification test, not a [REVIEWER-RUN] empirical-data fetch.

## Path to T2 / T3 (revised)

For B3 to reach T2 with empirical content:
1. **Independent reproduction of the simulation** by an unaffiliated
   reviewer (sandbox-runnable). Promotes B3 to T2 (structural).
2. **Empirical test in real neuroscience data:** test phase-gating
   in dopaminergic / ACh-mediated learning paradigms (Jang et al.
   tradition); requires fresh pre-registration in a future session.
   Promotes B3 to T3 if confirmed.

## Applied usefulness for 2026 and beyond (updated)

The AGI 2026 paper's primary applied claims:

- **Distributed multi-agent AGI architectures:** the phase-gating
  result implies that Markov-blanketed agent networks with Z₂/SO(2)
  pairwise coordination self-balance without central control. A
  network of 150 agents has 11,175 edges, each constituting an
  independent self-balancing two-channel system.
- **AI alignment temporal-misalignment metric:** "what matters is
  not only what a system believes, but when it reorganises its
  beliefs relative to its partner. The phase-gating results show
  that the functional character of an update depends on where in
  the partner channel's cycle it occurs, so a phase mismatch
  between human and AGI would constitute a detectable, measurable
  form of misalignment."
- **Continual learning:** weight-function independence "frees
  designers to optimise update rules without disrupting
  inter-channel coordination."
- **Hierarchical generative-model design:** Sabine notes the
  current test environment is a "toy POMDP, not an AGI system; the
  logical next step is to test phase-gating in a hierarchical
  generative model with non-stationary dynamics."

**Honest scope (per Sabine's own disclosure):**

> "The current test environment is a toy POMDP, not an AGI system;
> the restriction to one-dimensional manifolds does substantial
> work, and the 2:1 ratio's survival in higher dimensions is
> untested."

The AGI paper recommends further empirical testing rather than
declaring the result complete.
