# Ashes ledger rows for EQ3 (verbatim excerpt)

Source: Ashes `ledger/LEDGER.md` at commit a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d. Each line below is copied byte for byte; the number before it is its line number in that file. Column headers are those of the ledger table the row sits in (see the source file).

**line 45**

| EQ3-0 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | precondition: tuned EWC λ spans ≥ 10× across carriers | 10× | tuned λ = 283 / 3 / 30 / 0.212766 / 300 / 2.83 (fars / krkopt / led24 / led7 / mfeat_factors / mfeat_morphological), span 1410.00× | — | decidable | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 46**

| EQ3-1 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | H-EQ2: rule at Ω = 1 not behind the tuned λ by a step on every carrier AND no single λ transfers (replication of EQ2-1b on six unseen carriers) | step = max(1.0, 2·SE) = 3.3508 / 8.9180 / 4.3633 / 3.2031 / 4.5371 / 4.8719 | Ω=1 − tuned: −3.7400 / +0.9790 / +0.6886 / +4.0625 / +3.9000 / +3.7000; seeds not behind 3/5, 4/5, 5/5, 5/5, 5/5, 4/5; best single λ = 1 loses 3.7200 / 1.3187 / 2.6917 / 3.6250 / 12.4500 / 6.5500 (no single λ transfers) | 5/6 carriers not behind | **FAIL** (fars behind by 3.7400 > step; the rule at every Ω, the Bayes arm, A-GEM and MEGA-I all sit at 9.26–9.28 on fars, whose class 0 is empty after the pre-registered subsample and whose EWC family is at chance; scored as committed, no exemption); the replication of EQ2-1b fails on 1/6 and holds on 5/6 with the EQ2 margins (+3.7 to +4.1 on three) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 47**

| EQ3-2 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | reduction: rule within a step of fixed w = median derived w on every carrier | step per carrier | rule − fixed@median: +2.4200 / +7.6923 / +0.6260 / +16.2500 / +23.5500 / +14.4000 (median w 426.287 / 4.76098 / 31.6972 / 2.77719 / 1065.84 / 14.6744; the reduction arm diverges on 2/5, 3/5, 0/5, 3/5, 2/5, 2/5 seeds) | 0/6 within a step | does not reduce: normalised-gradient method (as EQ2-2) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 48**

| EQ3-3 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | control, same units (ER-sum): rule not ahead of the best fixed w by a step AND within a step of its reduction arm, every carrier | step per carrier | rule − best fixed: −4.6800 / −4.3756 / −1.2520 / −3.5000 / −0.2000 / +1.9000 (all < step); rule − reduction: +4.6200 / +3.0969 / +0.5008 / −0.8125 / −0.2500 / +2.9500 (fars 4.6200 > step 3.3508) | 5/6 | **VIOLATED** (fars: the rule is 4.62 ahead of its own reduction arm; on the other five the control holds as in EQ2-3) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 49**

| EQ3-4 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | control, constraint (DER++ and LwF), narrowed to load-bearing cells (finite grid spans ≥ 2 steps): rule at its best Ω behind the tuned weight by ≥ step in every load-bearing cell | step per carrier; load-bearing = span ≥ 2 steps | load-bearing 5/12 cells (7 inert, counted and excluded): fars/LwF +0.0200, led7/DER++ −0.5938, led7/LwF −7.1875, mfeat_factors/LwF −19.3000, mfeat_morphological/LwF +12.6000; behind by ≥ step in 2/5 | 2/5 load-bearing cells | **VIOLATED** (the rule ties LwF on fars, ties DER++ on led7 and is 12.60 ahead of tuned LwF on mfeat_morphological; the harm clause is retired) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 50**

| EQ3-5 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | diagnostic (SI, MAS): Ω = 1 − tuned | — | SI: −1.2400 / −1.5984 / −2.7543 / +0.5312 / −5.6000 / +5.7000; MAS: +3.1400 / +5.3746 / −0.0313 / +6.9062 / +1.6000 / +2.6000 | — | report: no systematic miss (as EQ2-5) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 51**

| EQ3-6 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | Ω plateau: best Ω on the EWC nine-point grid in {0.71, 1, 1.41} on every carrier (ties to the smallest Ω) | 6/6 | best Ω = 2.0 / 4.0 / 2.0 / 2.83 / 1.0 / 2.83 | 1/6 | **FAIL** (a plateau, no peak at 1, as EQ2-6 and as theory/checks/omega_sweeps.py predicts) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 52**

| EQ3-7 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | published baselines (A-GEM, GradNorm α=0, MEGA-I) vs rule at Ω = 1; 'dominates' if ahead by ≥ step on every carrier | step per carrier | baseline − rule: A-GEM +0.0200 / −5.2547 / −3.2238 / −4.2188 / −10.8000 / −10.1500; GradNorm +7.1000 / −17.8821 / −4.9139 / −26.0312 / −58.3500 / −37.9000 (diverges on 4/6); MEGA-I +0.0200 / −5.5744 / −3.5055 / −8.6562 / −16.5000 / −11.4500 | 0/3 dominate | no published baseline is ahead by a step on every carrier | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 53**

| EQ3-S | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | sensitivity: EQ3-1 'not behind' flips in > 1 of 54 cap × smooth cells → fragile | 1 cell | 6/54 cells flip: mfeat_factors at cap 10 (−11.15 ×3) and cap 100 (−5.25, −5.20, −5.15); every other carrier's verdict is the same in all 9 cells | 6/54 | fragile (the same cap dependence as EQ2-S on mfeat_pixel) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 54**

| EQ3-8 | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | diagnostic regime, standardised features × 4: Ω = 1 − tuned λ | — | −0.9200 (tuned 3) / +2.5774 (0.1) / +1.5336 (0.3) / +1.3125 (0.1) / +0.4000 (10) / +6.8500 (3) | — | report: the gate's forced-mismatch regime does not change the picture | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 55**

| EQ3-C | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | cap axis (mechanism): rule at Ω = 1 not behind the tuned λ by a step iff cap ≥ tuned λ, in all 18 cells | 18/18 | 16/18 as predicted; mismatches: fars/cap 1e4 (behind; predicted not behind) and led24/cap 10 (not behind at −1.56; predicted behind) | 16/18 | **FAIL** (the cap mechanism holds on mfeat_factors exactly as on EQ2's mfeat_pixel, and is not the whole story on led24 and fars) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 56**

| EQ3-D | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | empty-present diagnostic: late-w median vs whole-run median at Ω = 1 | — | ratio 0.762 / 1.095 / 1.433 / 1.035 / 0.821 / 1.246; seeds with late-w < 1: 0/5, 0/5, 0/5, 2/5, 0/5, 0/5 | — | report: the converged learner does not drop the past (late-w stays of the order of the whole-run median) except on led7 for 2/5 seeds | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 57**

| EQ3-A | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | capacity × epochs on mfeat_factors: rule not behind the tuned λ by the cell's step in ≥ 3 of 4 cells | 3/4 | hidden256/ep3 +3.90 (step 4.54) nb; hidden64/ep1 −1.15 (1.11) behind; hidden64/ep3 −3.05 (1.88) behind; hidden256/ep1 +2.65 (5.09) nb | 2/4 | **FAIL** (the pass is specific to the wide network) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 58**

| EQ3-I | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | lr × batch invariance on mfeat_factors: rule not behind by the cell's step in ≥ 4 of 5 cells | 4/5 | lr0.05/bs10 +3.90 (4.54); lr0.0125/bs10 +3.00 (2.68); lr0.2/bs10 +1.35 (2.42); lr0.05/bs5 +0.85 (4.63); lr0.05/bs20 +0.45 (3.26); all nb; tuned λ moves 300 → 300 / 3000 / 3000 / 300 across cells | 5/5 | **PASS-0** (weakly anchored; an invariance row, not a comparative win: the rule is ahead by ≥ step in 1/5 cells) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 59**

| EQ3-B | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | Bayes arm (Laplace weight 1/2 on the task-size-weighted Fisher), report only | — | Bayes − tuned: −3.7200 / +1.2587 / −2.7543 / +0.0000 / −12.5000 / −7.6000; rule(Ω=1) − Bayes: −0.0200 / −0.2797 / +3.4429 / +4.0625 / +16.4000 / +11.3000 | Bayes not behind tuned on 3/6 | report: the Laplace weight is the tuned weight on led7 (tuned λ 0.21) and krkopt, and 7.6 to 12.5 points behind where the tuned λ is in the hundreds; the rule's advantage over Bayes is 3.4 to 16.4 on 4/6 | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |

**line 60**

| EQ3-P | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | plateau width on the nine-point Ω grid (points within a step of the best), report only | — | 9/9 / 9/9 / 9/9 / 7/9 (0.5..4) / 9/9 / 7/9 (0.5..4), all contiguous; median width 9 | — | report: Ω is a plateau over the whole grid on 4/6 carriers and over 0.5–4 on the other two | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |
