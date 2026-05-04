# B5 — EEG validation: 11/11 class orderings correct; CV ratio 1.93 (vs 2.0)

## Prediction

In an EEG cohort study, 11/11 directional class orderings (B → A → C
across electrode pairs / brain regions) are correct, and the
empirical CV ratio (rupture-only embedding vs SO(2)-circuit) is
1.93 — close to the M2 / M22-predicted 2.0.

## Empirical regularity

Source: canonical brief reports the 11/11 ordering and 1.93 CV
ratio. The underlying EEG cohort is **not specified** in the
canonical brief; presumably described in `CRR_COMPREHENSIVE_SUMMARY.md`
or one of the unpublished AGI-26-related analyses.

Public reproductions could use:
- **Sleep-EDF expanded** (PhysioNet) — public sleep EEG.
- **TUH EEG Corpus** (Temple University) — open, large.
- **OpenNeuro EEG datasets** — many task / resting paradigms.

## Reproduction script

`crr-engine/consistency/eeg_class_ordering.py` (skeleton):
1. Identify cohort (author needs to specify).
2. Compute per-electrode-pair rupture-rate CV.
3. Classify pairs into B / A / C by CV vs Ω/2.
4. Test directional ordering across multiple-comparison-corrected
   pairs.
5. Compute Z₂-only / SO(2) CV ratio across regions.
6. Compare against 11/11 ordering and 1.93 ratio.

**[REVIEWER-RUN, BLOCKED]** — cohort identification needed from
author before reproduction script can be made concrete.

## Tier decision

**Remains T1.** B5 is a *post hoc* report of a single analysis on
an unspecified cohort. To reach T2 it requires:
1. Author to specify the cohort (database, version, electrode
   configuration, preprocessing).
2. Independent reviewer to reproduce the analysis pipeline.
3. The 11/11 + 1.93 numbers to fall out without parameter tuning.

The 11/11 (binary) result is suspicious without an explicit chance
baseline: 11/11 from binary directional comparisons has p = 1/2¹¹ ≈
0.0005 under naïve nulls, but if the comparisons are not
independent (likely in EEG), the effective p is much larger.

## Applied usefulness for 2026 and beyond

- **Clinical neurology biomarkers:** if EEG-CV directional ordering
  reliably tracks clinical state, it adds a parameter-free axis to
  diagnostic EEG interpretation. Most current EEG analysis
  (band-power, microstate-segmentation) uses subject-population norms;
  a CRR class label is absolute.
- **Anaesthesia depth monitoring:** EEG-derived BIS/SedLine indices
  use proprietary processing; a CRR class label is open and
  parameter-free, suitable for open-source perioperative monitoring.
- **Concussion / TBI tracking:** post-injury EEG CV ordering vs
  baseline gives a recovery indicator that current portable-EEG
  devices (Cognionics, Muse-S, Emotiv) could implement.
- **Epilepsy seizure-onset detection:** transitions through CRR
  classes correlate with pre-ictal states; consumer-wearable
  seizure prediction (Empatica Embrace, Epitel REMI) could use the
  CV signal.
- **Mental-state classification:** BCI-controlled VR / AR (Meta
  Quest, Apple Vision Pro 2026+) increasingly use neural
  intent-decoding; B5-confirmed class structure improves classifier
  robustness.

B5's applied potential is high IF the underlying cohort is opened
and the result is independently reproduced. Currently bottlenecked
by author-side data deposition.
