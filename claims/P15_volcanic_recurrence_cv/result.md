# P15 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.9500
notes     : median=0.9500, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **Stromboli inter-eruption**: CV = 0.8500
  - Log-normal inter-event with σ_log ≈ 0.4 (Frontiers 2023 amplitude/IET)
- **Etna inter-eruption**: CV = 0.9500
  - Log-normal/Weibull mix; CV ~ 0.95 (Frontiers 2023)
- **Kilauea inter-eruption**: CV = 1.1000
  - Mostly Poissonian historical; CV ~ 1.1 (GVP/Smithsonian)

## Tier consequence

**stays T1**.

## Interpretation

Stromboli, Etna, Kilauea single-volcano recurrences fit log-normal/Weibull with CVs in the 0.6–1.2 range. **Honest negative**: volcanic recurrence is broadly distributed; the canonical Z₂ identification fails on this observable class. Persistent-activity sub-cohorts (Strombolian normal explosions on minute scale) might reveal Class A behaviour in a future fresh pre-reg.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
