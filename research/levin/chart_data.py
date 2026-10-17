#!/usr/bin/env python3
"""Collects the numbers drawn in the four charts on levin.html from the committed study results.

Written for the web page (not part of the original record). It reads the verbatim result files in
phoenix/p23/ and computes nothing new beyond picking values out:
  (a) repair arms in the ageing NCA: P23-AGING-CRR results/test_n015.json (late fitness, share of time with all
      organs intact, cell writes), frozen test seeds 1000-1049, noise 0.15;
  (b) critical lesion: P23-AGING-COMPETENCY results/test_q2b_q5.json (Q2b, eye lost within 300 steps for 1-4 lost
      eye cells, with the study's 95% intervals);
  (c) injury recovery, same present / different past: P23-ALGOTYPES results/crr_history/crr_BS_w20.json and
      crr_SI_w20.json (simulator, 50 seeds x 3 continuations) and official_injury_BS.json / _SI.json (authors'
      classes, 20 runs each);
  (d) delayed gratification: P23-ALGOTYPES results/dg_analysis.json (official statistic, corrected statistic,
      strategy-free null, paper's values) for bubble and insertion cells, 0-5 frozen cells.
Run from this folder:  python chart_data.py > out/chart_data.json
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P23 = os.path.join(HERE, "phoenix", "p23")
load = lambda *p: json.load(open(os.path.join(P23, *p)))

crr = load("P23-AGING-CRR-2026-10-16", "results", "test_n015.json")["arms"]
arms = ["NONE", "C_PRIM", "C_CRR", "C_TARGET", "S_CRR", "S_CLOCK", "S_ANY", "S_IMMEDIATE", "S_CRR_TARGET",
        "S_CLOCK_TARGET", "C_CKPT", "C_EMACLOCK", "S_CRRFULL"]
repair = {a: {"late_fitness": round(crr[a]["late"], 2), "all_intact_share": round(crr[a]["t_all_intact"], 3),
              "cell_writes": round(crr[a]["writes"], 1), "n": crr[a]["n"]} for a in arms}

q2b = load("P23-AGING-COMPETENCY-2026-10-16", "results", "test_q2b_q5.json")["Q2b"]
lesion = [{"lost_cells": k, "eye_lost": q2b[f"dose_k{k}"]["eye_lost_at_300_injured"],
           "eligible": q2b[f"dose_k{k}"]["eligible"], "ci95": q2b[f"dose_k{k}"]["lost_ci95"],
           "uninjured_lost": q2b[f"dose_k{k}"]["eye_lost_at_300_uninjured"]} for k in (1, 2, 3, 4)]

injury = {}
for mix in ("BS", "SI"):
    s = load("P23-ALGOTYPES-2026-10-16", "results", "crr_history", f"crr_{mix}_w20.json")["summary"]
    o = load("P23-ALGOTYPES-2026-10-16", "results", f"official_injury_{mix}.json")["summary"]
    injury[mix] = {"simulator": {"seeds": s["seeds"], "history": s["repair_completed_history"],
                                 "fresh": s["repair_completed_fresh"], "local": s["repair_completed_local"]},
                   "authors_code": {"runs": o["exps"], "history": o["history_resorted"], "fresh": o["fresh_resorted"]}}

dg = load("P23-ALGOTYPES-2026-10-16", "results", "dg_analysis.json")
dgout = {}
for alg in ("bubble", "insertion"):
    rows = []
    for F, c in sorted(dg[alg]["conditions"].items(), key=lambda kv: int(kv[0])):
        rows.append({"frozen": int(F), "n": c["n"], "paper": c.get("paper_dg"),
                     "official": round(c["official_stat"]["dg_mean"], 3),
                     "corrected": round(c["corrected_stat"]["dg_mean"], 3),
                     "null": round(c["corrected_stat"]["null_mean"], 3)})
    dgout[alg] = rows

print(json.dumps({"repair_arms": repair, "critical_lesion": lesion, "injury_recovery": injury,
                  "delayed_gratification": dgout}, indent=1))
