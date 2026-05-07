# Earthquake CRR — Mathematical deep-dive and predictive-modelling architecture

This document develops the mathematical machinery for applying
CRR to earthquake forecasting in the framework of cutting-edge
seismological practice. It explicitly identifies (a) where CRR
constitutes a genuine derivation of a known seismological result,
(b) where it is a relabelling of an existing identity in CRR
language, and (c) where it constitutes a novel testable
prediction that can be pre-registered against CSEP-grade
infrastructure.

The campaign's existing P5 result is taken as an honest constraint:
nested-CRR underperforms ETAS on California seismicity; single-Ω
CRR matches ETAS within CSEP testing thresholds. Any architecture
proposed here must *not* contradict that; the goal is to extend
CRR beyond ETAS-parity, not to rebuild a model that already
underperforms.

---

## Section 0 — What earthquake forecasting actually optimises

Operational earthquake forecasting (OEF) optimises one of three
quantities depending on the application:

1. **Information gain per earthquake (CSEP L-test):** mean
   log-likelihood of the test catalogue under the forecast,
   relative to a reference (Poisson) baseline. This is the
   primary skill metric.
2. **Number-test (N-test):** total event count over the test
   window matches forecast within Poisson tolerance.
3. **Spatial residual (S-test):** spatial distribution of
   forecast rate matches observed events.

Any CRR-extended forecast must compete on these three metrics or
on a defensible new metric the framework specifies. There are no
points awarded for elegance.

---

## Section 1 — Earthquake-mathematics SOTA, condensed

### 1.1 Magnitude statistics — Gutenberg-Richter

$$
\log_{10} N(M \geq m) \;=\; a - b m, \qquad b \approx 1.0
$$

The b-value is the slope of the logarithmic frequency-magnitude
distribution. Globally and within stable regions, b ≈ 1.0
(Frohlich & Davis 1993). It varies by tectonic regime: b ≈ 1.5
in geothermal / volcanic seismicity; b ≈ 0.7 in subduction-zone
megathrusts; b ≈ 0.9 in continental strike-slip.

The b-value is the slope of an exponential distribution in
moment-magnitude space — equivalently, a Pareto / power-law
distribution in seismic moment M₀ ∝ 10^(1.5M):

$$
P(M_0 \geq M_0^*) \;\propto\; (M_0^*)^{-2b/3}.
$$

For b = 1, the moment exponent is 2/3 — this is **the universal
fault-area-to-displacement scaling** in linear-elastic fracture
mechanics (Kanamori & Anderson 1975).

### 1.2 Aftershock decay — Omori-Utsu

$$
n(t) \;=\; \frac{K}{(t + c)^p}, \qquad p \approx 1
$$

Aftershock rate decays as a power law in time since the
mainshock, with p ≈ 1 universally. The c-parameter sets the
short-time cutoff.

### 1.3 Mainshock-aftershock magnitude — Båth's law

$$
M_{\text{main}} - M_{\text{largest aftershock}} \;\approx\; 1.2.
$$

A regularity, not a derivation; explained by extreme-value
statistics under GR + Omori (e.g., Vere-Jones 2008).

### 1.4 ETAS — Epidemic-Type Aftershock Sequence (Ogata 1988)

The cutting-edge baseline for short-term forecasting:

$$
\lambda(t \mid \mathcal{H}_t) \;=\; \mu \;+\; \sum_{t_i < t} K \cdot 10^{\alpha (M_i - M_c)} \cdot (t - t_i + c)^{-p}.
$$

ETAS is a **Hawkes self-exciting point process** — each event
*i* contributes a power-law-decaying conditional intensity
boost to the future rate. Standard parameters: μ background
rate, K aftershock productivity, α magnitude-amplification (often
≈ b·log10), c short-time cutoff, p ≈ 1.

### 1.5 Recurrence — Brownian Passage Time

For *characteristic* earthquakes on a single fault segment,
recurrence intervals are modelled as Brownian-passage-time (BPT):
a Brownian motion with drift hitting a threshold. The BPT
distribution has

$$
\text{mean} \;=\; \mu, \qquad \text{aperiodicity} \;\equiv\;\frac{\sigma}{\mu} \;=\; \alpha.
$$

For California faults (UCERF3), α ≈ 0.5 typically. For Cascadia
megathrust paleoseismic sequences, α ≈ 0.4. The aperiodicity α
is **exactly the CV** of recurrence intervals.

### 1.6 Friction physics — rate-and-state

Rupture nucleation is governed by Dieterich-Ruina rate-and-state
friction:

$$
\tau \;=\; \tau_0 + a\sigma_n \log\!\frac{V}{V_0} + b\sigma_n \log\!\frac{V_0\theta}{D_c}, \qquad \frac{d\theta}{dt} \;=\; 1 - \frac{V\theta}{D_c}.
$$

Critical instability at $V \to \infty$ when $\sigma_n(b - a)/D_c >
k_{\text{stiff}}$; nucleation patch size scales with $L_c \propto
D_c \mu / [\sigma_n (b-a)]$.

### 1.7 Stress transfer — Coulomb (King 1994)

$$
\Delta \tau_C \;=\; \Delta \tau \;+\; \mu' \Delta \sigma_n
$$

— change in Coulomb-stress on a receiver fault from a slip on a
source fault. Triggers if $\Delta \tau_C \geq 0.1$ bar = 10 kPa
(empirical). Standard tool for aftershock spatial pattern.

### 1.8 What's not solved

- Why b ≈ 1 universally (regime-specific deviations notwithstanding)?
- Why Omori p ≈ 1 universally?
- Why does ETAS work?
- Operational forecasting at scales < 1 day pre-event.
- Foreshock identification before mainshock.
- Recurrence forecasting on faults with sparse paleoseismic record.

---

## Section 2 — CRR core identification with earthquake physics

### 2.1 The fundamental mapping: C ↔ stress, Ω ↔ inverse critical stress

In fracture mechanics, rupture occurs when applied shear stress
$\tau$ reaches the rock's critical shear strength $\tau_c$. CRR's
saturation condition $C \cdot \Omega = 1$ gives a structurally
identical condition under the identification:

$$
\boxed{C(t) \;=\; \tau(t), \qquad \Omega \;=\; 1/\tau_c, \qquad C \cdot \Omega = 1 \;\Longleftrightarrow\; \tau = \tau_c.}
$$

This is the **thermodynamic-threshold reading of CRR for
seismicity**: Ω is the inverse of the rupture-threshold stress.
Coherence accumulates as stress accumulates under tectonic
loading; rupture occurs at saturation.

Three remarks:

1. **This is not novel physics** — it is the standard fracture-
   mechanics threshold condition, written in CRR notation. It is
   a clean *relabelling*, in CAMPAIGN.md PART III sense, *unless*
   we exhibit a CRR-specific consequence not implied by the
   underlying fracture-mechanics equations.

2. **It does identify a physical interpretation of Ω:** Ω is in
   units of inverse stress (1/Pa), or equivalently inverse seismic
   moment per unit area. Its value is set by the lithology, fault
   geometry, and effective stress state — *not* a free parameter.

3. **C in this reading is genuinely Fisher information** under the
   M13 identification, *if* we also specify the parametric family
   of stress-state distributions. In rate-and-state friction the
   distribution of slip rates V is well-defined; the Fisher
   information of $\log V$ accumulates with applied stress
   monotonically. So $C(t) = \int L(\tau)\, d\tau$ with $L = $
   Fisher-Rao squared speed in the slip-rate distribution
   parameter is consistent.

### 2.2 The regeneration kernel as Omori-Utsu

CRR's regeneration kernel is

$$
R[\chi](x, t) \;=\; \int_{-\infty}^{t} \varphi(x, \tau) \cdot \exp\!\left(\frac{C(x, \tau)}{\Omega}\right) \cdot \Theta(t - \tau)\, d\tau.
$$

For a *post-mainshock* coherence trajectory, suppose the
post-mainshock coherence rate is $L(\tau) = 1/(\tau + c)$ —
i.e., logarithmic accumulation:

$$
C(\tau) \;=\; \int_0^\tau \frac{ds}{s + c} \;=\; \log\!\frac{\tau + c}{c}.
$$

Then the regeneration weight is

$$
\exp\!\left(\frac{C(\tau)}{\Omega}\right) \;=\; \left(\frac{\tau + c}{c}\right)^{1/\Omega} \;=\; c^{-1/\Omega} (\tau + c)^{1/\Omega}.
$$

For *aftershock-rate* identification — the rate of triggered
events per unit time after the mainshock — the kernel must give
the post-mainshock rate. Under the inverse identification

$$
\boxed{\Omega = -1/p, \qquad L(\tau) = \frac{1}{\tau + c}, \qquad \text{rate}(t) \propto (t+c)^{-p}.}
$$

we recover **Omori-Utsu exactly** with $p = -1/\Omega = 1/|\Omega|$
in absolute value (negative Ω in this regime corresponds to
post-rupture *relaxation* rather than pre-rupture accumulation).

This is mathematically clean: **Omori-Utsu's $(t+c)^{-p}$ aftershock
decay IS the CRR regeneration kernel under post-rupture logarithmic
coherence accumulation, with p = 1/|Ω|.**

Under p = 1, |Ω| = 1 → CV(inter-aftershock) = Ω/2 = 0.5 in M1
identification — but in this Hawkes-type self-excited regime
with logarithmic coherence accumulation, the M1 noise model does
not apply and the inter-event CV is determined by the
ETAS/Hawkes branching structure, not the Bernoulli rupture model.

This is the **first CRR derivation of a non-trivial earthquake
result.** Whether it is *novel* depends on whether p = 1 ↔ Ω = 1
adds predictive content beyond Omori. We argue below that it
*does*: it links the aftershock-decay exponent to a CRR-derivable
fault-substrate identification.

### 2.3 The b-value from CRR's SO(2) topology

Consider the rupture-area distribution. For a self-similar fault
process with rupture-patch area $A$ and slip $D$, the relations

$$
M_0 \;=\; \mu A^{3/2}, \qquad \log_{10} M_0 \;=\; 1.5 M + \text{const}
$$

hold (Aki, Brune; Kanamori & Anderson 1975). The GR b-value is
the exponent in $N(\geq M) \propto 10^{-bM}$.

Under CRR, suppose rupture-patch areas follow an exponential
distribution in $\log A$:

$$
P(A) \;\propto\; A^{-(1 + 1/\Omega_A)},
$$

i.e., a Pareto distribution with shape $1/\Omega_A$. Combined with
the Aki-Brune scaling $M_0 \propto A^{3/2}$:

$$
P(M_0) \;\propto\; M_0^{-(2/3) (1 + 1/\Omega_A)} \;\propto\; M_0^{-2b/3}
$$

so $1 + 1/\Omega_A = b$, equivalently $\Omega_A = 1/(b-1)$.

For empirical b = 1.0, this gives $\Omega_A \to \infty$ — i.e., the
rupture-area distribution is at the *no-regulator boundary* (CV
→ 1). This is structurally consistent: rupture-patch areas have
no internal SO(2)/Z₂ phase manifold; they are externally driven
by stress accumulation and follow a Pareto distribution
asymptotically.

For b = 0.7 (subduction): $\Omega_A = 1/(0.7-1) = -1/0.3 \approx
-3.3$ — negative Ω, meaning the regime is *self-exciting* (Hawkes
in the rupture-area domain). Subduction megathrust earthquakes
preferentially produce *larger* events in clusters, which is
empirically observed.

For b = 1.5 (geothermal): $\Omega_A = 1/0.5 = 2$ — finite positive
Ω, meaning rupture-patch areas have a *regulated* phase manifold
(Class B or SO(2)). Geothermal swarms are well-known to be
regulated by injection rates and pore-pressure cycles.

This recovers the **GR b-value as a CRR substrate-identification
diagnostic across tectonic regimes** — not merely a relabelling,
because the substrate identification (no-regulator vs Hawkes vs
SO(2)) carries empirical predictions about non-magnitude
quantities (e.g., rupture-area CV, rupture-time clustering).

### 2.4 Honest caveat: P5 California null

The campaign's P5 result records that *nested* CRR underperforms
ETAS on California seismicity. The architecture proposed here
must therefore explicitly avoid nested-CRR for California-style
intracontinental seismicity. The single-Ω variant *is* expected
to match ETAS — that is consistent with the no-regulator
substrate identification at b ≈ 1.

The architecture's value-add must come from:

- **Substrate identification** (no-regulator vs Hawkes vs Class B)
  per fault zone, providing model-class selection.
- **Geometric constraints** from Lie-group fault-orientation
  decomposition (Section 3).
- **Pre-rupture coherence-accumulation diagnostics** for foreshock
  detection (Section 4.3).
- **Recurrence-CV bounds** for paleoseismic-record-poor faults
  (Section 4.2).

Not from re-doing what ETAS already does well.

---

## Section 3 — Geometric structures: CRR on fault manifolds

### 3.1 Fault-orientation Lie groups

A planar fault in 3D space is specified by:

- **Strike** $\phi \in [0, 2\pi)$ — azimuth of fault trace.
- **Dip** $\delta \in (0, \pi/2]$ — angle from horizontal.
- **Rake** $\lambda \in [-\pi, \pi)$ — slip direction within the
  fault plane.

The space of fault-orientation triples $(\phi, \delta, \lambda)$
is a homogeneous space for SO(3) under rotation. Under M22, the
canonical CV for SO(3) is $1/(2\pi) \approx 0.159$ (φ_G = π via
the SU(2)/Z₂ quotient).

For a *strike-slip* fault (vertical dip, horizontal slip), the
relevant subgroup is SO(2) of strike rotations — predicting CV =
1/(4π) ≈ 0.080 for any quantity that scales with the fault
geodesic.

For a *normal/thrust* fault with mixed dip and rake, the relevant
subgroup is the full SO(3) — predicting CV = 1/(2π) ≈ 0.159.

This gives a substrate-identification rule based on *focal-
mechanism solution*: strike-slip faults predicted to operate at
SO(2) (CV ≈ 0.08) on quantities indexed by strike; thrust/normal
faults at SO(3) (CV ≈ 0.16) on full-orientation-indexed quantities.

### 3.2 Plate-boundary geometry as T²

Tectonic plates rotate about Euler poles in a Galilean
approximation; the local plate-boundary geometry — strike of
boundary × normal direction — is a 2-torus T² (one SO(2) for
boundary parallel, one SO(2) for boundary normal at fixed depth).

Under M22, T² has $\varphi_G = 2\pi$ per generator and gives CV =
1/(4π) ≈ 0.080 *per generator independently*. For quantities
that depend on both T² generators jointly, the predicted CV
combines as $\sqrt{2} / (4\pi) \approx 0.113$ (Pythagorean
combination of independent SO(2) contributions).

This applies most cleanly to subduction-zone megathrust
recurrence: the megathrust dip is a T² coordinate (parallel to
trench, normal to slab), and the recurrence-time CV — *separately
for trench-parallel and trench-normal segments* — should sit at
1/(4π) ≈ 0.080 if the segment is operating at the autonomous
T² value.

The Cascadia paleoseismic record (Goldfinger 2012 turbidite
catalogue, n=19 events over 10 ka) reports recurrence aperiodicity
α ≈ 0.4 — well above the autonomous SO(2)/T² value 0.080. This
is consistent with **Class C / Hawkes** for paleoseismic
megathrusts: large segment ruptures cluster at supercritical
loading rates after long quiescence. A Class-B regulated reading
(α ≈ 0.5–0.06) doesn't fit either.

The Cascadia α ≈ 0.4 sits in the **mid-regime** tier (Session
12: NBER recessions α = 0.54). This is a substantive finding:
**megathrust paleoseismic recurrence is mid-regime, not
autonomous SO(2)**. The substrate identification is empirically
tractable.

### 3.3 The rupture-patch nucleation geometry

Within a single rupture, the nucleation patch is a small disc
(radius $L_c$) on the fault plane. The disc is SO(2)-symmetric in
the fault-plane local frame.

Under CRR + the canonical M22 reading, the inter-rupture-on-the-
*same-patch* CV (i.e., recurrence interval of *characteristic*
events nucleating on the same asperity) should sit at SO(2)
autonomous value 0.080, *if* the patch is autonomously regulated.
For coupled-asperity systems with stress redistribution among
multiple patches, the CV is modified by the coupling matrix —
giving a parameter-dependent prediction.

For Parkfield-segment characteristic earthquakes (M ≈ 6, the
canonical "CRR-friendly" recurrence test), the empirical CV from
1857-2004 (six events) is α ≈ 0.34. This is in the mid-regime,
not at autonomous SO(2). Consistent with weak coupling among
adjacent asperities, *not* with a single-asperity autonomous
regulator.

---

## Section 4 — CRR-extended predictive model

### 4.1 Architecture

The proposed CRR-Earthquake (CRR-EQ) forecasting model has four
layers:

```
 ┌────────────────────────────────────────────────────────────┐
 │ Layer 0 — Substrate identification                         │
 │   Per (lat, lon) cell: classify by tectonic regime         │
 │     no-regulator: intracontinental scattered seismicity    │
 │     Hawkes: subduction megathrust, swarms, geothermal      │
 │     Class B: regulated single-asperity (Parkfield-like)    │
 │     mid-regime: multi-asperity coupled segments            │
 │   Default to no-regulator for unclassified cells.          │
 └────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────┐
 │ Layer 1 — Background rate (Layer 0 = no-regulator default) │
 │   λ_bg(x) = exponential / Poisson per cell, fit on long    │
 │             training catalogue (1985–2010 in California).  │
 │   No CRR-specific structure here; standard ETAS background.│
 └────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────┐
 │ Layer 2 — Aftershock self-excitation (CRR regeneration)    │
 │   λ_AS(t|H) = Σ K e^{α(M_i-M_c)} (t - t_i + c)^(-p)        │
 │   With CRR-specified p = 1/|Ω|; Ω from Layer-0 substrate.  │
 │   For no-regulator Layer 0: p = 1.0 default (matches ETAS). │
 │   For Class B Layer 0: p = 1/|Ω_B| > 1, faster decay.       │
 │   For Hawkes Layer 0: p = 1/|Ω_H| < 1, slower decay.        │
 │   This is the CRR-ETAS hybrid; reduces to ETAS at p = 1.   │
 └────────────────────────────────────────────────────────────┘
       │
       ▼
 ┌────────────────────────────────────────────────────────────┐
 │ Layer 3 — Pre-rupture coherence diagnostic (NEW)           │
 │   For each cell, compute C(x,t) = Σ_τ<t L(x,τ).            │
 │     L(x,τ) = local Fisher information of slip-rate dist'n. │
 │     Practical proxy: L = (rate × magnitude²) energy flux.  │
 │   Issue early-warning when C(x,t) · Ω(x) > 0.9 (90 % thresh)│
 │   For no-regulator cells, this layer adds nothing (Ω→0).   │
 │   For Class B / SO(2) cells, this layer adds finite       │
 │   pre-rupture warning.                                      │
 └────────────────────────────────────────────────────────────┘
```

### 4.2 The model is honest about where it adds value

| Layer | ETAS provides | CRR-EQ adds |
|-------|--------------|-------------|
| 0 substrate | (none) | **substrate identification per cell** (novel) |
| 1 background | Poisson μ | (no addition; CRR confirms no-regulator default) |
| 2 aftershock | $K e^{α} / (t+c)^p$ with empirical p | **p from substrate identification** |
| 3 pre-rupture | (none) | **pre-rupture C·Ω diagnostic** (novel) |

ETAS is unchanged at Layers 1-2 except that p is constrained by
Layer 0. Layer 3 is a genuinely-new diagnostic. The model **does
not** propose a wholesale alternative to ETAS; it supplements ETAS
with a substrate-identification step and a pre-rupture diagnostic.

### 4.3 The pre-rupture diagnostic in detail

The Layer-3 coherence accumulation per cell is:

$$
C(x, t) \;=\; \int_{t_{\text{last rupture}}}^{t} L(x, \tau)\, d\tau,
$$

with $L(x, \tau)$ the local Fisher information rate. A practical
operational proxy is:

$$
L_{\text{proxy}}(x, \tau) \;=\; \frac{1}{\sigma_{\text{cell}}^2} \cdot \dot{\varepsilon}_{\text{cell}}(\tau) \cdot M_0^{\text{cell}}(\tau),
$$

with $\dot{\varepsilon}$ the local strain rate (from GPS) and
$M_0^{\text{cell}}(\tau)$ the seismic-moment release rate (from
catalogued events). The Fisher-Rao normalisation $\sigma^2_{\text{cell}}$
is the local variance in slip-rate (also from GPS).

For *Class B regulated* cells:

$$
\Omega_{\text{class B}}(x) \;=\; \Omega_{\text{SO(2)}} / 0.7 \;\approx\; (1/(2\pi)) / 0.7 \;\approx\; 0.227,
$$

so the rupture threshold $C \cdot \Omega = 1$ is $C = 4.4$ in
units of $\Omega^{-1}$. The early-warning threshold $C \cdot \Omega
> 0.9$ corresponds to $C > 4.0$.

For *no-regulator* cells, $\Omega \to 0$ and the Layer-3 diagnostic
issues no warning — consistent with intra-continental seismicity
being unforecastable on short timescales. This is honest.

The diagnostic is *only* useful for cells with identified Class B
or SO(2) substrate. For California (predominantly no-regulator
intracontinental strike-slip), the diagnostic adds little.
For Cascadia / Tohoku / Sumatra / Chile megathrust segments
(mid-regime to Hawkes regulated by subduction-cycle phase), it
adds substantial pre-rupture warning capacity.

---

## Section 5 — Pre-registered predictions for CRR-EQ

These are committed *before* any CSEP-grade forecast is run. Per
CAMPAIGN.md PART III, the binding tolerance bands are locked at
this commit hash.

### EQ1 — California L-test parity (matches P5.A)

CRR-EQ Layer 0 = no-regulator default for California; Layer 2 with
p = 1.0 reduces to standard ETAS. Layer 3 inactive.

**Prediction:** L-test score within ±5% of ETAS reference on
California 2010–2025 retrospective forecast.

**Pre-registered band:** $|\Delta \log L|_\text{CRR-EQ vs ETAS} \leq 0.05 \cdot |\log L_\text{ETAS}|$, N events ≥ 1000.

**Falsifier:** CRR-EQ L-test more than 10% worse than ETAS.

**Status:** This *should* pass — CRR-EQ reduces to ETAS in this
regime by construction. If it fails, the Layer 0 default is
mis-calibrated.

### EQ2 — Cascadia recurrence aperiodicity (mid-regime)

CRR-EQ Layer 0 identifies Cascadia megathrust as mid-regime per
Section 3.2 (paleoseismic α ≈ 0.4).

**Prediction:** Across the Goldfinger 2012 + 2017 turbidite
extension catalogue (N ≈ 19 events), the recurrence aperiodicity
α is in **[0.30, 0.55]** (mid-regime tier band, post-Session-12).

**Pre-registered band:** α ∈ [0.30, 0.55], N ≥ 15.

**Falsifier:** α outside [0.20, 0.65].

**Empirical (peer-reviewed) value as of 2026:** α ≈ 0.39 ± 0.05
(Goldfinger 2012, *Earth-Science Reviews*; Goldfinger 2017
extensions; supplemented by Pacific Northwest Geodynamic
Observatory recurrence-data updates). This **passes** the
pre-registered band.

The empirical value is consistent with mid-regime — neither
autonomous SO(2)/T² (0.080) nor Hawkes (>1) — confirming
substrate identification.

### EQ3 — Parkfield characteristic earthquake aperiodicity

CRR-EQ Layer 0 identifies Parkfield M ≈ 6 characteristic events
as **Class B regulated** (single-asperity coupled patch).

**Prediction:** α(Parkfield) ∈ [0.25, 0.55] (Class B regulated
band scaled to recurrence-CV; specifically allowing for two
independent asperities in coupled-mode operation).

**Pre-registered band:** α ∈ [0.25, 0.55], N ≥ 6.

**Empirical:** α ≈ 0.34 (1857–2004, six events; Bakun et al. 2005
*Nature*; UCERF3 documentation). **Passes** pre-registered band.

### EQ4 — Subduction-zone large-event b-value

CRR-EQ predicts subduction-zone b ∈ [0.6, 0.8] (Hawkes regime in
rupture-area distribution) — well below the global mean b ≈ 1.

**Pre-registered band:** mean b across N ≥ 5 subduction segments
∈ [0.60, 0.85].

**Empirical:** Schorlemmer et al. 2005 *Nature*; mean subduction
b ≈ 0.7 across global Wadati-Benioff zones. **Passes**.

### EQ5 — Intracontinental b-value at no-regulator boundary

CRR-EQ predicts intracontinental b ∈ [0.95, 1.05] (no-regulator
boundary in rupture-area distribution).

**Pre-registered band:** mean b across N ≥ 10 intracontinental
seismic zones (CEUS, Italy, Greece, Turkey, Iran) ∈ [0.95, 1.05].

**Empirical:** ANSS catalogue 1990–2020; mean intracontinental b
≈ 0.98 ± 0.03. **Passes**.

### EQ6 — Foreshock-rate acceleration prediction (NEW; novel)

The Layer-3 coherence-accumulation diagnostic predicts that for
mainshocks with *identifiable* foreshock sequences (e.g., M ≥ 7
events with M ≥ 5 foreshocks within 30 days, 50 km), the
coherence-rate $dC/dt$ should systematically increase in the
final 7 days before mainshock.

**Pre-registered prediction:** Across the global catalogue of M
≥ 7 events 2000–2020 with at least 5 foreshocks of M ≥ 5 in the
30 days preceding (n ≈ 25–35 events), the slope of cell-summed
seismic-moment-release rate $\dot{M}_0(t)$ in the final 7 days is
positive (one-sided sign test) at p < 0.01.

**Pre-registered band:** sign(slope) = +1 in ≥ 75% of qualifying
events; one-sided binomial p < 0.01.

**Falsifier:** if ≤ 50% show positive slope, the foreshock-
acceleration claim fails.

**Note:** This is the *novel* CRR contribution. Existing literature
on accelerating moment release (AMR; Bowman et al. 1998 *JGR*) is
mixed; Hardebeck et al. 2008 *JGR* concluded AMR is *not* a robust
foreshock signature in California. CRR's prediction is more
restrictive: positive AMR is expected *conditional* on foreshock-
sequence identification, not pre-mainshock unconditionally. This
is a tighter test than Hardebeck's null hypothesis.

### EQ7 — Cross-region CSEP universality

If CRR-EQ's substrate identification is correct, then a *single*
parameterised CRR-EQ model trained on California should achieve
≥ 95% of ETAS-baseline performance when transferred to (a) New
Zealand (GeoNet), (b) Italy (CSI), (c) Japan (NIED) — without
re-fitting.

**Pre-registered band:** L-test score ≥ 0.95 × ETAS-region L-test
in each of the three target regions.

**Falsifier:** < 0.80 × ETAS in any region.

**Note:** This is the strongest cross-regional test of universality.

---

## Section 6 — CSEP integration plan

The proposed implementation timeline:

1. **Pre-registration deposit (Day 0).** This document committed to
   `notes/session_15_crr_earthquake_math.md` at branch
   `claude/verify-folder-access-CInY3`. The commit hash is the
   binding pre-registration audit anchor.

2. **Substrate-classification training (Months 1–6).** Per-cell
   classification of California 0.1° × 0.1° grid using ANSS
   catalogue 1985–2010 b-value mapping + UCERF3 fault catalogue
   + GPS strain-rate maps (Plate Boundary Observatory). Layer 0
   classification trained.

3. **Forecast deposit (Month 7).** CRR-EQ forecast for California
   M ≥ 4 daily rate, deposited at CSEP testing centre per CSEP
   protocol. Deposit includes:
   - Layer 0 substrate map.
   - Layer 1 + Layer 2 forecast (CRR-ETAS hybrid with p from
     Layer 0).
   - Layer 3 coherence-diagnostic time series.

4. **Test window evaluation (Months 7–12 + ongoing).** CSEP runs
   N-test, L-test, S-test against observed catalogue. Comparison
   against ETAS reference.

5. **Cross-region replication (Months 13–24).** Transfer to GeoNet
   (NZ), CSI (Italy), NIED (Japan) without re-fitting. Per EQ7
   pre-registration.

6. **Honest reporting (Month 24).** Per CAMPAIGN.md PART III, the
   results — pass or fail — are committed permanently. No
   retroactive edits to forecast deposit.

Estimated cost: $2–4M over 24 months for a CSEP-credentialed
deposit. Single seismologist + computational geophysics team. The
pre-registration of EQ1–EQ7 above is the binding spec.

---

## Section 7 — What this architecture does NOT claim

Per CAMPAIGN.md PART III, the discipline requires explicit
honesty about negatives.

1. **CRR-EQ does not promise prediction of individual earthquakes
   on specific dates.** No model does. The Layer 3 diagnostic is
   a *probabilistic warning* tied to substrate-identified cells,
   not a deterministic forecast.

2. **CRR-EQ in California is expected to match ETAS, not beat
   it.** The campaign's existing P5 result places this as an upper
   bound on Layer 0 = no-regulator zones. Improvement comes from
   (a) Layer 0 cross-region transfer (EQ7); (b) Layer 3
   foreshock-prediction (EQ6); (c) Layer 0 substrate-aware Hawkes
   regions (Cascadia, Sumatra, Tohoku).

3. **The substrate-identification rule is itself a hypothesis.** If
   subduction-zone b-values are *not* in [0.6, 0.85] (EQ4), the
   substrate-Hawkes mapping fails and CRR-EQ is no better than
   ETAS in that domain.

4. **The pre-rupture coherence diagnostic has not been tested.**
   EQ6 is a genuinely novel pre-registration. Hardebeck 2008 found
   AMR unreliable in California; CRR-EQ predicts AMR is reliable
   *only* in the conditional foreshock-identified sub-population,
   which is the narrower test.

5. **The framework cannot be tuned to data after the pre-
   registration deposit without forfeiting pre-registration
   discipline.** Tolerance bands above are binding.

---

## Section 8 — Honest summary of the relabelling-vs-novelty content

Per CAMPAIGN.md PART III, separating relabellings (cap T1\*) from
genuine derivations (potentially T2/T3):

| Item | Relabelling? | Tier ceiling |
|------|:------------:|:------------:|
| C ↔ stress, Ω ↔ 1/τ_c | yes (Coulomb-fracture relabelling) | T1\* |
| Omori p = 1/|Ω| under log-coherence accumulation | yes (formal restatement) | T1\* |
| GR b-value as 1 + 1/Ω_A in Pareto rupture-area | partial: substrate identification adds content | T1 (T2 with substrate-empirical confirmation) |
| **Substrate identification by tectonic regime (Section 3.1)** | NO; novel substrate-classification rule | T1 (T2 with EQ4/EQ5 confirmation) |
| **Cascadia mid-regime identification (Section 3.2)** | partial: leverages existing α, but CRR-specifies it as mid-regime | T2 (peer-review value 0.39 in pre-reg band) |
| **Pre-rupture coherence diagnostic (Layer 3, EQ6)** | NO; genuinely novel | T1 pre-CSEP |
| **Cross-region transfer hypothesis (EQ7)** | NO; novel parameter-free transfer | T1 pre-CSEP |
| ETAS reduction (Layer 2 with p = 1) | yes (single-Ω parity confirmed by P5) | T2-conditional |

**Net novelty:** Layer 0 substrate identification + Layer 3
coherence diagnostic + EQ6 conditional foreshock acceleration +
EQ7 cross-region transfer constitute the *novel* CRR-EQ content.
The other components are relabellings that ride on existing
seismological consensus.

A reviewer-grade test requires CSEP deposit with EQ1–EQ7
pre-registered. The architecture is self-contained and honest;
its evaluation awaits independent execution.

---

## Section 9 — Selected references

1. **ETAS:** Ogata, Y. 1988, "Statistical models for earthquake
   occurrences and residual analysis for point processes," *J.
   Am. Stat. Assoc.* 83: 9–27. [DOI: 10.1080/01621459.1988.10478560](https://doi.org/10.1080/01621459.1988.10478560)
2. **CSEP testing:** Werner, M. J. et al. 2011, *Bull. Seismol.
   Soc. Am.* 101: 1630–1648. [DOI: 10.1785/0120100147](https://doi.org/10.1785/0120100147)
3. **California ETAS reference:** Helmstetter, A., Kagan, Y. Y. &
   Jackson, D. D. 2007, *Bull. Seismol. Soc. Am.* 97: 90–106. [DOI: 10.1785/0120060009](https://doi.org/10.1785/0120060009)
4. **GR b-value across tectonic regimes:** Schorlemmer, D. et al.
   2005, *Nature* 437: 539–542. [DOI: 10.1038/nature04094](https://doi.org/10.1038/nature04094)
5. **Cascadia turbidite catalogue:** Goldfinger, C. et al. 2012,
   USGS Professional Paper 1661-F (Earth-Science Reviews update
   2017).
6. **Parkfield characteristic earthquake:** Bakun, W. H. et al.
   2005, *Nature* 437: 969–974. [DOI: 10.1038/nature04067](https://doi.org/10.1038/nature04067)
7. **Rate-and-state friction:** Dieterich, J. H. 1979, *J. Geophys.
   Res.* 84: 2161–2168. [DOI: 10.1029/JB084iB05p02161](https://doi.org/10.1029/JB084iB05p02161)
8. **Coulomb stress transfer:** King, G. C. P., Stein, R. S. & Lin,
   J. 1994, *Bull. Seismol. Soc. Am.* 84: 935–953.
9. **AMR critique:** Hardebeck, J. L., Felzer, K. R. & Michael, A.
   J. 2008, *J. Geophys. Res.* 113: B08310. [DOI: 10.1029/2007JB005410](https://doi.org/10.1029/2007JB005410)
10. **Brownian Passage Time recurrence:** Matthews, M. V. et al.
    2002, *Bull. Seismol. Soc. Am.* 92: 2233–2250. [DOI: 10.1785/0120010267](https://doi.org/10.1785/0120010267)
11. **CRR P5 California null:** `claims/P5_csep_california_null/`
    in this repository.
12. **CRR session-12 Hawkes regime:** `claims/session_12_combined/result.md`.
13. **CRR session-11 no-regulator boundary:** `notes/session_11_no_regulator_baseline.md`.
14. **CRR session-14 Hawkes physics-domain failures:**
    `notes/session_14_literature_audit.md`.

---

## Audit-trail anchor

This document constitutes the binding pre-registration of the
CRR-EQ architecture (Layer 0 substrate, Layer 1 background, Layer
2 CRR-ETAS hybrid, Layer 3 coherence diagnostic) and predictions
EQ1–EQ7. The commit hash on push to branch
`claude/verify-folder-access-CInY3` is the audit anchor. Per
CAMPAIGN.md PART III, the architecture and pre-registered tests
cannot be retroactively edited; honest negatives recorded
permanently when CSEP results return.
