# Session 12 — Three new pre-registered CRR tests on financial / economic event data

This document pre-registers three new CRR predictions using
publicly-available financial and macroeconomic event series.
Each tests a distinct CRR substrate identification under the
four-tier CV ladder formalised in `notes/session_11_no_regulator_baseline.md`.

The pre-registration commit hash is the binding audit anchor.
Per CAMPAIGN.md PART III, tolerance bands and falsifier bands
cannot be retroactively edited.

---

## P27 — VIX volatility-spike inter-arrival CV (no-regulator hypothesis)

### Statement

Inter-event intervals between days on which the CBOE VIX index
closes at or above 30 (the canonical "fear-regime" threshold;
Whaley 2000) are predicted to follow the **CRR no-regulator
boundary**: VIX spikes are externally driven by news / macro /
geopolitical shocks with no SO(2) or Z₂ phase manifold on the
market side. Under the four-tier CV ladder, no-regulator events
have CV → 1.

### Substrate

**No regulator** (CV → 1).

### Pre-registration

Across the full datasets/finance-vix daily-close series 1990 →
test-execution date,

    CV(inter-spike interval) ∈ [0.85, 1.15]   AND   N_spikes ≥ 30.

### Falsifier

CV outside [0.70, 1.30] with N ≥ 30.

A CV substantially below 1 (say 0.4–0.7) would suggest a hidden
regulator (e.g., a market-wide volatility cycle); CRR's
no-regulator identification would fail.

### Dataset

`datasets/finance-vix` GitHub repo, `data/vix-daily.csv`.
Canonical CBOE VIX daily OHLC since 1990-01-02.

### T3 promotion criterion

CV ∈ [0.85, 1.15] with N ≥ 30 + multi-domain replication (this
is the second domain in the broader P26 no-regulator baseline,
after I6 cyber).

---

## P28 — NBER US recession peak-to-peak interval CV (substrate-discriminating)

### Statement

NBER-dated US business-cycle recessions are tested as a *substrate
discrimination*: which CRR substrate, if any, governs inter-
recession timing? The pre-registration commits to *all three*
substrates simultaneously and reports which (if any) is matched.

### Substrate hypotheses

Three candidate substrates, each with an a priori prediction:

- **No-regulator (Poisson, no business cycle):** CV ≈ 1.0,
  band [0.85, 1.15].
- **Z₂ (binary expansion/recession switch):** CV ≈ 0.159,
  band [0.140, 0.180].
- **SO(2) (continuous business-cycle phase):** CV ≈ 0.080,
  band [0.070, 0.090].

### Pre-registration

Using NBER-published peak dates (post-WWII recessions only, peak
of 1948-11 through peak of 2020-02 inclusive, N = 12), compute
inter-peak intervals in months. CV = std/mean.

The result is reported against all three substrate bands. If CV
falls into one band, that substrate is identified. If CV falls
outside all three bands, no CRR substrate is identified for the
US business cycle.

### Falsifier

If CV falls outside [0.06, 1.30] *and* N ≥ 11, the entire CRR
four-tier ladder is inconsistent with US business-cycle timing.

### Dataset

NBER post-WWII business-cycle peak dates, embedded in
`analyse.py` (committed at this pre-registration). The 12 peaks
are: 1948-11, 1953-07, 1957-08, 1960-04, 1969-12, 1973-11,
1980-01, 1981-07, 1990-07, 2001-03, 2007-12, 2020-02. Source:
`https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions`
(referenced; the dates themselves are public-domain facts and
not subject to NBER access restrictions).

### T3 promotion criterion

CV ∈ one of the three pre-registered bands with N ≥ 11.

### Industrial bottleneck

Recession forecasting is a notoriously hard problem.
Macroeconomic-policy timing (Fed, ECB, BoJ rate-setting),
fixed-income strategy ($130 trn bonds), and CAT-bond pricing
all depend on probabilistic recession-timing models. A
parameter-free CRR substrate identification (or its honest
absence) sharpens what kind of model can be built.

---

## P29 — S&P 500 monthly drawdown-event inter-arrival CV (no-regulator hypothesis)

### Statement

Months in which the S&P 500 total real return falls below −5%
are tested for CRR substrate. A priori, equity drawdowns are
externally driven by macro shocks → predict no-regulator (CV
→ 1). A finding of CV ∈ Z₂ band would suggest a market-internal
binary regime-switching regulator; SO(2) would suggest a
continuous business-cycle regulator on monthly timescale.

### Substrate

**No regulator** (CV → 1) is the primary hypothesis.

### Pre-registration

Across `datasets/s-and-p-500` monthly close series 1871-01 →
test-execution date,

    CV(inter-drawdown interval) ∈ [0.85, 1.15]   AND   N_drawdowns ≥ 30.

### Falsifier

CV outside [0.70, 1.30] with N ≥ 30.

### Dataset

`datasets/s-and-p-500` GitHub repo, `data/data.csv`. Robert
Shiller's canonical SPX dataset from 1871; monthly resolution;
1864 observations.

### Drawdown definition

Drawdown event = month-on-month real-price return less than
−5%. Real price column (Real Price) is used (CPI-adjusted).
Sign convention: log(Real Price[t] / Real Price[t-1]) < −0.05.

### T3 promotion criterion

CV ∈ [0.85, 1.15] with N ≥ 30 + multi-domain replication via
P26.

---

## Joint significance for the no-regulator baseline P26

If P27 (VIX spikes) and P29 (SPX drawdowns) both pass the
no-regulator band, this constitutes:

- Two independent financial-market domain confirmations of
  the no-regulator boundary.
- Combined with I6 cyber-incidents (107 firms, CV = 0.969),
  three independent domain confirmations of CV → 1 at the
  no-regulator boundary.

The aggregate provides P26-style multi-domain support, even
if no single test is at T3 in isolation.

If P28 (NBER recessions) lands in one of the three substrate
bands, that substrate is the CRR identification of the US
business cycle. If it lands in none, the US business cycle has
no clean CRR substrate identification at the post-WWII
N = 12 sample size.

---

## Audit-trail anchor

This file's commit hash on push to branch
`claude/verify-folder-access-CInY3` is the binding pre-
registration commit for P27, P28, P29. Analysis scripts must
be committed *after* this commit. Honest negatives committed
permanently.
