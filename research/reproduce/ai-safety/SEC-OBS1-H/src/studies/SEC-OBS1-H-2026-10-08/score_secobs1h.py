"""SEC-OBS1-H frozen scorer (claim-specific). Usage: python score_secobs1h.py <heldout_episodes.jsonl> <dev_episodes.jsonl> <out.json>
Reads only the two episode files. Classifiers and regressions for H2/H3 are fitted on the development episodes (frozen with this study) and
evaluated on the held-out episodes. All intervals: percentile bootstrap over held-out episodes, B = 4000, numpy default_rng(0).
Every number the verdicts use is computed here; nothing is tuned on held-out data except the H1 comparator choice, which is the conservative
direction (the strongest inexpensive comparator is the one with the lowest held-out mean J)."""
import json, sys, math, numpy as np, warnings
warnings.filterwarnings('ignore')
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, r2_score

CONDS = ('full', 'proj', 'alias', 'missing', 'drift', 'concept', 'hideA', 'hideA+ref')
FLAGGED = ('proj', 'missing', 'concept', 'hideA')          # observation removes or corrupts task-A information (by construction)
INFORMATIVE = ('full', 'alias', 'drift', 'hideA+ref')
N_FEATS = ['rise_rec', 'rise_0', 'gconf', 'ovl1', 'ovl2', 'fdisp', 'fdisp_mod', 'cka', 'erank', 'Bprog', 'LBk', 's', 'Lrec', 'logmat', 'kl_anchor']
O_FEATS = ['d_anchor', 'iota', 'r_anchor', 'eta_mod', 'eta_emp', 'd_corr']
C_FEATS = ['coh', 'chord', 'surplus', 'surplus_frac']
DELTA, B, IOTA_MIN, KAPPA_CONST = 0.02, 4000, 0.5, 100
PG = 'D2:gpm@k'; COMPARATORS = ('sec', 'k100', 'gpm', 'sec+gpm', 'headonly')

def load(p): return [json.loads(l) for l in open(p) if l.strip()]
def admissible(e):
    r = e['runs']; fz = e['pre']['frozen']
    a = e['pre']['rec']['acc'] >= 0.70
    b = r['none']['true']['accB'] >= 0.75 and r['none']['true']['B'] <= fz['B'] - 0.5 and r['none']['true']['B'] <= r['headonly']['true']['B'] - 0.05
    f = r['none']['true']['A'] - fz['A'] >= 0.10
    return bool(a and b and f), dict(A_learned=a, B_learned=b, forgetting_at_stake=f)
def J(e, k, comp='J'): return e['runs'][k]['true'][comp]
def boot(x, seed=0):
    x = np.asarray(x, float); rng = np.random.default_rng(seed); n = len(x)
    bs = np.array([x[rng.integers(0, n, n)].mean() for _ in range(B)]); return dict(mean=float(x.mean()), lo=float(np.percentile(bs, 2.5)), hi=float(np.percentile(bs, 97.5)))
def boot_stat(fn, n, seed=0):
    rng = np.random.default_rng(seed); vals = []
    for _ in range(B):
        idx = rng.integers(0, n, n)
        try: vals.append(fn(idx))
        except ValueError: pass
    vals = np.array(vals); return dict(lo=float(np.percentile(vals, 2.5)), hi=float(np.percentile(vals, 97.5)), n_boot=int(len(vals)))
def feats(E, c, fset, D='D2'): return np.array([[e['conditions'][c][D]['features'][k] for k in fset] for e in E], float)
def y_gpm(E): return np.array([int(J(e, PG) < J(e, 'D2:mu1') - DELTA) for e in E])
def dJ_gpm(E): return np.array([J(e, PG) - J(e, 'D2:mu1') for e in E])
def dmg(E): return np.array([e['true_at_k']['D2']['k']['A'] - e['true_at_k']['D2']['anchor']['A'] for e in E])

def fit(Edev, fset, y, kind):
    X = np.vstack([feats(Edev, c, fset) for c in CONDS]); yy = np.concatenate([y for _ in CONDS]); sc = StandardScaler().fit(X)
    mdl = LogisticRegression(C=1.0, max_iter=2000).fit(sc.transform(X), yy) if kind == 'bin' else Ridge(alpha=10.0).fit(sc.transform(X), yy)
    return lambda Xn: (mdl.predict_proba(sc.transform(Xn))[:, 1] if kind == 'bin' else mdl.predict(sc.transform(Xn)))

def main(hpath, dpath, opath):
    H_all, D_all = load(hpath), load(dpath); S = {}
    adm = [admissible(e) for e in H_all]; H = [e for e, a in zip(H_all, adm) if a[0]]; Dv = [e for e in D_all if admissible(e)[0]]
    S['n_heldout'] = len(H_all); S['n_admissible'] = len(H); S['n_dev_admissible'] = len(Dv)
    S['screen_failures'] = {k: int(sum(not a[1][k] for a in adm)) for k in ('A_learned', 'B_learned', 'forgetting_at_stake')}
    S['branch_identical_all'] = all(e.get('D1_branch_identical') and e.get('D2_branch_identical') for e in H_all)
    S['powered'] = len(H) >= 80
    n = len(H)
    # ---------------- H1: the selected design against the strongest inexpensive comparator ----------------
    means = {k: float(np.mean([J(e, k) for e in H])) for k in COMPARATORS + (PG, 'none', 'replay1000', 'sec+replay1000', 'D2:mu1')}
    means['frozen'] = float(np.mean([e['pre']['frozen']['J'] for e in H]))
    cstar = min(COMPARATORS, key=lambda k: means[k]); d = [J(e, PG) - J(e, cstar) for e in H]; ci = boot(d)
    vs = {k: boot([J(e, PG) - J(e, k) for e in H]) for k in COMPARATORS + ('replay1000',)}
    A_pg, A_sec = np.mean([J(e, PG, 'A') for e in H]), np.mean([J(e, 'sec', 'A') for e in H]); B_pg, B_sec = np.mean([J(e, PG, 'B') for e in H]), np.mean([J(e, 'sec', 'B') for e in H])
    guard_B = bool(B_pg < B_sec); guard_A = bool(A_pg - A_sec <= 0.05)
    h1 = bool(ci['hi'] < 0 and ci['mean'] <= -0.005 and guard_B and guard_A)
    S['H1'] = dict(means=means, strongest_comparator=cstar, diff_vs_strongest=ci, diff_vs_each=vs, A=dict(pg=float(A_pg), sec=float(A_sec)), B=dict(pg=float(B_pg), sec=float(B_sec)),
                   guard_more_new_learning_than_SEC=guard_B, guard_retention_within_0p05_of_SEC=guard_A, verdict='PASS' if h1 else 'FAIL')
    by_mat = {}
    for mat in sorted({e['mat'] for e in H}):
        sub = [e for e in H if e['mat'] == mat]; by_mat[str(mat)] = dict(n=len(sub), **{k: float(np.mean([J(e, k) for e in sub])) for k in (PG,) + COMPARATORS})
    S['H1']['by_maturity'] = by_mat
    # ---------------- H2: the SEC-OBS hypothesis as posed (diagnostic predicts when the stronger intervention is worth it) ----------------
    yd, yh = y_gpm(Dv), y_gpm(H); S['H2'] = dict(prevalence_dev=float(yd.mean()), prevalence_heldout=float(yh.mean()))
    models = {name: fit(Dv, fs, yd, 'bin') for name, fs in (('N', N_FEATS), ('N+O', N_FEATS + O_FEATS))}
    P = {name: {c: mdl(feats(H, c, (N_FEATS if name == 'N' else N_FEATS + O_FEATS))) for c in CONDS} for name, mdl in models.items()}
    def mean_auc(name, idx):
        return float(np.mean([roc_auc_score(yh[idx], P[name][c][idx]) for c in CONDS]))
    allidx = np.arange(n)
    auc = {name: {c: float(roc_auc_score(yh, P[name][c])) for c in CONDS} for name in P}
    S['H2']['auc'] = auc; S['H2']['mean_auc'] = {name: mean_auc(name, allidx) for name in P}
    S['H2']['mean_auc_diff_NO_minus_N'] = dict(mean=S['H2']['mean_auc']['N+O'] - S['H2']['mean_auc']['N'], **boot_stat(lambda idx: mean_auc('N+O', idx) - mean_auc('N', idx), n))
    Jg, Js = np.array([J(e, PG) for e in H]), np.array([J(e, 'D2:mu1') for e in H]); pol = {}
    for name in P:
        Jpol = np.mean([np.where(P[name][c] >= 0.5, Jg, Js) for c in CONDS], axis=0)   # per-episode mean over the eight observation conditions
        pol[name] = dict(J=float(Jpol.mean()), vs_always_intervene=boot(Jpol - Jg), vs_never=boot(Jpol - Js),
                         false_intervention_rate=float(np.mean([np.mean((P[name][c] >= 0.5) & (Jg > Js)) for c in CONDS])),
                         missed_rate=float(np.mean([np.mean((P[name][c] < 0.5) & (yh == 1)) for c in CONDS])))
    S['H2']['policy'] = pol; S['H2']['always_intervene_J'] = float(Jg.mean()); S['H2']['never_J'] = float(Js.mean()); S['H2']['oracle_J'] = float(np.minimum(Jg, Js).mean())
    h2a = S['H2']['mean_auc']['N+O'] >= 0.70; h2b = S['H2']['mean_auc_diff_NO_minus_N']['mean'] >= 0.02 and S['H2']['mean_auc_diff_NO_minus_N']['lo'] > 0
    h2c = pol['N+O']['vs_always_intervene']['mean'] <= -0.002 and pol['N+O']['vs_always_intervene']['hi'] < 0
    n2a = S['H2']['mean_auc']['N'] >= 0.70; n2c = pol['N']['vs_always_intervene']['mean'] <= -0.002 and pol['N']['vs_always_intervene']['hi'] < 0
    S['H2'].update(H2a=bool(h2a), H2b=bool(h2b), H2c=bool(h2c), native_a=bool(n2a), native_c=bool(n2c),
                   verdict='YES-OBSERVATION-AWARE' if (h2a and h2b and h2c) else ('YES-NATIVE-ONLY' if (n2a and n2c) else 'NO'))
    # ---------------- H3: do CRR path quantities add predictive information beyond native diagnostics? ----------------
    S['H3'] = {}
    tgts = {'dJ_gpm': (dJ_gpm(Dv), dJ_gpm(H), 'reg'), 'y_gpm': (yd, yh, 'bin'), 'true_A_rise_at_k': (dmg(Dv), dmg(H), 'reg')}
    for tn, (ydv, yhv, kind) in tgts.items():
        res = {}
        for base, plus in ((N_FEATS, N_FEATS + C_FEATS), (N_FEATS + O_FEATS, N_FEATS + O_FEATS + C_FEATS)):
            mb, mp = fit(Dv, base, ydv, kind), fit(Dv, plus, ydv, kind); pb = {c: mb(feats(H, c, base)) for c in CONDS}; pp = {c: mp(feats(H, c, plus)) for c in CONDS}
            sc = (lambda yy, pr: roc_auc_score(yy, pr)) if kind == 'bin' else (lambda yy, pr: r2_score(yy, pr))
            def diff(idx): return float(np.mean([sc(yhv[idx], pp[c][idx]) - sc(yhv[idx], pb[c][idx]) for c in CONDS]))
            key = 'N+C vs N' if len(base) == len(N_FEATS) else 'N+O+C vs N+O'
            res[key] = dict(base=float(np.mean([sc(yhv, pb[c]) for c in CONDS])), plus=float(np.mean([sc(yhv, pp[c]) for c in CONDS])), diff=diff(allidx), **boot_stat(diff, n))
        S['H3'][tn] = res
    p = S['H3']['dJ_gpm']['N+C vs N']; S['H3']['verdict'] = 'PASS' if (p['diff'] >= 0.02 and p['lo'] > 0) else 'FAIL'
    # ---------------- H4: observation-aware abstention for monitor-driven tuning ----------------
    def jk(e, kap): return J(e, 'none') if float(kap) == 0 else J(e, f'k{int(float(kap))}')
    naive, aware = {}, {}
    for c in CONDS:
        naive[c] = np.array([jk(e, e['conditions'][c]['sweep']['kappa']) for e in H])
        aware[c] = np.array([jk(e, KAPPA_CONST) if e['conditions'][c]['D2']['features']['iota'] < IOTA_MIN else jk(e, e['conditions'][c]['sweep']['kappa']) for e in H])
    fl = np.mean([aware[c] - naive[c] for c in FLAGGED], axis=0); inf = np.mean([aware[c] - naive[c] for c in INFORMATIVE], axis=0)
    flagged_ci, inf_ci = boot(fl), boot(inf)
    detect = np.array([[e['conditions'][c]['D2']['features']['iota'] < IOTA_MIN for c in CONDS] for e in H])
    tpr = float(detect[:, [CONDS.index(c) for c in FLAGGED]].mean()); tnr = float(1 - detect[:, [CONDS.index(c) for c in INFORMATIVE]].mean()); bal = 0.5*(tpr + tnr)
    const = np.array([J(e, 'k100') for e in H])
    S['H4'] = dict(naive_sweep={c: float(naive[c].mean()) for c in CONDS}, aware_sweep={c: float(aware[c].mean()) for c in CONDS}, constant_k100=float(const.mean()),
                   gain_on_flagged=flagged_ci, change_on_informative=inf_ci, detection=dict(tpr=tpr, tnr=tnr, balanced_accuracy=bal,
                   flagged_rate_by_condition={c: float(detect[:, i].mean()) for i, c in enumerate(CONDS)}),
                   aware_vs_constant=boot(np.mean([aware[c] for c in CONDS], axis=0) - const))
    S['H4']['verdict'] = 'PASS' if (flagged_ci['mean'] <= -0.02 and flagged_ci['hi'] < 0 and inf_ci['hi'] < 0.005 and bal >= 0.90) else 'FAIL'
    # ---------------- descriptive (not registered as hypotheses) ----------------
    desc = {}
    desc['candidate3_direction_calibration'] = {D: {t: {c: float(np.mean([(e['conditions'][c][D]['c3'][t]['true'] or {'J': J(e, 'sec' if D == 'D1' else 'D2:mu1')})['J'] for e in H])) for c in CONDS} for t in ('a', 'b')} for D in ('D1', 'D2')}
    grid = (3, 10, 30, 100, 300, 1000, 3000)
    desc['C1_maturity'] = {str(mat): dict(median_kSEC_over_kstar=float(np.median([e['pre']['kSEC']/grid[int(np.argmin([J(e, f'k{g}') for g in grid]))] for e in H if e['mat'] == mat])),
                                         SEC_regret_vs_best_constant=float(np.mean([J(e, 'sec') - min(J(e, f'k{g}') for g in grid) for e in H if e['mat'] == mat]))) for mat in sorted({e['mat'] for e in H})}
    desc['worlds'] = dict(W6_full_obs_intervention_worth_it=dict(n=int(yh.sum()), sensitivity_NO=float(np.mean(P['N+O']['full'][yh == 1] >= 0.5)) if yh.sum() else None),
                          W8_full_obs_SEC_sufficient=dict(n=int((yh == 0).sum()), false_intervention_NO=float(np.mean(P['N+O']['full'][yh == 0] >= 0.5)) if (yh == 0).sum() else None),
                          W9_hideA_vs_W5_hideA_ref_true_A_rise_R2={k: dict(hideA=float(r2_score(dmg(H), fit(Dv, fs, dmg(Dv), 'reg')(feats(H, 'hideA', fs)))), hideA_ref=float(r2_score(dmg(H), fit(Dv, fs, dmg(Dv), 'reg')(feats(H, 'hideA+ref', fs)))))
                                                                    for k, fs in (('N', N_FEATS), ('N+O', N_FEATS + O_FEATS))})
    desc['recovery_head_refit_A'] = dict(none_true_A=float(np.mean([J(e, 'none', 'A') for e in H])), none_refit_on_64_buffer=float(np.mean([e['refit_A']['none'] for e in H])), anchor_A=float(np.mean([e['pre']['frozen']['A'] for e in H])))
    desc['costs_seconds'] = dict(A_train=float(np.mean([e['pre']['seconds_train'] for e in H])), sec_calibration=float(np.mean([e['pre']['seconds_calibration'] for e in H])), gpm_bases=float(np.mean([e['pre']['seconds_gpm'] for e in H])),
                                 run_sec=float(np.mean([e['runs']['sec']['seconds'] for e in H])), run_pg=float(np.mean([e['runs'][PG]['seconds'] for e in H])), pg_projection=float(np.mean([e['runs'][PG]['seconds_gpm'] for e in H])),
                                 run_k100=float(np.mean([e['runs']['k100']['seconds'] for e in H])), sweep_8_runs=float(np.mean([sum(e['runs'][f'k{g}']['seconds'] for g in grid) + e['runs']['none']['seconds'] for e in H])),
                                 replay1000=float(np.mean([e['runs']['replay1000']['seconds'] for e in H])), diagnostics_per_condition=float(np.mean([e['conditions'][c]['D2']['features']['_seconds'] + e['conditions'][c]['seconds_fobs'] for e in H for c in CONDS])),
                                 episode=float(np.mean([e['seconds_episode'] for e in H])))
    desc['stored_floats'] = H[0]['stored_floats'] if H else None
    S['descriptive'] = desc
    json.dump(S, open(opath, 'w'), indent=1)
    print(json.dumps({k: (v.get('verdict') if isinstance(v, dict) and 'verdict' in v else v) for k, v in S.items() if k != 'descriptive'}, indent=1))

if __name__ == '__main__': main(sys.argv[1], sys.argv[2], sys.argv[3])
