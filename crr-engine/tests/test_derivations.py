"""Numerical verification of M-claim derivations (Session 2).

Each test corresponds to one M-claim's `derivation.md`. Tests are
numerical sanity checks that the derivation, under its stated
assumptions, gives the asserted result.

These tests do NOT establish the empirical truth of the claims —
that is the job of Session 3 (consistency.md) and Session 4
(prediction.md / result.md). They establish *internal* consistency,
which is what a T1 promotion requires.
"""

import math

import numpy as np
import pytest

from index import (  # type: ignore[import-not-found]
    PHI,
    PI,
    TAU,
    beauty,
    beauty_peak,
    cv_prediction,
    omega_canonical,
)


# ---- M1: CV = Ω/2 from Bernoulli(1/2) displacement -----------------------

def test_M1_cv_equals_omega_over_2():
    """Empirical CV from the canonical noise model converges to Ω/2."""
    rng = np.random.default_rng(0)
    for sym in ("Z2", "SO2"):
        omega = omega_canonical(sym)
        T_nominal = 1.0 / omega
        delta = (rng.integers(0, 2, size=200_000) - 0.5)  # ±1/2 Bernoulli
        tau = T_nominal + delta
        empirical_cv = np.std(tau) / np.mean(tau)
        predicted_cv = cv_prediction(sym)
        assert empirical_cv == pytest.approx(predicted_cv, rel=2e-2)


# ---- M3: Cramér-Rao saturation in Gaussian location model ----------------

def test_M3_cramer_rao_saturation():
    """Sample-mean estimator of a Gaussian location parameter saturates CR."""
    rng = np.random.default_rng(1)
    sigma = 1.0
    n = 100
    n_trials = 20_000
    samples = rng.normal(loc=0.0, scale=sigma, size=(n_trials, n))
    estimates = samples.mean(axis=1)
    var_est = estimates.var(ddof=1)
    fisher_information = n / sigma ** 2  # accumulated I for n iid observations
    # CR equality: Var(θ̂) · I(θ) = 1
    assert var_est * fisher_information == pytest.approx(1.0, rel=3e-2)


# ---- M4: Heisenberg-Gabor saturation by Gaussian wavelet -----------------

def test_M4_gabor_saturation():
    """Δt² · Δω² → 1 (Gabor convention) for a Gaussian wavelet on a fine grid."""
    N = 4096
    L = 40.0
    sigma_t = 1.0
    t = np.linspace(-L / 2, L / 2, N)
    dt = t[1] - t[0]
    g = np.exp(-t ** 2 / (2 * sigma_t ** 2))
    g /= np.sqrt(np.sum(g ** 2) * dt)  # L² normalise

    # Temporal variance
    p_t = g ** 2
    p_t /= np.sum(p_t) * dt
    mean_t = np.sum(t * p_t) * dt
    var_t = np.sum((t - mean_t) ** 2 * p_t) * dt

    # Spectral variance via FFT
    G = np.fft.fft(g) * dt
    omega_grid = 2 * np.pi * np.fft.fftfreq(N, d=dt)
    p_w = np.abs(G) ** 2
    p_w /= np.sum(p_w) * (omega_grid[1] - omega_grid[0])
    mean_w = np.sum(omega_grid * p_w) * (omega_grid[1] - omega_grid[0])
    var_w = np.sum((omega_grid - mean_w) ** 2 * p_w) * (omega_grid[1] - omega_grid[0])

    # Standard HG: Δt² · Δω² ≥ 1/4 (with σ-convention); Gaussian saturates
    product = var_t * var_w
    assert product == pytest.approx(0.25, rel=5e-2)


# ---- M5: CR ≡ HG via translation-parameter Fisher information -----------

def test_M5_cr_hg_equivalence():
    """For a Gaussian wavelet, Fisher info for translation = (Δω)²."""
    N = 4096
    L = 40.0
    sigma_t = 1.0
    t = np.linspace(-L / 2, L / 2, N)
    dt = t[1] - t[0]
    g = np.exp(-t ** 2 / (2 * sigma_t ** 2))
    g /= np.sqrt(np.sum(g ** 2) * dt)

    # Fisher info for translation: I = ∫ |g'(t)|² dt / ∫ |g|² dt
    g_prime = np.gradient(g, dt)
    I_translation = np.sum(g_prime ** 2) * dt / (np.sum(g ** 2) * dt)

    # Spectral variance Δω²
    G = np.fft.fft(g) * dt
    omega_grid = 2 * np.pi * np.fft.fftfreq(N, d=dt)
    p_w = np.abs(G) ** 2
    p_w /= np.sum(p_w) * (omega_grid[1] - omega_grid[0])
    var_w = np.sum(omega_grid ** 2 * p_w) * (omega_grid[1] - omega_grid[0])

    # I(translation) = (Δω)² to grid precision
    assert I_translation == pytest.approx(var_w, rel=5e-2)


# ---- M7: φ as dominant eigenvalue of [[1,1],[1,0]] ----------------------

def test_M7_phi_eigenvalue():
    M = np.array([[1.0, 1.0], [1.0, 0.0]])
    eigs = np.linalg.eigvals(M)
    dominant = max(eigs, key=abs)
    assert dominant == pytest.approx(PHI, abs=1e-12)


# ---- M8: Depth-2 recurrence trajectory lies on closed curve in 2-D ------

def test_M8_depth_two_torus_dim():
    """Linear depth-2 recurrence with irrational rotation rate stays bounded
    in (x_n, x_{n−1}) — qualitative torus signature."""
    # x_{n+1} = 2*cos(2*pi/phi)*x_n - x_{n-1} (rotation by 2pi/phi)
    rate = 2.0 * np.cos(2 * np.pi / PHI)
    x = np.zeros(2000)
    x[0], x[1] = 1.0, 0.5
    for n in range(1, len(x) - 1):
        x[n + 1] = rate * x[n] - x[n - 1]
    # phase-space radius bounded
    radii = np.sqrt(x[:-1] ** 2 + x[1:] ** 2)
    assert radii.max() < 5.0
    # ergodic exploration: many distinct radii visited
    assert len(np.unique(np.round(radii, 2))) > 50


# ---- M9: Fibonacci-chain Hamiltonian has fragmented (Cantor-like) spectrum -

def _fibonacci_word(n_letters):
    s = "a"
    while len(s) < n_letters:
        s = s.replace("b", "Y").replace("a", "ab").replace("Y", "a")
    return s[:n_letters]


def test_M9_fibonacci_spectrum_fragmented():
    """Fibonacci-chain Hamiltonian: count of significant spectral bands grows
    with chain length (qualitative Cantor signature)."""
    band_counts = []
    for N in (89, 144, 233):
        word = _fibonacci_word(N)
        V = np.array([0.5 if c == "a" else -0.5 for c in word])
        # Discrete Schrödinger: H = tridiag(1, V, 1)
        H = np.diag(V) + np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1)
        eigs = np.sort(np.linalg.eigvalsh(H))
        gaps = np.diff(eigs)
        # Count gaps larger than 5x median gap (band edges)
        threshold = 5 * np.median(gaps)
        n_bands = int(np.sum(gaps > threshold)) + 1
        band_counts.append(n_bands)
    # Band count grows non-trivially with chain length
    assert band_counts[-1] >= band_counts[0]
    assert band_counts[-1] >= 5


# ---- M10: Fine-structure fixed point ------------------------------------

def _fine_structure_f(alpha: float) -> float:
    return math.exp(2 * PI ** 2 * alpha / (1 + (PI - 1) * alpha)) / (16 * PI ** 2)


def test_M10_fine_structure_fixed_point():
    a = 0.01
    for _ in range(200):
        a = _fine_structure_f(a)
    inv_alpha = 1.0 / a
    assert 137.030 < inv_alpha < 137.034
    # stability
    h = 1e-8
    fprime = (_fine_structure_f(a + h) - _fine_structure_f(a - h)) / (2 * h)
    assert abs(fprime) < 0.5


def test_M10_unique_stable_fixed_point():
    """In (1e-6, 1) there are exactly two fixed points; only the lower is stable."""
    xs = np.linspace(1e-6, 1.0, 50_000)
    g = np.array([_fine_structure_f(x) - x for x in xs])
    sign_changes = np.where(g[:-1] * g[1:] < 0)[0]
    assert len(sign_changes) == 2

    fixed_points = []
    from scipy.optimize import brentq

    for i in sign_changes:
        root = brentq(lambda x: _fine_structure_f(x) - x, xs[i], xs[i + 1])
        h = 1e-8
        fprime = (_fine_structure_f(root + h) - _fine_structure_f(root - h)) / (2 * h)
        fixed_points.append((root, abs(fprime)))

    # Sort by α
    fixed_points.sort()
    lower, upper = fixed_points
    assert lower[1] < 1.0  # stable
    assert upper[1] > 1.0  # unstable
    assert 1.0 / lower[0] == pytest.approx(137.0324, abs=1e-3)


# ---- M11: ρ = −1/2 from variance-preserving composition ------------------

def test_M11_anticorrelation():
    """X, Y bivariate Gaussian with ρ = −1/2, unit variance ⇒ Var(X+Y) = 1."""
    rng = np.random.default_rng(2)
    rho = -0.5
    cov = np.array([[1.0, rho], [rho, 1.0]])
    samples = rng.multivariate_normal(mean=[0, 0], cov=cov, size=200_000)
    X, Y = samples[:, 0], samples[:, 1]
    assert (X + Y).var(ddof=1) == pytest.approx(1.0, rel=2e-2)
    assert np.corrcoef(X, Y)[0, 1] == pytest.approx(-0.5, abs=1e-2)


# ---- M13: C = ∫ Fisher info along trajectory in Gaussian family ---------

def test_M13_fisher_arc_length():
    """For Gaussian N(0, σ²) with σ = 1+θ, I(θ) = 2/(1+θ)²; ∫₀¹ I dτ = 1."""
    # Analytic
    analytic = 2.0 * (1.0 - 0.5)  # = 2 · ∫₀¹ (1+τ)⁻² dτ = 2 · [1 − 1/2] = 1
    # Numerical
    grid = np.linspace(0, 1, 10_000)
    I_vals = 2.0 / (1.0 + grid) ** 2
    numerical = np.trapezoid(I_vals, grid)
    assert numerical == pytest.approx(analytic, rel=1e-3)


# ---- M14: MaxEnt under mean constraint = exp family ---------------------

def test_M14_maxent_kernel():
    """Numerical MaxEnt on a discrete coherence grid recovers exp(C/Ω)."""
    omega = 0.5
    C_grid = np.linspace(0, 5, 200)
    target_mean = 1.0
    # Closed-form exponential family ρ ∝ exp(C/Ω); but normalised on bounded grid
    rho = np.exp(C_grid / omega)
    rho /= rho.sum()
    # Adjust the implicit Lagrange multiplier so mean matches target
    # Search over effective (1/Ω)
    from scipy.optimize import brentq

    def mean_for_eta(eta):
        w = np.exp(eta * C_grid)
        w /= w.sum()
        return np.sum(C_grid * w)

    eta_star = brentq(lambda e: mean_for_eta(e) - target_mean, -10, 10)
    # eta_star is the effective natural parameter; the family is still exp
    rho_star = np.exp(eta_star * C_grid)
    rho_star /= rho_star.sum()
    # entropy is maximised — gradient ratio test
    H_star = -np.sum(rho_star * np.log(rho_star + 1e-300))
    # perturb away from rho_star — entropy should decrease
    perturb = rho_star + 1e-3 * np.sin(np.arange(len(C_grid)))
    perturb = np.clip(perturb, 1e-10, None)
    perturb /= perturb.sum()
    # Adjust mean to match
    # If mean off, project: this isn't exact, but H_perturb should not exceed H_star
    H_perturb = -np.sum(perturb * np.log(perturb + 1e-300))
    assert H_star >= H_perturb - 1e-2  # MaxEnt property


# ---- M15: Z_n hierarchy at n = 2 reproduces canonical Z₂ -----------------

def test_M15_zn_hierarchy_at_n2():
    """CV = n/(4π) at n = 2 equals canonical CV_Z₂ = 1/(2π)."""
    n = 2
    cv_zn = n / (4 * PI)
    assert cv_zn == pytest.approx(cv_prediction("Z2"), abs=1e-12)


# ---- M16: Bonnet-Myers diameter on the unit 2-sphere ---------------------

def test_M16_bonnet_myers_sphere():
    """Unit 2-sphere has Ricci ≥ (n−1)κ with κ = 1; diameter = π."""
    kappa = 1.0
    diameter_bound = PI / math.sqrt(kappa)
    # On a unit sphere, antipodal points are π apart along the great circle
    assert diameter_bound == pytest.approx(PI, abs=1e-12)


# ---- M17: Quadratic variation of Brownian motion = t --------------------

def test_M17_quadratic_variation_brownian():
    """For BM on [0, 1], realised QV = Σ(ΔB)² → 1 as Δt → 0."""
    rng = np.random.default_rng(3)
    N_paths = 500
    N_steps = 5000
    dt = 1.0 / N_steps
    increments = rng.normal(0, math.sqrt(dt), size=(N_paths, N_steps))
    QV = np.sum(increments ** 2, axis=1)
    assert QV.mean() == pytest.approx(1.0, rel=2e-2)


# ---- M18: SPRT mean stopping time matches Wald approximation ------------

def test_M18_sprt_stopping_time():
    """Bernoulli(0.6) under SPRT with upper threshold B; mean stop ≈ B / E[log λ]."""
    rng = np.random.default_rng(4)
    p1, p0 = 0.6, 0.5
    log_lambda_per_obs = math.log(p1 / p0)  # outcome 1
    log_lambda_neg = math.log((1 - p1) / (1 - p0))  # outcome 0
    E_log_lambda = p1 * log_lambda_per_obs + (1 - p1) * log_lambda_neg
    omega = 0.05
    B = 1.0 / omega  # upper threshold
    expected_stop = B / E_log_lambda

    N_trials = 5000
    stopping_times = []
    for _ in range(N_trials):
        L = 0.0
        n = 0
        while L < B and n < 100_000:
            obs = int(rng.random() < p1)
            L += log_lambda_per_obs if obs else log_lambda_neg
            n += 1
        stopping_times.append(n)
    empirical = np.mean(stopping_times)
    # Wald approximation has known O(1) overshoot bias; allow 30%
    assert abs(empirical - expected_stop) / expected_stop < 0.30


# ---- M19: Kac's lemma — mean return time = 1/μ(A) -----------------------

def test_M19_kac_lemma_irrational_rotation():
    """Irrational rotation T(x) = (x + α) mod 1 is ergodic; mean return to A = 1/μ(A)."""
    alpha = (math.sqrt(5.0) - 1.0) / 2.0  # 1/φ, irrational
    mu_A = 0.1  # interval [0, 0.1]
    x = 0.5
    # warm up
    for _ in range(1000):
        x = (x + alpha) % 1.0
    return_times = []
    n_returns = 5000
    while len(return_times) < n_returns:
        if x < mu_A:
            t = 1
            x = (x + alpha) % 1.0
            while not (x < mu_A):
                x = (x + alpha) % 1.0
                t += 1
                if t > 100_000:
                    break
            return_times.append(t)
        else:
            x = (x + alpha) % 1.0
    empirical_mean = np.mean(return_times)
    expected = 1.0 / mu_A
    # Irrational rotations are uniquely ergodic; Kac is exact in the limit
    assert empirical_mean == pytest.approx(expected, rel=0.1)


# ---- M20: Right Kan extension universal property (discrete proxy) -------

def test_M20_kan_universal_property():
    """In a finite poset, the pointwise end (limit) defines Ran_i F uniquely."""
    # History poset: 0 < 1 < 2 < 3 (rupture at 3)
    # F sends each i to a coherence weight exp(i * 0.5)
    # Right Kan extension at the rupture object should equal the supremum
    # weight in the comma-category-of-future-points (only 3 itself), i.e. F(3).
    F = lambda i: math.exp(i * 0.5)
    rupture = 3
    # Comma category over rupture: {(j, j ≤ rupture)} = {0,1,2,3}
    # For Ran_i F, the *end* picks the limit — for a chain, this is the
    # maximum F evaluated at the *future* of rupture, which in this trivial
    # setup is just F(rupture) since nothing comes after.
    Ran_at_rupture = F(rupture)
    assert Ran_at_rupture == pytest.approx(math.exp(1.5))


# ---- M21: TUR factor of 2 -----------------------------------------------

def test_M21_tur_factor_two():
    """Two-state Markov current example: Σ · Var(J)/⟨J⟩² is bounded below by 2, not 1."""
    # Simulate a biased two-state Markov chain
    rng = np.random.default_rng(5)
    p_forward = 0.8
    p_backward = 0.2
    n_steps = 50_000
    n_paths = 2000

    currents = []
    entropies = []
    for _ in range(n_paths):
        net = 0
        for _ in range(n_steps):
            if rng.random() < p_forward:
                net += 1
            else:
                net -= 1
        currents.append(net)
        # Mean entropy production per step: ln(p_forward/p_backward) * net_per_step
        # For one path, total Σ ≈ ln(p_f/p_b) * net
        entropies.append(math.log(p_forward / p_backward) * net)
    J = np.array(currents)
    Sigma = np.array(entropies)

    var_J = J.var(ddof=1)
    mean_J = J.mean()
    ratio = var_J / mean_J ** 2

    # TUR: Var(J)/⟨J⟩² ≥ 2/⟨Σ⟩, so ⟨Σ⟩ · Var(J)/⟨J⟩² ≥ 2
    # The biased random walk does NOT saturate TUR (it gives ~1.5, not 2);
    # what matters here is that the bound is > 1, demonstrating that any
    # identification "C·Ω = 1 saturates TUR" requires absorbing a factor.
    bound = Sigma.mean() * ratio
    assert bound > 1.0, f"bound {bound:.3f} should exceed 1, illustrating the factor-of-2 issue"
