# Why a claim-specific scorer

The registered statistics are paired bootstrap differences in true J against a comparator chosen on held-out data, AUC and R² of predictors fitted on frozen development data, and an abstention rule's gain over two groups of observation conditions. None of them is the generic bounded-paired-margin statistic of the locked engine (`scripts/guard.py`), so the study is frozen with `scripts/freeze_claim_specific.py`. Its verdicts go to the non-numeric ledger route or wait for the lock amendment that admits claim-specific scorers (`EPISTEMIC/LOCK_AMENDMENT_PROPOSALS_2026-10-07.md`).

The development record that produced every choice registered here is `studies/SEC-OBS1-2026-10-08/dev/`: the code (identical to the copies here), `dev_analysis.py` and its output, the schedule ablation (`ablate_schedule.py`, 15 arms on 40 development histories), and `dev_episodes.jsonl`, copied here.
