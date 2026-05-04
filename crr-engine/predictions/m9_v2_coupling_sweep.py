"""M9 v2 — coupling-strength sweep of Fibonacci-Hamiltonian box-dimension.

Pre-registration: claims/M9_singular_continuous_spectrum/prediction_v2.md
Pre-reg locked at git commit 102fedc.

Tests three pre-registered conditions:
1. Monotone non-increase of d_B as coupling λ grows.
2. d_B(λ=0.25) > 0.85 (weak-coupling band-limit).
3. d_B(λ=8.0) < 0.5 (strong-coupling Cantor regime).

All three met ⇒ M9 promotes to T2.
"""

from __future__ import annotations

import math
import sys

import numpy as np

PHI = (1.0 + math.sqrt(5.0)) / 2.0


def fibonacci_word(n_letters: int) -> str:
    s = "a"
    while len(s) < n_letters:
        s = s.replace("b", "Y").replace("a", "ab").replace("Y", "a")
    return s[:n_letters]


def fibonacci_hamiltonian_spectrum(N: int, lam: float) -> np.ndarray:
    """Spectrum with onsite potential ±λ/2 (so coupling = λ)."""
    word = fibonacci_word(N)
    V = np.array([+lam / 2 if c == "a" else -lam / 2 for c in word])
    H = np.diag(V) + np.diag(np.ones(N - 1), 1) + np.diag(np.ones(N - 1), -1)
    return np.sort(np.linalg.eigvalsh(H))


def box_counting_dimension(eigs: np.ndarray, n_scales: int = 10) -> float:
    """Box-counting fractal dimension with geometric scale sweep."""
    width = eigs[-1] - eigs[0]
    if width <= 0:
        return 0.0
    log_eps = []
    log_N = []
    for k in range(2, n_scales + 2):
        eps = width / (2 ** k)
        bins = np.unique(np.floor((eigs - eigs[0]) / eps).astype(int))
        log_eps.append(math.log(eps))
        log_N.append(math.log(len(bins)))
    slope, _ = np.polyfit(log_eps, log_N, 1)
    return -float(slope)


def main() -> int:
    print("M9 v2 — coupling-strength sweep")
    print("Pre-registration locked at git commit 102fedc")
    print()

    N = 1597  # F_17, matching v1
    couplings = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    dims = []
    print(f"{'λ':>6}  {'d_B (N=1597)':>14}")
    for lam in couplings:
        eigs = fibonacci_hamiltonian_spectrum(N, lam)
        d_B = box_counting_dimension(eigs)
        dims.append(d_B)
        print(f"{lam:>6.2f}  {d_B:>14.4f}")

    print()
    monotone = all(dims[i] >= dims[i + 1] - 1e-3 for i in range(len(dims) - 1))
    weak_ok = dims[0] > 0.85
    strong_ok = dims[-1] < 0.5

    print("Pre-registration check:")
    print(f"  Condition 1 (monotone non-increase): "
          f"{'✓' if monotone else '✗'}")
    print(f"  Condition 2 (d_B at λ=0.25 > 0.85):  "
          f"{'✓' if weak_ok else '✗'}  (got {dims[0]:.4f})")
    print(f"  Condition 3 (d_B at λ=8.0 < 0.5):    "
          f"{'✓' if strong_ok else '✗'}  (got {dims[-1]:.4f})")
    print()

    if monotone and weak_ok and strong_ok:
        print("RESULT: All three pre-registered conditions met.")
        print("        M9 promotes to T2 (Sütő-class consistency).")
        return 0
    else:
        print("RESULT: One or more conditions failed. M9 stays at T1.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
