#!/usr/bin/env bash
# RW1 (Ashes Real_World): is Hugging Face Trainer's resume-from-checkpoint an "empty cut" (bitwise identical continuation)
# on GPT-2 (full grid) and Qwen2.5-0.5B-Instruct (pilot)? A declared note (rung R4), not a preregistered test.
# Usage: bash run.sh    MODERATE: about 1 h CPU (single thread per run), needs network to the Hugging Face Hub on first run
#                       (GPT-2 ~0.5 GB, Qwen2.5-0.5B ~2 GB, pinned by revision) and ~8-10 GB free disk for checkpoints.
# Optional: WORK=<dir>, HF_HOME=<cache dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
WORK="${WORK:-$HERE/work}"
command -v uv >/dev/null || { echo "uv is required (https://docs.astral.sh/uv/)" >&2; exit 2; }
say "stage $WORK"; stage "$HERE" "$WORK" ashes
cd "$WORK"
say "environment (uv sync --frozen --group realsys: torch 2.14.0+cpu, transformers 5.17.0, accelerate 1.15.0)"
uv sync --frozen --group realsys -q
say "run (rw1.py downloads the pinned model revisions, then sets HF_HUB_OFFLINE=1 for every arm)"
time uv run --frozen --group realsys python Real_World/checks/rw1.py > Real_World/checks/rw1.txt
say "compare (rw1.txt is byte-compared upstream; rw1_timing.txt is machine-dependent and not compared)"
same Real_World/checks/rw1.txt "$HERE/expected/rw1.txt"
tail -n 1 Real_World/checks/rw1.txt
finish
