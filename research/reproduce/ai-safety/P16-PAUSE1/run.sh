#!/usr/bin/env bash
# P16-PAUSE1: regenerate the 600 synthetic MDP worlds, run the frozen scorer, compare with expected/.
# Usage: bash run.sh            (CPU, numpy only; about 5-10 min)
#        WORK=/tmp/p16 bash run.sh   PYTHON=/path/to/python-with-numpy bash run.sh
# The frozen commands (PREREG_CLAIM.json "frozen_commands") are run unchanged, from the layout they expect:
#   <WORK>/studies/P16-PAUSE1-2026-10-07/   (frozen folder)   <WORK>/RUNS/P16-PAUSE1-2026-10-07/raw/  (worlds)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
ID=P16-PAUSE1-2026-10-07; WORK="${WORK:-$HERE/work}"
say "stage $WORK"; stage "$HERE" "$WORK" phoenix
say "environment"; pyenv "$HERE/requirements.txt"
mkdir -p "$WORK/receipts/$ID" "$WORK/RUNS/$ID"
say "generate worlds (frozen generate_p16.py)"
( cd "$WORK/studies/$ID" && "$PY" -I -B generate_p16.py > ../../receipts/$ID/data_manifest.json )
say "score (frozen score_p16.py)"
( cd "$WORK" && time "$PY" -I -B studies/$ID/score_p16.py studies/$ID > RUNS/$ID/outcomes.json )
say "compare"
same "$WORK/receipts/$ID/data_manifest.json" "$HERE/expected/receipts/data_manifest.json"
same "$WORK/RUNS/$ID/outcomes.json" "$HERE/expected/outcomes.json"
python3 -c "import json,sys; print('verdict:', json.load(open(sys.argv[1]))['verdict'])" "$WORK/RUNS/$ID/outcomes.json"
finish
