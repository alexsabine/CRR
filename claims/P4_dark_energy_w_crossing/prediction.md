# P4 — Pre-registered novel prediction: post-2026 cosmology w(z) crossing

## Prediction

The DESI Year-1 + Pantheon+ + CMB joint analysis (2024) showed
preliminary evidence for w(z) crossing −1 near z ≈ 0.4 at ~3-4σ.
CRR predicts the crossing should persist at z ≈ 0.5 in
post-2026 datasets with tightened error budgets:

**Quantitative pre-registration:** the post-2026 joint cosmological
analysis (DESI Year-3 BAO + Euclid Year-1 weak-lensing + Roman
Space Telescope Year-1 SN-Ia) shall show:

    w(z) crossing −1 at z_cross ∈ [0.40, 0.60]
    AND
    crossing significance ≥ 5σ over ΛCDM.

The 5σ threshold pushes the prediction past "preliminary" into
"definitive" cosmological-discovery territory.

## Empirical test

**Data targets (all expected public 2026-2028):**

1. **DESI Year-3 BAO** — 6× the Year-1 sample.
   URL: `https://data.desi.lbl.gov`
2. **Euclid Year-1 weak-lensing + 3×2pt** — 2026 release.
   URL: `https://www.cosmos.esa.int/web/euclid`
3. **Roman Space Telescope Year-1 SN-Ia** — 2027+ release.
   URL: `https://roman.gsfc.nasa.gov`
4. **CMB-S4 + LiteBIRD** (later 2030+, optional cross-check).

## Protocol

1. Aggregate DESI-Y3 BAO + Euclid-Y1 + Roman-Y1 SN data using
   standard joint-likelihood pipeline (e.g., Cobaya / CosmoMC /
   CosmoSIS).
2. Reconstruct w(z) tomography via Gaussian-process regression
   (Holsclaw et al. 2010; or DESI collaboration's CPL / w0wa
   parameterisation).
3. Locate w = −1 crossing redshift z_cross with 1σ band.
4. Compute Δ(log Z) Bayes factor: w(z) ≠ −1 model vs ΛCDM.

## Quantitative pre-registration

P4 promotes to T3 iff:

    z_cross ∈ [0.40, 0.60]
    AND
    Δ(ln Z) ≥ 11.5 (corresponds to ~5σ in nested model comparison).

If z_cross ∈ [0.30, 0.70] with Δ(ln Z) ≥ 11.5, P4 stays at
T2-confirmed (broader band; partial validation).

## Falsifier

Two falsification modes:

1. **w(z) ≡ −1 (cosmological constant) at high significance:** if
   post-2026 data tightens to ΛCDM with Δ(ln Z) for w(z) ≠ −1
   model BELOW 5, P4 is downgraded.

2. **w(z) crossing OUTSIDE [0.30, 0.70]:** the crossing exists but
   at the wrong redshift; CRR's z ≈ 0.5 identification fails.

## Independence

DESI-Y3, Euclid-Y1, Roman-Y1 datasets do not exist as of the
campaign date. Pre-registration is committed before data release.

## T3 promotion criterion

z_cross ∈ [0.40, 0.60] AND Δ(ln Z) ≥ 11.5 ⇒ **P4 promotes to T3**.

## Applied usefulness for 2026 and beyond

- **Hubble-tension resolution:** if dark energy crosses w = −1, H₀
  systematic drift between local and CMB measurements may be
  explained by a non-constant w(z) extrapolation. CRR contributes
  a *non-ad-hoc* mechanism (rather than ad-hoc quintessence
  parameterisations).
- **Modified-gravity vs. dark-energy distinction:** w(z) shape
  constrains modified-gravity (f(R), DGP, etc.) vs. dynamical
  dark-energy explanations. CRR's R[χ] regeneration kernel sits
  in the dynamical-dark-energy class.
- **Cosmological-constant problem:** the ~120 orders of magnitude
  discrepancy between observed and naively-calculated vacuum
  energy is unsolved; if w ≠ −1 dynamics explain the observed
  scale, CRR contributes a process-theoretic perspective on why
  the small observed value is *natural* (rather than fine-tuned).
- **Survey-strategy optimisation:** Roman, Euclid, Rubin/LSST
  observation cadences could be optimised in real-time to maximise
  w(z) crossing constraint. CRR-specified target redshift z ≈ 0.5
  guides survey-cadence prioritisation.
- **Inflation theory cross-check:** w(z) shape constraints on
  early-universe physics propagate via integrated-Sachs-Wolfe and
  CMB-lensing. CRR-derived w(z) provides an alternative
  early-universe scenario testable by next-generation CMB
  experiments (CMB-S4, LiteBIRD).

P4-DESI is **the most consequential cosmological prediction in the
campaign**. A CRR-confirmed w(z) crossing would rank among the
most significant theoretical-cosmology results of the decade.
