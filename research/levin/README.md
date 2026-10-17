# CRR and Michael Levin's programme: code and record

This folder holds the code, protocols, results and reports behind [`levin.html`](../../levin.html), copied verbatim
from two research repositories, plus a few helpers written for the page (`chart_data.py`, `compare.py`, `run.sh`).
Nothing here is new research. Nothing here is a Phoenix *finding*: one study was exploratory, three were frozen tests
on one public computer model run by one builder, and the MP-REBUS checks are declared-synthetic (R4), not frozen.

Status: draft, 17 October 2026.

## Provenance

| source | branch / commit | what came from it | folder here |
|---|---|---|---|
| Phoenix | `origin/claude/sweet-gauss-i778w1` @ `8159e77d86d4549ba9c0ef02b921d6487d8d2ecb` (2026-10-17) | the four P23 studies (code, PREREG, FREEZE, DESIGN, results, REPORT); the consolidated findings; the Levin-lab survey; the P23-XMEM result | `phoenix/p23/`, `records/phoenix/PROGRAMMES/`, `records/phoenix/SOURCES/`, `records/phoenix/RUNS/` |
| Phoenix | `origin/claude/busy-franklin-yvjak0` @ `bb446ce996df74d8a400d35b5af83180ceef1001` (2026-10-15) | MP-REBUS-PLATONIC-CHECKS (declarations, checks, outputs, RESULT, sorting-arrays report as Markdown); the Platonic-space note | `phoenix/mp-rebus/`, `records/phoenix/FOUNDATIONS/PLATONIC_SPACE_FIELDS_REBUS_2026-10-14.md` |
| Phoenix | `claude/nifty-mccarthy-ck9nco` @ `1295af24e82e0502a6bd284cd021149d4891eb5b` (same as `main` for these files) | earlier checks: FORMS-AND-EASEMENT, bottleneck challenges, origin of life; M7, ND-2, P23-LEVIN1 declaration and other records | `phoenix/forms/`, `phoenix/bio_cog/`, `phoenix/origin_of_life/`, `records/phoenix/` |
| Ashes | `main` @ `a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d` | ontology battery 07 and the `src/crr` modules it imports | `ashes/`, `records/ashes/` |

Study commits inside sweet-gauss: P23-ALGOTYPES complete `36110c7` (exploratory, not frozen); P23-AGING frozen
`14cbb5c`, decision script `cc138ae`, complete `485e23f`; P23-AGING-CRR frozen `7fd6b14`, complete `90c22fc`;
P23-AGING-COMPETENCY frozen `25ef609`, complete `1c20a77`.

### Third-party code (not copied here)

| repository | pinned commit | used by | licence |
|---|---|---|---|
| github.com/Zhangtaining/cell_research | `1fd2bd5921c1f6b423a71f691d5189106a8a1020` | P23-ALGOTYPES official-class runs (`run_official.py`, `dg_official.py`, `official_injury.py`); MP-REBUS C7 | none stated, so it is not redistributed |
| github.com/bhartl/muse | `9404ec39cb4c6cda828eb1fe288dd4e6c05a1d99` | the ageing NCA of Pio-Lopez, Hartl & Levin (2025, *Adv. Sci.* e09872): P23-AGING, -CRR, -COMPETENCY | Apache 2.0 with the Tufts academic-use-only rider |
| github.com/bhartl/NeurEvo (`mindcraft`) | `c93ac2c9f1cab23e12a5323bb1b451f1d745edf0` | training stack imported by muse | Apache 2.0 with an academic-use-only rider |

`run.sh` clones these at the pinned commits into `out/ext/` when a mode needs them. The riders restrict use to
academic, non-commercial research.

## Layout

```
phoenix/p23/P23-ALGOTYPES-2026-10-16/          self-sorting arrays and algotypes (exploratory audit, authors' code)
phoenix/p23/P23-AGING-2026-10-16/              stale vs lost memory in the ageing NCA (frozen)
phoenix/p23/P23-AGING-CRR-2026-10-16/          CRR repair timing and content (frozen)
phoenix/p23/P23-AGING-COMPETENCY-2026-10-16/   competency, senescence, critical lesion, early warning (frozen)
phoenix/mp-rebus/MP-REBUS-PLATONIC-CHECKS-2026-10-14/   C1-C8 checks: information length, planarian kernels,
                                               the C3 Platonic-library fork, REBUS kernel, sorting battery
phoenix/forms, phoenix/bio_cog, phoenix/origin_of_life, ashes/   earlier checks (still cited on the page)
records/                                       notes the page quotes (verbatim copies)
expected/                                      committed outputs of the earlier checks, and chart_data.json
chart_data.py, compare.py, run.sh, requirements.txt
```

Each P23 study folder has its own `README.md` (how it was run), `PREREG.md` and `FREEZE.sha256` (frozen studies),
`REPORT.md` and `results/`. Raw per-lifetime and per-swap runs (about 3 GB and 450 MB) were never committed; every
run is seeded and regenerates them.

## Commands and runtimes

```
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
./run.sh quick      # about 4 min
./run.sh sorting    # about 20 min
NCA_PYTHON=/path/to/py311-with-torch/bin/python ./run.sh ageing   # about 10 min on 3 cores after setup
```

| script | what it does | runtime (1 CPU) | compared with |
|---|---|---|---|
| `phoenix/p23/P23-ALGOTYPES-2026-10-16/dg_analyze.py` | delayed-gratification summary from the committed per-run results: official statistic, corrected statistic, strategy-free null | 6 s | `results/dg_analysis.json` |
| `phoenix/p23/P23-ALGOTYPES-2026-10-16/crr_history.py` | M7 "same present, different past" injury check in the seeded simulator (`sim.py`) | 32 s (SI), 40 s (BS) | `results/crr_history/crr_{BS,SI}_w20.json` |
| `phoenix/p23/P23-AGING-CRR-2026-10-16/crr_repair.py` + `analyze_crr.py` | repair arms in the authors' ageing NCA; frozen paired-contrast rule | about 8 s per lifetime (50 lifetimes x 3 arms in about 7 min on 3 cores) | `results/test_n015.json` |
| `phoenix/mp-rebus/.../checks/c1`–`c5` | information length; planarian kernels; precedence-library fork; REBUS kernel; sorting surplus (first run) | 0.5 s, 26 s, 65 s, 3 s, 2 s | `outputs/c*.json`, `outputs/c*.txt` |
| `.../checks/c5b`, `c6b`, `c8` | sorting surplus on the paper's rules; state-sufficiency; scheduling stickiness | about 13 min, 3.7 min, 48 s | same |
| `.../checks/c6`, `c7` | full sorting battery (26 min); the authors' threaded bubble code (52 min, needs cell_research) | not re-run here | — |
| `chart_data.py` | picks the numbers for the four charts out of the committed P23 results | < 1 s | `expected/chart_data.json` |
| earlier checks (`ashes/…`, `phoenix/forms`, `bio_cog`, `origin_of_life`) | see `levin.html`, "Where CRR led to the standard mathematics" | about 1.5 min | `expected/` |

Every script that runs the authors' code is called with `python -I` and gets the clone's path as an argument, as the
studies did.

**Ageing environment.** The pinned `mindcraft` uses `numpy.product`, removed in numpy 2, so the ageing runs need
Python 3.11 with numpy 1.26.4 and torch 2.4.1 (CPU), plus PyYAML, h5py, pandas, matplotlib, argh, gymnasium, scipy,
cma 3.3.0, neat-python 0.92, networkx, numba, scikit-learn, scikit-image, pydot. The study README lists the first
group; `neat-python` must be 0.92 (later versions drop `neat.six_util`), and `numba`, `scikit-learn`,
`scikit-image` and `pydot` are imported by the pinned `mindcraft` and `musepy`. `crr_repair.py` changes directory
into the authors' example folder, so pass an absolute `--out` path.

## Re-run results (17 October 2026, this machine: Linux x86-64, CPU only)

| what | environment | result |
|---|---|---|
| P23-AGING-CRR arms NONE, C_PRIM, S_CLOCK_TARGET, 50 frozen test seeds (1000-1049), noise 0.15 | Python 3.11, numpy 1.26.4, torch 2.4.1+cpu | **identical** to `results/test_n015.json` in every stored field (late 196.31779…, 211.61903…, 226.53189…; all-intact share 0.2121, 0.8460, 0.9985; writes 0, 130.04, 50.42); the C_PRIM − NONE contrast (+15.30 [+13.48, +17.15]) is identical too. About 7 min on 3 cores |
| P23-ALGOTYPES `crr_history.py`, BS and SI, 20-cell window, 50 seeds | Python 3.13, numpy 2.5.4 | byte-identical |
| P23-ALGOTYPES `dg_analyze.py` | same | byte-identical |
| MP-REBUS C1, C2, C3, C4, C5, C6b, C8 | same | byte-identical (`.json` and `.txt`) |
| MP-REBUS C5b | same | byte-identical (10.5 min) |
| `chart_data.py` | same | byte-identical |
| earlier checks | same | three byte-identical; `bio_cog_challenges_output.json` equal except two numbers in the 16th significant digit (relative 2.2e-16) |

Not re-run here: the official-class sorting runs (`run_official.py`, `dg_official.py`, `official_injury.py`;
threaded, so they repeat only in distribution), MP-REBUS C6 and C7, the P23-AGING and P23-AGING-COMPETENCY drivers,
and the other ten P23-AGING-CRR arms. Their committed results are what the page reports.

## Excluded

- The consolidation zip `P23_LEVIN_FINDINGS_2026-10-16.zip` (its content is the folders above).
- `notebook/PROMPT_LOG.md`, agent manifests, receipts and anchoring files (they contain local paths and session
  material, and none is needed to re-run anything).
- MP-REBUS `outputs/c7_authors_code_run.json`, `c7_authors_code_run_poll005.json` and `c7_authors_code_smoke.json`:
  each records the session's local clone path. Their numbers are in `RESULT.md` and `outputs/c7_run*.log`.
- `REPORT/SORTING_ARRAYS_REPORT_2026-10-14.pdf` (a 0.5 MB rendering of the Markdown report kept here).
- The third-party code (licences above).

## Licence

Code written for this folder and the Phoenix/Ashes code: MIT. Text: CC BY 4.0. © Alexander Sabine 2026.
Third-party code fetched by `run.sh` keeps its own terms.

MIT licence: Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction, including without
limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The
above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
