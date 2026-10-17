#!/usr/bin/env bash
# EQ3 (Ashes): the equanimity rule on 6 PMLB carriers (FAIL recorded).
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=eq3
SCORER=runs/eq3/frozen/eq3_score.py
FETCH=pmlb
NOCHECK=1
IDS="fars krkopt led24 led7 mfeat_factors mfeat_morphological"
QUICKRUN="led7 ewc eq 1.0 0"
QUICKREF=rerun_led7_a.json
. "$HERE/../../_shared/ashes_study.sh"
