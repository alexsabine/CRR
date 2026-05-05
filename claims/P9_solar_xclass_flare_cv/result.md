# P9 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 1.0400
notes     : median=1.0400, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Solar X-class full-disk**: CV = 1.0400
  - Median 11.2 ± 11.6 hr (PMC published WTD studies; Poissonian / heavy-tail)

## Tier consequence

**stays T1**.

## Interpretation

Single-cohort full-disk X-class CV ≈ 1.04 (median waiting time 11.2 ± 11.6 hr). Solar flare WTD literature explicitly rejects Poisson but with heavy-tail / log-normal fits yielding CV near 1. Z₂ prediction **fails**; flare timing is Class C (noise-dominated) rather than memory-bearing Z₂ rupture.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
