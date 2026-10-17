#!/usr/bin/env bash
# Re-run every script in this folder and compare with expected/. Needs Python >= 3.11 with numpy and scipy
# (see requirements.txt). Writes only to ./out. Total about 1.5 minutes on one CPU core.
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
mkdir -p out
echo "1/5 Ashes ontology 07 battery (about 30 s)"
PYTHONPATH=ashes/src "$PY" ashes/ontology/checks/turing_safety_ingression.py > out/turing_safety_ingression.txt
echo "2/5 Phoenix FORMS-AND-EASEMENT checks (about 10 s)"
"$PY" phoenix/forms/forms_checks.py > out/forms_output.json
echo "3/5 Phoenix bottleneck challenges B1, B3, B4 (about 3 s)"
(cd phoenix/bio_cog && "$PY" bio_cog_challenges.py) > out/bio_cog_challenges_output.json
echo "4/5 Phoenix origin-of-life challenges O1-O4 (about 45 s)"
(cd phoenix/origin_of_life && "$PY" ool_challenges.py) > out/ool_challenges_output.json
echo "5/5 chart data for levin.html (about 10 s)"
"$PY" chart_data.py > out/chart_data.json
echo
status=0
for f in turing_safety_ingression.txt forms_output.json bio_cog_challenges_output.json ool_challenges_output.json chart_data.json; do
  "$PY" compare.py "out/$f" "expected/$f" || status=1
done
exit $status
