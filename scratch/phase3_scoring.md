# Phase 3 — Scoring

22 candidates. Scoring 1–5 on 8 axes. Composite max 40.

Tier thresholds: ≥32 fast pilot · 24–31 medium pilot · <24 strategic / R&D.

Scoring rubric reminders:
- **Mathematical fit** 5=load-bearing core; 1=forced.
- **Data availability** 5=open public; 1=needs new collection.
- **Buyer clarity** 5=identifiable buyer with budget line; 1=research-only.
- **Regulatory drag** 5=consumer software; 1=full clinical trial / De Novo.
- **Build complexity** 5=analytics overlay; 1=new physical sensor / clinical trial.
- **Defensibility** 5=baseline library + integration moat; 1=open-source after publication.
- **Time-to-revenue** 5=≤9 mo; 1=≥36 mo.
- **Capital efficiency** 5=<£250k; 1=>£5M.

---

## Candidate scores

### C01 — LLM training loss-spike & checkpoint-divergence early-warning service

CRR contribution: CV = Ω/2 anchors a parameter-free baseline for inter-spike interval CV during pre-training; three-class diagnostic distinguishes optimiser-induced (B), data-induced (A), and instability-induced (C); SO(2) → Z₂ pattern fits cyclic LR schedule modulating Z₂ gradient-explosion commit. Pre-registered prediction: under stable AdamW with WSD schedule, inter-spike CV converges to ≈ 1/(2π) on the optimiser-stability manifold. Buyer: frontier-model labs (Anthropic, OpenAI, Google DeepMind, Meta, Mistral, AI2, Cohere, ByteDance). Budget line: training-stability tooling, internal SRE-for-training. Procurement: enterprise contract or open-source-with-paid-tier.

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | CV=Ω/2 + class diagnostic load-bearing; SO(2)→Z₂ less direct than ideal |
| Data availability | 5 | OLMo, Pythia, Llama-3 training logs all public; in-house labs have own logs |
| Buyer clarity | 5 | Frontier labs procure ML-ops tooling; identifiable named decision-makers |
| Regulatory drag | 5 | No regulation |
| Build complexity | 5 | Pure analytics overlay over loss / gradnorm / activation traces |
| Defensibility | 4 | Pre-registered baseline library + integration with W&B / MLFlow workflows |
| Time-to-revenue | 5 | First paid pilot ≤9 mo |
| Capital efficiency | 5 | <£250k for v1 |
| **Composite** | **38** | **Fast pilot** |

---

### C02 — Predictive maintenance directional-baseline library for rotating machinery

CRR contribution: CV-of-inter-event-interval anchored at Ω/2 gives a parameter-free dispersion baseline against which bearing / gearbox / pump / compressor health states classify as A (autonomous wear), B (vibration-control regulated), or C (cavitation / surge / dust ingress noise-dominated). Replaces or augments per-plant CV thresholding currently fitted from history. Pre-registered prediction: under SO(2) → Z₂ (rotor → spalling commit), healthy CV-of-impulse-spacing approximates 1/(4π); developing inner-race spalling shifts the system to Class C with directional CV broadening. Buyer: SKF, Siemens Industrial, GE Vernova, Schaeffler, Bently Nevada (Baker Hughes), AspenTech, OSIsoft, plus end-asset operators (utilities, refineries, wind operators).

| axis | score | note |
|---|---|---|
| Mathematical fit | 5 | SO(2)→Z₂ architecture is the canonical fingerprint; directly load-bearing |
| Data availability | 5 | NASA IMS, Case Western, PRONOSTIA, NREL Wind, plus customer SCADA |
| Buyer clarity | 5 | Mature $5B+ market, named buyers, existing budget line |
| Regulatory drag | 4 | ISO 13373-style standards; no government approval |
| Build complexity | 5 | Analytics overlay over vibration / acoustic feeds |
| Defensibility | 4 | Class-baseline library scales with onboarded fleets; first-mover advantage |
| Time-to-revenue | 4 | 9–18 mo to first paid pilot via reseller / OEM |
| Capital efficiency | 4 | £250k–£750k for v1 + first integrations |
| **Composite** | **36** | **Fast pilot** |

---

### C03 — Wearable cardiac three-class triage (HRV directional baseline)

CRR contribution: HRV-CV-of-RR is the canonical Class A / B / C diagnostic test. Athletes regulate to Class B (vagal tone tightens), healthy resting at Class A (≈ Ω/2), arrhythmia / dehydration / heat-strain shift to Class C. The product is a parameter-free severity / readiness scale. Pre-registered prediction: 24h-resting HRV-CV in healthy adults clusters at 1/(4π); athlete-resting tightens below; CHF and AF cohorts broaden above. Buyer: Whoop, Oura, Polar, Garmin, Fitbit; secondary: Apple Health partners, telehealth platforms (Hims, Teladoc), corporate-wellness vendors.

| axis | score | note |
|---|---|---|
| Mathematical fit | 5 | Canon B2 PhysioNet rank-sum is exactly this test |
| Data availability | 5 | PhysioNet, plus partner data |
| Buyer clarity | 4 | Multiple identifiable wearables OEMs but consumer product layer crowded |
| Regulatory drag | 4 | Wellness scale ≠ medical claim; FDA general-wellness guidance |
| Build complexity | 5 | Analytics overlay; OEMs feed 1Hz PPG already |
| Defensibility | 3 | Easy to copy once published; moat is the 132-system class library + data partnerships |
| Time-to-revenue | 4 | 9–18 mo via licence / SDK |
| Capital efficiency | 5 | <£250k for v1 |
| **Composite** | **35** | **Fast pilot** |

---

### C04 — Atrial-fibrillation onset early-warning module

CRR contribution: hour-scale destination prediction — as autonomic regulation collapses pre-AF, RR-CV drifts from Class B (vagal-regulated) toward 1/(4π) autonomous baseline and broadens into Class C. Beauty function predicts the maximally-informative window at C* − Ω, i.e. the last quiet hour before episode onset. Replaces black-box ML models trained from scratch with a parameter-free directional prior. Pre-registered prediction: pre-AF window shows monotone CV trajectory crossing Ω/2 within 30–90 min; reverses upon successful sinus-rhythm restoration. Buyer: AliveCor, iRhythm (Zio), Boston Scientific (LUX-Dx), Medtronic (LINQ), plus arrhythmia clinics.

| axis | score | note |
|---|---|---|
| Mathematical fit | 5 | Destination + beauty peak both load-bearing |
| Data availability | 4 | PhysioNet AFDB plus partner ICM data |
| Buyer clarity | 4 | Mature implant-monitor and patch-monitor market; SaMD pathway |
| Regulatory drag | 2 | FDA SaMD; CE mark; longer cycle than wellness |
| Build complexity | 4 | Analytics + clinical-validation cohort |
| Defensibility | 4 | Pre-registration audit trail differentiates from ML competitors |
| Time-to-revenue | 3 | 18–24 mo via partner |
| Capital efficiency | 3 | £750k–£2M including reg pathway |
| **Composite** | **29** | **Medium pilot** |

---

### C05 — Power-grid frequency-stability anomaly detector for high-renewables grids

CRR contribution: SO(2) (50/60 Hz) → Z₂ (under-frequency relay trip / system split) is canonical. Class shift A → C as inertia falls below RoCoF threshold. Three-class diagnostic gives TSOs a pre-trip directional alert distinct from RoCoF threshold breach. Pre-registered prediction: in synchronously-connected segments with >70% inverter-based generation, inter-excursion-interval CV widens above 1/(2π); reversion under synthetic-inertia services tightens it back below baseline. Buyer: ENTSO-E TSOs (50Hertz, Eirgrid, National Grid ESO, RTE, Terna), NERC reliability coordinators, Hitachi Energy, GE Vernova grid-stability product lines.

| axis | score | note |
|---|---|---|
| Mathematical fit | 5 | SO(2)→Z₂ canonical; class shift directly maps to inertia decline |
| Data availability | 4 | ENTSO-E transparency portal; PMU data via BPA, Open µPMU |
| Buyer clarity | 4 | TSOs procure stability services; named individuals at GB/ESO, 50Hertz |
| Regulatory drag | 3 | Grid-code certification by national regulators; manageable |
| Build complexity | 4 | Analytics + PMU integration; some SCADA work |
| Defensibility | 4 | Class-baseline library, regulator-grade pre-registration audit trail |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **30** | **Medium pilot** |

---

### C06 — Tokamak ELM precursor / disruption-prediction service

CRR contribution: Z₂ on SO(2) pedestal turbulence is a textbook fingerprint of ELM physics. CV of inter-ELM intervals classifies operating regime (Type I = Class A; small-ELM = Class B regulated; ELM-free = transient Class B). Beauty peak at C* − Ω is the operationally interesting moment when ELM is committed-but-not-yet-released — precisely the prediction horizon. Pre-registered prediction: in DIII-D / JET BES data, inter-ELM-CV in Type-I H-mode lies in a band centred on 1/(4π) for fixed pedestal pressure; RMP-suppressed ELM-free regimes show CV → 0; pellet-pacing tightens CV to Class B. Buyer: ITER Organization, EUROfusion, Commonwealth Fusion, Tokamak Energy, TAE, Helion, General Fusion, plus national labs (PPPL, UKAEA).

| axis | score | note |
|---|---|---|
| Mathematical fit | 5 | Z₂ on SO(2) canonical, beauty peak directly maps to <100 ms prediction window |
| Data availability | 4 | DIII-D, JET, MAST-U public archives; ITER access via collaboration |
| Buyer clarity | 3 | Fusion sector R&D-heavy; budgets exist but procurement is grant-driven |
| Regulatory drag | 5 | No external regulation at R&D stage |
| Build complexity | 3 | Real-time inference + integration with plasma-control systems |
| Defensibility | 5 | Pre-registered class library + regulator-grade audit trail; very defensible in sector with publication-driven trust |
| Time-to-revenue | 3 | 18–24 mo via collaboration grants |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **31** | **Medium pilot** |

---

### C07 — Battery thermal-runaway precursor monitor for EV / stationary storage

CRR contribution: SO(2) (charge / discharge cycle) → Z₂ (cell internal-short ignition) architecture; class shift A → C in pre-runaway intervals reflects loss of regulating chemistry. Pre-registered prediction: inter-impedance-spike interval CV in Li-ion 18650 / pouch / prismatic cells under abuse testing lies near 1/(4π) for healthy cycling; precursor cells show monotone CV broadening 5–50 cycles before thermal event. Buyer: Tesla, BYD, CATL, LG Energy Solution, Northvolt, Form Energy, Fluence, Wärtsilä, plus BMS-chip vendors (Analog Devices, NXP, TI).

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | SO(2)→Z₂ clean; CV destination prediction load-bearing |
| Data availability | 4 | NREL battery DB, EUCAR, plus partner BMS telemetry |
| Buyer clarity | 4 | EV BMS and stationary storage operators have safety-incident motivation |
| Regulatory drag | 3 | UN ECE R100, IEC 62619, UL 9540A — manageable |
| Build complexity | 3 | Analytics + BMS firmware integration |
| Defensibility | 3 | Class-baseline library; BMS market is competitive |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **27** | **Medium pilot** |

---

### C08 — RL training-stability instrumentation (Class A / B distinguisher)

CRR contribution: Class A vs Class B distinguisher across PPO / DPO / GRPO trajectories. KL-penalty Class B regulated; reward-hacking events drive into Class C. Beauty peak C* − Ω identifies the optimal early-stopping window. Pre-registered prediction: in RLHF training of frontier models, inter-policy-update KL-divergence CV under stable PPO clusters at 1/(2π); reward-hacking drives CV above; KL-clip-induced regulation reverses to Class B. Buyer: Anthropic, OpenAI, Google DeepMind, Meta, Mistral, AI2, Mistral, Cohere, plus open-source RL frameworks (TRL, OpenRLHF).

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | Class diagnostic + beauty peak |
| Data availability | 5 | Open RLHF training logs; in-house lab data |
| Buyer clarity | 4 | Frontier labs same as C01 |
| Regulatory drag | 5 | None |
| Build complexity | 5 | Analytics overlay; integrate with TRL / Tunix / OpenRLHF |
| Defensibility | 3 | Easy to copy once published; bundling with C01 strengthens |
| Time-to-revenue | 4 | 9–18 mo |
| Capital efficiency | 5 | <£250k |
| **Composite** | **35** | **Fast pilot** |

---

### C09 — Anaesthesia-depth burst-suppression directional baseline

CRR contribution: cortical Z₂ (burst vs suppression) on SO(2) infraslow rhythm. Inter-burst-interval CV under deepening propofol shifts from Class A awake → Class B regulated → Class C suppressed-isolated. Provides parameter-free titration target distinct from BIS index. Pre-registered prediction: at MAC ≈ 1.0 sevoflurane, inter-burst-CV crosses below 1/(4π); awake baseline above 1/(2π). Buyer: Medtronic (BIS), Masimo (SedLine), Mindray, GE Healthcare, Drager, Philips Healthcare.

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | Class diagnostic; beauty peak as titration sweet-spot |
| Data availability | 4 | OASIS-B, MIMIC-IV, BISDB, partner OR data |
| Buyer clarity | 3 | Medical-monitor OEMs procure new indices but slowly |
| Regulatory drag | 2 | FDA 510(k) class II |
| Build complexity | 3 | Analytics + clinical-validation cohort |
| Defensibility | 4 | Pre-registration + class library |
| Time-to-revenue | 2 | 24–36 mo |
| Capital efficiency | 2 | £2M–£5M including 510(k) |
| **Composite** | **24** | **Medium pilot (border)** |

---

### C10 — Continuous-EEG seizure-onset early-warning service

CRR contribution: Class A → C transition in inter-spike-CV on cortical SO(2) substrate. Beauty peak at C* − Ω predicts pre-ictal window. Pre-registered prediction: in MAYO / NeuroVista chronic ECoG, inter-spike-CV in pre-ictal hour widens monotonically into Class C; postictal Class B reversal. Buyer: NeuroPace (RNS), Epitel (REMI), Neuvana, Ceribell, Beacon Biosignals, plus epilepsy monitoring units.

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | Class shift load-bearing; per-patient calibration needed |
| Data availability | 4 | NeuroVista/Epilepsiae public; partner clinical data |
| Buyer clarity | 3 | Niche but identifiable |
| Regulatory drag | 1 | FDA De Novo / PMA territory |
| Build complexity | 2 | Real-time analytics + clinical workflow |
| Defensibility | 4 | Pre-registration + class library |
| Time-to-revenue | 2 | 24–36 mo |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **22** | **Strategic / R&D** |

---

### C11 — EEG-aging dementia screening (band-redistribution diagnostic)

CRR contribution: per-band Ω redistribution (not uniform decline) signature; aging brain widens β/θ ratio in directionally diagnostic way. Class shift A → C as MCI progresses. Pre-registered prediction: in HBN / Cuban Human Brain Project, β/θ-ratio CV across 5-min eyes-closed segments widens with Mini-Mental score decline; carries directional ordering into MCI. Buyer: Cognito Therapeutics, Linus Health, Brainscope, Eisai diagnostic partners, NHS dementia-pathway services.

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | Band-Ω redistribution canon; class diagnostic |
| Data availability | 5 | Open EEG datasets |
| Buyer clarity | 3 | Pre-market dementia-diagnostic crowded |
| Regulatory drag | 1 | FDA 510(k) for dementia screening; long cycle |
| Build complexity | 2 | Clinical-validation cohort needed |
| Defensibility | 3 | Class library defensible; market crowded |
| Time-to-revenue | 2 | 24–36 mo |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **22** | **Strategic / R&D** |

---

### C12 — Gait-clinic Huntington's / Parkinson's destination triage

CRR contribution: stride-CV destination at 1/(4π) as cortical regulation removed (canon-illustrated via Hausdorff gait DB). Predicts not direction but destination and time-to-arrival. Pre-registered prediction: in pre-symptomatic HD gene carriers, stride-CV trends linearly toward 1/(4π); UHDRS motor-score correlates with rate of approach. Buyer: HD-clinic centres-of-excellence (Roche / Wave Life HD trials), Parkinson's UK, Cure HD Initiative, MJFF Parkinson's; gait-analysis vendors APDM (Clario), Mobility Lab.

| axis | score | note |
|---|---|---|
| Mathematical fit | 5 | Destination prediction is the load-bearing CRR contribution; canon-illustrated |
| Data availability | 5 | PhysioNet gait DB; HD trial gait substudies |
| Buyer clarity | 2 | Niche; mostly trial-endpoint vendors not B2C |
| Regulatory drag | 3 | FDA biomarker qualification; manageable |
| Build complexity | 3 | Wearable analytics + clinical-validation |
| Defensibility | 4 | Pre-registration + destination claim distinctive |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **28** | **Medium pilot** |

---

### C13 — Insulin-pump closed-loop controller diagnostic

CRR contribution: SO(2) (CGM glucose oscillation) → Z₂ (bolus commit) closed-loop. Class A unregulated (open-loop); Class B closed-loop hybrid; over-tuned controllers drift toward Class C oscillation. CV of inter-bolus interval as a regulator-quality scale. Pre-registered prediction: in well-tuned hybrid-closed-loop pumps (Medtronic 780G, Tandem Control-IQ), inter-bolus-CV approximates 1/(4π); over-aggressive PID drives Class C broadening (lev-mountain blood glucose). Buyer: Medtronic Diabetes, Tandem, Insulet, Beta Bionics, Tidepool open-loop community.

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | SO(2)→Z₂ clean; class shift load-bearing |
| Data availability | 4 | Tidepool, plus partner pump data |
| Buyer clarity | 3 | Pump OEMs procure controller-diagnostic but slowly |
| Regulatory drag | 1 | FDA PMA territory; 5+ year cycle for new controllers |
| Build complexity | 2 | Controller-firmware integration heavy |
| Defensibility | 3 | Class library; pump market is consolidated |
| Time-to-revenue | 2 | 24–36 mo |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **21** | **Strategic / R&D** |

---

### C14 — Quantum-error-correction logical-qubit cycle diagnostic

CRR contribution: Z₂ rupture (logical-error commit) on SO(2) gate cycle. Class A baseline = below-threshold logical qubit; Class B regulated by decoder; Class C above-threshold. CV of inter-logical-error interval gives parameter-free below-threshold confirmation independent of code-distance scaling fits. Pre-registered prediction: in Willow / IBM surface-code experiments, inter-logical-error-CV at d=5,7,9 clusters toward 1/(4π) below threshold; broadens into Class C above threshold. Buyer: IBM Quantum, Google Quantum AI, Riverlane, OQC, Quantinuum, IonQ, PsiQuantum.

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | Z₂ on SO(2); class diagnostic; below-threshold confirmation novel |
| Data availability | 4 | QEC papers publish syndrome traces; partner integration |
| Buyer clarity | 3 | Niche but well-funded; Riverlane natural integration partner |
| Regulatory drag | 5 | None |
| Build complexity | 3 | FPGA / decoder-stack integration |
| Defensibility | 4 | Pre-registration + class library; technical moat |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **29** | **Medium pilot** |

---

### C15 — CAT-bond / parametric-reinsurance pricing engine

CRR contribution: cross-domain Class C diagnostic for catastrophic-trigger event-spacing. ENSO, monsoon, hurricane, EQ all Class C; CRR-CV anchored at directional-baseline gives parametric-trigger pricing model independent of dataset-specific fits (B6 cross-domain claim). Pre-registered prediction: parametric-trigger inter-arrival CV in CRESTA Atlantic-hurricane bonds clusters above Ω/2 with directional ordering predicted by basin substrate symmetry. Buyer: Munich Re, Swiss Re, Hannover Re, RenaissanceRe, AXIS, plus ILS managers (Twelve Capital, ILS Capital, Schroders Capital).

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | B6 cross-domain claim load-bearing; directional baseline distinctive |
| Data availability | 4 | NOAA HURDAT2, USGS, plus Artemis CAT-bond DB |
| Buyer clarity | 3 | Reinsurance quants procure quietly; dec-makers identifiable |
| Regulatory drag | 4 | Reinsurance accounting; not a state-level regulator |
| Build complexity | 4 | Analytics + bond-pricing harness |
| Defensibility | 5 | Pre-registration audit trail + cross-domain library |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **30** | **Medium pilot** |

---

### C16 — Financial market regime-shift early warning

CRR contribution: Class C diagnostic for vol-regime change; CV of inter-flash-event interval drifts directionally into Class C pre-regime-flip; beauty peak at C* − Ω as informative pre-flip moment. Pre-registered prediction: in S&P-500 daily-realised-vol, inter-VIX-spike-CV widens monotonically across 5-day windows preceding regime shifts. Buyer: hedge funds (Two Sigma, Citadel, Renaissance), bank risk teams, MSCI risk products, Bloomberg / Refinitiv quant terminals.

| axis | score | note |
|---|---|---|
| Mathematical fit | 3 | Class C noise-dominated; directional but markets are crowded with similar signals |
| Data availability | 4 | TAQ, Bloomberg, OptionMetrics |
| Buyer clarity | 3 | Quant funds buy quietly; stochastic procurement |
| Regulatory drag | 4 | Buy-side; no state regulator on the analytics |
| Build complexity | 4 | Analytics + back-test harness |
| Defensibility | 2 | Quant edge erodes fast; CRR claim becomes free knowledge once published |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **26** | **Medium pilot** |

---

### C17 — Semiconductor manufacturing process-control overlay

CRR contribution: SO(2) (stage motion / scan) → Z₂ (alignment-mark capture commit) on lithography overlay; CRR-CV anchored baseline replaces per-fab Cpk fitting with cross-fab parameter-free directional ordering. Pre-registered prediction: under nominal NXT scanner operation, inter-overlay-residual-spike-CV clusters at 1/(4π); chuck temperature drift induces Class C broadening detectable 50–200 wafers earlier than current Cpk threshold. Buyer: ASML (virtual-metrology partner), KLA, Lam, AMAT, Tokyo Electron, plus fabs (TSMC, Intel, Samsung Foundry).

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | SO(2)→Z₂ canonical for stage-motion alignment commit |
| Data availability | 2 | Most process data behind fab confidentiality |
| Buyer clarity | 3 | Equipment OEMs procure but supplier list is short |
| Regulatory drag | 4 | SEMI standards |
| Build complexity | 3 | Integration with FDC / SPC stack |
| Defensibility | 4 | Pre-registration + class library |
| Time-to-revenue | 2 | 24–36 mo (long fab cycles) |
| Capital efficiency | 2 | £2M–£5M |
| **Composite** | **24** | **Medium pilot (border)** |

---

### C18 — Additive-manufacturing layer-defect monitoring

CRR contribution: Z₂ (defect-event commit) on SO(2) (recoater scan / build-plate rotation). CV of inter-defect-interval anchored to Ω/2 distinguishes process drift (Class B regulated) vs gas-flow contamination (Class C). Pre-registered prediction: in NIST AM Bench laser-powder-bed-fusion, inter-spatter-event-CV under nominal parameters clusters near 1/(2π); oxygen-rich excursion drives Class C broadening. Buyer: GE Additive, EOS, Trumpf, Carbon, Velo3D, Markforged, plus aerospace operators (Airbus, GE Aviation), medical-device printers.

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | SO(2)→Z₂ clean; defect-cluster CV directly measurable |
| Data availability | 4 | NIST AM Bench, Senvol, plus partner data |
| Buyer clarity | 3 | AM-process-monitoring market has 3-5 named buyers |
| Regulatory drag | 4 | ASTM F42; AS9100 if aerospace |
| Build complexity | 3 | Sensor + analytics integration |
| Defensibility | 3 | Class library; market modest |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **27** | **Medium pilot** |

---

### C19 — Sleep-stage transition timing for PSG / consumer sleep

CRR contribution: SO(2) ultradian → Z₂ NREM/REM commit. Class A baseline; Class B circadian-entrained; sleep apnoea Class C. CV of inter-stage-transition interval as parameter-free sleep-architecture quality index. Pre-registered prediction: in SHHS healthy cohort, inter-N3-N2-CV clusters at 1/(2π); OSA cohorts show directional broadening into Class C; CPAP titration restores Class B. Buyer: Philips Respironics, ResMed, Compumedics, plus consumer sleep tech (Eight Sleep, Whoop sleep, Oura sleep).

| axis | score | note |
|---|---|---|
| Mathematical fit | 4 | SO(2)→Z₂; class diagnostic |
| Data availability | 5 | SHHS, MESA, NSRR open archives |
| Buyer clarity | 3 | PSG vendors slow procurement; consumer faster |
| Regulatory drag | 3 | Wellness side fast; PSG side FDA 510(k) |
| Build complexity | 4 | Analytics overlay |
| Defensibility | 3 | Class library; market modest |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **28** | **Medium pilot** |

---

### C20 — Speech-pause dementia screening for telehealth

CRR contribution: Class C diagnostic on speech-pause CV in cognitive decline; SO(2) (intonation envelope) → Z₂ (pause commit). Pre-registered prediction: in DementiaBank Pitt corpus, inter-pause-CV in cookie-theft narrative clusters near 1/(4π) for healthy; AD cohort shifts into Class C broadening. Buyer: Linus Health, Canary Speech, Ellipsis Health, Cogniciti; insurance tele-triage vendors.

| axis | score | note |
|---|---|---|
| Mathematical fit | 3 | Class diagnostic only; SO(2)→Z₂ less crisp than gait |
| Data availability | 4 | DementiaBank open |
| Buyer clarity | 3 | Telehealth dementia screening crowded |
| Regulatory drag | 2 | FDA 510(k) for screening claims |
| Build complexity | 4 | Analytics overlay over speech pipeline |
| Defensibility | 3 | Class library |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **25** | **Medium pilot** |

---

### C21 — Aircraft / fleet structural-health fatigue triage

CRR contribution: Z₂ (crack initiation event) on SO(2) (flight-cycle envelope). CV of inter-event-interval as parameter-free crack-initiation distribution baseline. Pre-registered prediction: under nominal A320 / 737 family fatigue history, inter-crack-event-CV clusters at 1/(4π); operator-induced harsh-landing histories drive Class C broadening. Buyer: Boeing, Airbus, IATA member airlines via Sabre / Ramco, MROs (HAECO, AAR), regulator-funded ICAO research.

| axis | score | note |
|---|---|---|
| Mathematical fit | 3 | Z₂ commit clean; SO(2) less direct |
| Data availability | 2 | Fleet damage data heavily proprietary |
| Buyer clarity | 2 | Airlines procure SHM but slowly; OEM procurement is multi-year |
| Regulatory drag | 1 | FAA / EASA airworthiness; certification cycle is years |
| Build complexity | 2 | Sensor data + cert pathway |
| Defensibility | 4 | Pre-registration + class library |
| Time-to-revenue | 1 | ≥36 mo |
| Capital efficiency | 1 | >£5M |
| **Composite** | **16** | **Strategic / R&D** |

---

### C22 — Space-weather Hale-cycle anchored forecasting service

CRR contribution: P1 canon — solar Hale CV at 1/(4π) within SILSO band. SO(2) → Z₂ rupture (polarity reversal commit). Provides parameter-free 22-year baseline against which polar-route radiation, satellite-orbit decay, GPS error budgets are forecast. Pre-registered prediction: SC25–SC26 cycle-pair Hale CV aligns with 1/(4π); deviations lead by 9–18 months. Buyer: NOAA SWPC contractors, ESA SSA, satellite operators (Iridium, SpaceX Starlink, Eutelsat), polar airline routing (Air New Zealand, Cathay), space-weather insurance (AXA Climate, AON parametric).

| axis | score | note |
|---|---|---|
| Mathematical fit | 5 | P1 T2 canon — load-bearing |
| Data availability | 5 | SILSO, OMNI, NOAA real-time feeds |
| Buyer clarity | 3 | Government contractors + insurance niche |
| Regulatory drag | 4 | No regulation; government procurement bureaucracy |
| Build complexity | 3 | Real-time forecasting + integration with NOAA |
| Defensibility | 4 | Pre-registration; cycle-aligned baseline distinctive |
| Time-to-revenue | 3 | 18–24 mo |
| Capital efficiency | 3 | £750k–£2M |
| **Composite** | **30** | **Medium pilot** |

---

## Summary table

| ID  | Candidate | Composite | Tier |
|---|---|:---:|---|
| C01 | LLM training loss-spike & checkpoint-divergence early-warning | **38** | Fast pilot |
| C02 | Predictive maintenance directional-baseline library | **36** | Fast pilot |
| C03 | Wearable cardiac three-class triage (HRV) | **35** | Fast pilot |
| C08 | RL training-stability instrumentation | **35** | Fast pilot |
| C06 | Tokamak ELM precursor / disruption-prediction | **31** | Medium pilot |
| C05 | Power-grid frequency-stability anomaly detector | **30** | Medium pilot |
| C15 | CAT-bond / parametric-reinsurance pricing engine | **30** | Medium pilot |
| C22 | Space-weather Hale-cycle forecasting service | **30** | Medium pilot |
| C04 | Atrial-fibrillation onset early-warning module | **29** | Medium pilot |
| C14 | Quantum-error-correction logical-qubit cycle diagnostic | **29** | Medium pilot |
| C12 | Gait-clinic HD/PD destination triage | **28** | Medium pilot |
| C19 | Sleep-stage transition timing | **28** | Medium pilot |
| C07 | Battery thermal-runaway precursor | **27** | Medium pilot |
| C18 | Additive-manufacturing layer-defect | **27** | Medium pilot |
| C16 | Financial market regime-shift early warning | **26** | Medium pilot |
| C20 | Speech-pause dementia screening | **25** | Medium pilot |
| C09 | Anaesthesia-depth burst-suppression | **24** | Medium pilot (border) |
| C17 | Semiconductor process-control overlay | **24** | Medium pilot (border) |
| C10 | Continuous-EEG seizure-onset early warning | **22** | Strategic / R&D |
| C11 | EEG-aging dementia screening | **22** | Strategic / R&D |
| C13 | Insulin-pump closed-loop controller diagnostic | **21** | Strategic / R&D |
| C21 | Aircraft / fleet structural-health fatigue triage | **16** | Strategic / R&D |

Phase 3 complete. Move to Phase 4 deliverable.
