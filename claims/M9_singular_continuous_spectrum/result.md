# M9 — Result of the pre-registered Sturmian-Hamiltonian test

**Pre-registration:** committed at git commit `3fc9681` in
`prediction.md`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/m9_quasicrystal_spectrum.py`,
committed after `3fc9681`. Sandbox-executed.

## Result (honest negative)

```
N =    89: width = 4.1602, gaps > 1% =  23, box-dim = 0.4994
N =   144: width = 4.1615, gaps > 1% =  18, box-dim = 0.6077
N =   233: width = 4.1620, gaps > 1% =  13, box-dim = 0.6957
N =   377: width = 4.1621, gaps > 1% =  16, box-dim = 0.7489
N =   610: width = 4.1622, gaps > 1% =  13, box-dim = 0.7789
N =   987: width = 4.1622, gaps > 1% =  14, box-dim = 0.7868
N =  1597: width = 4.1622, gaps > 1% =  12, box-dim = 0.7958

Pre-registration check:
  Width stable:                  ✓ (0.017% << 5%)
  Gap counts monotone in N?      ✗ (actually decrease then plateau)
  Box-dim @ N=1597 within 0.10?  ✗ (deviation 0.39)
```

## Tier decision

**M9 stays at T1.** The pre-registered T3 promotion criteria are
not met. Per the discipline, this result is binding regardless of
direction.

**No downgrade either:** the pre-registration tested a *specific*
operational definition (α = 0.5, β = −0.5 onsite potential;
Cantor signature via box-counting dimension within 0.10 of the
Sütő-class target). M9's underlying claim (singular-continuous
spectral type) is *broader* than this specific test. The negative
result narrows the scope of M9's empirical reach but does not
falsify the analytical claim itself, which rests on Sütő-Bellissard-
Damanik canonical results (M9 derivation.md).

## What the negative result tells us

1. **The Cantor-fractal signature requires stronger coupling** than
   α=0.5, β=−0.5. The Fibonacci-Hamiltonian spectrum dimension
   depends sensitively on coupling strength λ = α − β. At λ = 1
   (this test) the spectrum has nontrivial structure but is *not*
   in the Sütő strong-coupling Cantor regime.

2. **The pre-registered target value (0.481, then numerically
   0.4028) was likely wrong.** The Sütő Cantor-dimension formula
   is more subtle than log(φ)/log(σ) for arbitrary σ; the correct
   formula depends on the coupling and on the substitution
   eigenvalue structure. The pre-registration was *too specific*
   in fixing a single numerical target.

3. **Box-counting at finite N is sensitive to the geometric scale
   range.** The 8-scale geometric covering used here may not have
   converged to the asymptotic dimension at N=1597.

## Discipline note

Per `CAMPAIGN.md` PART III: "the result is binding regardless of
direction." The negative result is recorded as committed; the
pre-registration is not adjusted retroactively.

A *new* pre-registration with refined target (e.g., coupling-
dependent dimension formula, multi-coupling sweep, larger N) could
be written and committed; that would be a separate audit-trail
entry, not a modification of this one.

## Implications for connected claims

- **B1 (biological 1/f singular-continuous):** B1's empirical T2
  was already pending. M9's failure to confirm a specific Cantor
  signature does NOT directly downgrade B1, but it weakens the
  bridge from M9 to B1. Reviewer assessing B1 should note the M9
  negative result.
- **M22 (Lie-group CV):** unaffected. M22 doesn't depend on
  spectral-type details.

## Applied usefulness implications (2026 and beyond)

The negative result tightens (rather than weakens) the applied use
case for CRR:

- **Quasi-crystal materials:** real quasi-crystals show singular-
  continuous spectra at *strong coupling*; the M9-as-tested result
  shows that simple Fibonacci-substitution at moderate coupling
  does NOT immediately give the Cantor signature. So CRR's M9
  claim cannot be casually applied to weak-coupling biological
  1/f signals; one needs explicit coupling-strength estimates.
- **Topological photonics:** designers wanting Cantor band-gap
  structures need strong-coupling Fibonacci stacks, not arbitrary
  ones. CRR M9 doesn't shortcut this.

## Author / reviewer follow-up

If the M9 pre-registration target should be coupling-dependent (i.e.,
the prediction is "as λ → strong coupling, dim → Sütő bound"),
this is a different prediction structurally and would require a
fresh pre-registration commit in a future session.
