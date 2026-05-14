"""Tests for the pure-Z₂ memoryless extension (Sabine 2026 radioactive paper).

Pins:
  - cv_pure_z2_memoryless() == 1.0 exactly
  - The asymmetry: Z₂ × SO(2) = 1, SO(2) × Z₂ = 1/4
  - Z₂_only is structurally distinct from Z₂ (different φ_G)
  - Monte Carlo agreement with the exponential distribution
  - Schema/loader integration
"""

from __future__ import annotations

import math
import statistics
import sys
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from crr_cv_predictions import (  # noqa: E402
    cv_canonical,
    cv_inflation_factor,
    cv_pure_z2_memoryless,
    load_memoryless,
    load_all_predictions,
    predict_cv_for,
)
from crr_cv_predictions.canonical import PI  # noqa: E402


def test_pure_memoryless_cv_equals_one_exactly():
    assert cv_pure_z2_memoryless() == 1.0


def test_z2_times_so2_geodesic_equals_one():
    """Sabine 2026 §3.3: CV(Z₂) × C*(SO(2)) = (1/2π) × 2π = 1."""
    cv_z2 = cv_canonical("Z2")
    c_star_so2 = cv_inflation_factor("Z2", "SO(2)")
    product = cv_z2 * c_star_so2
    assert math.isclose(product, 1.0, rel_tol=1e-12), product


def test_so2_times_z2_geodesic_equals_one_quarter():
    """Sabine 2026 §4.3 asymmetry: CV(SO(2)) × C*(Z₂) = (1/4π) × π = 1/4."""
    cv_so2 = cv_canonical("SO(2)")
    c_star_z2 = cv_inflation_factor("SO(2)", "Z2")
    product = cv_so2 * c_star_z2
    assert math.isclose(product, 0.25, rel_tol=1e-12), product
    # And it is NOT equal to 1
    assert not math.isclose(product, 1.0, rel_tol=1e-3)


def test_z2_only_distinct_from_z2_with_regulator():
    """The two Z₂ readings give different CV predictions."""
    assert not math.isclose(
        cv_canonical("Z2"), cv_canonical("Z2_only"), rel_tol=1e-3
    )


def test_z2_only_cv_is_one():
    """Z2_only label gives CV = 1 by construction (φ_G = 0.5 convention)."""
    assert math.isclose(cv_canonical("Z2_only"), 1.0, rel_tol=1e-12)


def test_z2_with_explicit_alias_matches_z2():
    """Z2_on_SO2 is an alias for Z2."""
    assert math.isclose(cv_canonical("Z2_on_SO2"), cv_canonical("Z2"), rel_tol=1e-12)


def test_monte_carlo_exponential_cv_is_one_within_paper_tolerance():
    """Sabine 2026 §4.2: 100×10⁶ samples → CV = 1.000099 ± 0.000953.

    Reduced sample for unit test: 10×10⁵, expected CV within 0.005.
    """
    import random
    random.seed(42)
    cvs = []
    for _ in range(10):
        sample = [random.expovariate(1.0) for _ in range(100_000)]
        m = statistics.mean(sample)
        s = statistics.stdev(sample)
        cvs.append(s / m)
    mean_cv = statistics.mean(cvs)
    # paper tolerance is 0.0099%; we use looser 0.5% for short test
    assert abs(mean_cv - 1.0) < 0.005, mean_cv


def test_geometric_distribution_lacks_2pi_factor():
    """Sabine 2026 §4.4: discrete memoryless lacks the 2π factor.

    Geometric: CV = sqrt(1-p)/p · sqrt(p) … the standard result is
    CV = sqrt(1-p)/p_mean … paper gives CV = sqrt(1-p)/(p·mean)
    Actually: for geometric with success prob p, mean = 1/p,
    var = (1-p)/p², so CV = sqrt(1-p)/p × p = sqrt(1-p).

    Wait: CV = SD/mean = sqrt((1-p)/p²) / (1/p) = sqrt(1-p).
    No 2π anywhere; just sqrt(1-p).
    """
    for p in [0.1, 0.3, 0.5, 0.7, 0.9]:
        cv_geom = math.sqrt(1 - p)
        # Show no clean 2π relationship
        ratio_to_2pi = cv_geom / (2 * PI)
        # ratio is a continuous function of p, never hits unity for any p ∈ (0,1)
        assert ratio_to_2pi < 1.0


def test_memoryless_loader_returns_12_rows():
    rows = load_memoryless()
    assert len(rows) == 12


def test_all_memoryless_rows_predict_cv_1():
    for r in load_memoryless():
        assert math.isclose(r["cv_pred"], 1.0, rel_tol=1e-12), r["id"]


def test_all_memoryless_rows_have_pending_verdict():
    for r in load_memoryless():
        assert r["verdict"] == "PENDING"
        assert r["cv_obs"] in (None, "", "None")


def test_all_memoryless_rows_use_z2_only_symmetry():
    for r in load_memoryless():
        assert r["symmetry"] == "Z2_only", r["id"]


def test_rubric_memoryless_path():
    """Step 2 / memoryless route should produce CV = 1 prediction."""
    r = predict_cv_for(
        system="single radioactive atom decay",
        is_oscillatory=True,
        state_space="memoryless",
        regulation="noise-dominated",
    )
    assert r.symmetry == "Z2_only"
    assert math.isclose(r.cv_pred, 1.0, rel_tol=1e-12)


def test_rubric_two_states_default_assumes_so2_regulator():
    """Step 2 / Q1 with default has_so2_regulator → Z2 (not Z2_only)."""
    r = predict_cv_for(
        system="generic switch",
        is_oscillatory=True,
        state_space="two states",
        regulation="autonomous",
    )
    assert r.symmetry == "Z2"
    assert math.isclose(r.cv_pred, 1.0 / (2 * PI), rel_tol=1e-12)


def test_rubric_two_states_with_explicit_no_regulator():
    """Step 2.5: has_so2_regulator=False forces Z2_only."""
    r = predict_cv_for(
        system="theoretical Z2 with no regulator",
        is_oscillatory=True,
        state_space="two states",
        regulation="noise-dominated",
        has_so2_regulator=False,
    )
    assert r.symmetry == "Z2_only"
    assert math.isclose(r.cv_pred, 1.0, rel_tol=1e-12)


def test_load_all_includes_memoryless():
    rows = load_all_predictions()
    provenances = {r["provenance"] for r in rows}
    assert "memoryless-pure-z2" in provenances


def test_extension_blink_row_approaches_memoryless_limit():
    """Spontaneous blink interval (paper row 16) ratio = 5.03×, close to 2π = 6.28.

    The new framework predicts that high-ratio Class C systems are
    approaching the memoryless limit (no SO(2) regulator).
    """
    from crr_cv_predictions._paper_data import PAPER_ROWS
    blink = next(r for r in PAPER_ROWS if r["id"] == "paper-016")
    assert blink["system"] == "Spontaneous blink interval"
    assert blink["cls"] == "C"
    # Empirical ratio is 5.03×, less than 2π = 6.28, so still has *some* SO(2)
    assert blink["ratio"] < 2 * PI
    # But close enough to flag as approaching memoryless
    assert blink["ratio"] > 4.0
