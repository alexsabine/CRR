"""M10-α³ — Lamb-shift residual dispersion test.

Pre-registration: claims/M10_fine_structure_fixed_point/prediction.md
Pre-reg locked at git commit 3fc9681.

Sandbox-runnable. Uses CODATA-grade Lamb-shift values for the
hydrogenic isoelectronic sequence. Tests whether the CV (std/mean)
of Z⁴-rescaled Lamb shifts across H, D, He+ matches α³.

Pre-registered prediction:
    |CV_residual − α³| < 0.5 · α³
where α³ ≈ 3.89 × 10⁻⁷.
"""

from __future__ import annotations

import math
import sys

import numpy as np


# Fundamental constants (CODATA 2018 values)
ALPHA = 7.2973525693e-3                  # fine-structure constant
ALPHA_CUBED = ALPHA ** 3                  # ≈ 3.890 × 10⁻⁷
RYDBERG_FREQ_HZ = 3.2898419602508e15      # Rydberg frequency (Hz)
RYDBERG_FREQ_MHZ = RYDBERG_FREQ_HZ / 1e6  # in MHz

# Hydrogenic 2S Lamb shifts (n=2, 2S_{1/2} − 2P_{1/2}), in MHz, CODATA-grade
# Sources: CODATA 2018; Hessels et al. 2019; Beyer et al. 2017
LAMB_SHIFTS_2S_MHZ = {
    "H (Z=1)":   (1057.8446, 1),    # H 2S Lamb shift
    "D (Z=1)":   (1059.2335, 1),    # D 2S (nuclear-mass-shifted)
    "He+ (Z=2)": (14040.2,    2),    # He+ 2S Lamb shift
    # Higher-Z hydrogenic data exists but with larger uncertainties:
    # "Li2+":   ~62737 MHz, but extrapolated; not used in primary test
    # "Be3+":   ~178000 MHz, theoretical; not used
}


def main() -> int:
    print("M10-α³ — Lamb-shift residual dispersion test")
    print("Pre-registration locked at git commit 3fc9681")
    print()
    print(f"α        = {ALPHA:.10e}")
    print(f"α³       = {ALPHA_CUBED:.10e}")
    print(f"Predicted: CV_residual ≈ α³, tolerance 0.5·α³")
    print()

    # Z⁴-rescaling: divide by Z⁴ × Rydberg frequency
    print(f"{'System':<12} {'Lamb (MHz)':<15} {'Z⁴ × Ry (MHz)':<18} {'Residual':<14}")
    residuals = []
    for system, (lamb, Z) in LAMB_SHIFTS_2S_MHZ.items():
        scale = (Z ** 4) * RYDBERG_FREQ_MHZ
        residual = lamb / scale
        residuals.append(residual)
        print(f"{system:<12} {lamb:<15.4f} {scale:<18.4e} {residual:<14.4e}")

    residuals = np.array(residuals)
    mean_r = residuals.mean()
    std_r = residuals.std(ddof=1)
    cv_r = std_r / mean_r

    print()
    print(f"Residual statistics:")
    print(f"  mean = {mean_r:.4e}")
    print(f"  std  = {std_r:.4e}")
    print(f"  CV   = {cv_r:.4e}")
    print()
    print(f"Pre-registered prediction:  CV_residual ≈ α³ = {ALPHA_CUBED:.4e}")
    print(f"Pre-registered tolerance:   |CV_residual − α³| < 0.5·α³ = {0.5*ALPHA_CUBED:.4e}")
    print()

    cv_minus_alpha3 = abs(cv_r - ALPHA_CUBED)
    pre_reg_pass = cv_minus_alpha3 < 0.5 * ALPHA_CUBED
    print(f"|CV_residual − α³|         = {cv_minus_alpha3:.4e}")
    print(f"Pre-registration met?       {pre_reg_pass}")
    print()

    # Alternative reading: mean residual ≈ α³ (not CV)
    mean_minus_alpha3 = abs(mean_r - ALPHA_CUBED)
    alt_pass = mean_minus_alpha3 < 0.5 * ALPHA_CUBED
    print(f"Alternative interpretation (mean ≈ α³):")
    print(f"  mean residual = {mean_r:.4e}")
    print(f"  α³            = {ALPHA_CUBED:.4e}")
    print(f"  |mean − α³|   = {mean_minus_alpha3:.4e}, < 0.5·α³? {alt_pass}")
    print()

    if pre_reg_pass:
        print("RESULT: Pre-registration met. M10-α³ → T3.")
        return 0
    else:
        print("RESULT: Pre-registration NOT met. M10-α³ stays at T1.")
        if alt_pass:
            print("  (Alternative-reading test ['mean ≈ α³'] would have passed —")
            print("   could motivate a fresh pre-registration in a future session.)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
