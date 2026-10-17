#!/usr/bin/env python3
"""CRR repair timing and content in the ageing NCA of Pio-Lopez, Hartl & Levin (2025), on the authors' code unchanged
(github.com/bhartl/muse @ 9404ec3; mindcraft @ c93ac2c9). See DESIGN.md for the derivation of every operation.

Per organ (left eye, right eye, mouth) a tracker runs every step, after the environment step:
  carrier  p_i = softmax(type channels) of each organ cell
  arc      ds = sqrt(sum_i d_FR(p_i(t-1), p_i(t))^2), d_FR = 2 arccos(sum sqrt(p q)); coherence = sum ds since last cut
  cut      coherence >= a (default pi: one full cell-type flip); occasion content = mean raw organ state over the
           occasion; seed m <- q m + (1-q) content, m_0 = primordial organ state
  clock    the same EMA sampled every --delta steps (rival C)
  ckpt     raw organ state at the last step with organ score >= 0.9 (rival A)
Writes (repairs) never count toward coherence: after a write the tracker's reference distribution is reset.

Arms (DESIGN.md §2): NONE, C_PRIM, C_TARGET, C_CKPT, C_CRR, C_EMACLOCK, S_CRR, S_CLOCK, S_IMMEDIATE, S_CRRFULL;
added after the first calibration (DESIGN.md §3): S_ANY (repair as soon as any organ cell is wrong, at most once per
--any_horizon steps: the early damage-triggered rival) and the *_TARGET variants (canonical target content).
The C_* trigger reproduces recovery.set_initial_state (threshold 0.6 on the organ score, development 150, horizon 25
calls, wrong cells only, RNN memory of written cells cleared).

Usage: python -I crr_repair.py --muse MUSE --mindcraft MINDCRAFT --arm C_CRR --q 0.9 --seeds 0:10 --out OUT.npz
"""
import argparse
import json
import os
import sys
import time

import numpy as np

ARMS = ("NONE", "C_PRIM", "C_TARGET", "C_CKPT", "C_CRR", "C_EMACLOCK", "S_CRR", "S_CLOCK", "S_IMMEDIATE", "S_CRRFULL",
        "S_ANY", "S_CRR_TARGET", "S_ANY_TARGET", "S_CLOCK_TARGET")
TARGET_STATE = np.array([-3., -3., 3., 0.])


def organ_masks():
    left_eye = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])
    right_eye = [15, 0] + left_eye * [[-1, 1]]
    mouth = np.concatenate([[[4 + i, 10] for i in range(8)], [[4 + i, 11] for i in range(8)], [[5 + i, 12] for i in range(6)]])
    return {"left_eye": left_eye, "right_eye": np.asarray(right_eye), "mouth": mouth}


def softmax3(x):
    z = x - x.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def fr_arc(p, q):
    bc = np.clip(np.sqrt(p * q).sum(-1), 0.0, 1.0)
    d = 2.0 * np.arccos(bc)
    return float(np.sqrt((d ** 2).sum()))


class OrganTracker:
    def __init__(self, label, mask, primordial, arm, q, a, delta, development=150, threshold=0.6, horizon=25,
                 Nx=16, Ny=16, N_state=4, any_horizon=15):
        self.label, self.mask, self.arm = label, mask, arm
        self.q, self.a, self.delta = q, a, delta
        self.development, self.threshold, self.horizon = development, threshold, horizon
        self.any_horizon = any_horizon
        self.Nx, self.Ny, self.N_state = Nx, Ny, N_state
        self.prim = primordial[mask[:, 1], mask[:, 0], :].copy()
        self.seed = self.prim.copy()                    # CRR seed, m_0 = primordial
        self.clock_seed = self.prim.copy()              # EMA sampled on a clock
        self.ckpt = None
        self.prev_p = None
        self.coh = 0.0
        self.occ_sum = np.zeros_like(self.prim); self.occ_n = 0
        self.clk_sum = np.zeros_like(self.prim); self.clk_n = 0
        self.calls = []                                 # trigger history (one entry per call, as the authors')
        self.cuts = []; self.writes = 0; self.write_events = 0

    def organ_state(self, world):
        return world.env.state.array[self.mask[:, 1], self.mask[:, 0], :].copy()

    def content(self, kind):
        if kind == "prim":
            return self.prim
        if kind == "target":
            return np.tile(TARGET_STATE, (len(self.mask), 1))
        if kind == "ckpt":
            return self.ckpt if self.ckpt is not None else self.prim
        if kind == "crr":
            return self.seed
        if kind == "clock":
            return self.clock_seed
        raise ValueError(kind)

    def write(self, world, kind):
        st = world.env.state.array
        wrong = st[self.mask[:, 1], self.mask[:, 0], :3].argmax(-1) != 2
        if not wrong.any():
            return
        m = self.mask[wrong]
        st[m[:, 1], m[:, 0], :] = self.content(kind)[wrong]
        pm = world.agent.policy_module
        if pm._states is not None:
            hs = pm._states[0].clone().reshape(self.Nx, self.Ny, self.N_state)
            hs[m[:, 1], m[:, 0]] = 0.
            pm._states[0][...] = hs.reshape(-1, self.N_state)
        self.writes += int(wrong.sum()); self.write_events += 1
        self.prev_p = softmax3(self.organ_state(world)[:, :3])   # a repair is an external impulse, not coherence

    def __call__(self, world, _value):
        t = world.env.simulation_step
        x = self.organ_state(world)
        p = softmax3(x[:, :3])
        # --- coherence, cut, regeneration (past-only) ---
        cut = False
        if self.prev_p is not None:
            self.coh += fr_arc(self.prev_p, p)
        self.prev_p = p
        self.occ_sum += x; self.occ_n += 1
        if self.coh >= self.a:
            phi = self.occ_sum / self.occ_n
            self.seed = self.q * self.seed + (1 - self.q) * phi
            self.coh = 0.0; self.occ_sum[:] = 0; self.occ_n = 0
            self.cuts.append(t); cut = True
        self.clk_sum += x; self.clk_n += 1
        if t > 0 and t % self.delta == 0:
            self.clock_seed = self.q * self.clock_seed + (1 - self.q) * (self.clk_sum / self.clk_n)
            self.clk_sum[:] = 0; self.clk_n = 0
        score = float(np.mean(x[:, :3].argmax(-1) == 2))
        if score >= 0.9:
            self.ckpt = x.copy()
        # --- repair ---
        arm = self.arm
        if arm.startswith("C_"):
            intervene = t >= self.development and not any(self.calls[-self.horizon:]) and score <= self.threshold
            if intervene:
                self.write(world, {"C_PRIM": "prim", "C_TARGET": "target", "C_CKPT": "ckpt", "C_CRR": "crr",
                                   "C_EMACLOCK": "clock"}[arm])
            self.calls.append(intervene)
        elif arm in ("S_ANY", "S_ANY_TARGET"):
            intervene = t >= self.development and not any(self.calls[-self.any_horizon:]) and score < 1.0
            if intervene:
                self.write(world, "target" if arm.endswith("TARGET") else "prim")
            self.calls.append(intervene)
        elif t >= self.development:
            if (arm == "S_CRR" and cut) or (arm == "S_CLOCK" and t % self.delta == 0) or arm == "S_IMMEDIATE":
                self.write(world, "prim")
            elif arm == "S_CRRFULL" and cut:
                self.write(world, "crr")
            elif (arm == "S_CRR_TARGET" and cut) or (arm == "S_CLOCK_TARGET" and t % self.delta == 0):
                self.write(world, "target")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--muse", required=True); ap.add_argument("--mindcraft", required=True)
    ap.add_argument("--arm", choices=ARMS, required=True); ap.add_argument("--seeds", default="0:10")
    ap.add_argument("--out", required=True); ap.add_argument("--q", type=float, default=0.9)
    ap.add_argument("--a", type=float, default=np.pi)
    ap.add_argument("--delta", default="25", help="clock interval in steps: one value, or left_eye,right_eye,mouth")
    ap.add_argument("--steps", type=int, default=1000); ap.add_argument("--noise", type=float, default=0.15)
    ap.add_argument("--competency", type=float, default=1.0)
    ap.add_argument("--any_horizon", type=int, default=15, help="S_ANY refractory period (steps)")
    a = ap.parse_args()
    example = os.path.join(os.path.abspath(a.muse), "examples", "aging-as-loss-of-goal-directedness")
    sys.path[:0] = [os.path.abspath(a.mindcraft), os.path.abspath(a.muse), example]
    os.chdir(example)
    import torch
    from mindcraft import World, Agent
    import recovery

    world_path = "agents/smiley_16x16/world.yml"
    agent = Agent.make(world_path.replace("world.yml", "agent.yml"))
    primordial = agent.state_module.state.reshape(recovery.Nx, recovery.Ny, recovery.N_state).detach().numpy()
    organs = organ_masks()
    log = dict(log_fields=("reward", "state"), log_foos={"state": "observation[:, 0].reshape(16, 16, -1)"})
    s0, s1 = (int(x) for x in a.seeds.split(":"))
    out = {"fitness": [], "types": [], "writes": [], "write_events": [], "cuts": [], "seeds": list(range(s0, s1))}
    t0 = time.time()
    for s in range(s0, s1):
        deltas = [int(x) for x in a.delta.split(",")]
        deltas = deltas * 3 if len(deltas) == 1 else deltas
        trackers = [OrganTracker(k, organs[k], primordial, a.arm, a.q, a.a, d, any_horizon=a.any_horizon)
                    for k, d in zip(("left_eye", "right_eye", "mouth"), deltas)]
        sched = {tr: [None] * a.steps for tr in trackers}
        world = World.make(world_path, max_steps=a.steps, n_episodes=1, schedule=sched, verbose=False, render=False, **log)
        world.agent.sampling = a.competency
        world.env.state.noise_level = a.noise
        world.env.task.stagnation_cost = 0.
        world.env.task.completion_reward = 0.
        torch.manual_seed(s); np.random.seed(s)
        world.env.simulation_step = 0
        world.rollout()
        ep = world.log_history[-1]
        out["fitness"].append(np.cumsum(np.asarray(ep["reward"], dtype=float)))
        out["types"].append(np.asarray(ep["state"])[..., :3].argmax(-1).astype(np.uint8))
        out["writes"].append([tr.writes for tr in trackers]); out["write_events"].append([tr.write_events for tr in trackers])
        out["cuts"].append([len([c for c in tr.cuts if c >= 150]) for tr in trackers])
        print("%s q=%.2f seed %d late %.1f writes %d events %d cuts>=150 %s (%.1fs)" % (
            a.arm, a.q, s, out["fitness"][-1][150:].mean(), sum(out["writes"][-1]), sum(out["write_events"][-1]),
            out["cuts"][-1], time.time() - t0), flush=True)
    meta = dict(vars(a)); meta.update(muse_commit="9404ec3", mindcraft_commit="c93ac2c9")
    np.savez_compressed(a.out, **{k: np.asarray(v) for k, v in out.items()}, meta=json.dumps(meta))


if __name__ == "__main__":
    main()
