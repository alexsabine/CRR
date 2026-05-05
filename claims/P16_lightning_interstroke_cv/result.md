# P16 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.8500
notes     : median=0.8500, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Brazil natural CG lightning (Saba+ studies)**: CV = 0.8500
  - Log-normal inter-stroke (geo mean 49.6 ms, SD 0.32 dec) → CV(arith) = sqrt(exp((0.32 ln10)^2)-1) ≈ 0.85

## Tier consequence

**stays T1**.

## Interpretation

Brazilian CG-lightning inter-stroke times are log-normal (geo mean 49.6 ms, log-SD 0.32 dec) → arithmetic CV ≈ 0.85. Honest negative on Z₂ pre-reg; another Class C case where memoryless statistics dominate.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
