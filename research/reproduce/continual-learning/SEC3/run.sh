#!/usr/bin/env bash
# SEC3 (Ashes): replication of SCL3 on 7 OpenML AutoML-benchmark carriers (FAIL recorded).
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=sec3
SCORER=runs/sec3/frozen/sec3_score.py
FETCH=openml
IDS="1596 41167 41164 41169 41168 40685 41166"
QUICK=41168
TIMES=1
. "$HERE/../../_shared/ashes_study.sh"
