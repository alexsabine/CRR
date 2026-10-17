#!/usr/bin/env bash
# SCL1 (Ashes): the lossless pause inside a real continual learner, 12 PMLB carriers reused from SEC1.
# Usage: bash run.sh [rescore|quick|full]   (default rescore; see README.md for times). Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
S=scl1
SCORER=runs/scl1/frozen/scl1_score.py
FETCH=pmlb
MANIFESTS="sec1"
IDS="fars krkopt led24 led7 mfeat_factors mfeat_morphological page_blocks satimage segmentation sleep wine_quality_white yeast"
QUICK=led7
. "$HERE/../../../_shared/ashes_study.sh"
