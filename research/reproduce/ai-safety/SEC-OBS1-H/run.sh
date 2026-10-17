#!/usr/bin/env bash
# SEC-OBS1-H (held-out run of the observation-aware SEC study).
# Usage: bash run.sh rescore   (default; minutes) re-run the frozen scorer on the committed held-out episodes
#                              expected/heldout_episodes.jsonl and compare score.json / score.txt byte for byte.
#        bash run.sh full      re-run the 100 held-out episodes (torch CPU; recorded 16 min wall / 46 CPU-min with
#                              3 workers on 4 cores), then score and compare. Seeds are derived from the freeze commit
#                              92c73fa15f41f586da1ed108edc108efde145640 exactly as run_heldout.sh does.
# Optional: WORK=<dir>, PYTHON=<python with the packages already installed>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
ID=SEC-OBS1-H-2026-10-08; SHA=92c73fa15f41f586da1ed108edc108efde145640; WORK="${WORK:-$HERE/work}"; MODE="${1:-rescore}"
say "stage $WORK"; stage "$HERE" "$WORK" phoenix
OUT="$WORK/RUNS/$ID"; mkdir -p "$OUT"
if [ "$MODE" = full ]; then
  say "environment (full)"; pyenv "$HERE/requirements.txt"
  # run_heldout.sh calls `python3` from PATH; put the environment first. It writes RUNS/<ID>/{draw_log.json,run.log,
  # heldout_episodes.jsonl,score.json,score.txt}. run_episodes.py appends to heldout_episodes.jsonl and skips finished
  # seeds, which is why the work tree starts with an empty RUNS/<ID>/.
  say "run_heldout.sh $SHA"; PATH="$(dirname "$PY"):$PATH" bash "$WORK/studies/$ID/run_heldout.sh" "$SHA"
  say "compare"
  # heldout_episodes.jsonl is NOT compared byte for byte: workers append in completion order (imap_unordered) and
  # each row carries wall-clock timings. The registered numbers are in score.json / score.txt.
else
  say "environment (rescore)"; pyenv "$HERE/requirements-rescore.txt"
  say "score (frozen score_secobs1h.py) on expected/heldout_episodes.jsonl"
  "$PY" -B "$WORK/studies/$ID/score_secobs1h.py" "$HERE/expected/heldout_episodes.jsonl" "$WORK/studies/$ID/dev_episodes.jsonl" "$OUT/score.json" > "$OUT/score.txt" 2>&1
  say "compare"
fi
same "$OUT/score.json" "$HERE/expected/score.json"
same "$OUT/score.txt" "$HERE/expected/score.txt"
cat "$OUT/score.txt"
finish
