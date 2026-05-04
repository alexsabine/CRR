# B1 — Biological 1/f signals: singular-continuous (Fibonacci-class) spectra

## Prediction

Biological 1/f signals (EEG, ECG, gait, neural avalanches) have
spectra in the **singular-continuous (Fibonacci-chain) class** —
neither pure-point (periodic) nor absolutely-continuous (white-
noise-like). Empirical realisation of M9.

## Empirical regularity

Sources (all public): **PhysioNet** (Goldberger et al. 2000) curates
- MIT-BIH NSR (normal-sinus-rhythm ECG): `https://physionet.org/content/nsrdb/`
- Sleep-EDF expanded EEG: `https://physionet.org/content/sleep-edfx/`
- PhysioBank gait databases (Hausdorff): walking inter-stride times.
- Crackt/Beggs-Plenz neural avalanches: openneuro.org

Established 1/f power-spectrum behaviour across these signals is
canonical (Voss & Clarke 1975; He 2014 review). The spectral *type*
(pure-point vs absolutely-continuous vs singular-continuous) is
less studied empirically; the CRR claim is that the spectrum is
singular-continuous.

## Reproduction script

`crr-engine/consistency/physionet_1f.py` (skeleton):
1. Fetch PhysioNet NSR ECG + Sleep-EDF EEG samples.
2. Compute power spectra; verify 1/f^β behaviour (β ≈ 1).
3. Apply spectral-type test (the **Last-Simon test** for singular-
   continuous spectra; Last 1996, Simon 1995): check that the
   spectral measure is supported on a Cantor-like set.
4. Compare against quasi-crystal (Fibonacci-chain) reference spectra.

**[REVIEWER-RUN]** sandbox blocks physionet.org.

## Tier decision

**Remains T1 (T2 pending).** The 1/f behaviour itself is well-
established. The *singular-continuous* classification is a stronger
claim that requires careful spectral-type analysis. No completed
analysis cited in canonical brief; promotion deferred.

## Applied usefulness for 2026 and beyond

- **Neurology biomarkers:** singular-continuous spectral classification
  could distinguish healthy / pathological states more sharply than
  power-law fits alone. Dementia (Alzheimer / FTD) EEG shows shifts
  in 1/f slope; if singular-continuous structure persists in healthy
  but dissolves in disease, gives a binary diagnostic marker.
- **Cardiology:** atrial fibrillation alters R-R-interval spectral
  type, not just power-law slope. ECG-based AFib detection in
  smartwatches (Apple, Garmin, Withings 2026+) could exploit this.
- **Locomotion analysis (Parkinson's, MS):** gait-CV and gait-
  spectral-type are independent biomarkers; spectral-type tracking
  could detect motor decline before CV crosses clinical thresholds.
- **Sleep science:** REM/NREM transitions show spectral-type shifts;
  CRR-classified spectra contribute to wearable sleep-staging
  algorithms (Oura Ring, Whoop, Polar).
- **Neuromorphic hardware (Intel Loihi 2, IBM NorthPole 2026+):**
  designing chips to *produce* singular-continuous-spectrum noise
  may better match biological neural-network statistics, improving
  the realism of brain-emulation workloads.
