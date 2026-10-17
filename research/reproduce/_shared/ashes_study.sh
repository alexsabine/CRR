# Shared driver for the Ashes continual-learning studies (sourced by each study's run.sh). MIT; see ../LICENSE.
# The study's run.sh sets, before sourcing:
#   S        short id used by Ashes paths (e.g. sec4)          SCORER  runs/<S>/frozen/<S>_score.py
#   FETCH    pmlb | openml                                     IDS     carriers (PMLB names or OpenML data ids)
#   MANIFESTS  committed manifest(s) the fetched files must match (default "$S")
#   PART     extra arguments for check/all (SEC6R: "--part B"; default empty)
#   QUICK    one carrier for the R9-style rerun:  all <QUICK> --out runs/<S>/rerun_<QUICK>.jsonl, compared with expected/results_<QUICK>.jsonl
#   QUICKRUN (EQ studies) arguments of a single-unit `run`, compared with expected/$QUICKREF (e.g. rerun_a.json)
#   NOCHECK  set to 1 if the scorer has no `check` command
#   TIMES    set to 1 if the scorer times each run (SEC3-SEC6R) and so takes --times
# Modes:  bash run.sh rescore   (default) re-run the frozen scorer on the committed per-carrier results; no data download
#         bash run.sh quick     fetch one carrier, rerun it, compare byte for byte (or as JSON for single-unit reruns)
#         bash run.sh full      fetch every carrier, check, rerun every carrier, score, compare everything
# Environment: uv with the committed Ashes lockfile (_shared/ashes/uv.lock; Python 3.14 from .python-version).

set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/common.sh"
WORK="${WORK:-$HERE/work}"; MODE="${1:-rescore}"; PART="${PART:-}"; MANIFESTS="${MANIFESTS:-$S}"
command -v uv >/dev/null || { echo "uv is required (https://docs.astral.sh/uv/); see the README for a pip fallback" >&2; exit 2; }
say "stage $WORK"; stage "$HERE" "$WORK" ashes
cd "$WORK"
say "environment (uv sync --frozen against the committed uv.lock)"; uv sync --frozen -q
UVR() { uv run --frozen -q python "$@"; }
UVR -c 'import sys, numpy, scipy; print("python", sys.version.split()[0], "numpy", numpy.__version__, "scipy", scipy.__version__)'

fetch() {   # fetch <ids...> into data/raw, writing data/manifests/<S>_refetch.sha256, then compare with the committed manifests
  if [ "$FETCH" = pmlb ]; then UVR data/fetch_pmlb.py --manifest "${S}_refetch" "$@"; else UVR data/fetch_openml.py --manifest "${S}_refetch" "$@"; fi
  python3 - "data/manifests/${S}_refetch.sha256" $(for m in $MANIFESTS; do echo "data/manifests/$m.sha256"; done) <<'PY'
import sys
new = [l.split()[:2] for l in open(sys.argv[1]) if l.strip()]
old = {tuple(l.split()[:2]) for m in sys.argv[2:] for l in open(m) if l.strip()}
bad = [p for h, p in new if (h, p) not in old and not p.endswith('.json')]
desc = [p for h, p in new if (h, p) not in old and p.endswith('.json')]
print(f"fetched {len(new)} files; data files matching the committed manifest: {len(new) - len(bad) - len(desc)}; differing data files: {bad or 'none'}")
if desc: print(f"note: OpenML description JSON changed since the study ({len(desc)} files); the scorer reads the ARFF, not these")
sys.exit(1 if bad else 0)
PY
}

mkdir -p "runs/$S"
case "$MODE" in
  rescore)
    say "rescore: frozen scorer on the committed results (expected/results_*.jsonl, and times_*.jsonl where the scorer reports CPU shares)"
    cp "$HERE"/expected/results_*.jsonl "runs/$S/"; cp "$HERE"/expected/times_*.jsonl "runs/$S/" 2>/dev/null || true
    UVR "$SCORER" score runs/$S/results_*.jsonl > "runs/$S/score.txt"
    same "runs/$S/score.txt" "$HERE/expected/score.txt" ;;
  quick)
    if [ -n "${QUICKRUN:-}" ]; then
      set -- $QUICKRUN; say "quick: fetch $1, single unit: run $QUICKRUN"; fetch "$1"
      UVR "$SCORER" run $QUICKRUN > "runs/$S/quick.json"
      if cmp -s "runs/$S/quick.json" "$HERE/expected/$QUICKREF"; then echo "MATCH   $QUICKREF (byte for byte)"; else
        python3 -c "import json,sys; a=json.loads(open(sys.argv[1]).read()); b=json.loads(open(sys.argv[2]).read()); print(('MATCH   ' if a==b else 'DIFFERS ')+sys.argv[2].split('/')[-1]+' (bytes differ; compared as JSON)'); sys.exit(a!=b)" "runs/$S/quick.json" "$HERE/expected/$QUICKREF" || MISMATCH=1; fi
    else
      say "quick: fetch $QUICK, rerun every arm on it (the study's own R9 rerun)"; fetch "$QUICK"
      # SEC3-SEC6R time every run; without --times the timing rows go to the --out path with results_ replaced by times_,
      # which for a rerun_ file is the same file, so the prereg's own R9 command passes --times explicitly.
      UVR "$SCORER" all "$QUICK" $PART --out "runs/$S/rerun_$QUICK.jsonl" ${TIMES:+--times "runs/$S/rerun_times_$QUICK.jsonl"}
      same "runs/$S/rerun_$QUICK.jsonl" "$HERE/expected/results_$QUICK.jsonl"
    fi ;;
  full)
    say "full: fetch all carriers"; fetch $IDS
    if [ -z "${NOCHECK:-}" ]; then UVR "$SCORER" check $PART > "runs/$S/data_check.txt" || true; fi
    for i in $IDS; do say "all $i"; UVR "$SCORER" all "$i" $PART --out "runs/$S/results_$i.jsonl" ${TIMES:+--times "runs/$S/times_$i.jsonl"}; same "runs/$S/results_$i.jsonl" "$HERE/expected/results_$i.jsonl"; done
    UVR "$SCORER" score runs/$S/results_*.jsonl > "runs/$S/score.txt"
    same "runs/$S/score.txt" "$HERE/expected/score.txt" ;;
  *) echo "usage: bash run.sh [rescore|quick|full]"; exit 1 ;;
esac
grep -E 'PASS|FAIL|NOT DECIDABLE|verdict' "runs/$S/score.txt" 2>/dev/null | head -20 || true
finish
