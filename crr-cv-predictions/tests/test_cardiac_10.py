"""Pre-registration discipline tests for the 10-prediction cardiac batch."""

from __future__ import annotations

import math
import sys
from collections import Counter
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from crr_cv_predictions import (  # noqa: E402
    cv_canonical,
    load_cardiac_10,
    load_paper_table,
    load_z2_on_so2,
)
from crr_cv_predictions.canonical import PI  # noqa: E402


def test_cardiac_10_has_10_rows():
    rows = load_cardiac_10()
    assert len(rows) == 10


def test_cardiac_10_all_pending():
    """Pre-registration discipline: all rows must be PENDING with no cv_obs."""
    for r in load_cardiac_10():
        assert r["verdict"] == "PENDING", r["id"]
        assert r["cv_obs"] in (None, "", "None"), r["id"]


def test_cardiac_10_all_cardiac_domain():
    for r in load_cardiac_10():
        assert r["domain"] == "cardiac", r["id"]


def test_cardiac_10_class_balance():
    """The set is designed to span every CV regime in the framework."""
    rows = load_cardiac_10()
    cls = Counter(r["class"] for r in rows)
    # Class A: autonomous (3 sub-rupture jitter rows)
    # Class B: regulated/precision (2 rows)
    # Class C: pathological/elevated (5 rows incl. 2 memoryless candidates)
    assert cls["A"] == 3
    assert cls["B"] == 2
    assert cls["C"] == 5


def test_cardiac_10_symmetry_coverage():
    """Set must include all three Z₂ readings + SO(2)."""
    rows = load_cardiac_10()
    syms = {r["symmetry"] for r in rows}
    assert "Z2" in syms          # Z₂-on-SO(2) sub-rupture and PVCs
    assert "Z2_only" in syms     # AF and VF candidates
    assert "SO(2)" in syms       # PP, paced, athlete, LQT, TdP


def test_cardiac_10_no_id_clash_with_existing():
    existing_ids = {r["id"] for r in load_paper_table() + load_z2_on_so2()}
    new_ids = {r["id"] for r in load_cardiac_10()}
    assert not (existing_ids & new_ids), existing_ids & new_ids


def test_cardiac_10_no_system_clash_with_existing():
    """Cardiac systems in the new batch are conceptually distinct from
    existing cardiac entries."""
    existing_systems = {
        r["system"].lower()
        for r in load_paper_table() + load_z2_on_so2()
        if r["domain"] == "cardiac"
    }
    for r in load_cardiac_10():
        assert r["system"].lower() not in existing_systems, r["system"]


def test_cardiac_10_provenance_label():
    for r in load_cardiac_10():
        assert r["provenance"] == "cardiac-10-batch", r["id"]


def test_cardiac_10_cv_pred_matches_canonical():
    """Every row's cv_pred equals 1/(2·φ_G) for its symmetry."""
    for r in load_cardiac_10():
        sym = r["symmetry"]
        assert math.isclose(r["cv_pred"], cv_canonical(sym), rel_tol=1e-12), r["id"]


def test_cardiac_10_z2_only_rows_predict_cv_1():
    """The two Z₂_only rows predict CV = 1 exactly (memoryless limit)."""
    z2_only_rows = [r for r in load_cardiac_10() if r["symmetry"] == "Z2_only"]
    assert len(z2_only_rows) == 2
    for r in z2_only_rows:
        assert math.isclose(r["cv_pred"], 1.0, rel_tol=1e-12), r["id"]


def test_cardiac_10_so2_rows_predict_canonical_so2_cv():
    """SO(2) rows predict CV = 1/(4π) ≈ 0.0796."""
    so2_rows = [r for r in load_cardiac_10() if r["symmetry"] == "SO(2)"]
    expected = 1.0 / (4 * PI)
    for r in so2_rows:
        assert math.isclose(r["cv_pred"], expected, rel_tol=1e-12), r["id"]


def test_cardiac_10_z2_with_regulator_rows_predict_canonical_z2_cv():
    """Z₂ rows (with implicit SO(2) regulator) predict CV = 1/(2π) ≈ 0.1592."""
    z2_rows = [r for r in load_cardiac_10() if r["symmetry"] == "Z2"]
    expected = 1.0 / (2 * PI)
    for r in z2_rows:
        assert math.isclose(r["cv_pred"], expected, rel_tol=1e-12), r["id"]


def test_cardiac_10_each_row_has_reference():
    """Pre-registration requires a citable empirical anchor per row."""
    for r in load_cardiac_10():
        assert r["reference"], r["id"]
        # at minimum: author + year
        assert any(c.isdigit() for c in r["reference"]), f"no year in {r['id']}"


def test_cardiac_10_each_row_records_expected_direction():
    """Notes field must record the Class-derived expected verdict
    (for the Step 6 directional-reversal check on later evaluation)."""
    for r in load_cardiac_10():
        notes = r["notes"] or ""
        assert "Pre-registered direction:" in notes, r["id"]
        # Must name one of the three directions
        assert any(
            d in notes for d in ("MATCH", "SUPPRESSED", "ELEVATED")
        ), r["id"]


def test_cardiac_10_class_to_direction_consistency():
    """Class A → expected MATCH; B → SUPPRESSED; C → ELEVATED or MATCH (if memoryless)."""
    for r in load_cardiac_10():
        notes = r["notes"] or ""
        if r["class"] == "A":
            assert "Pre-registered direction: MATCH" in notes, r["id"]
        elif r["class"] == "B":
            assert "Pre-registered direction: SUPPRESSED" in notes, r["id"]
        elif r["class"] == "C":
            # Class C with Z2 substrate → ELEVATED expected
            # Class C with Z2_only substrate → MATCH expected (CV = 1 IS the prediction)
            if r["symmetry"] == "Z2_only":
                assert "Pre-registered direction: MATCH" in notes, r["id"]
            else:
                assert "Pre-registered direction: ELEVATED" in notes, r["id"]
