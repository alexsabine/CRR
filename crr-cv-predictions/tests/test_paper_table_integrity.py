"""Integrity tests for the 132-system paper table.

Reproduce paper-reported counts:
  - 132 rows total
  - 53 MATCH, 34 SUPPRESSED, 45 ELEVATED   (paper Section 6 / Appendix A summary)
  - Three-class: A 40/45 (89%), B 34/40 (85%), C 40/47 (85%) → 114/132 = 86%
  - Zero directional reversals
"""

from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from crr_cv_predictions import (  # noqa: E402
    cv_canonical,
    load_paper_table,
    load_z2_on_so2,
    load_lie_group_extensions,
    load_all_predictions,
)
from crr_cv_predictions.canonical import (  # noqa: E402
    PI,
    cv_zn_paper,
)


PI = math.pi


def test_paper_has_132_rows():
    rows = load_paper_table()
    assert len(rows) == 132


def test_paper_verdict_tally_matches_paper_summary():
    rows = load_paper_table()
    tally = Counter(r["verdict"] for r in rows)
    # Paper summary line: "53/132 match, 34/132 suppressed, 45/132 elevated".
    assert tally["MATCH"] == 53, f"expected 53 MATCH, got {tally['MATCH']}"
    assert tally["SUPPRESSED"] == 34, f"expected 34 SUPPRESSED, got {tally['SUPPRESSED']}"
    assert tally["ELEVATED"] == 45, f"expected 45 ELEVATED, got {tally['ELEVATED']}"


def test_paper_three_class_correct_count_is_114():
    """Paper: A 40/45 + B 34/40 + C 40/47 = 114/132 correct three-class."""
    rows = load_paper_table()
    correct = 0
    for r in rows:
        cls = r["class"]
        v = r["verdict"]
        if cls == "A" and v == "MATCH":
            correct += 1
        elif cls == "B" and v == "SUPPRESSED":
            correct += 1
        elif cls == "C" and v == "ELEVATED":
            correct += 1
    assert correct == 114, f"expected 114, got {correct}"


def test_paper_class_totals_match():
    rows = load_paper_table()
    cls_counts = Counter(r["class"] for r in rows)
    assert cls_counts["A"] == 45, f"Class A: expected 45, got {cls_counts['A']}"
    assert cls_counts["B"] == 40, f"Class B: expected 40, got {cls_counts['B']}"
    assert cls_counts["C"] == 47, f"Class C: expected 47, got {cls_counts['C']}"


def test_paper_zero_directional_reversals():
    rows = load_paper_table()
    reversals = 0
    for r in rows:
        if r["class"] == "B" and r["verdict"] == "ELEVATED":
            reversals += 1
        if r["class"] == "C" and r["verdict"] == "SUPPRESSED":
            reversals += 1
    assert reversals == 0, f"expected 0 directional reversals, got {reversals}"


def test_paper_cv_pred_matches_canonical_formula():
    """For Z₂ and SO(2) every paper row's cv_pred must equal the canonical CV."""
    rows = load_paper_table()
    for r in rows:
        sym = r["symmetry"]
        cv_pred = r["cv_pred"]
        if sym == "Z2":
            assert math.isclose(cv_pred, 1.0 / (2 * PI), rel_tol=1e-9)
        elif sym == "SO(2)":
            assert math.isclose(cv_pred, 1.0 / (4 * PI), rel_tol=1e-9)
        elif sym == "Z3":
            # paper extrapolation
            assert math.isclose(cv_pred, cv_zn_paper(3), rel_tol=1e-9)


def test_ratio_recomputes_within_two_percent_of_paper_value():
    """Paper's printed ratios are 2-decimal-place rounded; our ratios are exact."""
    rows = load_paper_table()
    for r in rows:
        cv_obs = r["cv_obs"]
        cv_pred = r["cv_pred"]
        ratio = r["ratio"]
        if cv_pred > 0:
            assert math.isclose(ratio, cv_obs / cv_pred, rel_tol=1e-12), r["id"]


def test_no_unknown_verdicts():
    rows = load_paper_table()
    assert all(r["verdict"] in {"MATCH", "SUPPRESSED", "ELEVATED"} for r in rows)


def test_no_unknown_classes():
    rows = load_paper_table()
    assert all(r["class"] in {"A", "B", "C"} for r in rows)


def test_each_id_is_unique():
    rows = load_all_predictions()
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), f"duplicate ids: {[i for i in ids if ids.count(i) > 1]}"


def test_extensions_have_pending_verdict():
    """Pre-registration discipline: cv_obs is null and verdict is PENDING for all extensions."""
    for r in load_z2_on_so2() + load_lie_group_extensions():
        assert r["cv_obs"] in (None, "", "None"), f"{r['id']}: cv_obs leaked: {r['cv_obs']!r}"
        assert r["verdict"] == "PENDING", f"{r['id']}: verdict {r['verdict']!r} not PENDING"


def test_z2_on_so2_count_matches_doc():
    """docs/z2_on_so2_compositional.md says 14 pre-registered predictions."""
    rows = load_z2_on_so2()
    assert len(rows) == 14, f"expected 14 Z₂-on-SO(2) extension rows, got {len(rows)}"


def test_lie_group_count_matches_doc():
    """docs/lie_group_extensions.md says 14 pre-registered predictions."""
    rows = load_lie_group_extensions()
    assert len(rows) == 14, f"expected 14 Lie-group extension rows, got {len(rows)}"


def test_topological_z2_so2_ratio_is_two():
    """Paper Section 1.7: CV(Z₂)/CV(SO(2)) = 2 exactly."""
    assert math.isclose(cv_canonical("Z2") / cv_canonical("SO(2)"), 2.0, rel_tol=1e-12)


def test_su2_so2_cv_equality():
    """M22-A topological prediction: CV(SU(2)) = CV(SO(2))."""
    assert math.isclose(cv_canonical("SU(2)"), cv_canonical("SO(2)"), rel_tol=1e-12)


def test_so3_z2_cv_equality():
    """M22-B topological prediction: CV(SO(3)) = CV(Z₂)."""
    assert math.isclose(cv_canonical("SO(3)"), cv_canonical("Z2"), rel_tol=1e-12)


def test_so4_so3_cv_equality():
    """Package extension: CV(SO(4)) = CV(SO(3)) = CV(Z₂) (φ_G = π)."""
    assert math.isclose(cv_canonical("SO(4)"), cv_canonical("SO(3)"), rel_tol=1e-12)


def test_su4_sp2_cv_equality():
    """Package extension: CV(SU(4)) = CV(Sp(2)) (φ_G = 4π)."""
    assert math.isclose(cv_canonical("SU(4)"), cv_canonical("Sp(2)"), rel_tol=1e-12)


def test_su3_spin7_cv_equality():
    """Package extension: CV(SU(3)) = CV(Spin(7)) (φ_G = 2π√3)."""
    assert math.isclose(cv_canonical("SU(3)"), cv_canonical("Spin(7)"), rel_tol=1e-12)
