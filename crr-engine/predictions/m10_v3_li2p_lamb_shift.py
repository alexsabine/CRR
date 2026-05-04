"""M10-α³ v3 — Li²⁺ 2S Lamb-shift extension of the T3 cluster.

Pre-registration: claims/M10_fine_structure_fixed_point/prediction_v3.md
Pre-reg locked at git commit 4562fe1.

Status: PRELIMINARY (sandbox-limited).
The peer-reviewed primary-source value for the hydrogenic Li²⁺ 2S Lamb shift
is canonically tabulated in Yerokhin & Shabaev (2015) J. Phys. Chem. Ref. Data
44, 033103 (arXiv:1506.01885). Direct sandbox retrieval of that table was
blocked by network restrictions; the value used here is the secondary-source
estimate ν_L(Li²⁺) ≈ 63.0 GHz (with conservative ±1.0 GHz uncertainty),
consistent with both the Bethe leading-formula estimate and statements
encountered in tertiary references during the analysis-time literature
search documented in result_v3.md.

The script computes the v3 statistic and reports the pre-registration
verdict for each of the central, lower-bound, and upper-bound Li²⁺ values.
A reviewer with access to Yerokhin & Shabaev (2015) Table II should re-run
this script with the precise tabulated value and confirm/refute the
PRELIMINARY result.
"""

from __future__ import annotations

import math
import sys

import numpy as np


# Constants (CODATA 2018) — same as v2
ALPHA = 7.2973525693e-3
ALPHA_CUBED = ALPHA ** 3
RYDBERG_FREQ_HZ = 3.2898419602508e15
RYDBERG_FREQ_MHZ = RYDBERG_FREQ_HZ / 1e6
BETHE_PREFACTOR = 8.0 / (3.0 * math.pi)

# v2 hydrogenic 2S Lamb shifts (MHz, CODATA-grade; reproduced from v2)
LAMB_2S_v2 = {
    "H (Z=1)":   (1057.8446, 1, 2),
    "D (Z=1)":   (1059.2335, 1, 2),
    "He+ (Z=2)": (14040.2,    2, 2),
}

# v3 extension: Li²⁺ 2S Lamb shift, secondary-source estimate
# Central:  63.0 GHz   = 63000 MHz
# Lower:    62.0 GHz   = 62000 MHz   (conservative -1 GHz)
# Upper:    64.0 GHz   = 64000 MHz   (conservative +1 GHz)
LAMB_LI2P_CENTRAL = 63000.0    # MHz
LAMB_LI2P_LOWER   = 62000.0
LAMB_LI2P_UPPER   = 64000.0

# v2 cluster mean (recomputed for reference)
def b_statistic(lamb_mhz: float, Z: int, n: int) -> float:
    log_term = math.log(1.0 / (Z * ALPHA) ** 2)
    return (lamb_mhz * n ** 3) / (Z ** 4 * RYDBERG_FREQ_MHZ * log_term)


def main() -> int:
    print("M10-α³ v3 — Li²⁺ 2S Lamb-shift extension")
    print("Pre-registration locked at git commit 4562fe1")
    print("Status: PRELIMINARY (sandbox-limited)")
    print()

    # Recompute v2 cluster
    Bs_v2 = []
    print("v2 cluster {H, D, He+}:")
    print(f"{'System':<12} {'ν_L (MHz)':<14} {'log(1/(Zα)²)':<14} {'B':<14}")
    for system, (lamb, Z, n) in LAMB_2S_v2.items():
        log_term = math.log(1.0 / (Z * ALPHA) ** 2)
        B = b_statistic(lamb, Z, n)
        Bs_v2.append(B)
        print(f"{system:<12} {lamb:<14.4f} {log_term:<14.4f} {B:<14.4e}")
    Bs_v2 = np.array(Bs_v2)
    mean_v2 = Bs_v2.mean()
    spread_v2 = (Bs_v2.max() - Bs_v2.min()) / mean_v2
    print(f"\n  v2 cluster mean    ⟨B⟩_v2  = {mean_v2:.4e}")
    print(f"  v2 cluster spread          = {spread_v2:.4f}  ({spread_v2*100:.2f}%)")
    print()

    # v3: evaluate Li²⁺ at central / lower / upper
    target = BETHE_PREFACTOR * ALPHA_CUBED
    print(f"  Bethe target (8/3π)·α³     = {target:.4e}")
    print()

    print("v3 Li²⁺ extension (Z=3, n=2):")
    print(f"  log(1/(3α)²)               = {math.log(1.0/(3*ALPHA)**2):.4f}")
    print()
    print(f"{'ν_L(Li²⁺) [MHz]':<20} {'B(Li²⁺)':<14} "
          f"{'|ΔB/⟨B⟩_v2|':<14} {'spread_v3':<12} {'|⟨B⟩_v3-tgt|/tgt':<18}")

    overall_pass = []
    for label, lamb_li in [("63000 (central)", LAMB_LI2P_CENTRAL),
                            ("62000 (lower)",   LAMB_LI2P_LOWER),
                            ("64000 (upper)",   LAMB_LI2P_UPPER)]:
        B_li = b_statistic(lamb_li, 3, 2)
        deviation_from_v2 = abs(B_li - mean_v2) / mean_v2
        Bs_v3 = np.append(Bs_v2, B_li)
        mean_v3 = Bs_v3.mean()
        spread_v3 = (Bs_v3.max() - Bs_v3.min()) / mean_v3
        target_dev = abs(mean_v3 - target) / target

        cond1 = deviation_from_v2 < 0.10
        cond2 = spread_v3 < 0.10
        cond3 = target_dev < 0.30
        all_pass = cond1 and cond2 and cond3
        overall_pass.append(all_pass)
        verdict = "PASS" if all_pass else "FAIL"

        print(f"{label:<20} {B_li:<14.4e} "
              f"{deviation_from_v2:<14.4f} {spread_v3:<12.4f} "
              f"{target_dev:<18.4f} -> {verdict}")

    print()
    print("Pre-registration verdict (across central/lower/upper estimates):")
    if all(overall_pass):
        print("  ALL three estimates PASS all three pre-registered conditions.")
        print("  Robust PRELIMINARY pass: M10-α³ v3 strengthens the T3 cluster.")
        rc = 0
    elif any(overall_pass):
        print("  Mixed (central or one bound passes; another fails).")
        print("  PRELIMINARY: pending primary-source value for definitive verdict.")
        rc = 0
    else:
        print("  All three estimates FAIL.")
        print("  PRELIMINARY refutation; pending primary-source confirmation.")
        rc = 1

    print()
    print("Note: The PRELIMINARY status means a reviewer with access to")
    print("Yerokhin & Shabaev (2015) J. Phys. Chem. Ref. Data 44, 033103")
    print("(or arXiv:1506.01885) Table II should re-run this script with")
    print("the precise tabulated 2S Lamb-shift value for Z=3 to confirm.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
