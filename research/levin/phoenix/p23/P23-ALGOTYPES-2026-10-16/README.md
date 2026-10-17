# P23-ALGOTYPES (2026-10-16): CRR checks on Zhang, Goldstein & Levin's self-sorting arrays and algotypes

Start with `REPORT.md`. This is an exploratory audit (OD-47): a reproduction with the authors' own code, null models
and one CRR-explicit check. Nothing here was preregistered or frozen, so no result is a Phoenix finding. The
results are graded as reproduction, reduction or failure (see the report, §8).

**Sources.**
- Paper: Zhang T., Goldstein A., Levin M., *Classical sorting algorithms as a model of morphogenesis: self-sorting
  arrays reveal unexpected competencies in a minimal model of basal intelligence*, arXiv:2401.05375 (Adaptive
  Behavior). Local PDF sha256 `f4e78ddc…098ca`.
- Official code: github.com/Zhangtaining/cell_research, commit `1fd2bd59`, used unchanged.
- Independent replication consulted for prior art: github.com/alexbaker0/Self-sorting-cells, commit `3ebc155`.

**Scripts.** Every script that reads downloaded code runs it with `python -I` from a separate directory and passes
the clone's path as an argument.
- `run_official.py`: chimeric-array runs with the official cell classes (one group, all threads under one lock), with
  inert-label controls (BB, SS, II, BBB) and duplicated values. Saves per-swap type and value snapshots (`.npz`).
- `analyze_runs.py`: the official aggregation curve. It gives the peak of the mean curve with a bootstrap interval,
  the final value, the excess over the matched inert control and a Welch t.
- `peak_stats.py`: maximum of the mean curve compared with the mean of each run's own maximum.
- `sim.py`: a fast, seeded re-implementation of the three cell rules. With `burst=-1` it uses round-robin
  scheduling, which reproduces the official swap counts. `run_sim.py` runs it in batches in the same file format.
- `tie_blocks.py`: where each algotype sits inside final blocks of equal values.
- `dg_official.py`: delayed gratification with the official cells. It computes the official DG statistic
  (extracted unchanged by `ast`) and a copy with one correction, checks inversions after every step, and runs a
  strategy-free null. `dg_analyze.py` summarises the output.
- `crr_history.py`: the same-form, different-history check (commitment M7) in the simulator. It has three copies:
  HISTORY (pointers as sorting left them), FRESH (pointers new) and LOCAL (pointers renewed only inside the
  injured window). `crr_mechanism.py` counts pointers after sorting, after the injury and at the repair cap.
  `official_injury.py` runs the same check with the official classes.
- `results/`: every analysis output cited in the report.

**Reproduce** (OFFICIAL = the cell_research clone at 1fd2bd59, R = a run directory):

```bash
python3 -I run_official.py OFFICIAL R/official --mix BS --n 100 --exps 100        # also BI SI BSI BB SS II; BBB
python3 -I run_official.py OFFICIAL R/official --mix BS --n 100 --dup 10 --exps 100
python3 analyze_runs.py R/official results/official_analysis.json
python3 run_sim.py R/rr_uniq --mix BS --exps 200 --burst -1 --tag rr              # chimeric mixes and controls
python3 run_sim.py R/rr_speed --mix BB --exps 200 --burst -1 --tag rr-x16 --label_rates 0:1,9:16   # speed null
python3 run_sim.py R/rr_setpoint --mix BS --dup 10 --exps 200 --burst -1 --tag rr                  # setpoint sweep
python3 tie_blocks.py R/rr_setpoint BS_dup10-rr SI_dup10-rr BI_dup10-rr BB_dup10-rr
python3 -I dg_official.py OFFICIAL results/dg_bubble.json --kind bubble --frozen 0,1,2,3,4,5 --exps 100
python3 dg_analyze.py results/dg_analysis.json results/dg_bubble.json results/dg_insertion_*.json
python3 crr_history.py results/crr_BS_w20.json --mix BS --seeds 50 --k 3 --window 20 --max_ticks 400000
python3 -I official_injury.py OFFICIAL results/official_injury_BS.json --mix BS --exps 20 --window 20 --timeout 30
```

Environment: Python 3.13 with numpy. The official code imports only the standard library in the classes used.
CPU only; no API calls. The raw per-swap runs (about 450 MB) are not committed. They are regenerated
deterministically by the simulator. The official runs are regenerated up to thread scheduling: each run is seeded,
but the interleaving of threads is not.
