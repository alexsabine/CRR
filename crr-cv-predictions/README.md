# crr-cv-predictions

A self-contained, machine-readable package of CRR (Coherence–Rupture–
Regeneration) coefficient-of-variation predictions, organised so that
every claim can be traced from canonical formula → predicted value →
candidate system → empirical reference.

The package is a structured restatement of the predictions in Sabine,
*CRR: A Temporal Grammar — Three-Class Validation Across 132 Systems
in 20 Domains* (March 2026), extended with two pre-registered
prediction families that were implicit in the paper's framework but
not enumerated:

1. **Z₂-on-SO(2) compositional predictions.** Given the framework's
   convention C1 (rupture is Z₂ by construction) and C2 (the phase
   manifold is a compact connected Lie group), a single SO(2) cycle
   may be decomposed into one or more Z₂ rupture channels. This gives
   sub-cycle CV predictions, two-channel anti-correlation predictions
   (M11 ρ = −1/2), and nested-rupture jitter predictions.

2. **Lie-group CV predictions beyond M22.** The M22 generalisation
   CV_G = 1/(2·φ_G) was already stated for SU(2), SO(3), T², SU(3).
   This package adds compact-connected entries for SO(4), U(N), Sp(2),
   G₂, and the higher tori, each with a candidate empirical system and
   a data source for testing.

## Layout

```
crr-cv-predictions/
├── README.md                         # this file
├── RUBRIC.md                         # 6-step pre-registration protocol (Appendix C)
├── docs/
│   ├── framework_summary.md          # 1-page CRR framework recap
│   ├── derivation_chain.md           # Ω, φ_G, CV = Ω/2 derivation chain
│   ├── z2_on_so2_compositional.md    # rationale for the Z₂-on-SO(2) extensions
│   └── lie_group_extensions.md       # rationale for the beyond-M22 extensions
├── data/
│   ├── schema.json                   # JSON-Schema for prediction rows
│   ├── cv_predictions_132.csv        # paper's 132-system table (Appendix A)
│   ├── cv_predictions_132.json       # same, JSON
│   ├── cv_predictions_z2_on_so2.csv  # new compositional predictions
│   ├── cv_predictions_z2_on_so2.json
│   ├── cv_predictions_lie_groups.csv # new Lie-group extensions
│   └── cv_predictions_lie_groups.json
├── src/crr_cv_predictions/
│   ├── __init__.py
│   ├── canonical.py                  # CV = 1/(2·φ_G), φ_G table
│   ├── rubric.py                     # Appendix C 6-step algorithm in code
│   └── loader.py                     # CSV ↔ JSON loaders
└── tests/
    ├── test_canonical_values.py      # Z₂ ratio, SU(2)≡SO(2), SO(3)≡Z₂
    ├── test_paper_table_integrity.py # row count, verdict tally, ratio match
    └── test_rubric_reproduces_paper.py
```

## Schema (one row = one prediction)

Every row in every CSV/JSON file conforms to `data/schema.json`.
Fields:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | stable identifier (e.g. `paper-001`, `z2so2-cardio-resp`, `lie-su4-photonic`) |
| `system` | string | physical system being predicted |
| `domain` | string | one of 20 domains (cardiac, neural, cellular, …) |
| `class` | enum {A, B, C} | three-class assignment per Appendix C step 4 |
| `symmetry` | string | rupture/phase symmetry (`Z2`, `SO(2)`, `Z3`, `SU(2)`, `SO(3)`, `T2`, `SU(3)`, `SO(4)`, …) |
| `n` | integer or null | discrete-phase index where applicable |
| `phi_G` | float | bi-invariant geodesic length of the phase manifold |
| `omega_geo` | float | 1/φ_G |
| `cv_pred` | float | 1/(2·φ_G) — the CRR canonical prediction |
| `cv_obs` | float or null | empirical CV from cited source (null = pending) |
| `ratio` | float or null | cv_obs / cv_pred |
| `verdict` | enum {MATCH, SUPPRESSED, ELEVATED, PENDING} | per Appendix C step 5 |
| `physical_justification` | string | 1–2 sentence rationale for the symmetry class (Appendix C step 3) |
| `class_justification` | string | 1–2 sentence rationale for A/B/C (Appendix C step 4) |
| `data_extraction` | string | how cv_obs was derived from the source (e.g. "SD/mean of 24 cycle lengths") |
| `reference` | string | first-author year journal vol:page or DOI |
| `notes` | string | special features (asymmetric sub-cycles, regulation mechanism, etc.) |
| `provenance` | enum {paper-appendix-A, z2-on-so2-extension, lie-group-extension} | source of the prediction |

The two extension files share the schema but have `provenance` set to
`z2-on-so2-extension` or `lie-group-extension` and `cv_obs` typically
`null` (pre-registered, awaiting test).

## How to use

```python
from crr_cv_predictions import load_all_predictions, predict_cv_for

# load merged dataframe of all three CSVs
rows = load_all_predictions()

# apply the 6-step rubric to a new system
prediction = predict_cv_for(
    system="some new bistable oscillator",
    is_oscillatory=True,
    state_space="two distinguishable states",
    regulation="autonomous",  # → Class A
)
# returns dict with symmetry='Z2', n=2, cv_pred≈0.1592, class='A',
# acceptance_band=[0.0955, 0.2070], rubric_trace=[...]
```

## Provenance and pre-registration discipline

- The 132-system table (`cv_predictions_132.csv`) is a verbatim
  transcription of Appendix A of the paper. No CV values were
  recomputed. Verdicts and ratios match the paper's Section 6 totals
  (53 MATCH, 34 SUPPRESSED, 45 ELEVATED — overall 114/132 = 86%
  three-class correct with zero directional reversals).
- The Z₂-on-SO(2) and Lie-group extension files contain
  **pre-registered** predictions: `cv_pred` is filled before any
  attempt to look up `cv_obs`. The `verdict` column is `PENDING` for
  rows where empirical data has not yet been retrieved by an
  independent process.
- The `id` field is stable; re-running this package should produce
  identical predictions for identical inputs.
