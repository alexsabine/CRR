"""Regenerate the CSV+JSON data files from the Python sources of truth.

Run from the package root:

    python -m scripts.build_data
or
    python scripts/build_data.py
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
sys.path.insert(0, str(PKG_ROOT / "src"))

from crr_cv_predictions._extensions import (  # noqa: E402
    get_lie_group_rows,
    get_z2_on_so2_rows,
)
from crr_cv_predictions._memoryless import get_memoryless_rows  # noqa: E402
from crr_cv_predictions.loader import (  # noqa: E402
    DATA_DIR,
    load_paper_table,
    write_csv,
    write_json,
)


def main() -> None:
    paper = load_paper_table()
    write_csv(paper, DATA_DIR / "cv_predictions_132.csv")
    write_json(paper, DATA_DIR / "cv_predictions_132.json")

    z2so2 = get_z2_on_so2_rows()
    write_csv(z2so2, DATA_DIR / "cv_predictions_z2_on_so2.csv")
    write_json(z2so2, DATA_DIR / "cv_predictions_z2_on_so2.json")

    lie = get_lie_group_rows()
    write_csv(lie, DATA_DIR / "cv_predictions_lie_groups.csv")
    write_json(lie, DATA_DIR / "cv_predictions_lie_groups.json")

    memoryless = get_memoryless_rows()
    write_csv(memoryless, DATA_DIR / "cv_predictions_memoryless.csv")
    write_json(memoryless, DATA_DIR / "cv_predictions_memoryless.json")

    print(f"wrote {len(paper)} paper rows")
    print(f"wrote {len(z2so2)} Z₂-on-SO(2) extension rows")
    print(f"wrote {len(lie)} Lie-group extension rows")
    print(f"wrote {len(memoryless)} memoryless (pure-Z₂) extension rows")


if __name__ == "__main__":
    main()
