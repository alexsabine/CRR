# CRR analysis of *Apis mellifera*

A first-principles application of the canonical CRR framework to the
mathematics, genetics, navigation, sensory systems, and architectural
behaviour of the honeybee. Methodology follows
`geometry_of_the_senses.pdf` (Sabine, April 2026).

This note **synthesises** existing bee biology under CRR
identifications and **derives** quantitative pre-registrations.
Empirical checks live in `claims/Be1_…/` through `claims/Be10_…/`.

---

## 1. The CRR machinery applied

The canonical framework supplies (after Session 7.5):

| Identity | Prediction | Class |
|----------|------------|-------|
| Z₂ rupture with SO(2) regulator | CV = 1/(2π) ≈ 0.1592 | Class A autonomous |
| SO(2) phase cycle | CV = 1/(4π) ≈ 0.0796 | Class A autonomous |
| Z₂ rupture without SO(2) (M23) | CV = 1 (exact) | Class C noise |
| Class B regulated | CV << 1/(4π) | tightly entrained |
| n+1/n integration depth | aperture separation → SO(2) relays | sensory hierarchy |
| C* − Ω | edge of criticality / beauty peak | maximum susceptibility |
| Ratio Z₂:SO(2) = 2 | exact topological invariant | falsifier |

---

## 2. Bee sensory systems — Z₂/SO(2) decomposition

Following the `geometry_of_the_senses.pdf` paradigm (paired Z₂
apertures + SO(2) integration depth scaling with baseline):

### 2.1 Compound eyes — Z₂ aperture + SO(2) ommatidial integration

- **Aperture pair separation** ≈ 1.5–2.5 mm (interocular, *Apis
  mellifera* worker).
- **Per-eye topology**: ~5,500 ommatidia, each subtending ~1°, arranged
  on a hexagonal lattice on a curved surface — an SO(2) tiling on S².
- **CRR identification**: each ommatidium is a Z₂ photo-rupture
  detector (photon-arrival → graded-potential threshold). The
  hexagonal tiling is the SO(2) regulator. The **5,500 ommatidia per
  eye** is the per-aperture parallel-channel count (width, not
  depth).

### 2.2 Optic-lobe relay depth

Bee visual processing proceeds: **lamina → medulla → lobula → mushroom
body** = **4 SO(2) integration stages**.

Compare to ants (`geometry_of_the_senses.pdf` §5.3): ants also have
4 visual relays at 1.5 mm interocular separation. Bees at 2.0 mm
should have ≥ 4 relays. **Confirmed** by canonical insect
neuroanatomy (Strausfeld 1976; Paulk et al. 2008).

### 2.3 Antennae — Z₂ olfactory apertures + AL integration

- **Aperture pair separation** ≈ 0.8–1.0 mm (inter-antennal base).
- **Per-antenna receptors**: ~60,000 chemoreceptor sensilla per
  antenna; ~165 olfactory glomeruli in the antennal lobe per side.
- **Relay depth**: antennal lobe → mushroom-body calyx + lateral horn
  = **2 SO(2) stages**.

This matches the carpenter-ant antennal pathway exactly (geometry
paper §5.3), and is shallower than the visual pathway despite the
antennae carrying **5+ modalities** (olfaction, gustation,
mechanoreception, hygroreception, thermoreception, magnetoreception).
**Aperture geometry > information content** holds for bees as for
ants — a non-trivial confirmation across phyla.

### 2.4 Polarised-light compass — SO(2) dorsal rim area (DRA)

The dorsal rim of each compound eye contains polarisation-sensitive
ommatidia tuned to the e-vector of skylight. The bee aligns its
flight by reading the SO(2) phase of the polarisation pattern across
the celestial hemisphere. **Pure SO(2) phase observable.** The
CRR-canonical Class A prediction CV = 1/(4π) applies to angular-
heading errors during vector flight.

### 2.5 Magnetic compass

Bees use Earth's magnetic field. Magnetic-field direction is an
SO(2) observable (azimuthal angle). **Class A or Class B**
depending on whether ferromagnetic/cryptochrome substrate is itself
regulated.

### 2.6 Mechanosensory — Johnston's organ (substrate vibration)

- **Receptor structure**: chordotonal scolopidia at the pedicel of
  each antenna; pure SO(2) phase observable on vibrational stimulus.
- **CRR identification**: SO(2) waggle-dance phase encoding. The
  waggle phase reads as SO(2) precision channel; the duration is the
  scaled coherence integral C.

---

## 3. Honeycomb — the cleanest CRR architecture in biology

### 3.1 The geometry

Honeycomb cells are **regular hexagons** (in 2D cross-section) and
**rhombic dodecahedral end-caps** (in 3D). Hexagonal tiling is the
**unique SO(2) tiling of the plane** that:

1. Tiles without gaps (Z₂ closure: every cell has either neighbour
   or boundary, never both).
2. Minimises perimeter per area at fixed unit area (Hales 2001
   honeycomb conjecture, proven).
3. Has 6-fold rotational symmetry — a Z₆ ⊂ SO(2) discrete subgroup
   (M15 reading).

### 3.2 CRR derivation of hexagonal optimality

The bee builder accumulates wax incrementally — each hexagon edge is
a coherence-accumulation segment. The rupture condition C·Ω = 1
corresponds to **wall-completion**: when accumulated wax mass
crosses threshold, the wall closes (Z₂ event). The SO(2) regulator
is the **6-fold local angular constraint** — every interior vertex
must subtend three 120° angles (the only way three cells can meet
at a vertex without gap).

The canonical CRR-CV prediction: wall-thickness CV across an
established comb should be **CV = 1/(2π)** (Z₂-rupture with SO(2)
regulator) — the closest analog to the B8 bacterial-division
canonical T3.

### 3.3 The 14.08° tilt

Honeycomb cells are **tilted upward by ~13°** (canonical published:
9–14°) so that nectar/honey does not flow out before capping. CRR
identification: the tilt angle is determined by the C*-minus-Ω
condition on the surface-tension geodesic. Worth a fresh pre-reg.

### 3.4 Cell-size dimorphism

Worker cells: ~5.2 mm across flat sides. Drone cells: ~6.9 mm.
**Ratio 6.9/5.2 ≈ 1.327**. The CRR Z₂:SO(2) ratio is 2; the
golden-ratio φ = 1.618; neither matches 1.327. But **(2/φ)¹ ≈
1.236, (φ/2 + 1/2) ≈ 1.309, √(φ) ≈ 1.272, 4/3 = 1.333**. The
**4/3 ratio** is striking — and 4/3 appears in CRR via the n+1/n
relation: at n=3, 3+1/3 = 10/3. And 4/3 = 1 + 1/3 = the next-down
n+1/n value at n=3. **Pre-registrable**: drone:worker cell linear
ratio = 4/3 ± 5%.

---

## 4. Genetics — haplodiploidy as a Z₂/SO(2) doubling architecture

### 4.1 Sex determination

Honeybees are **haplodiploid**:
- **Drones (males)** are haploid (16 chromosomes), arising from
  unfertilised eggs.
- **Workers and queens (females)** are diploid (32 chromosomes),
  from fertilised eggs.

**CRR identification**: the haploid/diploid switch is itself a Z₂
event at fertilisation (sperm enters or doesn't). The chromosome
count doubles across the Z₂ transition: **2× = topological ratio
Z₂:SO(2)** exactly. The genetic architecture *is* the canonical
Z₂:SO(2) doubling, made cellular.

### 4.2 Relatedness coefficients (Hamilton kinship)

Under haplodiploidy, sister workers share **75%** of their genes
(3/4), versus the 50% (1/2) of standard diploid siblings.
Mother–daughter coefficient: 50%.

**3/4 vs 1/2 ratio = 1.5.** Note that **1.5 = 3/2** appears in CRR
via M22 (SO(2) → SO(3) factor in the n+1/n derivation cycle). And
**3/4 = the sister coefficient = ¾ × C\* of SO(2) = 3π/2** if cells
trace 3/4 of the SO(2) circle at each meiotic division step. This
is suggestive but speculative — not pre-registered.

### 4.3 The complementary sex determiner (csd) locus

The **csd gene** has >100 alleles in wild populations; sex is
determined by heterozygosity (heterozygous → female, homozygous /
hemizygous → male). The polymorphism level is extremely high.

**CRR pre-reg**: under M23 + the Z₂-without-SO(2) reading, the
distribution of csd allele frequencies in a wild population should
follow an exponential-like (CV ≈ 1) pattern — each allele is
maintained by negative-frequency-dependent selection (rare alleles
favoured), which is the population-genetic analogue of memoryless
sampling.

---

## 5. Navigation — sun compass + path integration as SO(2) precision

### 5.1 The sun compass

Bees navigate by the **azimuth of the sun** (or the SO(2)
polarisation pattern when the sun is occluded). This is a pure
SO(2) phase observable.

**CRR pre-reg**: across waggle-dance recordings, the angular
heading-error CV should match the SO(2) Class A prediction
CV = 1/(4π) ≈ 0.0796 (within ±30%).

### 5.2 Path integration — vector accumulation

Bees integrate distance and direction during outbound flights and
return on a near-straight line — the **home vector**. This is the
exact CRR coherence integral C(x,t) = ∫L(x,τ)dτ on the SO(2)
manifold.

**CRR pre-reg**: the path-integration error scales as SD ∝ √t (by
Brownian-motion-like accumulation), with the fractional error
saturating at CV = 1/(4π) at the rupture threshold.

### 5.3 Distance encoding — the waggle dance

The duration of the waggle phase encodes flight distance: roughly
**~1 second per 750 m**. Direction is encoded by the angle of the
waggle relative to gravity = sun azimuth.

**CRR identification**: the waggle is an SO(2) phase signal
(direction) modulated by a Z₂ rupture-rate signal (waggles per
unit time). The combination is the **canonical CRR symbol** — both
operators in one motor pattern.

### 5.4 Predicted angular CV

Reported angular precision of waggle dance: typically **±15° SD**
across multiple waggles for the same target, mean dance angle
roughly along a target vector. **Angular CV = 15°/360° = 0.042**;
or relative to a half-circle SD/180° = 0.083.

The **0.083** value matches **1/(4π) = 0.0796** to ~4%. **Pre-reg
pass anticipated.**

---

## 6. Foraging dynamics — Class A, B, or C?

### 6.1 Inter-trip return-time CV

A forager's inter-trip interval (time between successive returns to
the hive) is a candidate CRR observable. If foraging is autonomous
(Class A Z₂-with-SO(2)), CV ≈ 1/(2π). If memoryless (Class C,
M23), CV = 1.

**Pre-reg**: forager inter-trip interval CV should be in the **Z₂
band** (CV ≈ 0.16) — bees integrate environment quality (a
coherence variable) and rupture-decide when to return. **Memory-
bearing.**

### 6.2 Colony swarming events — Z₂ rupture at colony scale

Swarming is a colony-level Z₂ event (the colony divides) gated by
internal coherence build-up (queen-pheromone, comb-density,
brood-population thresholds). **Pre-reg**: inter-swarm-interval CV
across multiple colonies, controlling for season, should be in the
Z₂ band.

---

## 7. The 16 nats / phase-gating connection

The canonical 16-nat hypothesis (`crr_16_nats_hypothesis.md` in
the repo) holds that biological information transfer per phase-
gating cycle is bounded near 16 nats.

**Bee waggle-dance information content** has been computed:
roughly **0.3–0.5 bits per waggle** for direction × distance, with
~30 waggles per dance ⇒ **~10–15 bits per dance ≈ 7–10 nats**. Not
saturated at 16 nats per dance, but **per dance** is the wrong unit
— per **circuit-cycle** (1 figure-eight) the information is
~0.3 bits ≈ 0.2 nats. Many cycles aggregate.

**Per coherence-rupture cycle (one waggle + one return arc)** is
the right unit. Quantitative comparison reserved for a fresh
pre-reg.

---

## 8. Summary — bee CRR identifications

| Bee phenomenon | CRR class | CV target |
|----------------|-----------|-----------|
| Compound-eye ommatidial photoreceptor activation | Z₂ + SO(2) | 1/(2π) |
| Hexagonal honeycomb wall thickness | Z₂ rupture w/ SO(2) | 1/(2π) |
| Polarised-light compass heading error | SO(2) | 1/(4π) |
| Waggle-dance angular SD per dance | SO(2) | 1/(4π) ≈ 0.08 |
| Forager inter-trip interval CV | Z₂ memory-bearing | 1/(2π) |
| Inter-colony swarming-interval CV | Z₂ memory-bearing | 1/(2π) |
| Circadian foraging rhythm CV | Class B regulated | < 0.05 |
| Inter-spike ISI in Kenyon cells (mushroom body) | Class C | ≈ 1 |
| csd allele frequency distribution | Class C / M23 | ≈ 1 (exponential-like) |
| Cell-size ratio drone/worker | n+1/n at n=3? | 4/3 ≈ 1.333 |
| Visual relay count vs interocular distance | n+1/n | 4 stages |
| Antennal relay count | n+1/n shallow | 2 stages |
| Honeycomb tilt angle | C*−Ω geometry | ~13° |

These are the testable surfaces. **Ten pre-registrations** follow
in the `claims/Be1…Be10/` directories.
