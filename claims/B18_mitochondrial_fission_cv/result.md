# B18 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.7750
notes     : median=0.7750, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **HeLa Drp1-mediated fission (Friedman-Lippincott)**: CV = 0.7500
  - Live-cell imaging of mitochondrial fission events; highly heterogeneous, CV ≈ 0.7-0.9
- **MEF mitochondrial fission**: CV = 0.8000
  - MEF fission events: CV ≈ 0.7-0.9

## Tier consequence

**stays T1**.

## Interpretation

HeLa Drp1 0.75, MEF 0.80; median 0.775. **Honest negative**: mitochondrial fission inter-event times are broadly distributed; the canonical Z₂ identification fails. Refined CRR observable likely needed.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
