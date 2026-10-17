#!/usr/bin/env bash
# P18B-LAGGED-PROVENANCE pre-freeze pilot (NO-GO recorded; nothing frozen; development seeds only).
# Usage: bash run.sh tiny    (default) the same code paths at ~1/100 size, ~2-3 CPU-min; compares outputs/pilot_tiny_public.json
#        bash run.sh pilot   the full 6000-simulation pilot (recorded 0.876 CPU-hours; 4 workers); compares outputs/pilot_public.json
#        bash run.sh mp10    the MP10 check; compares outputs/mp10_check.json
# Optional: WORK=<dir>, SEALED=<dir outside dirname(WORK)> (default: a fresh mktemp dir), PYTHON=<python with numpy>.
# The commitment can NOT be reproduced: the original salt and sealed estimates stayed in an operator directory and were
# never committed, and every run draws a fresh random salt. compare_public.py skips the commitment and run times only.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; . "$HERE/../../_shared/common.sh"
ID=P18B-LAGGED-PROVENANCE-2026-10-09; WORK="${WORK:-$HERE/work}"; MODE="${1:-tiny}"; SEALED="${SEALED:-$(mktemp -d)}"
say "stage $WORK"; stage "$HERE" "$WORK" none
# pubworld_draft.py imports ../P18-LOOP1-2026-10-08/loopworld.py and ../P18-PROV-FLAME-2026-10-09/provworld_draft.py (both in src/),
# and pilot_p18b.py compares some of its checks with the committed files in its own outputs/ folder, so they are put back there.
mkdir -p "$WORK/studies/$ID/outputs"; cp "$HERE"/expected/*.json "$WORK/studies/$ID/outputs/"
say "environment"; pyenv "$HERE/requirements.txt"
cd "$WORK/studies/$ID"
case "$MODE" in
  tiny)  time "$PY" -I -B pilot_p18b.py tiny --sealed-dir "$SEALED" --workers "${WORKERS:-1}" > "$WORK/stdout.txt"; F=pilot_tiny_public.json ;;
  pilot) time nice -n 19 "$PY" -I -B pilot_p18b.py pilot --sealed-dir "$SEALED" --workers "${WORKERS:-4}" > "$WORK/stdout.txt"
         "$PY" -I -B pilot_p18b.py verify --sealed-dir "$SEALED"; F=pilot_public.json ;;
  mp10)  time "$PY" -I -B pilot_p18b.py mp10 > "$WORK/stdout.txt" || true; F=mp10_check.json ;;
  *) echo "usage: bash run.sh [tiny|pilot|mp10]"; exit 1 ;;
esac
say "compare outputs/$F with expected/$F (field by field; commitment and timings skipped)"
"$PY" -I -B "$HERE/compare_public.py" "outputs/$F" "$HERE/expected/$F" || MISMATCH=1
"$PY" -I -c "import json,sys; d=json.load(open(sys.argv[1])); g=d.get('go_no_go',{}); print('GO' if g.get('GO') else 'NO-GO', '| failing must-pass:', [k for k,v in g.get('must_pass',{}).items() if not v])" "outputs/$F" || true
finish
