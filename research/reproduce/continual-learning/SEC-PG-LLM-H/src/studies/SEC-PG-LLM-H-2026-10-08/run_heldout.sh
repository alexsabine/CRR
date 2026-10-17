#!/usr/bin/env bash
# SEC-PG-LLM-H data step and run, from Phoenix_Egg/ (PREREG.md, order of operations). Each data-step stage stops for a commit and push.
#   bash studies/SEC-PG-LLM-H-2026-10-08/run_heldout.sh anchor     -> RUNS/<id>/anchor_check.json (commit and push it with the upgraded receipts/<id>/FREEZE.json.ots)
#   bash studies/SEC-PG-LLM-H-2026-10-08/run_heldout.sh draw       -> raw/books (git-ignored), draw_attempts.jsonl, draw_log.json
#   bash studies/SEC-PG-LLM-H-2026-10-08/run_heldout.sh register   -> DATA/SEEN.md rows (commit and push with the draw files)
#   bash studies/SEC-PG-LLM-H-2026-10-08/run_heldout.sh run        -> units_*.jsonl, run.log, score.json (stdout of the scorer), score.txt
#   bash studies/SEC-PG-LLM-H-2026-10-08/run_heldout.sh receipts   -> receipts/<id>/{exposure_log,data_manifest,rerun_a,rerun_b,receipt}.json (RESULT.md goes in RUNS/<id>/, never in this folder)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; ID="$(basename "$HERE")"; OUT="$HERE/../../RUNS/$ID"; mkdir -p "$OUT"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
case "${1:-}" in
  anchor) python3 -I "$HERE/data_step.py" anchor ;;
  draw) python3 -I "$HERE/data_step.py" draw 2>&1 | tee -a "$OUT/draw.log" ;;
  register) python3 -I "$HERE/data_step.py" register ;;
  run) ( time python3 -I "$HERE/run_heldout.py" 4 all ) >> "$OUT/run.log" 2>&1
       python3 -I "$HERE/score_llmh.py" > "$OUT/score.json"; echo "SCORED $(date -u +%FT%TZ)" >> "$OUT/run.log" ;;
  receipts) python3 -I "$HERE/make_receipts.py" ;;
  *) echo "usage: run_heldout.sh anchor|draw|register|run|receipts"; exit 1 ;;
esac
