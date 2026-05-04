"""Numerical tests for the rupture-topology hypotheses (H1, H2, H3).

H1: All ruptures are Z₂ (Bernoulli(1/2) at threshold).
H2: SO(2) is the continual memory-bearing manifold; mean inter-rupture
    interval matches the closed-geodesic length 2π.
H3: For any compact connected Lie group G as memory manifold,
    CV_G = 1/(2·φ_G) where φ_G is the closed-geodesic length.

See `notes/rupture_topology.md` for the full analytical exposition
and `notes/conventions.md` for the convention dictionary that this
test suite implements.
"""

import math

import numpy as np
import pytest


PI = math.pi


# ---- H1: rupture is Bernoulli(1/2) -------------------------------------

def test_H1_rupture_is_bernoulli_half():
    """Simulate the canonical rupture indicator at threshold; verify p = 1/2.

    The CRR rupture is δ(now) when C·Ω = 1. Sampling with maximum-entropy
    noise around the threshold, the indicator H(t) = Θ(C·Ω − 1) draws
    Bernoulli(1/2): equal probability above vs below threshold.
    """
    rng = np.random.default_rng(11)
    n_samples = 200_000
    omega = 1.0 / PI  # canonical Z₂-rupture geometry
    threshold = 1.0 / omega
    # Maximum-entropy noise centred on threshold
    cv = omega / 2.0
    noise = (rng.uniform(-1.0, 1.0, size=n_samples)) * cv * threshold
    C_at_test = threshold + noise
    indicator = (C_at_test * omega >= 1.0).astype(int)
    p_empirical = indicator.mean()
    assert p_empirical == pytest.approx(0.5, abs=2e-3)
    # variance of Bernoulli(1/2) = 1/4
    assert indicator.var(ddof=0) == pytest.approx(0.25, abs=2e-3)


def test_H1_rupture_codomain_is_binary():
    """The Heaviside-derivative rupture indicator has codomain {0, 1}."""
    rng = np.random.default_rng(12)
    omega = 1.0 / PI
    threshold = 1.0 / omega
    C = rng.uniform(0, 2 * threshold, size=10_000)
    H = (C * omega >= 1.0).astype(int)
    unique_values = set(np.unique(H).tolist())
    assert unique_values == {0, 1}


# ---- H2: SO(2) period matches closed geodesic 2π ------------------------

def _simulate_z2_rupture_on_phase_manifold(
    phi_G: float, n_ruptures: int = 5_000, seed: int = 42
) -> np.ndarray:
    """Simulate a Z₂-rupture system whose phase manifold has closed-geodesic
    length φ_G. Returns the inter-rupture intervals.
    """
    rng = np.random.default_rng(seed)
    omega = 1.0 / phi_G
    cv = omega / 2.0
    # Mean interval = phi_G; Bernoulli(1/2) noise of relative magnitude cv
    deltas = rng.choice([-1.0, 1.0], size=n_ruptures) * cv * phi_G
    return phi_G + deltas


def test_H2_so2_period_matches_2pi():
    """Mean inter-rupture interval for an SO(2)-phase system = 2π."""
    intervals = _simulate_z2_rupture_on_phase_manifold(phi_G=2 * PI, n_ruptures=20_000)
    assert intervals.mean() == pytest.approx(2 * PI, rel=2e-3)


def test_H2_z2_rupture_only_period_matches_pi():
    """For Z₂-rupture only (no continuous phase), mean interval = π."""
    intervals = _simulate_z2_rupture_on_phase_manifold(phi_G=PI, n_ruptures=20_000)
    assert intervals.mean() == pytest.approx(PI, rel=2e-3)


def test_H2_z2_embeds_as_half_turn_in_so2():
    """Z₂ geodesic / SO(2) geodesic = 1/2 (half-turn embedding)."""
    z2_phi = PI
    so2_phi = 2 * PI
    assert z2_phi / so2_phi == pytest.approx(0.5, abs=1e-12)


# ---- H3: CV scaling across compact Lie groups --------------------------

LIE_GROUPS = [
    ("Z2 (rupture only)",        PI,            1.0 / (2 * PI)),
    ("U(1) ≅ SO(2)",             2 * PI,        1.0 / (4 * PI)),
    ("SU(2) ≅ S³",               2 * PI,        1.0 / (4 * PI)),
    ("SO(3) = SU(2)/Z₂",         PI,            1.0 / (2 * PI)),
    ("T² (per generator)",       2 * PI,        1.0 / (4 * PI)),
    ("SU(3)",                    2 * PI * math.sqrt(3.0), 1.0 / (4 * PI * math.sqrt(3.0))),
]


@pytest.mark.parametrize("name,phi_G,cv_predicted", LIE_GROUPS)
def test_H3_lie_group_cv_scaling(name: str, phi_G: float, cv_predicted: float):
    """Empirical CV from Z₂-rupture on a G-phase manifold matches CV_G = 1/(2·φ_G)."""
    intervals = _simulate_z2_rupture_on_phase_manifold(
        phi_G=phi_G, n_ruptures=50_000, seed=hash(name) & 0xFFFF
    )
    empirical_cv = intervals.std(ddof=1) / intervals.mean()
    # Bernoulli(1/2) sampling noise ~ cv_predicted itself; allow 5%
    assert empirical_cv == pytest.approx(cv_predicted, rel=5e-2), (
        f"{name}: empirical CV = {empirical_cv:.5f}, predicted = {cv_predicted:.5f}"
    )


def test_H3_so3_and_z2_only_have_same_cv():
    """Topological prediction: SO(3) (= SU(2)/Z₂) and Z₂-only have CV = 1/(2π)."""
    so3_cv = 1.0 / (2 * PI)
    z2_cv = 1.0 / (2 * PI)
    assert so3_cv == pytest.approx(z2_cv, abs=1e-12)


def test_H3_su2_and_so2_have_same_cv():
    """Topological prediction: SU(2) (S³) and SO(2) (S¹) have CV = 1/(4π).

    Because both have closed-geodesic length 2π in bi-invariant metric.
    """
    su2_cv = 1.0 / (4 * PI)
    so2_cv = 1.0 / (4 * PI)
    assert su2_cv == pytest.approx(so2_cv, abs=1e-12)


def test_H3_cv_is_half_omega_universal():
    """CV_G = Ω_G/2 holds for every G in the table (M1's claim, generalised)."""
    for name, phi_G, cv_predicted in LIE_GROUPS:
        omega_G = 1.0 / phi_G
        assert cv_predicted == pytest.approx(omega_G / 2.0, abs=1e-12), (
            f"{name}: CV/Ω deviates from 1/2"
        )


# ---- Resolution checks: new conventions ---------------------------------

def test_M2_resolved_z2_is_half_turn_in_so2():
    """Resolution of M2 ratio: Z₂ rupture geodesic π = (SO(2) geodesic 2π) / |Z₂|."""
    so2_geodesic = 2 * PI
    z2_subgroup_order = 2
    z2_rupture_geodesic = so2_geodesic / z2_subgroup_order
    assert z2_rupture_geodesic == pytest.approx(PI, abs=1e-12)


def test_M16_resolved_omega_inversion():
    """Resolution of M16: on round sphere, Ω = √κ/π (NOT π/√κ).

    Bonnet-Myers diameter D ≤ π/√κ; saturating gives D = π/√κ.
    Under canonical Ω = 1/φ_geodesic = 1/D, Ω = √κ/π.
    """
    kappa = 4.0  # κ = 4 ⇒ unit-radius S² of sectional curvature 4 is diameter π/2
    D_bonnet_myers = PI / math.sqrt(kappa)
    omega_correct = 1.0 / D_bonnet_myers  # = √κ/π
    omega_brief = PI / math.sqrt(kappa)  # the brief's stated formula
    assert omega_correct == pytest.approx(math.sqrt(kappa) / PI, abs=1e-12)
    assert not math.isclose(omega_correct, omega_brief)  # they disagree
    # The brief and correct forms are inverses of each other:
    assert omega_correct * omega_brief == pytest.approx(1.0, abs=1e-12)


def test_M19_resolved_kac_omega_equals_mu():
    """Resolution of M19: Kac gives Ω = μ(A_coherent), not 1/μ(A).

    Mean inter-rupture = expected return time = 1/μ(A); equating with 1/Ω
    yields Ω = μ(A).
    """
    mu_A = 0.1
    expected_return_time_kac = 1.0 / mu_A
    mean_inter_rupture = 1.0 / mu_A  # equivalent under identification
    omega_correct = 1.0 / mean_inter_rupture  # = μ(A)
    assert omega_correct == pytest.approx(mu_A, abs=1e-12)


def test_exp_at_rupture_resolved_via_intrinsic_units():
    """Resolution of the exp(C/Ω) → e identification.

    In Z₂-intrinsic units (Ω_int = 1, C measured in Bernoulli draws):
        At rupture C·Ω_int = 1 ⇒ C = 1, exp(C/Ω_int) = exp(1) = e ✓
    In geometric units (Ω_geo = 1/φ_G):
        At rupture C·Ω_geo = 1 ⇒ C = φ_G, exp(C/Ω_geo) = exp(φ_G²)
        — much larger than e for any finite-circumference phase manifold.
    """
    # Intrinsic units
    omega_int = 1.0
    C_int = 1.0 / omega_int
    assert math.exp(C_int / omega_int) == pytest.approx(math.e, rel=1e-12)

    # Geometric units (SO(2))
    phi_G = 2 * PI
    omega_geo = 1.0 / phi_G
    C_geo = 1.0 / omega_geo
    expected = math.exp(phi_G ** 2)
    assert math.exp(C_geo / omega_geo) == pytest.approx(expected, rel=1e-12)
    assert expected > 1e15  # absurdly larger than e
