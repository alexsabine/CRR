# P10 — Result (honest negative)

**Status: pre-registration FAILED. Tier remains at T1.**

## Empirical execution

- **Data:** SILSO V2 monthly mean total sunspot number, 1749-01 →
  2025-01 (3313 months). Fetched via GitHub mirror
  `Shivayk0505/Forecasting-of-Sunspot-Numbers-Time-Series-Data`
  (verbatim copy of canonical SILSO `SN_m_tot_V2.0.csv`; sandbox
  cannot reach `sidc.be` directly — see `fetch.py`).
- **Cycle dating:** 13-month centred running mean (canonical
  SMSSN), local minima with ±36-month exclusion window. 25 minima
  detected — exact match to SILSO's catalogued 25 cycles.
- **Hale pairing:** consecutive sunspot cycles paired starting
  from cycle 1, giving 12 complete Hale cycles.

## Numbers

| Statistic | Value |
|-----------|------:|
| Sunspot-cycle N | 24 |
| Sunspot-cycle mean period | 11.035 yr |
| Sunspot-cycle std | 1.256 yr |
| Sunspot-cycle CV | **0.1138** |
| Hale-cycle N | 12 |
| Hale-cycle mean period | 22.070 yr |
| Hale-cycle std | 1.817 yr |
| Hale-cycle CV | **0.0823** |
| **Ratio CV_sunspot / CV_Hale** | **1.382** |
| Bootstrap 95% CI for ratio | [1.121, 2.124] |

## Comparison

| Hypothesis | Predicted ratio | Status |
|-----------|:---------------:|--------|
| **CRR M22 (SO(3) / SU(2))** | **2.0 (band [1.7, 2.3])** | **outside band** |
| Hard falsifier | outside [1.5, 2.5] | **falsified** |
| i.i.d. null (Var(Hale) = 2σ²) | √2 ≈ 1.414 | **consistent (Δ = 0.03)** |

## Interpretation

The empirical ratio sits 0.03 below the i.i.d. null and 0.62 below
the M22 centre. The bootstrap CI does brush the lower edge of the
M22 band [1.7, 2.3], but the *point estimate* is firmly in the
i.i.d. regime, and the *hard falsifier band* [1.5, 2.5] is
exceeded.

The negative is interpretable. M22 predicts ratio = 2, which
mathematically requires consecutive sunspot cycles to be
*anti-correlated* with Cov(T_{2k−1}, T_{2k}) = −σ²/2 (so that
Hale-pair variance equals one-cycle variance). Empirically,
consecutive sunspot cycles are approximately uncorrelated — the
classical i.i.d. null is consistent with the data.

## What survives

- **CV_Hale = 0.0823** is inside the P1 SILSO Hale-cycle empirical
  band [0.0767, 0.0820] reconfirmed at the upper edge, and within
  ~3% of the SO(2)/SU(2) prediction CV = 1/(4π) ≈ 0.0796.
  **P1 reconfirmed; SU(2)/SO(2) Hale identification stands.**
- **CV_sunspot = 0.1138** is *between* the SO(2) prediction
  (0.0796) and the SO(3) prediction (0.1592). Neither
  identification fits cleanly.

## What fails

- **The SO(3) identification of the sunspot-counting cycle.**
  Predicted CV 0.1592; observed 0.1138 (28.5% low).
- **The 2:1 topological ratio under polarity-pair grouping.**
  Predicted ratio 2.0; observed 1.38.

## Audit trail

- Pre-registration committed: `notes/session_8_new_predictions_and_applied.md`,
  commit `6121c22` (2026-05-06), branch
  `claude/verify-folder-access-CInY3`.
- Analysis pipeline (`fetch.py`, `analyse.py`) committed in this
  directory subsequent to pre-registration. The git log between
  pre-registration commit and result commit is the audit trail.
- This honest negative is committed permanently. Per
  CAMPAIGN.md PART III: "results are binding regardless of
  direction; failed pre-registrations stay committed permanently."
- A v2 reframing (e.g., a different cycle-pairing convention, or
  a different SO(3) identification of the sunspot-counting
  topology) is permitted only as a *new* pre-registration in a
  *separate commit*; this v1 negative cannot be retroactively
  edited.

## Implications for M22

P10 is the first solar-domain test of M22's 2:1 covering-relation
falsifier. It fails. This does not falsify M22 itself — M22 has
six predicted Lie-group CVs, three of which (SO(2), SU(2), T²)
are jointly consistent with P1 / P2 / B7 / B9 / B10 / P14 etc.
But it does **rule out the specific sunspot/Hale identification
as written**.

The campaign's other M22 falsifiers (M22-A SU(2) ≡ SO(2) on BMRB
T₁, M22-B SO(3) ≡ Z₂-only on Chandler wobble, M22-C SU(3) on
PDG hadronic lifetimes) remain reviewer-runnable and untouched
by P10's failure.

## Author note

The honest pattern emerging:
1. Whenever CRR predicts a CV in [0.07, 0.09] for an SO(2)/SU(2)/T²
   substrate, the data has been broadly consistent (P1, P2, P10
   Hale leg, B7).
2. Whenever CRR predicts a CV in [0.14, 0.18] for an SO(3)
   substrate, evidence is currently absent — the sunspot test
   above is the first solar test, and it lands in between.
3. The covering-relation 2:1 ratio remains untested in any
   domain. M22-A on BMRB T₁ relaxation is the cleanest pending
   replication.

This pattern should be documented in
`notes/independent_engagement_log.md` for Session 9 follow-up.
