# P3 — Empirical consistency: Atomic spectral CV across 49 elements

## Prediction

Atomic-spectral CV across the 49 most-studied elements is consistent
with the M10 fine-structure derivation (CV-tied to α via the
self-consistency equation). Quantitative target: per-element
CV values clustered around CRR's α-derived prediction with
inter-element scatter set by atomic-Z scaling.

## Empirical regularity

Source: **NIST Atomic Spectra Database (ASD)** — Kramida et al.,
maintained at `https://physics.nist.gov/asd`. ~10⁵ tabulated
spectral lines covering all elements, public, machine-readable.

## Reproduction script

`crr-engine/consistency/nist_spectra.py` (skeleton):
1. Query NIST ASD for level energies and transition wavelengths
   per element (Z = 1 to 49 selected by canonical brief).
2. For each element, compute spectral CV across observed
   ground-state-allowed transitions.
3. Aggregate per-element CV values; compare against CRR-predicted
   distribution.

**[REVIEWER-RUN]** — sandbox blocks physics.nist.gov.

## Tier decision

**Remains T1 (T2 pending).** The CRR claim that 49-element atomic
spectra are consistent with the fine-structure derivation requires:
- a precisely-stated metric (which CV — over wavelengths? over
  Einstein A-coefficients? over level energies?);
- a precisely-stated prediction (CRR-derived value; the canonical
  brief is short on this);
- the actual cross-element computation.

None of these are committed yet at sufficient detail to constitute
a T2 reproduction. Promotion deferred to Session 4 (pre-registered
prediction phase).

## Applied usefulness for 2026 and beyond

- **Astrophysical spectroscopy:** JWST infrared spectroscopy of
  exoplanet atmospheres (in active operation 2026+) needs precise
  per-element line lists. A CV-bound on intra-element variability
  contributes to systematic-uncertainty budgets in atmospheric
  retrieval (e.g., planet C/O ratio measurements).
- **Plasma diagnostics in fusion (ITER, SPARC):** Stark-broadened
  spectral-line widths are temperature/density diagnostics; CRR
  CV-bound provides cross-element consistency check.
- **Stellar age-dating** (chromospheric Ca II K, Mg II h&k indices):
  CV across atomic-line ensembles tracks magnetic activity.
- **Quantum sensing** (Rb, Cs, Yb optical-pumping schemes): line-
  ratio dispersion bounds set magnetometer precision floors.

If P3 holds, the applied contribution is a *consistency check* for
spectroscopic measurement chains — most useful in cross-instrument
calibration pipelines.
