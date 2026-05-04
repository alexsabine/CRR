# P2 — Pre-registered novel prediction: LIGO O5 catalogue forecast

## Prediction

The CRR SO(2) prediction CV = 1/(4π) ≈ 0.0796 holds for the
LIGO/Virgo/KAGRA O5 observing run binary-black-hole population
(O5 began 2027, ongoing, expected 200+ BBH events post-completion).

**Quantitative pre-registration:** the post-O5 BBH radiated-fraction
CV will satisfy:

    CV_O5_BBH ∈ [0.075, 0.090].

This **tightens** the current GWTC-1/2/3 90% CI [0.077, 0.114] on
the basis that increased sample size will narrow the CI around the
true value. The CRR prediction commits to the lower portion of the
current band (which is where 1/(4π) ≈ 0.0796 sits).

## Empirical test

**Data target:** **GWTC-O5 catalogue** (LIGO/Virgo/KAGRA
Collaboration, expected release 2028).
URL: `https://www.gwosc.org` — eventually `gwtc-o5/` endpoint.

**Statistic:** radiated-mass fraction E_rad/M_total computed per
event from source-frame component masses and final mass:

    f_rad = (m₁ + m₂ − m_final) / (m₁ + m₂)

CV = std(f_rad) / mean(f_rad) across all O5 BBH events.

## Protocol

1. Fetch O5 catalogue when released.
2. Filter to BBH events with full source-frame mass triples
   (m₁, m₂, m_final) and signal-to-noise ratio ≥ 8.
3. Compute f_rad per event.
4. Compute population CV.
5. Compare to predicted band [0.075, 0.090].

## Quantitative pre-registration

P2-O5 promotes to T3 iff:

    CV_O5_BBH ∈ [0.075, 0.090]   AND   number of events ≥ 100.

The sample-size requirement is to ensure statistical power: O5 is
expected to deliver ~200 BBH detections, sufficient for tight CV
estimation.

## Falsifier

Two falsification modes:
1. **CV outside [0.070, 0.095]** with N ≥ 100: the SO(2)
   identification fails for the BBH population; CRR's CV bound is
   broken.
2. **CV inside [0.070, 0.095] but tightened CI excludes 0.0796**
   (e.g., point estimate 0.085 with tight CI [0.082, 0.088]): the
   identification holds order-of-magnitude but is not exact;
   downgrade to T2-marginal-confirmed.

## Independence

The O5 catalogue does not exist as of the campaign date; the
prediction is committed before any O5 data is publicly released.

## T3 promotion criterion

CV in [0.075, 0.090] AND N ≥ 100 ⇒ **P2 promotes to T3**.

## Applied usefulness for 2026 and beyond

- **Standard-siren cosmology with O5/O6 catalogues:** Hubble-
  tension resolution efforts use BBH posterior distributions;
  population-CV prior tightens the BBH-derived H₀ posterior. Each
  BBH contributes ~10% relative-precision constraint on H₀; with
  100+ BBH the H₀ from GW pure-standard-siren approach ~1%.
- **Population-synthesis model selection:** CV bound differentiates
  isolated-binary vs dynamical-formation models without requiring
  individual-event spin/mass-ratio likelihoods.
- **Multi-messenger triggering** (kilonova chasers): if BBH
  population CV is tight, posterior on remnant mass/spin is
  sharper, improving electromagnetic-follow-up triggering for
  systems with potential disks (NS-BH, EMRI hybrids).
- **LISA cross-band consistency** (launch ~2035): supermassive BBH
  populations should obey the same CRR CV; LIGO O5 and LISA
  cross-validation gives a 10-decade dynamic-range cross-check.
- **Test of binary-coalescence universality:** CV measures
  "how universal" the BBH coalescence process is; CRR predicts
  parameter-free universality, which is a strong claim about
  formation-channel independence.

If P2-O5 confirms, CRR has a **direct claim on the gravitational-
wave era**: a parameter-free prediction confirmed on the largest
BBH catalogue ever assembled. This would be among the strongest
applied-physics confirmations of CRR.
