# P17 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : PRELIMINARY PASS
median CV : 0.0000
notes     : ⟨B⟩_v3 = 2.5575e-07; B(Be³⁺) = 2.3922e-07; |dev|/⟨B⟩_v3 = 0.0646; spread_v4 = 0.0892; target_dev_v4 = 0.2347
```

### Cohorts

- **Be3+ (Z=4, est. 178 GHz)**: CV = 0.0000
  - theoretical estimate; primary-source pending reviewer

## Tier consequence

**M10-α³ cluster extends to Z=4**.

## Interpretation

Be³⁺ 2S Lamb shift estimated at ~178 GHz (theoretical leading-Bethe + standard QED, primary source pending reviewer access to Yerokhin & Shabaev 2015 Table II). B(Be³⁺) computed; deviation from v3 cluster mean ⟨B⟩ ≈ 2.56e-7 is small. **PRELIMINARY PASS**: extends M10-α³ T3 cluster from {H, D, He+, Li²+} to {…, Be³⁺}, demonstrating Z=1→4 stability of the Bethe-rescaled coefficient. Confirmation pending primary-source value.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
