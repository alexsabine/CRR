"""P18-PROV-FLAME power plan (draft helper; no simulation). Reads the development rows studies/P18-LOOP1-2026-10-08/outputs/loop_runs.jsonl
(200 seeds per world, designed confounder geometry) and writes outputs/power_plan.json with:
  1. development contrasts on the registered binary endpoint (timely detection: first alarm in [div - 5, div + W] at the aligned-world
     5 % threshold), for W in {3, 5, 10, 20}, in the confounded worlds (pooled and each) and the clean worlds; the continuous score
     (1 - delay/80) for reference; prov - inshift; prov - bbsd discordance; 95 % percentile bootstrap intervals (B 4000, default_rng(0));
  2. the exo world's alarm rates (Wilson 95 % intervals);
  3. localisation, provenance against the intervention rival (paired, pooled confounded worlds);
  4. winner's-curse corrections: the conditional MLE of a normal estimate reported because z > 1.96, per world and pooled;
     and the geometry dilution implied by the declared confounder distribution (25 % of drawn confounders lie wholly off the published
     top-2 support, against 6/7 in the designed worlds; provworld_draft.py geomstats);
  5. a Monte Carlo power grid for the registered decision rule (RESULT: L > 0 and estimate >= delta; FAIL: U < 0; REDUCES: 0 <= U < delta;
     otherwise NOT DECIDABLE) over planning scenarios, discordance levels and an interval-inflation factor for threshold uncertainty;
  6. the CPU cost of the planned frozen run and of the pre-freeze pilot, from 0.55 CPU-s per simulation (20 CPU-min / 2200 simulations
     in the development run; 0.48 CPU-s measured for one simulation on 2026-10-09).
Run: python3 -I power_plan.py   (a few seconds)."""
import sys; sys.dont_write_bytecode = True
import json, math, pathlib, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; DEV = HERE.parent / 'P18-LOOP1-2026-10-08' / 'outputs'; (HERE / 'outputs').mkdir(exist_ok=True)
R = [json.loads(l) for l in open(DEV / 'loop_runs.jsonl')]
H, EARLY, DELTA, DELTA_LOC = 80, 5, 0.02, 0.05
CONF, CLEAN = ['game_theta+exo', 'game_expl+exo'], ['game_theta', 'game_expl']
SEC_PER_SIM, MARGIN = 0.55, 1.5

def Phi(x): return 0.5*(1 + math.erf(x/math.sqrt(2)))
def log_sf(y):
    """log(1 - Phi(y)), stable for large y"""
    v = 0.5*math.erfc(y/math.sqrt(2))
    if v > 0: return math.log(v)
    return -y*y/2 - math.log(y*math.sqrt(2*math.pi))   # Mills-ratio asymptote
def timely(r, k, W): a, d = r['alarm_' + k], r['div']; return int(a is not None and d - EARLY <= a <= d + W)
def cont(r, k): a, d = r['alarm_' + k], r['div']; return 0.0 if a is None or a < d - EARLY else 1 - (max(a, d) - d)/H
def boot(x, B=4000):
    x = np.asarray(x, float); rng = np.random.default_rng(0); m = x[rng.integers(0, len(x), (B, len(x)))].mean(1)
    return dict(mean=round(float(x.mean()), 4), lo=round(float(np.percentile(m, 2.5)), 4), hi=round(float(np.percentile(m, 97.5)), 4), sd=round(float(x.std(ddof=1)), 4), n=len(x))
def wilson(k, n, z=1.96):
    p = k/n; c = (p + z*z/(2*n))/(1 + z*z/n); h = z*math.sqrt(p*(1 - p)/n + z*z/(4*n*n))/(1 + z*z/n); return [round(p, 4), round(c - h, 4), round(c + h, 4)]
def rows(worlds): return [r for r in R if r['world'] in worlds and r['div'] is not None]

def dev_contrasts():
    out = {}
    for name, ws in (('confounded_pooled', CONF), ('game_theta+exo', ['game_theta+exo']), ('game_expl+exo', ['game_expl+exo']), ('clean_pooled', CLEAN)):
        rr = rows(ws); e = dict(n=len(rr))
        for W in (3, 5, 10, 20):
            d = [timely(r, 'prov', W) - timely(r, 'bbsd', W) for r in rr]; di = [timely(r, 'prov', W) - timely(r, 'inshift', W) for r in rr]
            e[f'W{W}'] = dict(P_prov=round(float(np.mean([timely(r, 'prov', W) for r in rr])), 4), P_bbsd=round(float(np.mean([timely(r, 'bbsd', W) for r in rr])), 4),
                              P_inshift=round(float(np.mean([timely(r, 'inshift', W) for r in rr])), 4), P_prov_abl=round(float(np.mean([timely(r, 'prov_abl', W) for r in rr])), 4),
                              prov_minus_bbsd=boot(d), p_plus=round(float(np.mean(np.array(d) > 0)), 4), p_minus=round(float(np.mean(np.array(d) < 0)), 4),
                              prov_minus_inshift=boot(di), prov_minus_prov_abl=boot([timely(r, 'prov', W) - timely(r, 'prov_abl', W) for r in rr]))
        e['continuous_prov_minus_bbsd'] = boot([cont(r, 'prov') - cont(r, 'bbsd') for r in rr]); out[name] = e
    return out

def outcome_breakdown():
    """where the development contrast comes from: per-unit (prov, bbsd) outcome categories and delays when both detect"""
    def cat(r, k):
        a, d = r['alarm_' + k], r['div']
        return 'miss' if a is None else ('early' if a < d - EARLY else 'detected')
    out = {}
    for name, ws in (('confounded_pooled', CONF), ('clean_pooled', CLEAN)):
        rr = rows(ws); c = {}
        for r in rr: key = f"{cat(r, 'prov')}/{cat(r, 'bbsd')}"; c[key] = c.get(key, 0) + 1
        dl = np.array([(r['alarm_prov'] - r['div'], r['alarm_bbsd'] - r['div']) for r in rr if cat(r, 'prov') == cat(r, 'bbsd') == 'detected'], float)
        out[name] = dict(n=len(rr), categories_prov_slash_bbsd=dict(sorted(c.items())), both_detected=len(dl), mean_delay_prov=round(float(dl[:, 0].mean()), 3),
                         mean_delay_bbsd=round(float(dl[:, 1].mean()), 3), frac_prov_earlier=round(float(np.mean(dl[:, 0] < dl[:, 1])), 3),
                         frac_prov_later=round(float(np.mean(dl[:, 0] > dl[:, 1])), 3), delay_p95_prov=float(np.percentile(dl[:, 0], 95)), delay_p95_bbsd=float(np.percentile(dl[:, 1], 95)),
                         delay_max_prov=float(dl[:, 0].max()), delay_max_bbsd=float(dl[:, 1].max()))
    return out

def exo_rates():
    rr = [r for r in R if r['world'] == 'exo']; n = len(rr)
    return {k: wilson(sum(r['alarm_' + k] is not None for r in rr), n) for k in ('prov', 'bbsd', 'inshift', 'prov_abl', 'proxy', 'calib')} | dict(n=n,
            paired_prov_minus_bbsd=boot([(r['alarm_prov'] is not None) - (r['alarm_bbsd'] is not None) for r in rr]))

def localisation():
    rr = [r for r in rows(CONF) if 'loc' in r and 'intervention' in r['loc']]; G = [r['G'][0] for r in rr]
    p = np.array([r['loc']['prov'] == g for r, g in zip(rr, G)], float); iv = np.array([r['loc']['intervention'] == g for r, g in zip(rr, G)], float)
    ev = np.array([r['loc']['event'] == g for r, g in zip(rr, G)], float); d = p - iv
    return dict(n=len(rr), acc_prov=round(float(p.mean()), 4), acc_intervention=round(float(iv.mean()), 4), acc_event=round(float(ev.mean()), 4),
                prov_minus_intervention=boot(d), discordance=round(float(np.mean(d != 0)), 4),
                intervention_target_cost_mean=round(float(np.mean([r['loc']['intervention_target_cost'] for r in rr])), 4))

def cond_mle(x, se, c=1.96):
    """conditional MLE of mu for X ~ N(mu, se^2) observed only because X/se > c (Zhong and Prentice 2008 style truncation correction)"""
    grid = np.linspace(-3*abs(x) - 3*se, x + 3*se, 20001)
    ll = [-0.5*((x - m)/se)**2 - log_sf(c - m/se) for m in grid]; return float(grid[int(np.argmax(ll))])

def winners_curse(dc):
    out = {}
    for name in ('game_theta+exo', 'game_expl+exo', 'confounded_pooled'):
        for key in ('continuous_prov_minus_bbsd',):
            b = dc[name][key]; se = b['sd']/math.sqrt(b['n']); m = cond_mle(b['mean'], se)
            out[f'{name}:{key}'] = dict(observed=b['mean'], se=round(se, 5), z=round(b['mean']/se, 2), conditional_mle=round(m, 4), shrink_ratio=round(m/b['mean'], 3))
        b = dc[name]['W5']['prov_minus_bbsd']; se = b['sd']/math.sqrt(b['n']); m = cond_mle(b['mean'], se)
        out[f'{name}:W5'] = dict(observed=b['mean'], se=round(se, 5), z=round(b['mean']/se, 2), conditional_mle=round(m, 4), shrink_ratio=round(m/b['mean'], 3))
    return out

def classify(dhat, se, delta):
    L, U = dhat - 1.96*se, dhat + 1.96*se
    res = (L > 0) & (dhat >= delta); fail = U < 0; red = (U >= 0) & (U < delta); nd = ~(res | fail | red)
    return res, red, fail, nd

def power(delta_true, disc, n, delta=DELTA, infl=1.0, reps=20000, seed=1):
    """Monte Carlo of the paired binary contrast: P(d=+1) = (disc + delta_true)/2, P(d=-1) = (disc - delta_true)/2"""
    pp, pm = (disc + delta_true)/2, (disc - delta_true)/2
    if pm < 0: return None
    rng = np.random.default_rng(seed); c = rng.multinomial(n, [pp, pm, 1 - pp - pm], size=reps); dhat = (c[:, 0] - c[:, 1])/n
    var = (c[:, 0] + c[:, 1])/n - dhat**2; se = infl*np.sqrt(np.maximum(var, 1e-12)/n)
    res, red, fail, nd = classify(dhat, se, delta)
    return dict(RESULT=round(float(res.mean()), 3), REDUCES=round(float(red.mean()), 3), FAIL=round(float(fail.mean()), 3), NOT_DECIDABLE=round(float(nd.mean()), 3))

def n_analytic(delta0, delta1, disc, delta=DELTA, infl=1.0, za=1.96, zb=1.2816):
    """smallest n with P(U < delta | delta0) >= 0.9 and P(L > 0 and dhat >= delta | delta1) >= 0.9 (normal approximation)"""
    sd0 = math.sqrt(disc - delta0**2); sd1 = math.sqrt(disc - delta1**2)
    n_red = ((za + zb)*infl*sd0/(delta - delta0))**2
    n_res = max((zb*infl*sd1/(delta1 - delta))**2, ((za + zb)*infl*sd1/delta1)**2)
    return dict(n_for_REDUCES_at_delta0=math.ceil(n_red), n_for_RESULT_at_delta1=math.ceil(n_res), n=math.ceil(max(n_red, n_res)))

def main():
    dc = dev_contrasts(); wc = winners_curse(dc)
    conf5 = dc['confounded_pooled']['W5']; clean5 = dc['clean_pooled']['W5']['prov_minus_bbsd']['mean']; dev5 = conf5['prov_minus_bbsd']['mean']
    disc_dev = conf5['p_plus'] + conf5['p_minus']
    f_dev, f_drawn = 6/7, 0.25
    scen = {'S1_designed_as_observed': dev5,
            # the development edge was reported per world on the continuous score because each interval excluded 0 (z 2.8 and 2.2);
            # the mean of the two per-world conditional-MLE shrink ratios is applied to the pooled W = 5 estimate
            'S2_selection_corrected': dev5*float(np.mean([max(0.0, wc[f'{w}:continuous_prov_minus_bbsd']['shrink_ratio']) for w in CONF])),
            'S3_geometry_diluted': clean5 + (dev5 - clean5)*f_drawn/f_dev,
            'S4_clean_world_tie': clean5,
            'design_alternative_2delta': 2*DELTA}
    scen = {k: round(float(v), 4) for k, v in scen.items()}
    grid_n = [500, 1000, 2000, 3000, 4000, 5000, 6200, 8000, 12000]; discs = sorted({round(disc_dev, 4), 0.10, 0.15})
    pw = {f'{s}|disc={dsc}|infl={inf}': {n: power(v, dsc, n, infl=inf) for n in grid_n}
          for s, v in scen.items() for dsc in discs for inf in (1.0, 1.15)}
    req = {f'disc={dsc}|infl={inf}': n_analytic(clean5, 2*DELTA, dsc, infl=inf) for dsc in discs for inf in (1.0, 1.15)}
    N_CONF = 6200; N_CONF_DRAW_CAP = 6800   # diverged units; meets the disc 0.10, inflation 1.15 target (6175)
    # owner decision aid only: the registered delta is DELTA; other values show what the choice costs (n) and how the planning scenarios would fall
    delta_sens = {f'delta={dl}': dict(required_n_disc_0p10_infl_1p15=n_analytic(clean5, 2*dl, 0.10, delta=dl, infl=1.15),
                                      outcomes_at_registered_n_disc_0p10_infl_1p15={s: power(v, 0.10, N_CONF, delta=dl, infl=1.15) for s, v in scen.items()})
                  for dl in (0.01, 0.02, 0.03, 0.05)}
    def arms_cost(arms):
        tot = sum(a[2] for a in arms); h = tot*SEC_PER_SIM/3600
        return dict(arms=[dict(arm=a[0], units=a[1], sims=a[2]) for a in arms], total_sims=tot, cpu_hours=round(h, 2), cpu_hours_with_margin=round(h*MARGIN, 2),
                    wall_hours_on_4_cores_with_margin=round(h*MARGIN/4, 2))
    # (arm, units, simulations); a probed localisation needs a second full simulation of the same unit
    frozen = arms_cost([('calibration, aligned', 2000, 2000), ('false-alarm validation, aligned', 1000, 1000),
                        ('confounded drawn family: simulation (draw cap)', N_CONF_DRAW_CAP, N_CONF_DRAW_CAP), ('confounded drawn family: intervention probe m=6', N_CONF, N_CONF),
                        ('S13 probe m=2, first 1000 diverged units', 1000, 1000), ('S13 alarm-timed probe, first 1000 diverged units', 1000, 1000),
                        ('exo-only drawn (must-not-alarm)', 1000, 1000), ('clean gaming positive control (+probe)', 500, 1000),
                        ('S8 designed geometry, fresh seeds (+probe)', 1000, 2000), ('S9 drawn gameable channel', 1000, 1000),
                        ('SF3 confounder on the published support', 500, 500), ('SF5 open loop, paired with the first 2000 confounded units (+probe)', 2000, 4000)])
    frozen['fits_2_cpu_days'] = frozen['cpu_hours_with_margin'] <= 48
    pilot = arms_cost([('calibration, aligned', 1000, 1000), ('false-alarm check, aligned', 500, 500), ('confounded drawn family (+probe)', 500, 1000),
                       ('exo-only drawn', 300, 300), ('clean gaming positive control (+probe)', 200, 400), ('designed geometry (+probe)', 200, 400),
                       ('SF3 confounder on the published support', 200, 200), ('SF5 open loop, paired (+probe)', 200, 400)])
    worst = arms_cost([('confounded family raised to the 20000-unit ceiling of the n-update rule (extra simulation + probe)', 20000 - N_CONF, 2*(20000 - N_CONF))])
    dev_run = dict(sims=200 + 6*200 + 4*200, cpu_minutes_reported=20, sec_per_sim_implied=round(20*60/2200, 3), sec_per_sim_measured_2026_10_09=0.481)
    loc = localisation(); exo = exo_rates()
    precision = dict(
        H_loc_se_at_registered_n=round(loc['prov_minus_intervention']['sd']/math.sqrt(N_CONF), 5),
        H_loc_halfwidth_at_registered_n=round(1.96*loc['prov_minus_intervention']['sd']/math.sqrt(N_CONF), 5),
        C4_exo_wilson_n1000_at_dev_rate=wilson(round(exo['prov'][0]*1000), 1000), C4_exo_wilson_n1000_at_0p05=wilson(50, 1000),
        C2_far_wilson_n1000_at_0p05=wilson(50, 1000), S8_designed_se_n1000=round(conf5['prov_minus_bbsd']['sd']/math.sqrt(1000), 5),
        effect_0p019_vs_delta_n_needed_for_REDUCES=math.ceil(((1.96*1.15*math.sqrt(0.10 - 0.019**2))/(DELTA - 0.019))**2),
        primary_se_at_registered_n_disc0p10_infl1p15=round(1.15*math.sqrt(0.10)/math.sqrt(N_CONF), 5))
    out = dict(delta=DELTA, delta_loc=DELTA_LOC, precision=precision, early_tolerance=EARLY, development_contrasts=dc, outcome_breakdown=outcome_breakdown(), exo_development=exo, localisation_development=loc,
               winners_curse=wc, geometry_dilution=dict(p_off_top2_designed=round(f_dev, 4), p_off_top2_drawn=f_drawn), planning_scenarios_W5=scen, delta_sensitivity=delta_sens,
               discordance_development_W5=round(disc_dev, 4), power_grid=pw, required_n=req, n_confounded_registered=N_CONF, n_confounded_draw_cap=N_CONF_DRAW_CAP,
               cost=dict(sec_per_sim=SEC_PER_SIM, margin=MARGIN, development_run=dev_run, frozen_run=frozen, pilot=pilot,
                         budget_cpu_hours_OD12=48, n_update_ceiling_extra=worst, total_with_margin=round(frozen['cpu_hours_with_margin'] + pilot['cpu_hours_with_margin'], 2),
                         worst_case_with_margin=round(frozen['cpu_hours_with_margin'] + pilot['cpu_hours_with_margin'] + worst['cpu_hours_with_margin'], 2)))
    json.dump(out, open(HERE / 'outputs' / 'power_plan.json', 'w'), indent=1)
    short = dict(planning_scenarios_W5=scen, discordance_development_W5=out['discordance_development_W5'], required_n=req, winners_curse=wc,
                 key_power={k: pw[k][N_CONF] for k in pw if 'infl=1.15' in k}, cost=out['cost'])
    print(json.dumps(short, indent=1))

if __name__ == '__main__': main()
