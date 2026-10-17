# CRR–Phoenix–Levin: consolidated findings of the P23 line to 2026-10-16

**What this is.** The single summary that goes with `P23_LEVIN_FINDINGS_2026-10-16.zip`. The owner asked on
2026-10-16 (OD-52) for the earlier findings to be consolidated into one zip before the programme proper begins. The zip
holds copies of the five P23 study folders and the source survey, plus extracts of every record row that refers to
them. The originals stay where they are, because frozen hashes, ledger rows and commits point to those paths.

**Grade of everything below.** None of it is a Phoenix *finding* in the guardrail sense (PASS-2/S3). One study was
exploratory; three were frozen tests on one public computer model, run by one builder. The model is the authors' own,
so the results are statements about that model, not about organisms. Every frozen prediction that missed is listed.

## 1. Studies

| study | owner decision | design | ledger |
|---|---|---|---|
| `studies/P23-LEVIN-TESTBED-2026-10-07/` | owner: "keep that as Declaration" | declaration P23-LEVIN1: a wet-lab test of M7 (does a stable two-headed history change a different morphological switch?); not frozen, no run; needs a laboratory | stage ledger 2026-10-07 |
| `studies/P23-ALGOTYPES-2026-10-16/` | OD-47 | exploratory audit with the authors' code (cell_research 1fd2bd59) plus null models and one CRR check | D129 |
| `studies/P23-AGING-2026-10-16/` | OD-48 | frozen (14cbb5c; decision script cc138ae); ageing NCA of Pio-Lopez, Hartl & Levin 2025, authors' code unchanged | D130 |
| `studies/P23-AGING-CRR-2026-10-16/` | OD-49 | frozen (7fd6b14); CRR repair timing and content derived from CORE, against ordinary rivals | D131 |
| `studies/P23-AGING-COMPETENCY-2026-10-16/` | OD-50 | frozen (25ef609); CRR used as a question generator for the paper's "loss of goal-directedness" claim | D132 |
| `SOURCES/LEVIN_LAB_2026-10-16.md` | OD-51 | survey of the lab's 2026 papers, preprints, public data and code | — |

## 2. What was learned

### Self-sorting arrays and algotypes (Zhang, Goldstein & Levin, arXiv:2401.05375)

1. Chimeric aggregation is real, but its peaks are 0.04–0.15 below the paper's.
   - The paper's negative control matches the mean of each run's maximum, not the peak of the mean curve.
2. A tempo difference alone, with an identical rule and inert labels, gives the same transient clustering.
3. There is no 0.69 setpoint: the final segregation runs from 0.44 to 0.78. The persistence comes from stable versus
   non-stable sorting.
4. "Delayed gratification" is a property of the progress measure. The official statistic returns a sum instead of a
   mean in exactly the frozen-cell runs. Once corrected, there is no trend, and a strategy-free null matches.
5. **M7 check.** Two arrays identical in every visible value repair an injury completely differently depending on
   their history: history copies 0/50, fresh 50/50.
   - The whole effect sits in stale stored state: selection pointers that only advance.
   - Renewing the pointers locally repairs as well as rebuilding.
   - An ordinary hidden-state (Markov) model accounts for all of it.

### The ageing NCA (Pio-Lopez, Hartl & Levin 2025, Adv. Sci. e09872)

6. The cells' recurrent memory is rebuilt from current input every step. Stale memory cannot block repair here:
   keeping it equals clearing it (5/5).
7. A lost eye and a never-formed eye converge (48/50 lifetimes; median 38.5 steps). The paper's injection favours the
   just-lost eye only at the moment of loss (12/50 vs 0/50), and not after any delay of 10 steps or more.
8. Ageing needs noise: there is no decline at noise ≤ 0.025, and decline rises with noise (ρ = 0.93).
9. The paper's targeted repair reproduces (+15.3 [13.5, 17.1]).
10. **CRR-derived repair did not earn credit.**
    - Cut timing equals a matched clock and is slightly below an ordinary early trigger.
    - The past-weighted seed is worse than the paper's reset; fitness rises all the way to q = 1, which is the paper's
      method.
11. **What the CRR-guided search found anyway (ordinary improvements).**
    - Frequent early repair gives +10.8 over the paper's threshold.
    - Writing the canonical mature organ state gives +3.0 over the primordial state.
    - Combined, they reach the noise-free level (≈ 226).
12. **Competence does not decline with age.**
    - Repair of a given injury is equal at every age (eye-centre cell 61/63 young vs 34/36 mature).
    - There is no senescence: the hazard does not rise with age (−0.06 [−0.28, +0.17] per 1,000 steps).
13. Organ loss is a first passage past a critical lesion of one to two cells (48, 88, 96 and 100% for 1–4 cells).
    Losses do not cascade. Repair at the first wrong cell is best (+8.0 over k = 3).
14. CRR's Fisher–Rao coherence gives no early warning beyond the damage already present (−0.0008). That frozen
    prediction missed.

### The lab's 2026 programme (survey)

15. Seven themes. The one that meets Phoenix's commitment M7 is **history carried through regeneration or training**:
    - planarian memory surviving head regeneration;
    - regeneration history shaping BaCl₂ responses (GSE341203);
    - Xenobot memories (GSE320387);
    - ion-exposure history in nuclear-membrane voltage.

## 3. Frozen predictions missed (recorded before interpretation)

- **P23-AGING Q2.** The largest memory difference one step after a full wipe was 13% (predicted < 10%; the mean was 1%).
- **P23-AGING-COMPETENCY Q4.** CRR coherence was predicted to add a small early-warning gain; it added none.
- **P23-AGING-CRR.** CRR timing and content earned no credit. These were the frozen tests of CRR's operations, not
  predictions in CRR's favour.

## 4. What CRR contributed (heuristic ledger D129–D132)

| contribution | grade |
|---|---|
| The "same present, different past" design (M7) | **QUESTION/DESIGN** |
| Separating capacity to regenerate from the hazard of an unregenerable rupture | **DISTINCTION** |
| Cut as first passage, which led to the critical-lesion experiments | **QUESTION** |
| Cut and past-weighted regeneration as mechanisms | **NOTHING** |
| Recency weighting of the seed | mildly **MISLED** |
| Coherence as an early-warning measure | **NOTHING** |

No result moves ND-2: whether forms are produced by history or ingressed from a latent space stays NOT DECIDABLE.

## 5. Open questions carried into the programme

- **Real data, not a model.** Every frozen result so far is about one computer model. The programme's first study
  moves "same present, different past" to the lab's own public data (GSE341203, planarian regeneration history).
- **Re-evolve the smiley agent with a maintenance reward** (P23-AGING-COMPETENCY's next experiment). This tests
  whether the one-to-two-cell fragility belongs to what was selected for. It needs the authors' training stack and GPU
  time, so it is deferred.
- **The declaration P23-LEVIN1 still needs a laboratory partner.**
