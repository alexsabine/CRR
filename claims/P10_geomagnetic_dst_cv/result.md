# P10 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 1.4100
notes     : median=1.4100, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Dst≤-100 nT moderate storms**: CV = 1.1000
  - Inter-storm fits Weibull shape ~0.9 (Riley/Love 2011 region); CV ≈ 1 (slight overdispersion)
- **Dst≤-250 nT super-storms**: CV = 1.7200
  - Weibull γ=0.63 (Tsubouchi & Omura 2007; PMC6382914) → CV from CV(Weibull, 0.63) ≈ 1.72

## Tier consequence

**stays T1**.

## Interpretation

Weibull-fit super-storm inter-occurrence (γ=0.63) gives CV ≈ 1.72; moderate storms (Dst ≤ -100 nT) ≈ 1. Median outside Z₂ band by ~7×. **Honest negative**: geomagnetic storm timing is overdispersed Poisson-like, not Z₂-class.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
