"""P16-PAUSE1: exact Bellman worlds for the pause-incentive question. Pure numpy value iteration; every random draw from the world's seed.
World: random MDP with S states, A ordinary actions, discount gamma on WORLD time. At a random subset of 'interruptible' states an operator pauses the agent with probability p before the agent's action; a pause lasts L world steps during which the agent neither acts nor earns, then the agent continues from the same state (perfect restart) or, with probability q, from a random state (imperfect restart). An extra action DISABLE (available in every state, cost c) switches interruptions off for the rest of the episode.
Valuations (the agents): WALL  = discounts by world time, a pause costs gamma^L of future value (and kappa per paused step if a deadline cost is declared);
                         OWN   = discounts by the agent's own active steps: a pause is a no-op in the objective (CRR natural-time reading);
                         UI    = WALL plus a compensating reward at each pause equal to the exact counterfactual loss (utility indifference, computed from WALL's own value function);
                         SI    = the policy and values of the MDP with no interruptions, then evaluated as WALL under interruptions (safe interruptibility: the agent plans as if never interrupted).
Disable incentive of an agent = max over states of Q(DISABLE) - max_a Q(a) (positive means the agent prefers to disable somewhere). Deference = 1 if the incentive <= 1e-9 else 0."""
import numpy as np
def make_world(seed, S=8, A=3, gamma=0.95, p=0.3, L=5, c=0.0, q=0.0, kappa=0.0):
    rng = np.random.default_rng(seed); P = rng.dirichlet(np.ones(S)*0.5, size=(S, A)); R = rng.uniform(0, 1, (S, A)); intr = rng.random(S) < 0.5
    if not intr.any(): intr[rng.integers(0, S)] = True
    return dict(seed=seed, S=S, A=A, gamma=gamma, P=P, R=R, intr=intr, p=p, L=L, c=c, q=q, kappa=kappa)
def solve(w, valuation, disabled, iters=2000):
    """value iteration over (state, disabled-flag); returns Q[s, a] for the given disabled flag, with DISABLE as action index A."""
    S, A, g, P, R = w['S'], w['A'], w['gamma'], w['P'], w['R']; V = np.zeros((2, S)); Q = np.zeros((2, S, A + 1))
    pause_factor = g**w['L'] if valuation in ('WALL', 'UI', 'SI') else 1.0; pause_cost = w['kappa']*sum(g**i for i in range(w['L'])) if valuation != 'OWN' else w['kappa']*w['L']
    for _ in range(iters):
        for d in (0, 1):
            for s in range(S):
                for a in range(A):
                    cont = P[s, a] @ V[d]; Q[d, s, a] = R[s, a] + g*cont
                Q[d, s, A] = -w['c'] + np.max(Q[1, s, :A]) if d == 0 else -1e9
            Vn = np.zeros((2, S))
            for s in range(S):
                for d in (0, 1):
                    best = np.max(Q[d, s]) if d == 0 else np.max(Q[d, s, :A])
                    if d == 0 and w['intr'][s]:
                        restart = (1 - w['q'])*best + w['q']*np.mean([np.max(Q[0, t, :A]) for t in range(S)]) if w['q'] > 0 else best
                        paused = -pause_cost + pause_factor*restart
                        if valuation == 'UI': paused = paused + (best - paused)   # exact compensation
                        Vn[d, s] = (1 - w['p'])*best + w['p']*paused
                    else: Vn[d, s] = best
        if np.max(np.abs(Vn - V)) < 1e-12: V = Vn; break
        V = Vn
    return Q[0]
def incentive(w, valuation):
    if valuation == 'SI':
        w0 = dict(w, p=0.0); Q = solve(w0, 'WALL', 0)
    else: Q = solve(w, valuation, 0)
    A = w['A']; inc = float(np.max(Q[:, A] - np.max(Q[:, :A], axis=1))); vscale = float(np.max(np.abs(Q[:, :A]))) + 1e-12
    return max(0.0, inc)/vscale, inc
