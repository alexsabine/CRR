"""Tests for the Appendix C pre-registration rubric (src/crr_cv_predictions/rubric.py).

This module had no test coverage before; added alongside the fix for the
SO(2)/Z_n n-index bug (see test_no_zn_index_on_continuous_phase_rows in
test_paper_table_integrity.py for the data-file-level regression guard).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from crr_cv_predictions.rubric import classify, evaluate, predict_cv_for  # noqa: E402


def test_continuous_cycle_gets_no_zn_index():
    """SO(2) systems must not carry a discrete-phase n (see rupture_topology.md H2)."""
    r = classify("test rotational oscillator", True, "continuous cycle")
    assert r.symmetry == "SO(2)"
    assert r.n is None


def test_two_states_gets_n_2():
    r = classify("test bistable switch", True, "two states")
    assert r.symmetry == "Z2"
    assert r.n == 2


def test_lie_group_route_only_z2_gets_index():
    r_so2 = classify("test", True, "SO(2)")
    assert r_so2.n is None
    r_su2 = classify("test", True, "SU(2)")
    assert r_su2.n is None
    r_z2 = classify("test", True, "Z2")
    assert r_z2.n == 2


def test_cv_pred_values_match_canonical_constants():
    r_z2 = classify("test", True, "two states")
    assert math.isclose(r_z2.cv_pred, 1.0 / (2 * math.pi), rel_tol=1e-9)
    r_so2 = classify("test", True, "continuous cycle")
    assert math.isclose(r_so2.cv_pred, 1.0 / (4 * math.pi), rel_tol=1e-9)


def test_reversal_flag_on_class_b_elevated():
    r = classify("test", True, "continuous cycle", regulation="regulated")
    evaluate(r, cv_obs=0.5)  # far above prediction -> ELEVATED, class B -> reversal
    assert r.verdict == "ELEVATED"
    assert r.reversal_flag is True


def test_no_reversal_on_class_a_match():
    r = predict_cv_for("test", True, "continuous cycle", regulation="autonomous",
                        cv_obs=1.0 / (4 * math.pi))
    assert r.verdict == "MATCH"
    assert r.reversal_flag is False


def test_non_oscillatory_raises():
    import pytest
    with pytest.raises(ValueError):
        classify("not oscillatory", False, "two states")
