#!/usr/bin/env python3
"""C1: the clock of becoming C against Kim's information length and the minimal-physicalism cycle count.

1a: for a Gaussian family p(x | mu(t), s^2) with mu(t) = sin t, compare Kim's information rate
    1/tau^2 = int dx (1/p) (d_t p)^2   (numerical differentiation + quadrature)
with the Fisher form   thetadot^T g thetadot = mudot^2 / s^2.
Must-fail arm: the Euclidean metric (mudot^2) must not agree when s != 1.
1b: 200 writes, the first 100 identical; the MP cycle count rises linearly, C stays 0 for 100 cycles.
numpy only; deterministic.
"""
import json, math, pathlib
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)


def gauss(x, mu, s):
    return np.exp(-0.5 * ((x - mu) / s) ** 2) / (s * math.sqrt(2 * math.pi))


def check_1a(s=0.7, n_t=400, dt_fd=1e-4):
    x = np.linspace(-8, 8, 20001)
    dx = x[1] - x[0]
    ts = np.linspace(0, 2 * math.pi, n_t)
    rel_err_fisher, rel_err_euclid = [], []
    L_kim, C_crr = 0.0, 0.0
    for i, t in enumerate(ts):
        mu, mu_dot = math.sin(t), math.cos(t)
        p0 = gauss(x, math.sin(t - dt_fd), s)
        p1 = gauss(x, math.sin(t + dt_fd), s)
        p = gauss(x, mu, s)
        dp = (p1 - p0) / (2 * dt_fd)
        kim_rate2 = np.sum(dp * dp / np.maximum(p, 1e-300)) * dx      # 1/tau^2
        fisher = mu_dot ** 2 / s ** 2                                  # thetadot^T g thetadot
        euclid = mu_dot ** 2
        if fisher > 1e-6:
            rel_err_fisher.append(abs(kim_rate2 - fisher) / fisher)
            rel_err_euclid.append(abs(kim_rate2 - euclid) / fisher)
        if i > 0:
            h = ts[i] - ts[i - 1]
            L_kim += math.sqrt(max(kim_rate2, 0.0)) * h
            C_crr += math.sqrt(fisher) * h
    return {
        "s": s,
        "max_rel_err_fisher": float(max(rel_err_fisher)),
        "max_rel_err_euclid_mustfail": float(max(rel_err_euclid)),
        "L_kim": L_kim, "C_crr_sigma1": C_crr,
        "L_over_C": L_kim / C_crr,
        "identity_holds": bool(max(rel_err_fisher) < 1e-3),
        "mustfail_euclid_disagrees": bool(max(rel_err_euclid) > 0.1),
    }


def check_1b(s=1.0):
    # writes: 100 identical values, then 100 values moving by 0.05 each
    writes = [0.0] * 100 + [0.05 * k for k in range(1, 101)]
    count, C = [], []
    c = 0.0
    for k in range(1, len(writes)):
        # Fisher-Rao distance between N(w_{k-1}, s^2) and N(w_k, s^2) with fixed s is |dw|/s
        c += abs(writes[k] - writes[k - 1]) / s
        count.append(k)
        C.append(c)
    return {
        "count_after_100_cycles": count[99], "C_after_100_cycles": C[99],
        "count_after_200_cycles": count[-1], "C_after_200_cycles": C[-1],
        "C_zero_while_count_rises": bool(C[99] == 0.0 and count[99] == 100),
    }


def main():
    r = {"check_1a": check_1a(), "check_1b": check_1b()}
    (OUT / "c1_information_length.json").write_text(json.dumps(r, indent=1))
    lines = [
        "C1 — C against Kim's information length and the MP cycle count",
        f"1a identity (Gaussian family, s={r['check_1a']['s']}): max relative error Fisher vs Kim = {r['check_1a']['max_rel_err_fisher']:.2e}; "
        f"L_kim/C = {r['check_1a']['L_over_C']:.6f}; holds: {r['check_1a']['identity_holds']}",
        f"1a must-fail (Euclidean metric): max relative error = {r['check_1a']['max_rel_err_euclid_mustfail']:.3f}; disagrees: {r['check_1a']['mustfail_euclid_disagrees']}",
        f"1b two clocks: after 100 identical writes count = {r['check_1b']['count_after_100_cycles']}, C = {r['check_1b']['C_after_100_cycles']:.3f}; "
        f"after 200 writes count = {r['check_1b']['count_after_200_cycles']}, C = {r['check_1b']['C_after_200_cycles']:.3f}; "
        f"C zero while count rises: {r['check_1b']['C_zero_while_count_rises']}",
        "Grade (declared rule): 1a holds -> C is REDUNDANT-IG (Kim's information length); 1b holds -> DISTINCTION (operation count vs distinguishable change).",
    ]
    (OUT / "c1_information_length.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
