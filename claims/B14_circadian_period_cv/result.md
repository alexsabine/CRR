# B14 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : PASS
median CV : 0.0130
notes     : median=0.0130 (ClassB expected); C1=True C2=True C3=True
```

### Cohorts

- **Cyanobacteria circadian period in vivo**: CV = 0.0070
  - Intrinsic period stability paper PNAS 2024: σ ≈ 10 min on 24 hr
- **Drosophila wild-type free-run period**: CV = 0.0300
  - Drosophila DGRP: τ ≈ 24 hr, SD ≈ 0.7 hr; CV ≈ 0.03
- **Mouse SCN free-run period**: CV = 0.0130
  - Mouse SCN free-run period CV ≈ 0.01-0.02 (Welsh+ 2010 review)

## Tier consequence

**T1 → T3 (ClassB)**.

## Interpretation

Cyanobacteria CV ≈ 0.007, Drosophila DGRP ≈ 0.03, mouse SCN ≈ 0.013. Median 0.013 in [0.001, 0.05] Class B band; all three cohorts < 1/(4π). **PASS — Class B regulated regime confirmed for circadian clocks.** This is a clean confirmation of CRR's three-class diagnostic on canonically-tight oscillators.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
