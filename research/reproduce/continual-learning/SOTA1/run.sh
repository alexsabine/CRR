#!/usr/bin/env bash
# SOTA1 (Ashes): online Split-CIFAR-100 (10 tasks), the CRR learner against ER, ER-ACE, DER++ and X-DER in vendored Mammoth.
# Usage: bash run.sh rescore   (default; seconds, standard library only) re-run the frozen scorer prereg/sota1/sota1_score.py on
#                              the 115 committed unit records expected/units/*.json; compare score.txt and results.json.
#        bash run.sh full [tier ...]   HARD: train every unit. Budget 30.3 unit-hours (2 units x 2 threads on 4 CPUs; the
#                              recorded queue took ~17 h wall). Downloads CIFAR-100 (~160 MB) from cs.toronto.edu. CPU only.
#                              Six units (lwf, ewc_on x 3 seeds) failed on an argparse error in the original run and will
#                              fail again (NOT DECIDABLE in the record).
# Optional: WORK=<dir>.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
WORK="${WORK:-$HERE/work}"; MODE="${1:-rescore}"; shift || true
say "stage $WORK"; stage "$HERE" "$WORK" ashes
cd "$WORK"; mkdir -p runs/sota1
if [ "$MODE" = full ]; then
  command -v uv >/dev/null || { echo "uv is required" >&2; exit 2; }
  # The frozen runner hard-codes ROOT/studies/sota1/env/.venv/bin/python (sota1_run.py, PY = ...). Build that environment
  # from the frozen lock (Python 3.12, torch 2.14.0+cpu, torchvision 0.29.0+cpu) at the path it expects.
  say "environment (runs/sota1/frozen/env -> studies/sota1/env, uv sync --frozen)"
  mkdir -p studies/sota1/env; cp runs/sota1/frozen/env/pyproject.toml runs/sota1/frozen/env/uv.lock studies/sota1/env/
  ( cd studies/sota1/env && uv sync --frozen -q )
  say "fetch CIFAR-100 (md5-checked); the committed manifest is kept as sota1.sha256.committed for comparison"
  cp data/manifests/sota1.sha256 data/manifests/sota1.sha256.committed
  studies/sota1/env/.venv/bin/python data/fetch_cifar100.py
  diff <(awk '{print $1, $2}' data/manifests/sota1.sha256.committed) <(awk '{print $1, $2}' data/manifests/sota1.sha256) && echo "CIFAR-100 files match the committed manifest"
  # sota1_run.py runs MISSING units only: runs/sota1/units/ starts empty in the work tree (the committed units are in expected/).
  say "run (frozen sota1_run.py run $*)"; studies/sota1/env/.venv/bin/python runs/sota1/frozen/sota1_run.py run "$@"
else
  say "rescore: committed units"; cp -a "$HERE/expected/units" runs/sota1/units
fi
say "score (frozen prereg/sota1/sota1_score.py)"
python3 -B prereg/sota1/sota1_score.py > runs/sota1/score.txt
say "compare"
same runs/sota1/score.txt "$HERE/expected/score.txt"
same runs/sota1/results.json "$HERE/expected/results.json"
sed -n 1,14p runs/sota1/score.txt
finish
