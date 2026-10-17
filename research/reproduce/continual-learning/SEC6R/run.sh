#!/usr/bin/env bash
# SEC6R (Ashes): Part B held-out, 12 OpenML ids (gate CLOSED; SEC6R-1 PASS-0 UNINFORMATIVE recorded). Part A (seen data) is in expected/partA/.
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=sec6r
SCORER=runs/sec6r/frozen/sec6r_score.py
FETCH=openml
PART="--part B"
IDS="183 279 1534 1538 1542 1552 40985 46608 46684 46709 46745 46761"
QUICK=1552
TIMES=1
. "$HERE/../../_shared/ashes_study.sh"
