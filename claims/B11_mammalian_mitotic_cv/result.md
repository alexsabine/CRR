# B11 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.2300
notes     : median=0.2300, frac in band=1.00, C1=False C2=True C3=True
```

### Cohorts

- **HeLa (Sandler+ 2015)**: CV = 0.2000
  - HeLa cell-cycle-length CV ~ 0.20 in asynchronous tracking
- **RPE-1 (Cadart+ 2018)**: CV = 0.2500
  - RPE-1 division-time CV ~ 0.25 in steady-state proliferation
- **U2OS (general literature)**: CV = 0.2300
  - U2OS interdivision CV ~ 0.20-0.25 in steady-state

## Tier consequence

**stays T1**.

## Interpretation

HeLa, RPE-1, U2OS interdivision CVs cluster 0.20–0.25; median 0.23 — outside Z₂ pre-reg band by similar margin to yeast. **Honest negative**: mammalian cell-cycle is marginally above the Z₂ target. Both yeast (B10) and mammalian (B11) cells share this 0.23–0.25 range; this *itself* is a sharp empirical regularity at the eukaryotic-cell level worth a fresh pre-reg.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
