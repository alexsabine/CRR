"""Pytest coverage for the canonical CRR engine.

These tests verify only operational correctness — that the engine
implements the canonical formulation as specified in CAMPAIGN.md PART I.
They are NOT empirical-consistency tests. Those live in claims/<id>/
consistency.md per the campaign structure.
"""

import math

import pytest

from index import (  # type: ignore[import-not-found]
    PHI,
    PI,
    TAU,
    CRRAgent,
    beauty,
    beauty_peak,
    coherence_integral,
    cv_prediction,
    fourier_limit_kernel,
    omega_canonical,
    regeneration_integral,
    rupture_condition,
)


# ---- canonical Ω values --------------------------------------------------

def test_omega_canonical_z2():
    assert omega_canonical("Z2") == pytest.approx(1.0 / PI)
    assert omega_canonical("Z2") == pytest.approx(0.3183098861837907)


def test_omega_canonical_so2():
    assert omega_canonical("SO2") == pytest.approx(1.0 / TAU)
    assert omega_canonical("SO2") == pytest.approx(0.15915494309189535)


def test_omega_canonical_phi():
    assert omega_canonical("PHI") == pytest.approx(1.0 / (PI * PHI))


def test_topological_ratio_exactly_two():
    """M2: Z₂:SO(2) Ω-ratio is exactly 2."""
    ratio = omega_canonical("Z2") / omega_canonical("SO2")
    assert ratio == pytest.approx(2.0, abs=1e-12)


# ---- CV = Ω/2 prediction -------------------------------------------------

def test_cv_z2():
    assert cv_prediction("Z2") == pytest.approx(1.0 / TAU)


def test_cv_so2():
    assert cv_prediction("SO2") == pytest.approx(1.0 / (4.0 * PI))


def test_cv_ratio_exactly_two():
    """M1+M2: CV ratio matches Ω ratio (both exactly 2)."""
    assert cv_prediction("Z2") / cv_prediction("SO2") == pytest.approx(2.0, abs=1e-12)


# ---- rupture condition C·Ω = 1 ------------------------------------------

def test_rupture_at_unity():
    omega = omega_canonical("Z2")
    C_critical = 1.0 / omega
    assert rupture_condition(C_critical, omega)


def test_rupture_not_below_unity():
    omega = omega_canonical("SO2")
    C_below = 0.5 / omega
    assert not rupture_condition(C_below, omega)


def test_exp_kernel_at_rupture_for_unit_omega():
    """exp(C/Ω) = e exactly when C/Ω = 1.

    The canonical brief asserts: 'At C·Ω = 1, exp(C/Ω) → e.' But C·Ω = 1
    gives C = 1/Ω, so C/Ω = 1/Ω², and exp(C/Ω) = exp(1/Ω²) — which equals e
    only when Ω = 1 (not for the canonical Ω = 1/π or Ω = 1/(2π)).

    The two conditions C·Ω = 1 and C/Ω = 1 coincide only at Ω = 1. This
    test asserts the latter, which is the only condition under which the
    'exp → e' identity holds. The apparent identification of the two
    conditions in the canonical brief is recorded as a finding in
    notes/relabellings.md and claims/M3*/claim.md.
    """
    omega = 1.0
    C_critical = 1.0 / omega  # equals omega here; both conditions met
    assert math.exp(C_critical / omega) == pytest.approx(math.e)


def test_brief_exp_e_inconsistent_with_canonical_omega():
    """Negative test documenting the discrepancy.

    Under the canonical Z₂ Ω = 1/π, applying C·Ω = 1 gives exp(C/Ω) = e^{π²},
    not e. We assert this explicitly so any future reader is forced to the
    finding rather than away from it.
    """
    omega = omega_canonical("Z2")
    C_critical = 1.0 / omega
    assert math.exp(C_critical / omega) == pytest.approx(math.exp(PI ** 2))
    assert math.exp(C_critical / omega) > 19000  # ≈ 19333.69, not e


# ---- beauty function -----------------------------------------------------

def test_beauty_peak_location():
    """M12: B(C) = exp(C/Ω)(C* − C) attains max at C = C* − Ω."""
    omega = 0.5
    C_star = 3.0
    expected = beauty_peak(C_star, omega)
    assert expected == pytest.approx(C_star - omega)
    # numerical check: B'(C* − Ω) ≈ 0
    h = 1e-6
    derivative = (beauty(expected + h, C_star, omega) - beauty(expected - h, C_star, omega)) / (2 * h)
    assert abs(derivative) < 1e-4


def test_beauty_peak_dominates_neighbors():
    omega, C_star = 0.4, 2.5
    peak_C = beauty_peak(C_star, omega)
    assert beauty(peak_C, C_star, omega) > beauty(peak_C - 0.1, C_star, omega)
    assert beauty(peak_C, C_star, omega) > beauty(peak_C + 0.1, C_star, omega)


# ---- agent operational semantics ----------------------------------------

def test_agent_initial_state():
    a = CRRAgent("Z2")
    assert a.C == 0.0
    assert a.ruptures == 0
    assert not a.in_regen


def test_agent_accumulate():
    a = CRRAgent("Z2")
    a.accumulate(1.0, dt=0.5)
    assert a.C == pytest.approx(0.5)
    assert a.since_rupture == 1


def test_agent_ruptures_when_threshold_crossed():
    a = CRRAgent("Z2")
    threshold = 1.0 / a.omega  # ≈ π
    a.accumulate(threshold + 0.01, dt=1.0)
    assert a.should_rupture(noise=0.0)
    a.rupture()
    assert a.ruptures == 1
    assert a.in_regen
    assert a.last_rupture_C == pytest.approx(threshold + 0.01)


def test_agent_step_drives_ruptures():
    a = CRRAgent("Z2")
    for _ in range(20):
        a.step(L=1.0, phi=1.0, dt=1.0, noise=0.0)
    assert a.ruptures >= 1


# ---- coherence and regeneration integrals -------------------------------

def test_coherence_integral_constant_L():
    """C(t) = ∫₀ᵗ 1 dτ = t."""
    assert coherence_integral(lambda tau: 1.0, t=2.5, n_steps=500) == pytest.approx(2.5, rel=1e-6)


def test_coherence_integral_linear_L():
    """C(t) = ∫₀ᵗ τ dτ = t²/2."""
    assert coherence_integral(lambda tau: tau, t=3.0, n_steps=2000) == pytest.approx(4.5, rel=1e-4)


def test_regeneration_integral_decays_with_omega():
    """Larger Ω → smaller exp(C/Ω) weighting → smaller integral when C>0."""
    big_omega = regeneration_integral(
        phi=lambda t: 1.0, C_of_tau=lambda t: 1.0, omega=10.0, t=0.0, t_min=-1.0, n_steps=200
    )
    small_omega = regeneration_integral(
        phi=lambda t: 1.0, C_of_tau=lambda t: 1.0, omega=0.5, t=0.0, t_min=-1.0, n_steps=200
    )
    assert small_omega > big_omega


# ---- Fourier limit (M6) -------------------------------------------------

def test_fourier_limit_kernel_modulus():
    for k in (1.0, 2.0, 5.0):
        for tau in (0.0, 0.5, 1.7):
            z = fourier_limit_kernel(k, tau)
            assert abs(z) == pytest.approx(1.0, abs=1e-12)


def test_fourier_limit_kernel_phase_at_tau_zero():
    assert fourier_limit_kernel(3.0, 0.0) == pytest.approx(complex(1.0, 0.0))


# ---- structural constants ------------------------------------------------

def test_phi_satisfies_recurrence():
    """M7 sanity: φ² = φ + 1."""
    assert PHI * PHI == pytest.approx(PHI + 1.0)


def test_z2_so2_topological_ratio_in_engine():
    """The 2:1 ratio is structural, not parameterised."""
    assert math.isclose(omega_canonical("Z2") / omega_canonical("SO2"), 2.0)
