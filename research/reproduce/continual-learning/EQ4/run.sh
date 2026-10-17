#!/usr/bin/env bash
# EQ4 (Ashes): the bounded equanimity rule on 6 PMLB carriers (FAIL 4/6 recorded).
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=eq4
SCORER=runs/eq4/frozen/eq4_score.py
FETCH=pmlb
NOCHECK=1
IDS="satimage segmentation yeast wine_quality_white sleep page_blocks"
QUICKRUN="page_blocks ewc eqb 1.0 0"
QUICKREF=rerun_page_blocks_a.json
. "$HERE/../../_shared/ashes_study.sh"
