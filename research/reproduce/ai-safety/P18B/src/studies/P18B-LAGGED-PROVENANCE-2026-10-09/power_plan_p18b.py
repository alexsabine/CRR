"""P18B-LAGGED-PROVENANCE power and cost plan (DESIGN DRAFT helper; no simulation; a few seconds).

There are no development data for the P18B world yet. This script therefore
  1. gives n as a function of the discordance D that the pre-freeze pilot will measure (the registered n-rule), for the primary
     attribution endpoint (balanced accuracy, margin 0.05) and the secondary detection endpoint (timely detection, margin 0.02);
  2. runs a Monte Carlo of the registered verdict partitions (superiority and non-inferiority rules) at those n, over planning
     scenarios; the only scenario values taken from data are from the stylised surrogate (outputs/surrogate_check.json), which is
     not the world, and they are labelled as such;
  3. gives the n for the equivalence (TOST) checks of the negative direction;
  4. costs the pilot and the frozen run in CPU-hours from outputs/timing.json and checks them against the 2 CPU-day budget (OD-12).
Writes outputs/power_plan.json. Run: python3 -I power_plan_p18b.py"""
import sys; sys.dont_write_bytecode = True
import json, math, pathlib, numpy as np
HERE = pathlib.Path(__file__).resolve().parent; OUT = HERE / 'outputs'
Z_A, Z_B, Z_TOST = 1.959964, 1.281552, 1.644854
DELTA_A, DELTA_D, INFL = 0.05, 0.02, 1.15
SUR = json.load(open(OUT / 'surrogate_check.json')); TIM = json.load(open(OUT / 'timing.json'))

def n_tie(D, delta, infl=INFL):
    """paired binary contrast: n so that at true difference 0, P(U < delta) >= 0.9, and at -delta, P(U < 0) >= 0.9 (same bound)"""
    return math.ceil(D*infl**2*((Z_A + Z_B)/delta)**2)
def n_two_delta(D, delta, infl=INFL):
    """n so that at true difference 2*delta, P(L > 0 and estimate >= delta) >= 0.9 (approximately: both conditions at 0.9)"""
    se = min(delta/Z_B, 2*delta/(Z_A + Z_B)); return math.ceil(D*infl**2/se**2)
def n_ba(De, Dn, delta=DELTA_A, infl=INFL):
    """balanced-accuracy contrast with n/2 units of each class: Var = (De + Dn)/(2n); n so that SE <= delta/(Z_A + Z_B)"""
    return math.ceil((De + Dn)/2*infl**2*((Z_A + Z_B)/delta)**2)
def n_tost(D, delta, infl=INFL):
    """paired equivalence with 90 % interval inside (-delta, delta): at true 0, P(pass) >= 0.9"""
    return math.ceil(D*infl**2*((2*Z_TOST)/delta)**2)

def partition(true, se, delta, rule, reps=20000, seed=0):
    g = np.random.default_rng(seed); est = g.normal(true, se, reps); lo, hi = est - Z_A*se, est + Z_A*se
    if rule == 'superiority':
        fail = hi < 0; red = (hi >= 0) & (hi < delta); res = (lo > 0) & (est >= delta); nd = ~(fail | red | res)
        return dict(RESULT=round(float(res.mean()), 3), REDUCES=round(float(red.mean()), 3), FAIL=round(float(fail.mean()), 3), NOT_DECIDABLE=round(float(nd.mean()), 3))
    ni = lo > -delta; inf = hi < -delta; nd = ~(ni | inf)
    return dict(RESULT_noninferior=round(float(ni.mean()), 3), FAIL_inferior=round(float(inf.mean()), 3), NOT_DECIDABLE=round(float(nd.mean()), 3))

def main():
    out = dict(delta_attribution=DELTA_A, delta_detection=DELTA_D, interval_inflation=INFL, alpha_two_sided=0.05)
    # 0. development divergence timing (P18-LOOP1 world, read only): basis of the surrogate's stylised divergence round tau + 2
    R = [json.loads(l) for l in open(HERE.parent / 'P18-LOOP1-2026-10-08' / 'outputs' / 'loop_runs.jsonl')]
    out['development_div_minus_tau'] = {w: dict(n=len(dd), quantiles_0_10_50_90_100=[float(q) for q in np.percentile(dd, [0, 10, 50, 90, 100])])
                                        for w in ('game_theta', 'game_expl', 'game_theta+exo', 'game_expl+exo')
                                        for dd in [[r['div'] - r['tau'] for r in R if r['world'] == w and r['div'] is not None]]}
    # 1. registered n-rules
    out['n_rule_attribution'] = dict(rule='n_A = max over gating attribution contrasts of ceil((De + Dn)/2 * 1.15^2 * ((1.96 + 1.2816)/0.05)^2), De and Dn the '
                                     'pilot discordances in route-e and non-e units rounded up to 0.05; floor 2000, cap 6000 diverged units in the attribution mix',
                                     grid={f'De={De},Dn={Dn}': n_ba(De, Dn) for De in (0.2, 0.3, 0.45, 0.6) for Dn in (0.05, 0.15, 0.25)})
    out['n_rule_detection'] = dict(rule='n_main = max over gating detection contrasts of ceil(D * 1.15^2 * ((1.96 + 1.2816)/0.02)^2), D the pilot discordance rounded up '
                                   'to 0.05; floor 6000, cap 15000 diverged route-e units', grid={f'D={D}': dict(n_tie=n_tie(D, DELTA_D), n_two_delta=n_two_delta(D, DELTA_D))
                                                                                                   for D in (0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5)})
    # 2. planning scenarios and verdict partitions
    att = SUR['attribution']['by_condition']; e, th = att['e_drawn'], att['theta_drawn']
    sur_ba = SUR['attribution']['balanced_accuracy_e_vs_theta']
    De_tw = max(abs(e['passive_ri_yes'] - e['twin_jump_yes']), 0.0); Dn_tw = max(abs(th['passive_ri_yes'] - th['twin_jump_yes']), 0.0)
    De_plan, Dn_plan = 0.45, 0.15; nA = max(2000, n_ba(De_plan, Dn_plan)); se_A = INFL*math.sqrt((De_plan + Dn_plan)/(2*nA))
    out['attribution_planning'] = dict(
        stylised_surrogate=dict(source='outputs/surrogate_check.json (not the world)', passive_ri_BA=sur_ba['passive_ri_yes'], twin_jump_BA=sur_ba['twin_jump_yes'],
                                passive_minus_twin=round(sur_ba['passive_ri_yes'] - sur_ba['twin_jump_yes'], 4),
                                discordance_lower_bounds=dict(route_e=round(De_tw, 4), non_e=round(Dn_tw, 4))),
        planning_discordance=dict(route_e=De_plan, non_e=Dn_plan, note='conservative; the lower bounds above assume nested decisions'),
        n_A=nA, se=round(se_A, 4),
        superiority_vs_twin_or_projection={f'true={d}': partition(d, se_A, DELTA_A, 'superiority') for d in (-0.1425, -0.05, 0.0, 0.05, 0.1)},
        noninferiority_vs_intervention={f'true={d}': partition(d, se_A, DELTA_A, 'noninferiority') for d in (-0.2, -0.1, -0.05, 0.0, 0.05)})
    det = SUR['detection_by_statistic']; nM = 6000; seD = lambda D: INFL*math.sqrt(D/nM)
    out['detection_planning'] = dict(
        stylised_surrogate=dict(source='outputs/surrogate_check.json (not the world)', lag_ri_timely=det['selfnorm']['timely_rate_route_e_drawn'],
                                lag_mb_timely=det['floor']['timely_rate_route_e_drawn'], lag_mb_phantom_alarm_rate=det['floor']['phantom_alarm_rate_under_reentry'],
                                lag_mb_alarm_rate_telegraph_no_gaming=det['floor']['alarm_rate_telegraph'],
                                development_level_detectors_timely_confounded='P18-PROV-FLAME power_plan.json: prov 0.920, bbsd 0.8675 (designed geometry, LOOP1 world)'),
        n_main=nM, partitions={f'D={D},true={d}': partition(d, seD(D), DELTA_D, 'superiority') for D in (0.15, 0.3) for d in (-0.5, -0.02, 0.0, 0.02, 0.04)})
    # 3. negative direction: equivalence checks
    out['tost'] = dict(rule='90 % interval inside (-delta, delta); n so that at true 0 P(pass) >= 0.9',
                       detection={f'D={D}': n_tost(D, DELTA_D) for D in (0.02, 0.04, 0.06, 0.1)},
                       attribution_BA_vs_half=dict(note='BA estimated from n/2 units per class with yes-rate about 0.05: SE about sqrt(0.0475/n) for n units in all',
                                                   n_for_se_le_delta_over_3_29=math.ceil(0.0475/(DELTA_A/(2*Z_TOST))**2)))
    # 4. cost
    sps = 0.6; margin = 1.5; probe_sps = 0.5
    def cost(arms):
        sims = sum(a[1] for a in arms); h = sims*sps/3600; return dict(arms=[dict(arm=a[0], sims=a[1]) for a in arms], sims=sims, cpu_hours=round(h, 2),
                                                                     cpu_hours_with_margin=round(h*margin, 2), wall_hours_on_4_cores_with_margin=round(h*margin/4, 2))
    pilot = [('cal: no gaming, drawn nuisance, drawn publisher', 1000), ('far: as cal', 500), ('main: route e, drawn (about 1500 draws)', 1500),
             ('main probes: first 400 diverged', 400), ('theta, paired with main i < 400', 400), ('open, paired with main i < 400', 400), ('theta and open probes, 200 each', 400),
             ('det: deterministic publisher, route e', 300), ('nogame: drawn nuisance only', 500), ('pos: maximal publication variation, no nuisance (+ probes)', 600)]
    frozen = [('cal', 2000), ('far', 1000), ('main: route e, drawn; draws for 6000 diverged at a divergence rate of 0.8', 7500), ('main probes: first 1000 diverged (attribution)', 1000),
              ('theta, paired with main i < 2000 (N2 and attribution)', 2000), ('open, paired with main i < 2000 (N3 and attribution)', 2000),
              ('theta and open probes: 500 diverged each', 1000), ('det: deterministic publisher; route e 1000, theta 500, open 500 (N1)', 2000),
              ('nogame: drawn nuisance, no gaming (C4)', 2000), ('pos: route e 500, theta 250, open 250 (+ probes)', 2000),
              ('S-designed: designed smooth geometry, route e', 1000), ('S-tele: telegraph always on, on G, magnitude drawn', 1000),
              ('S-noise: publication-noise mechanism, route e', 1000), ('S-stale: stale-version mechanism, route e', 1000),
              ('S-probe-det: always-on probe detector on main i < 1000 (probed trajectories)', 1000), ('S-alarm-timed attribution probes, first 1000 diverged', 1000)]
    worst_extra = [('main raised to 15000 diverged', 11250), ('attribution mix raised to 6000 (probes and paired units)', 8000)]
    out['cost'] = dict(sec_per_sim_used=sps, margin=margin, measured=TIM, note='0.6 CPU-s per simulation including all statistics and B = 999 randomisation redraws '
                       '(measured 0.485 + 0.043 + 0.009 s); a probed simulation counts as one simulation',
                       pilot=cost(pilot), frozen=cost(frozen), worst_case_extra=cost(worst_extra),
                       scoring='two-level bootstrap, B = 4000, on stored statistic paths and attribution scores: about 0.5 CPU-hour (estimate; not measured)')
    tot = out['cost']['pilot']['cpu_hours_with_margin'] + out['cost']['frozen']['cpu_hours_with_margin'] + 0.5
    worst = tot + out['cost']['worst_case_extra']['cpu_hours_with_margin']
    out['cost']['total_cpu_hours_with_margin'] = round(tot, 2); out['cost']['worst_case_cpu_hours_with_margin'] = round(worst, 2)
    out['cost']['fits_2_cpu_days'] = bool(worst <= 48); out['cost']['headroom_factor_worst_case'] = round(48/worst, 1)
    json.dump(out, open(OUT / 'power_plan.json', 'w'), indent=1); print(json.dumps(out, indent=1))

if __name__ == '__main__': main()
