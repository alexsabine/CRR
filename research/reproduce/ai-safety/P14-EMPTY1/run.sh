#!/usr/bin/env bash
# P14-EMPTY1: regenerate the 2400 synthetic worlds, run the frozen scorer, compare with expected/, then recompute the
# decision table with the locked engine scripts/guard.py (decide.py). CPU, numpy only; about 5-10 min.
# Usage: bash run.sh     (WORK=<dir> and PYTHON=<python with numpy 2.4.6> are optional)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
ID=P14-EMPTY1-2026-10-07; WORK="${WORK:-$HERE/work}"
say "stage $WORK"; stage "$HERE" "$WORK" phoenix
say "environment"; pyenv "$HERE/requirements.txt"
mkdir -p "$WORK/receipts/$ID" "$WORK/RUNS/$ID"
say "generate worlds (frozen generate.py)"
( cd "$WORK/studies/$ID" && "$PY" -I -B generate.py > ../../receipts/$ID/data_manifest.json )
say "score (frozen score.py)"
( cd "$WORK" && time "$PY" -I -B studies/$ID/score.py studies/$ID > RUNS/$ID/outcomes.json )
say "compare"
# the generator's stdout is the full 2400-world manifest (receipts/data_manifest_full.json upstream); receipts/data_manifest.json
# is the 600 target-world subset with raw/-relative paths that the receipt checker reads, derived from it afterwards.
same "$WORK/receipts/$ID/data_manifest.json" "$HERE/expected/receipts/data_manifest_full.json"
same "$WORK/RUNS/$ID/outcomes.json" "$HERE/expected/outcomes.json"
say "decision (locked engine guard.decision; see decide.py)"
"$PY" -I -B "$HERE/decide.py" "$WORK/studies/$ID" "$WORK/RUNS/$ID/outcomes.json"
finish
