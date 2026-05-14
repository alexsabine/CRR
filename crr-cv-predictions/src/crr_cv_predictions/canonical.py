"""Canonical CRR CV constants.

The single formula is:

    CV_G = 1 / (2 * phi_G)

where phi_G is the bi-invariant closed-geodesic length of the
phase manifold G. Special cases (Z2, SO(2)) reproduce the paper's
1/(2π) and 1/(4π) predictions.

For the Z_n discrete-phase case the package records both the paper's
extrapolation (CV = 1/(nπ)) and the M15 discrete-phase derivation
(CV = n/(4π)); these agree at n=2 only.
"""

from __future__ import annotations

import math
from typing import Iterable

PI = math.pi
TAU = 2.0 * math.pi
SQRT3 = math.sqrt(3.0)
SQRT5 = math.sqrt(5.0)
PHI_GOLDEN = (1.0 + SQRT5) / 2.0


# Closed-geodesic length phi_G for canonical compact connected Lie
# groups in bi-invariant metric, normalised by smallest-orbit length.
#
# Three distinct Z2 readings — see docs/memoryless_pure_z2.md.
#
#   "Z2"          — Z2 rupture WITH an implicit SO(2) regulator in the
#                   causal chain. This is what every "Z2" entry in the
#                   132-system table actually is (heart valve on cardiac
#                   electrical cycle; neuron spike on membrane potential
#                   oscillation; light switch on rocker arc; …).
#                   φ_G = π. CV = 1/(2π) ≈ 0.1592.
#   "Z2_only"     — Pure Z2 rupture with NO SO(2) regulator anywhere in
#                   the causal chain. The truly memoryless case. CV = 1
#                   (the exponential distribution). Derived from
#                   CV_Z2 × C*_absent_SO(2) = (1/2π) × 2π = 1.
#                   See Sabine 2026 "The Geometric Origin of Memoryless
#                   Variability" (radioactive_crr_finding_2.pdf).
#                   φ_G = 1/2 by convention so that CV = 1.
#   "Z2_on_SO2"   — Explicit alias for "Z2"; introduced so callers can
#                   make the implicit substrate visible when they want.
PHI_G: dict[str, float] = {
    # discrete rupture topology (no continuous-phase content)
    "Z2": PI,
    "Z2_on_SO2": PI,           # explicit alias — same as "Z2"
    "Z2_only": 0.5,            # pure memoryless: CV = 1/(2 * 0.5) = 1.0
    # continuous phase manifolds — canonical CRR brief
    "SO(2)": TAU,
    "U(1)": TAU,
    # M22 — already in claims/M22_lie_group_cv_generalisation
    "SU(2)": TAU,
    "SO(3)": PI,
    "T2": TAU,        # per generator; full T^n is product
    "SU(3)": TAU * SQRT3,
    # Lie-group extensions added by this package
    "SO(4)": PI,            # SO(4) ≅ (SU(2)×SU(2))/Z2; minimal closed geodesic is π
    "U(2)": TAU,            # U(2) ≅ (SU(2)×U(1))/Z2; SU(2) factor sets minimal cycle
    "SU(4)": TAU * 2.0,     # closed geodesic in canonical SU(N) normalisation
    "Sp(2)": TAU * 2.0,     # Sp(2) ≅ Spin(5) — quaternionic, geodesic 2·2π
    "G2": TAU * 2.0 * SQRT3 / 3.0,   # exceptional G2; Killing-form derived
    "Spin(7)": TAU * SQRT3,
    "T3": TAU,              # per generator
    "T4": TAU,              # per generator
    # Z_n discrete phases (under the M15 discrete-phase reading)
    "Z3": TAU / 3.0,
    "Z4": TAU / 4.0,
    "Z5": TAU / 5.0,
    "Z6": TAU / 6.0,
    # Golden-ratio rotation (anyonic / quasicrystalline)
    "PHI": PI * PHI_GOLDEN,
}


OMEGA_GEO: dict[str, float] = {k: 1.0 / v for k, v in PHI_G.items()}
CV_PRED: dict[str, float] = {k: 1.0 / (2.0 * v) for k, v in PHI_G.items()}


def phi_g(symmetry: str) -> float:
    """Look up the bi-invariant closed-geodesic length for a symmetry label."""
    if symmetry not in PHI_G:
        raise KeyError(
            f"unknown symmetry {symmetry!r}; known: {sorted(PHI_G)}"
        )
    return PHI_G[symmetry]


def omega_canonical(symmetry: str) -> float:
    """Geometric Ω = 1/φ_G (convention C4)."""
    return 1.0 / phi_g(symmetry)


def cv_canonical(symmetry: str) -> float:
    """Canonical CRR CV = 1/(2·φ_G) (M22 generalisation; M1 specialisation)."""
    return 1.0 / (2.0 * phi_g(symmetry))


def cv_zn_paper(n: int) -> float:
    """Paper's Z_n extrapolation: CV = 1/(n·π).

    Equals the M15 discrete-phase value at n=2 only (1/(2π) ≈ 0.1592).
    For n=3 the paper gives 1/(3π) ≈ 0.1061 while M15 gives 3/(4π) ≈ 0.2387.
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    return 1.0 / (n * PI)


def cv_zn_discrete_phase(n: int) -> float:
    """M15 discrete-phase derivation: CV = n/(4π).

    Uses φ_{Z_n} = 2π/n (distance between adjacent discrete points)
    and CV = Ω/2 with Ω = 1/φ.
    """
    if n < 2:
        raise ValueError("n must be >= 2")
    return n / (4.0 * PI)


def acceptance_band(cv_pred: float, lo: float = 0.6, hi: float = 1.3) -> tuple[float, float]:
    """Paper's acceptance band [0.6×, 1.3×] of cv_pred."""
    return (lo * cv_pred, hi * cv_pred)


def cv_pure_z2_memoryless() -> float:
    """CV for a Z₂ rupture with NO SO(2) regulator anywhere in the causal chain.

    Derivation (Sabine 2026, "The Geometric Origin of Memoryless Variability"):

        CV_pure_Z₂ = CV_Z₂_on_SO(2) × C*_absent_SO(2)
                  = (1 / (2π)) × (2π)
                  = 1

    The Z₂ rupture's baseline variability gets multiplied by the geodesic
    extent of the absent SO(2) substrate (its missing circumference).
    The result is the exponential distribution's CV — the unique
    continuous memoryless distribution's signature.

    The reverse product is asymmetric: CV_SO(2) × C*_Z₂ = 1/(4π) × π =
    1/4 ≠ 1. Only Z₂ × SO(2) returns unity. This is physically correct:
    a Z₂ requires an SO(2) for regulation, not the reverse.
    """
    return 1.0


def cv_inflation_factor(present: str, absent: str) -> float:
    """Inflation of CV(present) when the regulator (absent) is removed.

    Returns C*_absent (the geodesic extent of the missing substrate).

    Examples:
        cv_inflation_factor("Z2", "SO(2)") = 2π    → CV(Z₂) × 2π = 1
        cv_inflation_factor("SO(2)", "Z2") = π     → CV(SO(2)) × π = 1/4
    """
    # C* = 1/Ω = phi_G in the canonical normalisation
    return phi_g(absent)


def verdict_from_ratio(ratio: float, lo: float = 0.6, hi: float = 1.3) -> str:
    """MATCH if lo <= ratio <= hi; SUPPRESSED if below; ELEVATED if above."""
    if ratio < lo:
        return "SUPPRESSED"
    if ratio > hi:
        return "ELEVATED"
    return "MATCH"


def topological_ratios(symmetries: Iterable[str]) -> dict[tuple[str, str], float]:
    """All pairwise CV ratios for a set of symmetries.

    The canonical M2 prediction is CV(Z2)/CV(SO(2)) = 2 exactly
    (Bernoulli diameter π / circle circumference 2π = 1/2).
    """
    syms = list(symmetries)
    out: dict[tuple[str, str], float] = {}
    for a in syms:
        for b in syms:
            if a == b:
                continue
            out[(a, b)] = cv_canonical(a) / cv_canonical(b)
    return out
