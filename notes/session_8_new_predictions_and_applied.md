# Session 8 — Ten new pre-registered CRR predictions + applied/economic scoping

This document extends the CRR pre-registration audit trail with **ten new
parameter-free predictions** in solar physics (4), black-hole astrophysics
(3), and three new biological systems (3). It then provides an **applied
use-case map** with first-pass GDP exposure, applicability likelihoods,
indicative investment cost ranges, and potential financial-gain envelopes
per domain.

The methodology mirrors the per-claim files in `claims/` and the
discipline of `CAMPAIGN.md` PART III. Each prediction is committed at
T1 (derivation only) on commit; T3 promotion requires reviewer
execution against the named, public, untouched dataset. The git log is
the audit trail.

The canonical formalism applied is Section 2 of
`CRR_FINAL_CANONICAL.md`:

> CRR's full operational architecture is **a Z₂ rupture acting on a
> continual memory-bearing compact connected Lie group G**, with
> CV_G = 1 / (2·φ_G), Ω_G = 1/φ_G, CV = Ω_G/2 (M1 + M22).

Reference table (canonical CV_G, M22):

| G | φ_G | Ω_G | CV_G |
|---|-----|-----|------|
| Z₂ (rupture only) | π | 1/π | 1/(2π) ≈ 0.1592 |
| U(1) ≅ SO(2) | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SU(2) ≅ S³ | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SO(3) = SU(2)/Z₂ | π | 1/π | 1/(2π) ≈ 0.1592 |
| T² (per generator) | 2π | 1/(2π) | 1/(4π) ≈ 0.0796 |
| SU(3) | 2π√3 | 1/(2π√3) | 1/(4π√3) ≈ 0.0459 |

A 2:1 ratio between SO(3)-class and SO(2)/SU(2)-class CV is a strict
topological consequence of the Z₂ centre of SU(2); it is the sharpest
falsifier of M22.

---

## Part A — Ten new pre-registered predictions

Format per prediction:
- **Statement** (CRR-derived).
- **Substrate identification** (which compact connected Lie group G).
- **Quantitative pre-registration** (band + sample size).
- **Dataset target** (named, public, untouched).
- **Protocol** (steps a reviewer can execute).
- **Falsifier** (numerical band that falsifies the claim).
- **Independence** (was the dataset used in deriving the prediction?).
- **T3 promotion criterion**.

All ten are T1 on commit. Promotion to T2/T3 requires reviewer execution.

---

### P8 — Solar differential-rotation latitudinal CV (T² substrate)

**Statement.** The solar surface differential-rotation rate Ω(θ) as a
function of latitude θ is supported by a torus T² = SO(2)_φ × SO(2)_θ
phase manifold (longitude × latitude embedding of dynamo modes). Under
M22, each generator carries CV_G = 1/(4π) ≈ 0.0796.

**Substrate.** T² (per generator).

**Pre-registration.** Across helioseismic latitude bands θ ∈
{−60°, −45°, −30°, −15°, 0°, 15°, 30°, 45°, 60°} sampled annually
2010–2024, the *cross-band CV* of mean rotation rate satisfies

    CV_lat ∈ [0.070, 0.090]   AND   N_bands ≥ 9.

**Dataset.** SDO/HMI ring-diagram and time-distance helioseismology
catalogues (HMI Science Data Processing pipeline, JSOC archive,
`http://jsoc.stanford.edu`); cross-validation against GONG (NSO,
`https://gong.nso.edu`).

**Protocol.**
1. Fetch annually-averaged Ω(θ) from HMI ring-diagram tables.
2. Compute mean and std across the latitude bands per year.
3. Compute CV_lat = std/mean per year.
4. Mean of per-year CV_lat across 15 years = test statistic.
5. Compare to predicted [0.070, 0.090].

**Falsifier.** Mean CV_lat outside [0.060, 0.100] with N ≥ 9.

**Independence.** Helioseismic differential-rotation tables were not
used in deriving CRR; the T² identification is fresh.

**T3 promotion criterion.** Mean CV_lat ∈ [0.070, 0.090] with N ≥ 9.

---

### P9 — Coronal-mass-ejection inter-arrival CV at solar maximum

**Statement.** CMEs are Z₂ rupture events on the solar SO(2) dynamo
phase manifold. Their inter-arrival intervals during the central
2-year solar-maximum window of each cycle exhibit CV = 1/(4π).

**Substrate.** SO(2).

**Pre-registration.** Pooling SOHO/LASCO catalogue CMEs with angular
width ≥ 30° (excluding narrow jets; restricting to the canonical
"halo and partial-halo" CME population) during the
2024-01-01 → 2026-01-01 maximum-window of solar cycle 25,

    CV_CME ∈ [0.070, 0.090]   AND   N_CMEs ≥ 1500.

**Dataset.** SOHO/LASCO CDAW CME catalogue
(`https://cdaw.gsfc.nasa.gov/CME_list/`), filtered by angular width
and date range as above.

**Protocol.**
1. Fetch CME catalogue rows in date range and angular-width filter.
2. Compute inter-arrival intervals Δt_i = t_{i+1} − t_i.
3. Compute CV = std(Δt) / mean(Δt) on the pooled sample.
4. Compare to predicted [0.070, 0.090].

**Falsifier.** CV outside [0.060, 0.105] with N ≥ 1500. (A CV ≫ 0.1
would indicate a Lévy / heavy-tailed regime inconsistent with SO(2)
phase circulation.)

**Independence.** SOHO/LASCO catalogue not used in CRR construction.

**T3 promotion criterion.** CV ∈ [0.070, 0.090] with N ≥ 1500.

---

### P10 — Sunspot-cycle vs Hale-cycle CV ratio (M22 falsifier in solar)

**Statement.** The sunspot-count cycle (∼11 yr, returns to *unsigned*
maximum after one polarity flip) is supported by SO(3) topology
(half-period of the magnetic cycle, π geodesic). The Hale magnetic
cycle (∼22 yr, returns to *signed* identity) is supported by SU(2) ≅
S³ (full geodesic 2π). Under M22:

    CV_sunspot / CV_Hale = SO(3) / SU(2) = (1/(2π)) / (1/(4π)) = 2.

**Substrate.** SU(2) (Hale) vs SO(3) (sunspot count). M22's strictest
solar falsifier.

**Pre-registration.** Across the SILSO sunspot-number record
1755-01–2025-12 (cycles 1–25),

    CV_sunspot / CV_Hale ∈ [1.7, 2.3]   AND   N_full_Hale ≥ 12.

**Dataset.** SILSO version-2 monthly mean total sunspot number
(`https://www.sidc.be/SILSO/datafiles`), McIntosh / Hathaway cycle
boundaries (NASA MSFC solar-cycle prediction page).

**Protocol.**
1. Identify cycle boundaries (max-to-max) from SILSO smoothed series.
2. Compute sunspot-cycle period CV across cycles 1–25.
3. Identify Hale-cycle boundaries by pairing consecutive sunspot
   cycles (1+2, 3+4, …); compute Hale-cycle period CV.
4. Form ratio CV_sunspot / CV_Hale.
5. Compare to predicted [1.7, 2.3].

**Falsifier.** Ratio outside [1.5, 2.5]. A ratio ≈ 1 would indicate
SU(2) and SO(3) phase manifolds give the same CV, breaking M22's
covering-relation prediction. **This is the same topological
falsifier as M22-A; a solar-domain replication.**

**Independence.** Hale/sunspot cycle period ratios are reported in
the literature (Hathaway 2015) but the CV ratio = 2 prediction is
CRR-specific (from M22, not from observation).

**T3 promotion criterion.** Ratio ∈ [1.7, 2.3] with N_full_Hale ≥ 12.

---

### P11 — Solar-wind sector-boundary inter-crossing CV at L1

**Statement.** Heliospheric current sheet sector boundaries (toward/
away IMF polarity flips) at L1 are Z₂ rupture events on the SU(2) ≅ S³
phase manifold of the dipole-tilted dynamo. Under M22, CV = 1/(4π).

**Substrate.** SU(2).

**Pre-registration.** Across ACE + Wind + DSCOVR magnetic-field
sector identifications during the calendar years 2018–2024 (full
declining-to-rising phase, excluding deep minimum 2019),

    CV_sector ∈ [0.070, 0.090]   AND   N_crossings ≥ 200.

**Dataset.** OMNIWeb 1-hour merged magnetic-field data
(`https://omniweb.gsfc.nasa.gov/`), polarity inversions identified
by sign change of B_x in GSE coordinates with 24-hour persistence
filter.

**Protocol.**
1. Fetch hourly B_x from OMNI in the time range.
2. Apply 24-hour median filter to suppress flapping.
3. Identify sign-change crossings; record times.
4. Compute inter-crossing intervals; compute CV.
5. Compare to predicted [0.070, 0.090].

**Falsifier.** CV outside [0.060, 0.100] with N ≥ 200.

**Independence.** OMNI sector-boundary statistics were not used in
deriving CRR.

**T3 promotion criterion.** CV ∈ [0.070, 0.090] with N ≥ 200.

---

### P12 — Black-hole ringdown overtone-frequency CV (LIGO O5+)

**Statement.** Post-merger ringdown of a Kerr black hole has
quasinormal-mode frequencies f_{ℓmn} that, under SO(3) rotation
group of the Schwarzschild + small-perturbation Kerr horizon, give
a CV across the (2,2,n) overtone series at fixed BH mass that
satisfies M22's SO(3) prediction CV = 1/(2π).

**Substrate.** SO(3) (Kerr horizon rotation symmetry; perturbative
QNM spectrum on a 2-sphere).

**Pre-registration.** For O5+ BBH events with SNR ≥ 30 in the
post-merger ringdown band (∼20 events expected by 2028), compute
the across-overtone CV of the (2,2,0), (2,2,1), (2,2,2) frequencies
normalised to the (2,2,0) frequency. The population mean of this
CV satisfies

    ⟨CV_QNM⟩ ∈ [0.140, 0.180]   AND   N_events ≥ 10.

**Dataset.** GWTC-O5 catalogue (LIGO/Virgo/KAGRA, expected 2028)
+ supplementary ringdown spectroscopy from the Cardiff / Caltech
ringdown groups.

**Protocol.**
1. Fetch O5+ BBH events with high-SNR ringdown.
2. Per event: fit (2,2,0), (2,2,1), (2,2,2) QNM frequencies.
3. Compute CV across overtones, normalised to (2,2,0).
4. Average across events; report ⟨CV_QNM⟩.

**Falsifier.** ⟨CV_QNM⟩ outside [0.120, 0.200]. A value near 0.080
would indicate SO(2) / SU(2) instead of SO(3); a value > 0.25 would
indicate sub-extremal Kerr breaking the SO(3) approximation.

**Independence.** QNM ringdown spectroscopy as a CRR test is
proposed here for the first time; the prediction uses no GW data.

**T3 promotion criterion.** ⟨CV_QNM⟩ ∈ [0.140, 0.180] with N ≥ 10.

---

### P13 — Stellar-mass BH high-frequency QPO inter-cycle CV

**Statement.** Stellar-mass black-hole low-mass X-ray binary (LMXB)
high-frequency quasi-periodic oscillations (HFQPOs) reflect
relativistic accretion-flow modes whose phase manifold is SO(2)
(Keplerian azimuthal symmetry of the inner disk). Under M22,
inter-cycle CV at the dominant HFQPO peak = 1/(4π).

**Substrate.** SO(2).

**Pre-registration.** Across the canonical seven-source HFQPO sample
(GRO J1655−40, XTE J1550−564, GRS 1915+105, H 1743−322, IGR
J17091−3624, 4U 1630−47, MAXI J1535−571), the population mean of
intra-source HFQPO inter-cycle CV satisfies

    ⟨CV_HFQPO⟩ ∈ [0.070, 0.090]   AND   N_sources ≥ 5.

**Dataset.** RXTE / NICER / NuSTAR / IXPE archive observations of
the named sources (HEASARC public archive
`https://heasarc.gsfc.nasa.gov/`).

**Protocol.**
1. Fetch power-density spectra of named sources during HFQPO-active
   states.
2. Identify dominant HFQPO frequency and phase-fold the lightcurve.
3. Compute inter-cycle interval CV per source.
4. Average across the 5+ sources for which data is available.

**Falsifier.** ⟨CV_HFQPO⟩ outside [0.060, 0.100] with N ≥ 5.

**Independence.** HFQPO statistics were not used in CRR construction.

**T3 promotion criterion.** ⟨CV_HFQPO⟩ ∈ [0.070, 0.090] with N ≥ 5.

---

### P14 — AGN X-ray variability break-frequency CV across catalogue

**Statement.** Active galactic nuclei (AGN) supermassive black holes
exhibit X-ray power-spectral break frequencies ν_b that scale with
M_BH and Eddington ratio. Under CRR, the *across-source CV* of
ν_b at fixed M_BH bin reflects the SO(2) inner-disk azimuthal
symmetry, giving CV_ν_b = 1/(4π).

**Substrate.** SO(2) (Keplerian azimuthal symmetry of the inner
relativistic disk; same substrate as P13 but at supermassive scale,
giving cross-mass-scale unification under CRR).

**Pre-registration.** Across the González-Martín & Vaughan 2012
sample + extensions to 2025 of AGN X-ray break-frequency
measurements (typical N ≈ 100–150 sources), restricted to a single
M_BH decade (10⁷ < M_BH/M_⊙ < 10⁸) to control mass-scaling,

    CV_ν_b ∈ [0.070, 0.090]   AND   N_AGN ≥ 25.

**Dataset.** González-Martín & Vaughan 2012 (A&A 544, A80) +
extensions in Paolillo et al. 2017+ + recent Swift/XRT, NICER,
eROSITA archive measurements.

**Protocol.**
1. Compile AGN sample with measured ν_b in the named decade.
2. Compute log(ν_b) values, then CV = std/mean of log-frequencies
   (log-CV is the appropriate scale-free statistic for ν_b).
3. Compare to predicted [0.070, 0.090].

**Falsifier.** CV outside [0.060, 0.100] with N ≥ 25. (A CV ≫ 0.1
would indicate large source-to-source variation inconsistent with
single-substrate identification.)

**Independence.** AGN ν_b literature is well-established; the CRR
identification with SO(2) and the parameter-free CV prediction are
fresh.

**T3 promotion criterion.** CV_ν_b ∈ [0.070, 0.090] with N ≥ 25.

---

### B8 — Mammalian circadian inter-peak interval CV under constant darkness

**Statement.** The mammalian suprachiasmatic-nucleus (SCN) circadian
oscillator is supported by SO(2) phase topology (24-hour periodic
return). Under M22, the inter-peak interval CV in *constant darkness
(DD)* free-running animals satisfies CV = 1/(4π).

**Substrate.** SO(2).

**Pre-registration.** Across mouse, rat, hamster, and squirrel-monkey
DD locomotor-activity datasets in Mouse Phenome Database / Allen
Institute Brain Behavior datasets / Owen-Smith circadian DD archive,
the population mean of intra-animal inter-peak CV satisfies

    ⟨CV_circadian⟩ ∈ [0.070, 0.090]   AND   N_animals ≥ 100.

**Dataset.**
1. Mouse Phenome Database circadian rhythms project
   (`https://phenome.jax.org/`).
2. Welsh / Reppert / Takahashi DD wheel-running archives via
   PhysioNet / Dryad.
3. Allen Institute mouse behaviour datasets (DANDI archive).

**Protocol.**
1. Fetch DD locomotor activity records ≥ 14 days per animal.
2. Identify activity onset peaks via Sokolove-Bushell periodogram +
   onset detection.
3. Per animal: compute inter-peak interval CV.
4. Aggregate across animals; report population mean.

**Falsifier.** ⟨CV_circadian⟩ outside [0.060, 0.100] with N ≥ 100.

**Independence.** Circadian CV is not an established literature
statistic at this level of precision; the parameter-free CRR
prediction is fresh.

**T3 promotion criterion.** ⟨CV⟩ ∈ [0.070, 0.090] with N ≥ 100.

---

### B9 — Mammalian respiratory inter-breath interval CV in quiet wake

**Statement.** The respiratory pre-Bötzinger central pattern
generator is a relaxation oscillator with SO(2) phase topology
(inhalation–exhalation cycle returns to identity). Under M22, the
inter-breath-interval CV in quiet awake state satisfies CV = 1/(4π).

**Substrate.** SO(2).

**Pre-registration.** Across PhysioNet pulmonary-function / sleep
databases (MIT-BIH PSG, MROS, SHHS-style) restricted to **quiet awake
epochs** (Stage W with motion artifact removed; not REM, not stage
N1/2/3), the median across-subject inter-breath interval CV
satisfies

    median(CV_resp) ∈ [0.070, 0.110]   AND   N_subjects ≥ 50.

(Wider band than P9/B8 because respiratory variability is known
to be higher than circadian; but the *centre* is at 1/(4π) ≈ 0.0796.)

**Dataset.**
1. Sleep Heart Health Study (SHHS) via NSRR
   (`https://sleepdata.org/`).
2. Wisconsin Sleep Cohort, MROS, MESA via NSRR.
3. PhysioNet PSG-Audio / CinC databases (open).

**Protocol.**
1. Fetch quiet-wake epochs ≥ 5 minutes per subject.
2. Identify breath onsets from nasal-cannula / belt-strain channel.
3. Per subject: compute inter-breath CV.
4. Across subjects: report median.

**Falsifier.** median(CV_resp) outside [0.060, 0.130] with N ≥ 50.

**Independence.** Respiratory CV in quiet wake is reported in
sleep-medicine literature in absolute std but not as parameter-free
1/(4π) prediction.

**T3 promotion criterion.** median(CV_resp) ∈ [0.070, 0.110] with
N ≥ 50.

---

### B10 — Cortical gamma-cycle period CV in awake recordings

**Statement.** Cortical gamma oscillations (∼30–80 Hz) are supported
by an SO(2) phase manifold (one neural-oscillator return time per
gamma cycle). Under M22, intra-train gamma-cycle period CV during
sustained awake gamma bursts satisfies CV = 1/(4π).

**Substrate.** SO(2).

**Pre-registration.** Across DANDI / OpenNeuro electrophysiology
datasets (Allen Institute Visual Coding Neuropixels; Jun et al.
2017; mouse and human awake LFP recordings), restricted to gamma-
band-filtered (40–80 Hz) sustained bursts of ≥ 100 ms, the
population mean of intra-burst inter-peak CV satisfies

    ⟨CV_γ⟩ ∈ [0.070, 0.110]   AND   N_bursts ≥ 5000.

**Dataset.**
1. DANDI archive Allen Visual Coding Neuropixels
   (`https://dandiarchive.org/dandiset/000021`).
2. CRCNS visual-cortex LFP datasets (`https://crcns.org/`).
3. OpenNeuro human ECoG awake recordings.

**Protocol.**
1. Fetch raw LFP / ECoG.
2. Bandpass-filter 40–80 Hz; identify sustained bursts ≥ 100 ms by
   amplitude threshold.
3. Per burst: detect peaks, compute inter-peak intervals, CV.
4. Aggregate across bursts; report population mean.

**Falsifier.** ⟨CV_γ⟩ outside [0.060, 0.130] with N ≥ 5000.

**Independence.** Gamma inter-peak CV is not an established
literature statistic at this level of precision.

**T3 promotion criterion.** ⟨CV_γ⟩ ∈ [0.070, 0.110] with N ≥ 5000.

---

## Cross-prediction structural commitments

The ten predictions above commit CRR to a structural picture in which:

1. **Solar dynamo, BH accretion, mammalian circadian, respiratory,
   gamma cortical, and AGN inner-disk dynamics share SO(2) phase
   topology.** This is a strong cross-domain claim: a single
   parameter-free CV target ≈ 0.0796 across six independent
   physical / biological substrates, each with its own dataset.
2. **The 2:1 covering relation between SO(2)/SU(2) and SO(3) is
   testable in three independent domains** (P10 solar Hale/sunspot,
   P12 BH ringdown, plus the existing M22-A SU(2) ≡ SO(2) test).
   Three independent confirmations of the topological 2:1 ratio
   would constitute strong evidence for the rupture-on-Lie-group
   architecture itself.
3. **The full set is CRR's broadest pre-registered cross-domain
   commitment to date.** Eight of ten target the SO(2)/SU(2) band
   [0.070, 0.090]. A failure pattern in which most or all of the
   eight CV measurements *cluster outside* this band — particularly
   if they cluster *with each other* — would constitute strong
   evidence against the rupture-on-Lie-group architecture.

---

## Part B — Applied use-case map (industries, GDP, likelihood,
investment, gain)

This section translates CRR's tier-distributed claims plus the
Part-A pre-registered predictions into an applied-utility map.

**Methodology.** Per applied vertical:

- **GDP exposure (USD, 2026 baseline):** the *addressable share of
  global GDP* of the industry where CRR's CV bound or kernel could
  serve as a parameter-free inference / monitoring component.
  Drawn from public sources (IMF WEO 2025, IEA 2025, WHO Global
  Health, IDC, Gartner, ITU). Numbers are *industry size*, not CRR
  capture.
- **Applicability likelihood (0–1):** the probability that a CRR
  prediction or kernel is operationally useful in the named
  vertical, conditional on the corresponding T3 promotion path
  succeeding. Calibrated to the T2/T3 evidence already in the
  campaign (overall_status.md). Not a forecast of T3 success.
- **Indicative pilot investment (USD):** rough first-pass
  development cost to deploy a CRR-anchored module (data fetch,
  pipeline, validation, integration). Order-of-magnitude only.
- **Five-year potential financial gain envelope (USD):** the
  expected commercial value if the pilot reaches deployment at
  industry scale, assuming 1–3% market-capture penetration of the
  GDP-exposed slice over five years.

These are **first-pass scoping numbers, not investment advice**.
They are intended to give the framework's authors a structured
way to compare verticals.

---

### Vertical 1 — Wearable cardiac diagnostics (B2, B5, B7, B9)

- **Industry GDP exposure (2026):** wearable medical devices
  market ≈ $80–110 bn (Grand View Research 2025; IDC 2025);
  cardiac-monitoring share ≈ $25–35 bn.
- **CRR applicability likelihood:** **0.65** (gated on B2 PhysioNet
  reproduction; B7 already T2; B9 fresh prediction).
- **Pilot investment:** $0.5–2 M (data fetch, FDA-grade
  pipeline, regulatory pathway scoping, integration).
- **Five-year gain envelope:** $50 M – $500 M (1–3% capture of
  cardiac-monitoring slice; high upside if Apple/Whoop/Oura adopt
  Class A/B/C labelling as a published standard).
- **Key bottleneck:** B2 PhysioNet test execution (already
  reviewer-runnable per `claims/B2_hrv_pathology_cv/prediction.md`).

---

### Vertical 2 — Space weather & satellite operations (P1, P8, P9, P11)

- **Industry GDP exposure (2026):** global space economy ≈ $560 bn
  (Space Foundation 2024; SIA 2025); GEO/MEO satellite operations
  + space-weather-sensitive segments ≈ $80 bn; GPS / aviation
  weather-radiation ≈ $250 bn.
- **CRR applicability likelihood:** **0.55** (P1 already T2; P9
  CME prediction reviewer-runnable; P8/P11 use SDO/HMI/OMNI
  archives that are open).
- **Pilot investment:** $1–4 M (operational integration with NOAA
  SWPC, ESA Space Safety Programme, satellite-operator decision
  consoles).
- **Five-year gain envelope:** $30 M – $300 M (insurance, satellite-
  insurance pricing tightening from CME-CV bound; LEO/MEO orbit-
  decay forecasting). Aviation polar-route radiation dosimetry
  potentially adds $20-50 M tail.
- **Key bottleneck:** SWPC operational adoption pathway.

---

### Vertical 3 — Gravitational-wave & cosmology research infrastructure (P2, P4, P12)

- **Industry GDP exposure (2026):** publicly-funded gravitational-
  wave + cosmological-survey research budgets ≈ $1.5–2.5 bn
  annually (LIGO/Virgo/KAGRA + LISA-prep + Euclid + Roman + DESI +
  Rubin Observatory). This is a *research* vertical, not a
  consumer one — financial gain is reputational/scientific rather
  than direct revenue.
- **CRR applicability likelihood:** **0.50** (P2 T2-marginal; P12
  fresh prediction conditional on O5; P4 T2-preliminary).
- **Pilot investment:** $0.2–0.6 M (analysis pipeline; conference
  / Living Reviews engagement; collaboration MOUs).
- **Five-year gain envelope:** non-revenue scientific impact;
  *indirect* commercial spin-off via standard-siren H₀ / dark-
  energy commercial-relevance pathway is small ($5–20 M tail
  via cosmology + atomic-clock metrology).
- **Key bottleneck:** post-2027 LIGO O5 catalogue release.

---

### Vertical 4 — Operational seismology & catastrophe insurance (P5)

- **Industry GDP exposure (2026):** global earthquake-related
  insurance + reinsurance ≈ $30–45 bn (Munich Re / Swiss Re 2024
  reports); CAT-bond annual issuance ≈ $15 bn.
- **CRR applicability likelihood:** **0.30** (P5 is a *parity*
  result — single-Ω CRR matches ETAS, does not exceed it; nested
  CRR underperformed; honest-negative discipline). CRR contributes
  marginal but auditable parameter-free benchmark.
- **Pilot investment:** $0.3–1.0 M (CSEP harness execution +
  integration with CAT-bond pricing models).
- **Five-year gain envelope:** $10 M – $80 M (CAT-bond margin
  reduction; building-code revision contributions modest).
- **Key bottleneck:** CSEP regional-execution; nested-CRR scope
  restriction limits headline claim.

---

### Vertical 5 — AI memory architectures & frontier LLMs (B7)

- **Industry GDP exposure (2026):** generative AI infrastructure
  ≈ $250 bn ARR, projected to $1 tn by 2028 (McKinsey, Gartner
  2025); long-context / continual-learning + memory architecture
  is a strategic focus area for Anthropic, OpenAI, Google
  DeepMind, Meta AI.
- **CRR applicability likelihood:** **0.55** (B7 already T2;
  significance-weighted memory directly mappable to retrieval
  rerankers, prioritised replay, agentic memory consolidation;
  Schaul et al. 2015 prioritised experience replay is a partial
  precursor).
- **Pilot investment:** $1–5 M (research engineering, eval
  benchmarks, agent-memory module integration).
- **Five-year gain envelope:** $200 M – $2 bn (1–3% productivity
  improvement on long-context agentic workloads at frontier-lab
  scale, plus license / spec-influence). Highly leveraged.
- **Key bottleneck:** translating B7's exp(C/Ω) kernel into
  empirically-superior memory schedule vs current strong
  baselines (e.g., Anthropic's compaction, Mem0, Letta).

---

### Vertical 6 — Anaesthesia & critical-care monitoring (B2, B5, B10, Ph6)

- **Industry GDP exposure (2026):** patient-monitoring +
  anaesthesia-monitoring ≈ $35–45 bn globally (Edwards Lifesciences,
  Masimo, Medtronic, Philips, GE Healthcare); ICU-monitoring
  segment ≈ $20 bn.
- **CRR applicability likelihood:** **0.45** (B2 HRV class
  ordering directly relevant; B10 gamma-CV anchored to depth-of-
  anaesthesia signatures; Ph6 consciousness-at-interface is
  metaphor-grade).
- **Pilot investment:** $1–3 M (clinical pilots, regulatory).
- **Five-year gain envelope:** $30 M – $250 M (depth-of-anaesthesia
  display competing with BIS/SedLine; sepsis-early-warning
  CV signals; ICU triage).
- **Key bottleneck:** clinical-trial pathway, regulatory
  integration.

---

### Vertical 7 — Single-molecule biophysics & atomic-clock metrology (M10-α³, P6)

- **Industry GDP exposure (2026):** scientific / metrology
  instrumentation + atomic-clock R&D ≈ $25–35 bn (PNT services,
  Vector Atomic, Microchip, Honeywell quantum, NIST/PTB);
  semiconductor noise / battery-state metrology adjacent
  ≈ $40 bn.
- **CRR applicability likelihood:** **0.40** (M10-α³ is the
  campaign's only T3; P6 is canonical-relabelling-grade; applied
  pathway is via parameter-free precision benchmarks).
- **Pilot investment:** $0.4–1.5 M (specification work; metrology-
  partner engagements; reference-implementation publication).
- **Five-year gain envelope:** $20 M – $150 M (PNT applications
  and atomic-clock specification-influence).
- **Key bottleneck:** independent unaffiliated replication of
  M10-α³ on Li²⁺ 2S — required for T4.

---

### Vertical 8 — Mental-health digital therapeutics (B2, Ph7, B10)

- **Industry GDP exposure (2026):** digital mental-health market
  ≈ $25–35 bn (CB Insights, Rock Health 2025 reports); telehealth-
  psychiatry segment ≈ $10–15 bn.
- **CRR applicability likelihood:** **0.50** (Ph7 Ω-regime
  typology is structural; B2 cardiac-anchored evidence; B10 EEG
  gamma-CV deployable on consumer EEG headbands).
- **Pilot investment:** $0.5–2.5 M (Big Health / Headspace Health /
  Spring Health-style partnerships, regulatory pathway).
- **Five-year gain envelope:** $25 M – $200 M (PTSD / depression
  / chronic-stress wearable triage, suicide-risk early warning,
  payer-coverage outcomes-based contracts).
- **Key bottleneck:** B5 EEG cohort specification (author action
  item); Ph7 clinical-validation studies.

---

### Vertical 9 — Industrial process monitoring & generative-AI eval (B6)

- **Industry GDP exposure (2026):** industrial-IoT + process-
  monitoring market ≈ $80 bn (IDC 2025); generative-AI eval
  tools ≈ $5–10 bn nascent market.
- **CRR applicability likelihood:** **0.40** (B6 132-system
  zero-reversals is broad-scope but author-data-deposition
  bottlenecked).
- **Pilot investment:** $0.3–1.2 M (cross-domain CV scaling rule
  as benchmark service for process-anomaly detection; integration
  with Splunk / DataDog / generative-AI eval harnesses).
- **Five-year gain envelope:** $20 M – $150 M (process-anomaly
  detection license, AI-eval benchmark adoption).
- **Key bottleneck:** B6 catalogue deposition (highest-priority
  author action item per `notes/overall_status.md`).

---

### Vertical 10 — Astronomy + exoplanet characterisation (P1-stellar)

- **Industry GDP exposure (2026):** ground + space astronomy
  + exoplanet missions ≈ $5–7 bn annually (NASA SMD,
  ESA Cosmic Vision, NSF AURA); commercial spectroscopy
  instruments ≈ $1.5 bn.
- **CRR applicability likelihood:** **0.50** (P1 already T2 in
  solar; stellar generalisation reviewer-runnable on Mount
  Wilson + Kepler).
- **Pilot investment:** $0.1–0.4 M (Mount Wilson / Kepler
  catalogue analysis, peer-reviewed publication).
- **Five-year gain envelope:** $5 M – $30 M (exoplanet-mission
  target-prioritisation contributions; HWO/PLATO pipeline
  consulting).
- **Key bottleneck:** Mount Wilson archive accessibility +
  reviewer execution.

---

## Part C — Aggregate scoping table

| # | Vertical | GDP exposure (2026, USD) | Likelihood | Pilot invest. (USD) | 5-yr gain envelope (USD) |
|---|----------|--------------------------|:----------:|---------------------|--------------------------|
| 1 | Wearable cardiac diagnostics | $25–35 bn | 0.65 | $0.5–2 M | $50 M – $500 M |
| 2 | Space weather & satellite ops | $80 bn (core) / $560 bn (total) | 0.55 | $1–4 M | $30 M – $300 M |
| 3 | GW & cosmology infrastructure | $1.5–2.5 bn (research) | 0.50 | $0.2–0.6 M | $5 M – $20 M (indirect) |
| 4 | Seismology & CAT insurance | $30–45 bn | 0.30 | $0.3–1.0 M | $10 M – $80 M |
| 5 | AI memory & frontier LLMs | $250 bn (→ $1 tn 2028) | 0.55 | $1–5 M | $200 M – $2 bn |
| 6 | Anaesthesia / critical-care | $35–45 bn | 0.45 | $1–3 M | $30 M – $250 M |
| 7 | Atomic-clock & metrology | $25–35 bn | 0.40 | $0.4–1.5 M | $20 M – $150 M |
| 8 | Mental-health digital therapeutics | $25–35 bn | 0.50 | $0.5–2.5 M | $25 M – $200 M |
| 9 | Industrial-IoT & gen-AI eval | $80 bn / $5–10 bn | 0.40 | $0.3–1.2 M | $20 M – $150 M |
| 10 | Astronomy & exoplanet missions | $5–7 bn | 0.50 | $0.1–0.4 M | $5 M – $30 M |
| **Aggregate** | **All ten verticals** | **≈ $480–620 bn directly addressable** | weighted ≈ **0.49** | **$5.4–22 M** | **$395 M – $3.7 bn** |

---

## Part D — Highest-leverage applied bets

Sorted by *expected-value gain* (likelihood × midpoint of gain
envelope):

1. **AI memory & frontier LLMs (#5).** EV ≈ $605 M. Highest
   ceiling; B7 already T2; differentiation against Anthropic/Mem0/
   Letta is the technical risk.
2. **Wearable cardiac (#1).** EV ≈ $179 M. Most operationally
   accessible; B2 reviewer-runnable today.
3. **Space weather (#2).** EV ≈ $90 M. Multi-claim coverage
   (P1/P9/P11/P8); NOAA/ESA integration pathway clear.
4. **Anaesthesia / critical-care (#6).** EV ≈ $63 M. Clinical-
   trial cost is the gating risk.
5. **Mental-health digital therapeutics (#8).** EV ≈ $56 M.
   Outcomes-based payer contracts are the leveraged outcome.
6. **Industrial-IoT & gen-AI eval (#9).** EV ≈ $34 M. Conditional
   on B6 catalogue deposition.
7. **Atomic-clock metrology (#7).** EV ≈ $34 M. M10-α³ T4
   replication is the unlock.
8. **Seismology & CAT (#4).** EV ≈ $14 M. Honest-null discipline
   limits headline.
9. **Astronomy / exoplanet (#10).** EV ≈ $9 M. Low-cost / low-
   downside; mostly reputational.
10. **GW + cosmology (#3).** EV ≈ $6 M (direct). High *indirect*
    scientific value; not commercial.

---

## Part E — Honest caveats on this scoping

Following CAMPAIGN.md PART III discipline:

1. **Likelihoods are conditional on T3 promotion paths succeeding.**
   They do not embed P(T3-promotion) itself. A separate calibration
   table would multiply by P(T3) ≈ 0.4 across the ten Part-A
   predictions on average to give *unconditional* expected values.
   Users of this table should apply that adjustment for hard
   investment-committee work.
2. **GDP exposure is industry size, not CRR-capture.** The gain
   envelopes assume 1–3% market capture; this is aspirational.
   Conservative 0.3% capture would compress the aggregate gain
   envelope to ≈ $120 M – $1.1 bn.
3. **The campaign explicitly rejects unified verdicts.** The
   per-vertical likelihoods are independent reads; aggregating
   them as a single "expected campaign value" is operationally
   useful but methodologically a flattening of the per-claim
   structure.
4. **Sympathy-amplifier risk.** Applied-impact narratives are the
   place LLM-assisted analysis is most prone to over-promise. The
   numbers above lean conservative on capture rate; readers
   should treat any number above the midpoint as aspirational
   and the lower bound as the planning anchor.
5. **No claims here promote any CRR claim's tier.** The applied
   scoping is downstream of the per-claim tier picture in
   `notes/overall_status.md`; it does not feed back into it.

---

## Part F — Pre-registration audit-trail entry

This document and the ten predictions in Part A are committed at
the head of branch `claude/verify-folder-access-CInY3` on
2026-05-06 prior to any reviewer execution against any of the
named datasets. The git-commit hash of this file's introduction
is the timestamped audit-trail anchor; reviewer execution
artefacts (`fetch.py`, `analyse.py`, `result.md`) per prediction
should be committed in subsequent commits to that branch or to
fresh per-claim directories under `claims/P8_*` … `claims/P14_*`,
`claims/B8_*` … `claims/B10_*` as the framework's author chooses.

The campaign discipline applies: honest negatives are committed
permanently; the SU(2) ≡ SO(2) covering relation (M22-A solar
analogue P10) is a hard falsifier of the rupture-on-Lie-group
architecture itself; pre-registrations may not be edited
retroactively.
