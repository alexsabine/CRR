#!/usr/bin/env bash
# SEC4 (Ashes): third carrier family, 9 OpenML ids (SEC4-1 PASS-1 recorded).
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=sec4
SCORER=runs/sec4/frozen/sec4_score.py
FETCH=openml
IDS="46906 1459 1466 23380 1476 375 46980 1491 377"
QUICK=377
TIMES=1
. "$HERE/../../_shared/ashes_study.sh"
