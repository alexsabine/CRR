# P1 — Pre-registered novel prediction: stellar generalisation

## Prediction

The CRR SO(2) prediction CV = 1/(4π) ≈ 0.0796 generalises beyond
the Sun to *any* late-type star (G/K/M dwarf) exhibiting a
chromospheric activity cycle.

**Quantitative pre-registration:** the population CV of Hale-cycle-
analogue durations (chromospheric Ca II H&K cycle period) across a
catalogued sample of stars with at least 3 complete cycles
observed shall lie within:

    CV_stellar ∈ [0.07, 0.09].

This is a tighter band than the original P1 SILSO Hale claim
[0.0767, 0.0820] because the stellar population provides
independent samples (one CV per star, then population CV across
stars).

## Empirical test

**Data targets (all public):**

1. **Mount Wilson HK Project** — long-baseline Ca II H&K
   chromospheric monitoring of ~80 stars (Wilson 1978; Baliunas
   et al. 1995; Hall et al. 2007 updates).
   URL: `https://mountwilsonsurvey.org` (or successor archives)
   citation: Baliunas et al. 1995, ApJ 438:269.

2. **Kepler / K2 long-baseline photometric variability** for
   chromospherically-active stars (Reinhold et al. 2017+ derived
   activity-cycle catalogues).
   URL: `https://archive.stsci.edu/kepler/` (MAST archive).

3. **TESS continuous monitoring** (2018–present, ongoing 2026+) —
   shorter baseline but more stars.
   URL: `https://archive.stsci.edu/tess/`

## Protocol

1. From Mount Wilson HK + Kepler-derived catalogues, identify all
   stars with **≥ 3 complete activity cycles** observed
   (eliminates systems with insufficient baseline).
2. For each star, compute the *intra-star* Hale-cycle CV from its
   own cycle durations.
3. Aggregate intra-star CVs into a population.
4. Compute the *population* CV (mean and std across the per-star
   CV ensemble).
5. Compare population mean to predicted 1/(4π) ≈ 0.0796.

## Quantitative pre-registration

Population mean of stellar Hale-cycle CVs:

    |⟨CV_per_star⟩ − 0.0796| < 0.010.

## Falsifier

If the population-mean CV departs from 0.0796 by more than 0.020
(2.5x the band), P1's stellar generalisation is falsified.
Specifically: a population-mean CV around 0.10–0.15 would suggest
chromospheric cycles do *not* follow SO(2) topology and may be
substrate-dependent (different stars might map to different
Lie groups).

## Independence

Mount Wilson and Kepler stellar-cycle catalogues were not used in
constructing P1 (which was derived from solar SILSO data). The
stellar generalisation is a genuine extrapolation.

## T3 promotion criterion

Population-mean stellar CV satisfies the band ⇒ P1 promotes to T3.
**This is the cleanest astrophysical T3 test in the campaign**:
public data, well-defined statistic, parameter-free CRR prediction.

## Applied usefulness for 2026 and beyond

- **Exoplanet habitability assessment:** chromospheric-cycle CV
  bounds host-star variability budgets that determine habitable-
  zone climate stability. CRR-derived CV gives a *parameter-free*
  prior for exoplanet-archive constraints (NASA Exoplanet
  Archive, ExoMol).
- **Radial-velocity exoplanet detection contamination:** stellar-
  cycle activity contaminates RV detection of small planets;
  CV bound informs activity-correction pipelines (HARPS-N, ESPRESSO,
  forthcoming HABEX/LUVOIR proposals).
- **Stellar-age dating** (gyrochronology, magnetic-braking age
  models): cycle CV is an age proxy; CRR-anchored CV calibration
  could supplement Skumanich-law / Mamajek-Hillenbrand calibrations.
- **Astro-seismology cross-checks** (TESS, PLATO 2026+): stellar
  oscillation modes vs activity cycles share rotational symmetry;
  CRR CV bound provides cross-channel consistency.
- **Solar analog identification:** sun-like-cycle stars (CV near
  0.080) are candidates for biosignature observations; CRR CV
  filter contributes to JWST / ARIEL / HWO target prioritisation.

P1's stellar generalisation is operationally relevant for any
2026+ exoplanet-discovery and characterisation programme that
must contend with host-star variability.
