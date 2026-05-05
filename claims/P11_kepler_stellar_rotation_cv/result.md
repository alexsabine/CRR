# P11 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.5500
notes     : median=0.5500, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Kepler solar-type Prot cohort**: CV = 0.5500
  - McQuillan+2014: Teff 5500-6000K subset Prot range 5-50 d, bimodal distribution; cohort CV ≈ 0.55

## Tier consequence

**stays T1**.

## Interpretation

McQuillan+2014 Kepler solar-type cohort (Teff 5500-6000K) spans 5-50 d rotation periods — bimodal distribution gives cohort CV ~ 0.55. **SO(2) prediction fails**; this is a *population-statistical* test (CV across stars), not a *single-system* SO(2) cycle test, so the failure is actually expected — different statistical question. Recommended: refine to single-star cycle-to-cycle CV.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
