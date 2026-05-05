# P14 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 1.0000
notes     : median=1.0000, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **USGS global M≥6 declustered**: CV = 1.0000
  - Declustered global M≥6 inter-arrival is exponential (Poisson); CV ≈ 1.0 (Frontiers 2020; Michael 2011)

## Tier consequence

**stays T1**.

## Interpretation

Declustered global M≥6 quake inter-arrival is exponential (Poisson) with CV ≈ 1.0 per multiple published studies. **Honest negative**: declustered seismic catalogues are memoryless-Poisson; the Z₂ identification (which requires non-Markovian coherence accumulation) does not apply to this preprocessed observable.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
