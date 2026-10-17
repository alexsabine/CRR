#!/usr/bin/env bash
# SEC-OBS1-H held-out run. Usage: bash run_heldout.sh <freeze_commit_sha>
# Seeds are derived from the freeze commit (the commit that adds this frozen folder), so they could not be chosen before the freeze.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; SHA="$1"; OUT="$HERE/../../RUNS/SEC-OBS1-H-2026-10-08"; mkdir -p "$OUT"
FIRST=$(python3 -c "print(200000 + int('$SHA'[:8], 16) % 700000)"); DRAW=$(python3 -c "print(int('$SHA'[8:16], 16))")
python3 -c "import json,datetime; json.dump(dict(freeze_commit='$SHA', first_seed=$FIRST, count=100, draw_seed=$DRAW, dev_seeds='10000-10119', started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()), open('$OUT/draw_log.json','w'), indent=1)"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
( time python3 "$HERE/run_episodes.py" --seeds "$FIRST:100" --draw_seed "$DRAW" --out "$OUT/heldout_episodes.jsonl" --workers 3 ) > "$OUT/run.log" 2>&1
python3 "$HERE/score_secobs1h.py" "$OUT/heldout_episodes.jsonl" "$HERE/dev_episodes.jsonl" "$OUT/score.json" > "$OUT/score.txt" 2>&1
echo ALL DONE >> "$OUT/run.log"
