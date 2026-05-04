# P5 — Pre-registered novel prediction: global repeating-earthquake CV

## Prediction

The single-Ω CRR forecast that matches ETAS on California (P5
canonical claim) generalises to other tectonic regions: Japan,
New Zealand, Chile. Specifically, in any region where ETAS is the
operational baseline, single-Ω CRR matches it within CSEP-test
95% CI.

**Quantitative pre-registration:** for each of three test regions
(Japan, NZ, Chile), single-Ω CRR forecast scored against the
region's operational seismic catalogue must satisfy:

    |L_CRR − L_ETAS| / |L_ETAS| < 0.10

where L is the CSEP log-likelihood score. (10% relative agreement
in log-likelihood corresponds to single-Ω CRR being effectively
indistinguishable from ETAS at conventional CSEP-test thresholds.)

## Empirical test

**Data targets:**

1. **GeoNet (New Zealand)** — open seismic catalogue.
   URL: `https://www.geonet.org.nz/data`

2. **NIED (Japan, F-net + Hi-net)** — open earthquake catalogue.
   URL: `https://www.fnet.bosai.go.jp`

3. **CSN (Chile)** — Chile's national seismic catalogue.
   URL: `https://www.sismologia.cl`

For each region:
- Use the local CSEP-style testing framework (or equivalent
  scoring on local catalogue).
- Train Ω on a pre-test window (typically 10-15 years).
- Forecast on a test window (typically 5-10 years).
- Score against ETAS reference for that region.

## Protocol

For each region r ∈ {Japan, NZ, Chile}:
1. Fetch regional catalogue with M_w ≥ M_completeness (region-
   specific).
2. Fit single-Ω = mean inter-event interval over training window
   (per Kac convention C5; Ω = μ(coherent region)).
3. Generate CRR forecast on test grid for test window.
4. Compute CSEP-style L (log-likelihood) score.
5. Compare to ETAS reference for the region.

## Quantitative pre-registration

P5-global promotes to T3 iff for **all three regions**
|L_CRR − L_ETAS| / |L_ETAS| < 0.10.

If satisfied for 2 of 3 regions, P5 stays at T2 (region-dependent
applicability). If satisfied for 1 or 0, **the SO(2) identification
for seismicity is downgraded** to "California-specific" rather
than universal.

## Falsifier

|L_CRR − L_ETAS| / |L_ETAS| > 0.30 in *any* region ⇒ single-Ω
CRR is **substantially worse** than ETAS in that region; structural
problem with the SO(2) identification for tectonic seismicity.

## Independence

GeoNet, NIED, CSN catalogues are independent of CSEP California
(and of CRR's construction). Single-Ω is a parameter-free CRR
forecast; "free parameter" is only the training-window choice
(committed here as 10-15 years pre-test, region-specific).

## T3 promotion criterion

All three regions' L-score relative agreement < 0.10 ⇒
**P5 promotes to T3** (and the *nested-CRR* California null
remains as a separate-scope restriction in `relabellings.md`).

## Applied usefulness for 2026 and beyond

- **Operational Earthquake Forecasting (OEF) globalisation:** USGS
  one-day aftershock probabilities are now consumer-facing
  (smartphone push notifications via ShakeAlert in California /
  Oregon / Washington 2026+). Adding CRR forecast to OEF ensemble
  provides model-uncertainty diversification; if P5-global
  confirms, deployment to international OEF systems
  (Japan JMA early-warning, Mexico SASMEX, Italy INGV) becomes
  defensible.
- **Catastrophe-bond pricing:** seismic CAT bonds use ETAS-derived
  exceedance probabilities; CRR CV bound contributes parameter-
  free anchor.
- **Resilience-investment prioritisation:** government and
  insurance-pool seismic-risk modelling (FEMA Hazus, RMS, Verisk
  AIR Worldwide) blend ETAS with regional empirical adjustments;
  CRR forecast is an alternative input.
- **Building-code revision cycles:** ASCE 7-22 and successors
  use seismic-hazard maps from USGS PSHA; OEF-derived adjustments
  enter at the time-dependent component. CRR contributes if
  P5-global confirms.
- **Tsunami warning** (NOAA NWS, JMA, INCOIS): subduction-zone
  earthquake forecasting feeds tsunami-risk products; CRR provides
  ensemble-modelling input.

P5-global is the **highest-stakes applied test in the campaign**.
Earthquake forecasting is operationally consumed by hundreds of
millions of people; even modest forecast-skill improvements have
direct life-and-property impact.
