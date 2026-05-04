"""M10-α³ v2 — mean-residual with leading-Bethe rescaling.

Pre-registration: claims/M10_fine_structure_fixed_point/prediction_v2.md
Pre-reg locked at git commit 102fedc.

Statistic:
    B(system) = (ν_L × n³) / (Z⁴ × Ry × log(1/(Zα)²))

Pre-registered conditions:
1. Intra-system spread (max−min)/mean < 0.20
2. |⟨B⟩ − (8/3π)·α³| < 0.30 × (8/3π)·α³  (within ±30%)
3. ⟨B⟩ > 0

All three met ⇒ M10-α³ promotes to T3.
"""

from __future__ import annotations

import math
import sys

import numpy as np


# Constants (CODATA 2018)
ALPHA = 7.2973525693e-3
ALPHA_CUBED = ALPHA ** 3
RYDBERG_FREQ_HZ = 3.2898419602508e15
RYDBERG_FREQ_MHZ = RYDBERG_FREQ_HZ / 1e6
BETHE_PREFACTOR = 8.0 / (3.0 * math.pi)

# Hydrogenic 2S Lamb shifts (MHz, CODATA-grade)
LAMB_2S = {
    "H (Z=1)":   (1057.8446, 1, 2),
    "D (Z=1)":   (1059.2335, 1, 2),
    "He+ (Z=2)": (14040.2,    2, 2),
}


def main() -> int:
    print("M10-α³ v2 — mean-residual Bethe-rescaling test")
    print("Pre-registration locked at git commit 102fedc")
    print()
    print(f"α³                  = {ALPHA_CUBED:.4e}")
    print(f"(8/3π) × α³ target  = {BETHE_PREFACTOR * ALPHA_CUBED:.4e}")
    print(f"Predicted band:      ±30% of target")
    print(f"Intra-system spread: < 0.20")
    print()

    print(f"{'System':<12} {'ν_L (MHz)':<14} {'log(1/(Zα)²)':<14} {'B(system)':<14}")
    Bs = []
    for system, (lamb, Z, n) in LAMB_2S.items():
        log_term = math.log(1.0 / (Z * ALPHA) ** 2)
        B = (lamb * n ** 3) / (Z ** 4 * RYDBERG_FREQ_MHZ * log_term)
        Bs.append(B)
        print(f"{system:<12} {lamb:<14.4f} {log_term:<14.4f} {B:<14.4e}")

    Bs = np.array(Bs)
    mean_B = Bs.mean()
    spread = (Bs.max() - Bs.min()) / mean_B
    target = BETHE_PREFACTOR * ALPHA_CUBED
    deviation = abs(mean_B - target) / target

    print()
    print(f"  ⟨B⟩          = {mean_B:.4e}")
    print(f"  spread       = {spread:.4f}  ({spread*100:.1f}%)")
    print(f"  |⟨B⟩−target| = {abs(mean_B - target):.4e}")
    print(f"  rel. deviation = {deviation:.4f}  ({deviation*100:.1f}%)")
    print()

    cond_1 = spread < 0.20
    cond_2 = deviation < 0.30
    cond_3 = mean_B > 0

    print("Pre-registration check:")
    print(f"  Condition 1 (intra-system spread < 0.20):    "
          f"{'✓' if cond_1 else '✗'}  (got {spread:.4f})")
    print(f"  Condition 2 (|⟨B⟩−target|/target < 0.30):    "
          f"{'✓' if cond_2 else '✗'}  (got {deviation:.4f})")
    print(f"  Condition 3 (⟨B⟩ > 0):                       "
          f"{'✓' if cond_3 else '✗'}")
    print()

    if cond_1 and cond_2 and cond_3:
        print("RESULT: All three pre-registered conditions met.")
        print("        M10-α³ promotes to T3.")
        return 0
    else:
        print("RESULT: One or more conditions failed. M10-α³ stays at T1.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
