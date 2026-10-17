#!/usr/bin/env bash
# SCL3 (Ashes): one SEC run against a tuned 17-point sweep, 10 OpenML-CC18 carriers.
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=scl3
SCORER=runs/scl3/frozen/scl3_score.py
FETCH=openml
IDS="1468 188 1475 4538 1478 300 40966 1501 40982 1497"
QUICK=1497
. "$HERE/../../_shared/ashes_study.sh"
