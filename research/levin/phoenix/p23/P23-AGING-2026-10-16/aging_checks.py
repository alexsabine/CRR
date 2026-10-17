#!/usr/bin/env python3
"""Checks on the ageing NCA of Pio-Lopez, Hartl & Levin (2025, Adv. Sci. e09872), using the authors' code unchanged:
github.com/bhartl/muse @ 9404ec3 (examples/aging-as-loss-of-goal-directedness: pretrained smiley_16x16 agent,
aging.py, recovery.py) and its training stack github.com/bhartl/NeurEvo (mindcraft) @ c93ac2c9.

Every arm runs the published recovery protocol (organ score <= threshold -> intervene, development 150, horizon 25,
noise 0.15, competency 1.0, 1000 steps) through the authors' own `recovery.set_initial_state`, except where an arm
changes exactly one thing. Each episode is a separate seeded lifetime, so arms are paired by seed (identical up to
the first intervention).

Arms
  NONE         no intervention (threshold -1: the trigger never fires)
  A_RESET      paper method A: inject the primordial (initial) state into the whole organ; clear the RNN memory
               of the injected cells (reset_memory=True, as in every published notebook run)
  A_KEEP       method A, but the injected cells keep their RNN memory (reset_memory=False)
  B_RESET      paper method B: inject the primordial state only into wrongly expressed organ cells; clear memory
  B_KEEP       method B, keep memory
  MEM_ORGAN    no state injection: only clear the RNN memory of the whole organ (same trigger)
  MEM_WRONGS   no state injection: only clear the RNN memory of wrongly expressed organ cells
  ... with --socket the organ masks add the eye sockets (the paper's organ+socket variant).
  PERTURB_RNN    memory timescale: at --perturb_step, zero the RNN memory of every cell, nothing else (compare
                 with NONE at the same seed: identical until then)
  PERTURB_HIDDEN at --perturb_step, zero the hidden (communication) channel of every cell's state
  History test for the "memory of lost structures" (the left eye; same present, different past):
  LOST_*         normal development; at step --T the left-eye cells are overwritten with a face-typed state and
                 their RNN memory is cleared (the eye is lost at T)
  NEVER_*        from step 0 to --T the left-eye cells are held at that same face-typed state with cleared memory
                 every step (the eye never forms); released at T
  *_INJ          at T, after the overwrite, the paper's regenerative information is injected into the left-eye cells
                 (primordial state, memory cleared: method A for that organ); *_NOINJ: nothing is injected
  LOST_B/NEVER_B exploratory (added after the freeze): as *_NOINJ, then from step T + delay the paper's method B
                 (recovery.set_initial_state, wrong cells only, memory cleared, threshold 0.6, horizon 25) runs for
                 the left eye

Usage (from the example directory, with MUSE and MINDCRAFT on the path):
  python -I aging_checks.py --muse MUSE --mindcraft MINDCRAFT --arm B_RESET --seeds 0:10 --out OUT.npz [--socket]
  python -I aging_checks.py ... --arm NONE --noise 0 --competency 1 --seeds 0:3 --out OUT.npz   # noise-free ageing
"""
import argparse
import json
import os
import sys
import time
from functools import partial

import numpy as np

ARMS = ("NONE", "A_RESET", "A_KEEP", "B_RESET", "B_KEEP", "MEM_ORGAN", "MEM_WRONGS",
        "PERTURB_RNN", "PERTURB_HIDDEN", "LOST_NOINJ", "NEVER_NOINJ", "LOST_INJ", "NEVER_INJ", "LOST_B", "NEVER_B")
FACE_STATE = np.array([-3., 3., -3., 0.])   # a fully "face"-typed cell (one-hot channels in [-3, 3]), hidden channel 0


def organ_masks(socket):
    # copied from the published notebooks (aging-smiley_16x16-recovery-*.ipynb), coordinates are (x, y)
    left_eye = np.array([[5, 3], [4, 4], [5, 4], [6, 4], [4, 5], [5, 5], [6, 5], [4, 6], [5, 6], [6, 6]])
    left_eye_socket = np.array([[4, 3], [6, 3], [3, 4], [7, 4], [3, 5], [7, 5], [3, 6], [7, 6], [4, 7], [5, 7], [6, 7]])
    right_eye = [15, 0] + left_eye * [[-1, 1]]
    right_eye_socket = [15, 0] + left_eye_socket * [[-1, 1]]
    mouth = np.concatenate([[[4 + i, 10] for i in range(8)], [[4 + i, 11] for i in range(8)], [[5 + i, 12] for i in range(6)]])
    return dict(left_eye=left_eye, right_eye=right_eye, mouth=mouth,
                left_eye_socket=left_eye_socket if socket else None,
                right_eye_socket=right_eye_socket if socket else None)


def memory_only(world, initial_state, organ_mask, socket_mask=None, target_state=2, socket_target=1, threshold=0.,
                development=150, horizon=25, label="left_eye", only_correct_wrongs=False, Nx=16, Ny=16, N_state=4):
    """Same trigger as recovery.set_initial_state; the only action is clearing the RNN memory of the masked cells
    (no cell state is written)."""
    try:
        intervened = world.env.intervened
    except AttributeError:
        intervened = {"left_eye": [], "right_eye": [], "mouth": []}
    state = world.env.state.get_val(channel="type")
    organ_state = state[organ_mask[:, 1], organ_mask[:, 0]].argmax(axis=-1)
    socket_loss = 0
    if socket_mask is not None:
        socket_state = state[socket_mask[:, 1], socket_mask[:, 0]].argmax(axis=-1)
        socket_loss = (socket_state != socket_target).sum() / len(organ_mask)
    intervene = world.env.simulation_step >= development
    intervene &= not any(intervened[label][-horizon:])
    intervene &= (np.mean(organ_state == target_state) - socket_loss) <= threshold
    if intervene:
        injection_mask = organ_mask if socket_mask is None else np.concatenate([organ_mask, socket_mask])
        if only_correct_wrongs:
            wrongs = state[injection_mask[:, 1], injection_mask[:, 0]].argmax(axis=-1) != target_state
            mask = injection_mask[wrongs]
        else:
            mask = injection_mask
        if world.agent.policy_module._states is not None and len(mask):
            hs = world.agent.policy_module._states[0].clone().reshape(Nx, Ny, N_state)
            hs[mask[:, 1], mask[:, 0]] = 0.
            world.agent.policy_module._states[0][...] = hs.reshape(-1, N_state)
    intervened[label].append(intervene)
    world.env.intervened = intervened


def make_history_cb(arm, T, left_eye, initial_state, Nx=16, Ny=16, N_state=4, delay=0):
    def clear_memory(world, mask):
        if world.agent.policy_module._states is not None:
            hs = world.agent.policy_module._states[0].clone().reshape(Nx, Ny, N_state)
            hs[mask[:, 1], mask[:, 0]] = 0.
            world.agent.policy_module._states[0][...] = hs.reshape(-1, N_state)

    def cb(world, _value):
        t = world.env.simulation_step
        clamp = (arm.startswith("NEVER") and t <= T) or (arm.startswith("LOST") and t == T)
        if clamp:
            world.env.state.array[left_eye[:, 1], left_eye[:, 0], :] = FACE_STATE
            clear_memory(world, left_eye)
        if arm.endswith("_INJ") and t == T + delay:
            world.env.state.array[left_eye[:, 1], left_eye[:, 0], :] = initial_state[left_eye[:, 1], left_eye[:, 0], :]
            clear_memory(world, left_eye)
    return cb


def make_perturb_cb(arm, step, Nx=16, Ny=16):
    def cb(world, _value):
        if world.env.simulation_step != step:
            return
        if arm == "PERTURB_RNN" and world.agent.policy_module._states is not None:
            world.agent.policy_module._states[0][...] = 0.
        if arm == "PERTURB_HIDDEN":
            world.env.state.set_val(np.zeros((Nx, Ny, 1)), channel="hidden")
    return cb


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--muse", required=True); ap.add_argument("--mindcraft", required=True)
    ap.add_argument("--arm", choices=ARMS, required=True); ap.add_argument("--seeds", default="0:10")
    ap.add_argument("--out", required=True); ap.add_argument("--socket", action="store_true")
    ap.add_argument("--steps", type=int, default=1000); ap.add_argument("--noise", type=float, default=0.15)
    ap.add_argument("--competency", type=float, default=1.0); ap.add_argument("--threshold", type=float, default=0.6)
    ap.add_argument("--save_states", action="store_true", help="also save full 4-channel states and RNN memory (float16)")
    ap.add_argument("--perturb_step", type=int, default=300); ap.add_argument("--T", type=int, default=300)
    ap.add_argument("--delay", type=int, default=0,
                    help="exploratory (added after the freeze; 0 = frozen behaviour): inject at T + delay")
    a = ap.parse_args()
    example = os.path.join(os.path.abspath(a.muse), "examples", "aging-as-loss-of-goal-directedness")
    sys.path[:0] = [os.path.abspath(a.mindcraft), os.path.abspath(a.muse), example]
    os.chdir(example)                                   # the published configs use paths relative to this folder
    import torch
    from mindcraft import World, Agent
    import recovery

    world_path = "agents/smiley_16x16/world.yml"
    organs = organ_masks(a.socket)
    agent = Agent.make(world_path.replace("world.yml", "agent.yml"))
    initial_state = agent.state_module.state.reshape(recovery.Nx, recovery.Ny, recovery.N_state).detach()

    special = a.arm.startswith(("PERTURB", "LOST", "NEVER"))
    thr = -1.0 if (a.arm == "NONE" or special) else a.threshold
    kw = dict(threshold=thr, development=150, horizon=25)
    if a.arm in ("NONE", "A_RESET", "A_KEEP", "B_RESET", "B_KEEP") or special:
        fn = recovery.set_initial_state
        kw.update(reset_memory=a.arm.endswith("RESET") or a.arm == "NONE", only_correct_wrongs=a.arm.startswith("B"))
    else:
        fn = memory_only
        kw.update(only_correct_wrongs=(a.arm == "MEM_WRONGS"))
    cbs = {}
    for label, sock in (("left_eye", "left_eye_socket"), ("right_eye", "right_eye_socket"), ("mouth", None)):
        cbs[partial(fn, organ_mask=organs[label], socket_mask=organs[sock] if sock else None, label=label, **kw)] = \
            [initial_state.numpy() for _ in range(a.steps)]

    if a.arm.startswith("PERTURB"):
        cbs[make_perturb_cb(a.arm, a.perturb_step)] = [None] * a.steps
    if a.arm.startswith(("LOST", "NEVER")):
        cbs[make_history_cb(a.arm, a.T, organs["left_eye"], initial_state.numpy(), delay=a.delay)] = [None] * a.steps
    if a.arm in ("LOST_B", "NEVER_B"):
        cbs[partial(recovery.set_initial_state, organ_mask=organs["left_eye"], socket_mask=None, label="left_eye",
                    threshold=a.threshold, development=a.T + a.delay, horizon=25, reset_memory=True,
                    only_correct_wrongs=True)] = [initial_state.numpy() for _ in range(a.steps)]

    log = dict(log_fields=("reward", "state", "intervened", "memory"),
               log_foos={"state": "observation[:, 0].reshape(16, 16, -1)",
                         "intervened": recovery.logging["log_foos"]["intervened"],
                         "memory": "self.agent.policy_module._states[0].detach().numpy().reshape(16, 16, -1).copy() "
                                   "if self.agent.policy_module._states is not None else np.zeros((16, 16, 4))"})
    def make_world():
        # a fresh world per lifetime (the published notebooks reuse one world across episodes; a fresh one keeps
        # every episode's log identical in layout and makes episodes independent)
        w = World.make(world_path, max_steps=a.steps, n_episodes=1, schedule=cbs, verbose=False, render=False, **log)
        w.agent.sampling = a.competency
        w.env.state.noise_level = a.noise
        w.env.task.stagnation_cost = 0.
        w.env.task.completion_reward = 0.
        return w

    s0, s1 = (int(x) for x in a.seeds.split(":"))
    out = {"fitness": [], "types": [], "interventions": [], "seeds": list(range(s0, s1))}
    if a.save_states:
        out["states"], out["memory"] = [], []
    t0 = time.time()
    for s in range(s0, s1):
        world = make_world()
        torch.manual_seed(s); np.random.seed(s)
        world.env.simulation_step = 0
        world.rollout()
        ep = world.log_history[-1]
        rew = np.asarray(ep["reward"], dtype=float)
        out["fitness"].append(np.cumsum(rew))
        st = np.asarray(ep["state"])
        out["types"].append(st[..., :3].argmax(-1).astype(np.uint8))
        iv = ep["intervened"]
        out["interventions"].append([[bool(isinstance(x, dict) and x.get(k)) for x in iv]
                                     for k in ("left_eye", "right_eye", "mouth")])
        if a.save_states:
            out["states"].append(st.astype(np.float16)); out["memory"].append(np.asarray(ep["memory"], dtype=np.float16))
        print("%s seed %d final fitness %.0f mean[150:] %.1f interventions %d (%.1fs)" % (
            a.arm, s, out["fitness"][-1][-1], out["fitness"][-1][150:].mean(), int(np.sum(out["interventions"][-1])),
            time.time() - t0), flush=True)
    meta = dict(arm=a.arm, socket=a.socket, perturb_step=a.perturb_step, T=a.T, delay=a.delay, steps=a.steps, noise=a.noise, competency=a.competency, threshold=thr,
                development=150, horizon=25, muse_commit="9404ec3", mindcraft_commit="c93ac2c9")
    for k, v in out.items():
        lens = sorted(set(len(x) if hasattr(x, "__len__") else -1 for x in v))
        if len(lens) > 1:
            print("WARNING ragged", k, lens, flush=True)
    np.savez_compressed(a.out, **{k: np.asarray(v) if k != "interventions" else np.asarray(v, dtype=bool)
                                  for k, v in out.items()}, meta=json.dumps(meta))


if __name__ == "__main__":
    main()
