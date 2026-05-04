# P5 — Empirical consistency: CSEP California seismicity (null result)

## Prediction (canonical brief)

Single-Ω CRR matches the ETAS (Epidemic-Type Aftershock Sequence)
baseline on California regional seismicity; nested CRR
*underperforms* ETAS there.

This is a **self-acknowledged null result** for the *nested* CRR
variant; for the *single-Ω* variant it is a **parity result** with
the canonical aftershock baseline.

## Empirical regularity

Source: **Collaboratory for the Study of Earthquake Predictability
(CSEP)** California regional testing centre, ETAS reference forecast
(Helmstetter, Kagan & Jackson 2007; Werner et al. 2011). Public.

URL: `https://cseptesting.org`

ETAS-baseline performance metrics on California (1985-2010 catalogue):
log-likelihood, T-test, N-test scores. Public.

## The two claims being assessed

**Claim P5.A — single-Ω CRR ≈ ETAS on California:** matches the
canonical ETAS baseline within standard CSEP testing thresholds.

**Claim P5.B — nested CRR < ETAS on California:** nested CRR
underperforms ETAS in CSEP scoring on California regional data.

## Tier decisions

### P5.A (single-Ω CRR matches ETAS): T2 conditional

A parity result with the canonical baseline (ETAS) is genuine
consistency, provided the CRR forecast was computed *blind* to the
test catalogue — i.e., the Ω parameter was set on training data,
not tuned on the test catalogue.

Promotion **conditional on** reviewer running the CRR forecast in
CSEP harness with pre-registered Ω from California training period
(1985–2000), evaluating on test catalogue (2001–2010).

The reproduction script `crr-engine/consistency/csep_california.py`
is committed (skeleton only — CSEP data fetch is outside the
sandbox). Mark as **[REVIEWER-RUN]**.

### P5.B (nested CRR underperforms): downgrade against any
"nested CRR is universally applicable" claim

This is **not a claim in our 42-item enumeration** — but it is
worth recording: the canonical CRR brief asserts P5.B
*self-acknowledges* that the nested CRR variant fails on California.
This is the campaign's first explicit downgrade candidate.

**Implication:** any future CRR-claim that extends nested CRR
universally must *exclude* California-style regional seismicity
or address why nested CRR fails there. The single-Ω variant is
not affected.

This is recorded in `notes/relabellings.md` as a domain-restriction
on nested-CRR's scope.

## Independence

CSEP is run by an unaffiliated international consortium (UC, USC,
NIED, ETH-Zurich, GFZ, …) with strict pre-registration discipline:
forecasts must be deposited before the test window. This is the
*gold standard* for independent earthquake-forecast testing.

If a CRR forecast were (a) deposited before the test window,
(b) evaluated by CSEP, and (c) matched ETAS, it would be one of the
strongest independent confirmations available in geophysics.

## Reproduction script

`crr-engine/consistency/csep_california.py` (skeleton):
1. Fetch CSEP California reference catalogue (1985–2010) from
   cseptesting.org.
2. Fit single-Ω on training portion (1985–2000): Ω = mean
   inter-event interval ≈ μ(coherent region)⁻¹ per Kac (M19).
3. Generate CRR forecast on test grid: rate λ_CRR(x,t) =
   1/Ω · exp(C(x,t)/Ω).
4. Run CSEP standard tests (N-test, L-test, T-test) against
   observed test catalogue (2001–2010).
5. Compare against ETAS reference forecast.

Single-Ω version expected to match ETAS within CSEP-test 95% CI
(per brief). **[REVIEWER-RUN]**

## Applied usefulness for 2026 and beyond

Earthquake forecasting is among the highest-stakes applied
domains where formal model evaluation already exists. Implications:

- **Operational hazard:** California's CSEP test centre evaluates
  forecasts continuously; any CRR-derived forecast that matches
  ETAS contributes to ensemble forecasting used by CGS / USGS for
  building-code revisions, insurance pricing, seismic-resilience
  investment.
- **Cross-region testing:** New Zealand's GeoNet, Japan's NIED,
  and Chile's CSN run analogous CSEP-style centres. A CRR forecast
  pre-registered in *multiple* regions tests whether the
  parameter-free Ω prediction holds globally or is region-specific.
- **Operational Earthquake Forecasting (OEF):** post-2025 OEF
  bulletins (e.g., USGS one-day aftershock probabilities) are now
  consumer-facing. Inclusion of a CRR forecast in OEF ensemble
  blends would reduce the dominance of ETAS in operational
  pipelines, providing model-uncertainty diversification.
- **Falsifier:** if CRR matches ETAS in California but fails in
  Japan or NZ, the universality of the SO(2) identification for
  seismicity is challenged — and the framework would need a
  region-specific Ω choice (or substrate-symmetry analysis).
- **Honest negative:** the *nested* CRR underperformance on
  California is recorded; without an explicit reason for the
  failure, "nested CRR" should not be sold operationally.

Earthquake forecasting is the cleanest applied test bed for CRR
because (a) the data are public, (b) the testing protocol is
standardised, (c) the baselines (ETAS) are mature, and
(d) end-users (engineers, insurers, civil defence) have actionable
demand for any incremental forecast skill.
