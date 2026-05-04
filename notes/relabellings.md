# Relabellings and apparent inconsistencies

Per `CAMPAIGN.md` PART III honesty discipline, this file records:
1. CRR statements that restate an existing canonical result without
   genuine independence.
2. Apparent inconsistencies in the canonical formulation that surface
   during the campaign.

A relabelling can reach T1 as a derivation, but does not promote
further on the basis of the underlying canonical result alone.

---

## Confirmed/likely relabellings

### M5 — "Cramér-Rao saturation = Heisenberg-Gabor saturation"

Both are equality cases of conjugate-variable uncertainty inequalities.
Under the time-frequency / parameter-estimator conjugate pair, the two
saturations are a single theorem in two parameterisations.

**Status:** This is well-known in statistical signal processing
(see e.g. Cohen, *Time-Frequency Analysis*, 1995). The CRR statement
is a relabelling unless an independent CRR-specific consequence not
already implied by the underlying theorem can be exhibited.

**Implication for tier:** M5 may reach T1 as derivation, capped at T1
unless an independent novel consequence is demonstrated.

### "√2 as optimal precision-allocation ratio"

Derived in canonical sources from a Kelly / portfolio-theory argument.
Identical to existing results on log-utility allocation under fair odds.

**Status:** Relabelling. Not enumerated as a separate claim in
`decomposition.md`.

### "exp(C/Ω) is the unique MaxEnt distribution under a mean-coherence constraint" (M14)

This is an instance of the Boltzmann-Gibbs MaxEnt theorem under one
moment constraint, where C plays the role of the energy function and
1/Ω the inverse temperature. The CRR statement is a *correct
application* of a canonical result. **Borderline relabelling** — the
identification of C with Fisher information (M13) is what gives the
result domain-specific content. M14 in isolation is a relabelling;
M13+M14 together are not.

---

## Apparent inconsistencies in the canonical brief

### The "exp(C/Ω) → e at C·Ω = 1" identification

The brief asserts both:
- `C·Ω = 1` is the rupture condition (ontological present).
- "At C·Ω = 1, exp(C/Ω) → e."

These are mutually consistent only if Ω = 1. Under the canonical
substrate values:
- Z₂: Ω = 1/π ⇒ at C·Ω = 1, C = π, C/Ω = π² ≈ 9.87,
  exp(C/Ω) = e^{π²} ≈ 19333.7.
- SO(2): Ω = 1/(2π) ⇒ at C·Ω = 1, C = 2π, C/Ω = 4π² ≈ 39.48,
  exp(C/Ω) = e^{4π²} ≈ 1.4 × 10¹⁷.

Neither equals e.

The two conditions C·Ω = 1 and C/Ω = 1 are distinct in general; they
coincide only at Ω = 1.

**Tests that record this:** `crr-engine/tests/test_engine.py::
test_exp_kernel_at_rupture_for_unit_omega` and
`test_brief_exp_e_inconsistent_with_canonical_omega`.

**Implications:**
- M3, M4, M21 should not invoke "exp(C/Ω) → e" as part of their
  derivation pathway without first resolving which of the two
  conditions is intended at the rupture point.
- This is a finding for resolution by the framework's author, not a
  modification to be made by the campaign (per `CAMPAIGN.md`
  non-goals).
- Recorded for review at end of Session 1.

### "exp(C/Ω)" clamping in the canonical engine

The reference engine `CRR_Church_eff.html` line 171 clamps `C/Ω` at
10 (`Math.min(10, this.C/Math.max(.001, this.omega))`). This is an
implementation detail to avoid numerical blow-up, but it means the
canonical engine never realises the analytic exp(C/Ω) when C·Ω = 1
under canonical Ω values (where C/Ω runs to π² ≈ 9.87 just at the
threshold and beyond).

**Implication:** The engine's operational rupture is a clamped
approximation, not the analytic limit. Recorded; no tier impact yet.
