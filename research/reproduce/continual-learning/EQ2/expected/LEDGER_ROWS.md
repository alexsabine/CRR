# Ashes ledger rows for EQ2 (verbatim excerpt)

Source: Ashes `ledger/LEDGER.md` at commit a403a96c8a091e87b6f4f0ab77fa7beaa9fe724d. Each line below is copied byte for byte; the number before it is its line number in that file. Column headers are those of the ledger table the row sits in (see the source file).

**line 31**

| EQ2-0 | 0da06fc1 (anchor: push-timestamp only; tag prereg-eq2-2026-09-17 at 4ba6035) | PMLB mfeat_fourier, mfeat_pixel, texture (Y); numpy MLP d-256-K, 3 epochs/task | precondition: tuned EWC λ spans ≥ 10× across carriers | 10× | tuned λ = 30 / 1410 / 100, span 47.00× | 3 carriers | DECIDABLE | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 32**

| EQ2-1 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | H-EQ2: rule at Ω = 1 not behind the tuned λ by a step on every carrier AND no single λ transfers | step = max(1.0, 2·SE) = 1.0000 / 3.5121 / 3.6120 | Ω=1 − tuned: +3.3000, +2.1000, +2.7800 (per seed not behind 5/5, 5/5, 5/5); best single λ = 30 loses 0.0000, 15.4500, 0.5600 | 3/3 carriers | **PASS, FRAGILE**: the "not behind" reading flips in 6 of 27 sensitivity cells (every cap = 10 and cap = 100 cell on mfeat_pixel: −16.60, −13.45); the pass exists only with cap = 1e4 (registered) | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 33**

| EQ2-2 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | reduction: rule within a step of fixed w = median derived w on every carrier | step per carrier | rule − fixed@median: +29.4000 (w = 1336.54, diverges), +10.0000 (w = 3183.87, 1/5 seeds diverge), +2.7800 (w = 110.561) | 0/3 within a step | DOES NOT REDUCE: normalised-gradient method (the median derived w is 45×, 2.3×, 1.1× the tuned λ; fixed at that value it diverges or trails) | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 34**

| EQ2-3 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | control, same units (ER-sum): rule not ahead of the best fixed w by a step and within a step of its reduction arm | step per carrier | rule − best fixed w: −0.6000, −0.2500, −0.6600; rule − reduction: −0.5000, −0.2500, −0.3600 | 3/3 | holds (on same-units replay the rule reduces to a constant and adds nothing; EQX repeated) | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 35**

| EQ2-4 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | control, constraint (DER++ and LwF): rule at its best Ω behind the tuned weight by ≥ step on every carrier, both methods | step per carrier | DER++: −1.5500, −0.7000, +0.5800 (tuned α = 1, 0.3, 0.01); LwF: −11.3500, −9.4000, −18.6200 | DER++ 1/3 carriers, LwF 3/3 | **VIOLATED** by DER++ (within a step on mfeat_pixel and texture, where accuracy is 95–99 % and α barely matters). Per prereg: the mechanism statement ("harmful for every constraint-type past term") is falsified as written; the LwF clause holds | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 36**

| EQ2-5 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | diagnostic (SI, MAS): Ω = 1 − tuned, expected to miss | — | SI: −0.1000, −7.9000, +0.1600; MAS: +1.3000, −1.7500, +1.6800 | SI misses by ≥ step on 1/3, MAS on 0/3 | report: the expected miss does not appear; SI and MAS are within a step of (or ahead of) their tuned weights on 2/3 and 3/3 carriers | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 37**

| EQ2-6 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | Ω plateau: best Ω on the EWC arm in {0.71, 1, 1.41} on every carrier (ties to the smallest Ω) | — | best Ω = 0.5, 2.0, 1.41; Ω profile (Ω − tuned): mfeat_fourier +3.60/+2.65/+3.30/+2.80/+2.90; mfeat_pixel +0.70/+0.35/+2.10/+0.65/+2.55; texture +1.26/+2.54/+2.78/+3.02/−2.04 | 1/3 | FAIL: a broad plateau over 0.5–1.41 with no resolvable peak at 1 | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 38**

| EQ2-7 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | published baselines on the EWC penalty vs rule at Ω = 1 (report; "dominates" if ahead by ≥ step on every carrier) | step per carrier | baseline − rule: A-GEM −4.2000, −14.1000, −4.9800; GradNorm α=0 −29.4000, −52.1500, −31.3400 (diverged on two carriers, chance on the third); MEGA-I −5.1500, −19.1000, −6.8400 | 0/9 ahead | report: no published baseline is ahead of the rule; GradNorm as implemented (weights summing to 2) starves the present term and diverges | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 39**

| EQ2-S | 0da06fc1 (anchor: push-timestamp only) | same (Y) | sensitivity: EQ2-1 "not behind" flips in > 1 of 27 cells → fragile | 1 cell | 6/27 cells flip (mfeat_pixel at cap 10: −16.60 ×3; at cap 100: −13.45, −13.45, −13.40); texture at cap 10 (−1.02, −1.26, −1.46) and smooth 0.98/cap 1e4 (−2.18) stay within its 3.61 step | — | FRAGILE (cap-dependent: the derived weight sits above the largest stable fixed λ, so a cap below the tuned λ turns the rule into a weaker fixed weight) | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 40**

| EQ2-8 | 0da06fc1 (anchor: push-timestamp only) | same (Y) | diagnostic regime, standardised features × 4 (the gate's mismatch regime): Ω = 1 − tuned λ | — | −0.4500 (tuned 3), −0.1500 (tuned 10000, grid edge), −16.6400 (tuned 30); reduction arms 0.0000 / 25.4500 / 43.7400 | — | report: the gate's premise does not reappear on real features when the units are forced apart; the pass in EQ2-1 is not explained by input scale | runs/eq2/frozen/eq2_score.py | runs/eq2/score.txt |

**line 42**

| EQ2-1b | 0da06fc1 (anchor: push-timestamp only) | same as EQ2-1 (Y) | re-labelling of EQ2-1 under the PASS levels accepted 2026-09-18 (prompt-log entry 56; docs/notes/2026-09-18_sharp_regime_review.md §4); no new computation | PASS-1 needs ≤ 1 sensitivity flip, no control violated, strong anchor | EQ2-S: 6/27 cells flip; EQ2-4: DER++ control violated on 2/3 carriers; anchor weak | — | **PASS-0 (provisional)**: a pre-registered pass on unseen data that is fragile, has a violated control and a weak anchor; not a result until replicated (study EQ2R) | — | ledger only |

**line 61**

| EQ2-1c | 5b3bec36 (anchor: push-timestamp only; prereg commit daf50e7 pushed 2026-09-22T01:21:32Z; data fetched 2026-09-22T01:23Z) | PMLB mfeat_factors, mfeat_morphological, led7, led24, krkopt (first 10 classes, 5000-row subsample), fars (8 classes, 5000-row subsample; class 0 empty after the subsample) (Y) | correction row for EQ2-1b: replication attempted in EQ3 (six unseen carriers, five days later, fresh prereg) | EQ3-1 | EQ3-1 FAIL on 1/6 (fars), not behind on 5/6 with margins +0.69 to +4.06; EQ3-S fragile; EQ3-3 and EQ3-4 violated | 5/6 | EQ2-1b stays **PASS-0 with a failed replication recorded**; PASS-1 and PASS-2 not reached (replication incomplete on 1/6, weak anchoring) | runs/eq3/frozen/eq3_score.py | runs/eq3/score.txt |
