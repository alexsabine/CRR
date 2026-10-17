# P23-AGING preregistration (OD-48, 2026-10-16): stale versus lost memory in the ageing NCA

Frozen before any test seed is run. Development used seeds 0–9 only (`dev/` results summarised in REPORT §2).
Code: `aging_checks.py`, `analyze_aging.py`, `analyze_history.py` at the freeze commit; authors' code unchanged:
bhartl/muse @ 9404ec3, bhartl/NeurEvo (mindcraft) @ c93ac2c9, pretrained agent `agents/smiley_16x16`.

**Subject.** Pio-Lopez, Hartl & Levin (2025), *Aging as a Loss of Goal-Directedness*, Adv. Sci. e09872. Claims under
check: (C1) ageing emerges "even without noise"; (C4) "despite organ loss, spatial information persists in tissue,
implementing a memory of lost structures, which can be reactivated for organ restoration"; (C5) targeted
regenerative information rejuvenates. Plus the question carried from P23-ALGOTYPES: does stale stored memory block
repair (lost memory versus stale memory)?

**Settings** (the published notebooks' defaults): noise 0.15, competency 1.0, 1,000 steps, recovery threshold 0.6,
development 150, horizon 25. Sensitivity: noise 0.125 (the paper's stated value) for Q1 and Q2.

## Questions, arms, endpoints, decision rules

**Q1 — stale memory in repair.** Arms A_RESET vs A_KEEP and B_RESET vs B_KEEP (organ masks), and B_RESET vs B_KEEP
with sockets. Seeds 1000–1049 (n = 50, paired). Endpoint: mean fitness over steps 150–1000 per lifetime.
Rule: paired mean difference with 95% bootstrap CI (10,000 resamples, seed 0). **Equivalent** if the CI lies within
±2 fitness units (under 1% of 256); **different** if it excludes 0 and |mean| ≥ 2; otherwise **undetermined**.
Development prediction: equivalent.

**Q2 — how long the cells' RNN memory carries information.** Arms PERTURB_RNN and PERTURB_HIDDEN at step 300 vs
NONE, seeds 1000–1019 (n = 20), noise 0.15 and 0.125, `--save_states`. Endpoints: share of cells whose expressed type
differs from the unperturbed run at steps 310, 400 and 1000; largest memory difference one step after the wipe.
Prediction: RNN wipe leaves type differences ≤ 0.5% of cells at every endpoint and the memory difference at step 301
is under 10% of the wiped values' typical size (|m| ≈ 0.28); the hidden-channel wipe is reported descriptively.

**Q3 — memory of the lost structure (same present, different past).** Arms LOST_NOINJ, NEVER_NOINJ, LOST_INJ,
NEVER_INJ (left eye, T = 300), seeds 1000–1049 (n = 50), `--save_states`, 600 steps; replication at T = 600 with
900 steps, seeds 1000–1029. Endpoints: (a) share of seeds in which the full state difference between LOST and NEVER
falls below 0.01 and stays below to the end, and the median number of steps it takes; (b) spontaneous regrowth (left-
eye score ≥ 0.6 at T + 50) in the NOINJ arms; (c) regrowth after injection at T + 50 and mean eye score over
T + 1…T + 100, LOST_INJ against NEVER_INJ (exact McNemar on regrowth; paired Wilcoxon on the score).
Reading fixed in advance: if (a) converges in ≥ 90% of seeds, the tissue keeps no lasting trace of whether the eye
ever existed, so the paper's "memory of lost structures" is not information about the lost structure in this agent;
a LOST advantage in (c) is read as a short-lived effect of the surrounding tissue, bounded by the convergence time.

**Q4 — ageing without noise (C1).** Arm NONE at noise 0, 0.025, 0.05, 0.075, 0.1, 0.125, 0.15, 0.2; seeds 2000–2019
(n = 20; noise 0 is deterministic, so one distinct lifetime). Endpoints: fitness at step 1000 minus fitness at step
150 (decline), and the number of organs (of 3) below score 0.6 at step 1000. Prediction: at noise 0 no decline after
step 150 and no organ lost; decline increases with noise (Spearman over levels, one value per seed).

**Q5 — the paper's repair result reproduces (C5).** Seeds 1000–1049: B_RESET vs NONE and A_RESET vs NONE on the Q1
endpoint, same rule; prediction from the paper and development: B better than NONE (CI excludes 0, mean ≥ 2),
A within ±5 of NONE. MEM_ORGAN vs NONE: memory-only repair, prediction equivalent.

**Multiplicity.** Five questions, each with its own fixed rule; no correction across questions; all results reported.
**Exclusions.** None; a crashed lifetime is rerun once with the same seed and the rerun is reported.
**Departures** after the freeze are recorded in REPORT §Departures with reasons.
