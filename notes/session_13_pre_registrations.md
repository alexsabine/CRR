# Session 13 — 20 new pre-registered CRR predictions (10 physics + 10 biology)

This document pre-registers 20 new CRR predictions on physical
and biological systems. Each prediction names a substrate from
the post–Session-12 extended CV ladder, a public dataset, a
falsifier band, and a T3 promotion criterion.

The pre-registration commit hash is the binding audit anchor.
Per CAMPAIGN.md PART III, tolerance bands and falsifier bands
cannot be retroactively edited. Honest negatives committed
permanently.

## Extended CV ladder (post-Session 12)

| Tier | CV | Mechanism |
|------|---:|-----------|
| Deterministic | → 0 | rich G, perfect sync |
| SU(3) / higher | 0.046 | richer compact group |
| **SO(2) / SU(2) / T²** | **0.080** | continuous closed-geodesic |
| **Class B regulated** | ≈ 0.05–0.07 | autonomous + feedback |
| **Z₂ / SO(3)** | **0.159** | discrete binary phase |
| **No regulator (Poisson)** | **1.0** | no phase manifold |
| **Self-exciting (Hawkes)** | **> 1** | event-triggered intensity boost |
| Mid-regime fluctuations | 0.3–0.7 | partial regulation |

Predictions in this session draw on all eight tiers.

## Substrate-coverage map of the 20 predictions

| Substrate / regime | Predictions |
|--------------------|-------------|
| SO(2) autonomous (CV ≈ 0.080) | P31, P34, B12, B13, B14, B15, B16, B19, B20 |
| Z₂ autonomous (CV ≈ 0.159) | B18 |
| Class B regulated (CV ≈ 0.05–0.13) | P33, P37, B11, B17 |
| No regulator (CV ≈ 1.0) | P30, P36, P38 |
| Hawkes self-exciting (CV > 1.30) | P32, P35, P39 |

---

# PHYSICS predictions (P30–P39)

---

## P30 — Geomagnetic Kp-index ≥ 7 storm inter-arrival CV (no-regulator)

**Substrate.** No regulator — geomagnetic storms are externally
driven by interplanetary CMEs / coronal-hole high-speed streams
with no closed Earth-side coherence cycle.

**Pre-registration.** Across NOAA/GFZ Potsdam Kp index 1932-01-01
to test-execution date, restricted to events where Kp ≥ 7
(canonical "severe storm" threshold; Bartels 1949):

    CV(inter-event interval) ∈ [0.85, 1.15]   AND   N ≥ 30.

**Falsifier.** CV outside [0.70, 1.30] with N ≥ 30.

**Dataset.** GFZ Potsdam Kp-index canonical archive
(`https://www.gfz-potsdam.de/en/section/geomagnetism/data-products-services/kp-index`),
or any GitHub mirror of the same.

**T3 promotion criterion.** CV ∈ [0.85, 1.15] with N ≥ 30.

---

## P31 — Solar p-mode oscillation lifetime CV across modes (SO(2))

**Substrate.** SO(2) — each acoustic standing-wave mode is a
closed-geodesic phase circle in the solar interior.

**Pre-registration.** Across SOHO/MDI + SDO/HMI catalogued
p-modes 2010-2024, restricted to ℓ = 0–3 modes with frequency
2–4 mHz (the dominant 5-minute-oscillation band):

    CV(mode lifetime) across modes ∈ [0.070, 0.100]
    AND   N_modes ≥ 20.

**Falsifier.** CV outside [0.060, 0.110] with N_modes ≥ 20.

**Dataset.** GONG / SOHO MDI / SDO HMI mode-parameter tables
(`https://gong.nso.edu/data/`; `https://jsoc.stanford.edu`).

**T3 promotion criterion.** CV ∈ [0.070, 0.100] with N ≥ 20.

---

## P32 — Pulsar glitch inter-arrival CV at single sources (Hawkes)

**Substrate.** Self-exciting (Hawkes regime, CV > 1) — glitches
in the Vela / Crab / PSR J0537 catalogues are known to cluster
on superfluid-vortex-unpinning relaxation timescales.

**Pre-registration.** Across Jodrell Bank / ATNF pulsar-glitch
catalogue, for any pulsar with ≥ 5 glitches in record:

    CV(inter-glitch interval) > 1.30   AND   N_pulsars ≥ 3.

**Falsifier.** Median CV across qualifying pulsars in [0.7, 1.3]
(would suggest no-regulator / Poisson, refuting Hawkes self-
excitation in glitch dynamics).

**Dataset.** Jodrell Bank glitch table
(`https://www.jb.man.ac.uk/pulsar/glitches.html`).

**T3 promotion criterion.** Median CV > 1.30 with N ≥ 3
qualifying pulsars.

---

## P33 — Tidal high-water inter-event interval CV (Class B regulated)

**Substrate.** Class B regulated below SO(2) — lunar-solar
gravitational forcing is a *very tight* SO(2)-class regulator;
expect CV well below the 0.080 autonomous prediction.

**Pre-registration.** Across UHSLC global tide-gauge fast-data
network (≥ 10 stations) 2010-2024, hourly tide gauges,

    median across stations of CV(inter-high-water interval)
    ∈ [0.020, 0.060]   AND   N_stations ≥ 10.

**Falsifier.** CV outside [0.010, 0.080] with N ≥ 10.

**Dataset.** UHSLC fast-data product
(`https://uhslc.soest.hawaii.edu/data/`).

**T3 promotion criterion.** Median CV ∈ [0.020, 0.060] with
N ≥ 10.

---

## P34 — Earth normal-mode (free-oscillation) Q-factor CV (SO(2))

**Substrate.** SO(2) — Earth's seismic free-oscillation modes
(0S2, 0S3, …, 1S0, …) are SO(2) standing waves with lifetimes
set by intrinsic Q.

**Pre-registration.** Across PREM-catalogued spheroidal modes
0S2–0S20 with measured Q-factors:

    CV(Q across modes) ∈ [0.070, 0.110]
    AND   N_modes ≥ 15.

**Falsifier.** CV outside [0.05, 0.15] with N_modes ≥ 15.

**Dataset.** PREM mode catalogue (Dziewonski & Anderson 1981);
IRIS catalogues for individual-mode measurements.

**T3 promotion criterion.** CV ∈ [0.070, 0.110] with N ≥ 15.

---

## P35 — Volcanic eruption inter-arrival at single arc volcanoes (Hawkes)

**Substrate.** Self-exciting (Hawkes) — magma-chamber
pressurisation after eruption produces self-exciting eruption
sequences (Bebbington 2007).

**Pre-registration.** Smithsonian GVP Volcanoes-of-the-World
catalogue, restricted to single arc volcanoes with ≥ 10 dated
Holocene eruptions of VEI ≥ 2:

    median across volcanoes of CV(inter-eruption interval)
    > 1.30   AND   N_volcanoes ≥ 10.

**Falsifier.** Median CV in [0.7, 1.3] (suggests no-regulator,
not Hawkes).

**Dataset.** GVP database
(`https://volcano.si.edu/database/search_eruption_results.cfm`).

**T3 promotion criterion.** Median CV > 1.30 with N ≥ 10.

---

## P36 — Cosmic-ray extensive-air-shower inter-event CV at fixed station (no-regulator)

**Substrate.** No regulator — primary cosmic-ray arrivals at the
top of atmosphere are unrelated to any Earth-side coherence
cycle.

**Pre-registration.** Across Pierre Auger Observatory or HAWC
public event catalogues, restricted to E ≥ 10 EeV ultra-high-
energy events at a single station,

    CV(inter-event interval) ∈ [0.85, 1.15]   AND   N ≥ 100.

**Falsifier.** CV outside [0.70, 1.30] with N ≥ 100.

**Dataset.** Auger Open Data (`https://opendata.auger.org/`);
HAWC public event catalogue.

**T3 promotion criterion.** CV ∈ [0.85, 1.15] with N ≥ 100.

---

## P37 — Old Faithful (Yellowstone) eruption inter-arrival CV post-2000 (Class B regulated SO(2))

**Substrate.** Class B regulated below SO(2) — Old Faithful's
geyser plumbing operates on a tight thermodynamic cycle; the
post-2000 record (after the 1998 earthquake recalibration) is
the cleanest regulated regime.

**Pre-registration.** USGS / NPS Old Faithful eruption logs
2000-01-01 to test-execution date,

    CV(inter-eruption interval) ∈ [0.040, 0.080]
    AND   N_eruptions ≥ 1000.

**Falsifier.** CV outside [0.020, 0.120] with N ≥ 1000.

**Dataset.** GeyserTimes
(`https://geysertimes.org/geyser/Old%20Faithful`); NPS Old
Faithful logs.

**T3 promotion criterion.** CV ∈ [0.040, 0.080] with N ≥ 1000.

---

## P38 — Aurora occurrence inter-arrival CV at fixed magnetic latitude (no-regulator)

**Substrate.** No regulator — auroral occurrence is driven by
external solar-wind / IMF orientation on minute-to-day
timescales without an Earth-side closed phase cycle.

**Pre-registration.** Across NOAA / NRL all-sky aurora-detection
records at single high-latitude stations (Alaska, Norway,
Svalbard, Yellowknife) 2000-2024,

    median across stations of CV(inter-event interval)
    ∈ [0.85, 1.15]   AND   N_stations ≥ 5.

**Falsifier.** Median CV outside [0.70, 1.30] with N ≥ 5.

**Dataset.** NOAA SWPC aurora catalogues; SuperMAG aurora
indices.

**T3 promotion criterion.** Median CV ∈ [0.85, 1.15] with
N ≥ 5.

---

## P39 — M-dwarf stellar flare inter-arrival CV (Hawkes)

**Substrate.** Self-exciting (Hawkes) — stellar flaring on
M-dwarfs shows superflare clustering linked to active-region
emergence and decay (Davenport 2016).

**Pre-registration.** Across Kepler / TESS catalogued M-dwarf
flare stars with ≥ 50 flares in single quarters / sectors,
restricted to flare amplitudes ≥ 1% photometric:

    median CV(inter-flare interval) > 1.30
    AND   N_stars ≥ 10.

**Falsifier.** Median CV in [0.7, 1.3].

**Dataset.** Davenport 2016 flare catalogue (Kepler);
TESS public flare catalogues.

**T3 promotion criterion.** Median CV > 1.30 with N ≥ 10.

---

# BIOLOGY predictions (B11–B20)

---

## B11 — Healthy adult walking gait stride-to-stride CV (Class B regulated SO(2))

**Substrate.** Class B regulated below SO(2) — the gait phase
circle is SO(2) (left-right alternation closes one gait period),
with strong descending feedback regulation in young healthy
adults.

**Pre-registration.** Across PhysioNet Gait in Aging and Disease
+ Hausdorff archives, restricted to healthy young adults (age
20–35):

    median CV(stride interval) ∈ [0.020, 0.060]
    AND   N_subjects ≥ 30.

**Falsifier.** CV outside [0.010, 0.090] with N ≥ 30.

**Dataset.** PhysioNet Gait in Aging and Disease database
(`https://physionet.org/content/gaitdb/1.0.0/`); Hausdorff gait
archives.

**T3 promotion criterion.** Median CV ∈ [0.020, 0.060] with
N ≥ 30.

---

## B12 — REM-cycle period CV in healthy adults (SO(2))

**Substrate.** SO(2) — the ultradian REM/non-REM cycle (~90 min)
is a closed-geodesic ultradian phase manifold.

**Pre-registration.** Across NSRR Sleep Heart Health Study
(SHHS) + MROS healthy controls, ≥ 4 complete REM cycles per
night,

    median across subjects of intra-subject
    CV(REM-cycle period) ∈ [0.070, 0.110]
    AND   N_subjects ≥ 50.

**Falsifier.** CV outside [0.050, 0.150] with N ≥ 50.

**Dataset.** NSRR SHHS / MROS / MESA polysomnography archive
(`https://sleepdata.org/`).

**T3 promotion criterion.** Median CV ∈ [0.070, 0.110] with
N ≥ 50.

---

## B13 — Avian dawn-chorus inter-syllable interval CV in single-species sustained bouts (SO(2))

**Substrate.** SO(2) — single-species sustained singing in dawn
chorus is a vocal-motor SO(2) phase circuit.

**Pre-registration.** Across xeno-canto / Macaulay Library
public-archive recordings of single-species sustained dawn-
chorus bouts (≥ 30 s continuous), restricted to common-passerine
species (e.g., Turdus, Erithacus, Parus, Sylvia genera):

    median across recordings of intra-bout
    CV(inter-syllable interval) ∈ [0.060, 0.100]
    AND   N_recordings ≥ 30.

**Falsifier.** CV outside [0.04, 0.13] with N ≥ 30.

**Dataset.** xeno-canto (`https://xeno-canto.org/`); Macaulay
Library (Cornell Lab of Ornithology).

**T3 promotion criterion.** Median CV ∈ [0.060, 0.100] with
N ≥ 30.

---

## B14 — Cricket chirp inter-pulse-train interval CV at constant temperature (SO(2))

**Substrate.** SO(2) — cricket calling-song central-pattern-
generator phase circuit; Dolbear (1897) law specifies tight
temperature-dependent rate.

**Pre-registration.** Across published Gryllus pennsylvanicus or
G. campestris recordings at controlled 25 °C ± 1 °C, ≥ 60 s
continuous calling:

    median across recordings of intra-bout
    CV(inter-pulse-train) ∈ [0.060, 0.100]
    AND   N_recordings ≥ 20.

**Falsifier.** CV outside [0.04, 0.13] with N ≥ 20.

**Dataset.** xeno-canto cricket recordings; Cornell BIRDS-DS
+ insect recordings.

**T3 promotion criterion.** Median CV ∈ [0.060, 0.100] with
N ≥ 20.

---

## B15 — Synchronised yeast cell-cycle period CV under glucose-limited continuous culture (SO(2))

**Substrate.** SO(2) — autonomous metabolic-respiratory
oscillation in continuously-grown synchronised S. cerevisiae
(period 0.7–4 h) is a closed-geodesic phase manifold (Klevecz
et al. 2004 *PNAS*).

**Pre-registration.** Across published continuous-culture
yeast oscillator datasets (Murray, Lloyd, Shadle / Tu / Mohler
groups), restricted to stable steady-state phases ≥ 100
oscillations:

    median across runs of CV(period) ∈ [0.060, 0.100]
    AND   N_runs ≥ 5.

**Falsifier.** CV outside [0.04, 0.13] with N ≥ 5.

**Dataset.** Klevecz 2004 supplementary; Tu et al. 2005
*Science* deposited timeseries; Murray 2003+ dissolved-O₂
traces.

**T3 promotion criterion.** Median CV ∈ [0.060, 0.100] with
N ≥ 5.

---

## B16 — Honeybee waggle-dance round-trip duration CV in stable foraging bouts (SO(2))

**Substrate.** SO(2) — each waggle-run + return-phase loop is a
closed-geodesic phase cycle on the bee's central-complex
heading-encoding manifold.

**Pre-registration.** Across published waggle-dance video-
analysis archives (Couvillon, Schultheiss, Seeley, Beekman
groups), restricted to single-bee single-foraging-bout dance
sequences ≥ 10 round-trips:

    median across bouts of intra-bout
    CV(round-trip duration) ∈ [0.060, 0.100]
    AND   N_bouts ≥ 30.

**Falsifier.** CV outside [0.04, 0.13] with N ≥ 30.

**Dataset.** Movebank.org honeybee tracking; Couvillon et al.
2014 published kinematics; deposited movie-analysis CSVs.

**T3 promotion criterion.** Median CV ∈ [0.060, 0.100] with
N ≥ 30.

---

## B17 — Spontaneous eyeblink inter-blink CV in healthy adults during reading (Class B regulated)

**Substrate.** Class B regulated — spontaneous blinking in
attentive cognitive states (reading) is regulated below the
autonomous SO(2) baseline by attention-driven dopaminergic
gating (Karson 1983).

**Pre-registration.** Across published EOG / video-eye-tracker
archives of healthy adults 20–40 yr in sustained reading-task
recordings ≥ 5 min:

    median CV(inter-blink interval)
    ∈ [0.060, 0.100]
    AND   N_subjects ≥ 30.

**Falsifier.** CV outside [0.04, 0.15] with N ≥ 30.

**Dataset.** OpenNeuro EOG / eye-tracking datasets; Doughty
2014 archives.

**T3 promotion criterion.** Median CV ∈ [0.060, 0.100] with
N ≥ 30.

---

## B18 — Healthy nulliparous menstrual cycle length CV (Z₂; M22 v2 Test 1 replication)

**Substrate.** Z₂ — replication of the M22 v2 Test 1 result on a
*non-Bull* independent dataset.

**Pre-registration.** Across an independent published cohort of
≥ 5,000 healthy nulliparous women age 18–35 with ≥ 6 cycles
tracked, the CV of cycle lengths:

    CV(cycle length) ∈ [0.140, 0.200]
    AND   N_women ≥ 5000.

**Falsifier.** CV outside [0.10, 0.25] with N ≥ 5000.

**Dataset.** Apple Women's Health Study (Mahalingaiah et al.
2022 *NPJ Digit. Med.*); Natural Cycles app deposited
aggregate datasets.

**T3 promotion criterion.** CV ∈ [0.140, 0.200] with N ≥ 5000.
This is an *independent replication* of M22 v2 Test 1
(menstrual CV = 0.177); a clean pass would promote the M22 Z₂
biological-cycle identification toward T4-eligibility on
multi-cohort confirmation.

---

## B19 — Bipedal quiet-stance centre-of-pressure (COP) sway-cycle CV in healthy adults (SO(2))

**Substrate.** SO(2) — postural-control oscillation in the
~0.3–1 Hz band reflects a closed-geodesic ankle-feedback phase
manifold.

**Pre-registration.** Across PhysioNet Force Platform Posture
archive + IEEE-DataPort COP datasets, healthy adults 20–40 yr,
quiet-stance trials ≥ 60 s eyes-open:

    median CV(inter-zero-crossing interval, AP axis)
    ∈ [0.060, 0.100]
    AND   N_subjects ≥ 30.

**Falsifier.** CV outside [0.04, 0.13] with N ≥ 30.

**Dataset.** PhysioNet posture databases; IEEE-DataPort COP
archives.

**T3 promotion criterion.** Median CV ∈ [0.060, 0.100] with
N ≥ 30.

---

## B20 — Bird first-arrival date interannual CV at fixed observatory (SO(2))

**Substrate.** SO(2) — annual photoperiod-driven migration is
a closed-geodesic phase circuit at calendar-year scale.

**Pre-registration.** Across eBird / Cornell Lab + UK BTO
constant-effort sites, restricted to common Palearctic
migrants (≥ 6 species) at ≥ 5 sites with ≥ 20 years of
records:

    median across (species, site) pairs of interannual
    CV(first-arrival DOY) ∈ [0.060, 0.100]
    AND   N_pairs ≥ 30.

**Falsifier.** CV outside [0.04, 0.13] with N ≥ 30.

**Dataset.** eBird basic dataset (`https://ebird.org/data/download/`);
BTO Constant Effort Sites scheme.

**T3 promotion criterion.** Median CV ∈ [0.060, 0.100] with
N ≥ 30.

---

# Joint significance

The 20 predictions stress-test all eight tiers of the post-
Session-12 extended CV ladder across two scientific domains.
Specifically:

- **3 no-regulator tests** (P30, P36, P38): externally-driven
  events with no Earth-/biology-side closed phase manifold.
  Expected CV ≈ 1.0. Confirms / extends the no-regulator
  baseline (cf. P26 multi-domain test, I6 cyber).

- **3 Hawkes self-exciting tests** (P32, P35, P39): clustered
  event sequences with self-excitation. Expected CV > 1.30.
  Cross-domain confirmation of the Hawkes regime discovered in
  Session 12 financial-event tests.

- **9 SO(2) autonomous tests** (P31, P34, B12, B13, B14, B15,
  B16, B19, B20): closed-geodesic phase manifolds in physics
  (acoustic, seismic) and biology (vocal, motor, postural,
  metabolic, migratory). Expected CV ≈ 0.080.

- **4 Class B regulated tests** (P33, P37, B11, B17): autonomous
  + feedback. Expected CV ≈ 0.05.

- **1 Z₂ test** (B18): independent replication of the
  M22 v2 menstrual-cycle Z₂ identification on a fresh cohort
  (Apple Women's Health Study).

If even half (≥ 10 of 20) pass their pre-registered band, this
constitutes the campaign's strongest physics+biology cross-
domain confirmation set to date. If fewer than half pass, the
honest-negative ledger gains material to refine substrate
identifications further. Either outcome is informative.

---

## Audit-trail anchor

This file's commit hash on push to branch
`claude/verify-folder-access-CInY3` is the binding pre-
registration commit for P30–P39 and B11–B20. Reviewer execution
scripts must be committed in subsequent commits. Honest
negatives committed permanently. No retroactive edits.
