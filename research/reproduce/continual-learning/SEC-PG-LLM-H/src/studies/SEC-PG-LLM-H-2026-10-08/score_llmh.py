"""SEC-PG-LLM-H frozen scorer. From Phoenix_Egg/: python3 -I studies/SEC-PG-LLM-H-2026-10-08/score_llmh.py > RUNS/<id>/score.json
Prints the outcomes as deterministic JSON on stdout (no timestamps; append_result_v2.py re-executes the scorer and requires byte identity)
and writes a readable summary to RUNS/<id>/score.txt. Reads RUNS/<id>/{units_pretrain,units_main,units_sens,units_rerun}.jsonl,
draw_log.json, anchor_check.json and this folder's config.json. Refuses (NOT DECIDABLE) if the frozen folder changed. Every verdict word and
condition is computed from the numbers here (R15); PREREG.md states the same rules in prose.

Metric: test J = (A_test + B_test)/2 per run. Grid arm: the run in T4's grid with the lowest validation q = (A_val + B_val)/2 rounded to 5
decimals, ties to the smaller lambda (T4's selection), scored on test. Constant: the grid's lambda = 5e3 run (T4's transferred constant).
Non-finite values: in SEC-PG or a sensitivity run, replaced by 10 nats (a loss for the claim) and listed; in any other arm, NOT DECIDABLE.
Independent unit: the seed. For a difference X - Y, each seed's value is its mean over its cells (all, or one stratum); estimate = mean over
seeds; 95 % interval = mean +/- t(0.975, n-1) sd/sqrt(n). A percentile bootstrap over seeds (B = 4000, default_rng(0)) is descriptive only.
Claim for an arm X:
  P1 upper(X - grid) <= +0.005
  P2 mean(X - SEC v2) <= -0.005 and upper(X - SEC v2) < 0, and mean(X - const) <= -0.005 and upper(X - const) < 0
  P3 upper(X - grid) <= +0.01 within the 8 M stratum (averaged over widths), and within the width-192 stratum (averaged over maturities)
  P4 mean B_test(X) <= mean B_test(SEC v2), and mean A_test(X) - mean A_test(grid) <= 0.05 (means over cells)
  P5 cells no worse than the grid beyond T4's tolerance (J - J_grid <= 0.02 and A - A_grid <= 0.05 and B - B_grid <= 0.05): X >= SEC v2
     (one-sided; T4's two-sided count, which also counts large improvements as misses, is reported as description only)
Admissible cell: A_test(none) - A_test(frozen) >= 0.10 and B_test(frozen) - B_test(none) >= 0.5.
Controls: K1 (positive) mean(none - grid) >= 0.01 and lower > 0; K2 (instrument) the transferred constant does not meet P1:
upper(const - grid) > 0.005; K3 (projection needed) upper(SEC-PG - light) < 0; K4 the light anchor alone does not meet the claim;
K5 (no constant reduction, R7) upper(SEC-PG - pgconst) < 0, where pgconst is the same GPM schedule with the constant anchor lambda = the
median over the study's cells of SEC-PG's own multiplier alpha s kappa_mult (checked here against units_pretrain.jsonl); K6 (no reduction to
published GPM) upper(SEC-PG - gpm_only) < 0, where gpm_only projects from the first task-B step with no anchor (checked here).
Verdict (words from append_result_v2's set): NOT DECIDABLE if the frozen folder changed, the draw failed, a registered unit is missing,
a non-SEC-PG unit is non-finite, a rival arm was not run as registered, or under 80 % of cells are admissible; else, if K1 fails:
'NOT DECIDABLE (UNINFORMATIVE: positive control K1 failed; the claim holds|fails)'; else FAIL if the claim fails for SEC-PG; else
'REDUCES (...)' naming the failing reduction controls among K3-K6; else RESULT (the registered claim holds).
Sensitivity: each override in config.json replaces SEC-PG; a flip is a change in whether P1-P5 hold. If the main claim fails, flips are
not counted toward anything (variants meeting P1-P5 are listed as exploratory, not as a rescue).
Scorer-computable PASS-1 preconditions (NOT a grade): verdict RESULT; at most one flip; K2-K6 hold; at least 80 % admissible; Bitcoin
attestation verified for this freeze with block time + 7200 s before the first fetch, and the anchor check itself before the first fetch
(both as recorded in draw_log.json at draw time); a signed annotated tag on origin at the anchor check (draw_log.json); both
rerun units identical to their main units in every field except timings. Outside this scorer: the reviewers' receipts, verification of
the tag's signature and of the attestation against a Bitcoin node, and the judgement on Gutenberg text under DATA/SEEN.md's scope note."""
import sys; sys.dont_write_bytecode = True
import json, math, pathlib, datetime, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; ROOT = HERE.parents[1]; SID = HERE.name; RUN = ROOT / 'RUNS' / SID
sys.path.insert(0, str(HERE)); import data_step
CFG = json.load(open(HERE / 'config.json')); GRID = [1000, 2000, 5000, 10000, 20000, 50000]; CONST = 5000
WIDTHS = [64, 128, 192]; MAT = [1_000_000, 2_000_000, 8_000_000]
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179}
ARMS = ['frozen', 'none'] + [f'grid_{l}' for l in GRID] + ['sec', 'pg', 'light', 'pgconst', 'gpm_only']; CLAIMANTS = ('pg',)
PRE_KEYS = ('s', 'c', 'rho', 'nd2', 'params', 'final_train_loss', 'path_length', 'kl_chord', 'loss_slope_window')
def load(name):
    p = RUN / f'units_{name}.jsonl'; out = []
    if p.exists():
        for line in p.read_text().splitlines():
            try: out.append(json.loads(line))
            except ValueError: pass
    return out
def same(x, y): return json.dumps(x, sort_keys=True) == json.dumps(y, sort_keys=True)
def notiming(r): return {k: v for k, v in r.items() if not any(t in k for t in ('second', 'rss', 'wall'))}
def main():
    out = dict(study_id=SID, config=CFG); lines = []
    fok, fbad, fm = data_step.frozen_ok(); out['frozen_unchanged'] = fok; out['freeze_sha256'] = data_step.sha((HERE / 'FREEZE.json').read_bytes())
    if not (RUN / 'draw_log.json').exists():
        out['verdict'] = 'NOT DECIDABLE (draw incomplete: no draw_log.json)'; print(json.dumps(out, sort_keys=True, indent=1)); (RUN / 'score.txt').write_text('VERDICT ' + out['verdict'] + '\n'); return
    draw = json.load(open(RUN / 'draw_log.json')); anchor = json.load(open(RUN / 'anchor_check.json')) if (RUN / 'anchor_check.json').exists() else {}
    seeds = draw['seeds']; cells = [(s, d, t) for s in seeds for d in WIDTHS for t in MAT]; sens_ids = list(CFG['sensitivity'])
    U = {(r['seed'], r['d'], r['tokens'], r['arm']): r['result'] for r in load('main') + load('sens')}
    need = ARMS + [f'sens_{k}' for k in sens_ids]; missing = [f'{c[0]}:{c[1]}:{c[2]}:{a}' for c in cells for a in need if (*c, a) not in U]
    nonfinite = [f'{c[0]}:{c[1]}:{c[2]}:{a}:{k}' for c in cells for a in need if (*c, a) in U for k in ('A_val', 'B_val', 'A_test', 'B_test') if not (isinstance(U[(*c, a)].get(k), (int, float)) and math.isfinite(U[(*c, a)][k]))]
    blocking = [x for x in nonfinite if x.split(':')[3] not in CLAIMANTS and not x.split(':')[3].startswith('sens_')]
    out.update(draw_ok=bool(draw.get('ok')), missing_units=missing, nonfinite=nonfinite)
    gate = None if fok else 'frozen folder changed: ' + ', '.join(fbad)
    pre_main = {(r['seed'], r['d'], r['tokens']): r['result'] for r in load('pretrain')}
    lam = float(np.median([10.0*pre_main[c]['s']*CFG['sec_pg']['kappa_mult'] for c in cells])) if all(c in pre_main for c in cells) else None; out['pgconst_lambda'] = lam
    rivals_ok = lam is not None and all(U[(*c, 'pgconst')].get('anchor') == 'const' and U[(*c, 'pgconst')].get('const') == lam and U[(*c, 'gpm_only')].get('switch') == 0.0 and U[(*c, 'gpm_only')].get('const') == 0.0 for c in cells if (*c, 'pgconst') in U and (*c, 'gpm_only') in U)
    gate = gate or (None if draw.get('ok') else 'draw failed') or (f'{len(missing)} registered units missing' if missing else None) or (f'non-finite values outside SEC-PG: {blocking}' if blocking else None) or (None if rivals_ok else 'rival arms pgconst/gpm_only not run as registered')
    if gate:
        out['verdict'] = 'NOT DECIDABLE (' + gate + ')'; print(json.dumps(out, sort_keys=True, indent=1)); (RUN / 'score.txt').write_text('VERDICT ' + out['verdict'] + '\n'); return
    f10 = lambda x: float(x) if math.isfinite(x) else 10.0
    C = {}
    for c in cells:
        best = min(GRID, key=lambda l: (round(0.5*(U[(*c, f'grid_{l}')]['A_val'] + U[(*c, f'grid_{l}')]['B_val']), 5), l))
        arms = {a: U[(*c, a)] for a in need}; arms['grid'] = U[(*c, f'grid_{best}')]; arms['const'] = U[(*c, f'grid_{CONST}')]
        C[c] = {a: dict(A=f10(r['A_test']), B=f10(r['B_test'])) for a, r in arms.items()}
        for a in C[c]: C[c][a]['J'] = 0.5*(C[c][a]['A'] + C[c][a]['B'])
        C[c]['_chosen'] = best; C[c]['_admissible'] = bool(C[c]['none']['A'] - C[c]['frozen']['A'] >= 0.10 and C[c]['frozen']['B'] - C[c]['none']['B'] >= 0.5)
    def diff(x, y, sel=lambda c: True):
        per = np.array([np.mean([C[c][x]['J'] - C[c][y]['J'] for c in cells if c[0] == s and sel(c)]) for s in seeds]); n = len(per); m = float(per.mean()); se = float(per.std(ddof=1)/math.sqrt(n))
        rng = np.random.default_rng(0); bs = np.array([per[rng.integers(0, n, n)].mean() for _ in range(4000)])
        return dict(mean=m, lower=m - T975[n - 1]*se, upper=m + T975[n - 1]*se, per_seed=[float(v) for v in per], boot_lower=float(np.quantile(bs, 0.025)), boot_upper=float(np.quantile(bs, 0.975)))
    def cellmean(a, k): return float(np.mean([C[c][a][k] for c in cells]))
    def tol(a): return int(sum(C[c][a]['J'] - C[c]['grid']['J'] <= 0.02 and C[c][a]['A'] - C[c]['grid']['A'] <= 0.05 and C[c][a]['B'] - C[c]['grid']['B'] <= 0.05 for c in cells))
    def tol2(a): return int(sum(abs(C[c][a]['J'] - C[c]['grid']['J']) <= 0.02 and abs(C[c][a]['A'] - C[c]['grid']['A']) <= 0.05 and abs(C[c][a]['B'] - C[c]['grid']['B']) <= 0.05 for c in cells))
    def claim(x):
        r = {}; d_g = diff(x, 'grid'); d_s = diff(x, 'sec'); d_c = diff(x, 'const'); d_8 = diff(x, 'grid', lambda c: c[2] == 8_000_000); d_192 = diff(x, 'grid', lambda c: c[1] == 192)
        r['P1'] = dict(ok=d_g['upper'] <= 0.005, vs_grid=d_g)
        r['P2'] = dict(ok=(d_s['mean'] <= -0.005 and d_s['upper'] < 0) and (d_c['mean'] <= -0.005 and d_c['upper'] < 0), vs_sec=d_s, vs_const=d_c)
        r['P3'] = dict(ok=d_8['upper'] <= 0.01 and d_192['upper'] <= 0.01, stratum_8M=d_8, stratum_w192=d_192)
        bx, bs_, ax, ag = cellmean(x, 'B'), cellmean('sec', 'B'), cellmean(x, 'A'), cellmean('grid', 'A')
        r['P4'] = dict(ok=bx <= bs_ and ax - ag <= 0.05, B_x=bx, B_sec=bs_, A_x=ax, A_grid=ag)
        r['P5'] = dict(ok=tol(x) >= tol('sec'), tol_x=tol(x), tol_sec=tol('sec'))
        r['holds'] = all(r[p]['ok'] for p in ('P1', 'P2', 'P3', 'P4', 'P5')); return r
    adm = [c for c in cells if C[c]['_admissible']]; out['admissible'] = dict(n=len(adm), of=len(cells), frac=len(adm)/len(cells), inadmissible=[list(c) for c in cells if not C[c]['_admissible']])
    mc = claim('pg'); out['claim_SEC_PG'] = mc; lc = claim('light')
    K = dict(K1_positive=diff('none', 'grid'), K2_const_meets_P1=diff('const', 'grid'), K3_vs_light=diff('pg', 'light'), K5_vs_pgconst=diff('pg', 'pgconst'), K6_vs_gpm_only=diff('pg', 'gpm_only'))
    ctl = dict(K1=K['K1_positive']['mean'] >= 0.01 and K['K1_positive']['lower'] > 0, K2=K['K2_const_meets_P1']['upper'] > 0.005, K3=K['K3_vs_light']['upper'] < 0, K4=not lc['holds'],
               K5=K['K5_vs_pgconst']['upper'] < 0, K6=K['K6_vs_gpm_only']['upper'] < 0)
    out['controls'] = dict(holds=ctl, estimates=K, light_claim=lc)
    sens = {k: claim(f'sens_{k}') for k in sens_ids}; flips = [k for k in sens_ids if sens[k]['holds'] != mc['holds']]
    out['sensitivity'] = dict(cells={k: dict(holds=v['holds'], **{p: v[p]['ok'] for p in ('P1', 'P2', 'P3', 'P4', 'P5')}, pg_minus_grid=v['P1']['vs_grid']['mean'], shift_from_main=v['P1']['vs_grid']['mean'] - mc['P1']['vs_grid']['mean']) for k, v in sens.items()})
    out['sensitivity'].update(flips=flips if mc['holds'] else None, n_flips=len(flips) if mc['holds'] else None, exploratory_variants_meeting_claim=None if mc['holds'] else [k for k in sens_ids if sens[k]['holds']])
    names = dict(K3='projection not shown necessary (SEC-PG not below the light anchor alone)', K4='the light anchor alone meets P1-P5', K5='the same GPM schedule with a constant anchor of matched size is not worse', K6='GPM as published (projection from the first step, no anchor) is not worse')
    if out['admissible']['frac'] < 0.80: verdict = 'NOT DECIDABLE (fewer than 80 % of cells admissible)'
    elif not ctl['K1']: verdict = 'NOT DECIDABLE (UNINFORMATIVE: positive control K1 failed; the claim ' + ('holds' if mc['holds'] else 'fails') + ')'
    elif not mc['holds']: verdict = 'FAIL (' + ', '.join(p for p in ('P1', 'P2', 'P3', 'P4', 'P5') if not mc[p]['ok']) + ' not met)'
    elif not all(ctl[k] for k in ('K3', 'K4', 'K5', 'K6')): verdict = 'REDUCES (' + '; '.join(names[k] for k in ('K3', 'K4', 'K5', 'K6') if not ctl[k]) + ')'
    else: verdict = 'RESULT (the registered claim P1-P5 holds; no reduction found)'
    out['verdict'] = verdict
    rr = []
    for r in load('rerun'):
        k = (r['seed'], r['d'], r['tokens'])
        if r['arm'] == 'pretrain+pg': ident = same({q: r['result']['pre'].get(q) for q in PRE_KEYS}, {q: pre_main.get(k, {}).get(q) for q in PRE_KEYS}) and same(notiming(r['result']['pg']), notiming(U.get((*k, 'pg'), {})))
        else: ident = same(notiming(r['result']), notiming(U.get((*k, r['arm']), {})))
        rr.append(dict(unit=[*k, r['arm']], identical=ident))
    out['rerun'] = rr; rerun_ok = len(rr) == 2 and all(x['identical'] for x in rr)
    first = draw['first_fetch_utc']; ft = datetime.datetime.fromisoformat(first).timestamp()
    anchor_same = bool(anchor) and data_step.sha((RUN / 'anchor_check.json').read_bytes()) == draw.get('anchor_check_sha256')
    strong = bool(anchor_same and anchor.get('ok') and draw.get('attested_block_timestamp') and draw['attested_block_timestamp'] + 7200 < ft and datetime.datetime.fromisoformat(draw['anchor_checked_utc']).timestamp() < ft)
    pre = dict(verdict_RESULT=verdict.startswith('RESULT'), at_most_one_flip=mc['holds'] and len(flips) <= 1, controls_K2_to_K6_hold=all(ctl[k] for k in ('K2', 'K3', 'K4', 'K5', 'K6')),
               admissible_at_least_80pc=out['admissible']['frac'] >= 0.80, bitcoin_attestation_before_first_fetch=strong, signed_tag_on_origin_at_anchor=bool(draw.get('tag_ok_at_anchor')), deterministic_repeat=rerun_ok)
    out['pass1_scorer_preconditions'] = dict(items=pre, all_met=all(pre.values()), note='NOT a grade. Outside this scorer: reviewer receipts; verification of the tag signature and of the attestation against a Bitcoin node; the judgement on Gutenberg text under DATA/SEEN.md scope note (1). The ledger records the verdict word through LA-1 (append_result_v2.py), which caps the row at a weak-anchor PASS-0 unless the attestation precedes exposure and the tag is verified.')
    out['first_fetch_utc'] = first
    out['descriptive'] = dict(mean_J={a: cellmean(a, 'J') for a in ['frozen', 'none', 'grid', 'const', 'sec', 'pg', 'light', 'pgconst', 'gpm_only']}, frozen_minus_grid=diff('frozen', 'grid'),
                              by_tokens={str(t): {a: float(np.mean([C[c][a]['J'] for c in cells if c[2] == t])) for a in ('grid', 'const', 'sec', 'pg', 'light', 'pgconst', 'gpm_only')} for t in MAT},
                              by_width={str(w): {a: float(np.mean([C[c][a]['J'] for c in cells if c[1] == w])) for a in ('grid', 'const', 'sec', 'pg', 'light', 'pgconst', 'gpm_only')} for w in WIDTHS},
                              cell_w192_8M_pg_minus_grid=diff('pg', 'grid', lambda c: c[1] == 192 and c[2] == 8_000_000), tolerance_two_sided={a: tol2(a) for a in ('sec', 'pg', 'light', 'const', 'pgconst')},
                              grid_choice_counts={str(l): sum(C[c]['_chosen'] == l for c in cells) for l in GRID},
                              seconds={a: float(np.mean([U[(*c, a)].get('seconds', 0.0) for c in cells])) for a in ['none', 'sec', 'pg', 'light', 'pgconst', 'gpm_only'] + [f'grid_{l}' for l in GRID]},
                              basis_frac=float(np.mean([U[(*c, 'pg')].get('basis_frac', float('nan')) for c in cells])))
    out['cells'] = [dict(seed=c[0], d=c[1], tokens=c[2], chosen=C[c]['_chosen'], admissible=C[c]['_admissible'], **{a: C[c][a] for a in ['frozen', 'none', 'grid', 'const', 'sec', 'pg', 'light', 'pgconst', 'gpm_only']}) for c in cells]
    print(json.dumps(out, sort_keys=True, indent=1))
    f = lambda d: f"{d['mean']:+.4f} [{d['lower']:+.4f}, {d['upper']:+.4f}]"; L = lines.append
    L(f'SEC-PG-LLM-H score, written {datetime.datetime.now(datetime.timezone.utc).isoformat()}; seeds {seeds}; cells {len(cells)}; admissible {len(adm)}/{len(cells)}; non-finite (SEC-PG/sensitivity, replaced by 10 nats) {nonfinite}')
    L(f"books A {draw['domain_A_files']} B {draw['domain_B_files']}; freeze sha256 {out['freeze_sha256']}")
    L('P1 SEC-PG - grid ' + f(mc['P1']['vs_grid']) + (' ok' if mc['P1']['ok'] else ' NOT MET'))
    L('P2 SEC-PG - SEC v2 ' + f(mc['P2']['vs_sec']) + '; SEC-PG - const 5e3 ' + f(mc['P2']['vs_const']) + (' ok' if mc['P2']['ok'] else ' NOT MET'))
    L('P3 8 M stratum ' + f(mc['P3']['stratum_8M']) + '; width 192 ' + f(mc['P3']['stratum_w192']) + (' ok' if mc['P3']['ok'] else ' NOT MET'))
    p4 = mc['P4']; L(f"P4 B_test SEC-PG {p4['B_x']:.4f} vs SEC v2 {p4['B_sec']:.4f}; A_test SEC-PG - grid {p4['A_x'] - p4['A_grid']:+.4f}" + (' ok' if p4['ok'] else ' NOT MET'))
    p5 = mc['P5']; L(f"P5 cells within tolerance (one-sided) SEC-PG {p5['tol_x']} vs SEC v2 {p5['tol_sec']}" + (' ok' if p5['ok'] else ' NOT MET'))
    L('controls ' + ', '.join(f"{k} {'holds' if v else 'VIOLATED'}" for k, v in ctl.items()))
    L('K1 none - grid ' + f(K['K1_positive']) + '; K2 const - grid ' + f(K['K2_const_meets_P1']) + '; K3 SEC-PG - light ' + f(K['K3_vs_light']) + '; K5 SEC-PG - pgconst ' + f(K['K5_vs_pgconst']) + '; K6 SEC-PG - gpm_only ' + f(K['K6_vs_gpm_only']) + f"; K4 light meets claim {lc['holds']}")
    L(f"sensitivity: flips {out['sensitivity']['flips']}; exploratory variants meeting the claim {out['sensitivity']['exploratory_variants_meeting_claim']}")
    L(f'rerun identical {rerun_ok}; attestation before first fetch {strong}; signed tag at anchor {pre["signed_tag_on_origin_at_anchor"]}; first fetch {first}')
    L('VERDICT ' + verdict); L('scorer-computable PASS-1 preconditions: ' + ('all met' if all(pre.values()) else 'not all met: ' + ', '.join(k for k, v in pre.items() if not v)) + '. ' + out['pass1_scorer_preconditions']['note'])
    (RUN / 'score.txt').write_text('\n'.join(lines) + '\n')
if __name__ == '__main__': main()
