"""SEC-OBS1 development testbed (written 2026-10-08; development register, not a preregistered study).

A small task-incremental continual learner (shared tanh MLP trunk, one head per task) on synthetic latent-variable tasks, with SEC v2 ported
unchanged from CRR-LLM-CALIBRATION/llm/cl.py: diagonal empirical Fisher from squared micro-batch gradients (64 micro-batches of 2); secant scale
s = clip(c/rho, 1e-3, 1e6) along the last 20 % of task-A training; weight w = alpha s F with alpha = 10; adaptive-metric proximal step
theta <- (D theta + eta w a)/(D + eta w) after every AdamW step, D = sqrt(v_hat) + eps from AdamW's own state.

Worlds. A latent z in R^12 is mixed into x in R^24. Task A varies latent dims 0..7 (sd 1; the rest sd 0.1); task B varies 8 dims of which
`overlap` are shared with A. Each task's labels come from its own random two-layer teacher on its own active dims. Overlap sets how much of B's
input lies in the input subspace A's features use, so it sets interference through the shared trunk.

Observation. Observation channels act only on the monitoring probes the learner sees about task A while it trains on B (and on the A-side of
the validation data used by the tuned sweep). Within one underlying history, training is therefore identical across observation conditions and
only what the monitors can see differs: this is what makes the worlds paired."""
import math, time, numpy as np, torch, torch.nn as nn, torch.nn.functional as Fn
torch.set_num_threads(1)
DZ, DX, H, KCLS = 12, 24, 64, 4
SD_OFF = 0.1

# ---------------- worlds ----------------
class Teacher:
    """random two-layer tanh teacher on a subset of latent dimensions -> 4-class labels (argmax)"""
    def __init__(self, rng, dims):
        self.dims = np.array(dims); self.W1 = rng.normal(size=(len(dims), 24))/math.sqrt(len(dims)); self.W2 = rng.normal(size=(24, KCLS))
        self.b2 = np.zeros(KCLS)
    def logits(self, z): return np.tanh(2.0*z[:, self.dims] @ self.W1) @ self.W2 + self.b2
    def __call__(self, z): return self.logits(z).argmax(1)

def make_history(seed, overlap):
    rng = np.random.default_rng(seed); M = rng.normal(size=(DZ, DX))/math.sqrt(DZ)
    dimsA = list(range(8)); dimsB = [(8 - overlap + i) % DZ for i in range(8)]
    tA = Teacher(rng, dimsA); tB = Teacher(rng, dimsB)
    # balance class frequencies roughly (bias the teacher's logits by minus the log class frequency on a calibration draw)
    for t, dims in ((tA, dimsA), (tB, dimsB)):
        z = latent(rng, 20000, dims)
        for _ in range(20):
            f = np.bincount(t(z), minlength=KCLS)/len(z); t.b2 -= 0.5*np.log(np.maximum(f, 1e-3)*KCLS)
    return dict(seed=seed, M=M, tA=tA, tB=tB, dimsA=dimsA, dimsB=dimsB, overlap=overlap)

def latent(rng, n, dims, shift=None):
    sd = np.full(DZ, SD_OFF); sd[dims] = 1.0; z = rng.normal(size=(n, DZ))*sd
    return z if shift is None else z + shift

def sample(hist, task, n, rng, shift=None):
    dims = hist['dimsA'] if task == 'A' else hist['dimsB']; z = latent(rng, n, dims, shift)
    x = z @ hist['M'] + 0.05*rng.normal(size=(n, DX)); y = (hist['tA'] if task == 'A' else hist['tB'])(z)
    return x.astype(np.float32), y.astype(np.int64), z

def a_relevant_projector(hist):
    """orthogonal projector (in x-space) onto the span of the rows of M for A's active latent dims"""
    Q, _ = np.linalg.qr(hist['M'][hist['dimsA']].T); return (Q @ Q.T).astype(np.float32)

CHANNELS = ('full', 'proj', 'alias', 'missing', 'drift', 'concept', 'hideA')

class Channel:
    """observation channel on task-A monitoring probes.
    full    : identity
    proj    : known lossy projection onto a random 12-dim subspace of x
    alias   : classes 0 and 1 merged in the observed label (an output-side Markov channel; observed loss is the merged-class NLL)
    missing : each input feature zeroed independently with probability 0.4 (mask not reported)
    drift   : covariate drift of the probe stream (A's latent mean shifted along A's dims, length 1.5); labels follow the unchanged concept
    concept : concept drift of the probe stream (for latent z_0 > 0 the observed label is a fixed permutation of the true label)
    hideA   : projection removing the A-relevant input subspace (the observation carries essentially no A information)"""
    def __init__(self, kind, hist, rng):
        self.kind = kind; self.merge = (0, 1) if kind == 'alias' else None; self.shift = None
        if kind == 'proj':
            Q, _ = np.linalg.qr(rng.normal(size=(DX, DX))); B = Q[:, :12]; self.P = (B @ B.T).astype(np.float32)
        if kind == 'hideA': self.P = (np.eye(DX, dtype=np.float32) - a_relevant_projector(hist))
        if kind == 'drift':
            d = np.zeros(DZ); d[hist['dimsA']] = rng.normal(size=len(hist['dimsA'])); self.shift = 1.5*d/np.linalg.norm(d)
        if kind == 'concept': self.perm = np.array([1, 2, 3, 0])
    def probes(self, hist, n, rng):
        """draw n task-A monitoring probes from the stream and return what the learner observes: (x_obs, y_obs, merge)"""
        x, y, z = sample(hist, 'A', n, rng, shift=self.shift)
        if self.kind in ('proj', 'hideA'): x = (x @ self.P).astype(np.float32)
        elif self.kind == 'missing': x = (x*(rng.random(x.shape) > 0.4)).astype(np.float32)
        elif self.kind == 'concept': y = np.where(z[:, 0] > 0, self.perm[y], y)
        return x, y, self.merge

# ---------------- learner ----------------
class Net(nn.Module):
    def __init__(self):
        super().__init__(); self.l1 = nn.Linear(DX, H); self.l2 = nn.Linear(H, H); self.hA = nn.Linear(H, KCLS); self.hB = nn.Linear(H, KCLS)
    def trunk(self, x): return torch.tanh(self.l2(torch.tanh(self.l1(x))))
    def forward(self, x, task): h = self.trunk(x); return self.hA(h) if task == 'A' else self.hB(h)
    def trunk_layers(self): return [self.l1, self.l2]

def flat(m): return torch.cat([p.detach().reshape(-1) for p in m.parameters()])
def set_flat(m, v):
    i = 0
    for p in m.parameters(): n = p.numel(); p.data.copy_(v[i:i + n].reshape(p.shape)); i += n
def grad_flat(m): return torch.cat([(p.grad if p.grad is not None else torch.zeros_like(p)).reshape(-1) for p in m.parameters()])
def trunk_mask(m):
    return torch.cat([torch.full((p.numel(),), 1.0 if (n.startswith('l1') or n.startswith('l2')) else 0.0) for n, p in m.named_parameters()])

def log_probs(m, x, task, merge=None):
    lp = Fn.log_softmax(m(torch.as_tensor(x), task), -1)
    if merge is None: return lp
    i, j = merge; keep = [k for k in range(KCLS) if k not in merge]
    return torch.cat([torch.logsumexp(lp[:, [i, j]], -1, keepdim=True), lp[:, keep]], -1)
def merged_labels(y, merge):
    if merge is None: return y
    keep = [k for k in range(KCLS) if k not in merge]; return np.array([0 if t in merge else 1 + keep.index(t) for t in y])
def loss_fn(m, x, y, task, merge=None): return Fn.nll_loss(log_probs(m, x, task, merge), torch.as_tensor(merged_labels(y, merge)))
def eval_loss(m, x, y, task, merge=None):
    with torch.no_grad(): return float(loss_fn(m, x, y, task, merge))
def accuracy(m, x, y, task):
    with torch.no_grad(): return float((m(torch.as_tensor(x), task).argmax(1).numpy() == y).mean())
def marginal_entropy(y, merge=None):
    yy = merged_labels(y, merge); f = np.bincount(yy)/len(yy); f = f[f > 0]; return float(-(f*np.log(f)).sum())
def make_opt(m, lr): return torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
def adam_metric(opt, m, eps=1e-8):
    out = []
    for p in m.parameters():
        st = opt.state.get(p, {})
        if 'exp_avg_sq' in st:
            t = int(st['step']) if not torch.is_tensor(st['step']) else int(st['step'].item()); b2 = opt.param_groups[0]['betas'][1]
            out.append((st['exp_avg_sq']/(1 - b2**t)).sqrt().reshape(-1) + eps)
        else: out.append(torch.ones(p.numel()))
    return torch.cat(out)

def fisher_diag(m, x, y, task, rng, n_micro=64, micro=2, merge=None):
    """cl.py's estimator: mean squared micro-batch gradient (micro-batch of 2), labels as given (empirical Fisher)"""
    acc = torch.zeros_like(flat(m))
    for _ in range(n_micro):
        idx = rng.integers(0, len(x), micro); m.zero_grad(); loss_fn(m, x[idx], y[idx], task, merge).backward(); g = grad_flat(m); acc += g*g
    m.zero_grad(); return acc/n_micro

def secant(m, x, y, theta_a, theta_b, Fd):
    """SEC v2's rule, unchanged: s = c/rho along the window displacement d = theta_a - theta_b"""
    d = theta_a - theta_b; nd2 = float(d @ d)
    set_flat(m, theta_b); m.zero_grad(); lb = loss_fn(m, x, y, 'A'); lb.backward(); gb = grad_flat(m); Lb = float(lb)
    set_flat(m, theta_a); La = eval_loss(m, x, y, 'A'); set_flat(m, theta_b); m.zero_grad()
    c = 2.0*(La - Lb - float(gb @ d))/nd2; rho = float((Fd*d*d).sum())/nd2
    s = float(np.clip(c/rho, 1e-3, 1e6)) if (c > 0 and rho > 0) else 1.0; return s, c, rho

def train_A(hist, steps, seed, lr=3e-3, batch=64, window=0.2):
    torch.manual_seed(seed); rng = np.random.default_rng(seed + 1); m = Net(); opt = make_opt(m, lr); theta_a = None; t0 = time.time()
    xA, yA, _ = sample(hist, 'A', 20000, np.random.default_rng(seed + 2))
    for s in range(steps):
        if s == int(round((1 - window)*steps)): theta_a = flat(m).clone()
        idx = rng.integers(0, len(xA), batch); m.zero_grad(); loss_fn(m, xA[idx], yA[idx], 'A').backward(); opt.step()
    theta_b = flat(m).clone(); t_train = time.time() - t0; t1 = time.time()
    Fd = fisher_diag(m, xA, yA, 'A', np.random.default_rng(seed + 3)); s_, c, rho = secant(m, xA[:512], yA[:512], theta_a, theta_b, Fd); t_cal = time.time() - t1
    # recorded at the end of A on clean held-back A data (what any learner can log at task end): loss, accuracy, label entropy
    xr, yr, _ = sample(hist, 'A', 2000, np.random.default_rng(seed + 4))
    rec = dict(L=eval_loss(m, xr, yr, 'A'), acc=accuracy(m, xr, yr, 'A'), H=marginal_entropy(yr))
    t2 = time.time(); bases = gpm_bases(m, xA[:2000]); t_gpm = time.time() - t2
    return dict(theta_A=theta_b, F=Fd, s=s_, c=c, rho=rho, steps=steps, rec=rec, gpm=bases, seconds_train=t_train, seconds_calibration=t_cal,
                seconds_gpm=t_gpm, gpm_dims=[int(b.shape[1]) for b in bases])

def gpm_bases(m, x, threshold=0.97):
    """GPM (Saha et al. 2021): per trunk layer, SVD of the layer-input representation matrix on old-task samples; keep the leading left
    singular vectors covering `threshold` of the energy"""
    bases = []
    with torch.no_grad():
        h0 = torch.as_tensor(x); inputs = [h0, torch.tanh(m.l1(h0))]
        for R in inputs:
            U, S, _ = torch.linalg.svd(R.T, full_matrices=False); e = (S**2).cumsum(0)/(S**2).sum(); k = int((e < threshold).sum()) + 1; bases.append(U[:, :k].clone())
    return bases

def subspace_energy(m, x, bases):
    """fraction of each trunk layer's input energy (on samples x) inside the stored old-task bases"""
    out = []
    with torch.no_grad():
        h0 = torch.as_tensor(x); inputs = [h0, torch.tanh(m.l1(h0))]
        for R, U in zip(inputs, bases): out.append(float(((R @ U)**2).sum()/(R**2).sum()))
    return out

def continue_B(pre, hist, seed, steps=400, lr=3e-3, batch=64, kappa=None, gpm_from=None, replay=None, replay_from=None, kappa_from=None,
               checkpoints=(), trunk_frozen=False):
    """task-B continuation from the A anchor.
    kappa: None (no anchor penalty) or the scalar multiplying F (SEC v2: kappa = alpha s; a transferred constant: kappa = const).
    gpm_from: step from which GPM is on (update projection of trunk weights off the stored old-task input subspaces; None = never).
    replay/replay_from: (x, y) buffer of clean A samples; from that step one buffer batch's A loss is added to each B step.
    kappa_from: (step, new_kappa) switches the penalty weight at a step (a stronger retention mechanism, or a recalibration).
    checkpoints: steps at which the parameter vector is saved (0 = the anchor). trunk_frozen: only the B head trains."""
    torch.manual_seed(seed + 7); m = Net(); set_flat(m, pre['theta_A'].clone()); a = pre['theta_A'].clone()
    params = [p for n, p in m.named_parameters() if (not trunk_frozen or n.startswith('hB'))]
    opt = torch.optim.AdamW(params, lr=lr, betas=(0.9, 0.95), weight_decay=0.1); rng = np.random.default_rng(seed + 10)
    xB, yB, _ = sample(hist, 'B', 20000, np.random.default_rng(seed + 11)); Fd = pre['F']; t0 = time.time(); saved = {}
    if 0 in checkpoints: saved[0] = flat(m).clone()
    full_params = list(m.parameters()); kap = kappa; gpm_t = 0.0; prox_t = 0.0
    for s in range(steps):
        if kappa_from is not None and s == kappa_from[0]: kap = kappa_from[1]
        use_gpm = gpm_from is not None and s >= gpm_from; use_rep = replay is not None and replay_from is not None and s >= replay_from
        if use_gpm: old = [L.weight.detach().clone() for L in m.trunk_layers()]
        idx = rng.integers(0, len(xB), batch); m.zero_grad(set_to_none=True); loss = loss_fn(m, xB[idx], yB[idx], 'B')
        if use_rep: j = rng.integers(0, len(replay[0]), batch); loss = loss + loss_fn(m, replay[0][j], replay[1][j], 'A')
        loss.backward(); opt.step()
        if use_gpm:
            t1 = time.time()
            with torch.no_grad():
                for L, U, W0 in zip(m.trunk_layers(), pre['gpm'], old):
                    dW = L.weight - W0; L.weight.copy_(W0 + dW - (dW @ U) @ U.T)
            gpm_t += time.time() - t1
        if kap is not None and kap > 0:
            t1 = time.time(); th = flat(m); eta = opt.param_groups[0]['lr']
            if trunk_frozen: D = torch.ones_like(th)
            else: D = adam_metric(opt, m)
            w = kap*Fd; set_flat(m, (D*th + eta*w*a)/(D + eta*w)); prox_t += time.time() - t1
        if (s + 1) in checkpoints: saved[s + 1] = flat(m).clone()
    return dict(theta=flat(m).clone(), seconds=time.time() - t0, seconds_gpm=gpm_t, seconds_prox=prox_t, checkpoints=saved)

def true_eval(theta, hist, seed):
    """the territory: clean test sets drawn from the world's own A and B distributions (never shown to any method)"""
    m = Net(); set_flat(m, theta); rng = np.random.default_rng(seed + 99)
    xA, yA, _ = sample(hist, 'A', 4000, rng); xB, yB, _ = sample(hist, 'B', 4000, rng)
    LA, LB = eval_loss(m, xA, yA, 'A'), eval_loss(m, xB, yB, 'B')
    return dict(A=LA, B=LB, J=0.5*(LA + LB), accA=accuracy(m, xA, yA, 'A'), accB=accuracy(m, xB, yB, 'B'))
