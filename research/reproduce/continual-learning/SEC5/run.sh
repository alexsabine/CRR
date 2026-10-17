#!/usr/bin/env bash
# SEC5 (Ashes): replication of SEC4-1 on 12 OpenML ids (FAIL recorded).
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=sec5
SCORER=runs/sec5/frozen/sec5_score.py
FETCH=openml
IDS="57 155 1503 1509 1529 1530 1532 1541 1549 41671 41972 41982"
QUICK=1549
TIMES=1
. "$HERE/../../_shared/ashes_study.sh"
