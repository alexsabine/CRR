#!/usr/bin/env python3
"""C3: the precedence signature and the only interventions that decide a Platonic library against history.

Worlds (K form types, N instances, T draws per instance, seed 0):
  A  fixed heterogeneous library (Zipf), no update
  C  local Polya urn per instance (weights += 1 per realised form)
  P  CRR production: next form from the settled block under age weights q plus a novelty floor eps (a fading Polya)
  S  one Polya urn shared by all instances (ingression from a common learning space)
Statistics:
  T1 precedence: entropy of the realised form by precedent-count bin (falls in C, P, S; flat in A)
  T2 cross-instance transfer: JSD between a naive instance's first draws and (i) the base prior, (ii) the others' realised distribution
  T3 reset: erase instance 1's physical record at draw T/2; JSD of its next 200 draws from its pre-reset distribution
  T4 recency (C vs P): order gain of a fitted fading kernel over a non-fading urn, original vs shuffled order, at T and at 300 draws
numpy only.
"""
import json, math, pathlib
import numpy as np

OUT = pathlib.Path(__file__).resolve().parents[1] / "outputs"
OUT.mkdir(exist_ok=True)
K, N, T = 8, 24, 2000
Q_PROD, EPS = 0.98, 0.02


def zipf(K):
    w = 1.0 / np.arange(1, K + 1)
    return w / w.sum()


def entropy(p):
    p = p[p > 0]
    return float(-(p * np.log(p)).sum())


def jsd(p, q):
    p = np.asarray(p, float) + 1e-12; q = np.asarray(q, float) + 1e-12
    p /= p.sum(); q /= q.sum(); m = 0.5 * (p + q)
    kl = lambda a, b: float((a * np.log(a / b)).sum())
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def simulate(world, rng, reset_at=None, naive_last=False):
    """Returns draws [N, T] and per-step predictive distributions for T1."""
    base = zipf(K)
    draws = np.zeros((N, T), int)
    pred_entropy_by_bin = {}  # precedent count bin -> list of predictive entropies
    shared = np.ones(K) * 1.0 if world == "S" else None
    for i in range(N):
        local = np.ones(K) * 1.0
        block = []  # (age index, form) for production
        start = T // 2 if (naive_last and i == N - 1) else 0  # naive instance draws only from mid-run on (after others' histories exist)
        for t in range(T):
            if naive_last and i == N - 1 and t < start:
                draws[i, t] = -1
                continue
            if reset_at is not None and i == 0 and t == reset_at:
                local = np.ones(K) * 1.0; block = []
            if world == "A":
                p = base.copy()
            elif world == "C":
                p = (base + local - 1.0); p = p / p.sum()
            elif world == "S":
                p = (base + shared - 1.0); p = p / p.sum()
            elif world == "P":
                p = np.zeros(K)
                for age, f in enumerate(reversed(block)):
                    p[f] += Q_PROD ** age
                p = (1 - EPS) * (p / p.sum() if p.sum() > 0 else base) + EPS * base
            n_prec = len(block) if world == "P" else int(local.sum() - K) if world in ("C",) else int(shared.sum() - K) if world == "S" else t
            b = min(n_prec // 100, 19)
            pred_entropy_by_bin.setdefault(b, []).append(entropy(p))
            f = int(rng.choice(K, p=p))
            draws[i, t] = f
            local[f] += 1.0
            if shared is not None:
                shared[f] += 1.0
            block.append(f)
    return draws, {b: float(np.mean(v)) for b, v in sorted(pred_entropy_by_bin.items())}


def hist(x):
    x = x[x >= 0]
    h = np.bincount(x, minlength=K).astype(float)
    return h / max(h.sum(), 1)


def order_gain(seq, rng, q_fade=0.98, n_shuffle=20):
    """log-likelihood of a fading-urn predictor minus a non-fading urn predictor; original minus shuffled mean."""
    def ll(s, q):
        w = np.ones(K); tot = 0.0
        for f in s:
            p = w / w.sum(); tot += math.log(p[f])
            w = w * q + 1.0 * np.eye(K)[f] if q < 1 else w + np.eye(K)[f]
        return tot
    g_orig = ll(seq, q_fade) - ll(seq, 1.0)
    g_sh = []
    for _ in range(n_shuffle):
        s = seq.copy(); rng.shuffle(s)
        g_sh.append(ll(s, q_fade) - ll(s, 1.0))
    return float(g_orig - np.mean(g_sh)), float(np.std(g_sh))


def main():
    rng = np.random.default_rng(0)
    res = {}
    for world in ("A", "C", "P", "S"):
        d, ent = simulate(world, np.random.default_rng(0))
        # T1: entropy at low vs high precedent count
        bins = sorted(ent)
        t1 = {"entropy_low_bin": ent[bins[0]], "entropy_high_bin": ent[bins[-1]], "drop": ent[bins[0]] - ent[bins[-1]]}
        # T2: naive instance
        dn, _ = simulate(world, np.random.default_rng(1), naive_last=True)
        naive_first = dn[N - 1, T // 2: T // 2 + 100]
        others = dn[: N - 1].ravel()
        t2 = {"jsd_naive_vs_base": jsd(hist(naive_first), zipf(K)), "jsd_naive_vs_others": jsd(hist(naive_first), hist(others))}
        # T3: reset
        dr, _ = simulate(world, np.random.default_rng(2), reset_at=T // 2)
        pre = dr[0, T // 2 - 400: T // 2]; post = dr[0, T // 2: T // 2 + 200]
        t3 = {"jsd_post_vs_pre_reset": jsd(hist(post), hist(pre))}
        # T4: order gain on instance 2 at full and short length
        g_full, sd_full = order_gain(d[2].copy(), np.random.default_rng(3))
        g_short, sd_short = order_gain(d[2, :300].copy(), np.random.default_rng(4))
        t4 = {"order_gain_T2000": g_full, "shuffle_sd_T2000": sd_full, "z_T2000": g_full / max(sd_full, 1e-9),
              "order_gain_T300": g_short, "shuffle_sd_T300": sd_short, "z_T300": g_short / max(sd_short, 1e-9)}
        res[world] = {"T1_precedence": t1, "T2_transfer": t2, "T3_reset": t3, "T4_recency": t4}
    (OUT / "c3_precedence_library.json").write_text(json.dumps(res, indent=1))
    lines = ["C3 — precedence signature and the deciding interventions (K=8, N=24, T=2000, seed 0)",
             "world | T1 entropy drop (low->high precedent) | T2 JSD naive vs others (transfer) | T3 JSD post vs pre reset | T4 order-gain z at 2000 / 300"]
    for w, r in res.items():
        lines.append(f"{w} | {r['T1_precedence']['drop']:+.3f} | {r['T2_transfer']['jsd_naive_vs_others']:.3f} | {r['T3_reset']['jsd_post_vs_pre_reset']:.3f} | {r['T4_recency']['z_T2000']:+.1f} / {r['T4_recency']['z_T300']:+.1f}")
    lines.append("Declared predictions: T1 falls in C,P,S and is flat in A; T2 transfer only in S; T3 reset in C,P but not S; T4 separates P from C at 2000 draws, not reliably at 300.")
    (OUT / "c3_precedence_library.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
