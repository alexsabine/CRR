"""SEC-PG on T4's byte-level Transformer: library (written 2026-10-08 for CPU-1, development register).

Generalises run() in studies/SEC-OBS1-2026-10-08/llm_pilot/pg_t4_pilot.py. With the defaults (anchor 'sec', multiplier 1/16, three
protected maps, switch 0.25, energy 0.97, 32 basis sequences) it executes the pilot's computation in the same order, so it reproduces
the pilot's numbers on the same anchor (checked by cpu1/cpu1_run.py --check).

What can vary (CPU-1's variants, LLM_NEXT_STEPS.md):
  maps       3: attention in-projection, MLP up- and down-projection (the pilot);
             4: the same plus the attention out-projection. Its input (the concatenated head outputs) is recomputed from the
                in-projection input with an explicit causal attention, used for the basis only; checked against the module.
  switch     fraction of task B after which the update projection is on.
  threshold  GPM energy threshold for the basis rank.
  anchor     'sec': weight alpha * s * kappa_mult * F (SEC's weight scaled down); 'const': weight const * F.
  gpm        False gives the light anchor alone.

Task-B stream, optimiser, the adaptive-metric proximal anchor step and the evaluation sets are those of T4's continue_on_B
(CRR-LLM-CALIBRATION/llm/cl.py), with the same seeds."""
import math, time, numpy as np, torch, torch.nn.functional as F
from cl import GPT, set_flat, flat, eval_loss, fixed_eval_set, batches, DATA, domain, CTX, BATCH, TOK_PER_STEP, make_opt, adam_metric
ALPHA, TOK, LR = 10.0, 1_000_000, 3e-4

def attn_concat(attn, a, mask):
    """input to attn.out_proj for input a (B, T, d): causal multi-head attention without the output projection"""
    B, T, d = a.shape; h = attn.num_heads; hd = d//h
    q, k, v = F.linear(a, attn.in_proj_weight, attn.in_proj_bias).split(d, -1)
    q, k, v = (t.reshape(B, T, h, hd).transpose(1, 2) for t in (q, k, v))
    att = (q @ k.transpose(-2, -1))/math.sqrt(hd); att = att.masked_fill(mask[:T, :T], float('-inf')).softmax(-1)
    return (att @ v).transpose(1, 2).reshape(B, T, d)

def gpm_bases(m, xs, threshold=0.97, maps=3):
    caps = {}; hooks = []
    for bi, b in enumerate(m.blocks):
        hooks.append(b.ln1.register_forward_hook(lambda mod, i, o, bi=bi: caps.setdefault((bi, 'in_proj'), []).append(o.detach().reshape(-1, o.shape[-1]))))
        hooks.append(b.ln2.register_forward_hook(lambda mod, i, o, bi=bi: caps.setdefault((bi, 'mlp0'), []).append(o.detach().reshape(-1, o.shape[-1]))))
        hooks.append(b.mlp[1].register_forward_hook(lambda mod, i, o, bi=bi: caps.setdefault((bi, 'mlp2'), []).append(o.detach().reshape(-1, o.shape[-1]))))
        if maps == 4:
            def hook_out(mod, i, o, bi=bi, b=b):
                c = attn_concat(b.attn, o.detach(), m.mask); caps.setdefault((bi, 'out_proj'), []).append(c.reshape(-1, c.shape[-1]))
                ref = b.attn(o.detach(), o.detach(), o.detach(), attn_mask=m.mask[:o.shape[1], :o.shape[1]], need_weights=False)[0]
                err = float((F.linear(c, b.attn.out_proj.weight, b.attn.out_proj.bias) - ref).abs().max()); caps.setdefault('_check', []).append(err)
            hooks.append(b.ln1.register_forward_hook(hook_out))
    with torch.no_grad(): m(torch.from_numpy(xs))
    for h in hooks: h.remove()
    check = max(caps.pop('_check', [0.0])); assert check < 1e-4, f'out_proj input reconstruction error {check}'
    bases = {}
    for k, v in caps.items():
        R = torch.cat(v, 0); U, S, _ = torch.linalg.svd(R.T, full_matrices=False); e = (S**2).cumsum(0)/(S**2).sum(); r = int((e < threshold).sum()) + 1; bases[k] = U[:, :r].clone()
    return bases, check

def weight_of(m, key):
    bi, kind = key; b = m.blocks[bi]
    return {'in_proj': b.attn.in_proj_weight, 'out_proj': b.attn.out_proj.weight, 'mlp0': b.mlp[0].weight, 'mlp2': b.mlp[2].weight}[kind]

def run(pre, seed, anchor='sec', kappa_mult=1/16, const=None, gpm=True, switch=0.25, threshold=0.97, maps=3, basis_seqs=32, new_domain='B'):
    d, L = pre['d'], pre['layers']; torch.manual_seed(10_000 + seed); rng = np.random.default_rng(10_000 + seed); m = GPT(d, L, 4, CTX); set_flat(m, pre['theta_A']); a = pre['theta_A'].clone()
    w = ALPHA*pre['s']*kappa_mult*pre['F'] if anchor == 'sec' else const*pre['F']; opt = make_opt(m, LR); steps = TOK//TOK_PER_STEP; DB = domain(new_domain); B = DB['dev']; t0 = time.time()
    xyA = {k: fixed_eval_set(DATA['A'][k], 2000 + seed, 64, CTX) for k in ('val', 'test')}; xyB = {k: fixed_eval_set(DB[k], 3000 + seed, 64, CTX) for k in ('val', 'test')}
    tg = time.time(); bases, check = gpm_bases(m, fixed_eval_set(DATA['A']['dev'], 7100 + seed, basis_seqs, CTX)[0], threshold, maps) if gpm else ({}, None); t_bases = time.time() - tg; t_proj = 0.0
    on_from = int(round(switch*steps))
    for s in range(steps):
        x, y = batches(B, rng, BATCH, CTX); xt, yt = torch.from_numpy(x), torch.from_numpy(y); m.zero_grad(); logits = m(xt); loss = F.cross_entropy(logits.reshape(-1, 256), yt.reshape(-1)); loss.backward()
        project = gpm and s >= on_from
        if project: old = {k: weight_of(m, k).detach().clone() for k in bases}
        opt.step()
        if project:
            t1 = time.time()
            with torch.no_grad():
                for k, U in bases.items():
                    W = weight_of(m, k); dW = W - old[k]; W.copy_(old[k] + dW - (dW @ U) @ U.T)
            t_proj += time.time() - t1
        th = flat(m); eta = opt.param_groups[0]['lr']; D = adam_metric(opt, m); set_flat(m, (D*th + eta*w*a)/(D + eta*w))
    n_par = sum(p.numel() for p in m.parameters()); basis_floats = sum(int(U.numel()) for U in bases.values())
    return dict(A_val=eval_loss(m, xyA['val']), A_test=eval_loss(m, xyA['test']), B_val=eval_loss(m, xyB['val']), B_test=eval_loss(m, xyB['test']), seconds=time.time() - t0,
                seconds_bases=t_bases, seconds_projection=t_proj, gpm_ranks={f'{k[0]}:{k[1]}': int(U.shape[1]) for k, U in bases.items()}, gpm_dims={f'{k[0]}:{k[1]}': int(U.shape[0]) for k, U in bases.items()},
                basis_floats=basis_floats, params=n_par, basis_frac=basis_floats/n_par, out_proj_check=check,
                anchor=anchor, kappa_mult=kappa_mult, const=const, gpm=gpm, switch=switch, threshold=threshold, maps=maps, basis_seqs=basis_seqs, finite=bool(torch.isfinite(flat(m)).all()))
