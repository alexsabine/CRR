# P23-AGING-COMPETENCY (2026-10-16): using CRR's rupture–regeneration framing to develop Levin's ageing model

Start with `REPORT.md`. The protocol is `PREREG.md`, frozen at commit 25ef609 (hashes in `FREEZE.sha256`) before any
test seed; it also records the development observations (seeds 3000–3049). The model is the ageing NCA of
Pio-Lopez, Hartl & Levin (2025, Adv. Sci. e09872), with the authors' code unchanged (github.com/bhartl/muse
@ 9404ec3, mindcraft @ c93ac2c9); the environment is as in `../P23-AGING-2026-10-16/README.md`.

**Scripts.**
- `levin_checks.py` has three modes:
  - `lifecourse`: long unrepaired lifetimes, saving organ-cell states every step;
  - `competency`: a standard injury at a chosen age, compared with the same-seed uninjured lifetime (identical
    noise); fixed cells, k random eye cells, or any single cell;
  - `kthresh`: repair an organ as soon as it has ≥ k wrong cells.
- `analyze_lifecourse.py`: discrete-time hazard of organ loss against age (Q1) and against other organs lost (Q3);
  early warning of organ loss (Q4): CRR coherence, variance, autocorrelation, margin and damage, with
  cross-validated AUC gains.
- `analyze_competency.py`: repair rate by age (Q2).
- `analyze_q2b_q5.py`: lesion size and position (Q2b, Q2c); lesion-size-triggered repair (Q5).
- `results/`: development (`results/dev/`) and test analyses.

CPU only, no API use. Raw lifetimes are not committed; every run is seeded and deterministic.
