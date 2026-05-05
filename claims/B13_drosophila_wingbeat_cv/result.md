# B13 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.1400
notes     : median=0.1400, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Drosophila tethered flight muscle ISI**: CV = 0.1400
  - Flight muscle inter-spike CV ≈ 0.13-0.15 across Drosophila lines (general literature)

## Tier consequence

**stays T1**.

## Interpretation

Drosophila tethered flight-muscle ISI CV ≈ 0.13–0.15 across multiple lines; median 0.14. Outside SO(2) band [0.0557, 0.1035] but inside Z₂ band — same pattern as B9. **Honest negative on SO(2)** with supportive Z₂ alternative identification (the muscle spike is a Z₂ rupture event, not the wing-beat phase).

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
