# P18B-LAGGED-PROVENANCE — pre-freeze pilot (NO-GO)

**Source.** Phoenix `Phoenix_Egg/studies/P18B-LAGGED-PROVENANCE-2026-10-09/` (with its two read-only dependencies
`studies/P18-LOOP1-2026-10-08/loopworld.py` and `studies/P18-PROV-FLAME-2026-10-09/`), at commit
`1295af24e82e0502a6bd284cd021149d4891eb5b`.

**Status: a development pilot. Nothing is frozen, hashed or anchored; no held-out world exists; no ledger row**
(`DESIGN.md:3-5`, `PILOT.md:303`). It is included because its decision was NO-GO and the record keeps failures.

## Question

Can a lagged-response test that uses the agent's own publication record (which of its published outputs re-entered
its inputs, and with what lag) detect and attribute a gamed feedback channel, with controls that must pass and must
fail? The pilot checks, before any freeze, whether the design's controls behave (DESIGN.md §6.4, §8.3).

## What CRR suggested / established comparator

The provenance reading of P17/P18 ("which of my outputs re-entered my inputs"; see [P18-LOOP1](../P18-LOOP1)). Rivals in
the design: passive and intervention randomisation tests (`passive_ri`, `intervention_ri`), BBSD/MO-BBSD shift
detectors, projection and jump statistics (`DESIGN.md`).

## Decision (as recorded)

**NO-GO** — `PILOT.md:3` "**Decision under the design's rules (§8.3): NO-GO.** Nothing is frozen." and `PILOT.md:175`.
The failing item (`PILOT.md:6`, `:314`): **MP5 (positive control C1)**: in `pos_e`, passive_ri's sensitivity was
94/150 = **0.627** (Wilson 95 % 0.547–0.700) against a registered threshold ≥ 0.80. MP1–MP10: 9 of 10 pass; MF1–MF5
all pass (`PILOT.md:173-174`). No fix has been made; any fix is an owner decision (`PILOT.md:305`).

## Data and effort

* Synthetic, development world seeds 340000–346149 (pilot), 390000–396003 (tiny), 398000–398099 (mp10). No download.
* **tiny: Easy** (~2 CPU-min; code paths only, "its numbers mean nothing"). **pilot: Moderate** — 6000 simulations,
  0.876 CPU-hours over 4 workers (`PILOT.md:79`). numpy only; version not recorded upstream.

## Commands

```bash
bash run.sh            # tiny (default), compare outputs/pilot_tiny_public.json field by field
bash run.sh pilot      # the full pilot (4 workers), then `verify` of the new commitment, compare outputs/pilot_public.json
bash run.sh mp10       # the MP10 check, compare outputs/mp10_check.json
```

Original commands (`PILOT.md:24,27`):
`nice -n 19 env OMP_NUM_THREADS=1 python3 -I pilot_p18b.py pilot --sealed-dir <dir outside repo> --workers 4`, then
`python3 -I pilot_p18b.py verify --sealed-dir <same>`.

## Expected outputs and how to compare

`expected/` holds the committed public outputs (`pilot_public.json`, `pilot_tiny_public.json`, `mp10_check.json`,
`power_plan.json`, surrogate/equivalence/access/timing checks). `compare_public.py` (written for this folder) compares a
re-run's public JSON with the committed one field by field and skips only `commitment`, `runtime`, `date_utc` and
`cpu_s_*`/`wall_s_*` fields.

## What cannot be reproduced

* **The commitment hash.** The pilot seals its primary estimates and publishes only `sha256(salt + '|' + payload)`.
  The salt and sealed estimates were written to an operator directory outside the repository and **never committed**;
  every new run draws a fresh random salt (`secrets.token_hex`), so a re-run's commitment cannot equal the recorded one.
  The D values, controls and GO flag can be compared.
* `--sealed-dir` must lie outside `dirname(WORK)` (the script refuses otherwise); `run.sh` uses a fresh `mktemp -d`.
* The pilot compares some in-process checks with the committed files in its own `outputs/` folder, so `run.sh`
  copies `expected/*.json` there first.

## Verified re-run on 2026-10-17

`bash run.sh tiny` (python 3.11.17, numpy 2.4.6, 1 worker): ~2 min. `pilot_tiny_public.json` **matches** the
committed file on all 453 compared fields (0 differ; skipped by design: commitment, runtime, date_utc, cpu_s_*). The
full 6000-simulation pilot and `mp10` were **not** re-run here.
