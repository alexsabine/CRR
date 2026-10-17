# P23-XMEM result (OD-52; frozen run 2026-10-17T00:12Z): Xenobot stimulus memory, residue or rewrite?

**Machine verdict (R15, printed by the frozen scorer before this text was written):**
- H1 NOT DETECTED;
- H2 NOT DECIDABLE (H1 not present);
- H3 NOT DECIDABLE;
- H4 NOT DECIDABLE (H1 not present);
- H2a NO ALIGNMENT DETECTED.

The two reruns are byte-identical (`outcomes.json` = `rerun_a.json` = `rerun_b.json`). All eight sensitivity cells give
the same verdicts.

## 1. Failures first

- **P1 (the authors' claim) missed.**
  - In the 12 unseen stimulus samples of GSE320387, a stimulus-specific transcriptional difference 4 h after a brief
    exposure to embryo extract versus ATP (E4 − A4, batch-paired) is **not detected**.
  - The rotation test of the mean squared moderated t gives p = 0.2447 (9,999 rotations). Across the sensitivity cells
    p ranges from 0.22 to 0.26.
  - No gene reaches BH 5% for E4 − A4, paired or unpaired. Neither does any gene for the immediate contrast E0 − A0.
- **P2 and the CRR §V prediction were not reached.** H2 is NOT DECIDABLE by the frozen rule, because H1 is not present.
  The registered CRR mapping is therefore **NOT DECIDABLE**. The residue-versus-rewrite question cannot be asked of
  these data.
- **Power caveat, fixed before the data (`power.json`).**
  - H1 has power ≥ 0.8 only for a large, consistent 4 h programme: about 1,500 genes at σ = 0.7 log₂ with full
    persistence, or σ = 1.5.
  - Power is 0.07–0.17 for 300 genes at σ = 0.7.
  - The null result therefore rules out a large stimulus-specific transcriptional state at 4 h in these samples. It
    does not rule out a small one.

## 2. Numbers (from `outcomes.json`)

| quantity | value |
|---|---|
| genes after the frozen filter (12 samples) | 23,908 of 42,638 |
| TMM factors | 0.79–1.16 |
| residual df / prior df | 6 / 5.01 |
| H1 rotation p (E4 − A4) | 0.2447 |
| H2a alignment p (two-sided) | 0.4531 (statistic +0.466) |
| cross-batch energies S00 / S44 / S40 | 0.622 / 0.294 / 0.321 |
| ρ (full); leave-one-batch-out ρ | 0.75; 1.64, −0.16, 0.94 |
| DE at BH 5%: E4 − A4 / E0 − A0 (paired and unpaired) | 0 / 0 |
| Fisher–Rao distance, mean between replicates of one condition | 0.414 |
| Fisher–Rao distance between condition centroids | 0.14 (E0–E4) to 0.32 (E4–A0) |
| Fisher–Rao carrier S44 | −6.9 × 10⁻⁹, so ρ is undefined |

**Reading.** The cross-batch energies are positive overall, but the leave-one-batch-out estimates disagree in sign. The
stimulus differences are smaller than the differences between replicate experiments. Replicate-to-replicate (batch)
variation dominates these transcriptomes.

## 3. Exploratory analyses (after the verdict; labelled; not confirmatory)

`exploratory/explore_posthoc.py` produces `exploratory/posthoc_results.json`. It uses all 15 columns, including the
three seen "before stimulus" (C) columns that the frozen run excluded.

1. **No contrast has individually detectable genes.** In a 15-sample batch-aware model (residual df 8), every
   contrast has at most one gene at BH 5%: E0 − C 1, A4 − C 1, all others 0. This includes "4 h after vs before",
   the comparisons closest to the authors' description. Unpaired two-group comparisons (6 samples, no batch term) also
   give 0–1. The rotation tests in the 15-sample model all have p > 0.16: E4 − A4 0.23, E0 − A0 0.16, shared 4 h
   change 0.16, shared 0 h change 0.29.
2. **Diffuse signal where it would be expected, none where the memory claim needs it.** Storey's π₀ (the estimated
   share of genes with no change) and the count of genes at raw p < 0.05 (about 1,200 expected by chance):
   - E0 − A0, immediately after: π₀ 0.74 (1,889 genes);
   - E4 − C: π₀ 0.76 (2,353);
   - shared 4 h change: π₀ 0.82;
   - **E4 − A4, the stimulus-specific 4 h difference:** π₀ 0.97 (1,403), close to no effect;
   - A4 − C: π₀ 0.96.

   So there may be a weak, diffuse **immediate** stimulus-specific difference and a weak change after 4 h for
   extract. There is little sign that the stimulus-specific difference **persists** at 4 h.
3. **The design cannot separate memory from time.** The "4 h after vs before" contrasts confound the stimulus with 4 h
   of time and handling: there is no 4 h unstimulated control. Any change seen there cannot by itself be called a
   stimulus memory. Only the time-matched Ext-vs-ATP contrast can be, and it is the one closest to null.

## 4. What this means for the authors' claim, and for CRR

- **For the paper.** Pai et al. report "distinct, long-term, stimulus-specific memories, detectable through both
  transcriptional and physiological signatures".
  - In their public counts, under a batch-paired analysis robust to gene–gene correlation, the transcriptional part
    of that claim is not supported at 4 h for Ext vs ATP. The immediate specific difference is also not individually
    detectable.
  - The authors' own analysis could not be compared: the full text was refused by bioRxiv (HTTP error 1015) on
    2026-10-16 and 2026-10-17. Their contrasts, thresholds and gene lists are unknown here. They may have used
    unadjusted p-values or contrasts against "before stimulus".
  - Nothing here bears on their behavioural or calcium-imaging results, which are not public.
- **For CRR.** NOT DECIDABLE. The study could not reach the question CRR raised. Had it reached it, a residue would have
  reduced to relaxation (no credit) and a rewrite would have failed CRR §V's content rule.
- **Heuristic ledger D133.** CRR's role was a QUESTION (residue vs rewrite in a same-present, different-past contrast).
  The answer is that this dataset is too small and too batch-dominated to pose it.

## 5. Departures and incidents (all recorded before interpretation)

1. **Three holdout records seen through the development set.** The three "before stimulus" columns were probably seen
   through GSE275807 (same sequencing run). They were excluded from the frozen run (`admissibility.md`; AGENT_LOG item
   43) and are used only in the labelled exploratory section.
2. **Frozen stdout copied afterwards.** The `tee` target directory did not exist when the run started, so the frozen
   stdout transcript (`receipts/…/run/frozen_stdout.txt`) was copied from the session output afterwards. The JSON
   outputs are the record.
3. **Receipt layout and derived bytecode.** Two receipt-format additions were needed for the numeric append route:
   - GitHub's nested commit-date layout, with the same values;
   - a per-record list in the data manifest.

   Derived bytecode (`__pycache__`) written into the frozen folder by the run was removed. The frozen files are
   unchanged (`append_attempt_2026-10-17.txt`).
4. **Terminal numeric row blocked.** The numeric route (`append_result_v2.py`) refused at "frozen scorer re-execution
   differs from outcomes.json". It re-executes the scorer as `python3 -I score_xmem.py <study_dir>` under the system
   Python. This scorer takes a counts path and an output path and needs numpy. This is the same route-convention
   mismatch as P16-REPL1. The H1 failure is recorded here, in the receipts and in HEURISTIC/LEDGER.md D133. The
   registered CRR verdict, NOT DECIDABLE, is closed through the non-numeric route.
5. **Anchor checked through an explorer.** The Bitcoin attestation was verified against block headers from a public
   explorer (blockstream.info), not a local node.

## 6. Next step for the programme

- **What the data allow.** This dataset (3 replicate runs, strong batch effects, no 4 h unstimulated control) cannot
  carry a residue-versus-rewrite question.
- **Within the lab's public data.** The next decisive test needs a series with more replicates per condition and a
  time-matched unstimulated control.
- **Proposal for the lab.** Ask the authors for the behavioural and calcium data ("on request"). Ask also for any 4 h
  unstimulated control: S06/S12/S18 are embryo libraries, so none exists in this run.
- **GSE341203.** The planarian series stays blocked until 2027-07-23.
