#!/usr/bin/env bash
# SEC-PG-LLM-H (held-out Gutenberg books, byte-level Transformer, continual learning EN -> FR/DE).
# Usage: bash run.sh rescore  (default; about a minute) re-run the frozen scorer score_llmh.py on the committed per-unit
#                             results expected/units_*.jsonl and compare score.json / score.txt byte for byte.
#        bash run.sh full     HARD: re-train every unit. Recorded 409 min wall (~6.8 h) / ~27 CPU-hours on 4 cores, CPU
#                             only, torch 2.14.1+cpu. Fetches the 4 recorded books from gutenberg.org (sha256-checked).
# Optional: WORK=<dir>, PYTHON=<python with the packages>, WORKERS is fixed at 4 by the frozen run_heldout.sh.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
ID=SEC-PG-LLM-H-2026-10-08; WORK="${WORK:-$HERE/work}"; MODE="${1:-rescore}"
say "stage $WORK"; stage "$HERE" "$WORK" phoenix
RUN="$WORK/RUNS/$ID"; mkdir -p "$RUN"
# Inputs the frozen code reads from RUNS/<ID>/: the recorded lottery outcome and anchor check (both committed upstream).
cp "$HERE/expected/draw_log.json" "$HERE/expected/anchor_check.json" "$RUN/"
if [ "$MODE" = full ]; then
  say "environment (full)"; pyenv "$HERE/requirements.txt"
  say "fetch the 4 admitted books"; "$PY" -I -B "$HERE/fetch_books.py" "$RUN/draw_log.json" "$RUN/raw/books"
  # The runner is resumable: it skips every unit already in RUNS/<ID>/units_*.jsonl (run_heldout.py line 85). The
  # work tree therefore starts with NO units; the committed ones stay in expected/ for comparison.
  say "run (frozen run_heldout.sh run: pretrain, main, sens, rerun, then score)"
  ( cd "$WORK" && PATH="$(dirname "$PY"):$PATH" bash studies/$ID/run_heldout.sh run )
  for f in units_pretrain units_main units_sens units_rerun; do echo "$f: $(wc -l < "$RUN/$f.jsonl") produced, $(wc -l < "$HERE/expected/$f.jsonl") committed"; done
  echo "(unit rows carry wall-clock timings, so they are compared through the scorer's outputs, not byte for byte)"
else
  say "environment (rescore)"; pyenv "$HERE/requirements-rescore.txt"
  cp "$HERE"/expected/units_{pretrain,main,sens,rerun}.jsonl "$RUN/"
  say "score (frozen score_llmh.py) on the committed units"
  ( cd "$WORK" && "$PY" -I -B studies/$ID/score_llmh.py > "$RUN/score.json" )
fi
say "compare"
same "$RUN/score.json" "$HERE/expected/score.json"
# score.txt line 1 carries the time the scorer ran ("written <UTC>"); compare from line 2 on.
tail -n +2 "$RUN/score.txt" > "$RUN/score.body.txt"; tail -n +2 "$HERE/expected/score.txt" > "$WORK/expected_score.body.txt"
same "$RUN/score.body.txt" "$WORK/expected_score.body.txt"
grep '^VERDICT' "$RUN/score.txt"
finish
