#!/usr/bin/env bash
# SCL2 (Ashes): the lossless pause on 11 unseen PMLB carriers (9 scored).
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=scl2
SCORER=runs/scl2/frozen/scl2_score.py
FETCH=pmlb
IDS="allhyper allrep car_evaluation nursery wine_quality_red analcatdata_authorship analcatdata_dmft analcatdata_germangss collins soybean vehicle"
QUICK=vehicle
. "$HERE/../../../_shared/ashes_study.sh"
