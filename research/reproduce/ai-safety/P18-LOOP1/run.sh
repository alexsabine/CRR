#!/usr/bin/env bash
# P18-LOOP1 (DEVELOPMENT ONLY: no preregistration, no ledger row). Re-runs the synthetic feedback-loop harness.
# Usage: bash run.sh          full size, as recorded: loopworld.py 200 200 (about 20 CPU-minutes), then loop_contrasts.py
#        bash run.sh quick    200 calibration seeds, 40 test seeds per world (about 5 CPU-minutes); rows compared one by one
# Optional: WORK=<dir>, PYTHON=<python with numpy>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
ID=P18-LOOP1-2026-10-08; WORK="${WORK:-$HERE/work}"; MODE="${1:-full}"
say "stage $WORK"; stage "$HERE" "$WORK" none
say "environment"; pyenv "$HERE/requirements.txt"
cd "$WORK/studies/$ID"
if [ "$MODE" = quick ]; then N_TEST=40; else N_TEST=200; fi
say "loopworld.py 200 $N_TEST"; time "$PY" -I -B loopworld.py 200 $N_TEST > outputs_stdout.txt
say "compare"
"$PY" -I -B "$HERE/compare_rows.py" outputs/loop_runs.jsonl "$HERE/expected/loop_runs.jsonl" || MISMATCH=1
if [ "$MODE" != quick ]; then
  "$PY" -I -B loop_contrasts.py > /dev/null
  same outputs/loop_runs.jsonl "$HERE/expected/loop_runs.jsonl"
  same outputs/loop_summary.json "$HERE/expected/loop_summary.json"
  same outputs/loop_contrasts.json "$HERE/expected/loop_contrasts.json"
fi
finish
