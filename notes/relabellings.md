# Relabellings and apparent inconsistencies

## ★ Status after rupture-topology resolution (post-Session 2)

The rupture-topology framework (`notes/rupture_topology.md`) and
convention dictionary (`notes/conventions.md`) **resolve** most of
the inconsistencies catalogued below. Each entry is annotated with
its resolution status:

- **[RESOLVED]** — dissolved by H1+H2+H3 framing or by typo
  identification; consult `notes/conventions.md` for the unified
  convention.
- **[CLOSED]** — confirmed canonical relabelling; tier permanently
  capped at T1*.
- **[OPEN]** — remains for author resolution after Session 2.

| Issue | Status |
|-------|--------|
| exp(C/Ω) → e at C·Ω = 1 (S1) | **[RESOLVED]** Two distinct Ωs (C3); identity holds in Z₂-intrinsic units |
| M2 ratio 2:1 | **[RESOLVED]** Half-turn embedding (M2 derivation rewritten) |
| M5 CR↔HG | **[CLOSED]** Confirmed canonical relabelling |
| M6 "limit" framing | **[RESOLVED]** Cosmetic; "specialisation" instead of "limit" |
| M8 1-D state assumption | **[CLARIFIED]** Generalised under M22 |
| M9 Fibonacci identification | **[OPEN]** — Session 4 pre-registration target |
| M10 26 ppm CODATA | **[OPEN]** — independent of rupture topology; T2 question |
| M11 ρ=−1/2 constraint | **[RESOLVED]** Variance-preservation derived (M11 rewritten) |
| M14 MaxEnt | **[CLOSED]** Confirmed canonical relabelling |
| M15 Z_n non-monotone | **[RESOLVED]** Discrete vs continuous phase distinction (M15 rewritten) |
| M16 Ω = π/√κ | **[RESOLVED]** Inversion typo; corrected to Ω ≥ √κ/π (M16 rewritten) |
| M19 Ω = μ(A) vs 1/μ(A) | **[RESOLVED]** Convention C5: Ω = μ(A); brief typo (M19 rewritten) |
| M21 TUR factor of 2 | **[OPEN]** — structural mismatch; not resolved by rupture-topology framework |

**Outstanding inconsistencies after this session:** 3 (M9, M10, M21).
Down from 11 at end of Session 2.

**New T1 claim added:** M22 (Lie-group CV generalisation).

---

## Pre-resolution catalogue (kept for audit)


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

### M14 — "exp(C/Ω) is the unique MaxEnt regeneration kernel" (Session 2)

Confirmed relabelling of Boltzmann-Gibbs MaxEnt under one moment
constraint. The exponential family with sufficient statistic C and
natural parameter 1/Ω is the canonical MaxEnt distribution by the
standard theorem; CRR's statement applies the theorem with chosen
labels.

**Status:** T1 cap. Domain content arrives only via M13 + M14
(Fisher-information identification + MaxEnt) jointly.

**Source:** `crr_full_proofs.md` Part I.5; `CRR_Complete_Proof_Sketch.md` §13.

### M11 — composition-constraint ambiguity (Session 2)

The canonical claim "Z₂ + Z₂ → SO(2) gives ρ = −1/2" is derivable
from the variance-preserving composition constraint Var(X+Y) = Var(X)
(with X, Y equal-variance), but NOT from the rupture-rate-halving
constraint Var(X+Y) = Var(X)/2 implied by M2. The two constraints
yield ρ = −1/2 vs ρ = −3/4 respectively. The canonical brief does
not state which constraint is intended.

**Status:** Recorded for clarification.

### M15 — Z_n hierarchy non-monotone (Session 2)

CV = n/(4π) for Z_n gives:
- n = 2 (Z₂): CV = 1/(2π) ≈ 0.1592 ✓
- n = 3: CV = 3/(4π) ≈ 0.2387
- n = 4: CV = 1/π ≈ 0.3183
- n → ∞: CV → ∞

But SO(2) reportedly has CV = 1/(4π) ≈ 0.0796, which is *smaller*
than every Z_n (n ≥ 2). So the language of "Z_n hierarchy interpolating
to SO(2)" is misleading — SO(2) is not a limit of the Z_n sequence.

**Status:** Flagged for author review.

### M16 — Ω-convention inconsistency (Session 2)

The brief simultaneously asserts:
- Ω = 1/φ_geodesic (everywhere)
- Ω = π/√κ on positively-curved manifolds (Bonnet-Myers)

These are inconsistent unless φ_geodesic = √κ/π, which is not a
Bonnet-Myers consequence. Bonnet-Myers gives diameter ≤ π/√κ; under
Ω = 1/diameter the corresponding statement is Ω ≥ √κ/π, not
Ω = π/√κ.

**Status:** Convention resolution required from author.

### M19 — Ω = μ(A) vs Ω = 1/μ(A) ambiguity (Session 2)

Kac's lemma gives expected return time = 1/μ(A); equating with mean
inter-rupture interval = 1/Ω yields Ω = μ(A_coherent), not
Ω = 1/μ(A_coherent) as the brief might suggest.

**Status:** Convention resolution required from author.

### M21 — TUR factor-of-2 mismatch (Session 2)

The thermodynamic uncertainty relation reads Var(J)/⟨J⟩² ≥ 2/Σ,
giving Σ · Var(J)/⟨J⟩² ≥ 2 — not 1. Direct identification
C ↔ Σ, Ω ↔ Var(J)/⟨J⟩² yields C·Ω ≥ 2, not the canonical C·Ω = 1.

To recover C·Ω = 1 saturation, a factor-of-2 must be absorbed into
one of the identifications (e.g., C ≡ Σ/2 or Ω ≡ 2·Var(J)/⟨J⟩²).
This is not stated in the canonical brief.

`crr-engine/tests/test_derivations.py::test_M21_tur_factor_two`
demonstrates the mismatch numerically: a biased two-state random
walk gives Σ · Var(J)/⟨J⟩² ≈ 1.5, comfortably above 1, illustrating
that the natural TUR bound is incompatible with C·Ω = 1.

**Status:** Convention resolution required.

### M10 — CODATA-precision discrepancy (Session 2)

The CRR self-consistency equation has a unique stable fixed point at
1/α* = 137.0324 (numerically verified to 6 decimal places via
fixed-point iteration; uniqueness via brentq sign-change scan).

CODATA empirical: 1/α = 137.035999084 (uncertainty ~10⁻¹⁰).

Discrepancy: 26.3 ppm — six orders of magnitude beyond CODATA
precision. The brief reports the CRR value as "137.032" (matching to
3 dp) and the empirical as "137.036," correctly acknowledging the
discrepancy but not addressing its size relative to experimental
precision.

**Status:** Quantitative consistency at 10⁻⁵, falsification at
CODATA precision. T2 promotion in Session 3 will require deciding
the relevant tolerance.

### exp(C/Ω) clamping in the canonical engine

The reference engine `CRR_Church_eff.html` line 171 clamps `C/Ω` at
10 (`Math.min(10, this.C/Math.max(.001, this.omega))`). This is an
implementation detail to avoid numerical blow-up, but it means the
canonical engine never realises the analytic exp(C/Ω) when C·Ω = 1
under canonical Ω values (where C/Ω runs to π² ≈ 9.87 just at the
threshold and beyond).

**Implication:** The engine's operational rupture is a clamped
approximation, not the analytic limit. Recorded; no tier impact yet.
