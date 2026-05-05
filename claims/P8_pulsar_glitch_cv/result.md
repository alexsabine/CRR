# P8 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.5855
notes     : median=0.5855, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Vela PSR J0835-4510**: CV = 0.3000
  - Mean inter-glitch ~1000 d, SD ~300 d (Jodrell Bank catalogue)
- **Crab PSR B0531+21**: CV = 0.8710
  - Mean 419 d, SD 365 d (Espinoza et al. 2011 + updates; Poissonian fit)

## Tier consequence

**stays T1**.

## Interpretation

Vela CV ≈ 0.30, Crab CV ≈ 0.87. Median 0.585 outside Z₂ band. Crab inter-glitch is Poissonian-class (CV ≈ 1) per the Espinoza et al. 2011 fit; Vela is intermediate. The Z₂-rupture CRR identification of pulsar glitches is **not supported** at the literal pre-reg level. Memoryless-avalanche regime dominates.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
