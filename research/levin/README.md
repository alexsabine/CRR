# CRR and Michael Levin's programme: code and record

This folder holds everything needed to re-run the computations quoted on [`levin.html`](../../levin.html), and the
record files the page cites. Nothing here is new research. The scripts are copied verbatim from two research
repositories; two small helpers (`chart_data.py`, `compare.py`) and `run.sh` were written for the web page.

Status: draft, 17 October 2026.

## Sources

| repository | commit | what came from it |
|---|---|---|
| Ashes (`ashes_crr`) | `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d` (main, 2026-10-01; the commit Phoenix pins) | `ontology/checks/turing_safety_ingression.py` and its pinned output; the `src/crr` modules it imports; ontology note 07 and its citation record |
| Phoenix (`Phoenix-1-`) | `1295af24e82e0502a6bd284cd021149d4891eb5b` (branch `claude/nifty-mccarthy-ck9nco`; for these files identical to `main` at `bfd0972`) | `Phoenix_Egg/studies/FORMS-AND-EASEMENT-2026-10-06/forms_checks.py`, `Phoenix_Egg/BOTTLENECK_CHALLENGES/2026-10-05_RUN/{bio_cog_challenges.py, crr_instrument.py}`, `Phoenix_Egg/BOTTLENECK_CHALLENGES/2026-10-06_ORIGIN_OF_LIFE/{ool_challenges.py, crr_instrument.py}`, their committed outputs, and the record files under `records/phoenix/` (paths kept, relative to `Phoenix_Egg/`) |

## Layout

```
ashes/src/crr/...                         Ashes modules imported by the battery (8 files, verbatim)
ashes/ontology/checks/turing_safety_ingression.py   Ashes ontology 07 battery, 9 rows (verbatim)
phoenix/forms/forms_checks.py             FORMS-AND-EASEMENT checks F1-F5 (verbatim)
phoenix/bio_cog/                          bottleneck challenges B1, B3, B4 + crr_instrument.py (verbatim)
phoenix/origin_of_life/                   origin-of-life challenges O1-O4 + crr_instrument.py (verbatim)
chart_data.py                             page helper: reads the numbers drawn in the three charts
compare.py                                page helper: byte / JSON / numeric comparison
run.sh                                    runs everything into out/ and compares with expected/
expected/                                 committed outputs from the two repositories, plus chart_data.json
records/                                  the notes the page quotes (verbatim copies)
requirements.txt                          numpy and scipy versions used for the re-run below
```

## The scripts

| script | what it is | used on the page for | runtime (1 CPU) | expected output |
|---|---|---|---|---|
| `ashes/ontology/checks/turing_safety_ingression.py` | Ashes ontology battery 07, "Turing systems, AI safety and platonic ingression" (SYNTHESIS class, 9 rows, seeded, no data) | row 4: 40-cell sort with a wrong-way cell, surplus = 2 x away-moves (REDUNDANT-DOMAIN); row 8: Hopfield mixture state (REDUNDANT-DOMAIN) | about 30 s (row 4 alone well under 1 s) | `expected/turing_safety_ingression.txt` |
| `phoenix/forms/forms_checks.py` | Phoenix FORMS-AND-EASEMENT checks F1-F5 on the M7 reading, each with a must-fail arm; no rung | F1b form selection 0.981 vs P(form +) 0.5145; F2 hysteresis; F4 precedence 3.00 to 2.54 bits | about 10 s | `expected/forms_output.json` |
| `phoenix/bio_cog/bio_cog_challenges.py` | Phoenix bottleneck challenges, biology and cognition, 2026-10-05 | B1 ageing (Raz ... Alon 2026): AUC 0.90 for state vs 0.42 for accumulated arc, NO CONTACT; B4 Blattner identifiability | about 3 s | `expected/bio_cog_challenges_output.json` |
| `phoenix/origin_of_life/ool_challenges.py` | Phoenix origin-of-life challenges, 2026-10-06 | O4: M7 as history versus state, REDUCES (accuracies 0.65 to 0.97) | about 45 s | `expected/ool_challenges_output.json` |
| `chart_data.py` | page helper; calls `cell_view_sort` from the Ashes battery with row 4's arguments and executes `forms_checks.py` unchanged, then prints the values the charts draw. Checks the F4 endpoints against the committed output | the three charts | about 15 s | `expected/chart_data.json` |

No script needs a GPU, a network connection or any input data. All write only to standard output.

## How to run and compare

```
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
./run.sh                    # or: PYTHON=/path/to/python ./run.sh
```

Single scripts, from this folder:

```
PYTHONPATH=ashes/src python ashes/ontology/checks/turing_safety_ingression.py > out/turing_safety_ingression.txt
python phoenix/forms/forms_checks.py > out/forms_output.json
(cd phoenix/bio_cog && python bio_cog_challenges.py) > out/bio_cog_challenges_output.json
(cd phoenix/origin_of_life && python ool_challenges.py) > out/ool_challenges_output.json
python chart_data.py > out/chart_data.json
python compare.py out/forms_output.json expected/forms_output.json
```

`compare.py` reports byte-identical, JSON-equal, or the largest relative difference between numbers (it passes
below 1e-12). The Ashes CI uses `cmp` on the battery output; the same byte comparison applies here.

## Re-run result (17 October 2026)

Python 3.13.16, numpy 2.5.4, scipy 1.18.1, Linux x86-64, CPU only. Run from a fresh copy of this folder with
`./run.sh`; total wall time 1 min 48 s.

| output | result |
|---|---|
| `turing_safety_ingression.txt` | byte-identical |
| `forms_output.json` | byte-identical |
| `bio_cog_challenges_output.json` | B1 and B3 identical; the two B4 residual sums of squares differ in the last digit only (506.84708315609237 vs 506.8470831560925 and 506.8470831560924; relative difference 2.2e-16 and 1.1e-16) |
| `ool_challenges_output.json` | byte-identical |
| `chart_data.json` | byte-identical (generated in a first run and re-generated in the second); the F4 endpoints equal the committed `forms_output.json` |

## What this folder does not contain

- No Levin-lab data. There is no public per-animal regeneration dataset (`records/phoenix/studies/P23-LEVIN-TESTBED-2026-10-07/DATA_ACCESS.md`).
- No script for the planarian test P23-LEVIN1. It is a declaration, not frozen and not run.
- No reproduction of Zhang, Goldstein and Levin (2025). Row 4 of the Ashes battery is inspired by that paper, read only as a search snippet, and is not a reproduction.
- No ageing-reversal or recovery result. None exists in either repository.

## Licence

Code: MIT. Text: CC BY 4.0. © Alexander Sabine 2026.

MIT licence for the code in this folder:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice
and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS
PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
