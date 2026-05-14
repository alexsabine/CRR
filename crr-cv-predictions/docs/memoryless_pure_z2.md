# The third Z₂ reading: pure memoryless (CV = 1)

Source: Sabine (April 2026), *The Geometric Origin of Memoryless
Variability — A CRR derivation of CV = 1 for the exponential
distribution* (`radioactive_crr_finding_2.pdf`).

## The reinterpretation

The 132-system table in the main paper labels many systems "Z₂" with
predicted CV = 1/(2π) ≈ 0.159 — heart-valve open/close, neuron
spike/no-spike, light switch on/off, etc. Each of these systems has,
on physical inspection, an **implicit SO(2) regulator** in the causal
chain: cardiac electrical cycle, membrane potential oscillation,
rocker arc, etc. The "Z₂" label is shorthand for a Z₂ rupture
*regulated* by an SO(2) substrate — what convention C2 in
`notes/conventions.md` already calls the compositional reading.

The new finding identifies a third case: **pure Z₂ with no SO(2)
regulator anywhere in the causal chain** — the truly memoryless case.
Its CV is not 1/(2π); it is **1 exactly** (the exponential distribution).

## Three Z₂ readings, one formula chain

| Label | Reading | C* substrate | CV |
|-------|---------|--------------|-----|
| `Z2_only` | Pure Z₂ rupture; no SO(2) regulator anywhere. Memoryless. | C*_absent = 2π (vacuum geodesic) | **1** |
| `Z2` (or `Z2_on_SO2`) | Z₂ rupture with implicit SO(2) regulator. The 132-table default. | C*_present = 2π (regulating cycle) | **1/(2π) ≈ 0.159** |
| `SO(2)` | Continuous SO(2) cycle observed directly (no Z₂ projection). | C*_present = 2π | **1/(4π) ≈ 0.080** |

The key identity:

    CV(pure Z₂) = CV(Z₂-on-SO(2)) × C*_absent_SO(2)
                = (1/2π) × 2π
                = 1

The Z₂ baseline CV is inflated by the geodesic extent of the *absent*
SO(2) substrate. The absence is quantified by the geometry of what is
absent.

## The asymmetry

Only `Z₂ × SO(2) = 1` returns unity:

| Product | Value | Physical reading |
|---------|-------|------------------|
| CV(Z₂) × C*_SO(2) | (1/2π) × 2π = **1** | Removing the SO(2) regulator from a Z₂ event gives memoryless Poisson statistics. |
| CV(SO(2)) × C*_Z₂ | (1/4π) × π = **1/4** | Removing a Z₂ projection from an SO(2) cycle does not produce memorylessness. |

This asymmetry is physically necessary: a continuous rotation can
exist without producing binary events; a binary event cannot occur in
physical reality without a continuous substrate somewhere in the
causal chain. Pure Z₂ exists only in the limit of a system with no
geometric closure — the radioactive nucleus.

## The structural specificity

The 2π factor appears only on continuous manifolds, not on discrete
ones. Verification:

- **Exponential distribution** (continuous memoryless): CV = 1, with
  the 2π factor explicit.
- **Geometric distribution** (discrete memoryless): CV = √(1−p)/p,
  varies continuously with p, no clean 2π factor at any value.

This rules out numerological coincidence: the inflation factor is
specifically the geodesic of the absent **continuous** rotational
substrate. Where there is no continuous substrate to be missing
(the discrete lattice case), the factor does not appear.

## What this means for the 132-system table

**No row in the 132-table needs to be reclassified.** Every "Z₂"
entry in Appendix A is empirically consistent with CV ≈ 1/(2π), so
each genuinely sits in the Z₂-on-SO(2) regime — confirming the
"every Z₂ has an SO(2) regulator" claim from physical inspection.

But several Class C "elevated" systems in the table sit at high
ratios that approach the 2π = 6.28 inflation limit:

| Row | System | Ratio | Reading |
|-----|--------|-------|---------|
| 16 | Spontaneous blink interval | 5.03× | Approaching memoryless limit (Poisson-like blinks) |
| 21 | Head direction cell ISI | 4.27× | Near-Poisson point process |
| 68 | Mast seeding interval | 3.77× | Near-Poisson recurrence |
| 111 | Inter-sigh interval | 3.77× | Near-Poisson sighing |
| 75 | Earthquake recurrence | 3.14× | Self-organised criticality, partially memoryless |

The framework's diagnostic for these now sharpens: a Class C system
at ratio ≈ 2π is not just "elevated" — it is **approaching the pure
memoryless limit** because its SO(2) regulator is absent or weak.

## Predictions for genuinely memoryless processes

The radioactive paper's central prediction is:

**Any system with NO SO(2) regulator anywhere in the causal chain has
CV = 1 exactly.**

Candidate systems (filed in `data/cv_predictions_memoryless.csv`):

1. **Radioactive decay** — the canonical case. Theoretically exact;
   any single-isotope inter-decay-time CV is 1.
2. **Single-photon arrival times** in a steady incoherent source.
3. **Cosmic ray inter-arrival times** at a detector.
4. **M/M/1 queue inter-arrival times** in queueing theory.
5. **Single-molecule unbinding events** in the rate-limited regime.
6. **Spontaneous synaptic vesicle release** (under conditions where
   release is Poisson, e.g., low-Ca²⁺ minis at NMJ).
7. **Quantum tunneling escape times** for a single particle (no
   coherent oscillation).
8. **Thermal-noise bit flips** in a non-feedback memory cell.

For each, the prediction is CV = 1 ± ε with ε set by sample size
(Monte Carlo: 100 trials of 10⁶ samples gave 1.000099 ± 0.000953).

## Falsification criteria

The CV = 1 prediction is falsified by:

1. A memoryless continuous process with CV ≠ 1. Mathematically
   impossible — this is a theorem about the exponential distribution.
2. A physical Z₂ system *demonstrably* lacking SO(2) regulation but
   with CV ≠ 1.
3. A physical Z₂ system *demonstrably* having SO(2) regulation but
   with CV ≈ 1.

Note that (2) and (3) require independent characterisation of whether
an SO(2) regulator is present. The framework predicts: SO(2) presence
↔ CV ≈ 1/(2π); SO(2) absence ↔ CV ≈ 1.

## Relationship to existing claims

- **Convention C1** (rupture is Z₂ by construction) — unchanged. The
  rupture event is always Z₂.
- **Convention C2** (phase manifold is compact connected Lie group G)
  — extended. G can be the trivial group (no continuous-phase
  content), in which case the system is memoryless and CV = 1.
- **M11** (ρ = -1/2 between two Z₂ on shared SO(2)) — unchanged for
  Z₂_on_SO(2) systems; trivially undefined for Z₂_only (no shared
  substrate).
- **M22** (CV_G = 1/(2·φ_G)) — extended. The trivial group case
  (G = {e}, φ_G = 0 is degenerate) is replaced by the formal
  φ_G = 1/2 convention so that CV = 1.

## The general principle (Appendix A of the radioactive paper)

> Discrete states require boundaries, boundaries require continuous
> substrates, and the continuous substrate governs the timing of the
> discrete transition. When the continuous substrate is absent, the
> timing becomes memoryless, and the variability is inflated by
> exactly the geometric extent of what is missing.
