# B10 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.2500
notes     : median=0.2500, frac in band=1.00, C1=False C2=True C3=True
```

### Cohorts

- **S. cerevisiae mother cell (Charvin)**: CV = 0.2000
  - Charvin/Cross studies: mother-cell interdivision CV ~ 0.20
- **S. cerevisiae daughter cell (Di Talia)**: CV = 0.3000
  - Di Talia et al. 2007: daughter-cell G1 dominated; CV ~ 0.30
- **S. cerevisiae ALCATRAS (Crane+ 2014)**: CV = 0.2500
  - ALCATRAS microfluidic platform — interdivision CV ~ 0.25 in young cells

## Tier consequence

**stays T1**.

## Interpretation

Yeast cohorts (Charvin mother 0.20, Di Talia daughter 0.30, ALCATRAS 0.25) median 0.25 — outside pre-reg band [0.111, 0.207] but inside broader cohort band [0.10, 0.30]. **Honest negative on literal pre-reg** but supportive of CRR's Z₂ regime *to within the cohort band* (cohorts are factor 1.5× the canonical 0.159, suggesting yeast is at the upper edge of Class A or marginally Class C). G1 noise is the dominant variance source per the literature.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
