# Session 4 — Pre-registered novel predictions

This document is committed **before any analysis script exists** to
serve as the campaign's audit trail per `CAMPAIGN.md` PART III
pre-registration discipline:

> Every empirical claim assessed for T3 promotion must follow the
> pre-registration pattern: prediction.md committed before fetch.py
> or analyse.py exist. The git log is the audit trail.

## Predictions catalogued in this session (9)

Each pre-registration commits to:
- The exact CRR claim being tested.
- The data target (specific public dataset, version, time window).
- The quantitative prediction with band.
- The explicit falsifier (what result downgrades the claim).
- The T3 promotion criterion.
- Applied usefulness for 2026 and beyond.

### Mathematical / physical (5)

| ID | Pre-registration | Claim under test | Data target |
|----|------------------|------------------|-------------|
| M22-A | SU(2) ≡ SO(2) CV equality | M22 (Lie-group CV) | NMR T₁ relaxation (BMRB) vs harmonic-oscillator literature |
| M22-B | SO(3) ≡ Z₂-only CV equality | M22 + M2 | Rigid-body precession data (gyroscope databases) vs bistable literature |
| M22-C | SU(3) CV ≈ 0.0459 | M22 | Color-confinement timescale CV from PDG hadronic-decay data |
| M10-α³ | Subatomic CV scales with α³ | M10 (extension) | NIST hydrogenic Lamb-shift dispersion |
| P1-stellar | Stellar chromospheric-cycle CV ≈ 1/(4π) | P1 generalisation | Mount Wilson + Kepler stellar-cycle catalogues |

### Geophysical / cosmological (2)

| ID | Pre-registration | Claim under test | Data target |
|----|------------------|------------------|-------------|
| P5-global | Global repeating earthquakes: single-Ω ≈ ETAS | P5 generalisation | GeoNet, NIED, CSN catalogues |
| P4-DESI-Y3 | w(z) crossing in [0.4, 0.6] persists | P4 confirmation | DESI Year-3 + Euclid Year-1 (post-2026) |

### Biological (2)

| ID | Pre-registration | Claim under test | Data target |
|----|------------------|------------------|-------------|
| B2-HRV | HRV B → A → C ordering across PhysioNet cohorts | B2 | MIT-BIH NSR / Fantasia / CHF / SDDB |
| M9-quasicrystal | Sturmian-Hamiltonian spectral-type test | M9 / B1 | Specific Fibonacci-substitution chains (numerical) |

## Pre-registration discipline (this session)

**Step 1 (this commit):** all `prediction.md` files committed; no
analysis or fetch scripts written yet. The git log shows
`prediction.md` exists before any `fetch_*.py` or `analyse_*.py`.

**Step 2 (subsequent commits):** analysis / fetch scripts added.
Each script header states the prediction.md commit hash it tests
against.

**Step 3 (future sessions):** when data fetch + analysis are run,
result.md is written. T3 is promoted if the prediction's threshold
is met; the claim is downgraded if it is not. **The result is
binding regardless of direction.**

## What is NOT in this session

- No analysis scripts (committed in Step 2 separately).
- No "result.md" files (require actual data execution; future
  session).
- No T3 promotions (require result.md confirmation).

## Sandbox limitation acknowledged

Most data sources for these predictions are blocked by the campaign
sandbox (BMRB, PDG, NIST, Mount Wilson, Kepler, DESI, GeoNet,
PhysioNet). Predictions are committed for unaffiliated reviewer
execution; the sandbox-runnable ones (M9 numerical, M10-α³ from
hardcoded CODATA constants) can be tested in-session.

## Applied-usefulness orientation

Each pre-registration ends with a 2026+ applied-usefulness
section. Themes recurring across predictions:

- **AI / ML:** AGI evaluation, LLM memory, brain-emulation
- **Healthcare:** wearable cardiac/neurological monitoring
- **Space science:** GW astronomy, cosmology, solar / stellar physics
- **Geophysics:** earthquake forecasting, climate-system variability
- **Quantum / subatomic:** precision metrology, fundamental constants

The *ensemble* of pre-registrations gives a multi-domain robustness
test: if CRR's CV = Ω/2 holds across all nine, the framework's
applied-usefulness footprint expands dramatically; if it fails on
even one of the *sharpest* falsifiers (M22-A SU(2) ≡ SO(2) is the
sharpest), the rupture-topology framing needs revision.
