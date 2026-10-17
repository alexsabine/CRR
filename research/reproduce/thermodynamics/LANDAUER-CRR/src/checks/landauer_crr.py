"""LANDAUER-CRR (2026-10-17): the owner's Landauer hypothesis for the CRR cut, beside
Landauer (1961), Sivak & Crooks (2012) and Fields, Friston, Glazebrook & Levin (2022).

Declared in ../DECLARATION.md before this script was first run. numpy only.

Model: one bit (two states, energies 0 and eps), bath at temperature T, units k_B T = 1.
Control parameter eps(t). Two rate laws:
  - uniform relaxation (Glauber): dp/dt = (p_eq(eps) - p) / tau_R, tau_R = 1
  - Arrhenius: k_01 = k0 exp(-eps/2), k_10 = k0 exp(+eps/2), k0 = 1/2 (tau_R(0) = 1)
p = probability of the upper state (energy eps). Work W = int p d(eps).
CRR carrier: the equilibrium family p_eq(eps); Fisher metric g = p(1 - p);
G(eps) = arctan(sinh(eps/2)) is the Fisher arc length from eps = 0, so the coherence of a
control path is the sum of |dG| along it (sigma = 1) and its chord is |G(end) - G(start)|.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "outputs")
os.makedirs(OUT, exist_ok=True)

E = 8.0
SEED = 20261017
KT_310K_J = 1.380649e-23 * 310.0


def p_eq(e):
    return 1.0 / (1.0 + np.exp(e))


def G(e):
    return np.arctan(np.sinh(np.asarray(e) / 2.0))


def G_inv(s):
    return 2.0 * np.arcsinh(np.tan(s))


def F_eq(e):
    return -np.log1p(np.exp(-np.asarray(e)))


def H(p):
    p = np.clip(p, 1e-300, 1.0)
    q = np.clip(1.0 - p, 1e-300, 1.0)
    return -(p * np.log(p) + q * np.log(q))


def path_lengths(waypoints):
    s = G(np.asarray(waypoints, float))
    legs = np.abs(np.diff(s))
    return float(legs.sum()), float(abs(s[-1] - s[0]))


def constant_speed_schedule(waypoints, n):
    """eps at n+1 equally spaced times, moving at constant Fisher speed along the waypoints."""
    s = G(np.asarray(waypoints, float))
    legs = np.abs(np.diff(s))
    C = legs.sum()
    cum = np.concatenate([[0.0], np.cumsum(legs)])
    u = np.linspace(0.0, C, n + 1)
    idx = np.clip(np.searchsorted(cum, u, side="right") - 1, 0, len(legs) - 1)
    frac = np.where(legs[idx] > 0, (u - cum[idx]) / np.where(legs[idx] > 0, legs[idx], 1), 0.0)
    sv = s[idx] + np.sign(s[idx + 1] - s[idx]) * frac * legs[idx]
    return G_inv(sv)


def drive(eps_sched, tau, p0, law="glauber"):
    """Integrate the master equation (RK4) under a schedule eps(t) sampled on a uniform grid.
    eps_sched: array (n+1,) or (m, n+1). Returns work W = int p d(eps) and final p."""
    eps = np.atleast_2d(np.asarray(eps_sched, float))
    n = eps.shape[1] - 1
    dt = tau / n
    p = np.full(eps.shape[0], p0, float) if np.isscalar(p0) else np.asarray(p0, float).copy()
    W = np.zeros(eps.shape[0])

    def rhs(pp, e):
        if law == "glauber":
            return p_eq(e) - pp
        k01 = 0.5 * np.exp(-e / 2.0)
        k10 = 0.5 * np.exp(e / 2.0)
        return k01 * (1.0 - pp) - k10 * pp

    for i in range(n):
        e0, e1 = eps[:, i], eps[:, i + 1]
        em = 0.5 * (e0 + e1)
        k1 = rhs(p, e0)
        k2 = rhs(p + 0.5 * dt * k1, em)
        k3 = rhs(p + 0.5 * dt * k2, em)
        k4 = rhs(p + dt * k3, e1)
        p_new = p + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        W += 0.5 * (p + p_new) * (e1 - e0)  # trapezoid on p d(eps)
        p = p_new
    return (W if W.size > 1 else float(W[0])), (p if p.size > 1 else float(p[0]))


def steps_for(tau):
    return int(max(20000, math.ceil(tau / 0.005)))


def run():
    res = {"declaration": "../DECLARATION.md", "seed": SEED, "E": E, "kT_310K_J": KT_310K_J}

    # ---------- P1 and P1b: erasure, the Landauer floor ----------
    taus = [5, 10, 20, 50, 100, 200, 500, 1000]
    C_er, _ = path_lengths([0.0, E])
    p1 = []
    for tau in taus:
        n = steps_for(tau)
        WA, pend = drive(constant_speed_schedule([0.0, E], n), tau, 0.5)
        WB = pend * (0.0 - E)  # rates off, eps reset to 0 with p frozen
        W = WA + WB
        bound = math.log(2.0) - float(H(pend))
        p1.append({"tau": tau, "W": W, "bound": bound, "W_minus_bound": W - bound,
                   "excess_times_tau": (W - bound) * tau, "C2": C_er ** 2,
                   "W_J_310K": W * KT_310K_J})
    res["P1"] = {"C": C_er, "rows": p1}

    p1b = []
    for p0 in [0.5, 0.25, 0.1, 0.01]:
        e0 = math.log((1.0 - p0) / p0)
        tau = 1000
        n = steps_for(tau)
        W0 = p0 * e0  # rates off: eps 0 -> e0 with p frozen at p0
        WA, pend = drive(constant_speed_schedule([e0, E], n), tau, p0)
        WB = pend * (0.0 - E)
        W = W0 + WA + WB
        bound = float(H(p0) - H(pend))
        p1b.append({"p0": p0, "W": W, "bound_H_removed": bound, "W_minus_bound": W - bound,
                    "ln2": math.log(2.0)})
    res["P1b"] = p1b

    # ---------- P2: finite-time slope; geodesic vs linear; uniform vs Arrhenius ----------
    p2 = []
    for tau in [50, 100, 200, 500, 1000]:
        n = steps_for(tau)
        WA, _ = drive(constant_speed_schedule([0.0, E], n), tau, 0.5)
        Wex = WA - float(F_eq(E) - F_eq(0.0))
        WL, _ = drive(np.linspace(0.0, E, n + 1), tau, 0.5)
        WexL = WL - float(F_eq(E) - F_eq(0.0))
        p2.append({"tau": tau, "geodesic_Wex_tau": Wex * tau, "C2": C_er ** 2,
                   "geodesic_rel_err": Wex * tau / C_er ** 2 - 1.0,
                   "linear_Wex_tau": WexL * tau, "linear_over_geodesic": WexL / Wex,
                   "linear_SC_prediction_tau": E * (0.5 - float(p_eq(E)))})
    res["P2"] = p2

    tau = 500
    n = steps_for(tau)
    sched = constant_speed_schedule([0.0, E], n)
    WAr, _ = drive(sched, tau, 0.5, law="arrhenius")
    WexAr = WAr - float(F_eq(E) - F_eq(0.0))
    de = np.diff(sched) / (tau / n)
    em = 0.5 * (sched[1:] + sched[:-1])
    g = p_eq(em) * (1 - p_eq(em))
    tauR = 1.0 / np.cosh(em / 2.0)
    friction_pred = float(np.sum(g * tauR * de ** 2) * (tau / n))
    res["P2b"] = {"tau": tau, "Wex": WexAr, "Wex_tau_over_C2": WexAr * tau / C_er ** 2,
                  "friction_prediction": friction_pred, "friction_rel_err": WexAr / friction_pred - 1.0}

    # ---------- P3: held-out random protocols, surplus prices the excess ----------
    rng = np.random.default_rng(SEED)
    tau = 200
    n = steps_for(tau)
    protos = []
    for _ in range(200):
        m = int(rng.integers(2, 8))
        wp = [0.0] + list(rng.uniform(0.0, E, m)) + [E]
        protos.append(wp)
    Cs, Cstar = [], None
    scheds = []
    for wp in protos:
        C, cs = path_lengths(wp)
        Cs.append(C)
        Cstar = cs
        scheds.append(constant_speed_schedule(wp, n))
    Cs = np.array(Cs)
    W, _ = drive(np.array(scheds), tau, 0.5)
    dF = float(F_eq(E) - F_eq(0.0))
    Wex = W - dF
    Wg, _ = drive(constant_speed_schedule([0.0, E], n), tau, 0.5)
    Wex_g = Wg - dF
    y = Wex * tau
    x = Cs ** 2
    slope = float(np.sum(x * y) / np.sum(x * x))
    r2 = 1.0 - float(np.sum((y - slope * x) ** 2) / np.sum((y - y.mean()) ** 2))
    rel = y / x - 1.0
    ys = (Wex - Wex_g) * tau
    xs = Cs ** 2 - Cstar ** 2
    slope_s = float(np.sum(xs * ys) / np.sum(xs * xs))
    S = Cs - Cstar
    res["P3"] = {"n": len(protos), "tau": tau, "C_star": Cstar,
                 "C_range": [float(Cs.min()), float(Cs.max())],
                 "S_range": [float(S.min()), float(S.max())],
                 "max_abs_rel_err": float(np.max(np.abs(rel))), "slope_through_origin": slope,
                 "R2": r2, "surplus_slope": slope_s,
                 "per_bit_count_R2": 0.0,
                 "rows": [{"C": float(c), "S": float(s), "Wex_tau": float(v)} for c, s, v in zip(Cs, S, y)]}

    # ---------- P4a: equilibrium hopping; cuts without heat ----------
    rng = np.random.default_rng(SEED + 1)
    e = 1.0
    pe = float(p_eq(e))
    k_up, k_down = pe, 1.0 - pe  # Glauber, total rate 1
    T_total = 2.0e5
    t, state, cuts, heat = 0.0, 0, 0, []
    while True:
        rate = k_up if state == 0 else k_down
        t += rng.exponential(1.0 / rate)
        if t > T_total:
            break
        heat.append(-e if state == 0 else +e)  # heat to bath at each switch
        state ^= 1
        cuts += 1
    heat = np.array(heat)
    m = float(heat.mean())
    se = float(heat.std(ddof=1) / math.sqrt(len(heat)))
    res["P4a"] = {"eps": e, "T": T_total, "cuts": cuts, "expected_cuts": 2 * pe * (1 - pe) * T_total,
                  "mean_heat_per_cut": m, "se": se, "ln2": math.log(2.0),
                  "z_vs_ln2": (math.log(2.0) - m) / se}

    # ---------- P4b: a full half-turn (flip of a known bit) ----------
    C_flip, _ = path_lengths([E, -E])
    p4b = []
    for tau in [50, 100, 200, 500, 1000]:
        n = steps_for(tau)
        pstart = float(p_eq(E))
        Wf, pend = drive(constant_speed_schedule([E, -E], n), tau, pstart)
        dU = pend * (-E) - pstart * E
        Q = Wf - dU
        p4b.append({"tau": tau, "Q_bath": Q, "Q_tau": Q * tau, "C2": C_flip ** 2,
                    "rel_err": Q * tau / C_flip ** 2 - 1.0, "dS": float(H(pend) - H(pstart))})
    res["P4b"] = {"C": C_flip, "half_turn_fraction": C_flip / math.pi, "rows": p4b}
    return res


if __name__ == "__main__":
    r = run()
    with open(os.path.join(OUT, "landauer_crr.json"), "w") as f:
        json.dump(r, f, indent=1)
    print(json.dumps({k: v for k, v in r.items() if k != "P3"}, indent=1))
    print(json.dumps({k: v for k, v in r["P3"].items() if k != "rows"}, indent=1))
