#!/usr/bin/env bash
# EQ2 (Ashes): the equanimity rule (Omega = 1) against a tuned EWC lambda, 3 PMLB carriers (PASS, FRAGILE recorded).
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=eq2
SCORER=runs/eq2/frozen/eq2_score.py
FETCH=pmlb
NOCHECK=1
IDS="mfeat_fourier mfeat_pixel texture"
QUICKRUN="mfeat_fourier ewc eq 1.0 3"
QUICKREF=rerun_a.json
. "$HERE/../../_shared/ashes_study.sh"
