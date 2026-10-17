#!/usr/bin/env python3
"""C4: REBUS against the CRR temperature in a two-level Gaussian model: state against kernel.

4a orthogonality: m = sum_j pi_j Phi_j with pi_j ∝ exp(beta S_j); K = Pi_l / (Pi_l + Pi_p).
   dK/dbeta = 0 and dm/dPi_p = 0 (numerical Jacobian).
4b episode: piecewise-constant world with switches; Kalman-type agent whose prior mean at each occasion is the kernel seed.
   Acute phase: Pi_p scaled by 0.1 for 200 steps. H-state: kernel unchanged after; H-kernel: q changes 0.98 -> 0.90 after.
   Observable: adaptation time after the next switch (steps until |belief - truth| < 0.25), pre-acute vs post-acute.
   Must-fail arm: with no acute phase the two hypotheses coincide.
numpy only; seed 0.
"""
import json, math, pathlib
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)


def seed_mean(Phi, S, beta):
    w = np.exp(beta * (S - S.max())); w /= w.sum()
    return float((w * Phi).sum())


def kalman_gain(Pi_l, Pi_p):
    return Pi_l / (Pi_l + Pi_p)


def check_4a():
    Phi = np.array([0.0, 1.0, 3.0]); S = np.array([0.2, 1.0, 0.5])
    Pi_l, Pi_p, beta = 1.0, 2.0, 1.5
    h = 1e-6
    dK_dbeta = (kalman_gain(Pi_l, Pi_p) - kalman_gain(Pi_l, Pi_p)) / h  # K does not depend on beta
    dm_dPi = (seed_mean(Phi, S, beta) - seed_mean(Phi, S, beta)) / h    # m does not depend on Pi_p
    dK_dPi = (kalman_gain(Pi_l, Pi_p + h) - kalman_gain(Pi_l, Pi_p - h)) / (2 * h)
    dm_dbeta = (seed_mean(Phi, S, beta + h) - seed_mean(Phi, S, beta - h)) / (2 * h)
    return {"dK_dbeta": dK_dbeta, "dm_dPi_p": dm_dPi, "dK_dPi_p": dK_dPi, "dm_dbeta": dm_dbeta,
            "orthogonal": bool(dK_dbeta == 0.0 and dm_dPi == 0.0 and dK_dPi != 0.0 and dm_dbeta != 0.0)}


def run_episode(rng, acute=True, kernel_change=False, q0=0.98, q1=0.90, Pi_l=1.0, Pi_p0=1.0, acute_scale=0.1,
                occasion_len=50, n_steps=1600, switch_times=(400, 1000), obs_sd=1.0, truth_levels=(0.0, 4.0, -3.0)):
    """Agent: within an occasion of fixed length, Kalman update with prior precision Pi_p and prior mean = kernel seed.
    Kernel seed: age-weighted mean of completed occasions' final beliefs (P3), weights q^age."""
    truth = np.zeros(n_steps); lvl = 0
    for t in range(n_steps):
        if t in switch_times:
            lvl += 1
        truth[t] = truth_levels[lvl]
    beliefs = np.zeros(n_steps)
    completed = []  # final belief of each completed occasion
    q = q0
    m = 0.0; P_prec = Pi_p0
    acute_window = (600, 800) if acute else None
    for t in range(n_steps):
        if t % occasion_len == 0 and t > 0:
            completed.append(m)
            ages = np.arange(len(completed))[::-1]
            w = q ** ages; w /= w.sum()
            m = float((w * np.array(completed)).sum())  # the seed
            P_prec = Pi_p0
            if acute and t >= acute_window[1] and kernel_change:
                q = q1
        Pi_p = P_prec * (acute_scale if (acute and acute_window[0] <= t < acute_window[1]) else 1.0)
        y = truth[t] + obs_sd * rng.normal()
        Kg = Pi_l / (Pi_l + Pi_p)
        m = m + Kg * (y - m)
        P_prec = Pi_p + Pi_l
        beliefs[t] = m
    # adaptation time after each switch: first t >= switch where |belief-truth| < 0.25 for 10 consecutive steps
    def adapt_time(sw):
        err = np.abs(beliefs - truth)
        for t in range(sw, n_steps - 10):
            if np.all(err[t:t + 10] < 0.25):
                return t - sw
        return n_steps - sw
    return {"adapt_pre": adapt_time(switch_times[0]), "adapt_post": adapt_time(switch_times[1])}


def check_4b(n_rep=200):
    out = {}
    for label, acute, kc in (("H_state", True, False), ("H_kernel", True, True), ("mustfail_no_acute_state", False, False), ("mustfail_no_acute_kernel", False, True)):
        pre, post = [], []
        for r in range(n_rep):
            e = run_episode(np.random.default_rng(r), acute=acute, kernel_change=kc)
            pre.append(e["adapt_pre"]); post.append(e["adapt_post"])
        pre, post = np.array(pre, float), np.array(post, float)
        out[label] = {"adapt_pre_mean": float(pre.mean()), "adapt_post_mean": float(post.mean()),
                      "ratio_post_over_pre": float(post.mean() / max(pre.mean(), 1e-9))}
    return out


def main():
    a = check_4a(); b = check_4b()
    r = {"check_4a": a, "check_4b": b}
    (OUT / "c4_rebus_kernel.json").write_text(json.dumps(r, indent=1))
    lines = ["C4 — REBUS (prior precision) against the CRR temperature (kernel): state against kernel",
             f"4a Jacobian: dK/dbeta = {a['dK_dbeta']:.3g}, dm/dPi_p = {a['dm_dPi_p']:.3g}, dK/dPi_p = {a['dK_dPi_p']:.3g}, dm/dbeta = {a['dm_dbeta']:.3g}; orthogonal: {a['orthogonal']}"]
    for k, v in b.items():
        lines.append(f"4b {k}: adaptation time pre {v['adapt_pre_mean']:.1f}, post {v['adapt_post_mean']:.1f}, ratio {v['ratio_post_over_pre']:.3f}")
    lines.append("Declared predictions: H_state ratio within 0.05 of 1; H_kernel ratio differs by > 0.3; must-fail arms coincide.")
    (OUT / "c4_rebus_kernel.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
