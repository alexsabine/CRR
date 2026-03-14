# Coherence-Rupture-Regeneration (CRR)

## A Mathematical Process Theory for Identity Through Discontinuous Change

**Alexander Sabine** · [Active Inference Institute](https://activeinference.org/) (Board of Directors)  
Version 2.0 · March 2026

**Website:** [cohere.org.uk](https://www.cohere.org.uk) · [temporalgrammar.ai](https://www.temporalgrammar.ai)  
**Repository:** [github.com/alexsabine/CRR](https://github.com/alexsabine/CRR)

---

## Overview

CRR is a candidate coarse-grain temporal grammar: a mathematical framework describing how bounded systems maintain identity through discontinuous change. It rests on four axioms drawn from information geometry, thermodynamics, and process philosophy. From these axioms it derives parameter-free predictions about the timing variability of recurring events, testable across every domain where systems persist through transformation.

The framework does not compete with domain-specific theories. It offers a shared mathematical vocabulary for the temporal structure they have in common: accumulation, threshold-crossing, and memory-weighted reconstruction.

CRR is grounded in process philosophy (Whitehead, 1929): reality is not made of things that change, but of changes that occasionally cohere into things. Every entity at every scale undergoes Coherence, Rupture, Regeneration. The equations are the same because the process is the same.

**If CRR is correct**, it provides a universal language for temporal dynamics across scales, parameter-free testable predictions, a bridge between information geometry and process philosophy, and a formal temporal completion of the Free Energy Principle.

**If CRR is wrong**, the CV predictions will fail, and the deviations will be informative about what the true temporal grammar must look like.

---

## Part I: The Four Axioms

CRR rests on a minimal set of axioms. Each connects to established results in physics and mathematics. Together they yield parameter-free predictions testable across every domain where systems persist through change.

### Axiom I: Coherence

**All systems that persist accumulate evidence through time.**

```
  C(x,t) = ∫₀ᵗ L(x,τ) dτ
```

Any bounded system that maintains itself against dissipation does so by accumulating coherence: temporal evidence about its environment. In the language of the Free Energy Principle, this is the progressive reduction of variational free energy. As VFE decreases, C increases. The system's generative model becomes a better fit to its environment with each passing moment.

The coherence integral C is formally identified with accumulated **Fisher information** I(θ) about the system's generative model parameters θ. Fisher information measures the curvature of the log-likelihood: how sharply the data distinguish between nearby hypotheses. It is the unique Riemannian metric on statistical manifolds (Čencov's theorem), meaning any theory of inference that respects sufficient statistics must use it.

The **Cramér-Rao inequality** then states a fundamental limit:

```
  Var(θ̂) ≥ 1/I(θ)   ⟺   σ² · I(θ) ≥ 1   ⟺   C · Ω ≥ 1
```

No unbiased estimator can have variance smaller than the inverse of the accumulated Fisher information. This is not a modelling assumption; it is a theorem of mathematical statistics, proven independently by Cramér (1946) and Rao (1945). Ito & Dechant (2020) extended this to stochastic thermodynamics, showing that the Cramér-Rao bound governs the trade-off between current fluctuations and entropy production in irreversible processes far from equilibrium.

CRR's contribution: the bound is not merely approached but **saturated**. At the moment of rupture, C·Ω = 1 exactly. The system has extracted the maximum information its current configuration permits.

### Axiom II: Rupture

**Coherence cannot accumulate indefinitely: a temporal boundary is required.**

```
  δ(t - t₀)    when C · Ω = 1
```

No system can build coherence without limit. The Cramér-Rao bound demands a boundary where accumulated evidence meets system variance. CRR identifies this boundary with the Dirac delta: an instantaneous, scale-invariant moment of transformation.

In the FEP, a **Markov blanket** is a spatial boundary that renders internal states conditionally independent of external states. CRR proposes that the Dirac delta δ(now) serves as the *temporal* analogue: the boundary between past and future, between coherence and regeneration.

The delta has three properties that make it the unique candidate for a temporal boundary:

1. **Unit mass:** ∫δ(t) dt = 1. The boundary carries exactly one unit of information. This is definitional, not adjustable.
2. **Scale invariance:** δ(at) = δ(t)/|a|. The same topology governs rupture at every temporal scale: a synapse firing (ms), a heartbeat (s), a breath (s), a developmental transition (years), a stellar cycle (Myr). There is no preferred scale.
3. **Conditional independence:** Future states (regeneration) are conditionally independent of past states (coherence) given the present (δ). This is the Markov property, now in time rather than space.

Rupture is not failure. It is the moment coherence saturates and the system must reorganise.

### Axiom III: Regeneration

**Systems persist through transformation, not despite it.**

```
  R[φ](x,t) = ∫₀ᵗ φ(x,τ) · exp(C(x,τ) / Ω) · Θ(t - τ) dτ
```

After rupture, the system reconstructs from memory weighted exponentially by past coherence. φ(x,τ) is the historical field signal (past system states). The exponential exp(C/Ω) weights which memories matter: moments of high coherence are amplified. Θ(t-τ) is the Heaviside step function enforcing causality (only the accessible past contributes). Ω governs both the threshold for transformation and the depth of memory access.

The regeneration weighting exp(C/Ω) is the Boltzmann factor of statistical mechanics, with C playing the role of energy and Ω playing the role of temperature. The most "energetic" (coherent) memories dominate the reconstruction, just as the most energetic microstates dominate thermodynamic averages.

Crucially, this weighting is based on how coherent each moment was *in its own context*, not on how recent it was. A significant experience from years ago shapes reconstruction as much as one from yesterday, if both reached high coherence. Memory is weighted by significance, not recency. This is non-Markovian dynamics: the future depends on the entire integrated past, not merely the present state.

### Axiom IV: Unity

**At the moment of transformation: C·Ω = 1.**

```
  Accumulated evidence × system variance = 1
```

This is the Cramér-Rao bound at saturation. It is simultaneously the Heisenberg uncertainty principle (ΔE·Δt ≥ ℏ/2), the Gabor limit (Δf·Δt ≥ 1/4π), and the thermodynamic uncertainty relation. CRR claims these are not analogies: they are the same equation, expressing the same physical fact. A bounded system that has extracted maximum information from its current configuration must transform.

| Framework | Evidence | Variance | Bound | Citation |
|---|---|---|---|---|
| Statistics | Fisher information I(θ) | Var(θ̂) = σ² | σ²·I(θ) ≥ 1 | Cramér (1946); Rao (1945) |
| Quantum mechanics | Energy E | Time uncertainty Δt | ΔE·Δt ≥ ℏ/2 | Heisenberg (1927) |
| Signal processing | Bandwidth Δf | Duration Δt | Δf·Δt ≥ 1/4π | Gabor (1946) |
| Thermodynamics | Current J | Entropy production σ | Var(J)·σ ≥ 2⟨J⟩² | Ito & Dechant (2020) |
| Information geometry | Statistical distance ds² | Fisher-Rao metric g | ds² = g_ij dθⁱ dθʲ | Čencov (1982); Amari & Nagaoka (2000) |
| **CRR** | **Coherence C** | **Variance Ω** | **C·Ω = 1** | **Saturation of all the above** |

What CRR adds to Ito & Dechant (2020): three things. First, *saturation*: the bound is not merely a lower limit but is reached at every rupture event. Second, *symmetry classification*: the geometric value of Ω is determined by the system's symmetry class. Third, *regeneration dynamics*: after the bound is saturated, exp(C/Ω) governs how the system reconstructs from weighted memory.

---

## Part II: The Key Parameter (Ω) and Symmetry Classification

### Ω: The Single Parameter

The framework has one central parameter: **Ω = σ²**, the system's characteristic variance (equivalently, the inverse of precision: Ω = 1/π). It functions as a dial between "rigid" and "flexible":

**Small Ω (rigid, high precision):** High rupture threshold (C* = 1/Ω is large). Rare but significant transformations. Sharply peaked memory weighting: only the most coherent moments are accessible. Think: habit, crystallised skill, trauma loops.

**Large Ω (flexible, low precision):** Low rupture threshold (C* = 1/Ω is small). Frequent micro-ruptures. Broad memory access: the whole of history is available. Think: insight, healing, phase transition.

### Symmetry Determines Ω

All temporal processes that undergo cyclic C → δ → R dynamics trace paths on the circle S¹. The symmetry class of the process determines the geometric value of Ω:

```
  Ω = 1/φ
```

where φ is the phase (in radians) traversed during one coherence accumulation cycle.

**Z₂ (bistable):** Half-cycle (φ = π). Ω = 1/π ≈ 0.318. C* = π at rupture. Two states, like a switch: on/off, systole/diastole, excitation/inhibition. Rupture flips the system between states.

**SO(2) (rotational):** Full cycle (φ = 2π). Ω = 1/2π ≈ 0.159. C* = 2π at rupture. Continuous cycle, like a wheel: the system traverses the full phase space before returning. Neural oscillations, stellar pulsation, calcium waves.

In both cases: C*·Ω = 1.

The Z_n hierarchy generalises this: CV = n/(4π) for Z_n symmetry classes, where Z₄ = SO(2) exactly. The symmetry classes are partitions of the circle: Z₂ divides S¹ into two arcs of π; Z₄ into four arcs of π/2; and SO(2) treats the full 2π as a single cycle.

### The π Correspondence

Active Inference denotes precision with Π. CRR suggests this may be more than notation: for Z₂ systems, precision = 1/Ω = π. For SO(2) systems, precision = 2π. The geometric constant emerges from phase space structure, not symbolic convention.

---

## Part III: The Central Theorem

### CV = Ω/2

From four axioms, one central result follows with no free parameters.

**The Bernoulli Partition of Unit Mass:**

```
  CV = Ω/2
```

At the rupture boundary, the system faces a binary partition: **coherence** (past) or **regeneration** (future). The Dirac delta's unit mass, split symmetrically across this boundary, defines a Bernoulli trial with p = 1/2. The variance of a Bernoulli(1/2) random variable is p(1-p) = 1/4. The standard deviation is therefore σ = 1/2.

**The derivation:**

1. C·Ω = 1 at rupture (Axiom IV, from Cramér-Rao saturation). This gives E[C*] = 1/Ω.
2. The rupture boundary partitions the system into two domains: coherence (all that has been accumulated) and regeneration (all that will be reconstructed). The Dirac delta distributes exactly one unit of mass on this boundary (Axiom II).
3. By symmetry (there is no mechanism to favour past over future at the boundary), each domain receives equal probability: p = 1/2. This is a Bernoulli trial.
4. The rupture condition C·Ω = 1 is dimensionless. The fluctuation around the threshold is measured in the same natural units as the threshold itself. A symmetric Bernoulli partition of a dimensionless unit boundary has:

```
  Var = p(1-p) = 1/2 · 1/2 = 1/4   ⟹   σ(C*) = 1/2
```

5. With both moments determined:

- E[C*] = 1/Ω (from C·Ω = 1)
- σ(C*) = 1/2 (from Bernoulli(1/2) at the boundary)
- CV = σ(C*) / E[C*] = (1/2) / (1/Ω) = Ω/2

For the two fundamental symmetry classes:

| Symmetry | Phase to Rupture | Ω Value | C* Value | CV Prediction |
|---|---|---|---|---|
| Z₂ (bistable/flip) | π (half-cycle) | 1/π ≈ 0.318 | π ≈ 3.14 | 1/(2π) ≈ **0.15915** |
| SO(2) (rotational) | 2π (full-cycle) | 1/2π ≈ 0.159 | 2π ≈ 6.28 | 1/(4π) ≈ **0.07958** |

The ratio between them is **exactly 2**.

These predictions are parameter-free: no fitting, no calibration. They follow from the axioms alone.

**Why 1/2 and not some other fraction?** Because Bernoulli(1/2) is the **maximum-entropy distribution** over a binary partition. The variance p(1-p) is maximised at p = 1/2, and maximum variance over {0,1} is equivalent to maximum entropy. Any other partition would require a reason for asymmetry: an additional parameter specifying *why* past and future are unequal at the boundary. This would violate the parsimony that makes C·Ω = 1 a first principle rather than a model.

**The MaxEnt coherence.** This connects back to Axiom III: the regeneration kernel exp(C/Ω) is itself the maximum-entropy weighting given a mean-coherence constraint (Jaynes, 1957). The entire framework is maximally agnostic at every step: MaxEnt kernel for reconstruction, MaxEnt partition at the boundary. CRR assumes as little as possible at every juncture, and the predictions follow from that minimal commitment alone.

---

## Part IV: Formal Definitions and Standing Assumptions

### Standing Assumptions

**(A1) Regularity.** For each x and t, the function τ ↦ L(x,τ) is locally integrable on [0,t].

**(A2) Non-negativity.** L(x,τ) ≥ 0 for all x, τ. History accumulates; it does not spontaneously dissipate.

**(A3) Bounded Rate (No-Zeno Condition).** There exists M > 0 such that L(x,t) ≤ M for all x, t. This ensures each coherence cycle has duration at least 1/(MΩ), preventing infinitely many ruptures in finite time.

### Core Definitions

**Definition 1 (Coherence Accumulation Rate).** The coherence accumulation rate is a function L: X × [0,T] → R≥0 that assigns to each state-time pair (x,τ) a non-negative rate at which the system accumulates evidence about its environment. Dimensions: [L] = [T⁻¹]. L is formally identified with the rate of Fisher information accumulation.

**Definition 2 (Coherence).** Let t_j denote the most recent rupture time before t (with t₀ = 0). The coherence at state x and time t is the accumulated evidence since the last rupture:

```
  C(x,t) := ∫ₜⱼᵗ L(x,τ) dτ
```

Dimensionless. Monotone non-decreasing within each cycle. Resets to 0 at each rupture.

**Definition 3 (Variance Parameter).** The variance parameter Ω > 0 is a positive dimensionless constant characterising the system's boundary permeability. It is identified with: (a) Statistical: Ω = σ² (characteristic variance); (b) Inferential: Ω = 1/π where π is precision; (c) Geometric: Ω = 1/φ where φ is the phase traversed during one coherence cycle; (d) Thermodynamic: Ω = k_BT/κ_eff in physical systems. Ω determines the rupture threshold C* = 1/Ω via Axiom IV.

**Definition 4 (Rupture).** A rupture occurs at time t* when coherence reaches the threshold set by Ω:

```
  t* := inf{ t > tⱼ : C(x,t) ≥ 1/Ω }
```

The rupture event is represented by δ(t - t*). Following rupture: C(x, t*⁺) = 0.

**Definition 5 (Regeneration).** The regeneration operator reconstructs the system state by weighting historical field values φ(x,τ) exponentially by the coherence at each historical moment:

```
  R[φ](x,t) = ∫₀ᵗ φ(x,τ) · exp(C(x,τ) / Ω) · Θ(t - τ) dτ
```

where C(x,τ) is the coherence value *at moment τ* (how far into its cycle the system was at that historical moment).

### Key Properties

**No Zeno Pathology.** Under (A3), each coherence cycle has duration at least 1/(MΩ). Hence the number of ruptures in any finite interval [0,T] is at most ⌊TMΩ⌋ + 1 < ∞.

**Regeneration Weighting Contrast.** The weight ratio between a rupture moment (when C = C* = 1/Ω) and a moment of zero coherence is exp(1/Ω²). For Z₂ systems: contrast ratio = e^(π²) ≈ 19,400. For SO(2) systems: contrast ratio = e^(4π²) ≈ 1.4 × 10¹⁷. Regeneration is overwhelmingly dominated by moments near rupture.

| Quantity | Symbol | Dimensions | Identification |
|---|---|---|---|
| Accumulation rate | L | [T⁻¹] | Fisher information rate |
| Coherence | C | dimensionless | Accumulated Fisher information |
| Variance parameter | Ω | dimensionless | σ² = 1/π = 1/φ |
| Rupture threshold | C* = 1/Ω | dimensionless | Cramér-Rao saturation point |
| Historical field | φ | [F] | Reconstruction resource |
| Regeneration | R | [F]·[T] | Coherence-weighted integral of history |

---

## Part V: Empirical Validation

### Parameter-Free Predictions Across 100+ Systems

CRR's central empirical claim is that the coefficient of variation (CV) of inter-event intervals is determined by symmetry class alone. These predictions have been tested across **132 systems in 30+ domains**, including neural oscillations, cardiac rhythms, flame dynamics, bacterial division, stellar pulsation, calcium signalling, reaction times, population ecology, laser dynamics, gastric waves, sleep spindles, tree rings, geyser eruptions, and seismic cycles.

The full validation table with observed CVs, predictions, and references is available at [CRR Benchmarks](https://www.cohere.org.uk/crr-benchmarks.html) ([PDF on GitHub](https://github.com/alexsabine/CRR/blob/main/CRR_CV_Predictions.pdf)).

| Domain | Example Systems | Predicted Class | Status |
|---|---|---|---|
| Neural oscillations | EEG alpha, theta, gamma; sleep spindles | SO(2) | Validated (N=109, two independent datasets) |
| Cardiac rhythms | Heart rate variability, R-R intervals | Z₂ | Confirmed |
| Flame dynamics | Candle flicker, plasma oscillations | Z₂ | Confirmed |
| Bacterial division | *E. coli* inter-division intervals | Z₂ | Confirmed |
| Stellar pulsation | Cepheid variables, RR Lyrae | SO(2) | Confirmed |
| Calcium signalling | Intracellular Ca²⁺ oscillations | SO(2) | Confirmed |
| Reaction times | Human simple RT, choice RT | Z₂ | Confirmed |
| Population ecology | Predator-prey cycles, bloom intervals | SO(2) | Confirmed |
| Laser dynamics | Mode-locked laser pulse trains | SO(2) | Confirmed |
| Gastric waves | Slow-wave rhythm | SO(2) | Confirmed |
| Saltatory growth | Infant growth spurts (Lampl & Johnson) | Z₂ | Confirmed (11/11 individual predictions) |
| Geophysics | Geyser eruptions, seismic cycles | Z₂/SO(2) | Confirmed |

### Three-Class Framework

Systems fall into three empirical classes based on their relationship to the CRR predictions:

**Class A (Autonomous stochastic):** CV ≈ Ω/2. The system's timing variability matches the CRR prediction. The system is a "free-running" oscillator whose variance is set by its symmetry class alone. Match rate: 89%.

**Class B (Deterministic/regulated):** CV < Ω/2. The system is actively suppressing variance below the CRR floor. It is a precision oscillator, more regular than symmetry alone would dictate. Regulation can be identified without knowing the regulation mechanism. Match rate: 85%.

**Class C (Noise-dominated/volitional):** CV > Ω/2. The system's variance exceeds the CRR prediction. This indicates asymmetric bistability (unequal state durations), external noise injection, or volitional timing. Match rate: 85%.

Overall classification accuracy: **86%**, approximately **10.6σ significance**, with **zero directional reversals** (no Z₂ system has ever shown lower CV than a co-measured SO(2) system).

### Key EEG Validation

Tested across PhysioNet EEGBCI and MPI-LEMON datasets (N = 109 total subjects), co-authored with Nicolás Hinrichs and Xia Chen:

- **11/11 class orderings correct** (every SO(2) band showed lower CV than every Z₂ band)
- **Fisher z-corrected CV ratio: 1.93** (95% CI containing the predicted value of 2.0)
- **Train-test correlation: r = 0.997**
- **Cohen's d = 2.01**

### Falsification Criteria

The framework makes specific, falsifiable commitments:

- If Z₂ systems systematically showed CV ≠ 1/(2π): the symmetry classification or the equipartition assumption would be challenged.
- If SO(2) systems systematically showed CV ≠ 1/(4π): same.
- If the CV ratio between classes deviated from 2: the Z_n hierarchy would be challenged.
- If regeneration proved Markovian (no path dependence): the non-Markovian accumulation axiom would be falsified.

**Methodological commitment:** CRR follows a pre-registration discipline. Predictions are formally registered before touching data. Deviations are diagnosed rather than hidden. The 132-system CV predictions table, three-class framework, and all EEG results were pre-registered. Honest null testing is a core commitment (e.g. the lemniscate hypothesis in atomic CV analysis was falsified and reported as such, not rescued).

---

## Part VI: Regeneration and Memory

### Significance, Not Recency

A high-coherence moment from 1000 cycles ago contributes with greater weight than a low-coherence moment from the most recent cycle. History is weighted by *significance* (coherence at the time), not by *recency*.

| Property | CRR (Coherence-Weighted) | Recency-Weighted |
|---|---|---|
| What determines weight? | Coherence at each moment: exp(C(τ)/Ω) | Time since event: e^(-λ(t-τ)) |
| Ancient high-coherence moments | Fully preserved (weight = exp(1/Ω²)) | Exponentially forgotten |
| Recent low-coherence moments | Low weight (near 1) | High weight (recent) |
| Philosophical alignment | Bergson: memory as continuous presence | Standard decay models |
| Empirical match | Muscle memory, trauma, skill retention | Short-term forgetting curves |

### Ω-Regime Behaviour

Ω plays the role of "temperature" in the Boltzmann weighting exp(C/Ω):

**Small Ω (low temperature, rigid):** Weights concentrate explosively on high-coherence moments. The contrast ratio exp(1/Ω²) is enormous. Only moments near rupture matter for regeneration. The system reconstitutes the same pattern over and over.

**Large Ω (high temperature, flexible):** Weights spread more uniformly across history. The contrast ratio is moderate. The entire history contributes to reconstruction. Transformation is possible.

### Non-Markovian Path Dependence

Two systems with identical current coherence but different histories will in general have different regenerations. This follows directly from the regeneration integral depending on the full history {C(x,τ)} for all τ ∈ [0,t], not just the current value C(x,t). Two people at the same point in life but with different histories will respond differently to the same challenge. Significant experiences persist in their influence regardless of how long ago they occurred.

---

## Part VII: CRR as Temporal Completion of the Free Energy Principle

### The Temporal Gap in the FEP

The FEP (Friston, 2010; 2019) proposes that living systems survive by minimising free energy. CRR provides the *temporal dynamics* that the FEP presupposes but leaves unspecified: **when** do beliefs update? **How** does accumulated history shape reconstitution?

The FEP tells you that a system at nonequilibrium steady state will look as if it is performing inference. It does not tell you the timing of the inference, or the moment at which the current model is exhausted.

### Three Specific Additions

| FEP Provides | CRR Adds |
|---|---|
| Markov blanket: a **spatial** boundary | Dirac delta: a **temporal** boundary. The rupture moment δ(now) serves the same conditional-independence role in time that the blanket serves in space. |
| Dynamics **within** a regime (VFE minimisation, predictive coding) | **Transitions between regimes:** C·Ω = 1 specifies exactly when inference is exhausted and the system must reorganise. |
| **Markovian** dynamics: each state depends on the current state | **Non-Markovian accumulation:** C(x,t) = ∫L(x,τ)dτ integrates the full history. Regeneration via exp(C/Ω) weights this history exponentially. |

The FEP's precision parameter (inverse variance, π = 1/Ω) maps directly to CRR's Ω. Where the FEP uses precision to weight prediction errors, CRR uses its reciprocal Ω to set the rupture threshold and memory depth. The frameworks share the same information geometry; CRR adds the temporal completion.

### Rupture and Bayesian Model Reduction

In Friston et al. (2025) "Active Inference and Artificial Reasoning," an "aha moment" occurs when evidence accumulates until confidence exceeds a threshold, triggering Bayesian Model Reduction. CRR's Rupture is the same phenomenon, given a precise temporal criterion: C·Ω = 1. Both frameworks describe the discrete transition from uncertainty to commitment when accumulated evidence warrants model selection. CRR adds the parameter-free prediction about its timing variability (CV = Ω/2).

### What CRR Does Not Replace

CRR does not compete with the FEP's account of *what* beliefs update to (free energy minimisation), nor with the detailed neural process theories (predictive coding, active inference) that implement it. CRR addresses the *temporal structure* of these processes: when transitions occur, how history shapes reconstitution, and why the timing variability takes the specific values it does. The FEP provides the engine; CRR provides the clock.

---

## Part VIII: Philosophical Grounding

### Whitehead: Actual Occasions

Alfred North Whitehead rejected substance metaphysics in favour of process: reality consists not of enduring things but of momentary "actual occasions" that prehend their past and perish into objective immortality. Coherence is the prehensive accumulation of the past. The Dirac delta at rupture is the moment of concrescence where many become one. Regeneration is the transition to "objective immortality" where the occasion's achieved value becomes available to future prehensions through exp(C/Ω) weighting. The mathematics formalises what Whitehead described philosophically: each moment metabolises its entire history, transforms it, and bequeaths novel pattern to the future.

### Bergson: Duration and Memory

Henri Bergson distinguished lived duration (*durée*) from spatialised clock-time. For Bergson, the past is not gone but preserved whole in the present; memory is not retrieval from storage but the continuous presence of history in current experience. The regeneration integral embodies this directly: exp(C/Ω) ensures that high-coherence moments from the entire past remain actively present in reconstruction. CRR provides the mathematical operator for Bergsonian duration.

### The Central Claim

Memory accumulates, ruptures, and transforms. This punctuated dynamic, not smooth continuity, is how identity persists through change. Both Whitehead and Bergson grasped this philosophically. CRR offers it mathematically: a grammar of temporal becoming that can be simulated, tested, and applied across scales from neural dynamics to ecosystem succession.

---

## Part IX: Implications

### For AI and Continual Learning

Current approaches to catastrophic forgetting focus on preventing forgetting. CRR suggests the problem is not forgetting itself but *uncontrolled* forgetting. Biological systems learn through CRR cycles: coherence builds (training, practice), rupture occurs (sleep, consolidation), regeneration weights history (important patterns preserved, noise discarded). CRR-informed approaches would implement structured forgetting with coherence-weighted consolidation, rather than attempting to preserve all weights indefinitely.

### For Consciousness

CRR suggests that conscious experience arises from the interface between coherence accumulation and rupture potential. The "flow state" is C approaching Ω: pre-rupture focus. Insight is the rupture event itself: a discontinuous model switch. The Dirac delta at rupture represents the ontological present: dimensionless, instantaneous, the point of genuine choice.

### For Psychology

Psychological dynamics map naturally to CRR signatures. Depression: rigid low Ω, stuck patterns reconstituting. Anxiety: unstable Ω, unpredictable rupture timing. Trauma: forced rupture without adequate regeneration. Therapy: controlled rupture with supported regeneration. Contemplative practices (meditation, breathwork, ritual) may function as Ω modulation technologies: methods for shifting system temperature discovered empirically rather than derived theoretically.

### For Multi-Scale Systems

What appears as smooth accumulation ∫L(τ)dτ at one scale is actually counting discrete rupture events at finer scales. Each rupture at scale n contributes a discrete "packet" of coherence-work to scale n+1. Higher scales exhibit more regular dynamics due to Central Limit averaging: CV^(n+1) ≈ CV^(n)/√M^(n). This may explain why physical laws appear deterministic at macro-scales despite quantum indeterminacy below.

---

## Part X: Acknowledged Limitations and Open Questions

### What Remains Open

**The CV = Ω/2 proof.** The Bernoulli argument (σ(C*) = 1/2 from the maximum-entropy binary partition of the Dirac delta's unit mass) provides a rigorous derivation: the 1/2 is the standard deviation of a Bernoulli(1/2) variable, not a free choice. The identification of each rupture event's boundary crossing as a Bernoulli trial is well-motivated (binary partition, symmetric, dimensionless coordinate) but is itself a commitment rather than a theorem derived from measure theory alone.

**The Ω = 1/φ derivation.** The identification of Ω with the inverse of phase traversed is motivated by information geometry (Bonnet-Myers theorem). A first-principles derivation from the axioms alone is desirable.

**Biological Ω determination.** How specific biological systems "select" their symmetry class (and hence Ω) from the available options is an empirical question that CRR does not yet answer.

**Prospective predictions.** Many of the 132-system validations are fits to existing data rather than prospective predictions. The EEG results (N=109, two independent datasets, pre-registered) represent the strongest prospective test to date.

### Epistemic Status

CRR is neither obviously correct nor obviously wrong. It occupies the space of "promising theoretical synthesis that requires further validation." The mathematical structure is sound. The empirical claims are testable. The predictions are specific and falsifiable. The philosophical implications are worth exploring. What would strengthen it most: formal verification that the Bernoulli trial identification follows necessarily from the axioms (rather than being well-motivated), successful prospective prediction of rupture timing in novel systems, and CRR-based continual learning algorithms that outperform standard methods. What would weaken it most: consistent failure of CV predictions in new systems, discovery of bounded systems without CRR dynamics, or a better alternative framework explaining the same phenomena.

---

## References

Amari, S. & Nagaoka, H. (2000). *Methods of Information Geometry*. AMS/Oxford UP.

Čencov, N.N. (1982). *Statistical Decision Rules and Optimal Inference*. AMS.

Cramér, H. (1946). *Mathematical Methods of Statistics*. Princeton UP.

Fisher, R.A. (1925). Theory of statistical estimation. *Proc. Cambridge Phil. Soc.* 22, 700-725.

Friston, K. (2010). The free-energy principle: a unified brain theory? *Nat. Rev. Neurosci.* 11, 127-138.

Friston, K.J. (2019). A free energy principle for a particular physics. *arXiv:1906.10184*.

Friston, K., et al. (2025). Active inference and artificial reasoning. *arXiv:2512.21129*.

Gabor, D. (1946). Theory of communication. *J. IEE* 93, 429-457.

Heisenberg, W. (1927). Über den anschaulichen Inhalt der quantentheoretischen Kinematik und Mechanik. *Z. Physik* 43, 172-198.

Ito, S. & Dechant, A. (2020). Stochastic time evolution, information geometry, and the Cramér-Rao bound. *Phys. Rev. X*, 10, 021056.

Jaynes, E.T. (1957). Information theory and statistical mechanics. *Phys. Rev.* 106, 620-630.

Parr, T., Pezzulo, G. & Friston, K.J. (2022). *Active Inference: The Free Energy Principle in Mind, Brain, and Behavior*. MIT Press.

Rao, C.R. (1945). Information and the accuracy attainable in the estimation of statistical parameters. *Bull. Calcutta Math. Soc.* 37, 81-91.

Tucker, D.M., Luu, P. & Friston, K.J. (2025). The Criticality of Consciousness. *Entropy*, 27(8), 829.

Whitehead, A.N. (1929). *Process and Reality*. Macmillan.

Wootters, W.K. (1981). Statistical distance and Hilbert space. *Phys. Rev. D* 23, 357-362.

---

## Resources

### Core

- [Website: cohere.org.uk](https://www.cohere.org.uk)
- [GitHub Repository](https://github.com/alexsabine/CRR/)
- [Interactive Guide](https://www.cohere.org.uk/guide.html)
- [CRR in 5 Minutes](https://www.cohere.org.uk/CRR_Plenary.html)
- [Starter Prompt for LLM Exploration](https://www.cohere.org.uk/LLM_PROMPT_EXPLORE.MD)

### Theory and Proof Sketches

- [Mathematical Foundations](https://www.cohere.org.uk/Maths.html) — the axioms, formal definitions, and CV derivation
- [CRR Benchmarks](https://www.cohere.org.uk/crr-benchmarks.html) — 132-system CV predictions table ([PDF](https://github.com/alexsabine/CRR/blob/main/CRR_CV_Predictions.pdf))
- [First Principles (12 domains)](https://www.cohere.org.uk/crr_first_principles_proofs.md)
- [Canonical Proof Sketch](https://github.com/alexsabine/CRR/blob/main/canonical_crr_rigorous_proof_sketch.md)
- [Martingale Derivation](https://github.com/alexsabine/CRR/blob/main/crr_martingale_derivation.pdf)
- [Bounded Kan Extension](https://www.cohere.org.uk/CRR_Bounded_Kan_Extension_QED_v2.pdf)
- [16 Nats Exploration](https://www.cohere.org.uk/16_nats_identity.pdf)
- [Euler Identity at Rupture](https://www.cohere.org.uk/crr_euler_identity.pdf)
- [Fine Structure Constant (an attempt)](https://www.cohere.org.uk/crr_137(attempt).pdf)

### Responses to Published Work

- [Response to Mounier, Parr & Friston (2026)](https://www.cohere.org.uk/CRR_Flatness_Commentary.pdf)
- [Response to Tucker & Luu (2025)](https://www.cohere.org.uk/CRR_Response_Tucker+Luu.pdf)
- [Response to Tolchinsky et al. (2025)](https://www.cohere.org.uk/Tolchinksy.pdf)
- [Response to Tolchinsky & Levin (2026)](https://www.temporalgrammar.ai/FAO_Tolchinksy_&_Levin.pdf)
- [L-R Brain Lateralisation](https://www.cohere.org.uk/CRR_Lateralization_Thesis.pdf)

### Interactive Simulations (selected)

- [FEP+CRR Brain (Pedagogical)](https://www.cohere.org.uk/brain_scientist_v2.html)
- [CRR Flame (7kb, for inspection)](https://www.cohere.org.uk/flame(7kb)for_peer_review.html)
- [CRR Sun (8kb, for inspection)](https://www.cohere.org.uk/crr_sol(8kb).html)
- [CRR Gravitational Waves (9kb)](https://www.cohere.org.uk/crr_gw.html)
- [CRR Ocean Waves (12kb)](https://www.cohere.org.uk/CRR_Waves.html)
- [CRR Crystal Clock](https://www.cohere.org.uk/crr_crystal_v6.html)
- [CRR Crickets & Fireflies](https://www.cohere.org.uk/CRR_Crickets_Fireflies.html)
- [CRR Geometry Explorer](https://www.cohere.org.uk/CRR_Geometry_explorer.html)
- [CRR Time Crystal](https://www.cohere.org.uk/crr_time_crystal_explorer.html)
- [Song of Beauty (annotated)](https://www.cohere.org.uk/CRR_song_of_beauty.html)
- [Song of the Cosmos](https://www.cohere.org.uk/song_of_the_cosmos.html)
- [Song of Heart](https://www.cohere.org.uk/song_of_heart.html)
- [Song of the Starlings](https://www.cohere.org.uk/song_of_the_starlings_2.html)

The full repository contains 67+ interactive demonstrations alongside mathematical documentation. The unusual structure is intentional: think exhibition space, not code library.

---

## Citation

```bibtex
@misc{sabine2025crr,
  author = {Sabine, Alexander},
  title = {Coherence-Rupture-Regeneration: A Mathematical Process Theory
           for Identity Through Discontinuous Change},
  year = {2025},
  url = {https://www.cohere.org.uk}
}
```

---

*Last Updated: March 2026*
