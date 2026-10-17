#!/usr/bin/env python3
"""Lifecourse and competency runs of the ageing NCA of Pio-Lopez, Hartl & Levin (2025), authors' code unchanged
(github.com/bhartl/muse @ 9404ec3; mindcraft @ c93ac2c9). No repair is applied in either mode.

mode lifecourse  one long unrepaired lifetime per seed; saves fitness, the full type map and the raw states of the
                 organ cells (left eye, right eye, mouth: 42 cells x 4 channels, float16) at every step
mode competency  per seed, one uninjured baseline lifetime plus one lifetime per injury age t in --ages; the injury
                 overwrites the fixed --injury_cells of the left eye with a face-typed state and clears their RNN
                 memory at step t. Same seed = identical noise, so the injured run differs from the baseline only by
                 the injury (checked: identical before t). Saves the left-eye score trajectory of every run and the
                 step-wise share of grid cells whose type differs from the baseline.

Usage:
  python -I levin_checks.py --muse M --mindcraft N lifecourse --seeds 3000:3050 --steps 2000 --noise 0.125 --out LC.npz
  python -I levin_checks.py --muse M --mindcraft N competency --seeds 3000:3020 --ages 200,400,600 --out CP.npz
"""
import argparse
import json
import os
import sys
import time

import numpy as np

FACE_STATE = np.array([-3., 3., -3., 0.])
INJURY_STATES = {"face": FACE_STATE, "organ": np.array([-3., -3., 3., 0.]), "background": np.array([3., -3., -3., 0.])}
LEFT_EYE = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])
RIGHT_EYE = [15, 0] + LEFT_EYE * [[-1, 1]]
MOUTH = np.concatenate([[[4 + i, 10] for i in range(8)], [[4 + i, 11] for i in range(8)], [[5 + i, 12] for i in range(6)]])
ORGANS = np.concatenate([LEFT_EYE, RIGHT_EYE, MOUTH])          # 42 cells: 0-9 left eye, 10-19 right eye, 20-41 mouth


def setup(a):
    example = os.path.join(os.path.abspath(a.muse), "examples", "aging-as-loss-of-goal-directedness")
    sys.path[:0] = [os.path.abspath(a.mindcraft), os.path.abspath(a.muse), example]
    os.chdir(example)
    import torch
    from mindcraft import World
    return torch, World


def make_world(World, a, steps, schedule):
    log = dict(log_fields=("reward", "state"), log_foos={"state": "observation[:, 0].reshape(16, 16, -1)"})
    w = World.make("agents/smiley_16x16/world.yml", max_steps=steps, n_episodes=1, schedule=schedule,
                   verbose=False, render=False, **log)
    w.agent.sampling = a.competency
    w.env.state.noise_level = a.noise
    w.env.task.stagnation_cost = 0.
    w.env.task.completion_reward = 0.
    return w


def run(torch, World, a, seed, steps, schedule=None):
    w = make_world(World, a, steps, schedule or {})
    torch.manual_seed(seed); np.random.seed(seed)
    w.env.simulation_step = 0
    w.rollout()
    ep = w.log_history[-1]
    return np.cumsum(np.asarray(ep["reward"], dtype=float)), np.asarray(ep["state"])


def make_injury(t_inj, cells, value, Nx=16, Ny=16, N_state=4):
    def cb(world, _v):
        if world.env.simulation_step != t_inj:
            return
        world.env.state.array[cells[:, 1], cells[:, 0], :] = value
        pm = world.agent.policy_module
        if pm._states is not None:
            hs = pm._states[0].clone().reshape(Nx, Ny, N_state)
            hs[cells[:, 1], cells[:, 0]] = 0.
            pm._states[0][...] = hs.reshape(-1, N_state)
    return cb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--muse", required=True); ap.add_argument("--mindcraft", required=True)
    ap.add_argument("--noise", type=float, default=0.125); ap.add_argument("--competency", type=float, default=1.0)
    sub = ap.add_subparsers(dest="mode", required=True)
    lc = sub.add_parser("lifecourse"); lc.add_argument("--seeds", required=True); lc.add_argument("--steps", type=int, default=2000)
    lc.add_argument("--out", required=True)
    cp = sub.add_parser("competency"); cp.add_argument("--seeds", required=True); cp.add_argument("--ages", required=True)
    cp.add_argument("--injury_cells", default="4,4;5,5;6,6", help="x,y;x,y;... left-eye cells to injure")
    cp.add_argument("--injury_state", choices=sorted(INJURY_STATES), default="face",
                    help="state written into the injured cells (face-typed for eye cells, organ-typed for face cells)")
    cp.add_argument("--injury_k", type=int, default=0,
                    help="if > 0: injure k left-eye cells drawn at random per seed (random.Random(seed)); overrides --injury_cells")
    cp.add_argument("--follow", type=int, default=60); cp.add_argument("--out", required=True)
    kt = sub.add_parser("kthresh", help="repair an organ (write the canonical organ state into its wrong cells, clear "
                                        "their RNN memory) whenever it has >= k wrong cells, after step 150")
    kt.add_argument("--seeds", required=True); kt.add_argument("--k", type=int, required=True)
    kt.add_argument("--steps", type=int, default=1000); kt.add_argument("--out", required=True)
    a = ap.parse_args()
    torch, World = setup(a)
    s0, s1 = (int(x) for x in a.seeds.split(":"))
    t0 = time.time()
    if a.mode == "kthresh":
        TARGET = np.array([-3., -3., 3., 0.])
        organs = {"left_eye": LEFT_EYE, "right_eye": np.asarray(RIGHT_EYE), "mouth": MOUTH}

        class KRepair:
            def __init__(self):
                self.writes = 0; self.events = 0

            def __call__(self, world, _v):
                if world.env.simulation_step < 150:
                    return
                st = world.env.state.array
                for m in organs.values():
                    wrong = st[m[:, 1], m[:, 0], :3].argmax(-1) != 2
                    if wrong.sum() >= a.k:
                        mm = m[wrong]
                        st[mm[:, 1], mm[:, 0], :] = TARGET
                        pm = world.agent.policy_module
                        if pm._states is not None:
                            hs = pm._states[0].clone().reshape(16, 16, 4)
                            hs[mm[:, 1], mm[:, 0]] = 0.
                            pm._states[0][...] = hs.reshape(-1, 4)
                        self.writes += int(wrong.sum()); self.events += 1
        out = {"fitness": [], "types": [], "writes": [], "events": [], "seeds": list(range(s0, s1))}
        for s in range(s0, s1):
            kr = KRepair()
            fit, st = run(torch, World, a, s, a.steps, {kr: [None] * a.steps})
            out["fitness"].append(fit); out["types"].append(st[..., :3].argmax(-1).astype(np.uint8))
            out["writes"].append(kr.writes); out["events"].append(kr.events)
            print("kthresh k=%d seed %d late %.1f writes %d (%.0fs)" % (a.k, s, fit[150:].mean(), kr.writes, time.time() - t0), flush=True)
        meta = dict(mode="kthresh", k=a.k, steps=a.steps, noise=a.noise, competency=a.competency)
    elif a.mode == "lifecourse":
        out = {"fitness": [], "types": [], "organ_states": [], "seeds": list(range(s0, s1))}
        for s in range(s0, s1):
            fit, st = run(torch, World, a, s, a.steps)
            out["fitness"].append(fit); out["types"].append(st[..., :3].argmax(-1).astype(np.uint8))
            out["organ_states"].append(st[:, ORGANS[:, 1], ORGANS[:, 0], :].astype(np.float16))
            print("lifecourse seed %d fitness@%d %.0f (%.0fs)" % (s, a.steps, fit[-1], time.time() - t0), flush=True)
        meta = dict(mode="lifecourse", steps=a.steps, noise=a.noise, competency=a.competency)
    else:
        ages = [int(x) for x in a.ages.split(",")]
        fixed_cells = np.array([[int(v) for v in c.split(",")] for c in a.injury_cells.split(";")])
        steps = max(ages) + a.follow + 1
        le = lambda st: (st[..., LEFT_EYE[:, 1], LEFT_EYE[:, 0], :3].argmax(-1) == 2).mean(-1)
        out = {"seeds": list(range(s0, s1)), "ages": ages, "base_eye": [], "inj_eye": [], "type_diff": [], "pre_identical": [],
               "region_match": [], "base_region": []}
        for s in range(s0, s1):
            if a.injury_k > 0:
                import random
                cells = LEFT_EYE[sorted(random.Random(s).sample(range(len(LEFT_EYE)), a.injury_k))]
            else:
                cells = fixed_cells
            _, base = run(torch, World, a, s, steps)
            bt = base[..., :3].argmax(-1)
            out["base_eye"].append(le(base))
            ie, td, pre, rm = [], [], [], []
            out["base_region"].append([bt[t - 1, cells[:, 1], cells[:, 0]] for t in ages])   # baseline types of injured cells at t-1
            for t in ages:
                _, st = run(torch, World, a, s, steps, {make_injury(t, cells, INJURY_STATES[a.injury_state]): [None] * steps})
                tt = st[..., :3].argmax(-1)
                ie.append(le(st)[t - 1:t + a.follow + 1])
                td.append((tt[t - 1:t + a.follow + 1] != bt[t - 1:t + a.follow + 1]).mean((1, 2)))
                pre.append(bool(np.array_equal(st[:t], base[:t])))
                # share of the injured cells whose type equals the uninjured baseline's (1 = repaired back)
                rm.append((tt[t - 1:t + a.follow + 1, cells[:, 1], cells[:, 0]] == bt[t - 1:t + a.follow + 1, cells[:, 1], cells[:, 0]]).mean(-1))
            out["inj_eye"].append(ie); out["type_diff"].append(td); out["pre_identical"].append(pre); out["region_match"].append(rm)
            print("competency seed %d eye@ages %s pre-identical %s (%.0fs)" % (
                s, [round(float(out["base_eye"][-1][t]), 1) for t in ages], all(pre), time.time() - t0), flush=True)
        if a.injury_k > 0:
            a.injury_cells = "random-%d" % a.injury_k
        meta = dict(mode="competency", ages=ages, injury_cells=a.injury_cells, injury_k=a.injury_k, injury_state=a.injury_state, follow=a.follow, noise=a.noise,
                    competency=a.competency, window="inj_eye/type_diff index 0 = step t-1, index k = step t-1+k")
    meta.update(muse_commit="9404ec3", mindcraft_commit="c93ac2c9")
    np.savez_compressed(a.out, **{k: np.asarray(v) for k, v in out.items()}, meta=json.dumps(meta))


if __name__ == "__main__":
    main()
