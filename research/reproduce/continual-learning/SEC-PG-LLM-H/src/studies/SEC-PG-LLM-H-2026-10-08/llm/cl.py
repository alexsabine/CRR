"""Continual-learning library for CRR-LLM-CALIBRATION: pretrain on domain A (cached per seed), diagonal Fisher and the secant calibration at the anchor, continuation on domain B with an anchor penalty under (a) a decoupled proximal anchor step (the AdamW-appropriate safeguard: exact implicit step on the diagonal quadratic penalty applied after the optimiser step, as decoupled weight decay is) or (b) the coupled form (penalty gradient added into the AdamW moments). Also the reference-KL line and the EMA-schedule line."""
import sys, time, json, math, pathlib, resource, copy, numpy as np, torch, torch.nn.functional as F
HERE = pathlib.Path(__file__).resolve().parent; sys.path.insert(0, str(HERE))
from model import GPT, n_params; from data import load, batches, fixed_eval_set
CTX = 128; BATCH = 16; TOK_PER_STEP = CTX*BATCH; CACHE = HERE.parent / 'outputs' / 'cache'; CACHE.mkdir(parents=True, exist_ok=True)
DATA = {d: load(d) for d in ('A', 'B')}
def domain(name):
    if name not in DATA: DATA[name] = load(name)
    return DATA[name]
def rss_mb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
def flat(m): return torch.cat([p.detach().reshape(-1) for p in m.parameters()])
def set_flat(m, v):
    i = 0
    for p in m.parameters(): n = p.numel(); p.data.copy_(v[i:i + n].reshape(p.shape)); i += n
def grad_flat(m): return torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).reshape(-1) for p in m.parameters()])
def eval_loss(m, xy):
    m.eval()
    with torch.no_grad(): x, y = xy; l = float(m.loss(torch.from_numpy(x), torch.from_numpy(y)))
    m.train(); return l
def loss_and_grad(m, xy):
    m.zero_grad(); x, y = xy; l = m.loss(torch.from_numpy(x), torch.from_numpy(y)); l.backward(); return float(l), grad_flat(m).clone()
def fisher_diag(m, arr, rng, n_micro=64, micro=2):
    """empirical Fisher diagonal approximated by the mean squared micro-batch gradient (micro-batch of 2 sequences); labelled an approximation"""
    acc = torch.zeros_like(flat(m))
    for _ in range(n_micro): _, g = loss_and_grad(m, batches(arr, rng, micro, CTX)); acc += g*g
    m.zero_grad(); return acc/n_micro
def fisher_token(m, arr, rng, n_seq=16):
    """per-token empirical Fisher diagonal: mean over tokens of the squared gradient of that token's own loss (one backward per token; 128 tokens x n_seq sequences)"""
    acc = torch.zeros_like(flat(m)); n = 0
    for _ in range(n_seq):
        x, y = batches(arr, rng, 1, CTX); xt, yt = torch.from_numpy(x), torch.from_numpy(y)
        for t in range(0, CTX, 4):  # every 4th token (32 per sequence) to bound cost; unbiased for the mean
            m.zero_grad(); logits = m(xt); l = F.cross_entropy(logits[0, t:t + 1], yt[0, t:t + 1]); l.backward(); g = grad_flat(m); acc += g*g; n += 1
    m.zero_grad(); return acc/n
def fisher_batch(m, arr, rng, n_batches=32, batch=16):
    """squared mean gradient over full batches (what Adam's second moment tracks); the coarsest estimator"""
    acc = torch.zeros_like(flat(m))
    for _ in range(n_batches): _, g = loss_and_grad(m, batches(arr, rng, batch, CTX)); acc += g*g
    m.zero_grad(); return acc/n_batches
def secant(m, xy, theta_a, theta_b, Fd):
    """s = c/rho: chord curvature of the anchor-domain loss along the last pretraining window over the curvature the Fisher claims along it (SEC10's rule, unchanged)"""
    d = theta_a - theta_b; nd2 = float(d @ d)
    set_flat(m, theta_b); Lb, gb = loss_and_grad(m, xy); set_flat(m, theta_a); La, _ = loss_and_grad(m, xy); set_flat(m, theta_b); m.zero_grad()
    c = 2.0*(La - Lb - float(gb @ d))/nd2; rho = float((Fd*d*d).sum())/nd2
    s = float(np.clip(c/rho, 1e-3, 1e6)) if (c > 0 and rho > 0) else 1.0; return s, c, rho, nd2  # clip widened from SEC10's [1e-3, 1e3] before the declaration: the micro-batch-mean Fisher estimator is under-scaled by about 1e3 (first development pass: c/rho = 1226)
def kl_chord(m, xy, theta_a, theta_b):
    """chord curvature of KL(p_theta_b || p_theta) along the same window: 2 KL(theta_a)/|d|^2 (KL and its gradient vanish at theta_b)"""
    d = theta_a - theta_b; nd2 = float(d @ d); set_flat(m, theta_b); m.eval()
    with torch.no_grad(): x = torch.from_numpy(xy[0]); pb = F.log_softmax(m(x), -1); set_flat(m, theta_a); pa = F.log_softmax(m(x), -1); kl = float((pb.exp()*(pb - pa)).sum(-1).mean())
    set_flat(m, theta_b); m.train(); return 2.0*kl/nd2, kl
def adam_metric(opt, m, eps=1e-8):
    """D = sqrt(v_hat) + eps from the optimiser state, bias-corrected with the optimiser's own step count; parameters without state (before the first step) get D = 1"""
    out = []
    for p in m.parameters():
        st = opt.state.get(p, {})
        if 'exp_avg_sq' in st:
            t = int(st['step']) if not torch.is_tensor(st['step']) else int(st['step'].item()); b2 = opt.param_groups[0]['betas'][1]; out.append((st['exp_avg_sq']/(1 - b2**t)).sqrt().reshape(-1) + eps)
        elif 'square_avg' in st: out.append(st['square_avg'].sqrt().reshape(-1) + eps)
        else: out.append(torch.ones(p.numel()))
    return torch.cat(out)
def make_opt(m, lr, wd=0.1): return torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=wd)
def pretrain(seed, d=128, layers=4, tokens=4_000_000, lr=1e-3, warmup=100, window=0.2, force=False):
    """returns dict(theta_A, F, s, c, rho, theta_a) cached per (seed, d, layers, tokens)"""
    key = CACHE / f'pre_s{seed}_d{d}_L{layers}_t{tokens}.pt'
    if key.exists() and not force: return torch.load(key)
    torch.manual_seed(seed); rng = np.random.default_rng(seed); m = GPT(d, layers, 4, CTX); opt = make_opt(m, lr); steps = tokens//TOK_PER_STEP; A = DATA['A']['dev']; t0 = time.time(); theta_a = None; curve = []
    path_len = 0.0; prev = flat(m).clone(); theta0 = prev.clone()
    for s in range(steps):
        for g in opt.param_groups: g['lr'] = lr*min(1.0, (s + 1)/warmup)
        if s == int(round((1 - window)*steps)): theta_a = flat(m).clone()
        l, _ = loss_and_grad(m, batches(A, rng, BATCH, CTX)); opt.step()
        if s % 100 == 0: cur = flat(m); path_len += float((cur - prev).norm()); prev = cur.clone(); curve.append((s, round(l, 3)))
    theta_b = flat(m).clone(); dev_xy = fixed_eval_set(A, 1000 + seed, 32, CTX); Fd = fisher_diag(m, A, rng); s_, c, rho, nd2 = secant(m, dev_xy, theta_a, theta_b, Fd); ckl, kl = kl_chord(m, dev_xy, theta_a, theta_b)
    cur = flat(m); path_len += float((cur - prev).norm()); vstat = adam_metric(opt, m); losses = [c_[1] for c_ in curve]
    out = dict(theta_A=theta_b, F=Fd, theta_a=theta_a, s=s_, c=c, rho=rho, nd2=nd2, kl_chord=ckl, kl_window=kl, seconds=time.time() - t0, curve=curve, d=d, layers=layers, tokens=tokens, params=n_params(m), path_length=path_len, disp_from_init=float((cur - theta0).norm()), D_median_end=float(vstat.median()), D_mean_end=float(vstat.mean()), loss_slope_window=(losses[-1] - losses[max(0, int(0.8*len(losses)) - 1)]) if len(losses) > 2 else None, final_train_loss=losses[-1] if losses else None); torch.save(out, key); return out
def continue_on_B(pre, seed, tokens=1_000_000, lr=3e-4, rule='none', lam=0.0, rho_pref=1.0, safeguard='proximal', kl=None, ema=None, eval_every=None, log=None, new_domain='B', F_override=None, s_override=None, controller=None, optimizer='adamw'):
    """controller (T2 feedback comparator): dict(target=rise in L_A on the calibration batch allowed at the end, K=0.1, every=20, lam0=initial lambda); multiplies the raw-F weight up or down every `every` steps to hold the measured rise at the target (an anchor-penalty analogue of the adaptive-KL controller); costs one extra evaluation per interval"""
    """rule: 'none' | 'fixed' (lam * F) | 'sec' (rho_pref * s * F) | 'kl' (reference-KL term, weight by kl dict) ; safeguard: 'proximal' (decoupled implicit anchor step) | 'coupled' (penalty gradient into AdamW)
    ema: None or dict(mode='step'|'change', tau=...) for the schedule line. Returns metrics on A and B validation and test sets, runtime, peak RSS, and the per-step effective weight statistics."""
    d, L = pre['d'], pre['layers']; torch.manual_seed(10_000 + seed); rng = np.random.default_rng(10_000 + seed); m = GPT(d, L, 4, CTX); set_flat(m, pre['theta_A']); a = pre['theta_A'].clone(); Fd = pre['F'] if F_override is None else F_override; s_cal = pre['s'] if s_override is None else s_override
    w = None
    if rule == 'fixed': w = lam*Fd
    elif rule == 'sec': w = rho_pref*s_cal*Fd
    ref = None
    if rule == 'kl': ref = GPT(d, L, 4, CTX); set_flat(ref, a); ref.eval()
    opt = make_opt(m, lr) if optimizer == 'adamw' else torch.optim.SGD(m.parameters(), lr=lr, momentum=0.9, weight_decay=0.0) if optimizer == 'sgdm' else torch.optim.RMSprop(m.parameters(), lr=lr, alpha=0.95, eps=1e-8, weight_decay=0.0); steps = tokens//TOK_PER_STEP; DB = domain(new_domain); B = DB['dev']; A = DATA['A']['dev']; t0 = time.time(); rss0 = rss_mb()
    xyA = {k: fixed_eval_set(DATA['A'][k], 2000 + seed, 64, CTX) for k in ('val', 'test')}; xyB = {k: fixed_eval_set(DB[k], 3000 + seed, 64, CTX) for k in ('val', 'test')}
    beta = kl['beta'] if kl else 0.0; kl_hist = []; beta_hist = []; ema_theta = flat(m).clone() if ema else None; ema_acc = 0.0; curve = []; diag_D = []
    cal_xy = fixed_eval_set(DATA['A']['dev'], 7000 + seed, 32, CTX) if controller else None; L0_cal = eval_loss(m, cal_xy) if controller else None; lam_hist = []
    if controller:
        lam_c = (rho_pref*s_cal if controller['lam0'] == 'sec' else controller['lam0']); w = lam_c*Fd
    for s in range(steps):
        x, y = batches(B, rng, BATCH, CTX); xt, yt = torch.from_numpy(x), torch.from_numpy(y); m.zero_grad(); logits = m(xt); lossB = F.cross_entropy(logits.reshape(-1, 256), yt.reshape(-1)); total = lossB
        if ref is not None:
            with torch.no_grad(): pr = F.log_softmax(ref(xt), -1)
            klv = (pr.exp()*(pr - F.log_softmax(logits, -1))).sum(-1).mean(); total = total + beta*klv; kl_hist.append(float(klv))
            if kl.get('controller') == 'ziegler' and s > 0 and s % kl.get('every', 20) == 0:
                err = float(np.clip((np.mean(kl_hist[-kl['every']:]) - kl['target'])/kl['target'], -0.2, 0.2)); beta = beta*(1 + kl.get('K', 0.1)*err)
            elif kl.get('controller') == 'ratio':
                gB = torch.autograd.grad(lossB, list(m.parameters()), retain_graph=True); gK = torch.autograd.grad(klv, list(m.parameters()), retain_graph=True); nb = math.sqrt(sum(float((g*g).sum()) for g in gB)); nk = math.sqrt(sum(float((g*g).sum()) for g in gK)) + 1e-12
                r = nb/nk; kl['_ema'] = r if '_ema' not in kl else 0.9*kl['_ema'] + 0.1*r; beta = min(kl['_ema'], 1e4)
            beta_hist.append(beta)
        total.backward()
        if controller and s > 0 and s % controller.get('every', 20) == 0:
            rise = eval_loss(m, cal_xy) - L0_cal
            if controller.get('mode') == 'budget': lam_c = lam_c*controller.get('up', 1.3) if rise > controller['epsilon'] else lam_c/controller.get('down', 1.1)
            else: err = float(np.clip((rise - controller['target'])/max(controller['target'], 1e-6), -0.2, 0.2)); lam_c = lam_c*(1 + controller.get('K', 0.1)*err)
            w = lam_c*Fd; lam_hist.append(lam_c)
        if w is not None and safeguard == 'coupled':
            th = flat(m); g = grad_flat(m) + w*(th - a); i = 0
            for p in m.parameters(): n = p.numel(); p.grad.copy_(g[i:i + n].reshape(p.shape)); i += n
        opt.step()
        if w is not None and safeguard == 'proximal':
            th = flat(m); eta = opt.param_groups[0]['lr']; set_flat(m, (th + eta*w*a)/(1 + eta*w))
        elif w is not None and safeguard == 'adaptive':
            # adaptive-metric proximal step (T1 hypothesis): minimise ||theta - theta_hat||^2_D/(2 eta) + 1/2 sum_i w_i (theta_i - a_i)^2 with D = sqrt(v_hat) + eps from AdamW's own state
            th = flat(m); eta = opt.param_groups[0]['lr']; D = adam_metric(opt, m); set_flat(m, (D*th + eta*w*a)/(D + eta*w))
            if s % 50 == 0: diag_D.append((s, float(D.median()), float(D.mean()), float((eta*w/D).median()), float((eta*w/D).mean()), float((eta*w/D).max())))
        if ema:
            th = flat(m)
            if ema['mode'] == 'step': tau = ema['tau']
            else: ema_acc += float((th - ema['_prev']).norm()) if '_prev' in ema else 0.0; tau = math.exp(-float((th - ema['_prev']).norm())/ema['tau']) if '_prev' in ema else 1.0
            ema['_prev'] = th.clone(); ema_theta = tau*ema_theta + (1 - tau)*th
        if eval_every and s % eval_every == 0: curve.append((s, eval_loss(m, xyA['val']), eval_loss(m, xyB['val'])))
    out = dict(rule=rule, lam=lam, rho_pref=rho_pref, safeguard=safeguard, new_domain=new_domain, s_used=s_cal if rule == 'sec' else None, seconds=time.time() - t0, peak_rss_mb=rss_mb(), tokens=tokens, A_val=eval_loss(m, xyA['val']), A_test=eval_loss(m, xyA['test']), B_val=eval_loss(m, xyB['val']), B_test=eval_loss(m, xyB['test']), curve=curve, finite=bool(torch.isfinite(flat(m)).all()))
    if w is not None:
        out.update(w_max=float(w.max()), w_median=float(w.median()), lr_w_max=float(opt.param_groups[0]['lr']*w.max()), lr_w_median=float(opt.param_groups[0]['lr']*w.median()))
        D = adam_metric(opt, m); eta = opt.param_groups[0]['lr']; out.update(D_median=float(D.median()), D_mean=float(D.mean()), D_p10=float(D.quantile(0.1)), D_p90=float(D.quantile(0.9)), eff_euclid_median=float((eta*w).median()), eff_adaptive_median=float((eta*w/D).median()), eff_adaptive_mean=float((eta*w/D).mean()), diag_D=diag_D)
    if ref is not None: out.update(kl_final=float(np.mean(kl_hist[-20:])), beta_final=beta, beta_init=kl['beta'])
    if controller: out.update(controller_lam_final=lam_c, controller_lam_hist=lam_hist[::5], controller_extra_evals=len(lam_hist), controller_rise_final=eval_loss(m, cal_xy) - L0_cal)
    if ema:
        set_flat(m, ema_theta); out.update(ema_A_val=eval_loss(m, xyA['val']), ema_B_val=eval_loss(m, xyB['val']), ema_A_test=eval_loss(m, xyA['test']), ema_B_test=eval_loss(m, xyB['test']))
    return out
def calibrate_direction(pre, seed, new_domain='B', h_rule='u', k_shadow=1, lr=3e-4, probe_batch=16, cal_seqs=32, random_direction=False):
    """T2: curvature of L_A along the incoming task's actual direction. u = theta_hat - a from k_shadow AdamW steps (fresh optimiser, momentum and weight decay included) on a FIXED incoming batch; model and optimiser are discarded afterwards (the matched runs start from the anchor with a fresh optimiser). d = h u/|u| with h by h_rule: 'u' (the proposal's own length), '10u', 'window' (the pretraining window's length sqrt(nd2)). s_dir = clip((L_A(a+d) + L_A(a-d) - 2 L_A(a)) / sum F d^2, 1e-3, 1e6) on a fixed old-task calibration batch (A dev, seed 7000+seed; disjoint from validation/test). Stability: recomputed at h/2; |log ratio| > log 2 flags unstable. Fallbacks (logged): nonfinite or nonpositive numerator or denominator -> the window s. random_direction=True replaces u by a Gaussian direction (the matched control)."""
    t0 = time.time(); d_, L = pre['d'], pre['layers']; m = GPT(d_, L, 4, CTX); set_flat(m, pre['theta_A']); a = pre['theta_A'].clone(); Fd = pre['F']; DB = domain(new_domain)
    rng_u = np.random.default_rng(6000 + seed); xb, yb = batches(DB['dev'], rng_u, probe_batch, CTX)
    if random_direction: u = torch.randn_like(a); u_norm = float(u.norm()); kind = 'random'
    else:
        opt = make_opt(m, lr)
        for _ in range(k_shadow): m.zero_grad(); l = m.loss(torch.from_numpy(xb), torch.from_numpy(yb)); l.backward(); opt.step()
        u = flat(m) - a; u_norm = float(u.norm()); kind = f'shadow_k{k_shadow}'
    set_flat(m, a); h_base = {'u': u_norm, '10u': 10*u_norm, 'window': math.sqrt(pre['nd2'])}[h_rule]; cal_xy = fixed_eval_set(DATA['A']['dev'], 7000 + seed, cal_seqs, CTX); out = dict(kind=kind, h_rule=h_rule, u_norm=u_norm, h=h_base, fallback=None)
    def curv(h):
        dvec = h*u/u_norm; set_flat(m, a + dvec); Lp = eval_loss(m, cal_xy); set_flat(m, a - dvec); Lm = eval_loss(m, cal_xy); set_flat(m, a); L0 = eval_loss(m, cal_xy); num = Lp + Lm - 2*L0; den = float((Fd*dvec*dvec).sum()); return num, den, (num/den if den > 0 else float('nan')), L0
    num, den, ratio, L0 = curv(h_base); num2, den2, ratio2, _ = curv(h_base/2); out.update(num=num, den=den, ratio=ratio, num_half=num2, den_half=den2, ratio_half=ratio2, L0=L0)
    ok = all(np.isfinite([num, den, ratio])) and num > 0 and den > 0
    out['unstable'] = bool(ok and np.isfinite(ratio2) and ratio2 > 0 and abs(math.log(ratio/ratio2)) > math.log(2))
    if ok: out['s_dir'] = float(np.clip(ratio, 1e-3, 1e6))
    else: out['s_dir'] = pre['s']; out['fallback'] = 'window_s (nonfinite or nonpositive curvature)'
    out['seconds'] = time.time() - t0; out['evals'] = 6; out['shadow_steps'] = 0 if random_direction else k_shadow; return out
def learner_state(pre, seed, n_micro=32):
    """ordinary ML quantities at the anchor, for the question 'what is s measuring?': Fisher trace/mean/median/quantiles, gradient norm and gradient noise on A, prediction entropy, effective rank of final hidden states, random-direction chord curvature (sharpness), loss and curvature along the window, Adam metric stats and path length from pretraining."""
    m = GPT(pre['d'], pre['layers'], 4, CTX); set_flat(m, pre['theta_A']); rng = np.random.default_rng(8000 + seed); Fd = pre['F']; A = DATA['A']['dev']; out = dict(F_trace=float(Fd.sum()), F_mean=float(Fd.mean()), F_median=float(Fd.median()), F_p90=float(Fd.quantile(0.9)), F_p99=float(Fd.quantile(0.99)), F_max=float(Fd.max()))
    gs = []
    for _ in range(n_micro): _, g = loss_and_grad(m, batches(A, rng, 2, CTX)); gs.append(g)
    G = torch.stack(gs); gbar = G.mean(0); out.update(grad_norm=float(gbar.norm()), grad_noise=float((G.norm(dim=1)**2).mean() - gbar.norm()**2), grad_noise_scale=float(((G.norm(dim=1)**2).mean() - gbar.norm()**2)/max(float(gbar.norm()**2), 1e-12)))
    xy = fixed_eval_set(A, 1000 + seed, 32, CTX); m.eval()
    with torch.no_grad():
        x = torch.from_numpy(xy[0]); h = m.tok(x) + m.pos(torch.arange(CTX)); mask = m.mask
        for b in m.blocks: h = b(h, mask)
        h = m.ln(h); logits = h @ m.tok.weight.T; p = torch.softmax(logits, -1); ent = float(-(p*torch.log(p + 1e-12)).sum(-1).mean()); conf = float(p.max(-1).values.mean())
        H = h.reshape(-1, h.shape[-1]); Hc = H - H.mean(0); sv = torch.linalg.svdvals(Hc); pr = sv**2/(sv**2).sum(); erank = float(torch.exp(-(pr*torch.log(pr + 1e-12)).sum()))
    m.train(); out.update(pred_entropy=ent, pred_confidence=conf, erank_hidden=erank)
    a = pre['theta_A'].clone(); h_ = math.sqrt(pre['nd2']); cal = fixed_eval_set(A, 7000 + seed, 32, CTX); set_flat(m, a); L0 = eval_loss(m, cal)
    r = torch.randn_like(a); r = h_*r/r.norm(); set_flat(m, a + r); Lp = eval_loss(m, cal); set_flat(m, a - r); Lm = eval_loss(m, cal); set_flat(m, a); out.update(sharp_random=(Lp + Lm - 2*L0)/(h_*h_), c_window=pre['c'], rho_window=pre['rho'], window_norm=h_, s=pre['s'], L_A_anchor=L0, path_length=pre.get('path_length'), disp_from_init=pre.get('disp_from_init'), D_median_end=pre.get('D_median_end'), D_mean_end=pre.get('D_mean_end'), loss_slope_window=pre.get('loss_slope_window'), final_train_loss=pre.get('final_train_loss'), tokens=pre['tokens'], d=pre['d'])
    return out
def frozen_metrics(pre, seed):
    m = GPT(pre['d'], pre['layers'], 4, CTX); set_flat(m, pre['theta_A']); xyA = {k: fixed_eval_set(DATA['A'][k], 2000 + seed, 64, CTX) for k in ('val', 'test')}; xyB = {k: fixed_eval_set(DATA['B'][k], 3000 + seed, 64, CTX) for k in ('val', 'test')}
    return dict(rule='frozen', A_val=eval_loss(m, xyA['val']), A_test=eval_loss(m, xyA['test']), B_val=eval_loss(m, xyB['val']), B_test=eval_loss(m, xyB['test']), seconds=0.0, tokens=0)
