# M10 — Derivation: Fine-structure self-consistency unique stable fixed point at 1/α = 137.032

## Claim

The fine-structure self-consistency equation

    α = exp(2π²α / (1 + (π−1)α)) / (16π²)

admits a unique *stable* fixed point at 1/α = 137.032, against the
empirical 1/α = 137.036.

## Assumptions

(A1) The self-consistency equation is taken as given by the canonical
brief; no derivation of the equation itself is attempted at this
tier (that would require Sessions 4+ work on the underlying CRR
137 derivation in `crr_137(attempt).pdf`).
(A2) "Unique stable fixed point" means there is exactly one solution
α* ∈ (0, 1) of f(α) = α with |f'(α*)| < 1.

## Derivation (numerical, under A1, A2)

Define f(α) = exp(2π²α / (1 + (π−1)α)) / (16π²).

**Fixed-point iteration** starting from α₀ = 0.01 converges in ~50
iterations to

    α* ≈ 0.007297544741

so 1/α* ≈ **137.032390**.

**Uniqueness (in (0, 1))** by exhaustive grid search at 100,000
points in [10⁻⁶, 1] for sign changes of f(α) − α: exactly **two**
fixed points exist:

| Fixed point | 1/α      | |f'(α*)| | Stability |
|-------------|----------|---------|-----------|
| α* ≈ 0.007298 | 137.032 | 0.140  | **stable** |
| α* ≈ 0.367989 | 2.717   | 2.272  | unstable  |

The unstable fixed point near α ≈ 1/e is a numerical curiosity (note
the proximity to e⁻¹ ≈ 0.3679; the fixed-point equation has a
mathematical attractor near the natural-log-base value but it is not
a basin of attraction).

So **the unique stable fixed point is at 1/α = 137.032**, confirming
the canonical claim.

## Empirical comparison

| Quantity | CRR fixed point | CODATA empirical | Discrepancy |
|----------|-----------------|------------------|-------------|
| α | 0.0072975447 | 0.0072973526 | 26.3 ppm |
| 1/α | 137.0324 | 137.0360 | 0.0036 (3.6 mu) |

The CRR prediction differs from the empirical value at the **4th
decimal place** of 1/α. This is a non-trivial discrepancy — far
outside the CODATA experimental uncertainty (which is ~10⁻¹⁰ in
1/α). The brief reports the prediction as "1/α = 137.032 from
CRR self-consistency" and the empirical as "137.036," correctly
acknowledging the discrepancy.

## Numerical verification

`crr-engine/tests/test_derivations.py::test_M10_fine_structure_fixed_point`
runs fixed-point iteration to convergence and asserts
1/α* ∈ (137.030, 137.034) and |f'(α*)| < 0.5;
`test_M10_unique_stable` asserts the unstable fixed point near 0.368
is the only other solution in (0, 1).

## Caveats

- **The equation itself is not derived at this tier.** Without a
  derivation of why the canonical CRR formalism produces *this*
  particular self-consistency equation, M10 reduces to: "this
  algebraic expression has a stable fixed point near the empirical
  1/α." The derivation of the equation from CRR first principles is
  outside Session 2's scope; it is queued for Session 3 or later.
- **The 26 ppm discrepancy is not a small correction.** CODATA
  measures 1/α to ~10 parts per trillion. The CRR prediction is
  off by 26 parts per million — six orders of magnitude beyond
  experimental uncertainty. A genuine theoretical prediction of α
  from first principles must either match CODATA at the 10⁻¹⁰
  level or explain why a 26-ppm correction term is missing. The
  canonical brief acknowledges the discrepancy ("137.032 vs
  empirical 137.036") but does not address its size relative to
  CODATA precision.
- **Recorded in `notes/relabellings.md`** as a *quantitative
  discrepancy*: the prediction agrees to ~10⁻⁵ but disagrees to
  CODATA precision. Whether this counts as "consistency" or
  "falsification" depends on the tolerance one demands of a parameter-
  free prediction.

## Status

**T1.** Fixed-point existence, uniqueness, and stability are
numerically verified. The empirical-comparison discussion is
recorded but does not affect the T1 status (which only requires
internal consistency under stated assumptions). T2 promotion in
Session 3 will need to address the CODATA-precision mismatch.
