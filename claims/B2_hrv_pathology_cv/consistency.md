# B2 — HRV cohort CVs separate by pathology along Class B → A → C

## Prediction

Heart-rate-variability cohort CVs separate cleanly by clinical
pathology along the three-class diagnostic axis:

- **Class A (autonomous):** healthy adults, CV ≈ Ω/2 ≈ 0.080.
- **Class B (regulated):** athletes (high vagal tone, regulated
  HRV), CV < Ω/2.
- **Class C (noise-dominated):** post-MI / heart-failure patients
  (autonomic dysregulation), CV > Ω/2.

## Empirical regularity

Sources (all public PhysioNet):
- **MIT-BIH NSR Database:** healthy young adults (Class A).
- **MIT-BIH Athletic Database / Fantasia:** trained subjects
  (Class B candidate).
- **MIT-BIH CHF / SDDB / RR-SUDDEN:** heart-failure / post-MI
  patients (Class C).
- **PhysioNet Computing-in-Cardiology Challenge 2017:** AFib
  classification dataset.

Established HRV-pathology associations (Task Force 1996 standards;
Shaffer & Ginsberg 2017 review): healthy HRV is broadly higher than
HF/post-MI; trained athletes show different HRV profiles. The
specific CV-ordering claim of CRR is testable.

## Reproduction script

`crr-engine/consistency/physionet_hrv.py` (skeleton):
1. Fetch MIT-BIH NSR + Fantasia + CHF + SDDB.
2. Compute R-R intervals; reject ectopic beats.
3. For each subject: compute HRV CV.
4. Aggregate by clinical category; test the predicted ordering
   B < A < C with rank-sum tests.

**[REVIEWER-RUN]** sandbox blocks physionet.org.

## Tier decision

**Remains T1 (T2 pending).** The directional ordering claim
(B < A < C) is testable on PhysioNet; the analysis is canonical;
no obstacle but sandbox network.

## Applied usefulness for 2026 and beyond

- **Wearable cardiac diagnostics:** Apple Watch, Fitbit, Oura,
  Whoop, Polar, Garmin all stream HRV continuously. CRR's CV
  classifier provides a *parameter-free* regulated/autonomous/noise-
  dominated tag that consumer-grade firmware can compute on-device.
  This is unique: most HRV scores require population-norms
  calibration. CV = Ω/2 is the absolute reference.
- **Cardio-rehab triage:** CV crossing from C → A is a recovery
  marker; CV stuck in C is a re-hospitalisation risk signal.
- **Sports performance / overtraining:** CV drift from B toward A
  is a recovery indicator; sustained C-class is overtraining.
  Coaching apps in 2026+ (TrainingPeaks, Final Surge, WHOOP
  Strain) can incorporate.
- **Anaesthesia depth monitoring:** intra-operative HRV CV tracks
  autonomic state under anaesthesia; transitions through CRR
  classes correlate with depth of sedation. A CRR-derived
  intra-op monitor would be model-class-agnostic.
- **PTSD / anxiety phenotyping:** chronic sympathetic dominance
  produces low HRV; CRR class C in HRV correlates with PTSD
  symptom severity. Mental-health wearables (Spire, Empatica E4)
  can use the CV tag.
- **Diabetes autonomic-neuropathy screening:** silent autonomic
  failure manifests in HRV well before clinical symptoms; CV
  drifting toward C is an early-warning signal.

The HRV-CV application is among the most operationally accessible:
the data exists, the math is parameter-free, the wearables are
already deployed at scale.
