# P23-AGING-CRR preregistration (OD-49, 2026-10-16)

Frozen before any test seed. Design and derivation: `DESIGN.md` (§1–2), calibration on development seeds 0–9 (§3).
Code: `crr_repair.py`, `analyze_crr.py` at the freeze commit; authors' code unchanged (bhartl/muse 9404ec3,
NeurEvo c93ac2c9). Frozen parameters: a = π, q = 0.99, Δ = 21, 18, 10 (left eye, right eye, mouth), S_ANY H = 15,
noise 0.15, competency 1.0, 1,000 steps; paper trigger threshold 0.6, development 150, horizon 25.

**Test seeds 1000–1049** (n = 50, paired) for the arms NONE, C_PRIM, C_TARGET, C_CKPT, C_CRR, C_EMACLOCK, S_CRR,
S_CLOCK, S_ANY, S_IMMEDIATE, S_CRRFULL, S_CRR_TARGET and S_CLOCK_TARGET.

**Sensitivity at noise 0.125** (same seeds) for C_PRIM, C_CRR, S_CRR, S_CLOCK and S_ANY. Δ for S_CLOCK at 0.125 is
fixed by rule from the 0.125 S_CRR test run: Δ_organ = round(850 / mean cuts after step 150), computed before
S_CLOCK runs.

**Endpoint.** Mean fitness over steps 150–1000.
**Rule** (`analyze_crr.py`): 95% bootstrap CI of the paired mean difference (10,000 resamples, seed 0).
- **equivalent** if the CI lies within ±2;
- **different** if the CI excludes 0 and |mean| ≥ 2;
- **undetermined** otherwise.

Cost (cell writes) is reported for every arm.

| id | contrast | question | prediction from calibration |
|---|---|---|---|
| P1 | S_CRR vs S_CLOCK | does CRR cut timing beat a clock at the same rate? | equivalent |
| P2 | S_CRR vs S_ANY | does it beat an early damage trigger with as many repairs? | not better (equivalent or undetermined) |
| P3 | C_CRR vs C_PRIM | does CRR's past-weighted content beat the paper's primordial reset? | not better |
| P4 | C_CRR vs C_EMACLOCK | does cut sampling of the content matter? | equivalent |
| P5 | S_CRR vs C_PRIM | does repairing at CRR cuts beat the paper's damage threshold? | different, positive |

**CRR earns credit only if** P1 or P2 comes out "different" with S_CRR ahead (cut timing beats ordinary timing at
matched rate), or P3 comes out "different" with C_CRR ahead (past-weighted content beats ordinary content). P5 alone
does not credit CRR: an early or frequent ordinary trigger may give the same gain (P2).

**Secondary, reported without a verdict.** C_TARGET vs C_PRIM; S_CRR_TARGET vs S_CLOCK_TARGET; S_CRRFULL vs S_CRR;
C_CKPT vs C_PRIM; the cost of S_CRR against S_ANY and S_IMMEDIATE.

No correction across contrasts; all are reported. A crashed lifetime is rerun once with the same seed. Departures
are recorded in REPORT.md.
