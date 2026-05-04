"""Canonical CRR engine.

Factored from CRR_Church_eff.html (the canonical reference engine for
Coherence-Rupture-Regeneration). The JS class CRRAgent (lines 159-190 of
the HTML) defines the operational semantics; this module reproduces those
semantics in Python with exact numeric agreement where the operations are
deterministic.

Status: Session 1 scaffolding. The engine implements only what the canonical
formulation in CAMPAIGN.md PART I specifies. No empirical fits, no domain
specialisations — those live in the per-claim consistency notebooks built
in later sessions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Literal

PI = math.pi
TAU = 2.0 * math.pi
PHI = (1.0 + math.sqrt(5.0)) / 2.0

Symmetry = Literal["Z2", "SO2", "PHI"]


def omega_canonical(symmetry: Symmetry) -> float:
    """Canonical Ω from substrate symmetry.

    Z₂ open arc:        geodesic length π,  Ω = 1/π   ≈ 0.3183
    SO(2) ring:         geodesic length 2π, Ω = 1/(2π) ≈ 0.1592
    PHI rotation:                            Ω = 1/(πφ) ≈ 0.1967
    """
    if symmetry == "Z2":
        return 1.0 / PI
    if symmetry == "SO2":
        return 1.0 / TAU
    if symmetry == "PHI":
        return 1.0 / (PI * PHI)
    raise ValueError(f"unknown symmetry {symmetry!r}")


def cv_prediction(symmetry: Symmetry) -> float:
    """CV = Ω/2 (parameter-free, derived from Bernoulli(1/2) variance of Z₂ rupture).

    Z₂:    CV = 1/(2π)  ≈ 0.1592
    SO(2): CV = 1/(4π)  ≈ 0.0796
    Ratio Z₂:SO(2) = 2 (exact).
    """
    return omega_canonical(symmetry) / 2.0


def beauty(C: float, C_star: float, omega: float) -> float:
    """B(C) = exp(C/Ω)·(C* − C). Peaks at C = C* − Ω."""
    return math.exp(C / omega) * (C_star - C)


def beauty_peak(C_star: float, omega: float) -> float:
    """Argmax of B(C) on (-∞, C*]. dB/dC = 0 ⇒ C = C* − Ω."""
    return C_star - omega


def rupture_condition(C: float, omega: float) -> bool:
    """δ(now) when C·Ω = 1 (canonical rupture equality)."""
    return math.isclose(C * omega, 1.0, rel_tol=1e-9, abs_tol=1e-12)


@dataclass
class CRRAgent:
    """Operational CRR agent.

    Mirrors the JS class CRRAgent in CRR_Church_eff.html: maintains accumulated
    coherence C, tests rupture against threshold 1/Ω, and runs an exp(C/Ω)-
    weighted regeneration over a finite memory buffer.
    """

    symmetry: Symmetry = "Z2"
    omega_scale: float = 1.0
    memory_depth: int = 64

    C: float = 0.0
    last_rupture_C: float = 0.0
    ruptures: int = 0
    since_rupture: int = 0
    in_regen: bool = False
    regen_progress: float = 0.0
    post_rupture_C: float = 0.0
    _memory: list[float] = field(default_factory=list)

    @property
    def omega(self) -> float:
        return omega_canonical(self.symmetry) * self.omega_scale

    @property
    def exp_C_over_omega(self) -> float:
        """exp(C/Ω). Clamped to match the canonical engine's Math.min(10, ...)."""
        return math.exp(min(10.0, self.C / max(1e-3, self.omega)))

    def accumulate(self, L: float, dt: float = 1.0) -> None:
        """C(t+dt) = C(t) + L·dt."""
        self.C += L * dt
        self.since_rupture += 1
        self._memory.append(self.C)
        if len(self._memory) > self.memory_depth:
            self._memory.pop(0)

    def should_rupture(self, noise: float = 0.0) -> bool:
        """Rupture when ΔC ≥ 1/Ω + ε, ε ~ Uniform(±CV·threshold)."""
        threshold = 1.0 / self.omega
        accumulated = self.C - self.last_rupture_C
        cv = self.omega / 2.0
        return accumulated >= threshold + noise * cv * threshold

    def rupture(self) -> None:
        self.last_rupture_C = self.C
        self.ruptures += 1
        self.since_rupture = 0
        self.in_regen = True
        self.regen_progress = 0.0

    def regenerate(self, phi: float = 1.0) -> float:
        """R[χ] = ∫ φ·exp(C/Ω)·Θ dτ over the buffered past."""
        if not self.in_regen:
            return self.C
        self.regen_progress = min(1.0, self.regen_progress + 0.025 * phi)
        if not self._memory:
            return self.regen_progress
        weighted_sum = 0.0
        weight_total = 0.0
        for c_past in self._memory:
            w = math.exp(min(6.0, c_past / max(1e-3, self.omega)))
            weighted_sum += c_past * w
            weight_total += w
        self.post_rupture_C = weighted_sum / weight_total if weight_total > 0 else self.C
        if self.regen_progress >= 1.0:
            self.in_regen = False
            rigidity = math.exp(-self.omega * 2.0)
            self.C = self.post_rupture_C * rigidity + self.C * (1.0 - rigidity) * 0.3
        return self.regen_progress

    def step(self, L: float, phi: float = 1.0, dt: float = 1.0, noise: float = 0.0) -> None:
        """Single integration step: accumulate, test, rupture, regenerate."""
        self.accumulate(L, dt)
        if self.should_rupture(noise):
            self.rupture()
        if self.in_regen:
            self.regenerate(phi)


def coherence_integral(L: Callable[[float], float], t: float, n_steps: int = 1000) -> float:
    """C(x,t) = ∫₀ᵗ L(x,τ) dτ via composite trapezoid."""
    if n_steps <= 0 or t <= 0:
        return 0.0
    h = t / n_steps
    total = 0.5 * (L(0.0) + L(t))
    for i in range(1, n_steps):
        total += L(i * h)
    return total * h


def regeneration_integral(
    phi: Callable[[float], float],
    C_of_tau: Callable[[float], float],
    omega: float,
    t: float,
    t_min: float = -10.0,
    n_steps: int = 1000,
) -> float:
    """R[χ](t) = ∫₋∞ᵗ φ(τ)·exp(C(τ)/Ω)·Θ(t−τ) dτ.

    Heaviside Θ(t−τ) = 1 for τ ≤ t. We truncate the lower bound at t_min.
    """
    span = t - t_min
    if span <= 0 or n_steps <= 0:
        return 0.0
    h = span / n_steps

    def integrand(tau: float) -> float:
        return phi(tau) * math.exp(C_of_tau(tau) / omega)

    total = 0.5 * (integrand(t_min) + integrand(t))
    for i in range(1, n_steps):
        total += integrand(t_min + i * h)
    return total * h


def fourier_limit_kernel(k: float, tau: float) -> complex:
    """The trivial CRR limit: C(τ)=τ, Ω=i/k, no Θ ⇒ exp(−ikτ).

    Verifying the M6 claim that the Fourier kernel is recovered when:
      C(τ) = τ              (linear coherence accumulation)
      Ω    = i/k            (imaginary precision parameter)
      Θ    absent           (no causal cut)
    Then exp(C/Ω) = exp(τ / (i/k)) = exp(−ikτ).
    """
    return complex(math.cos(-k * tau), math.sin(-k * tau))
