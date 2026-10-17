#!/usr/bin/env bash
# Re-run the scripts in this folder and compare with the committed outputs. Writes only to ./out.
#   ./run.sh quick     earlier checks (Ashes, forms, bottleneck, origin of life), MP-REBUS C1-C5,
#                      P23-ALGOTYPES delayed-gratification analysis, chart data            (about 4 min)
#   ./run.sh sorting   quick + the P23-ALGOTYPES "same present, different past" simulator (about 1.5 min more)
#                      and MP-REBUS C5b, C6b, C8 (about 17 min more)
#   ./run.sh ageing    quick + three P23-AGING-CRR repair arms on the 50 frozen test seeds, using the authors'
#                      ageing model, cloned at the pinned commits (about 25 min on 3 cores; Python 3.11, torch)
# Python >= 3.11 with numpy and scipy (requirements.txt) for quick/sorting; see README for the ageing environment.
set -euo pipefail
cd "$(dirname "$0")"
MODE="${1:-quick}"
PY="${PYTHON:-python3}"
HERE="$PWD"
mkdir -p out
status=0
cmpf() { "$PY" compare.py "$1" "$2" || status=1; }

echo "== earlier checks"
PYTHONPATH=ashes/src "$PY" ashes/ontology/checks/turing_safety_ingression.py > out/turing_safety_ingression.txt
"$PY" phoenix/forms/forms_checks.py > out/forms_output.json
(cd phoenix/bio_cog && "$PY" bio_cog_challenges.py) > out/bio_cog_challenges_output.json
(cd phoenix/origin_of_life && "$PY" ool_challenges.py) > out/ool_challenges_output.json
for f in turing_safety_ingression.txt forms_output.json bio_cog_challenges_output.json ool_challenges_output.json; do
  cmpf "out/$f" "expected/$f"; done

echo "== MP-REBUS checks (busy-franklin); run in a copy so committed outputs stay untouched"
MP=phoenix/mp-rebus/MP-REBUS-PLATONIC-CHECKS-2026-10-14
rm -rf out/mp && mkdir -p out/mp && cp -r "$MP/checks" out/mp/checks && mkdir -p out/mp/outputs
CHECKS="c1_information_length c2_planarian_kernels c3_precedence_library c4_rebus_kernel c5_sorting_surplus"
[ "$MODE" = sorting ] && CHECKS="$CHECKS c5b_sorting_surplus_run2 c6b_state_sufficiency_visits c8_scheduling_stickiness"
for c in $CHECKS; do
  (cd out/mp/checks && "$PY" "$c.py" > /dev/null)
  for x in json txt; do cmpf "out/mp/outputs/$c.$x" "$MP/outputs/$c.$x"; done
done

echo "== P23-ALGOTYPES delayed-gratification analysis (sweet-gauss)"
AL=phoenix/p23/P23-ALGOTYPES-2026-10-16
(cd "$AL" && "$PY" dg_analyze.py "$HERE/out/dg_analysis.json" results/dg_bubble.json results/dg_insertion_*.json > /dev/null)
cmpf out/dg_analysis.json "$AL/results/dg_analysis.json"

echo "== chart data"
"$PY" chart_data.py > out/chart_data.json
cmpf out/chart_data.json expected/chart_data.json

if [ "$MODE" = sorting ]; then
  echo "== P23-ALGOTYPES same present, different past (simulator; no third-party code needed)"
  for m in BS SI; do
    "$PY" "$AL/crr_history.py" "out/crr_${m}_w20.json" --mix "$m" --seeds 50 --k 3 --window 20 --max_ticks 400000
    cmpf "out/crr_${m}_w20.json" "$AL/results/crr_history/crr_${m}_w20.json"
  done
  echo "== authors' code for the official-class runs (not run by default): Zhangtaining/cell_research @ 1fd2bd59 (no licence)"
  [ -d out/ext/cell_research ] || git clone -q https://github.com/Zhangtaining/cell_research.git out/ext/cell_research
  git -C out/ext/cell_research checkout -q 1fd2bd5921c1f6b423a71f691d5189106a8a1020
  echo "   e.g. python3 -I $AL/official_injury.py out/ext/cell_research out/official_injury_BS.json --mix BS --exps 20 --window 20 --timeout 30"
  echo "   (thread interleaving is not seeded: official runs repeat in distribution only)"
fi

if [ "$MODE" = ageing ]; then
  echo "== P23-AGING-CRR: authors' ageing NCA (bhartl/muse @ 9404ec3, bhartl/NeurEvo @ c93ac2c9; Apache 2.0 + academic-use rider)"
  [ -d out/ext/muse ] || git clone -q https://github.com/bhartl/muse.git out/ext/muse
  [ -d out/ext/NeurEvo ] || git clone -q https://github.com/bhartl/NeurEvo.git out/ext/NeurEvo
  git -C out/ext/muse checkout -q 9404ec39cb4c6cda828eb1fe288dd4e6c05a1d99
  git -C out/ext/NeurEvo checkout -q c93ac2c9f1cab23e12a5323bb1b451f1d745edf0
  NPY="${NCA_PYTHON:-$PY}"
  CR="$HERE/phoenix/p23/P23-AGING-CRR-2026-10-16"
  mkdir -p out/nca
  export OMP_NUM_THREADS=1
  R="$NPY -I $CR/crr_repair.py --muse $HERE/out/ext/muse --mindcraft $HERE/out/ext/NeurEvo --q 0.99 --seeds 1000:1050"
  $R --arm NONE --out "$HERE/out/nca/NONE.npz" & $R --arm C_PRIM --out "$HERE/out/nca/C_PRIM.npz" &
  $R --arm S_CLOCK_TARGET --delta 21,18,10 --out "$HERE/out/nca/S_CLOCK_TARGET.npz" & wait
  "$PY" "$CR/analyze_crr.py" out/nca_summary.json out/nca --contrasts C_PRIM:NONE,S_CLOCK_TARGET:C_PRIM
  "$PY" - <<'EOF'
import json
new = json.load(open("out/nca_summary.json"))["arms"]
ref = json.load(open("phoenix/p23/P23-AGING-CRR-2026-10-16/results/test_n015.json"))["arms"]
for a in new:
    print(a, {k: (new[a][k], ref[a][k]) for k in ("late", "t_all_intact", "writes")},
          "identical" if all(new[a][k] == ref[a][k] for k in new[a]) else "DIFFERS")
EOF
fi
exit $status
