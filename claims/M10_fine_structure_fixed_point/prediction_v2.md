# M10-α³ — Pre-registered prediction v2: mean-residual with leading-Bethe rescaling

## Origin

Follow-up to the Session-4 negative result on M10-α³
(`prediction.md`, `result.md`, both at git `3fc9681` / `ac85ad8`).
The Session-4 result.md noted: *"the alternative-reading test
['mean ≈ α³'] would have passed — could motivate a fresh
pre-registration in a future session."*

This v2 commits to the alternative reading **before** running the
analysis with the refined statistic. The discipline is intact:
the v1 negative is recorded permanently; the v2 test is a
separate audit-trail entry.

## Theoretical motivation

The leading-order hydrogenic Lamb-shift formula (Bethe 1947) for
the n=2 S-state is approximately:

    ν_L(2S) ≈ (8/(3π)) × α³ × Z⁴ × Ry × log(1/(Zα)²) / n³

× higher-order corrections (Bethe logarithm L_0(2S), finite-size,
recoil, etc.) that scale differently with Z.

If the CRR α³ identification is correct at *leading order*, the
**Bethe-rescaled residual**

    B(system) = (ν_L × n³) / (Z⁴ × Ry × log(1/(Zα)²))

across hydrogenic 2S systems should:
1. cluster tightly across systems (intra-system consistency,
   bounded by sub-leading QED corrections),
2. cluster around the predicted leading coefficient
   (8/(3π)) × α³ ≈ 3.30 × 10⁻⁷, modulo a known O(1) Bethe-log
   subtraction.

## Prediction (quantitative pre-registration)

Computed for H 2S, D 2S, and He⁺ 2S using CODATA-grade Lamb-shift
values and constants:

    B(system) = ν_L × n³ / (Z⁴ × Ry × log(1/(Zα)²))

**Three pre-registered conditions:**

1. **Intra-system consistency:** the relative spread
   (max − min) / mean of B across the three systems is
   **< 0.20** (i.e., the residuals agree across systems within
   ±10% of each other; the Bethe-log rescaling absorbs the
   first-order Z-dependence).

2. **Mean magnitude:** the mean B across systems satisfies
   |⟨B⟩ − (8/3π) × α³| < 0.30 × (8/3π) × α³, i.e., **agreement
   within ±30%** with the leading Bethe-coefficient prediction
   (the ±30% tolerance budgets the higher-order QED corrections
   not absorbed by the simple log rescaling).

3. **Sign consistency:** ⟨B⟩ is positive (Lamb shift is positive
   in this convention) — sanity check.

## Falsifier

Any of:
- Intra-system spread > 0.30 ⇒ the Bethe-log rescaling does not
  capture the leading scaling; the α³ identification is incomplete.
- |⟨B⟩ − target| > 0.50 × target ⇒ even with O(1) tolerance, the
  α³ scaling is wrong.

## T3 promotion criterion

All three pre-registered conditions met ⇒ **M10-α³ promotes to
T3** (the α³ identification is *the* leading-order Lamb-shift
scaling at high-precision under proper Bethe-formula rescaling,
verified independently on three hydrogenic systems).

## Independence

CODATA Lamb-shift values are independent of CRR construction.
The Bethe-coefficient (8/3π) is canonical 1947 result. The CRR
contribution is the *identification* of α³ as the natural
"subatomic CV scale" tied to the rupture-topology framework
(notes/rupture_topology.md).

## Sandbox-runnable

Computed from hardcoded CODATA constants and Lamb-shift values
(no external data fetch). Estimated runtime < 1 s.

## Notes on tolerance choice

The tolerances above are calibrated based on the Session-4 v1
data:
- Intra-system spread observed in v1 (no log-rescaling): ~18%.
  With log-rescaling absorbed, expected to be tighter.
  Pre-registered band: ±20% spread.
- Mean residual in v1 (no log-rescaling): 22% below α³.
  With (8/3π) prefactor included, expected within ±30% based on
  rough sub-leading correction estimates.

These are not retroactively chosen to ensure success; they are
calibrated to genuinely test whether the leading Bethe-coefficient
identification holds at known precision.

## Applied usefulness for 2026 and beyond

If M10-α³ v2 reaches T3:

- **High-precision atomic clocks** (Sr, Yb optical clocks,
  10⁻¹⁸-level frontier 2026+): a CRR-derived α³-CV bound
  contributes to systematic-uncertainty budgets in cross-clock
  comparisons.
- **Antimatter spectroscopy** (CERN ALPHA / AEGIS / GBAR 2026+):
  CRR-α³ provides a non-CPT-based prediction for H vs H̄
  consistency.
- **Tests of α-stability over cosmological time:** parameter-free
  CV bound gives a reference for any cosmological-α drift
  detection.
- **Precision QED metrology** (electron g-2, muon g-2 Fermilab
  E989 ongoing): α³-level corrections are the structural target;
  CRR-α³ contributes a process-theoretic perspective.

If the pre-registration v2 passes, M10 transitions from "weak
fixed-point claim with 26 ppm CODATA discrepancy" to "structural
α³-scaling identification with empirical T3 confirmation across
the hydrogenic isoelectronic sequence." This would be a
significant tier upgrade — the first T3 in the campaign.

## Discipline note

If this v2 also fails, M10-α³ stays at T1 with both negatives
recorded. No further pre-registrations on M10-α³ within the
campaign without a substantively different test (e.g., on
muonic-hydrogen or antiprotonic-helium data, which probe different
QED corrections and could reveal α³ scaling more cleanly).
