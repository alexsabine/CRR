# PACKAGE_OVERVIEW.md — what's inside, mapped to your request

You asked for a clean software package that breaks the CRR CV
predictions into pieces, with each aspect broken down, the full
table of predictions, clear rationale per prediction, what data
was used, and how it was utilised. Here's the map.

## Each aspect, broken down

| Aspect from your request | Where it lives | What it contains |
|---|---|---|
| **The rubric for making the claims** | `RUBRIC.md` (distilled), `src/crr_cv_predictions/rubric.py` (runnable) | Appendix C 6-step protocol, both as prose and as a function `predict_cv_for(...)`. |
| **Full table of CV predictions (132)** | `data/cv_predictions_132.csv`, `…json` | Verbatim Appendix A; reproduces paper's 53/34/45 verdict tally and 114/132 three-class correct. |
| **Clear rationale per system** | Same CSV/JSON, columns `physical_justification` and `class_justification` | One row per system, 1–2 sentences for symmetry-class rationale and for A/B/C rationale. |
| **What data was used** | Same CSV/JSON, columns `reference` and `data_extraction` | First-author year journal vol:page (DOI when available); explicit notes when the paper text gives mean ± SD. |
| **How that data was utilised** | Same CSV/JSON, columns `cv_obs`, `ratio`, `verdict` | Empirical CV from the source, the recomputed ratio against the canonical prediction, and the rubric's verdict. |
| **Other CV values predicted by Z₂-on-SO(2)** | `docs/z2_on_so2_compositional.md` + `data/cv_predictions_z2_on_so2.csv` | 14 pre-registered new predictions: ρ = −1/2 cardio-resp anti-correlation, nested sub-rupture jitter, k-channel ρ = −1/(k−1), Z₂-on-larger-G corollaries. |
| **Predictions from Z₂ ruptures on any Lie group** | `docs/lie_group_extensions.md` + `data/cv_predictions_lie_groups.csv` | M22 generalisation extended to SO(4), U(2), SU(4), Sp(2), G₂, Spin(7), T³, T⁴, golden-ratio PHI; each with a candidate empirical system and source. |
| **Specific systems each prediction suits** | Same CSV/JSON files, `system` and `domain` columns | NV-centre Rabi, NMR T₂ jitter, Earth LOD jitter, hydrogen orbital lifetime, transmon-cavity, charmonium, pentaquark, double pendulum, cardio-resp-circadian, etc. |

## The five files you'll most often reach for

1. `data/cv_predictions_132.csv` — the source of truth for the
   paper table.
2. `data/cv_predictions_z2_on_so2.csv` — the new compositional
   pre-registered predictions.
3. `data/cv_predictions_lie_groups.csv` — the new Lie-group
   pre-registered predictions.
4. `RUBRIC.md` — the 6-step protocol you must apply before
   adding a row.
5. `tests/test_paper_table_integrity.py` — the safety net that
   pins the paper's headline numbers.

## Tested invariants (run `pytest tests/`)

- 132 rows; 53 MATCH, 34 SUPPRESSED, 45 ELEVATED (paper Section 6).
- Class A 45, B 40, C 47.
- Three-class correct: 114/132 = 86%.
- Zero directional reversals (paper's strongest claim).
- CV(Z₂)/CV(SO(2)) = 2 exactly.
- M22 topological CV-equivalences hold:
  CV(SU(2)) = CV(SO(2)),  CV(SO(3)) = CV(Z₂),
  CV(SO(4)) = CV(SO(3)),  CV(SU(4)) = CV(Sp(2)),
  CV(SU(3)) = CV(Spin(7)).
- All extension rows have `verdict = PENDING` and `cv_obs = null`
  (pre-registration discipline).

## How to add a new prediction

```python
from crr_cv_predictions import predict_cv_for

# Apply the rubric
result = predict_cv_for(
    system="my new bistable oscillator",
    is_oscillatory=True,
    state_space="two states",        # → Z₂
    regulation="autonomous",          # → Class A
)

# To turn into a row for the extension CSVs
row = result.to_row(
    domain="cellular",
    physical="State A / state B switching, no continuous-phase content.",
    klsjust="Autonomous, no external regulation; Class A.",
    reference="Author 2026 Journal vol:page",
    provenance="z2-on-so2-extension",
)
```

After that, append the row to the appropriate CSV/JSON, update
the count tests in `tests/test_paper_table_integrity.py`, and
re-run `python scripts/build_data.py` if regenerating from a
Python source.

## Discrepancies and open questions recorded

The package documents (rather than papers over) two known issues:

1. **Z_n formula discrepancy.** Paper extrapolation 1/(nπ) vs M15
   discrete-phase derivation n/(4π) disagree for n ≥ 3.
   Both are exposed: `cv_zn_paper(n)` and `cv_zn_discrete_phase(n)`.
   The repressilator row `lie-z3-trefoil-repressilator-paper`
   carries a `notes` field that flags this.
2. **G₂ normalisation ambiguity.** Killing-form normalisation
   vs Lie-algebra-orbit-length normalisation give CV in
   [0.069, 0.097]. The G₂ extension row records the wider value.
3. **Open derivations from paper Section 8.** Listed in
   `docs/derivation_chain.md`: constant-speed geodesic
   traversal, circular Landauer barrier, A4 (Kac return-time
   identification), independent third-batch classification.

## What this package does *not* claim

- It does not fit any parameter. Every `cv_pred` is computed
  from canonical formulas in `canonical.py`.
- It does not adjudicate the open theoretical questions; it
  records them.
- It does not include re-runs of the paper's Monte Carlo nulls.
  Those live in `crr-engine/consistency/significance_memory.py`.
- It does not replace the existing claim-by-claim notebooks in
  `claims/`. It is a *predictions catalogue* that points at
  those derivations.
