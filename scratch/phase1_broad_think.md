# Phase 1 — Broad think (≥60 candidates)

Audit trail. Divergent. Each candidate gets a 1–3 line working note with:
- substrate symmetry (Z₂ / SO(2) / Zₙ / unclear) + justification
- candidate accumulator L, rupture event, regeneration resource φ
- whether peer-reviewed empirical CV data is plausibly available (Y/N/?)
- expected three-class designation (A/B/C) and direction

CRR's load-bearing claims (memorise):
1. CV = Ω/2 (parameter-free); Z₂ → 1/(2π); SO(2) → 1/(4π); Zₙ candidate → n/(4π)
2. Topological ratio Z₂:SO(2) = 2 (sanity check across paired comparisons)
3. Three-class diagnostic A/B/C; falsified by directional reversal
4. Linear scaling of CV with Ω (vs √Ω alternative; ΔAIC 1445)
5. SO(2) → Z₂ regulator architecture (rotation timing a switch)
6. Beauty function peak at C* − Ω (most informative regime is one-Ω before rupture)
7. Nested CRR cycles (Gleissberg → Hale → Schwabe pattern)

---

## Cluster A — Cardiac, neural, respiratory physiology

1. **Heart rate variability (HRV) class ordering.** Z₂ rupture (sinoatrial firing as bistable) on SO(2) substrate (cardiac cycle). Class A healthy → Class B athlete (vagal regulation lowers CV) → Class C arrhythmia (raises CV). Empirical: PhysioNet, ample. **YES**.
2. **Respiratory inter-breath interval CV.** SO(2) substrate of central pattern generator regulating Z₂ inspiratory commitment. Class A awake, B during sleep stage N3 (regulated), C during apnoea. Empirical: PSG datasets. **YES**.
3. **Photoplethysmography PPG-derived pulse intervals.** Same as HRV but consumer-wearable layer. **YES, vast wearable corpus.**
4. **Anaesthesia depth monitoring (BIS-style).** EEG burst-suppression interval CV. Z₂ on SO(2). Anaesthesia titrated → Class B; emergence → Class A. **YES** (BIS index already the standard product).
5. **Sudden cardiac death (SCD) early warning.** CV destination prediction: as ANS-control is removed, CV drifts toward autonomous baseline 1/(4π). **YES** (long-QT, syncope cohorts).
6. **Atrial fibrillation onset prediction.** CV-of-RR sharply rises pre-AF (loss of regulation, Class B → A→C). **YES.**
7. **Sleep stage transition timing.** SO(2) ultradian cycle modulating Z₂ NREM/REM switches. Beauty peak C*−Ω = pre-transition micro-arousal. **YES** (Sleep Heart Health Study).
8. **Epileptic seizure inter-event intervals.** Z₂ rupture on SO(2) cortical rhythm; many cohorts show Class C broadening. **YES** (NeuroVista, Epilepsiae).
9. **Ictal-interictal transitions in subclinical EEG.** CV destination prediction for tip-into-Class-C. **YES** (Mayo/Melbourne ECoG).
10. **Migraine cluster timing.** Inter-headache intervals; loss of headache-prophylaxis = Class B→A. **YES** (CaMEO, AMPP).
11. **Tremor frequency in Parkinson's.** SO(2) basal-ganglia oscillator timing Z₂ tremor bursts. Class B (medicated) vs A. **YES.**
12. **Gait stride-to-stride CV in Huntington's & Parkinson's disease.** Already a known CRR signature: as regulation removed, CV drifts to 1/(4π) destination. **YES** (PhysioNet gait DB).
13. **Apnoea-hypopnoea event timing in OSA.** Z₂ on respiratory SO(2). CV-AHI in adaptive servo-ventilation Class B vs untreated A. **YES.**

## Cluster B — Sleep, EEG, neurodegeneration, neuropsychiatry

14. **EEG band-power redistribution with age.** Already a CRR signature (band-specific Ω redistribution, not uniform decline). Class boundary test. **YES** (Cuban Human Brain Project; HBN; UK Biobank).
15. **Resting-state alpha-rhythm CV in MCI/AD risk stratification.** Aging brain widens Ω; AD broadens further. **YES.**
16. **PTSD startle-burst inter-event intervals.** Z₂ rupture on autonomic SO(2). Class A → C in symptom-bearing. **YES.**
17. **Major depressive episode timing in bipolar.** Inter-episode CV under lithium (Class B) vs unmedicated (Class A → C). **YES** (STEP-BD).
18. **Schizophrenia thought-disorder eye-blink intervals.** Blink CV widens — Class C. **YES.**
19. **ADHD attention lapse inter-event intervals.** SO(2) prefrontal modulation of Z₂ vigilance switches. Methylphenidate Class B vs unmedicated. **YES** (ANT, gradCPT).
20. **Tinnitus phantom-percept gating.** Z₂ phantom on SO(2) cortical rhythm. **?** (sparse CV literature).
21. **Disorders-of-consciousness (DOC) recovery prediction.** Coma → MCS → emergence; CV-of-cortical-bursts as endpoint. **YES** (CRS-R datasets, EU PerBrain).
22. **Migraine aura cortical-spreading-depression timing.** Z₂ at calcarine; possible Class B baseline. **?**

## Cluster C — Cell biology, synthetic biology, gene-circuit engineering

23. **Repressilator inter-pulse interval CV.** Z₃ candidate (n/(4π) at n=3 ≈ 0.0796 ≈ 1/(4π)). Already in canon. **YES.**
24. **Synthetic toggle switch (Gardner-Collins) flipping CV.** Z₂ canonical. **YES** (Elowitz et al. lineage).
25. **NF-κB pulsatile signalling intervals.** Z₂ on SO(2) calcium oscillation. Class A baseline; LPS Class C. **YES.**
26. **p53 dynamics under DNA damage.** Z₂ (apoptosis vs survival) gated by SO(2)-like Mdm2 negative-feedback timer. **YES** (Lahav lab data).
27. **Yeast mating-decision interval CV.** Z₂ commitment under SO(2) cyclin clock. **YES.**
28. **Circadian period CV in PER mutants.** SO(2) → Z₂ rupture (sleep entry). Mutants reveal Class shifts. **YES.**
29. **Synthetic-biology bioreactor switch reliability.** Industrial Z₂ commitment quality control. CV directly maps to switching faithfulness. **YES** (Ginkgo, Lygos process data).

## Cluster D — Developmental biology, segmentation, morphogenesis

30. **Vertebrate somite formation CV.** SO(2) (segmentation clock) → Z₂ (somite commitment). Class A baseline. **YES** (Pourquié lab; Hubaud-Lubensky 2018).
31. **Zebrafish presomitic mesoderm oscillation CV.** As above. **YES.**
32. **Drosophila oogenesis stage transitions.** Discrete Z₂ commitments cycled. **YES.**
33. **Neural-tube closure timing in vertebrate embryos.** Z₂. **?** (possible empirical gap).
34. **Wound-healing inflammatory phase transitions.** Already in canon (`crr_wound_validation_*`). **YES.**

## Cluster E — Photosynthesis, biophotonics, photovoltaics

35. **Photosystem II Kok S-state cycling.** Already in canon — Kok miss matches 1/(4π). **YES.**
36. **Single-molecule fluorescence blinking intervals.** Z₂ (bright/dark). Class A or C depending on environment. **YES.**
37. **Photovoltaic cell I-V hysteresis under varying irradiance.** SO(2) → Z₂ in perovskite cell ion migration. **YES.**
38. **OLED degradation event-spacing in lifetime tests.** Z₂ defect commitment. **YES** (industry test data, but proprietary).

## Cluster F — Chemical oscillators, enzyme kinetics, metabolic

39. **Belousov-Zhabotinsky inter-spike intervals.** Already in canon — Class B suppression. **YES.**
40. **Ca²⁺ oscillations in non-excitable cells.** SO(2) → Z₂ release. **YES.**
41. **Mitochondrial flickering inter-event intervals.** Z₂ Δψm collapse. **YES** (Aon et al.).
42. **Glycolytic oscillation CV in yeast suspensions.** SO(2). Class A baseline. **YES** (Sel'kov / Hess data).

## Cluster G — Engineered oscillators, clocks, lasers

43. **Quartz oven-controlled crystal oscillator (OCXO) Allan deviation.** Class B regulation of Z₂ phase-noise events. **YES.**
44. **Atomic clock fractional frequency stability.** Class B precision. CV of inter-tick errors. Already linked via M10-α³. **YES.**
45. **MEMS gyroscope Allan-variance / drift-rate CV.** SO(2) substrate. **YES.**
46. **Mode-locked laser pulse-to-pulse jitter CV.** SO(2) → Z₂. **YES** (Menlo, Toptica datasheets).
47. **Optical frequency comb stability for spectroscopy.** **YES.**

## Cluster H — Power systems, grid frequency

48. **Grid frequency excursion event timing.** SO(2) (50/60 Hz cycle) → Z₂ (under-frequency relay trip). Class B regulated grid; Class C high-renewables grid. **YES** (ENTSO-E, NERC).
49. **Phasor measurement unit (PMU) inter-event spike CV.** **YES** (BPA, Open µPMU data).
50. **Battery state-of-charge swing reversal events.** SO(2) → Z₂. **YES** (Tesla Megapack, fleet data via NREL).
51. **HVDC converter station fault-clearing intervals.** Z₂ rare events; Class C if poorly tuned. **YES** (CIGRE B4 data).
52. **Distribution-feeder reclose attempts (auto-reclose CV).** Z₂. **YES** (utility SCADA logs).

## Cluster I — Semiconductors, lithography, process control

53. **Lithography overlay error CV across exposures.** SO(2) (stage motion) → Z₂ (alignment-mark capture commit). Class B regulated. **YES** (ASML field data).
54. **Etch endpoint detection CV in plasma reactors.** Z₂ commitment timing. **YES** (Lam / TEL test wafers).
55. **Wafer chuck temperature ripple → defect-event CV.** SO(2) → Z₂. **YES.**
56. **Reticle-particle inspection inter-event interval CV.** **?** (proprietary).
57. **Bit-error-rate burst spacing CV in storage media (NAND, HDD).** **YES** (Seagate, Western Digital research).

## Cluster J — Predictive maintenance, rotating machinery

58. **Bearing inner-race spalling event CV in roller bearings.** SO(2) → Z₂. Class A run-to-failure baseline; Class B with active vibration control. **YES** (NASA Bearing Dataset, Case Western, PRONOSTIA).
59. **Wind-turbine gearbox fault-event CV.** **YES** (NREL Wind Plant DB).
60. **Pump cavitation pulsation CV.** SO(2) → Z₂. **YES** (Hydraulic Institute test data).
61. **Centrifugal-compressor surge event spacing.** Z₂ stall. **YES** (gas-turbine OEM data).
62. **Aero-engine borescope-finding intervals.** Z₂ defect commit. **YES** (CFM, Rolls-Royce SHM data).
63. **Helicopter HUMS impact-event CV.** **YES** (UK CAA HUMS database).
64. **Steam turbine creep-fatigue rupture intervals.** **YES** (EPRI, GE PowerGen).

## Cluster K — Structural health, fatigue

65. **Bridge cable fatigue cracking event CV.** Z₂. **YES** (FHWA-LTBP).
66. **Wind-turbine blade leading-edge erosion event CV.** Z₂. **YES.**
67. **Aircraft fatigue critical-location crack initiation interval CV.** Z₂. Class B with damage-tolerance design. **YES** (FAA, USAF ASIP).
68. **Pipeline corrosion-pit growth-to-leak event CV.** **YES** (PHMSA).
69. **Concrete spalling rupture intervals in marine structures.** **YES** (DNV).

## Cluster L — Climate, ENSO, monsoon, MJO

70. **ENSO inter-event interval CV.** SO(2) annual cycle → Z₂ El-Niño commit. Class C noise-dominated (already established). **YES** (NOAA ONI).
71. **Madden-Julian Oscillation phase 1→8 transition CV.** SO(2). **YES.**
72. **Monsoon onset date CV.** Z₂ pluvial commit on SO(2) annual. **YES.**
73. **Atmospheric blocking event spacing CV.** Z₂. **YES** (ERA5).
74. **Atlantic meridional overturning weakening events.** **YES** (RAPID array).
75. **Stratospheric sudden warming event interval CV.** Z₂. **YES.**

## Cluster M — Seismology, volcanism, geyser

76. **Earthquake inter-event intervals in single fault systems.** Z₂. Class C (already in canon as P5). **YES.**
77. **Volcanic eruption interval CV.** Z₂. **YES** (Smithsonian Global Volcanism).
78. **Geyser eruption interval CV (Old Faithful).** SO(2) thermal cycle → Z₂. Class A baseline. **YES.**
79. **Volcanic tremor onset-to-eruption time CV.** Z₂. **YES.**
80. **Ice-quake / cryoseismic event CV.** **YES** (Polar Geophysical Inst.).

## Cluster N — Astrophysics

81. **Solar dynamo Hale CV.** Already canonical (P1). Class B regulated. **YES.**
82. **Cepheid period CV.** SO(2). Class B. **YES** (OGLE, Gaia).
83. **RR Lyrae period CV.** **YES.**
84. **Pulsar inter-pulse glitch interval CV.** Z₂. **YES** (Jodrell Bank).
85. **Gravitational-wave inspiral-merger-ringdown amplitude CV (P2).** Z₂. Already canonical. **YES.**
86. **FRB (fast radio burst) repeater intervals.** Z₂. **YES** (CHIME catalogue).
87. **Solar-flare X-ray peak event spacing CV.** Z₂. **YES** (GOES).
88. **Coronal mass ejection (CME) event interval CV.** **YES** (LASCO).

## Cluster O — Hydrology, oceans

89. **Tidal extremum Z₂ flip CV.** SO(2) → Z₂. Class B trivially. **YES.**
90. **Ocean-swell rogue-wave event spacing CV.** Z₂. **YES.**
91. **Glacial-interglacial cycle CV.** SO(2) Milankovitch → Z₂ commit. Class B. **YES** (paleoclimate).
92. **River flood return-interval CV.** Z₂. **YES** (USGS).

## Cluster P — Population ecology, swarms

93. **Predator-prey peak-trough interval CV.** SO(2). **YES** (lynx-hare).
94. **Mast seeding inter-event interval CV.** Z₂ on multi-year SO(2) phenology. **YES.**
95. **Honeybee swarm departure interval CV.** Z₂. **?**
96. **Ant raid wave inter-event interval CV.** SO(2) → Z₂. **YES.**

## Cluster Q — AI / ML alignment, RL stability, continual learning

97. **RL policy-collapse "catastrophic forgetting" event CV during long-context training.** Z₂. **YES** (open-source training logs at OpenRLHF, AI2).
98. **LLM training loss-spike CV.** Z₂ on optimisation SO(2)-like cyclic LR. **YES** (Llama-3, Pythia, OLMo public logs).
99. **Inference-time hallucination-cluster spacing CV in long-context generation.** Z₂. **?** (TruthfulQA-Long).
100. **Tool-use commitment event CV in agentic LLMs.** Z₂. **YES** (SWE-bench traces).
101. **RL exploration-exploitation phase-transition timing in PPO/DPO.** Class A baseline; Class B with KL-penalty. **YES.**
102. **Speculative-decoding rejection-event CV.** Z₂. **YES.**
103. **Foundation-model checkpoint-divergence-event CV in continual learning.** **YES.**

## Cluster R — Financial markets

104. **Equity volatility-regime change interval CV.** Z₂. Class C noise-dominated. **YES** (TAQ, OptionMetrics).
105. **FX flash-crash event interval CV.** Z₂. **YES.**
106. **Order-book imbalance Z₂ flip CV (HFT-tier microstructure).** **YES** (LOBSTER).
107. **Credit-default-swap spread-blowout interval CV.** Z₂. **YES** (Markit).
108. **Yield-curve inversion / un-inversion interval CV.** Z₂ on SO(2)-like macro cycle. **YES.**
109. **Crypto-flash-crash event interval CV.** **YES** (Kaiko).

## Cluster S — Cybersecurity, anomaly detection

110. **Intrusion-detection alert-cluster interval CV.** Z₂. **YES** (CICIDS).
111. **DDoS surge inter-event interval CV.** Z₂. **YES** (Akamai, Cloudflare reports).
112. **Insider-threat anomaly inter-event CV.** Z₂. **?**
113. **Bot-net beacon interval CV.** SO(2) → Z₂. **YES.**

## Cluster T — Supply chain, logistics, queuing

114. **Manufacturing OEE downtime-event interval CV.** Z₂. **YES.**
115. **Cargo-port berth congestion stress-event CV.** Z₂ on SO(2) tide / shift cycle. **YES** (Marine Traffic, IHS).
116. **Just-in-time stockout interval CV.** Z₂. **YES.**
117. **Air-traffic-control sector overload event CV.** Z₂. **YES** (FAA, Eurocontrol).

## Cluster U — Pharmacokinetics, drug delivery

118. **Insulin pump bolus-spacing CV in T1D control.** SO(2) → Z₂ (closed-loop). Class B vs Class A. **YES** (Tidepool, Loop).
119. **PCA pump opioid-bolus interval CV.** Z₂. **YES.**
120. **Antibiotic resistance-emergence event timing in chemostats.** Z₂ on SO(2) cell-cycle. **YES.**
121. **Vaccine-effect waning-to-rupture interval CV.** Z₂. **YES** (CDC VSD).

## Cluster V — Speech, language, music

122. **Conversational turn-taking inter-event interval CV.** SO(2) → Z₂ floor-yield. **YES** (Stivers cross-cultural).
123. **Musical onset / beat-induction inter-onset interval CV.** SO(2). **YES** (MAPS, MIREX).
124. **Stuttering disfluency inter-event interval CV.** Z₂. Class C. **YES.**
125. **Speech-pause inter-pause interval CV in dementia speech tasks.** **YES** (DementiaBank).

## Cluster W — Misc / cross-cutting

126. **CRP-cycling inflammation flare interval CV in autoimmune disease.** Z₂. **YES** (RA, IBD cohorts).
127. **Volcano-bound glacial outburst flood (GLOF) interval CV.** Z₂. **YES.**
128. **Concentrated-solar plant heliostat-tracking commitment-error CV.** SO(2) → Z₂. **YES.**
129. **Quantum-computer logical-qubit error-event interval CV.** Z₂ on SO(2) gate cycle. **YES** (IBM Quantum, Google).
130. **Fusion plasma ELM (edge-localised-mode) interval CV.** Z₂ on SO(2). **YES** (ITER, JET, MAST-U).
131. **Tokamak disruption inter-event interval CV.** Z₂. **YES.**
132. **Insurance catastrophe-bond trigger-event interval CV.** Z₂. **YES** (Artemis CAT bond DB).
133. **3D-print layer-defect inter-event interval CV.** Z₂. **YES** (NIST AM Bench).
134. **Battery-cell thermal-runaway precursor-event CV.** Z₂. **YES** (NREL battery DB).
135. **Hyperscale data centre PUE excursion-event CV.** SO(2) cooling cycle → Z₂. **YES.**

---

Total: 135 candidates. Phase 1 complete. Move to filtering.
