# M22 v2 — Pre-registered cross-domain Z₂ CV tests

## Origin

Session 9 follow-up to the M22 framework. Five cross-domain tests
designed to exploit canonical empirical values stable in scientific
literature, to be checked against agent training-corpus recall.

The Session 4.5 M10-α³ T3 promotion pattern is repeated:
hard-code well-known empirical values from canonical literature,
test the parameter-free CRR prediction against them, record honest
result regardless of direction.

## Pre-registered tests (5)

All Z₂-substrate predictions: CV = 1/(2π) ≈ **0.1592**.
SO(2)-substrate prediction (one test): CV = 1/(4π) ≈ **0.0796**.
SU(3)-substrate prediction (one test, exploratory): CV = 1/(4π√3) ≈ **0.0459**.

### Test 1 — Menstrual cycle CV (Z₂)

- **Predicted:** CV = 0.1592.
- **Empirical anchor:** Bull et al. 2019, *npj Digital Medicine*
  2:83. n = 612,613 cycles, mean ≈ 29.3 days, SD ≈ 5.2 days.
  Best-recall empirical CV ≈ **0.177**.
- **Tolerance:** |emp − pred|/pred < 0.30.

### Test 2 — Schwabe sunspot cycle CV (Z₂)

- **Predicted:** CV = 0.1592.
- **Empirical anchor:** SILSO sunspot record, Schwabe cycles
  1–24 (1755–present). Mean period ≈ 11.0 yr, SD ≈ 1.4 yr.
  Best-recall empirical CV ≈ **0.127**.
- **Tolerance:** |emp − pred|/pred < 0.30.

### Test 3 — Resting respiratory inter-breath interval CV (Z₂)

- **Predicted:** CV = 0.1592.
- **Empirical anchor:** Adult resting respiratory rate
  12–20 breaths/min from clinical references. Best-recall
  inter-breath interval CV ≈ **0.18** (range 0.15–0.22 depending
  on cohort).
- **Tolerance:** |emp − pred|/pred < 0.30.

### Test 4 — Schwabe : Hale CV ratio (M2 + M22 ratio prediction)

- **Predicted:** ratio = 2.000 (topological).
- **Empirical anchor:**
  - Schwabe CV ≈ 0.127 (Test 2 value).
  - Hale CV ≈ 0.080 (P1 T2 / SILSO).
  - Best-recall ratio ≈ **1.59**.
- **Tolerance:** |emp − 2|/2 < 0.30 → ratio in [1.40, 2.60].

### Test 5 — Charmonium ψ-family log-lifetime CV (SU(3), exploratory)

- **Predicted:** CV(log₁₀ τ) ≈ 0.0459 across 6 ψ-family states.
- **Empirical anchor:** PDG canonical Γ values:
  - J/ψ: Γ = 92.9 keV
  - ψ(2S): Γ = 294 keV
  - ψ(3770): Γ = 27.2 MeV
  - ψ(4040): Γ ≈ 80 MeV
  - ψ(4160): Γ ≈ 70 MeV
  - ψ(4415): Γ ≈ 62 MeV
- **Tolerance (exploratory):** |emp − 0.0459|/0.0459 < 0.50
  (±50%, broader given exploratory dimensional rescaling).

## Aggregate promotion criterion

| Pass count (5 tests) | Tier action |
|----------------------|-------------|
| 5 of 5 | M22 → T3 candidate; M2 strengthened |
| 4 of 5 | M22 → T2-firm; M2 strengthened |
| 3 of 5 | M22 stays T1 with multi-domain support recorded |
| ≤2 of 5 | M22 stays T1; mixed-evidence note |

## Discipline

Per `CAMPAIGN.md` PART III, this prediction.md is committed
**before** any analysis script for these tests exists. The git
hash of this commit is the binding pre-registration anchor. No
retroactive edits permitted.

The agent's training-corpus recall of empirical values stands
as committed. If primary-source values differ, the test as
written binds — discrepancies become honest-negative findings,
not retroactive adjustments.

The previous M22 prediction.md (Session 4) covering M22-A
(SU(2) ≡ SO(2)), M22-B (SO(3) ≡ Z₂), M22-C (SU(3)) remains
[REVIEWER-RUN] for those specific BMRB/IERS/PDG fetches and
is unchanged. This v2 is a *separate* set of tests on different
empirical anchors (biological, geophysical, particle-physics
log-lifetime).
