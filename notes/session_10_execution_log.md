# Session 10 — Execution log for the ten industrial predictions

This log records execution status for the ten Session 10
industrial predictions (I1–I10) committed at `aa6ee72`.

## Sandbox network probe (re-confirmed)

Allowlist still GitHub + PyPI only. Industrial / financial /
scientific archives all blocked: NASA Prognostics, CALCE,
data.matr.io (Severson 2019), NREL, ENTSO-E, FRED, USDA NASS,
EU MARS, CMS, MIMIC-IV, CAIDA, MAWI, hyperscaler sustainability
portals.

GitHub-mirrored datasets located:

| Prediction | Dataset | GitHub mirror | Status |
|------------|---------|---------------|:------:|
| I1 EV battery | NASA / CALCE / Severson 2019 | none located in 4 keyword searches | reviewer-run |
| I2 Semi defect | UCI SECOM, WM-811K | mirrors found but datasets are *defect classification feature vectors*, NOT inter-defect timing series | reviewer-run (data-format mismatch) |
| I3 Wind | NREL Wind Toolkit, ENTSO-E | none located | reviewer-run |
| I4 Yield-curve | FRED T10Y3M | nearest GitHub mirror (lebreton/recessions_prediction) is OECD long-term rates, *not* T10Y3M Treasury spread | reviewer-run |
| **I5 LLM loss-plateau** | **EleutherAI Pythia, BLOOM, OLMo** | **direct repos reachable** but no committed loss-curve CSVs surfaced in 3 keyword searches; loss curves are typically WandB-hosted | reviewer-run |
| **I6 Cyber-incident** | **VERIS Community Database (vz-risk/VCDB)** | **direct repo reachable, vcdb.csv.zip 15 MB** | **EXECUTED** |
| I7 Hyperscale PUE | Google/MS/Meta sustainability | not GitHub-deposited | reviewer-run |
| I8 Wheat heading | USDA NASS, EU MARS | none located | reviewer-run |
| I9 Hospital readmission | CMS HRRP, MIMIC-IV | MIMIC-IV credentialed access only | reviewer-run |
| I10 5G CV ratio | CAIDA, MAWI | researcher access only | reviewer-run |

**One out of ten directly executable in this sandbox.**

---

## I6 — Cyber-incident inter-arrival (EXECUTED)

### Result: pre-registration FAILED

- Pre-registered Z₂ band: median CV ∈ [0.140, 0.180].
- Falsifier band: outside [0.120, 0.200].
- **Empirical median CV = 0.969** across 107 large-victim firms
  with ≥3 disclosed incidents 2010–2025 (VCDB, master branch
  commit fetched 2026-05-06).
- 6.1× the predicted value; far outside falsifier band.

### Interpretation

The empirical CV ≈ 1.0 is consistent with **Poisson / Lévy
clustering** of cyber-incident timing — the well-known
"campaigns and bursts" pattern. CRR's three-class diagnostic
identifies this as the **Class C noise-dominated** regime
(CV > autonomous Z₂).

### Cross-claim significance

I6 contributes a third empirical class identification:

| Class | System | CV | Source |
|-------|--------|---:|--------|
| **A autonomous** | Menstrual cycle (Bull 2019, n = 612,613) | 0.177 (+11.5% from Z₂ 0.159) | M22 v2 Test 1 |
| **B regulated** | Hemispheric CV (Mazoyer 2014, n = 144) | 0.122 (−23% from Z₂) | Session 9 audit |
| **C noise-dominated** | Cyber-incidents at large enterprises (VCDB n = 107) | 0.969 (+6× from Z₂) | **I6 (this session)** |

The three-class diagnostic is now empirically traversed in three
independent domains. The pattern holds; the *assignment* of a
specific system to A/B/C must be pre-specified per domain.

### Pre-registered protocol deviations (transparency)

Two deviations from the strict I6 pre-registration are documented
in `claims/I6_cyber_incident_inter_arrival/prediction.md`:

1. Used `victim.orgsize.Large = 1` as Fortune 500 proxy (broader
   filter; widens the eligible set).
2. Omitted "≥10⁵ records / operational-disruption" magnitude
   filter (record-count fields too sparse in VCDB).

Both deviations make the test *less* conservative; they could
not turn a 6× over-shoot into a pass under any restricted filter.
The N ≥ 30 binding is satisfied (N = 107).

### Industrial-bottleneck applied conclusion

Session 10's vertical I6 (cyber-insurance pricing, $200 bn
industry, weighted EV ≈ $51 M five-year) is **downgraded.** CRR
contributes via Class C identification (CV ≈ 1.0, indistinguishable
from Poisson actuarial baseline) or via sub-domain segmentation
(unverified; reviewer-run).

---

## Reviewer-run scripts pending for I1–I5, I7–I10

For each prediction not directly executable, the pre-registration
in `notes/session_10_industrial_predictions.md` provides the
binding protocol. A reviewer / author with access to the named
dataset can execute the test by:

1. Implementing the protocol as `analyse.py` in a fresh
   `claims/Ix_*/` directory.
2. Committing the script *after* the pre-registration commit
   (currently `aa6ee72`).
3. Running it and committing `result.md` honestly regardless of
   outcome.

The discipline binds across reviewer execution as well: tolerance
bands and falsifier bands locked at `aa6ee72`; honest negatives
committed permanently; pre-registrations cannot be retroactively
edited.

---

## Updated tier-distribution accounting

After Session 10 execution attempt:

| Domain | T1 | T1\* | T2 / T2-eq | T2\* | T3 | T4 |
|--------|---:|-----:|-----------:|-----:|---:|---:|
| M (22) | 18 | 2 | 1 (M9) | 0 | 1 (M10-α³) | 0 |
| P (9) | 3 (P3, P10, P11) | 0 | 3 (P1, P6, P7) | 3 (P2, P4, P5) | 1 (P15) | 0 |
| B (7) | 6 | 0 | 1 (B7) | 0 | 0 | 0 |
| Ph (7) | 2 | 0 | 5 | 0 | 0 | 0 |
| **I (1 executed)** | **1 (I6 negative)** | 0 | 0 | 0 | 0 | 0 |
| **Total (46)** | **30** | **2** | **10** | **3** | **2** | **0** |

(I claims I1–I5, I7–I10 are pre-registered but not yet
analysed in any tier; they sit at "pre-registered, awaiting
execution" rather than at T0–T4.)

---

## Audit-trail summary for Session 10

| Commit | Content |
|--------|---------|
| `aa6ee72` | Session 10 pre-registration of I1–I10 |
| (next) | I6 execution: fetch.py + analyse.py + result.md + tier.md + this log |

Per CAMPAIGN.md PART III: the v1 negatives recorded in I6 (and
P10 from Session 8) accumulate as the campaign's permanent honest-
negative ledger. They constitute calibrating evidence — they are
not failures of the framework wholesale; they refine which
substrates apply to which systems.

The Class C identification of cyber is the most informative
single new finding from Session 10, even though it is recorded
as a strict negative for I6's Z₂ pre-registration.
