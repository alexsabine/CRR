# B9 — Pre-registered prediction (Session 6)

**Pre-registered before any PubMed lookup or analysis script.**

## Statement

The cohort-median breath-to-breath-interval (BBI) CV across
published healthy-resting-adult cohorts (PubMed-indexed) is

    median(CV) = 1/(4π) ± 30% = 0.0796 ± 0.0239
                              = [0.0557, 0.1035].

Explicitly: in **at least 3 of 5** independent peer-reviewed
cohorts selected by the protocol below, the reported (or
reconstructible) CV falls inside [0.05, 0.11].

## Sampling protocol (locked here, before any lookup)

1. **PubMed query** (executed at analysis time, not now):

       (respiratory rate variability[Title/Abstract] OR
        breath interval variability[Title/Abstract] OR
        respiratory variability[Title/Abstract] OR
        breathing variability[Title/Abstract])
       AND (healthy[Title/Abstract] OR control[Title/Abstract])
       AND (rest[Title/Abstract] OR resting[Title/Abstract] OR
            quiet breathing[Title/Abstract])
       AND ("2000"[Date - Publication] : "2025"[Date - Publication])

2. **Inclusion:** primary research articles reporting *individual-
   level* breath-to-breath interval variability in healthy adult
   humans (≥ 18 years), at rest, awake, spontaneously breathing
   (no pacing). Reported quantities must include either (a) cohort
   mean BBI and SD or (b) cohort CV directly, on N ≥ 10 individuals.

3. **Exclusion:** sleep stages (BBI variability differs by NREM/REM
   stage and is canonically excluded from "rest" here); paced
   breathing studies; clinical patient cohorts (COPD, asthma,
   apnea, anxiety disorder); studies in altitude / hypoxia /
   exercise; studies in pregnant women (respiratory drive
   differs).

4. **Selection rule for the 5 cohorts:** if the search returns
   more than five qualifying primary studies, take the five with
   the largest reported N (subject count). Ties broken by
   most-recent publication date.

5. **CV extraction:** if reported as mean BBI and SD,
   CV = SD / mean. If reported as RR (respiratory rate per minute)
   and SD-RR, the conversion is BBI = 60/RR seconds and the BBI CV
   is computed as SD-RR / RR (same dimensionless ratio under the
   inverse map; the small-RSD approximation introduces ~1% error
   for SD-RR/RR ≲ 0.10, which is below the pre-reg tolerance).
   If a CV is reported directly, use it.

6. **Cohort representative:** the healthy-control row (or wild-
   type / untreated row) under standard resting conditions.

If fewer than 5 qualifying cohorts obtainable, the test runs on
whatever the search yields (minimum 3).

## Pre-registered conditions (for promotion)

**Condition 1 — Median CV falls in band:**

    median(CV) ∈ [0.0557, 0.1035]   ( = 1/(4π) ± 30% )

**Condition 2 — Cohort consistency:**

    fraction of cohorts with CV ∈ [0.04, 0.12] ≥ 0.6

i.e., at least 3 of 5 cohorts (or proportional minimum) inside
the broader SO(2) band.

**Condition 3 — Class-discrimination:**

    median(CV) is **not** in the Z₂ band [0.140, 0.180]

(i.e., the cohort median is unambiguously SO(2)-class, not
mistakenly Z₂-class.)

## Falsifier

Any of:
- median(CV) outside [0.04, 0.13] ⇒ SO(2) identification fails for
  resting respiration.
- Two or more cohorts with median CV in the Z₂ band [0.140, 0.180]
  ⇒ class-discrimination ambiguous; no T3.
- Cohort spread > factor of 4 across qualifying studies ⇒ no
  single regime captures resting respiration; the SO(2)
  prediction is regime-conditional.

## Tier promotion criterion

- **All three conditions met** ⇒ B9 promotes T1 → T3.
- **Conditions 1 & 2 met but not 3** ⇒ B9 promotes T1 → T2.
- **Condition 1 only** ⇒ B9 promotes T1 → T2 (m).
- **Condition 1 fails** ⇒ B9 stays at T1; no further pre-reg
  without a substantively different test.

## Independence

Polysomnography and resting-state metabolic studies pre-date
CRR. The SO(2) identification is the CRR-novel theoretical move;
the empirical match (or mismatch) of the published cohort CVs
to 1/(4π) is the test.

## Honest exposure

I (Claude, the campaign analyst) have prior literature exposure
suggesting healthy resting BBI variability is in the 5–15% range,
consistent with the SO(2) band. The pre-reg's tightness (±30%) is
calibrated against this rough prior.

A genuine risk: many published studies report BBI variability in
units of *standard deviation* (seconds) without reporting mean,
or vice versa, blocking CV computation. The protocol allows a
minimum of 3 cohorts; if fewer than 3 qualify, the result is
recorded as **inconclusive**, not as a falsification.

## Applied usefulness for 2026 and beyond

If B9 reaches T3:

- **Wearable respiratory monitoring** (Apple Watch RR, Whoop,
  consumer 2026+): a parameter-free target CV against which
  consumer-grade RR sensors are calibrated; deviations from
  1/(4π) at rest are candidate biomarkers of stress / arousal.
- **Sleep medicine** (polysomnography, CPAP titration 2026+): the
  SO(2) baseline for *quiet wakefulness* contrasts with N3-sleep
  and REM dynamics; clinical thresholds become CRR-grounded.
- **Anaesthesia depth monitoring**: CV deviation from 1/(4π) as
  a brainstem-level depth marker complementing EEG-derived
  indices.
- **Long-COVID / post-viral dysautonomia 2026+:** chronic
  deviation from SO(2) baseline as a candidate physiological
  biomarker.
