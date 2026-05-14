# RUBRIC.md — the CRR pre-registration protocol

This is a distilled, operational form of Appendix C of Sabine (2026).
It encodes the algorithm that was applied to every system in the
132-system table *before* any empirical CV was consulted, and it is
the same algorithm `src/crr_cv_predictions/rubric.py` implements.

## The 6 steps

### Step 1 — Is the system oscillatory?

The system must exhibit repeated temporal events with a measurable
period or inter-event interval. If it does not oscillate or cycle,
CRR does not apply — exclude.

### Step 2 — Identify the state space

Ask in order; stop at the first **yes**.

| # | Question | If yes, assign | n | Notes |
|---|----------|----------------|---|-------|
| Q1 | Does the system alternate between exactly two distinguishable states? (open/closed, firing/resting, contracted/relaxed, on/off) | **Z₂** | 2 | Discrete boundary crossing between qualitatively different configurations. |
| Q2 | Does the system traverse a continuous cycle with no preferred stopping point? (rotation, continuous phase progression, limit cycle) | **SO(2)** | 4 | Phase wraps continuously 0 → 2π. SO(2) is dynamically equivalent to Z₄. |
| Q3 | Does the system have n > 2 discrete phases per cycle? (4-stroke engine, cell cycle G1/S/G2/M, segmentation clock) | **Z_n** | counted n | Less certain than Z₂/SO(2): Z_n predictions for n > 2 are extrapolations. |
| Q4 | None of the above? | **Z₂** (default) | 2 | Conservative fallback: any cycle crosses at least one boundary. |

### Step 2.5 — SO(2) regulator present in the causal chain?

(Added from Sabine 2026 *Geometric Origin of Memoryless Variability*.)

If Step 2 returned **Z₂**, you must now ask whether there is an SO(2)
regulator anywhere in the system's causal chain (cardiac electrical
cycle behind the valve, membrane potential behind the spike,
escapement wheel behind the tick, …).

| Has SO(2) regulator? | Refined symmetry | CV prediction |
|----------------------|------------------|---------------|
| **Yes** (default for any physical system) | `Z2` (= `Z2_on_SO2`) | 1/(2π) ≈ 0.1592 |
| **No** (truly memoryless: radioactive decay, Poisson minis, etc.) | `Z2_only` | **1 (exponential distribution)** |

Default is **Yes** — physical Z₂ events almost always have an SO(2)
regulator (paper Appendix A: door/hinge, switch/rocker, neuron/
membrane, heart/cardiac-cycle). Only assert **No** when memorylessness
is established as a property of the source process, not a fitting
choice. The Z₂_only assignment is the strongest possible classification
because it predicts CV = 1 *exactly* (a theorem about the exponential
distribution, not an empirical claim).

### Step 3 — Register the prediction

Compute the canonical CV under the M22 generalisation (CV = 1/(2·φ_G)):

| Symmetry | φ_G | CV_pred | Acceptance band [0.6×, 1.3×] |
|----------|-----|---------|-------------------------------|
| Z₂_only (pure memoryless) | 1/2 | **1.0** | [0.6, 1.3] |
| Z₂ (= Z₂-on-SO(2)) | π | 1/(2π) ≈ **0.1592** | [0.0955, 0.2070] |
| SO(2) | 2π | 1/(4π) ≈ **0.0796** | [0.0478, 0.1035] |
| SU(2) | 2π | 1/(4π) ≈ **0.0796** | [0.0478, 0.1035] |
| SO(3) | π | 1/(2π) ≈ **0.1592** | [0.0955, 0.2070] |
| T² (per generator) | 2π | 1/(4π) ≈ **0.0796** | [0.0478, 0.1035] |
| SU(3) | 2π√3 | 1/(4π√3) ≈ **0.0459** | [0.0276, 0.0597] |
| Z_n (paper extrapolation) | — | **1/(nπ)** | [0.6/(nπ), 1.3/(nπ)] |
| Z_n (M15 discrete-phase reading) | 2π/n | **n/(4π)** | [0.6n/(4π), 1.3n/(4π)] |

Record system, physical justification (1–2 sentences citing the
**physical structure**, not the observed CV), symmetry, n, predicted
CV. Do not consult empirical CV until this step is complete.

> **Discrepancy flag.** For n ≥ 3 the paper's extrapolation
> CV = 1/(nπ) and the discrete-phase derivation CV = n/(4π) disagree.
> The package records both and treats their gap as a falsifiable
> open question.

### Step 4 — Three-class assignment

Before looking at empirical CV, classify on physics alone:

- **Class A — autonomous stochastic.** No strong external regulation
  or noise injection. Intrinsic stochasticity dominates timing.
  CRR predicts CV = 1/(2·φ_G) within [0.6×, 1.3×].
  Examples: cardiac RR (supine), Ca²⁺ oscillations, candle flame,
  somite clock, simple reaction time.

- **Class B — deterministic / actively regulated.** Feedback control,
  entrainment, engineering precision, or evolutionary
  synchronisation crushes Ω below the thermodynamic value.
  CRR predicts CV ≪ 1/(2·φ_G) (suppressed).
  Examples: circadian free-run, quartz crystal, pulsar, sinoatrial
  node, elite swimmer strokes.

- **Class C — noise-dominated / volitional.** External stochastic
  forcing, volitional or cortical modulation, molecular noise from
  low copy numbers, or point-process (Poisson-like) statistics
  inflate effective Ω above the thermodynamic value.
  CRR predicts CV ≫ 1/(2·φ_G) (elevated).
  Examples: spontaneous blink interval, ENSO, repressilator
  (single-cell), earthquake recurrence, awake respiratory rate.

Record class and its physical justification alongside the symmetry.
Do not consult empirical CV until this step is complete.

### Step 5 — Look up empirical CV and assign verdict

Find observed CV in peer-reviewed literature. Compute
`ratio = cv_obs / cv_pred`. Assign:

- **MATCH**: 0.60 ≤ ratio ≤ 1.30. Timing variability consistent
  with the predicted symmetry class.
- **SUPPRESSED**: ratio < 0.60. System more precise than the
  prediction. Diagnostic: active regulation, feedback, engineering.
- **ELEVATED**: ratio > 1.30. System more variable than the
  prediction. Diagnostic: stochastic forcing, volitional
  modulation, asymmetric sub-cycles, or nested oscillation.

A **directional reversal** (Class B predicted suppressed but actually
elevated, or Class C predicted elevated but actually suppressed) is
the strongest form of misprediction and must be flagged.

### Step 6 — Document honestly

Record the result regardless of verdict. Do not reclassify after
seeing CV. If the original classification feels wrong post-hoc,
note this as a limitation, do not silently reassign.

## Decision summary table

| If physics says… | Assign | n | CV prediction | Example |
|------------------|--------|---|---------------|---------|
| Two states **with SO(2) regulator** (default) | Z₂ | 2 | 1/(2π) ≈ 0.1592 | Heart (systole/diastole) on cardiac cycle |
| Two states **without any SO(2) regulator** (truly memoryless) | Z₂_only | 2 | **1.0** (exponential) | Radioactive decay |
| Continuous cycle | SO(2) | 4 | 1/(4π) ≈ 0.0796 | Respiration (NREM) |
| n discrete phases | Z_n | n | 1/(nπ) (paper) **or** n/(4π) (discrete-phase) | Cell cycle (n = 4) |
| Compact Lie group G | M22 | — | 1/(2·φ_G) | Spin-1/2 (SU(2), φ = 2π) |
| Ambiguous | Z₂ default | 2 | 0.1592 | Conservative fallback |

## Pre-registration discipline (from Appendix C)

The integrity of the protocol depends on:

1. The classification (steps 2–4) is recorded **before** the
   empirical CV is consulted.
2. The classification is **not changed** after seeing CV.
3. Misses are documented honestly with diagnostic interpretation,
   not retroactively reassigned to a different class.
