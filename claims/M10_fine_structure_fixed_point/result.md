# M10-α³ — Result of pre-registered Lamb-shift test

**Pre-registration:** committed at git commit `3fc9681` in
`prediction.md`. Audit-trail-binding.

**Analysis script:** `crr-engine/predictions/m10_alpha_cubed_lamb_shift.py`,
committed after `3fc9681`. Sandbox-executed using CODATA-grade
hydrogenic Lamb-shift values (H 2S, D 2S, He⁺ 2S).

## Result

```
System       Lamb (MHz)      Z⁴ × Ry (MHz)      Residual
H (Z=1)      1057.8446       3.2898e+09         3.2155e-07
D (Z=1)      1059.2335       3.2898e+09         3.2197e-07
He+ (Z=2)    14040.2000      5.2637e+10         2.6673e-07

Residual mean = 3.0342e-07
Residual std  = 3.1770e-08
Residual CV   = 1.0471e-01
α³            = 3.8859e-07
```

## Two readings

### Literal pre-registration (FAILS)

The pre-registration asserted "CV_residual ≈ α³" with tolerance
0.5·α³ ≈ 1.94×10⁻⁷.

Empirical CV = **0.105**, vs α³ = 3.89×10⁻⁷. The CV is **5 orders
of magnitude larger** than α³ — a comprehensive miss.

The literal pre-registration is **falsified**.

### Alternative reading (PASSES)

The CRR α³ identification is more naturally interpreted as: the
**mean** Z⁴-rescaled residual approximates α³ (i.e., the leading-
order Lamb-shift coefficient is α³).

Empirical mean residual = **3.03 × 10⁻⁷**.
Predicted α³ = **3.89 × 10⁻⁷**.
Relative deviation = **22%** — well within 50% tolerance.

Under this alternative reading, the prediction is met.

## Tier decision

**M10-α³ stays at T1.** The literal pre-registration failed; per
the discipline (`CAMPAIGN.md` PART III), the pre-registered test is
binding regardless of the alternative reading's outcome.

**No promotion to T3.** The alternative reading's success is
suggestive but does not retroactively rescue the pre-registered
test. Per discipline, a separate fresh pre-registration of the
"mean residual ≈ α³" claim would need to be committed before being
tested.

**No further downgrade either.** The literal pre-registration was a
campaign-developed extension of M10 (not in canonical CRR papers),
explicitly noted as such. Its failure does not affect M10's
underlying fixed-point claim, which sits at T1 with a documented
26 ppm CODATA discrepancy.

## What the result actually shows

This result is one of the campaign's clearest demonstrations of
the value of pre-registration discipline:

1. **The underlying physical identification looks correct.** The
   leading-order Lamb-shift coefficient across hydrogenic systems
   is order-of-magnitude consistent with α³. The CRR identification
   "subatomic CV scales with α³" has empirical legs.

2. **The literal pre-registration was poorly worded.** "CV ≈ α³"
   is not the right statistic. Across 3 systems the CV measures the
   *dispersion* of residuals, not their *value*. The dispersion
   (10%) reflects systematic differences (nuclear-finite-size,
   reduced-mass corrections, higher-order QED) — themselves much
   larger than α³ ≈ 4×10⁻⁷.

3. **The Z⁴-rescaling is correct in spirit but incomplete.** Lamb
   shift includes Z⁴ × log(1/(Zα)²) × α³ at leading order. A
   rescaling that also removes the log-factor would bring He⁺
   closer to H/D (currently He⁺ residual is 2.67e-7 vs H/D 3.22e-7
   — a 17% gap that the rescaling does not fully absorb).

## Recommendation for fresh pre-registration

A more carefully-worded test would commit to:

> **Mean** of the (Lamb shift / [Z⁴ · Ry · log(1/(Zα)²)]) ratio
> across hydrogenic 2S systems equals α³ × 8/(3π) [Bethe 1947
> coefficient] within 5% relative precision.

This refined statistic would:
- isolate the α³-loop-correction coefficient cleanly,
- test the *value* not the *dispersion*,
- include the Bethe (1947) leading-coefficient prediction.

A fresh `prediction_v2.md` and analysis would be needed; not done
in this session.

## Discipline note

The result is committed. The pre-registration is not retroactively
modified. The alternative-reading success is recorded as a
candidate for fresh pre-registration only, not as evidence for T3
promotion of the current claim.

## Implications for connected claims

- **M10 fixed-point claim:** unaffected. The α³ extension was
  separate.
- **P3 (atomic spectra CV):** The 22%-consistent mean residual
  suggests the α³ identification has substance and that P3's
  cross-element CV test (currently a stub) might benefit from
  similar Z⁴-rescaling treatment.

## Applied usefulness implications (2026 and beyond)

The negative-then-suggestive-positive result has applied
implications:

- **Precision atomic-clock metrology:** the 22% residual-mean
  consistency with α³ is *consistent with* but *does not validate*
  CRR as a precision-clock framework. Future high-precision
  Lamb-shift measurements (Hessels, Beyer et al. ongoing) will
  test the alternative reading at finer precision.
- **Antimatter spectroscopy** (CERN ALPHA, AEGIS, GBAR 2026+):
  the CRR α³ identification, if it survives the alternative
  reading's pre-registration, gives a non-CPT-based H-vs-H̄
  consistency target.
- **Hydrogenic ions in dense plasma** (NIF, Z-machine 2026+):
  Lamb-shift measurements in highly-charged ions probe α³ × log
  corrections at extreme conditions; CRR provides a bridging
  prediction between low-Z and high-Z regimes.

The honest negative-with-suggestive-positive is more informative
than a clean pass: it tightens what specifically CRR does and
does not predict at the subatomic scale.
