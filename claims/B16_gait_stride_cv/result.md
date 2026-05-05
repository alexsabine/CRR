# B16 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : PASS
median CV : 0.0250
notes     : median=0.0250 (ClassB expected); C1=True C2=True C3=True
```

### Cohorts

- **Hausdorff young adult preferred-speed**: CV = 0.0200
  - Hausdorff+ 2007: CV ~ 0.018-0.022 in healthy young adults
- **Beauchet older healthy**: CV = 0.0300
  - Beauchet+ 2009: CV ~ 0.025-0.035 in older healthy adults
- **Stergiou treadmill cohort**: CV = 0.0250
  - Stergiou treadmill walking CV ~ 0.022-0.028

## Tier consequence

**T1 → T3 (ClassB)**.

## Interpretation

Hausdorff young-adult ≈ 0.020, Beauchet older ≈ 0.030, Stergiou treadmill ≈ 0.025. Median 0.025 in [0.005, 0.05] Class B band; all three cohorts < 1/(4π). **PASS — Class B regulated regime confirmed for healthy gait.** Gait sits with circadian as a canonical Class B exemplar.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
