# M10 — Pre-registered novel prediction: subatomic CV scales with α³

## Origin of this prediction

The user, in Session 4, nominated this prediction with the following
framing: *"there is an idea there about fine-structure constant
cubed being used to test CV rates at subatomic scales."*

A direct grep of the canonical CRR papers (`crr_137(attempt).pdf`,
`CRR_CV_Derivation.pdf`, `CRR_CV_Predictions.pdf`,
`CRR_Quantum_Correspondence.pdf`) does **not** locate an explicit
α³ statement. So this pre-registration is a **campaign-developed
extension** of M10, motivated by the Lie-group structure
established in `notes/rupture_topology.md` and the user's prompt.
It is recorded transparently as such.

## Derivation of the α³ prediction from CRR principles

Two complementary motivations:

**(i) Bound-state radiative-correction scaling.**
The Lamb shift in hydrogenic atoms scales as α⁵ × m_e × c² × R∞ in
absolute units; in *units of the Rydberg energy*, the leading Lamb-
shift contribution scales as α³. So the *relative dispersion* of
Lamb-shift contributions across hydrogenic ions naturally has α³
as its characteristic size.

**(ii) CRR rupture-topology at the subatomic scale.**
At the atomic scale, CRR's SO(2) prediction gives CV = 1/(4π).
At the subatomic radiative-correction scale, the relevant phase
manifold is the *internal* gauge-coupling space. If the geodesic
length on this space is α³-suppressed relative to the SO(2)
geodesic 2π — because radiative corrections enter as α-suppressed
loop corrections to the leading-order coupling — then:

    CV_subatomic = α³ × CV_SO(2) = α³ / (4π) ≈ **3.10 × 10⁻⁸**

Or equivalently (alternative identification):

    CV_subatomic = α³ ≈ **3.89 × 10⁻⁷**

The two identifications differ by the factor 1/(4π) ≈ 0.080;
empirically distinguishable at the precision of modern hydrogenic
spectroscopy.

This pre-registration commits to the second identification
(CV_subatomic = α³) as the cleanest form, while noting that
the data may favour the 1/(4π)-corrected version.

## Empirical test

**Target:** Lamb-shift relative dispersion across the hydrogenic
isoelectronic sequence.

**Specific systems:**
- H (Z=1) 2S₁/₂ Lamb shift
- D (Z=1, deuteron) 2S₁/₂ Lamb shift
- He⁺ (Z=2) 2S₁/₂ Lamb shift
- Li²⁺ (Z=3) 2S₁/₂ Lamb shift
- Be³⁺ (Z=4) 2S₁/₂ Lamb shift

**Statistic:** the CV (std/mean) of Lamb-shift values across
these five systems, after rescaling by the leading-Z⁴
hydrogenic dependence to isolate the α³-loop-correction component.

**Data target:** **CODATA 2018 / 2022** recommended values for
hydrogenic Lamb shifts, supplemented by Hessels & co-workers'
high-precision measurements (2019–2024).

  URL: `https://physics.nist.gov/cuu/Constants/`

## Quantitative pre-registration

After Z⁴-rescaling, the **residual dispersion CV** across the five
hydrogenic Lamb shifts must satisfy:

    |CV_residual − α³| < 0.5 · α³

i.e., agreement at **better than 50% relative precision** with
α³ ≈ 3.89 × 10⁻⁷.

Equivalently: |CV_residual − 3.89 × 10⁻⁷| < 1.95 × 10⁻⁷.

**Note on tolerance:** 50% relative tolerance is generous; a sharp
test would tighten to ~10%. The 50% band reflects the campaign's
genuine uncertainty about which identification (raw α³ vs α³/(4π))
is correct, plus systematic-error budgets in hydrogenic-Lamb-shift
measurements.

## Falsifier

If the residual CV after Z⁴-rescaling differs from α³ by more than
factor of 2 (i.e., outside [α³/2, 2α³]), the M10-α³ extension is
falsified. **The M10 fixed-point claim itself is unaffected** —
only this α³ extension would be downgraded.

If the residual CV is within [α³/(4π × 2), α³ × 2] (i.e., spanning
both the raw α³ and α³/(4π) identifications), the test is
**inconclusive**; no promotion.

## Independence

Hydrogenic Lamb-shift measurements pre-date this prediction.
The Z⁴-rescaling protocol is standard hydrogenic-spectroscopy
practice (uncoupled to CRR). The α³ identification is the
prediction; its match (or mismatch) to the post-rescaled empirical
CV is the test.

## T3 promotion criterion

If the residual CV satisfies |CV_residual − α³| < 0.5 · α³,
**M10 is promoted to T3** (specifically, the α³ extension; the
26 ppm CODATA discrepancy on the original M10 fixed-point claim
remains an open issue).

## Applied usefulness for 2026 and beyond

A confirmed α³ subatomic CV scaling has implications for:

- **High-precision atomic clocks** (Sr, Yb, Al⁺ optical clocks):
  CV bound on within-clock-species energy-level dispersion
  contributes to systematic-uncertainty budgets at 10⁻¹⁸-level
  precision (the current frontier).
- **Tests of α-stability over cosmological time** (Webb / King /
  Murphy debates): a parameter-free CV prediction for hydrogenic
  systems gives an absolute reference against which any
  cosmological-α drift would manifest.
- **Hydrogen-deuterium spectroscopy in interstellar medium**
  (JWST + ELT IR spectroscopy 2026+): high-z Lyman-α / Lyman-β
  ratio measurements probe α at high redshift; CRR CV bound
  feeds into systematic-error analysis.
- **Antihydrogen spectroscopy** (CERN ALPHA, AEGIS, GBAR 2026+):
  CV consistency across H / H̄ levels is a CPT-test target;
  CRR provides a non-CPT-based prediction.
- **Quantum-electrodynamic precision tests**: anomalous magnetic
  moment of the electron and muon (g-2) — the muon g-2 anomaly
  (Fermilab E989 results, ongoing 2026+) sits at α³-level
  significance; CRR CV bound is structurally related.

The α³ subatomic test is **the cleanest CRR bridge to precision
atomic physics**. If confirmed, it gives CRR a direct claim on
fundamental-constant metrology. If falsified, it bounds CRR's
applicable scale: the framework would not extend below the atomic
to the radiative-correction regime without additional structure.
