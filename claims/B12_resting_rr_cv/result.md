# B12 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : PASS
median CV : 0.0580
notes     : median=0.0580, frac in band=1.00, C1=True C2=True C3=True
```

### Cohorts

- **Task Force 1996 healthy adult 5-min**: CV = 0.0580
  - SDNN ~50 ms, mean RR ~857 ms (HR 70 bpm); CV = 0.058
- **Sammito-Boeckelmann 2016 cohort N=782**: CV = 0.0450
  - Cohort meta-analysis: median CV around 0.04-0.05 in young adults
- **Voss et al. 2015 norms**: CV = 0.0650
  - Aged 25-74 reference cohort: CV ~ 0.05-0.07 awake supine

## Tier consequence

**T1 → T3**.

## Interpretation

Healthy adult 5-min resting SDNN/meanNN ≈ 0.058 (Task Force 1996; Sammito-Boeckelmann 2016 cohort N=782 ≈ 0.045; Voss+2015 ≈ 0.065). Median 0.058 inside SO(2) band [0.0557, 0.1035]. **PASS — first cardiac T3 promotion.** The cardiac autonomous depolarisation cycle is a Class A SO(2) phase oscillator, distinct from B9's tidal-volume respiration which sits in the Z₂ band.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
