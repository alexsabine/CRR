"""CSV and JSON loaders + writers for prediction tables."""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from typing import Any, Iterable

from .canonical import (
    PI,
    SQRT3,
    cv_canonical,
    omega_canonical,
    phi_g,
    verdict_from_ratio,
)
from ._paper_data import PAPER_ROWS, PaperRow


PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PACKAGE_ROOT / "data"

# canonical column order for both CSV and JSON-as-records form
FIELDS: list[str] = [
    "id", "system", "domain", "class", "symmetry", "n",
    "phi_G", "omega_geo", "cv_pred", "cv_obs", "ratio", "verdict",
    "physical_justification", "class_justification",
    "data_extraction", "reference", "notes", "provenance",
]


def _paper_phi_g(sym: str, n: int) -> float:
    """Paper convention for phi_G:
        Z2  -> π
        SO(2) -> 2π (paper uses n=4 via SO(2)≅Z4 equivalence)
        Z3  -> 2π/3 *under M15 reading*, but the paper's CV = 1/(3π)
               corresponds to phi_G = 3π/2 (no closed-form derivation).
    We use the paper's CV formula directly, not phi_G, by setting
    phi_G to whatever value reproduces the paper's CV exactly.
    """
    if sym == "Z2":
        return PI
    if sym == "SO(2)":
        return 2.0 * PI
    if sym == "Z3":
        # paper extrapolation: CV = 1/(nπ); so phi_G = nπ/2
        return n * PI / 2.0
    raise ValueError(f"unrecognised paper symmetry {sym!r}")


def _row_dict_from_paper(p: PaperRow) -> dict[str, Any]:
    sym = p["sym"]
    n = p["n"]
    phi = _paper_phi_g(sym, n)
    cv_pred = 1.0 / (2.0 * phi)
    cv_obs = p["cv_obs"]
    ratio = cv_obs / cv_pred if cv_pred > 0 else None
    return {
        "id": p["id"],
        "system": p["system"],
        "domain": p["domain"],
        "class": p["cls"],
        "symmetry": sym,
        "n": n,
        "phi_G": phi,
        "omega_geo": 1.0 / phi,
        "cv_pred": cv_pred,
        "cv_obs": cv_obs,
        "ratio": ratio,
        "verdict": p["verdict"],
        "physical_justification": p["physical_justification"],
        "class_justification": p["class_justification"],
        "data_extraction": p["data_extraction"],
        "reference": p["reference"],
        "notes": p["notes"],
        "provenance": "paper-appendix-A",
    }


def load_paper_table() -> list[dict[str, Any]]:
    """Materialise the 132-system paper table as a list of dict rows."""
    return [_row_dict_from_paper(p) for p in PAPER_ROWS]


def load_z2_on_so2() -> list[dict[str, Any]]:
    """Load the Z₂-on-SO(2) compositional extension predictions."""
    return _load_csv(DATA_DIR / "cv_predictions_z2_on_so2.csv")


def load_lie_group_extensions() -> list[dict[str, Any]]:
    """Load the Lie-group beyond-M22 extension predictions."""
    return _load_csv(DATA_DIR / "cv_predictions_lie_groups.csv")


def load_all_predictions() -> list[dict[str, Any]]:
    """Merge all three prediction files into a single list."""
    out: list[dict[str, Any]] = []
    out.extend(load_paper_table())
    out.extend(load_z2_on_so2())
    out.extend(load_lie_group_extensions())
    return out


def _load_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            for fld in ("n",):
                r[fld] = int(r[fld]) if r[fld] not in ("", "None", None) else None
            for fld in ("phi_G", "omega_geo", "cv_pred", "cv_obs", "ratio"):
                v = r[fld]
                r[fld] = float(v) if v not in ("", "None", None) else None
            rows.append(r)
    return rows


def write_csv(rows: Iterable[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            row = {k: ("" if r.get(k) is None else r[k]) for k in FIELDS}
            writer.writerow(row)


def write_json(rows: Iterable[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    serialised = []
    for r in rows:
        cleaned = {}
        for k in FIELDS:
            v = r.get(k)
            if isinstance(v, float) and math.isnan(v):
                v = None
            cleaned[k] = v
        serialised.append(cleaned)
    with path.open("w") as f:
        json.dump(serialised, f, indent=2)


def regenerate_paper_files() -> tuple[Path, Path]:
    """Write the canonical 132-system CSV+JSON from the Python source of truth."""
    rows = load_paper_table()
    csv_path = DATA_DIR / "cv_predictions_132.csv"
    json_path = DATA_DIR / "cv_predictions_132.json"
    write_csv(rows, csv_path)
    write_json(rows, json_path)
    return csv_path, json_path
