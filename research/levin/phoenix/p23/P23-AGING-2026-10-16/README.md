# P23-AGING (2026-10-16): stale versus lost memory in Levin's team's ageing model

Start with `REPORT.md`. Protocol `PREREG.md`, frozen at commit 14cbb5c (hashes in `FREEZE.sha256`) before any test
seed ran; `decide.py` (commit cc138ae, also before the test) applies its rules.

**Subject.** Pio-Lopez, Hartl & Levin (2025), *Aging as a Loss of Goal-Directedness: An Evolutionary Simulation and
Analysis Unifying Regeneration with Anatomical Rejuvenation*, Adv. Sci. 12(46) e09872, doi 10.1002/advs.202509872.
The paper's data statement says data are available on request and gives no code link. The code is public in the
co-author's repository: github.com/bhartl/muse @ 9404ec3, `examples/aging-as-loss-of-goal-directedness/`
(pretrained `smiley_16x16` agent, `aging.py`, `recovery.py`, three notebooks), with the training stack
github.com/bhartl/NeurEvo (`mindcraft`) @ c93ac2c9. Both are used unchanged.

**Scripts.**
- `aging_checks.py` runs one arm over a seed range. Each lifetime is a fresh, seeded world, so arms are paired by
  seed. The published repair runs through the authors' own `recovery.set_initial_state`, with one switch changed
  per arm. The arms are:
  - repair with memory cleared or kept;
  - memory-only repair;
  - wiping all memory, or the hidden channel, at one step;
  - the history test (left eye lost at step T, or never formed), with and without the paper's regenerative injection.
- `analyze_aging.py`: per-arm summary and paired comparisons.
- `analyze_history.py`: state and memory divergence between paired arms (convergence time).
- `decide.py`: the frozen decision rules.
- `analyze_delay.py`: exploratory, after the test. It covers the injection delay after loss; the repeated-repair
  history arms (`--arm LOST_B/NEVER_B --delay d`) are summarised in `results/explore_repeated_repair.json`.
- `results/`: all analysis outputs, development (`results/dev/`) and test.

**Environment.** Python 3.11 venv with numpy 1.26 and torch 2.4.1 (CPU), plus PyYAML, h5py, pandas, matplotlib,
argh, gymnasium, scipy, cma 3.3, neat-python, networkx, ipywidgets. The pinned mindcraft uses `numpy.product`, which
numpy 2 removed; the code was not edited. Run from any directory:

```bash
python -I aging_checks.py --muse MUSE --mindcraft NEUREVO --arm B_RESET --seeds 1000:1050 --out organ_B_RESET.npz
python -I aging_checks.py --muse MUSE --mindcraft NEUREVO --arm LOST_NOINJ --T 300 --steps 600 --save_states \
       --seeds 1000:1050 --out hist_LOST_NOINJ.npz
python3 decide.py results/decisions.json TEST_DIR
```

CPU only, no API use. Raw lifetimes (about 3 GB with saved states) are not committed. Every run is seeded and
deterministic (verified: identical seeds reproduce identical trajectories).
