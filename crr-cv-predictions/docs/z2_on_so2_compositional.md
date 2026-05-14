# Z₂-on-SO(2) compositional predictions

## The framing

CRR convention C1 says **the rupture event is structurally Z₂** by
construction (Dirac-delta / Heaviside-derivative / Cramér–Rao
saturation arguments; see `notes/rupture_topology.md`). Convention C2
says **the continual memory-bearing manifold is a compact connected
Lie group G**, with the canonical choice G = SO(2).

The conventions together imply: every CRR system has a Z₂ rupture
*and* a continual phase substrate. The paper's Z₂ / SO(2) entries in
the 132-system table are therefore not two parallel substrates but
two limit cases of a single compositional structure:

- **Z₂-only** (no continuous phase): one Bernoulli draw per cycle.
  Geodesic = π (half-turn embedding of Z₂ inside SO(2)).
  CV = 1/(2π).
- **One Z₂ rupture on a single SO(2) circuit**: one Bernoulli draw
  per full revolution. Geodesic = 2π. CV = 1/(4π).
- **k Z₂ ruptures per SO(2) circuit**: k Bernoulli draws per
  revolution. Predictions in this section.

This is *not* the discrete-phase Z_n hierarchy (M15), which uses
n equally-spaced phase points on a circle. The k-Z₂-per-SO(2)
construction is **continuous-phase** with k Z₂ rupture events at
arbitrary phase angles. The two structures coincide only when k = n
*and* the ruptures are forced to the n-gon vertices.

## New parameter-free predictions

### P1 — Two Z₂ ruptures per SO(2) circuit have ρ = −1/2 anti-correlation

From M11 (`claims/M11_z2_compose_so2_anticorrelation/`), forced by
variance preservation on the shared SO(2) phase. Two examples:

- **Cardio-respiratory coupling.** Heart and breath each have Z₂
  rupture structure (systole/diastole; inspiration/expiration). If
  they share a single coupled SO(2) substrate (cardiac arrhythmia
  literature: respiratory-sinus-arrhythmia; Heitmann 2020 *Front
  Physiol* 11:494) then rupture-rate fluctuations should
  anti-correlate at ρ = −1/2.
- **EEG cross-frequency theta-gamma coupling.** Gamma bursts (Z₂)
  riding on theta phase (SO(2)). Two gamma-burst channels sharing
  a single theta substrate should show ρ = −1/2 amplitude
  fluctuation correlation.

### P2 — Nested CV: cycle-period vs sub-rupture jitter

If a system has k Z₂ ruptures per SO(2) circuit, then:

- **Full-cycle CV** (one revolution) = 1/(4π) ≈ 0.0796 (SO(2)).
- **Sub-rupture jitter CV** (one Z₂ event) = 1/(2π) ≈ 0.1592 (Z₂).
- The ratio CV_sub / CV_cycle = 2 exactly (M2 topological).

Predicted in:

- **Cardiac P-Q-R-S-T sub-intervals.** RR period CV ≈ 1/(4π);
  individual P-R, QT, etc. sub-interval CVs ≈ 1/(2π).
- **Respiratory inspiration vs full breath.** Inspiration sub-CV
  ≈ 1/(2π); full inhale-exhale CV ≈ 1/(4π).
- **Neural burst-rate vs intra-burst spike CV.** Burst-period CV
  ≈ 1/(4π); intra-burst inter-spike interval CV ≈ 1/(2π).

### P3 — k Z₂ ruptures per SO(2) circuit: total cycle CV

The k-channel construction gives a total cycle CV that depends on
how the ruptures share the SO(2) circuit's variance. If they share
equally (each contributes 1/k of the total variance, conditional on
sharing a single revolution), the analogue of M11 generalises to
ρ_{ij} = −1/(k−1) anti-correlation between every pair.

Predicted in:

- **KaiC circadian phosphorylation.** ~24 phosphorylation sites
  per ~24 hr cycle, but ~60 effective sub-states. Treating as
  k = 24 Z₂ events per SO(2) circuit gives ρ_{ij} = −1/23 ≈ −0.043
  between any two site-occupancy time series. Testable against
  Rust et al. 2007 / Nakajima 2005 cycle data.
- **Drosophila syncytial divisions.** 13 rapid nuclear divisions
  per maternally-loaded SO(2) developmental clock; predicted
  ρ_{ij} = −1/12 ≈ −0.083.
- **Hippocampal theta cycle phase-locked gamma bursts.** 6–8 gamma
  bursts per theta cycle → ρ_{ij} ≈ −1/6 ≈ −0.167.

### P4 — Z₂ ruptures embedded in larger G inherit φ_G

If the rupture event is Z₂ but the system's continual substrate is
a larger Lie group G (e.g. SU(2), SO(3), or T²), then the predicted
cycle CV is still 1/(2·φ_G), set by the substrate alone — not by
the rupture topology. This is the M22 generalisation read forward:

- A **spin-1/2 NMR relaxation** event is a Z₂ flip on an SU(2)
  substrate. φ_{SU(2)} = 2π → CV = 1/(4π).
- A **rigid-body precession reversal** is a Z₂ flip on an SO(3)
  substrate. φ_{SO(3)} = π → CV = 1/(2π).
- A **bicommensurate biological clock** with two phase-locked
  rotational oscillators is Z₂ on T². CV per generator = 1/(4π).

This is the central content of "all Z₂ ruptures on a Lie group
structure": the rupture is always the same Bernoulli draw, but the
*observable cycle CV* is determined by the substrate's geodesic
length φ_G alone.

## Concrete candidate systems for testing

The CSV file `data/cv_predictions_z2_on_so2.csv` contains 14
pre-registered Z₂-on-SO(2) predictions with target empirical sources.
Verdicts are `PENDING` until data is consulted.
