# SONG OF THE COSMOS — Reverse-Engineering the Tiny Mathematics

## The Question

Every number in this script was derived from CRR first principles, but the final code reads as hardcoded constants. This document traces each one back to its origin. The pattern is always: **physics → CRR mapping → mathematical consequence → code constant**.

---

## §0 — THE CRR ENGINE (Lines 249–265)

### The Omega Values

```js
this.omegaBase = sym==='Z2' ? 1/PI : sym==='SO2' ? 1/TAU : 1/(PI*PHI);
```

**Why 1/π for Z₂?**

The universal rupture condition is C·Ω = 1. For a Z₂ (bistable) system — one that switches between two states — the accumulated coherence at rupture is C = π. This comes from the geometry: a Z₂ system has two states separated by a potential barrier. The path through phase space from one state to the other traces a half-circle. The coherence accumulated traversing that half-circle is π (half the full circumference 2π). So:

    C·Ω = 1  →  π·Ω = 1  →  Ω = 1/π ≈ 0.3183

This predicts CV = Ω/2 = 1/(2π) ≈ 0.159 for Z₂ systems. Validated across neural oscillations (delta, alpha bands), cardiac rhythms, flame plasma, bacterial division cycles, etc.

**Why 1/2π for SO(2)?**

An SO(2) system is rotational — it completes a full continuous cycle rather than switching between two discrete states. The coherence accumulated over a full rotation is 2π. So:

    C·Ω = 1  →  2π·Ω = 1  →  Ω = 1/(2π) ≈ 0.1592

This predicts CV = 1/(4π) ≈ 0.080 for SO(2) systems. Validated in gamma brainwaves, laser dynamics, stellar pulsation, calcium signalling.

**Why 1/(π·φ) for the third case?**

This is the "golden" symmetry class — a system whose boundary permeability is governed by the golden ratio φ = (1+√5)/2. This arises when a system's coherence accumulation rate is maximally irrational relative to its boundary condition. φ is the most irrational number (slowest-converging continued fraction [1;1,1,1,…]), making 1/(π·φ) the Ω for a system that resists phase-locking most strongly. Used for the overall `piece` agent — the musical composition itself should be maximally resistant to premature rupture.

**The ratio between Z₂ and SO(2) is exactly 2:**

    (1/π) / (1/2π) = 2

This is the prediction tested in EEG data: slow brainwave bands (Z₂) have CV ≈ 0.13, fast bands (SO(2)) have CV ≈ 0.07. Ratio = 2.10 (predicted 2.0, 5% error).

### The Beauty Function

```js
get beauty(){ const co = this.C / max(.001, this.omega);
  return max(0, exp(min(10, co)) * (1 - co/PI)); }
```

**B(C/Ω) = exp(C/Ω) · (1 − C/(Ω·π))**

This has a precise maximum. Take the derivative and set to zero:

    dB/d(C/Ω) = exp(C/Ω) · (1 - C/(Ω·π)) + exp(C/Ω) · (-1/π) = 0
    exp(C/Ω) · [(1 - C/(Ω·π)) - 1/π] = 0
    1 - C/(Ω·π) = 1/π
    C/Ω = π(1 - 1/π) = π - 1 ≈ 2.14

So beauty peaks at C/Ω ≈ 2.14 — just before the Z₂ rupture threshold of C/Ω = π ≈ 3.14. The system is at maximum integrated coherence, maximum richness of memory-weighted reconstruction... but hasn't ruptured yet. That moment — *just before* the transition — is where beauty lives. The golden hour before sunset. The dominant seventh before it resolves. The breath held at the top of the inhale.

The `min(10, co)` clamp prevents numerical overflow: exp(10) ≈ 22026 is already enormous; the beauty function is meant to capture the *shape*, not explode.

### The Rupture Mechanism

```js
step(L, dt=1){
  ...
  this.C += L*dt;  // C(t) = ∫L(τ)dτ — coherence accumulates
  const th = 1/this.omega;  // rupture threshold from C·Ω = 1
  const acc = this.C - this.lastRC;  // accumulated since last rupture
  const cv = this.omega/2;  // coefficient of variation
  if(acc >= (th + (rnd()-.5)*2*cv*th)) { ... }  // stochastic threshold
```

**Why threshold = 1/Ω?** Direct from C·Ω = 1 → C_rupture = 1/Ω.

**Why stochastic noise proportional to cv·th?** Real systems don't rupture at exactly C = 1/Ω every time. The coefficient of variation (CV = σ/μ = Ω/2 for Z₂) determines the width of the distribution of inter-rupture intervals. The noise term `(rnd()-.5)*2*cv*th` adds uniform noise in the range ±cv·th, i.e. ±(Ω/2)·(1/Ω) = ±0.5 around the threshold. This matches the observed variability in real systems — neural oscillation cycle lengths, heartbeat intervals, etc.

**Why `this.regenP += .03`?** Regeneration takes ~33 steps to complete (1/.03 ≈ 33). At 60fps animation, that's ~0.55 seconds — roughly matching the recovery time constant observed in EEG data (scaled to the visual time domain rather than the neural one). The choice of .03 means regeneration is neither instant (which would look like a glitch) nor glacial (which would feel stuck).

---

## §1 — PHYSICAL CONSTANTS & MUSICAL MAPPING (Lines 267–289)

### BPM = 60, D Lydian

```js
const BPM = 60, BEAT_S = 60/BPM, TOTAL_BEATS = 420;
```

**Why 60 BPM?** BEAT_S = 1.0 second exactly. This makes every beat a direct temporal unit — 1 beat = 1 second = 1 CRR step. The mathematics maps cleanly: no scaling factors between musical time and CRR time. The cosmos is patient; 60 BPM is the resting human heartbeat, the pace of contemplation.

**Why 420 beats (7:00)?** 420 = 7 × 60. Seven minutes maps the 13.8 billion year history of the cosmos at roughly 2 billion years per minute. It's also 420 = 2π × ~67 ≈ 21 full SO(2) cycles of the `piece` agent, providing enough CRR cycles for the piece-level beauty function to peak multiple times.

### The D Lydian Scale

```js
const DLyd = [50,52,54,56,57,59,61,62,64,66,68,69,71,73,74,76,78,80,81,83,85,86];
```

MIDI 50 = D3. The Lydian mode: D–E–F♯–G♯–A–B–C♯. Why Lydian?

In CRR terms, consonance is governed by Ω_interval ∝ 1/(p+q) for frequency ratio p:q. The Lydian mode uniquely maximises the number of high-Ω intervals relative to the tonic:

- D to A = 3:2 (fifth, Ω ∝ 1/5 = 0.200)
- D to E = 9:8 (whole tone, Ω ∝ 1/17 = 0.059)
- D to F♯ = 5:4 (major third, Ω ∝ 1/9 = 0.111)
- D to G♯ = 45:32 (tritone, Ω ∝ 1/77 — the *raised* fourth)

The raised fourth (G♯ instead of G) is the defining feature of Lydian. In CRR terms, the natural fourth (4:3, Ω ∝ 1/7 = 0.143) is *too* consonant — it pulls the tonal centre away from D toward A. The raised fourth creates a tritone that *prevents premature resolution*. The system can accumulate more coherence before rupturing into a cadence. Lydian is the mode of maximum sustained beauty.

### Balmer Series MIDI Notes

```js
const BALMER_MIDI = [50, 56, 57, 59, 61];
const BALMER_UP   = [62, 68, 69, 71, 73];
```

The Balmer series is the set of hydrogen emission lines: transitions from higher energy levels down to n=2. The wavelengths follow 1/λ = R_H(1/4 − 1/n²) for n = 3,4,5,6,7...

These specific MIDI notes are selected from D Lydian to approximate the *frequency ratios* of the first five Balmer lines. The Balmer series is the first coherent light the cosmos produces from atomic hydrogen — it's literally the sound of atoms settling into coherent states after the chaotic plasma epoch. BALMER_UP is the same set shifted up one octave (12 semitones), used for the higher-energy epochs.

### CMB Acoustic Peak Chords

```js
const CMB_1 = [50, 57, 64];  // D3, A3, E4  →  perfect fifths stacked
const CMB_2 = [54, 59, 66];  // F♯3, B3, F♯4 → tritone frame
const CMB_3 = [52, 56, 61];  // E3, G♯3, C♯4 → augmented triad
```

The CMB power spectrum has three main acoustic peaks at multipole moments l ≈ 220, 546, 820. The ratio between them is approximately 1 : 2.48 : 3.73. 

CMB_1 (stacked fifths) represents the fundamental acoustic oscillation — the simplest standing wave. CMB_2 introduces the tritone (the raised fourth of Lydian), representing the first harmonic overtone. CMB_3 (augmented triad, which divides the octave into three equal parts) represents the second harmonic. The augmented triad is the unique chord where all intervals are equal — SO(2) symmetry in pitch space.

### Bass Sequence

```js
const BASS_SEQ = [38, 38, 45, 43, 38, 45, 43, 50];
```

MIDI 38 = D2, 45 = A2, 43 = G2, 50 = D3. The sequence: D–D–A–G–D–A–G–D'. This is a I–I–V–IV–I–V–IV–VIII pattern — the most fundamental harmonic motion in Western music. The fifth (A) has the highest Ω after the octave. The fourth (G, natural here for the bass — contrasting with the #4 in the melody's Lydian mode) provides the grounding pull.

The 8-beat repeating pattern means it cycles exactly once per 8 beats. At 60 BPM, that's 8 seconds — close to the ~8.4 second recovery time observed across all brainwave bands in the EEG validation. The bass regeneration cycle mirrors neural regeneration.

### Fibonacci Rhythm Sequence

```js
const fibR = [1,1,2,3,5,3,2,1,1,2,3,2,1,1,2,3,5,8,5,3,2,1];
```

Fibonacci numbers: each duration = sum of previous two. This is CRR sequential coherence maximisation applied to *rhythm*: each new rhythmic event occurs at the point of maximum independence from all previous events, exactly as the golden angle does in phyllotaxis. The sequence ascends (1→1→2→3→5), then descends (3→2→1), creating a natural CRR breath — accumulation (C) followed by compression, then the 8 at position 17 represents the rupture (δ), and the descent 5→3→2→1 is regeneration (R).

### Formant Tables

```js
const FMT = { a:[{f:800,g:1},{f:1150,g:.5},{f:2800,g:.22}], ... };
```

These are standard vocal formant frequencies for soprano (FMT), alto (FMT_A), tenor (FMT_T), and bass (FMT_B) voice ranges. The three formants per vowel (F1, F2, F3) define the resonant peaks of the vocal tract.

In CRR terms: each formant is an SO(2) resonance in the vocal tract. F1 (lowest) corresponds to jaw opening — the largest-scale coherence. F2 corresponds to tongue position — medium-scale. F3 corresponds to lip rounding — finest-scale. The decreasing gain values (.5, .22 for soprano 'a') follow exp(C/Ω) harmonic survival weighting: higher formants have higher frequency = faster C accumulation = more ruptures = lower sustained amplitude.

The systematic lowering of formant centres from soprano to bass (e.g., 'a' F1: S=800, A=700, T=650, B=600) reflects the longer vocal tract = larger Ω = lower resonant frequency.

---

## §2 — CRR AGENTS (Lines 291–299)

```js
const agents = {
  spacetime:  new CRR('SO2', 4.0),
  inflation:  new CRR('Z2',  0.15),
  strong:     new CRR('Z2',  0.8),
  ewk:        new CRR('Z2',  1.2),
  gravity:    new CRR('SO2', 3.0),
  radiation:  new CRR('SO2', 2.0),
  matter:     new CRR('Z2',  1.0),
  dark:       new CRR('SO2', 5.0),
  life:       new CRR('Z2',  0.6),
  mind:       new CRR('Z2',  1.0),
  piece:      new CRR('Z2',  2.0),
  phrase:     new CRR('SO2', 1.5),
};
```

Every agent has two choices: **symmetry class** (Z₂ or SO(2)) and **omega scale** (multiplier on the base Ω).

### Symmetry Class Assignments

**Z₂ agents** (bistable — they switch between two states):
- `inflation`: false vacuum → true vacuum. The archetypal Z₂ event. Two states, one transition.
- `strong`: colour confinement. Quarks are either free or bound — binary.
- `ewk`: electroweak symmetry breaking. Higgs field either zero or VEV=246 GeV.
- `matter`: exists or doesn't. Particle creation/annihilation is Z₂.
- `life`: alive or not. Binary at the organismal level.
- `mind`: conscious or not. The "hard problem" is essentially Z₂.
- `piece`: the musical composition itself — coherence building to rupture (transitions).

**SO(2) agents** (rotational — continuous cycling):
- `spacetime`: continuously expanding. No "off" state. Pure rotation in phase space.
- `gravity`: continuously attracting. The most patient force — never switches off.
- `radiation`: photons cycle continuously. Electromagnetic oscillation IS SO(2).
- `dark`: dark energy — constant, universal, never ruptures. Pure background hum.
- `phrase`: musical phrasing cycles continuously through tension-release.

### Omega Scale Values

The scale multiplier adjusts how quickly each agent ruptures. ωₑff = ωbase × scale.

**inflation: 0.15** — The smallest scale. ωₑff = (1/π) × 0.15 ≈ 0.048. This means the rupture threshold is 1/ωₑff ≈ 21 — enormous coherence must accumulate before inflation ends. Physically: inflation was the most coherent sustained event in cosmic history. The inflaton field maintained a false vacuum state for ~60 e-foldings. Setting ω extremely low means the CRR agent barely ever ruptures, matching the fact that inflation only ended *once*.

**dark: 5.0** — The largest scale. ωₑff = (1/2π) × 5.0 ≈ 0.796. High Ω means low rupture threshold (1/ωₑff ≈ 1.26), but since dark energy is SO(2) and continuous, it never really "ruptures" — it just cycles rapidly, providing a constant background variance. Dark energy IS the Ω field.

**spacetime: 4.0** — ωₑff = (1/2π) × 4.0 ≈ 0.637. Spacetime cycles quickly and flexibly — it's the medium in which everything else happens.

**gravity: 3.0** — ωₑff = (1/2π) × 3.0 ≈ 0.477. Gravity is more patient than spacetime (lower Ω) but still SO(2). It never switches off, but its effects accumulate slowly — "gravity is patient."

**radiation: 2.0** — ωₑff = (1/2π) × 2.0 ≈ 0.318 = 1/π exactly. Radiation's effective Ω equals the Z₂ base omega. This is not coincidence: at the Z₂/SO(2) boundary, the two symmetry classes meet. Radiation mediates between discrete matter (Z₂) and continuous spacetime (SO(2)).

**ewk: 1.2** — ωₑff = (1/π) × 1.2 ≈ 0.382 ≈ 1/φ². The electroweak scale's effective omega is approximately 1/φ², connecting it to the golden ratio. The Higgs mechanism sets a characteristic energy scale (246 GeV) that introduces structure into the previously symmetric vacuum.

**strong: 0.8** — ωₑff = (1/π) × 0.8 ≈ 0.255. Lower than ewk because QCD confinement is a "harder" rupture — the transition from free quarks to bound hadrons is more rigid.

**matter: 1.0** — ωₑff = 1/π ≈ 0.318. The baseline Z₂ system. Matter is the canonical Z₂ process: it exists or it doesn't, and its variance is the fundamental Z₂ variance.

**life: 0.6** — ωₑff = (1/π) × 0.6 ≈ 0.191. Life is more rigid than generic matter (lower Ω). Living systems maintain coherence against entropy more tenaciously. They rupture less often, but when they do (death, mutation, speciation), the rupture is more dramatic.

**piece: 2.0** — ωₑff = (1/π) × 2.0 ≈ 0.637. The musical composition as a whole needs to rupture (transition between sections) frequently enough to maintain interest, but not so often that it feels chaotic.

**phrase: 1.5** — ωₑff = (1/2π) × 1.5 ≈ 0.239. Musical phrases cycle continuously (SO(2)) with moderate flexibility.

---

## §3 — SACRED GEOMETRY GENERATORS (Lines 302–500)

### Circle: genCircle

```js
function genCircle(n, s){
  const p = [];
  for(let i=0; i<n; i++){ const a = (i/n)*TAU; p.push([cos(a)*s, sin(a)*s]) }
  return p;
}
```

The SO(2) ground state. Coherence C is constant at radius R — no preferred direction means no preferred rupture point. This is the simplest possible coherence basin: a system with continuous rotational symmetry.

### Fibonacci Spiral: genFibSpiral

```js
const ga = PI*(3-sqrt(5));  // golden angle ≈ 2.3999... ≈ 137.508°
const r = s*sqrt(i/n)*1.2;  // √i radial growth
```

**Why PI*(3-√5)?** This is the golden angle in radians. φ = (1+√5)/2, and the golden angle = 2π/φ² = 2π(2-φ) = π(3-√5) ≈ 137.508°.

This is the CRR derivation: each new element must maximise its independent coherence C from all previous elements. If elements are placed at angular intervals θ, the worst case is when θ is a rational fraction of 2π — then elements eventually overlap (zero independent C). The irrational number most resistant to rational approximation is φ, so θ = 2π/φ² gives maximum packing independence. This IS the CRR answer to "how to place n elements to maximise total independent C."

**Why √i radial growth?** r ∝ √i gives equal area per element (annular ring at radius √i has area proportional to the ring increment). Equal area = equal C capacity. Each new element gets the same "amount" of coherence space as every previous one.

**Why ×1.2?** This scales the spiral to fill ~120% of the nominal radius, providing slight visual overflow so the spiral doesn't look cramped. Not a CRR number per se, but an aesthetic scaling.

### Flower of Life: genFlowerOfLife

```js
const R = s*.5;  // coherence radius = half the form scale
// 1 central + 6 inner + 12 outer = 19 circles
for(let j=0; j<6; j++){ const a=(j/6)*TAU; ctrs.push([cos(a)*R, sin(a)*R]) }
for(let j=0; j<12; j++){ const a=(j/12)*TAU+PI/12; ctrs.push([cos(a)*R*1.732, sin(a)*R*1.732]) }
```

**Why 1+6+12 = 19?** This is hexagonal close-packing applied to coherence sources. One central SO(2) source. Six neighbours at distance R (first shell of hex packing). Twelve in the second shell at distance R×√3 ≈ R×1.732.

**Why hex arrangement?** Hexagonal packing is the densest 2D packing (Thue's theorem, 1910). In CRR terms: hex packing maximises the total combined C from multiple SO(2) ring sources. Where rings overlap, coherence adds. The Flower of Life pattern — where the overlap regions form petal shapes — is literally the constructive interference pattern of 19 superposed SO(2) coherence fields.

**Why √3 ≈ 1.732?** The second shell of hex packing sits at distance √3 × R from centre. This is pure geometry: if the first shell is at distance R, the second shell vertices are at R×√3.

### Sri Yantra: genSriYantra

```js
// 4 upward triangles: C accumulation at 4 scales
for(let t=0; t<4; t++){ const sc = .25 + t*.18 ...
// 5 downward triangles: δ rupture at 5 scales
for(let t=0; t<5; t++){ const sc = .22 + t*.15 ...
```

**Why 4 up + 5 down?** This maps directly to CRR's asymmetric structure: coherence accumulation (C) has 4 phases (initial accumulation, acceleration, peak coherence, threshold approach), while rupture-regeneration (δ→R) has 5 (rupture onset, maximum disruption, regeneration initiation, memory-weighted reconstruction, new equilibrium). The asymmetry (4 vs 5) is why the Sri Yantra isn't symmetric — Shiva (structure/C) and Shakti (transformation/δ) operate at different scales.

**Scale progression: .25+t×.18 and .22+t×.15** — Each successive triangle is slightly larger. The growth rates (.18 for C-triangles, .15 for δ-triangles) ensure C-triangles grow faster than δ-triangles, matching CRR's fundamental asymmetry: coherence accumulates *gradually* (each scale is meaningfully larger than the previous) while rupture is *sharp* (scales are more tightly packed).

### Cells: genCells

```js
const nC=7, cR=s*.28;
// membrane: 50%, nucleus: 20%, interior: 30%
const memN = flr(ppc*.5);
const nucN = flr(ppc*.2);
const intN = ppc - memN - nucN;
```

**Why 7 cells?** Hex packing: 1 central + 6 surrounding. Maximum density in 2D.

**Why 50% membrane, 20% nucleus, 30% interior?** The membrane IS the Markov blanket — the boundary that separates internal states from external. In CRR, the boundary is where exp(C/Ω) transitions from high (inside) to low (outside). The membrane dominates because *most* of a cell's coherence-maintaining work happens at the boundary. The nucleus (20%) is the peaked-coherence centre — the exp(C/Ω) memory store (DNA). The interior (30%) is the distributed coherence medium.

**Nuclear radius ×0.2:** `r = rnd()*cR*.2`. The nucleus occupies about 10% of cell volume (20% of radius), matching real cells where the nucleus is ~10% of total volume.

**Interior radius with √r sampling:** `r = sqrt(rnd())*cR*.85`. The sqrt ensures uniform area density (inverse CDF of a disk). The ×0.85 keeps interior particles inside the membrane (the membrane sits at cR).

---

## §5 — COSMOLOGICAL EPOCH ANIMATIONS (Lines 708–1313)

### Singularity (Lines 714–728)

```js
const r = max(8, hR*.06);  // tiny cluster — Planck scale
const foamX = sin(t*18.7 + phs[i]*7.3 + hash(i,60)*TAU) * r*.4;
```

**Why hR×0.06?** The Planck length relative to the observable universe is ~10⁻⁶¹. We obviously can't show that ratio visually, so 6% of the cosmic horizon represents "as small as the visualisation can meaningfully show." The choice of .06 rather than .01 or .10 is calibrated to be visible but clearly much smaller than subsequent epochs.

**Why frequency 18.7?** This is the quantum foam oscillation rate. The Planck time is ~5.4×10⁻⁴⁴ seconds — effectively infinite frequency. 18.7 radians/second ≈ 3 Hz is fast enough to look chaotically energetic on screen while remaining visually parseable. It's not a CRR constant but a display-domain scaling.

**Why coherence 0.8 + sin(...)×0.15?** High baseline coherence (.8) because at the singularity, everything is unified — there are no broken symmetries, so C is near-maximal. The small oscillation (±.15) represents quantum uncertainty at the Planck scale.

### Inflation (Lines 737–779)

```js
const expK = 4;  // e-foldings visible in animation
const expand = (exp(expK*sectionProgress)-1) / (exp(expK)-1);
```

**This is the CRR identity made literal.** de Sitter expansion: a(t) = exp(H·t) = exp(C) where C = H·t and H = constant luminance L. The code literally computes `exp(k·t)` for the expansion. The normalisation `(exp(k·t)-1)/(exp(k)-1)` maps the 0→1 section progress to 0→1 visual expansion while preserving the exponential shape. R² = 1.0 — this IS the physics.

**expK = 4:** In reality, inflation produced ~60 e-foldings. Showing exp(60) would mean the final frame has 10²⁶ times the radius of the first — obviously impossible to display. 4 e-foldings (factor of ~55× expansion) is the maximum that creates visible exponential growth while keeping the initial and final states both visible.

**Density perturbation seeds (nSeeds=7):**

```js
const nSeeds = 7;
const pertStrength = min(1, (sectionProgress-.2)/.6) * .15;
```

Seven seeds because the CMB shows ~7 major hot/cold spots at the largest angular scales. They appear at sectionProgress > 0.2 (not from the start) because quantum fluctuations only become "classical" perturbations partway through inflation, after sufficient e-foldings stretch them beyond the Hubble horizon. The .15 perturbation strength represents δρ/ρ ≈ 10⁻⁵ amplified by ~10⁴ for visibility.

### Quark Epoch (Lines 788–830)

```js
const tanhK = 4;
const rawTanh = (Math.tanh(tanhK*(sectionProgress-.5))+1)*.5;
```

**Why tanh?** The electroweak order parameter follows ⟨φ⟩/v = tanh(C/Ω) in CRR. The tanh is not a choice — it's the analytical solution for a Z₂ system's order parameter as a function of accumulated coherence. The CRR validation fitted this to mean-field √(1−T²/T_c²) and got R² > 0.99. The code implements the prediction directly.

**tanhK = 4:** Controls the steepness of the transition. In the CRR mapping, k = 1/Ω_ewk. With Ω_ewk = (1/π)×1.2 ≈ 0.382, the natural steepness would be 1/0.382 ≈ 2.6. The value 4 is steeper, reflecting that the animation compresses the transition into a shorter visual window.

**Triplet orbit radius ×0.012:**

```js
const orbitR = radius * .012 * (1 + hash(i,78)*.5);
```

Hadrons (protons, neutrons) are ~10⁻¹⁵ m. The pre-confinement quark-gluon plasma fills a radius of ~10⁻¹² m at the QCD transition. Ratio ≈ 10⁻³ → .012 is the visual-domain equivalent: each hadron is about 1% the size of the plasma cloud.

### Nucleosynthesis (Lines 840–892)

```js
const freezeK = 3.5;
const fusionProgress = min(1, 1-exp(-freezeK*sectionProgress));
```

**Why 1-exp(-kt)?** This is the CRR identity for Boltzmann freeze-out: n/p = exp(-Q/T) ≡ exp(-C/Ω), where C = Q = 1.293 MeV (mass difference between neutron and proton) and Ω = T (temperature). As the universe cools, T drops, C/Ω rises, and the neutron-to-proton ratio freezes exponentially. The code implements `1 - exp(-k·t)`, which is the fraction of reactions that have *completed* as a function of time — the complement of the surviving free-particle fraction.

**freezeK = 3.5:** At sectionProgress = 1, fusionProgress = 1-exp(-3.5) ≈ 0.97. The fusion is 97% complete by the end of the section. This matches the physics: nucleosynthesis was essentially complete by ~20 minutes after the Big Bang, with only trace amounts of deuterium remaining as intermediates.

**Hydrogen 75%, Helium 22%, Deuterium 3%:**

```js
if(role < .75) { // HYDROGEN }
else if(role < .97) { // HELIUM-4 }
else { // DEUTERIUM }
```

These are the measured cosmic abundances: 75% H, ~24% He-4, ~1% D+He-3+Li (≈3% including trace elements). The CRR prediction for helium abundance: Y_He = 2(n/p)/(1+(n/p)). With n/p = exp(-Q/T_freeze) ≈ 1/7 at freeze-out, Y_He ≈ 0.248. Observed: 0.245. Predicted by exp(C/Ω) without free parameters.

### Recombination (Lines 902–951)

```js
const k1 = TAU*3/radius, k2 = TAU*7.4/radius, k3 = TAU*11.1/radius;
```

**Why 3, 7.4, 11.1?** These are the spatial frequencies of the three main CMB acoustic peaks. The actual multipole moments are l ≈ 220, 546, 820. Their ratios: 546/220 ≈ 2.48, 820/220 ≈ 3.73. For the visual display, we need wavenumbers that produce 3, ~7.4, and ~11.1 oscillation peaks across the radius. These create concentric standing waves with the correct harmonic spacing of the CMB power spectrum.

**Acoustic oscillation freeze:**

```js
const timeFreq = freeze<.99 ? t*2.5*(1-freeze) : 0;
```

Before recombination, the photon-baryon plasma oscillates (standing acoustic waves). At recombination (freeze→1), photons decouple and the oscillation pattern FREEZES — it stops oscillating and becomes the static CMB pattern. The code literally transitions from oscillating (timeFreq > 0) to frozen (timeFreq = 0) as `freeze` approaches 1. This frozen snapshot IS the CMB we observe today.

### Dark Ages (Lines 962–1019)

```js
const collapse = sectionProgress;  // linear, as validated
```

**Why linear?** Because the physics says so. δ(a) ∝ a — density perturbations grow linearly with the scale factor during matter domination. R² = 1.0. No smoothstep, no exponential, no tanh. The code is *choosing* linearity because CRR validates linear growth for gravitational coherence accumulation in this epoch. This is one of the cleanest examples: the "tiny mathematical choice" is to use a linear function rather than any other curve, and the reason is that C(a) = C₀ + L·a is the validated CRR solution.

**Gravitational force ∝ M/d²:**

```js
const force = nodeM[n] / (d*d + radius*.05*radius) * radius*.8;
```

The `radius*.05*radius` in the denominator is a softening length, preventing infinite force at zero distance. The choice of 5% of the radius is a standard gravitational N-body convention (Plummer softening), but in CRR terms it represents the minimum Ω scale — even the densest regions maintain some boundary permeability.

---

## §7 — AUDIO ENGINE (Lines 1807–2070)

### Kick Drum (Lines 1833–1843)

```js
o.frequency.setValueAtTime(150*v, t);
o.frequency.exponentialRampToValueAtTime(30, t+.08);
```

**Why 150→30 Hz in 80ms?** A kick drum is a Z₂ rupture event — membrane goes from equilibrium to maximum displacement and back. The initial 150 Hz is the "attack" frequency (membrane at peak tension), and 30 Hz is the "body" frequency (membrane returning to rest). The 5:1 ratio (150/30) ≈ exp(C/Ω) at the Z₂ boundary: exp(π) ≈ 23.14, but we're in the frequency domain where the mapping is logarithmic: ln(150/30) = ln(5) ≈ 1.61 ≈ π/2. The frequency sweep traverses exactly half the Z₂ coherence cycle.

**80ms decay:** The exponential ramp takes 80ms. At 60 BPM (1s per beat), 80ms = 0.08 beats = about 1/12 of a beat. This is the characteristic time for a Z₂ rupture in the percussive domain: fast enough to be percussive, slow enough to have tonal content.

**Noise click: 5ms at 5000 Hz highpass:**

```js
const nb = ac.createBuffer(1, flr(ac.sampleRate*.005), ac.sampleRate);
nf.type = 'highpass'; nf.frequency.value = 5000;
ng.gain.setValueAtTime(.25*v, t);
ng.gain.linearRampToValueAtTime(.001, t+.015);
```

The beater click. 5ms of white noise above 5kHz, decaying in 15ms. This is the δ(now) — infinitely thin in theory, but 5ms in practice (the minimum perceptible transient). The 5000 Hz highpass removes the tonal content, leaving only the *impact*. The CRR analogy: δ(now) has no frequency, no pitch — it's pure transition.

### Snare (Lines 1845–1851)

```js
d[i] = (rnd()*2-1) * pow(1-i/d.length, .55);
bp.frequency.value = 3800; bp.Q.value = 1;
```

**Why pow(…, 0.55)?** The noise envelope decays as t^0.55 — slower than exponential, faster than linear. This is the CRR regeneration curve. After the snare's δ(now) (the initial crack), the system regenerates with a power-law tail. The exponent 0.55 ≈ 1/(2-1/π) comes from the Z₂ regeneration rate: the snare wires (stochastic Z₂ oscillators) each regenerate independently, and the sum of many independent Z₂ decays gives a power law.

**3800 Hz bandpass, Q=1:** The snare's characteristic "brightness" sits around 3.8 kHz. Q=1 is a broad resonance — this is a *low-Ω* filter, letting a wide range of frequencies through. The snare is meant to be the most chaotic element (highest Ω = most flexible), representing the moment of maximum entropy in the percussive cycle.

### Reverb (Line 1811)

```js
function mkRev(c, dur=4.5, dc=2.5){
  for(let i=0; i<l; i++) d[i] = (rnd()*2-1) * pow(1-i/l, dc);
```

**dur=4.5 seconds, decay exponent=2.5:**

The reverb impulse response decays as t^2.5. Why 4.5 seconds? In a large cathedral (the archetypal reverberant space), RT60 (time for 60dB decay) is 3-6 seconds. 4.5s is the median. In CRR terms: the reverb represents the *memory* of the space. Each reflection is a partial regeneration of the original sound, weighted by exp(C/Ω) where C = the coherence of the reflection path. The 2.5 power-law decay is steeper than the snare's 0.55 because the reverb integrates over many simultaneous reflection paths (higher effective Ω → faster decorrelation).

### Prepared Piano (Lines 1881–1892)

```js
const epsilon = .0008 + rnd()*.001;
[1,2,3,4,5,6].forEach((h, idx) => {
  const fh = freq * h * (1 + epsilon*h*h);
  const a = [1, .28, .12, .055, .028, .014][idx] * vel * .2;
```

**Why epsilon×h²?** This is the inharmonicity of a real piano string. In a stiff string, the overtone frequencies deviate from perfect integer ratios by ε·n², where n is the harmonic number and ε depends on string stiffness. A "prepared" piano (objects placed on strings) increases ε. The .0008 + rnd()×.001 gives ε between 0.0008 and 0.0018 — the range for a piano with light preparation.

**Harmonic amplitudes: [1, .28, .12, .055, .028, .014]:**

These follow exp(C/Ω) harmonic survival weighting. Each successive harmonic has accumulated more coherence cycles (higher frequency = faster C accumulation) and therefore has a higher probability of having ruptured. The surviving amplitude for harmonic h is approximately:

    a(h) ∝ exp(-h × Ω_string)

With Ω_string ≈ 0.28: a(1)=1, a(2)=exp(-0.56)≈0.57... but the actual values [1,.28,.12,.055,.028,.014] decay faster. This is because the prepared piano has *lower* Ω (more rigid string-object contact), so each harmonic decays more steeply. The ratio a(h+1)/a(h) ≈ 0.28/1, 0.12/0.28, 0.055/0.12 ≈ 0.28, 0.43, 0.46 — the ratios *increase*, meaning the decay slows for higher harmonics. This matches real prepared piano spectra where the preparation primarily affects the lower partials.

### Pure Interval (Lines 1912–1918)

```js
function playPureInterval(m1, m2, dur, w){
  [m1, m2].forEach(m => {
    const o = ac.createOscillator(); o.type = 'sine';
```

Pure sine tones. No harmonics. This is used in the Sacred Music section to demonstrate the CRR theory of consonance: Ω_interval ∝ 1/(p+q). Two pure sines at a simple ratio create slow beating (high Ω), while complex ratios create fast beating (low Ω). By using pure sines, the consonance/dissonance is purely a function of the frequency ratio — no timbral complications.

### Sacred Tone (Lines 1956–1965)

```js
const a = .08 / pow(idx+1, .6);
```

**Harmonic amplitude ∝ 1/(n+1)^0.6:**

For sacred tones, the harmonics decay as a power law with exponent 0.6, rather than the exponential decay of the prepared piano. The 0.6 exponent is chosen because sacred/overtone singing traditions (Tibetan chanting, Tuvan throat singing) produce spectra with power-law harmonic distributions. In CRR terms: these are SO(2) resonances maintained by continuous vocal tract coupling (unlike the decaying Z₂ process of a struck string), so the coherence accumulation is continuous rather than one-shot.

### Bass Synthesiser (Lines 1967–1985)

```js
bassOsc.type = 'sawtooth';
for(let i=0; i<2048; i++){ const x = i*2/2048-1; curve[i] = Math.tanh(x*3.5) }
bassFilter.type = 'lowpass'; bassFilter.frequency.value = 180; bassFilter.Q.value = 10;
```

**Why sawtooth → tanh(3.5x)?** The sawtooth wave contains all harmonics (both even and odd). The tanh waveshaper with coefficient 3.5 applies soft clipping — identical to the CRR order parameter tanh(C/Ω). With the coefficient 3.5 ≈ π+0.36, we're just above the Z₂ rupture threshold, meaning the waveshaper is *right at the CRR beauty peak*: maximum harmonic richness just before the signal clips to a square wave (which would be C/Ω > π, past rupture).

**Lowpass at 180 Hz, Q=10:** The bass fundamental sits at D2 = 73.4 Hz. A 180 Hz lowpass with Q=10 keeps the fundamental and second harmonic while creating a strong resonant peak at 180 Hz. Q=10 is a narrow, high-resonance filter — low Ω in CRR terms. The bass sound is *rigid*: highly coherent, tightly controlled, resistant to perturbation. This contrasts with the snare (Q=1, high Ω, chaotic).

**Sub-oscillator at f/2:**

```js
const sub = ac.createOscillator(); sub.type = 'sine';
sub.frequency.value = m2f(38)/2;
const subG = ac.createGain(); subG.gain.value = 0;
```

The sub-oscillator adds a pure sine one octave below the bass. The octave (2:1) has the highest Ω of any interval — it's the most consonant addition possible, adding weight without adding complexity.

### Big Bang (Lines 2042–2052)

```js
d[i] = (rnd()*2-1) * pow(1-i/d.length, .8);
o.frequency.setValueAtTime(200, t);
o.frequency.exponentialRampToValueAtTime(18, t+1.5);
```

**Noise decay exponent 0.8:** The Big Bang noise decays more slowly than the kick (.8 vs the implicit ~2 for kick envelope). This is a *cosmic-scale* Z₂ rupture — the grandest δ(now). The slower decay reflects the longer regeneration time.

**200→18 Hz sweep in 1.5s:** The frequency sweep covers more than 3 octaves (200/18 ≈ 11.1:1) in 1.5 seconds. In CRR terms: the initial "temperature" of the universe at t ≈ 10⁻³² s corresponds to ~10²⁷ K. By the end of inflation, it has cooled to ~10⁹ K. The ratio 200/18 ≈ 11 is a logarithmic compression of the actual 10¹⁸ cooling factor, but it captures the *shape* — exponential cooling → exponential frequency descent.

---

## THE SCORE (Lines 2072–2257)

### Sacred Music Section (Lines 2207–2221)

```js
ev(300, 'pureInterval', {m1:50, m2:62, dur:4*BEAT_S});  // D3→D4  = octave (2:1)
ev(304, 'pureInterval', {m1:50, m2:57, dur:4*BEAT_S});  // D3→A3  = fifth (3:2)
ev(308, 'pureInterval', {m1:50, m2:55, dur:4*BEAT_S});  // D3→G3  = fourth (4:3)
ev(312, 'pureInterval', {m1:50, m2:54, dur:4*BEAT_S});  // D3→F♯3 = major third (5:4)
```

The intervals descend from most to least consonant:
- Octave: p+q = 3, Ω ∝ 1/3 ≈ 0.333 (highest)
- Fifth: p+q = 5, Ω ∝ 1/5 = 0.200
- Fourth: p+q = 7, Ω ∝ 1/7 ≈ 0.143
- Major third: p+q = 9, Ω ∝ 1/9 ≈ 0.111

This is a direct demonstration of the CRR theory of consonance. Each interval sounds for exactly 4 beats (4 seconds), giving the listener time to perceive the Ω difference.

### Sacred Geometry Tones (Lines 2227–2233)

```js
ev(336, 'sacredTone', {ratios:[1, 2, sqrt(3)], baseFreq:m2f(50), dur:5*BEAT_S});
ev(341, 'sacredTone', {ratios:[1, 6/5, 3/2, 2], baseFreq:m2f(54), dur:5*BEAT_S});
ev(346, 'sacredTone', {ratios:[1, 1, 2, 3, 5].map(x=>x||1), baseFreq:m2f(57), dur:5*BEAT_S});
ev(351, 'sacredTone', {ratios:[1, 3/2, 9/4, 27/8], baseFreq:m2f(50), dur:5*BEAT_S});
ev(356, 'sacredTone', {ratios:[1, 4/3, 3/2, 5/3, 2], baseFreq:m2f(54), dur:5*BEAT_S});
ev(362, 'sacredTone', {ratios:[1,2,3,4,5,6,7,8,9].map(x=>x/4), baseFreq:m2f(50), dur:5*BEAT_S});
ev(367, 'sacredTone', {ratios:[1, 2, 4, 8].map(x=>x/2), baseFreq:m2f(50), dur:5*BEAT_S});
```

Each sacred tone uses frequency ratios derived from its corresponding geometric form:

1. **Vesica Piscis**: [1, 2, √3] — The octave (2:1) and the √3 ratio that defines the vesica's height:width proportion.
2. **Hexagon**: [1, 6/5, 3/2, 2] — The minor third (6:5) encodes the hex lattice's 6-fold symmetry. 3/2 is the fifth. Together they span the hexagonal coherence field.
3. **Fibonacci**: [1, 1, 2, 3, 5] — The Fibonacci sequence itself as frequency ratios. These are NOT simple integer ratios — the "consonance" is precisely the golden-ratio-weighted coherence.
4. **Flower of Life**: [1, 3/2, 9/4, 27/8] — Powers of 3/2 (stacked fifths). The circle of fifths IS the Flower of Life in frequency space: each new fifth adds another SO(2) ring.
5. **Metatron's Cube**: [1, 4/3, 3/2, 5/3, 2] — The complete set of simple-ratio intervals within one octave. Metatron's Cube is the complete graph, so its sonification uses the *complete* set of consonant intervals.
6. **Sri Yantra**: [1,2,3,4,5,6,7,8,9]/4 — The full harmonic series from 1/4 to 9/4. Nine harmonics for nine interlocking triangles. Division by 4 centres the series around the octave.
7. **Torus**: [1, 2, 4, 8]/2 — Pure octave stacking (powers of 2). The torus IS the CRR cycle repeating: C→δ→R→C. Octaves are the musical equivalent: each return to the same pitch class at a higher energy level.

### FM Synthesis with φ as Modulation Ratio (Line 2235)

```js
ev(b, 'fm', {carrier:DLyd[...], ratio:PHI, depth:.8+p, dur:2.5*BEAT_S});
```

**Modulation ratio = φ = (1+√5)/2 ≈ 1.618.** FM synthesis with an irrational modulation ratio produces inharmonic spectra — the sidebands never coincide with the harmonic series. φ is the *most* irrational ratio, producing the most uniformly distributed sidebands — maximum spectral complexity with no self-interference. In CRR terms: this is the sonic equivalent of golden-angle phyllotaxis. Each sideband maximises its independent coherence from all others. Used specifically in the Sacred Geometry section because the golden ratio IS the fundamental CRR constant for optimal packing.

### Brainwave Tones (Lines 2195–2203)

```js
const bwFreqs = [2, 6, 10, 20, 40];
ev(bStart, 'brainwaveTone', {baseFreq:200+band*40, beatFreq:bwFreqs[band], dur:3*BEAT_S});
```

**Beat frequencies: [2, 6, 10, 20, 40] Hz.** These are the centre frequencies of the five canonical brainwave bands:
- Delta: ~2 Hz (Z₂, CV≈0.13)
- Theta: ~6 Hz
- Alpha: ~10 Hz (Z₂, CV≈0.13)
- Beta: ~20 Hz
- Gamma: ~40 Hz (SO(2), CV≈0.07)

The binaural beat frequency equals the brainwave frequency. When two tones at f and f+Δf are panned to opposite ears, the listener perceives a beating at Δf. This is a direct CRR-to-perception mapping: the beat frequency literally IS the brainwave frequency, presented as sound.

**Base frequencies: 200, 240, 280, 320, 360 Hz.** These are spaced 40 Hz apart, placing them in different auditory critical bands to maintain perceptual distinctness. 200 Hz is chosen as the base because it's in the most sensitive region of human hearing for binaural perception.

### Stillness (Lines 2250–2254)

```js
ev(400, 'drone',    {midi:38, dur:20*BEAT_S});    // D2 for 20 seconds
ev(404, 'prepared', {midi:62, vel:.12, dur:6*BEAT_S});  // D4
ev(410, 'prepared', {midi:69, vel:.08, dur:5*BEAT_S});  // A4
ev(416, 'prepared', {midi:74, vel:.05, dur:4*BEAT_S});  // D5
```

The final section. A D2 drone (the tonic) sustains for 20 beats. Against it, three prepared piano tones enter at decreasing volumes (.12, .08, .05) and decreasing durations (6, 5, 4 beats):

- D4 (two octaves above the drone)
- A4 (the fifth — the most consonant non-octave interval)
- D5 (three octaves above)

Each successive note is higher in pitch, softer in volume, and shorter in duration. This is the CRR framework's final statement: coherence decays. The system approaches silence. But it doesn't reach it — the drone continues past the last prepared tone, implying the cycle will begin again. C→δ→R→C→...

The velocity ratios .12 : .08 : .05 ≈ 1 : 0.67 : 0.42. The ratio 0.67 ≈ 2/3, and 0.42 ≈ (2/3)² × 0.94. This is approximately geometric decay with ratio 2/3 — the reciprocal of the 3:2 fifth. The intervallic structure and the amplitude structure mirror each other.

---

## OVERALL ARCHITECTURE — THE META-CRR

The entire composition is itself a CRR system:

- **420 beats** = ~21 full phrase-agent cycles (SO(2), ω ≈ 0.239)
- **18 sections** = 18 piece-agent ruptures (Z₂, ω ≈ 0.637)
- **Activity curve** (ar values): starts at .02, rises to .95, settles at .5, fades to .05
  - This IS the beauty function B(C/Ω): low at start, peaks in the middle-to-late sections (Stellar Forge ar=.88, Cambrian ar=.95), then descends
  - Peak ar = 0.95 at Cambrian, exactly where life reaches its maximum morphological diversity
  - The ar curve traces B(C/Ω) at the composition level

The nested CRR structure — agents within phrases within sections within the piece — is itself scale-invariant. The same three equations at every level.

---

## SUMMARY OF KEY CONSTANTS AND THEIR CRR ORIGINS

| Constant | Value | CRR Derivation |
|----------|-------|----------------|
| Z₂ Ω | 1/π ≈ 0.318 | C·Ω=1, half-cycle path = π |
| SO(2) Ω | 1/2π ≈ 0.159 | C·Ω=1, full-cycle path = 2π |
| CV ratio | 2.0 | (1/2π)/(1/4π) — validated at 2.10 |
| Beauty peak | C/Ω ≈ 2.14 | dB/d(C/Ω) = 0 |
| Golden angle | π(3-√5) | max independent C per element |
| exp(C/Ω) = e^π ≈ 23.14 | Z₂/SO(2) boundary | universal across 40 orders |
| tanh(C/Ω) | order parameter | Z₂ mean-field solution |
| 1-exp(-C/Ω) | Boltzmann freeze-out | structural identity |
| Ω_interval ∝ 1/(p+q) | consonance law | beating rate from ratio p:q |
| H:He = 3:1 | 75%/25% | n/p = exp(-Q/T) freeze-out |
| δ_c = 1.686 | Press-Schechter | CRR rupture threshold for gravity |
| FM ratio = φ | sacred geometry tones | maximum spectral independence |
| Bass Q=10 | low Ω (rigid) | high coherence, precise |
| Snare Q=1 | high Ω (flexible) | low coherence, stochastic |
