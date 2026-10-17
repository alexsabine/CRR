# P18-LOOP1 — provenance localisation in a performative feedback loop (DEVELOPMENT ONLY)

**Source.** Phoenix `Phoenix_Egg/studies/P18-LOOP1-2026-10-08/` (`loopworld.py`, `loop_contrasts.py`, `README.md`,
`outputs/`), at commit `1295af24e82e0502a6bd284cd021149d4891eb5b`.

**Status: development only — no preregistration, no hash, no anchor, no ledger row.** "Development only: synthetic
worlds, no preregistration, no ledger rows" (`src/studies/P18-LOOP1-2026-10-08/README.md:3`). Nothing here is a
preregistered test; it is the harness that later designs (P18B) build on.

## Question

An agent refits a logistic classifier each round and publishes its outputs (θ, and in some worlds an "explanation" e
= its top-2 coefficients). Applicants game one feature along the published output, so the proxy label drifts from the
true target. Can a **provenance** statistic — the input shift projected on every output the agent has published ("which
of my outputs re-entered my inputs") — detect the divergence and name the gamed channel, including when a larger
exogenous change sits in another channel?

## What CRR suggested

The Empty Centre's operational rule: track which of the agent's own outputs re-enter its inputs
(`HEURISTIC/EMPTY_CENTRE.md` §3 in Phoenix).

## Established comparators

Proxy-accuracy and calibration (ECE) monitors, a generic input-drift detector, black-box shift detection on the model's
own score (BBSD; Lipton et al. 2018, Rabanser et al. 2019), an event log, and the **native causal rival**: six rounds of
randomised sign flips of the published output (an intervention).

## Result (as recorded; development)

Localisation accuracy, `src/studies/P18-LOOP1-2026-10-08/README.md:94-97` (also `expected/loop_summary.json`):

| world | event log | provenance | intervention | shuffled | none |
|---|---|---|---|---|---|
| game_theta | 1.00 | 1.00 | 0.975 | 0.46 | 0.095 |
| game_expl | 1.00 | 1.00 | 0.98 | 0.475 | 0.095 |
| game_theta+exo | 0.32 | **0.96** | 0.975 | 0.385 | 0.095 |
| game_expl+exo | 0.645 | **0.985** | 0.98 | 0.40 | 0.095 |

"It names the gamed channel 0.96–0.985 of the time, where the event log is misled to 0.32–0.645. **But the native causal
rival does as well.** Six rounds of randomised sign flips of the published output localise at 0.975–0.98"
(`README.md:106-107`). In clean worlds provenance adds nothing over a generic drift detector, and it cannot tell
re-entry from exogenous change that projects on its outputs (`README.md:102-103`).

## Data and effort

* Synthetic: 200 calibration seeds (10000+) and 200 test seeds per world, 6 worlds. No download.
* CPU, numpy only (version not recorded upstream; numpy 2.4.6 pinned here). Recorded "about 20 CPU-minutes"
  (`README.md:11`). **Easy.**

## Commands

```bash
bash run.sh            # full size, as recorded: loopworld.py 200 200, then loop_contrasts.py; compare all outputs
bash run.sh quick      # 200 calibration seeds, 40 test seeds per world; each produced row is compared with the committed row
```

Original: `python3 -I loopworld.py 200 200` then `python3 -I loop_contrasts.py`, from the study folder (outputs go to
`outputs/`). `compare_rows.py` (written for this folder) checks a reduced run row by row: with 200 calibration seeds
the detector thresholds are the same, and test seed *s* of world *w* is simulated identically whatever the test count.

## Expected outputs

`expected/loop_runs.jsonl` (one row per world and seed), `loop_summary.json`, `loop_contrasts.json` (paired bootstrap,
B = 4000, `default_rng(0)`), `loop_log.txt` (stdout). These were force-added upstream although `studies/*/outputs/` is
git-ignored in Phoenix.

## Verified re-run on 2026-10-17

`bash run.sh` (full size; python 3.11.17, numpy 2.4.6): `loopworld.py 200 200` took 25 min 40 s wall (24.5 CPU-min).
All 1200 rows equal the committed rows; `loop_runs.jsonl`, `loop_summary.json` and `loop_contrasts.json` **match** byte for
byte. (`quick` mode was not run separately; it uses the same row comparison.)
