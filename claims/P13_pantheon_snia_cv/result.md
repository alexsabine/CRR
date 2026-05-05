# P13 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.0460
notes     : median=0.0460, frac in band=1.00, C1=False C2=True C3=True
```

### Cohorts

- **Pantheon+ standardised SNe Ia**: CV = 0.0460
  - σ_int ≈ 0.05 mag (Brout-Scolnic 2021); fractional flux CV ~ 0.046

## Tier consequence

**stays T1**.

## Interpretation

Pantheon+ standardised SNe Ia fractional brightness CV ≈ 0.046 (σ_int ≈ 0.05 mag → frac flux 4.6%). Just below the SO(2) pre-reg band [0.0557, 0.1035]. **Marginal fail**: the data are 17% below the SO(2) target — closer to Class B regulated than Class A SO(2) under the canonical Chandrasekhar-mass identification. Refined Class B pre-reg might pass.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
