# P18 — Result of pre-registered Session-7 test

**Pre-registration:** locked at git commit `cc21772`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/session7_run_all.py`,
committed after `cc21772`. Sandbox-executed.

## Result

```
verdict   : FAIL
median CV : 0.4089
notes     : median=0.4089, frac in band=0.00, C1=False C2=False C3=True
```

### Cohorts

- **PDG hyperons {Λ,Σ⁺,Σ⁻,Ξ⁰,Ξ⁻}**: CV = 0.4089
  - PDG world avgs (ps): Λ=263.2, Σ⁺=80.18, Σ⁻=147.9, Ξ⁰=290.0, Ξ⁻=163.9; CV(τ) = 0.4089

## Tier consequence

**stays T1**.

## Interpretation

PDG hyperon octet {Λ, Σ⁺, Σ⁻, Ξ⁰, Ξ⁻} lifetimes (ps): 263.2, 80.18, 147.9, 290, 163.9. CV(τ) = 0.41. **Honest negative**: the literal SU(3) prediction CV = 1/(4π√3) ≈ 0.046 fails by ~9× on this observable. The hyperon lifetime spread is dominated by the strangeness-changing weak-decay matrix element variation, not by SU(3) geodesic structure. Different observable (e.g., fractional-mass spread within isospin multiplets) might be the right SU(3) target — refined pre-reg needed.

## Discipline note

- Pre-registration locked at `cc21772` BEFORE any data lookup.
- Result.md committed without retroactive edits to prediction.md.
- Honest negatives recorded permanently per Session-4-style
  campaign discipline.
