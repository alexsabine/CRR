# CRR application discovery

Ranked commercial-pathway map for the Coherence-Rupture-Regeneration framework, scoped to deployment in 2026 and beyond. Twenty-two candidates survived three filters from an initial Phase 1 list of 135. Engine layer (CRR mathematics: Ω, C·Ω = 1, exp(C/Ω), Z₂ / SO(2) topology) is held internal. Product layer is in peer-reviewed Active Inference and Free Energy Principle vocabulary plus each domain's own established terminology.

Scoring rubric: each axis 1–5, composite max 40. Tier thresholds: ≥32 fast pilot, 24–31 medium pilot, <24 strategic / R&D.

---

## Tier 1: Fast pilots (composite ≥ 32)

### 1. LLM training loss-spike and checkpoint-divergence early-warning service · 38

**Description.** A pre-training observability layer that watches loss, gradient-norm and activation traces in real time, classifies the run as autonomous, regulator-stabilised, or instability-prone, and predicts loss-spike onset 200–2000 optimiser steps in advance.

**Bottleneck.** Frontier-model training runs ($50M–$500M each) lose days of wall-clock to loss spikes that current detection tools (gradient-norm thresholds, EMA smoothers) catch only as the spike commits. There is no parameter-free baseline against which to declare a run "healthy"; each lab fits its own ad hoc thresholds.

**CRR contribution.** Inter-spike-interval CV is anchored at Ω/2 by the canonical claim. Three-class A/B/C diagnostic separates optimiser-induced regulation (Class B) from data-induced shocks (Class A) from instability (Class C). The SO(2) cyclic-LR substrate timing Z₂ gradient-explosion commits is the architectural fingerprint.

**Pre-registered prediction.** Under stable AdamW with WSD schedule and warm-restart-free LR, inter-spike-interval CV across the second half of pre-training clusters within ±15% of 1/(2π) ≈ 0.159 across architectures. Runs that go on to crash show monotone CV broadening crossing 1/(2π) at least 200 steps before the terminal spike.

**Product layer.** "Predictive uncertainty under bounded-precision regularisation"; "free-energy-trajectory anomaly detection during pre-training"; vocabulary: prediction error, surprise, precision-weighting, KL-divergence stability, Markov blanket of optimiser state.

**Natural buyer.** Frontier-model labs (Anthropic, OpenAI, Google DeepMind, Meta AI, Mistral, AI2, Cohere, ByteDance, Alibaba, xAI). Procurement: enterprise contract or paid-tier on top of an open-source v1 plug-in to W&B / MLflow.

**Capital and time.** Time-to-revenue 5 (≤9 months on a paid pilot via the open-source plug-in route). Capital efficiency 5 (<£250k for v1, since the entire first build is analytics over already-emitted training logs).

**Failure modes.** Falsified specifically by: a regulator-stabilised training run (Class B by KL-clip / weight-decay) showing CV above 1/(2π) (a directional reversal). Fastest negative test: compute inter-spike-interval CV on the public Pythia and OLMo training logs and check class ordering against the tightness of their explicitly applied stabilisation.

**Data dependency.** Public: OLMo, Pythia, Llama-3 logs, BLOOM telemetry; partner: customer training logs. No new collection.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | CV = Ω/2 and class diagnostic both load-bearing |
| Data availability | 5 | Public open-LLM logs cover the v1 baseline |
| Buyer clarity | 5 | Frontier labs procure ML-ops tooling against a budget line |
| Regulatory drag | 5 | None |
| Build complexity | 5 | Pure analytics overlay |
| Defensibility | 4 | Pre-registered baseline library plus W&B integration |
| Time-to-revenue | 5 | ≤9 months |
| Capital efficiency | 5 | <£250k |
| **Composite** | **38** | |

---

### 2. Predictive maintenance directional-baseline library for rotating machinery · 36

**Description.** Cross-asset analytics overlay that ranks bearings, gearboxes, pumps and compressors by a parameter-free dispersion baseline, replacing per-plant CV thresholds with a directional A/B/C class library.

**Bottleneck.** The vibration-analytics market ($5B+, SKF, Bently Nevada, AspenTech, OSIsoft) currently fits per-plant CV thresholds from history. False-alarm rates are high; cross-fleet comparison is impossible without recalibration; "early warning" lead time is variable.

**CRR contribution.** The SO(2) (rotor) → Z₂ (spalling commit) architecture is the canonical CRR fingerprint. Healthy CV approximates 1/(4π); active vibration control regulates to Class B; cavitation, surge, dust ingress drive Class C broadening. The directional baseline is invariant across plants.

**Pre-registered prediction.** On the IMS Bearing test-to-failure dataset (Bearing 3 inner race, Bearing 4 roller), inter-spike-spacing CV crosses 1/(4π) at least 12 hours before the published failure timestamp; healthy CV across the run-in 36 hours sits within ±20% of 1/(4π).

**Product layer.** "Anomaly detection with directional baselines"; "predictive maintenance with parameter-free priors"; vocabulary: condition monitoring, prognostic horizon, remaining useful life (RUL), Cpk-equivalent baseline, vibration spectrum kurtosis.

**Natural buyer.** SKF, Siemens Industrial, GE Vernova, Schaeffler, Bently Nevada (Baker Hughes), AspenTech, OSIsoft (AVEVA); end-asset operators (utilities, refineries, wind operators).

**Capital and time.** Time-to-revenue 4 (9–18 months via OEM reseller). Capital efficiency 4 (£250k–£750k for v1 plus first three integrations).

**Failure modes.** Falsified by: a Class C bearing run (active cavitation injected) returning CV below 1/(4π) (directional reversal). Fastest negative test: re-analyse PRONOSTIA dataset bearings 1_3 through 1_7 with class labels and check ordering.

**Data dependency.** Public: NASA IMS Bearing, Case Western Bearing, PRONOSTIA, NREL Wind Plant DB. No new collection for v1.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 5 | SO(2)→Z₂ canonical architecture |
| Data availability | 5 | Multiple public bearing run-to-failure archives |
| Buyer clarity | 5 | Named OEMs with established budget lines |
| Regulatory drag | 4 | ISO 13373, no government approval |
| Build complexity | 5 | Analytics overlay over vibration / acoustic feeds |
| Defensibility | 4 | Class library scales with onboarded fleets |
| Time-to-revenue | 4 | 9–18 months |
| Capital efficiency | 4 | £250k–£750k |
| **Composite** | **36** | |

---

### 3. Wearable cardiac three-class triage (HRV directional baseline) · 35

**Description.** A Class A / B / C autonomic-state index for consumer wearables that distinguishes athletic vagal regulation, healthy autonomous baseline and arrhythmia / dehydration / heat-strain noise broadening, on a single parameter-free scale.

**Bottleneck.** HRV indices on Whoop, Oura, Polar, Garmin are calibrated per-user. Cross-user comparison is unreliable; "recovery score" is opaque; no parameter-free reference scale exists below the level of named-disease detection.

**CRR contribution.** The B2 PhysioNet HRV class-ordering test is the canonical CRR diagnostic. Athlete tightens to Class B (CV < 1/(4π)); healthy resting at Class A (CV ≈ 1/(4π)); arrhythmia / heat-strain shifts to Class C. The directional ordering is the load-bearing claim.

**Pre-registered prediction.** In 24-hour resting-state RR sequences, healthy adult inter-beat-interval CV clusters within ±20% of 1/(4π); endurance-trained cohorts tighten by 20–40%; documented atrial-fibrillation cohorts widen above 1/(2π).

**Product layer.** "Autonomic balance index with parameter-free reference"; "predictive precision under cardiovascular Markov-blanket regulation"; vocabulary: heart rate variability, vagal tone, sympathetic-parasympathetic balance, autonomic regulation, cardiovascular surprise.

**Natural buyer.** Whoop, Oura, Polar, Garmin, Fitbit; secondary: Apple Health partners, telehealth platforms (Hims, Teladoc), corporate-wellness vendors.

**Capital and time.** Time-to-revenue 4 (9–18 months via SDK or licence). Capital efficiency 5 (<£250k).

**Failure modes.** Falsified by: an endurance-trained cohort showing CV above the healthy-resting cohort, with both stratified by age. Fastest negative test: PhysioNet rank-sum on healthy vs CHF vs AF cohorts, reproducing the canonical B2 protocol.

**Data dependency.** Public: PhysioNet (NSR, AFDB, CHFDB). Plus partner wearable data for production tuning.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 5 | B2 canonical class-ordering test directly |
| Data availability | 5 | PhysioNet open |
| Buyer clarity | 4 | Multiple OEMs but consumer product layer crowded |
| Regulatory drag | 4 | Wellness scale, FDA general-wellness guidance |
| Build complexity | 5 | Analytics overlay |
| Defensibility | 3 | Easy to copy once published; partnerships are the moat |
| Time-to-revenue | 4 | 9–18 months |
| Capital efficiency | 5 | <£250k |
| **Composite** | **35** | |

---

### 4. RL training-stability instrumentation (PPO / DPO / GRPO Class A vs B) · 35

**Description.** Companion to candidate 1: extends the CRR class diagnostic to reinforcement-learning fine-tuning runs, distinguishing KL-regulated stable training (Class B) from reward-hacking instability (Class C) and from autonomous exploration (Class A).

**Bottleneck.** RLHF / DPO / GRPO training is famously unstable; existing tools (KL-divergence, reward variance, ELO score) report state but offer no parameter-free criterion for "this run is regulated" vs "drift toward collapse". Reward-hacking is detected after damage.

**CRR contribution.** Inter-policy-update KL-divergence CV anchored at Ω/2; Class B regulation by KL-clip pulls CV below 1/(2π); reward-hacking drives Class C broadening; beauty function peak C* − Ω flags the optimal early-stopping window before mode collapse.

**Pre-registered prediction.** On TRL-trained PPO runs of sub-10B models with default hyperparameters, KL-divergence CV across optimisation steps clusters near 1/(2π); enabling KL-clip moves CV to 1/(4π) ± 20%; observed reward-hacking collapses raise CV by ≥1.5× before final divergence.

**Product layer.** "Stability monitoring under bounded KL precision"; "free-energy regularisation diagnostic for policy gradient methods"; vocabulary: KL stability, mode collapse, reward hacking, optimal stopping, regularised policy gradient.

**Natural buyer.** Same labs as candidate 1; additionally Vercel-AI / open-source RL framework maintainers (TRL, OpenRLHF, Tunix, verl).

**Capital and time.** Time-to-revenue 4 (9–18 months). Capital efficiency 5 (<£250k bundled with candidate 1).

**Failure modes.** Falsified by: a KL-clipped run (Class B) showing CV above an unclipped run (Class A) on the same task. Fastest negative test: rerun the open TRL examples with and without KL-clip and compare CV ordering.

**Data dependency.** Public OpenRLHF logs, plus partner traces.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | Class diagnostic plus beauty peak |
| Data availability | 5 | Open RLHF training logs |
| Buyer clarity | 4 | Same labs as C01 |
| Regulatory drag | 5 | None |
| Build complexity | 5 | Analytics overlay |
| Defensibility | 3 | Easy to copy; bundled with C01 strengthens |
| Time-to-revenue | 4 | 9–18 months |
| Capital efficiency | 5 | <£250k |
| **Composite** | **35** | |

---

## Tier 2: Medium pilots (composite 24–31)

### 5. Tokamak ELM precursor / disruption-prediction service · 31

**Description.** A real-time inference engine for plasma-control systems that classifies operating regime and flags edge-localised-mode commit ≤100 ms before onset.

**Bottleneck.** ITER-relevant tokamaks need pre-emptive ELM detection but current neural-network classifiers (BES-ELMnet, DIII-D ConvNets) are dataset-specific and lack a parameter-free cross-machine baseline. Type-I ELMs at ITER scale would damage divertor tiles within seconds without mitigation.

**CRR contribution.** Z₂ (ELM commit) on SO(2) (pedestal turbulence) is a textbook fingerprint of H-mode ELM physics. Class A Type-I; Class B small-ELM regime; resonant-magnetic-perturbation suppression yields Class B with CV → 0; pellet pacing tightens CV to Class B. Beauty peak at C* − Ω is precisely the prediction horizon.

**Pre-registered prediction.** In DIII-D BES inter-ELM-interval traces at fixed pedestal pressure, Type-I H-mode CV sits within ±15% of 1/(4π); RMP-suppressed shots show CV ≤ 0.02; pellet-pacing brings CV below 1/(4π) by 30–50%.

**Product layer.** "Pedestal-stability anomaly detection"; "free-energy precursor diagnostics for high-confinement plasmas"; vocabulary: edge pedestal, H-mode confinement, RMP suppression, divertor heat flux mitigation.

**Natural buyer.** ITER Organization, EUROfusion, Commonwealth Fusion Systems, Tokamak Energy, TAE Technologies, Helion, General Fusion, UKAEA, PPPL, ASDEX-Upgrade collaboration.

**Capital and time.** Time-to-revenue 3 (18–24 months via collaboration grants). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: RMP-suppressed shot returning CV above Type-I baseline. Fastest negative test: re-analyse DIII-D 2018–2024 RMP campaigns with class labels.

**Data dependency.** DIII-D, JET, MAST-U, ASDEX-Upgrade public archives; ITER access via collaboration agreement.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 5 | Z₂ on SO(2) plus beauty peak both load-bearing |
| Data availability | 4 | DIII-D, JET, MAST-U publicly available |
| Buyer clarity | 3 | Sector R&D-heavy, grant-driven procurement |
| Regulatory drag | 5 | No external regulation at R&D stage |
| Build complexity | 3 | Real-time integration with plasma-control systems |
| Defensibility | 5 | Pre-registration plus class library, publication-driven trust |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **31** | |

---

### 6. Space-weather Hale-cycle anchored forecasting service · 30

**Description.** A 22-year solar Hale-cycle baseline forecast published as a parameter-free reference for satellite operators, polar airline routing, GPS providers and space-weather insurers.

**Bottleneck.** NOAA SWPC and ESA SSA solar-cycle predictions fit nonlinear regression to historical SSN; predictions vary with model. Operators (Iridium, Starlink, polar airlines) lack a parameter-free reference for orbit-decay budgeting and radiation-dose planning.

**CRR contribution.** P1 canon: solar Hale CV at 1/(4π) within the SILSO empirical band [0.0767, 0.0820]. SO(2) cycle → Z₂ polarity-reversal commit. Provides the parameter-free baseline against which operational departures lead by 9–18 months.

**Pre-registered prediction.** SC25 + SC26 paired Hale CV computed end-of-2030 falls in the band [0.075, 0.085]; SC25 minimum-amplitude departures from 1/(4π) by more than 15% indicate Class C transition implying lower operational confidence.

**Product layer.** "Bayesian solar-cycle anomaly detection"; "free-energy precursor for geomagnetic storms"; vocabulary: SSN, SILSO, Hale polarity reversal, geomagnetic Kp, polar HF blackout.

**Natural buyer.** NOAA SWPC contractors (Lockheed Martin Space, Ball Aerospace), ESA SSA, satellite operators (Iridium, SpaceX Starlink, OneWeb, Eutelsat), polar-route airlines (Air New Zealand, Cathay Pacific), space-weather insurance (AXA Climate, AON parametric).

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: completed SC25 (2030) Hale CV outside the [0.075, 0.085] band. Fastest negative test: rolling SC25 north-hemisphere CV update at every annual SILSO release.

**Data dependency.** SILSO, NOAA OMNI, GOES, SDO, all open.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 5 | P1 T2 canon |
| Data availability | 5 | SILSO, OMNI, GOES open |
| Buyer clarity | 3 | Government contractors plus insurance niche |
| Regulatory drag | 4 | Government procurement bureaucracy not regulation |
| Build complexity | 3 | Real-time integration with NOAA feeds |
| Defensibility | 4 | Pre-registration plus 22-year cycle baseline distinctive |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **30** | |

---

### 7. Power-grid frequency-stability anomaly detector for high-renewables grids · 30

**Description.** A class-shift early-warning overlay for transmission system operators that detects loss of regulating inertia ahead of relay trip, distinct from RoCoF threshold breach.

**Bottleneck.** ENTSO-E continental Europe inertia is falling as fossil units retire; ENTSO-E modelling identifies an increase in scenarios where |RoCoF| exceeds 1 Hz/s post-split. Synthetic-inertia services exist but lack a parameter-free directional metric for "have we regulated enough?"

**CRR contribution.** SO(2) (50 / 60 Hz cycle) → Z₂ (under-frequency relay trip / system split) is canonical. Class A baseline; Class B regulated grid; Class C high-renewables grid that has lost regulator capacity. The class shift is detectable before RoCoF threshold.

**Pre-registered prediction.** In synchronously-connected segments with > 70% inverter-based generation and < 0.5 GVA·s/MW inertia, inter-excursion-interval CV widens above 1/(2π) compared with a < 30% IBR baseline; reversion under synthetic-inertia services tightens CV back below baseline.

**Product layer.** "Inertia-aware frequency-stability monitoring"; "free-energy excursion detection for power systems"; vocabulary: RoCoF, inertia, synthetic inertia, frequency containment reserve, fast frequency response.

**Natural buyer.** ENTSO-E TSOs (50Hertz, Eirgrid, National Grid ESO, RTE, Terna, Statnett, TenneT), NERC reliability coordinators, Hitachi Energy, GE Vernova, Siemens Energy, ABB grid-stability product lines.

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: a high-renewables grid (Eirgrid 2024+, South Australia) showing CV below a low-renewables comparator. Fastest negative test: ENTSO-E transparency-portal frequency data, segmented by SNSP (system non-synchronous penetration), classified.

**Data dependency.** ENTSO-E transparency portal, BPA Open µPMU, NERC Bulk-Electric-System data.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 5 | SO(2)→Z₂ canonical, class shift maps to inertia decline |
| Data availability | 4 | ENTSO-E transparency, public PMU |
| Buyer clarity | 4 | TSOs procure stability services |
| Regulatory drag | 3 | Grid-code certification, manageable |
| Build complexity | 4 | Analytics plus PMU / SCADA integration |
| Defensibility | 4 | Class library plus regulator-grade audit trail |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **30** | |

---

### 8. CAT-bond / parametric-reinsurance pricing engine · 30

**Description.** Cross-domain Class C dispersion baseline for catastrophe-bond and parametric-reinsurance pricing, supplementing dataset-specific fits with a directional ordering invariant from the framework's 132-system catalogue.

**Bottleneck.** The 2025 CAT-bond market is at $61.3B outstanding with $25.6B issued in 2025. Pricing depends on dataset-specific historical fits; parametric triggers (~7% of issuance and growing) lack a single cross-peril dispersion benchmark. Models vary by basin, peril, structurer.

**CRR contribution.** B6 cross-domain claim: Class C noise-dominated systems (ENSO, monsoon, hurricane, EQ) carry directional CV ordering by basin substrate symmetry. Provides a parameter-free dispersion prior independent of bond-specific fits.

**Pre-registered prediction.** Atlantic-hurricane parametric-trigger inter-arrival CV in 1990–2025 HURDAT2 lies above 1/(2π); Pacific basin (different substrate) sits in a directionally distinct cluster; the ordering is invariant under re-binning at 5, 10, 20-year windows.

**Product layer.** "Cross-peril tail-risk dispersion baseline"; "free-energy parametric-trigger pricing under structural-uncertainty priors"; vocabulary: CRESTA zones, exceedance probability, parametric trigger, modelled annual loss, structuring spread.

**Natural buyer.** Munich Re, Swiss Re, Hannover Re, RenaissanceRe, AXIS, Everest Re; ILS managers (Twelve Capital, ILS Capital, Schroders Capital, Stone Ridge); structurers (Aon Securities, Guy Carpenter, GC Securities).

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: Atlantic-basin trigger CV ranking below Pacific-basin under same-magnitude trigger threshold. Fastest negative test: Artemis CAT-bond DB historical-trigger inter-arrival CV computed by basin and ordered.

**Data dependency.** NOAA HURDAT2, USGS ComCat, ECMWF reanalysis, Artemis CAT-bond DB.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | B6 cross-domain directional baseline load-bearing |
| Data availability | 4 | NOAA, USGS, Artemis open |
| Buyer clarity | 3 | Reinsurance quants procure quietly |
| Regulatory drag | 4 | Reinsurance accounting, no state-level regulator |
| Build complexity | 4 | Analytics plus bond-pricing harness |
| Defensibility | 5 | Pre-registration plus cross-domain library distinctive |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **30** | |

---

### 9. Atrial-fibrillation onset early-warning module · 29

**Description.** A 30–90 minute pre-AF directional warning that runs on implantable cardiac monitors and patch monitors, distinguishing maximally-informative (beauty-peak) windows from steady-state.

**Bottleneck.** Existing AF prediction is dominated by black-box ML on HRV features that needs cohort-specific tuning, with PPV ranges that vary by population. There is no parameter-free directional baseline.

**CRR contribution.** Class B → A → C destination. As autonomic regulation collapses pre-AF, RR-CV drifts from vagal Class B toward 1/(4π) autonomous baseline and broadens into Class C. Beauty function predicts the maximally-informative window at C* − Ω, the last quiet hour before episode onset.

**Pre-registered prediction.** In the pre-AF 90 minute window in PhysioNet AFDB, RR-CV trajectory is monotone and crosses 1/(2π) at least 30 minutes before onset in ≥70% of episodes; reverses on successful sinus-rhythm restoration.

**Product layer.** "Predictive precision under autonomic-blanket regulation"; "free-energy precursor for arrhythmia"; vocabulary: heart rate variability, autonomic nervous system, sinus rhythm, paroxysmal AF.

**Natural buyer.** AliveCor, iRhythm (Zio), Boston Scientific (LUX-Dx), Medtronic (LINQ II), arrhythmia clinics, AF-screening telehealth.

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: pre-AF CV trajectory not monotone, or absent class shift. Fastest negative test: AFDB rank-sum on annotated pre-AF segments.

**Data dependency.** PhysioNet AFDB, MIT-BIH; partner ICM data for production.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 5 | Destination plus beauty peak both load-bearing |
| Data availability | 4 | PhysioNet plus partner ICM |
| Buyer clarity | 4 | Implant and patch monitor market mature |
| Regulatory drag | 2 | FDA SaMD plus CE mark |
| Build complexity | 4 | Analytics plus clinical-validation cohort |
| Defensibility | 4 | Pre-registration audit trail differentiates from ML competitors |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **29** | |

---

### 10. Quantum-error-correction logical-qubit cycle diagnostic · 29

**Description.** A FPGA-stack-integrated diagnostic that confirms below-threshold logical-qubit operation on a parameter-free CV baseline, independent of code-distance scaling fits.

**Bottleneck.** Below-threshold confirmation in surface-code experiments (Google Willow 2024, IBM 2025 multi-round) currently relies on observing logical-error-rate decreasing with code distance. There is no parameter-free baseline at which inter-logical-error CV settles, so "below threshold" is empirical-fit-relative.

**CRR contribution.** Z₂ (logical-error commit) on SO(2) (gate cycle). Class A baseline = below-threshold; Class B regulated by decoder; Class C above-threshold. Inter-logical-error-interval CV anchors at 1/(4π) below threshold; broadens above.

**Pre-registered prediction.** In Willow d=3,5,7 surface-code experiments with logical-error-rate published, inter-logical-error-interval CV at d=5 and d=7 lies within ±25% of 1/(4π); above-threshold d=3 shows CV broadening above.

**Product layer.** "Below-threshold confirmation under stochastic-syndrome priors"; "free-energy diagnostic for surface-code logical qubits"; vocabulary: logical error rate, surface code, syndrome decoder, fault-tolerant threshold, code distance.

**Natural buyer.** Riverlane (UK QEC stack vendor with Deltaflow / Deltakit, natural integration partner), IBM Quantum, Google Quantum AI, OQC, Quantinuum, IonQ, PsiQuantum.

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: above-threshold d=3 logical qubit showing CV at or below the d=7 baseline. Fastest negative test: re-analyse Willow public syndrome traces and check class ordering.

**Data dependency.** Public QEC papers (Willow, IBM, OQC) plus partner integration.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | Z₂ on SO(2), below-threshold confirmation novel |
| Data availability | 4 | QEC papers plus partner |
| Buyer clarity | 3 | Niche but well-funded, Riverlane natural partner |
| Regulatory drag | 5 | None |
| Build complexity | 3 | FPGA / decoder-stack integration |
| Defensibility | 4 | Pre-registration plus class library, technical moat |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **29** | |

---

### 11. Gait-clinic Huntington's / Parkinson's destination triage · 28

**Description.** A wearable-and-walkway analytics module for gait clinics that predicts not direction-of-change but destination of CV, anchored at 1/(4π) for fully de-regulated stride-time.

**Bottleneck.** Gait analytics in HD / PD trials currently report direction (worsening or stable) but lack a quantitative endpoint for "how far has regulation collapsed?" Trial endpoints lean on cohort-fit rates of change.

**CRR contribution.** Stride-CV destination at 1/(4π) as cortical regulation removed (canon-illustrated via Hausdorff PhysioNet gait DB). Predicts not direction but end-state. Beauty peak at C* − Ω identifies the pre-symptomatic phase carrying maximal trial-endpoint information.

**Pre-registered prediction.** In pre-symptomatic HD gene carriers within 5 years of motor onset, stride-CV trajectory regresses linearly with UHDRS-TMS toward 1/(4π); rate of approach correlates with CAG-repeat length (r > 0.4).

**Product layer.** "Trajectory-to-deregulation endpoint for movement disorders"; "free-energy biomarker under cortico-basal-ganglia precision loss"; vocabulary: stride time, gait variability, prodromal Huntington's, motor reserve, UHDRS.

**Natural buyer.** HD-clinic centres-of-excellence (Roche / Wave Life HD trials, Triplet), Cure HD Initiative, MJFF Parkinson's; gait-analysis vendors APDM (Clario), Mobility Lab; trial-endpoint CRO partners (IQVIA, Parexel).

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: HD gene carriers with longer CAG repeats showing slower CV approach to 1/(4π) than shorter-repeat carriers, holding age constant. Fastest negative test: re-analyse PhysioNet gait DB for Hausdorff cohorts with CAG annotation.

**Data dependency.** PhysioNet gait DB, plus partner trial substudies (Enroll-HD, PPMI).

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 5 | Destination prediction load-bearing, canon-illustrated |
| Data availability | 5 | PhysioNet gait DB plus public trial substudies |
| Buyer clarity | 2 | Niche, mostly trial-endpoint vendors |
| Regulatory drag | 3 | FDA biomarker qualification, manageable |
| Build complexity | 3 | Wearable analytics plus clinical-validation |
| Defensibility | 4 | Pre-registration plus destination claim distinctive |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **28** | |

---

### 12. Sleep-stage transition timing for PSG and consumer sleep · 28

**Description.** A sleep-architecture quality index based on CV of inter-stage-transition intervals, deployable on PSG hardware and consumer wearables.

**Bottleneck.** Sleep-stage scoring is rule-based (R&K / AASM); transition-timing distributions are descriptive but not anchored. Consumer wearables compute "deep sleep minutes" without a directional health prior.

**CRR contribution.** SO(2) (ultradian cycle) → Z₂ (NREM / REM commit). Class A baseline; Class B circadian-entrained; OSA Class C broadening. CV of inter-stage-transition-interval as parameter-free architecture-quality index.

**Pre-registered prediction.** In SHHS healthy adult cohort, inter-N3-N2-CV across the night clusters within ±20% of 1/(2π); moderate-to-severe OSA cohorts show CV ≥ 1.4 × healthy; CPAP at adherent users restores CV to within 1.1 × healthy.

**Product layer.** "Sleep-architecture stability index"; "predictive precision under ultradian-blanket regulation"; vocabulary: NREM / REM cycle, sleep efficiency, AHI, CPAP adherence, sleep-onset latency.

**Natural buyer.** Philips Respironics, ResMed, Compumedics, Natus; consumer sleep tech (Eight Sleep, Whoop sleep, Oura sleep, Withings).

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: severe-OSA cohort CV at or below healthy cohort, holding age and BMI constant. Fastest negative test: SHHS / MESA NSRR rank-sum on stratified cohorts.

**Data dependency.** SHHS, MESA, NSRR open archives.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | SO(2)→Z₂, class diagnostic |
| Data availability | 5 | NSRR open |
| Buyer clarity | 3 | PSG slow procurement, consumer faster |
| Regulatory drag | 3 | Wellness fast, PSG FDA 510(k) |
| Build complexity | 4 | Analytics overlay |
| Defensibility | 3 | Class library, modest market |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **28** | |

---

### 13. Battery thermal-runaway precursor monitor · 27

**Description.** A BMS-integrated diagnostic that detects pre-runaway class shift in Li-ion cells 5–50 cycles before thermal event, deployable on EV packs and stationary-storage modules.

**Bottleneck.** Thermal-runaway precursor detection is dominated by impedance-spectroscopy heuristics tuned per chemistry; cross-pack baseline comparison is poor; field-event prediction lead times vary widely.

**CRR contribution.** SO(2) (charge / discharge cycle) → Z₂ (cell internal-short ignition) architecture. Class A → C destination as regulating chemistry depletes. Inter-impedance-spike-interval CV broadens monotonically pre-event.

**Pre-registered prediction.** In NREL Li-ion abuse-test cohorts, healthy-cycling impedance-spike-CV clusters within ±25% of 1/(4π); precursor cells show monotone CV broadening crossing 1/(2π) at least five charge / discharge cycles before thermal event.

**Product layer.** "Battery-state predictive precision"; "free-energy precursor for thermal runaway"; vocabulary: state of health, internal short circuit, thermal runaway propagation, BMS impedance spectroscopy.

**Natural buyer.** Tesla, BYD, CATL, LG Energy Solution, Northvolt, Form Energy, Fluence, Wärtsilä; BMS-chip vendors (Analog Devices, NXP, Texas Instruments).

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: pre-runaway cell CV trajectory non-monotone, or precursor cells indistinguishable from healthy at cycle-50 ahead. Fastest negative test: re-analyse NREL battery DB abuse-test cohorts.

**Data dependency.** NREL battery DB, EUCAR, plus partner BMS telemetry.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | SO(2)→Z₂ clean, CV destination prediction load-bearing |
| Data availability | 4 | NREL plus partner BMS |
| Buyer clarity | 4 | EV BMS and stationary-storage operators motivated |
| Regulatory drag | 3 | UN ECE R100, IEC 62619, UL 9540A |
| Build complexity | 3 | Analytics plus BMS firmware integration |
| Defensibility | 3 | Class library, BMS market competitive |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **27** | |

---

### 14. Additive-manufacturing layer-defect monitoring · 27

**Description.** Process-monitoring overlay for laser powder-bed-fusion and binder-jet additive systems that distinguishes process-drift Class B (regulated) from contamination Class C in real time.

**Bottleneck.** AM process monitoring (in-situ photodiode / acoustic / thermography) reports state but lacks a parameter-free baseline for "this machine is in spec". Per-machine fits are required.

**CRR contribution.** Z₂ (defect-event commit) on SO(2) (recoater scan / build-plate rotation). CV of inter-defect-event-interval baseline to 1/(2π) distinguishes process drift (regulated, Class B) from oxygen-rich contamination (broadening, Class C).

**Pre-registered prediction.** In NIST AM Bench laser powder-bed-fusion under nominal Ar atmosphere, inter-spatter-event-CV clusters at 1/(2π) ± 20%; oxygen-rich excursion (≥ 2% O₂) drives CV broadening above 1.4 × baseline within 50 layers.

**Product layer.** "In-process anomaly detection with directional baselines"; "free-energy process-control diagnostic for additive manufacturing"; vocabulary: melt-pool monitoring, recoater scoring, oxygen monitoring, AS9100 process control.

**Natural buyer.** GE Additive, EOS, Trumpf, Carbon, Velo3D, Markforged, SLM Solutions; aerospace operators (GE Aviation, Airbus); medical-device printers.

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: Class C contamination experiment showing CV at or below baseline. Fastest negative test: NIST AM Bench artefact-cohort CV ordering.

**Data dependency.** NIST AM Bench, Senvol Database, plus partner machine logs.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | SO(2)→Z₂ clean, defect-cluster CV directly measurable |
| Data availability | 4 | NIST AM Bench plus partner |
| Buyer clarity | 3 | AM-process-monitoring market modest |
| Regulatory drag | 4 | ASTM F42, AS9100 if aerospace |
| Build complexity | 3 | Sensor plus analytics integration |
| Defensibility | 3 | Class library, modest market |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **27** | |

---

### 15. Financial market regime-shift early warning · 26

**Description.** A buy-side overlay for hedge funds and bank risk teams that flags Class A → C transitions in vol-regime statistics ahead of regime-flip events.

**Bottleneck.** Vol-regime change detection (HMMs, Markov-switching models, GARCH) is widely available but tuned post-hoc to historical regimes. Pre-flip directional warnings carry edge but degrade as competitors adopt the same techniques.

**CRR contribution.** Class C diagnostic on inter-flash-event interval; CV drifts directionally into Class C pre-regime-flip; beauty peak C* − Ω as informative pre-flip moment.

**Pre-registered prediction.** In S&P-500 daily realised volatility 2000–2025, inter-VIX-spike-CV across 5-day rolling windows widens monotonically by ≥ 1.3× across the 10 windows preceding documented regime-shift dates (e.g. 2008-09-15, 2020-03-09, 2022-02-24).

**Product layer.** "Vol-regime stability under bounded-precision priors"; "free-energy regime-shift detection for systematic strategies"; vocabulary: realised volatility, regime-switching, jump diffusion, tail-risk hedging.

**Natural buyer.** Hedge funds (Two Sigma, Citadel, Renaissance, Man AHL, AQR), bank risk teams, MSCI risk products, Bloomberg / Refinitiv quant terminals.

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: pre-regime-shift windows showing CV non-monotone or below baseline. Fastest negative test: open TAQ data with 5-day rolling CV computed across documented regime-flip dates.

**Data dependency.** TAQ, Bloomberg, OptionMetrics; partner buy-side data for production.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 3 | Class C noise-dominated, directional but markets crowded |
| Data availability | 4 | TAQ, Bloomberg |
| Buyer clarity | 3 | Quant funds buy quietly |
| Regulatory drag | 4 | Buy-side, no state regulator on analytics |
| Build complexity | 4 | Analytics plus back-test harness |
| Defensibility | 2 | Quant edge erodes once published |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **26** | |

---

### 16. Speech-pause dementia screening for telehealth · 25

**Description.** A telehealth-friendly speech-analytics module that runs on a 60-second narrative recording and returns a CV-of-inter-pause-interval class score for cognitive-decline screening.

**Bottleneck.** Speech-based cognitive screening (Linus Health, Canary Speech, Cogniciti) is deep-learning-driven and needs cohort-specific tuning. No parameter-free directional baseline.

**CRR contribution.** Class C diagnostic on speech-pause CV in cognitive decline; SO(2) (intonation envelope) → Z₂ (pause commit). Autonomic-control loss broadens inter-pause CV directionally.

**Pre-registered prediction.** In DementiaBank Pitt cookie-theft narratives, healthy-control inter-pause CV clusters at 1/(4π) ± 25%; AD cohort widens to ≥ 1.4 × healthy; MCI cohort sits in between with directional ordering preserved.

**Product layer.** "Speech-temporal anomaly screening"; "free-energy precursor under cortico-bulbar precision loss"; vocabulary: speech-pause distribution, narrative speech, cognitive-screening biomarker, MMSE-correlated.

**Natural buyer.** Linus Health, Canary Speech, Ellipsis Health, Cogniciti, NHS dementia-pathway services; insurance telehealth (Cigna, Aetna).

**Capital and time.** Time-to-revenue 3 (18–24 months). Capital efficiency 3 (£750k–£2M).

**Failure modes.** Falsified by: AD cohort CV at or below healthy in Pitt corpus. Fastest negative test: DementiaBank Pitt rank-sum on healthy / MCI / AD cohorts.

**Data dependency.** DementiaBank (Pitt, Lu, ADReSSo), partner telehealth data.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 3 | Class diagnostic, SO(2)→Z₂ less crisp than gait |
| Data availability | 4 | DementiaBank open |
| Buyer clarity | 3 | Telehealth dementia screening crowded |
| Regulatory drag | 2 | FDA 510(k) for screening claims |
| Build complexity | 4 | Analytics overlay over speech pipeline |
| Defensibility | 3 | Class library |
| Time-to-revenue | 3 | 18–24 months |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **25** | |

---

### 17. Anaesthesia-depth burst-suppression directional baseline · 24

**Description.** An adjunct EEG index for the operating-room monitor market that classifies cortical burst-suppression regime against a parameter-free directional baseline.

**Bottleneck.** BIS index (Medtronic) and SedLine (Masimo) are proprietary spectral indices; neither offers a directional class scale, and inter-patient variability is significant. Anaesthetists titrate to BIS but lack a class-shift indicator distinct from the index value.

**CRR contribution.** Cortical Z₂ (burst vs suppression) on SO(2) infraslow rhythm. Inter-burst-interval CV under deepening propofol shifts from awake Class A → regulated Class B → suppressed-isolated Class C. Beauty peak at C* − Ω is the operationally informative titration sweet-spot.

**Pre-registered prediction.** At MAC ≈ 1.0 sevoflurane in MIMIC-IV / OASIS-B EEG records, inter-burst-CV crosses below 1/(4π); awake baseline above 1/(2π); deep suppression below 0.05.

**Product layer.** "Cortical-precision titration index"; "free-energy diagnostic for anaesthetic depth"; vocabulary: BIS, burst suppression, MAC, processed-EEG, awareness under anaesthesia.

**Natural buyer.** Medtronic (BIS), Masimo (SedLine), Mindray, GE Healthcare, Drager, Philips Healthcare.

**Capital and time.** Time-to-revenue 2 (24–36 months). Capital efficiency 2 (£2M–£5M).

**Failure modes.** Falsified by: deep-suppression cohort showing CV above awake-cohort. Fastest negative test: MIMIC-IV / OASIS-B retrospective cohort rank-sum.

**Data dependency.** MIMIC-IV, OASIS-B, BISDB; partner OR data for clinical study.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | Class diagnostic, beauty peak as titration sweet-spot |
| Data availability | 4 | MIMIC-IV / BISDB |
| Buyer clarity | 3 | Medical-monitor OEMs slow procurement |
| Regulatory drag | 2 | FDA 510(k) class II |
| Build complexity | 3 | Analytics plus clinical-validation |
| Defensibility | 4 | Pre-registration plus class library |
| Time-to-revenue | 2 | 24–36 months |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **24** | |

---

### 18. Semiconductor manufacturing process-control overlay · 24

**Description.** Fab-floor analytics overlay that supplements Cpk-based statistical-process-control with a directional CV class baseline detectable 50–200 wafers earlier than threshold-based detection.

**Bottleneck.** SPC + Cpk in fabs is per-tool, per-process; cross-fab benchmarking is hard; modern AI-enhanced SPC products (NEXSPC, iFactory) accelerate detection but still rely on dataset-specific fits.

**CRR contribution.** SO(2) (stage motion / scan) → Z₂ (alignment-mark capture commit) on lithography overlay. CRR CV-anchored baseline replaces per-fab Cpk fitting with cross-fab parameter-free directional ordering.

**Pre-registered prediction.** Under nominal NXT-class scanner operation (recipe-anonymised), inter-overlay-residual-spike-CV clusters at 1/(4π) ± 20%; chuck-temperature drift induces Class C broadening that crosses 1/(2π) at least 50 wafers before the current Cpk threshold trip.

**Product layer.** "Process-control directional-baseline overlay"; "free-energy fault-detection-and-classification (FDC) augmentation"; vocabulary: Cpk, FDC, SPC chart, chuck thermal management, alignment metrology.

**Natural buyer.** ASML (virtual-metrology partner), KLA, Lam Research, Applied Materials, Tokyo Electron; fabs (TSMC, Intel, Samsung Foundry, GlobalFoundries).

**Capital and time.** Time-to-revenue 2 (24–36 months, fab cycles). Capital efficiency 2 (£2M–£5M).

**Failure modes.** Falsified by: a deliberate chuck-thermal-drift experiment that fails to produce CV broadening before Cpk threshold. Fastest negative test: partner fab retro-data on chuck-thermal logs.

**Data dependency.** Mostly proprietary; partner-data dependent for v1.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | SO(2)→Z₂ canonical for stage-motion alignment commit |
| Data availability | 2 | Most process data behind fab confidentiality |
| Buyer clarity | 3 | Equipment OEMs short list |
| Regulatory drag | 4 | SEMI standards |
| Build complexity | 3 | Integration with FDC / SPC stack |
| Defensibility | 4 | Pre-registration plus class library |
| Time-to-revenue | 2 | 24–36 months |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **24** | |

---

## Tier 3: Strategic / R&D bets (composite < 24)

### 19. Continuous-EEG seizure-onset early warning · 22

**Description.** A real-time pre-ictal class-shift detector for chronic ECoG and scalp-EEG monitoring, predicting seizure onset 5–60 minutes ahead.

**Bottleneck.** Seizure-prediction algorithms struggle with per-patient calibration and high false-alarm rates; FDA-cleared products (NeuroPace RNS, Epitel REMI) do detection not prediction.

**CRR contribution.** Class A → C transition in inter-spike-CV on cortical SO(2) substrate. Beauty peak at C* − Ω predicts pre-ictal window. Per-patient calibration remains an open challenge.

**Pre-registered prediction.** In Mayo / NeuroVista chronic ECoG, inter-spike-CV in the pre-ictal hour is monotone and crosses Class C threshold within 60 minutes for ≥ 50% of seizures; postictal Class B reversal in ≥ 70%.

**Product layer.** "Pre-ictal predictive-precision diagnostic"; "free-energy precursor for seizure"; vocabulary: ictal / pre-ictal / inter-ictal, seizure prediction, NeuroPace, ECoG.

**Natural buyer.** NeuroPace (RNS), Epitel (REMI), Ceribell, Beacon Biosignals; epilepsy monitoring units; epilepsy-trial CROs.

**Capital and time.** Time-to-revenue 2 (24–36 months). Capital efficiency 2 (£2M–£5M).

**Failure modes.** Falsified by: pre-ictal CV trajectory not monotone above per-patient baseline. Fastest negative test: NeuroVista public dataset re-analysis.

**Data dependency.** Mayo / NeuroVista, Epilepsiae, FreiburgEEG.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | Class shift load-bearing, per-patient calibration weakness |
| Data availability | 4 | NeuroVista / Epilepsiae public |
| Buyer clarity | 3 | Niche but identifiable |
| Regulatory drag | 1 | FDA De Novo / PMA territory |
| Build complexity | 2 | Real-time analytics plus clinical workflow |
| Defensibility | 4 | Pre-registration plus class library |
| Time-to-revenue | 2 | 24–36 months |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **22** | |

---

### 20. EEG-aging dementia screening (band-redistribution diagnostic) · 22

**Description.** A 5-minute eyes-closed resting-state EEG screening tool for dementia risk that scores per-band Ω redistribution against a directional class library.

**Bottleneck.** EEG dementia biomarkers (β/θ ratio, α-rhythm slowing) are descriptive; no parameter-free directional baseline; cohort-fit thresholds vary by study.

**CRR contribution.** Per-band Ω redistribution canon (B5 lineage). Class A → C as MCI progresses; β/θ-ratio CV widens directionally with Mini-Mental decline.

**Pre-registered prediction.** In HBN / Cuban Human Brain Project data, β/θ-ratio CV across 5-min eyes-closed segments rank-orders cohorts: cognitive-reserve-high < healthy-aging < MCI < AD, with all pairwise comparisons p < 0.05 under FDR.

**Product layer.** "Spectral-precision biomarker for cognitive-reserve assessment"; "free-energy spectral diagnostic for prodromal dementia"; vocabulary: alpha-rhythm slowing, β/θ ratio, qEEG, cognitive reserve.

**Natural buyer.** Cognito Therapeutics, Linus Health, Brainscope; Eisai diagnostic partners (Lecanemab patient-flow); NHS dementia-pathway services.

**Capital and time.** Time-to-revenue 2 (24–36 months). Capital efficiency 2 (£2M–£5M).

**Failure modes.** Falsified by: AD-cohort β/θ-CV at or below healthy-aging cohort, controlling for age. Fastest negative test: HBN cohort rank-sum.

**Data dependency.** HBN (Healthy Brain Network), Cuban Human Brain Project, OpenNeuro.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | Band-Ω redistribution canon, class diagnostic |
| Data availability | 5 | Open EEG datasets |
| Buyer clarity | 3 | Pre-market dementia-diagnostic crowded |
| Regulatory drag | 1 | FDA 510(k) for dementia screening, long cycle |
| Build complexity | 2 | Clinical-validation cohort needed |
| Defensibility | 3 | Class library, market crowded |
| Time-to-revenue | 2 | 24–36 months |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **22** | |

---

### 21. Insulin-pump closed-loop controller diagnostic · 21

**Description.** A controller-quality diagnostic for hybrid-closed-loop pumps (and the open-source pump community) that scores closed-loop tuning quality on a parameter-free Class A / B / C scale.

**Bottleneck.** HCL pump tuning relies on per-user CGM history; cross-pump benchmarking is descriptive (TIR, GMI); over-aggressive PID drives oscillation but there is no directional baseline at which "well-tuned" is defined.

**CRR contribution.** SO(2) (CGM glucose oscillation) → Z₂ (bolus commit) closed-loop. Class A unregulated (open-loop); Class B closed-loop hybrid; over-tuned controller drifts to Class C oscillation.

**Pre-registered prediction.** Inter-bolus-CV on Tidepool open-source-pump community data clusters at 1/(4π) ± 20% for users with TIR > 70%; over-aggressive PID parameter regimes show CV broadening above 1/(2π) with corresponding GMI deterioration.

**Product layer.** "Closed-loop precision-titration diagnostic"; "free-energy controller-quality biomarker for type-1 diabetes"; vocabulary: time in range, GMI, hybrid closed loop, hypoglycaemia minimisation.

**Natural buyer.** Tidepool open-loop community first (no FDA), then Medtronic Diabetes, Tandem, Insulet, Beta Bionics partner. Tidepool bypass is the strategic value here.

**Capital and time.** Time-to-revenue 2 (24–36 months for OEM, 9–18 for Tidepool). Capital efficiency 2 (£2M–£5M for OEM; <£500k for Tidepool path).

**Failure modes.** Falsified by: TIR-stratified Tidepool cohorts showing no CV ordering. Fastest negative test: Tidepool open-data CV by TIR-stratum.

**Data dependency.** Tidepool open data; partner OEM data.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 4 | SO(2)→Z₂ clean, class shift load-bearing |
| Data availability | 4 | Tidepool plus partner pump |
| Buyer clarity | 3 | Pump OEMs slow procurement |
| Regulatory drag | 1 | FDA PMA, 5+ year cycle for new controllers |
| Build complexity | 2 | Controller-firmware integration heavy |
| Defensibility | 3 | Class library |
| Time-to-revenue | 2 | 24–36 months OEM |
| Capital efficiency | 2 | £2M–£5M OEM (Tidepool path lower) |
| **Composite** | **21** | |

---

### 22. Aircraft / fleet structural-health fatigue triage · 16

**Description.** A fleet-level fatigue-triage score for airline maintenance planning that ranks tail numbers by inter-crack-event-CV class shift.

**Bottleneck.** Aircraft SHM is regulator-driven (FAA / EASA airworthiness); long certification cycles; data is heavily proprietary; the buyer side procurement is multi-year.

**CRR contribution.** Z₂ (crack initiation) on SO(2) (flight-cycle envelope). Class A baseline; harsh-landing histories drive Class C broadening.

**Pre-registered prediction.** In FAA-LTBP-equivalent fleet histories, inter-crack-event-CV under nominal A320 / 737 family operations clusters at 1/(4π); operator-induced harsh-landing histories (≥ 2.0 g threshold breaches per 1000 cycles) drive CV broadening above 1/(2π).

**Product layer.** "Fleet-fatigue precision biomarker"; "free-energy structural-health diagnostic"; vocabulary: damage-tolerance design, fatigue critical location, ASIP, AS9100.

**Natural buyer.** Boeing, Airbus, IATA member airlines via Sabre / Ramco; MROs (HAECO, AAR, ST Engineering); ICAO research.

**Capital and time.** Time-to-revenue 1 (≥ 36 months). Capital efficiency 1 (> £5M).

**Failure modes.** Falsified by: harsh-operator fleet showing CV at or below benign-operator fleet. Fastest negative test: anonymised fleet-history paired comparison from one airline-customer pilot.

**Data dependency.** Fleet data heavily proprietary; partner-dependent.

| axis | score | one-line |
|---|:---:|---|
| Mathematical fit | 3 | Z₂ commit clean, SO(2) less direct |
| Data availability | 2 | Fleet damage data heavily proprietary |
| Buyer clarity | 2 | Airlines and OEMs slow procurement |
| Regulatory drag | 1 | FAA / EASA airworthiness, certification cycle is years |
| Build complexity | 2 | Sensor data plus cert pathway |
| Defensibility | 4 | Pre-registration plus class library |
| Time-to-revenue | 1 | ≥ 36 months |
| Capital efficiency | 1 | > £5M |
| **Composite** | **16** | |

---

## Portfolio recommendation

**Top 3 fast pilots (≤ 9–18 months to first revenue):**

1. **C01 LLM training loss-spike early warning (38).** Highest composite, lowest capital, frontier-lab buyer with budget. Pre-registration audit trail is uniquely well-suited to the buyer's epistemic culture (open training-log papers).
2. **C02 Predictive maintenance directional-baseline library (36).** Highest mathematical fit (5/5) of any commercial candidate. SO(2) → Z₂ canonical fingerprint. Mature buyer market with $5B+ existing budget category.
3. **C03 Wearable cardiac three-class triage (35).** Direct realisation of B2 canon. Public PhysioNet data carries v1 to a credible directional ordering. Low capital, fast SDK / licence path.

(Honourable mention: C08 RL training-stability instrumentation is the natural bundle with C01 and adds <5% incremental cost.)

**Top 3 medium pilots (18–24 months to first revenue):**

1. **C06 Tokamak ELM precursor / disruption-prediction (31).** The highest defensibility (5/5) across the entire candidate set. Beauty-peak architecture maps directly to the < 100 ms prediction horizon ITER needs. Procurement is grant-driven but the customer count is small and the names are known.
2. **C22 Space-weather Hale-cycle anchored forecasting (30).** Direct realisation of P1 canon (T2). The 22-year cycle baseline is publishable on open SILSO data with a falsifier that resolves at SC25 end (2030, before the pilot exits beta).
3. **C05 Power-grid frequency-stability anomaly detector (30).** SO(2) → Z₂ canonical, named TSO buyers, regulatory pathway is grid-code certification (manageable). The macro tailwind is irresistible: ENTSO-E Project Inertia Phase II 2024+ reports identify the gap this product fills.

**Top 2 strategic bets (long horizon, high payoff if delivered):**

1. **C13 Insulin-pump closed-loop controller diagnostic (21).** The Tidepool open-source pump community gives a regulator-bypassed v0 path that proves the directional-CV class diagnostic before any FDA engagement. If the directional ordering survives, the OEM market follows. Composite is held down by FDA PMA cycle and pump-OEM consolidation, but the underlying mathematical fit (clean SO(2) → Z₂) is strong and the patient population (T1D, T2D-on-pump) is large.
2. **C20 EEG-aging dementia screening (22).** Slow regulator path, but the underlying band-redistribution canon (B5 lineage) carries a distinctive directional ordering across cognitive-reserve cohorts. Strategic for the same reason MCI-detection biomarkers attracted the Lecanemab market: dementia-pathway services pay for screening that selects responders to disease-modifying drugs. Public open-EEG data carries v1.

---

## Cross-cutting infrastructure note

These shared tools amortise across multiple candidates and should be built once:

- **CRR-CV analytics library (Python + Rust core).** Domain-agnostic CV-of-inter-event-interval estimation with bootstrap CI for n = 1 small-sample correction; class-A / B / C classifier with directional-ordering hypothesis test. Used by C01, C02, C03, C04, C08, C09, C10, C12, C13, C19, C20.
- **Z₂ / SO(2) / Zₙ symmetry-classification protocol.** A decision-tree document plus reference notebooks: given a system's attractor topology, classify the substrate symmetry; output is a predicted CV anchor and class-A baseline. This is the published-method moat. Used by every candidate.
- **Pre-registration logging service.** A Git-backed registry for committed-then-tested predictions; timestamps in commit chain prove no retroactive editing. Differentiates CRR-anchored products from black-box ML competitors. Used by every candidate; particularly load-bearing for C01, C04, C06, C09, C10, C18.
- **Directional-baseline class library.** A community-curated CSV of (system name, substrate symmetry, predicted CV, empirical CV, citation) seeded by the framework's 132-system catalogue. Each candidate adds rows from its own deployment, increasing collective defensibility.
- **Beauty-peak (C* − Ω) windowing module.** A short library that computes beauty-function maxima from a coherence trajectory. Used by C04 (AF onset window), C06 (ELM prediction horizon), C08 (RL early-stop), C09 (anaesthesia titration), C10 (pre-ictal window).
- **Domain CV vocabulary translator.** An internal mapping table from CRR engine vocabulary to the seven product-layer vocabularies (FEP / AI, ML-ops, condition monitoring, cardiology, EEG, plasma physics, finance). Reduces hand-rolled vocabulary drift across the portfolio.

A single team of three (one mathematician, one ML engineer, one product-aware writer) can maintain all six tools at <£300k per annum across the portfolio. The library + protocol + registry combination is itself a defensible position even if individual candidates fail to find buyers.

---

## Candidates dropped at each filter

### Dropped at Filter 1 (mathematical relabelling or unclear manifold)

- **Migraine cluster timing (10).** Symptom-defined "rupture", manifold fuzzy.
- **PTSD startle bursts (16).** Reflex commit, manifold unclear; merge candidate with HRV not stand-alone.
- **MDE timing in bipolar (17).** Episode "boundary" is clinical not dynamical.
- **Tinnitus phantom-percept gating (20).** No transition rate to time.
- **Migraine aura CSD (22).** Z₂ but manifold not clean.
- **Drosophila oogenesis stage transitions (32).** Narrative more than dynamical.
- **Neural-tube closure timing (33).** Single event per embryo, not recurrent.
- **PV cell I-V hysteresis (37).** Material-physics relabelling.
- **OLED degradation event-spacing (38).** Defect timing without clear substrate.
- **Ca²⁺ oscillations non-excitable (40).** Substrate boundary unclear.
- **Glycolytic oscillation CV (42).** Relabelling.
- **Optical comb stability (47).** Relabelling of phase-locked-loop.
- **HVDC fault clearing (51), Auto-recloser CV (52).** Too few events per system.
- **Wafer chuck temperature (55).** Sensing, not Z₂.
- **Reticle particle inspection (56).** Proprietary opacity, no manifold.
- **NAND/HDD bit-error burst CV (57).** Proprietary.
- **Helicopter HUMS (63).** Niche, regulatory drag dominates.
- **Steam turbine creep (64), Wind blade leading-edge erosion (66), Concrete spalling (69).** Too slow / relabelling.
- **MJO 1→8 transition CV (71).** Class boundary muddled.
- **Monsoon onset (72).** Single event/year.
- **AMOC weakening (74), Volcanic tremor onset-to-eruption (79), Cryoseismic (80), Rogue-wave spacing (90), Atlantic-blocking timing (no longer in list), River-flood return-interval (92).** Too rare or dataset-redundant with retained climate / volcano candidates.
- **RR Lyrae CV (83), Solar-flare X-ray peak CV (87), CME interval CV (88).** Drop in favour of P1 / P2 retained candidates.
- **Predator-prey peak CV (93), Mast seeding CV (94), Honeybee swarm departure (95), Ant raid wave (96).** Slow data, sparse, or no buyer.
- **Hallucination-cluster spacing in long-context generation (99).** Substrate unclear; LLM hallucinations are not bounded accumulation.
- **Speculative-decoding rejection CV (102).** Too low-level, no buyer.
- **CDS spread-blowout (107), Yield-curve inversion (108), Crypto flash-crash (109).** Niche, sparse, or duplicates of retained candidates.
- **DDoS surge (111), Insider-threat anomaly (112).** Sparse or duplicates.
- **Stockout interval CV (116).** Operational not load-bearing.
- **PCA opioid bolus interval (119).** Load-bearing weak, small market.
- **Antibiotic-resistance emergence (120).** Too slow for chemostat data.
- **Vaccine waning interval (121).** Single rupture per cohort.
- **Music beat-induction CV (123).** Load-bearing weak, market unclear.
- **GLOF interval (127), Heliostat-tracking commitment-error (128).** Sparse or niche.
- **Hyperscale data-centre PUE excursion (135).** Data closed.

### Dropped at Filter 2 (empirical accessibility insufficient)

- **SCD long-QT (5).** Genotype-stratified CV sparse; merged into C03.
- **Schizophrenia blink CV (18).** Sparse modern CV reports.
- **Disorders-of-consciousness recovery (21).** Small cohorts.
- **SSW interval CV (75).** Sparse.
- **Yeast mating-decision interval (27).** Sparse CV.
- **Single-molecule fluorescence blinking (36).** Accepted, but no CRR buyer for relabelling.
- **Mitochondrial flickering (41), MEMS gyroscope drift (45), Etch endpoint (54).** Niche or proprietary.
- **Cargo-port congestion (115).** Low fit for buyer.
- **Stuttering disfluency CV (124).** Sparse modern CV.
- **Geyser eruption CV (78).** Niche, no commercial buyer.

### Dropped at Filter 3 (architectural cleanliness fails or no commercial buyer)

- **Repressilator inter-pulse CV (23).** Synthetic-bio buyer wants Z₃ exposed; thin market.
- **Circadian period CV in PER mutants (28).** Academic research only.
- **Vertebrate somite formation CV (30).** Beautiful biology, grant-funded buyer only.
- **PSII Kok cycling (35).** Bioenergetics academic.
- **BZ inter-spike CV (39).** Chemistry textbook validation, no buyer.
- **Earthquake inter-event CV stand-alone (76).** Public-good seismology, retained via C15 (CAT bond).
- **Cepheid CV (82), Pulsar glitch CV (84), FRB repeater intervals (86).** Astronomy, no commercial buyer.
- **Volcanic eruption interval CV (77).** Public-good seismology.
- **Bridge cable fatigue (65), Pipeline corrosion-pit (68).** Government-funded asset-management; possible later but not commercial 2026 priority.
- **Compressor surge / pump cavitation (60, 61), wind-turbine gearbox (59).** Merged into C02 predictive-maintenance bundle rather than dropped.
- **NF-κB / p53 dynamics (25, 26).** Strong CRR fit but no commercial buyer at 2026 horizon (academic only).
- **Synthetic toggle switch (24), Bioreactor switch reliability (29).** Synthetic-bio market still small at 2026 horizon.
- **Conversational turn-taking (122).** Buyer unclear (HCI research more than commercial).
- **CRP inflammation flare CV (126).** Possibly retainable as autoimmune-disease biomarker but FDA cycle disqualifies for 2026 first revenue.
- **Parkinson's tremor CV (11), ADHD attention-lapse CV (19).** Folded into wearable C03 / gait-clinic C12 family.
- **Epileptic seizure intervals (8).** Retained as C19 (cEEG seizure).
- **Atmospheric blocking event spacing (73).** Climate-attribution market crowded; retainable in long term not 2026.
- **3D-print AM defect (133).** Retained as C18.
- **ATC sector overload (117).** Possible but retained only as future strategic; sector has multi-year procurement.
- **Botnet beacon CV (113), IDS alert-cluster CV (110).** Cybersecurity retainable but the fit is weak (Class C noise-dominated only) and the moat is shallow.
