#!/usr/bin/env bash
# LANDAUER-CRR: check the frozen files against their hashes, run the frozen script and the labelled post hoc
# diagnostic, and compare both outputs with expected/. CPU, numpy only; about 2 minutes.
# Usage: bash run.sh     (WORK=<dir> and PYTHON=<python with numpy 2.5.3> are optional)
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
WORK="${WORK:-$HERE/work}"
if [ -e "$WORK" ] && [ -n "$(ls -A "$WORK" 2>/dev/null | grep -v '^\.venv$' || true)" ]; then
  echo "refusing: $WORK is not empty. Remove it or set WORK=<new dir>." >&2; exit 2; fi
say "frozen files against FROZEN.sha256"; ( cd "$HERE/src" && sha256sum -c ../FROZEN.sha256 )
say "stage $WORK"; mkdir -p "$WORK"; cp -a "$HERE/src/." "$WORK/"
say "environment"; pyenv "$HERE/requirements.txt"
say "frozen run"; ( cd "$WORK" && time "$PY" -I -B checks/landauer_crr.py > /dev/null )
say "post hoc diagnostic (written after the P4b failure was recorded)"; ( cd "$WORK" && "$PY" -B checks/posthoc_p4b_excess_work.py > /dev/null )
say "compare"
same "$WORK/outputs/landauer_crr.json" "$HERE/expected/landauer_crr.json"
same "$WORK/outputs/posthoc_p4b_excess_work.json" "$HERE/expected/posthoc_p4b_excess_work.json"
finish
